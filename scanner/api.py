"""
OpenDocket API Server.

Flask backend that powers live scanning from the web.
"""

import os
import re
import sys
import time
import threading
from collections import defaultdict, deque
from datetime import datetime, timedelta

from flask import Flask, jsonify, request
from flask_cors import CORS

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.database import (
    init_db, create_scan, update_scan_status, save_findings,
    get_scan, delete_scan, get_stats, increment_stat, add_to_waitlist,
    get_directory_with_scores, get_recent_scans, get_recent_scan,
    track_event, get_event_counts, record_evidence_patterns,
    record_question_accuracy, store_remediation,
    save_feedback, get_feedback_for_scan, get_feedback_stats,
    record_visitor, get_visitor_stats, get_discovered_patterns,
)
from scanner.repo_fetcher import fetch_and_qualify, cleanup_repo
from scanner.domain_detector import detect_domains
from scanner.compliance_mapper import map_frameworks
from scanner.report_generator import (
    generate_html_report, generate_markdown_report,
    generate_failed_gate_html, calculate_score,
)
from scanner.agents.hipaa_agent import HIPAAAgent
from scanner.agents.soc2_agent import SOC2Agent
from scanner.agents.pci_dss_agent import PCIDSSAgent
from scanner.agents.gdpr_agent import GDPRAgent
from scanner.agents.tcpa_agent import TCPAAgent
from scanner.agents.sox_agent import SOXAgent
from scanner.agents.ccpa_agent import CCPAAgent
from scanner.agents.coppa_agent import COPPAAgent
from scanner.agents.ferpa_agent import FERPAAgent
from scanner.agents.glba_agent import GLBAAgent

AGENTS = {
    "hipaa": HIPAAAgent,
    "soc2": SOC2Agent,
    "pci_dss": PCIDSSAgent,
    "gdpr": GDPRAgent,
    "tcpa": TCPAAgent,
    "sox": SOXAgent,
    "ccpa": CCPAAgent,
    "coppa": COPPAAgent,
    "ferpa": FERPAAgent,
    "glba": GLBAAgent,
}

# ── Scan cancellation flags and params for restart ──
_cancel_flags: dict[str, threading.Event] = {}
_scan_params: dict[str, dict] = {}

# ── Scan log ring buffers (last 200 lines per scan) ──
_scan_logs: dict[str, deque] = {}
_LOG_MAX = 200


def _log(scan_id: str, message: str):
    """Append a timestamped log line for a scan."""
    if scan_id not in _scan_logs:
        _scan_logs[scan_id] = deque(maxlen=_LOG_MAX)
    ts = datetime.utcnow().strftime("%H:%M:%S")
    _scan_logs[scan_id].append(f"[{ts}] {message}")


app = Flask(__name__, static_folder="../docs", static_url_path="")
CORS(app, origins=[
    "https://anurag-mohanty.github.io",
    "https://opendocket.dev",
    "http://localhost:3000",
    "http://localhost:5000",
    "http://localhost:8080",
    "null",
])


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


# Rate limiting
_rate_limits: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT = 3
RATE_WINDOW = 3600  # 1 hour

# Daily/monthly cost protection
DAILY_SCAN_LIMIT = int(os.environ.get("DAILY_SCAN_LIMIT", 200))
MONTHLY_SCAN_LIMIT = int(os.environ.get("MONTHLY_SCAN_LIMIT", 2000))

GITHUB_URL_RE = re.compile(r"^https://github\.com/[\w.\-]+/[\w.\-]+/?$")


def _check_rate_limit(ip: str) -> bool:
    """Returns True if request is allowed."""
    now = time.time()
    _rate_limits[ip] = [t for t in _rate_limits[ip] if now - t < RATE_WINDOW]
    if len(_rate_limits[ip]) >= RATE_LIMIT:
        return False
    _rate_limits[ip].append(now)
    return True


def _check_global_limits() -> str | None:
    """Check daily/monthly scan limits. Returns error message or None."""
    stats = get_stats()
    today = stats.get("scans_today", 0)
    month = stats.get("scans_this_month", 0)
    if today >= DAILY_SCAN_LIMIT:
        return f"Daily scan limit reached ({DAILY_SCAN_LIMIT}). Bring your own Anthropic API key to continue scanning without limits."
    if month >= MONTHLY_SCAN_LIMIT:
        return f"Monthly scan limit reached ({MONTHLY_SCAN_LIMIT}). Bring your own Anthropic API key to continue scanning without limits."
    return None


def _extract_repo_name(url: str) -> str:
    """Extract owner/repo from GitHub URL."""
    parts = url.rstrip("/").split("/")
    return f"{parts[-2]}/{parts[-1]}"


def _run_scan(scan_id: str, repo_url: str, api_key: str | None = None, gemini_key: str | None = None):
    """Execute a full scan in a background thread."""
    start_time = time.time()
    old_key = os.environ.get("ANTHROPIC_API_KEY")
    old_gemini = os.environ.get("GEMINI_API_KEY")
    cancel = _cancel_flags.get(scan_id)

    def _cancelled():
        return cancel and cancel.is_set()

    try:
        if api_key:
            os.environ["ANTHROPIC_API_KEY"] = api_key
        if gemini_key:
            os.environ["GEMINI_API_KEY"] = gemini_key

        import json as _json

        def _prog(step, detail="", fw_done=None, fw_total=None, fw_current=""):
            """Build structured progress string."""
            p = {"step": step, "detail": detail}
            if fw_done is not None:
                p["fw_done"] = fw_done
                p["fw_total"] = fw_total
                p["fw_current"] = fw_current
            return _json.dumps(p)

        _log(scan_id, f"Scan started for {repo_url}")
        update_scan_status(scan_id, "running", _prog("clone", "Cloning repository"))
        _log(scan_id, "Cloning repository...")
        repo_ctx = fetch_and_qualify(repo_url)
        _log(scan_id, f"Clone complete — {len(repo_ctx.file_index)} files indexed")

        if _cancelled():
            raise InterruptedError("Scan cancelled by user")

        try:
            update_scan_status(scan_id, "running", _prog("qualify", "Running qualification gates"))
            _log(scan_id, "Running qualification gates...")
            if not repo_ctx.qualification.qualified:
                _log(scan_id, f"Did not qualify: {'; '.join(repo_ctx.qualification.reasons)}")
                update_scan_status(
                    scan_id, "complete",
                    progress=_prog("qualify", "Repository did not qualify"),
                    error_message="; ".join(repo_ctx.qualification.reasons),
                    scan_duration_seconds=time.time() - start_time,
                )
                report = generate_failed_gate_html(
                    repo_ctx.name, repo_url,
                    repo_ctx.qualification.reasons,
                    repo_ctx.qualification.stats,
                )
                report_path = os.path.join("docs", "reports", f"{repo_ctx.name}_report.html")
                os.makedirs(os.path.dirname(report_path), exist_ok=True)
                with open(report_path, "w") as f:
                    f.write(report)
                update_scan_status(scan_id, "complete", report_url=f"/reports/{repo_ctx.name}_report.html")
                increment_stat("total_scans")
                increment_stat("scans_today")
                increment_stat("scans_this_month")
                return

            _log(scan_id, "Qualification passed")

            if _cancelled():
                raise InterruptedError("Scan cancelled by user")

            update_scan_status(scan_id, "running", _prog("domain", "Detecting domains and frameworks"))
            _log(scan_id, "Detecting domains...")
            domains = detect_domains(repo_ctx.path)
            _log(scan_id, f"Domains detected: {', '.join(d.domain for d in domains)}")

            update_scan_status(
                scan_id, "running", _prog("domain", "Mapping frameworks"),
                domains_detected=[{"domain": d.domain, "confidence": d.confidence} for d in domains],
                files_scanned=len(repo_ctx.file_index),
            )

            frameworks = map_frameworks(domains)
            if not frameworks:
                frameworks = ["soc2"]
            _log(scan_id, f"Frameworks triggered: {', '.join(f.upper() for f in frameworks)}")

            # Log what the system learned from previous scans
            try:
                from scanner.database import _get_conn as _gc
                with _gc() as _conn:
                    corpus_size = _conn.execute("SELECT COUNT(*) as c FROM evidence_patterns").fetchone()
                    qa_size = _conn.execute("SELECT COUNT(*) as c FROM question_accuracy").fetchone()
                    disc_size = _conn.execute("SELECT COUNT(*) as c FROM discovered_patterns").fetchone()
                if corpus_size and corpus_size["c"] > 0:
                    _log(scan_id, f"--- Intelligence from previous scans ---")
                    _log(scan_id, f"  [CORPUS] {corpus_size['c']} evidence patterns guiding search priority")
                    _log(scan_id, f"  [ACCURACY] {qa_size['c']} question accuracy records for confidence context")
                    if disc_size and disc_size["c"] > 0:
                        _log(scan_id, f"  [DISCOVERY] {disc_size['c']} novel patterns added to question library from past scans")
            except Exception:
                pass

            if _cancelled():
                raise InterruptedError("Scan cancelled by user")

            update_scan_status(
                scan_id, "running",
                progress=_prog("scan", f"Starting {len(frameworks)} frameworks", 0, len(frameworks)),
                frameworks_triggered=frameworks,
            )

            agent_results = []
            fw_complete = []
            fw_lock = threading.Lock()

            def _run_agent(fw, idx):
                """Run a single framework agent (called from thread pool)."""
                if _cancelled():
                    return None
                agent_class = AGENTS.get(fw)
                if not agent_class:
                    return None
                agent = agent_class()
                agent._repo_name = repo_ctx.name
                # Log learned questions
                discovered = [q for q in agent.questions if q.get("category", "").startswith("[Discovered]")]
                if discovered:
                    _log(scan_id, f"Running {fw.upper()} agent ({idx+1}/{len(frameworks)}) — {len(agent.questions)} questions ({len(discovered)} learned from previous scans)")
                    for dq in discovered:
                        _log(scan_id, f"    [LEARNED] {dq['id']}: {dq['category']}")
                else:
                    _log(scan_id, f"Running {fw.upper()} agent ({idx+1}/{len(frameworks)}) — {len(agent.questions)} questions")
                result = agent.scan(repo_ctx.path, repo_ctx.file_index, repo_ctx.readme_content)
                finding_count = len(result.findings)
                with fw_lock:
                    fw_complete.append(fw.upper())
                    update_scan_status(
                        scan_id, "running",
                        progress=_prog("scan", f"{fw.upper()} complete", len(fw_complete), len(frameworks), fw.upper()),
                    )
                corpus_info = ""
                if result.corpus_questions_boosted:
                    corpus_info = f" | corpus: {result.corpus_questions_boosted} questions search-boosted, {result.corpus_prioritized_files} files prioritized"
                _log(scan_id, f"  {fw.upper()} complete — {finding_count} findings ({len(fw_complete)}/{len(frameworks)}){corpus_info}")
                return result

            from concurrent.futures import ThreadPoolExecutor, as_completed
            max_agents = min(3, len(frameworks))
            _log(scan_id, f"Running {len(frameworks)} framework agents ({max_agents} concurrent)...")
            with ThreadPoolExecutor(max_workers=max_agents) as executor:
                futures = {
                    executor.submit(_run_agent, fw, i): fw
                    for i, fw in enumerate(frameworks)
                }
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        agent_results.append(result)

            if _cancelled():
                raise InterruptedError("Scan cancelled by user")

            # Independent review pass (Gemini)
            g_key = gemini_key or os.environ.get("GEMINI_API_KEY")
            total_findings = sum(len(r.findings) for r in agent_results)
            if g_key:
                _log(scan_id, f"Starting Gemini independent review ({total_findings} findings, 5 concurrent workers)...")
                update_scan_status(scan_id, "running", _prog("judge", "Running Gemini independent review"))
                try:
                    from scanner.agents.base_agent import JudgeAgent
                    judge = JudgeAgent(g_key)
                    repo_ctx_dict = {
                        "repo_name": repo_ctx.name,
                        "domains": ", ".join(d.domain for d in domains),
                    }

                    def _judge_progress(done, total, qid):
                        _log(scan_id, f"  Gemini reviewed {qid} ({done}/{total})")
                        update_scan_status(
                            scan_id, "running",
                            _prog("judge", f"Reviewing findings ({done}/{total})",
                                  fw_done=done, fw_total=total, fw_current=qid),
                        )

                    judge.review_all(agent_results, repo_ctx_dict, progress_callback=_judge_progress)
                    _log(scan_id, "Gemini review complete")
                except Exception as e:
                    _log(scan_id, f"Gemini review failed: {e}")
                    print(f"[OpenDocket] Gemini review failed: {e}")
            else:
                _log(scan_id, "Skipping Gemini review (no API key)")
                update_scan_status(scan_id, "running", _prog("judge", "Skipping (no Gemini key)"))

            if _cancelled():
                raise InterruptedError("Scan cancelled by user")

            # Calculate stats — use confirmed counts when judge has run
            all_findings = [f for r in agent_results for f in r.findings]
            has_judge = any(f.review_verdict and f.review_verdict != "NOT REVIEWED" for f in all_findings)
            if has_judge:
                high = sum(1 for f in all_findings if f.finding_level == "High Risk" and f.review_verdict == "CONFIRMED")
                med = sum(1 for f in all_findings if f.finding_level == "Medium Risk" and f.review_verdict == "CONFIRMED")
            else:
                high = sum(1 for f in all_findings if f.finding_level == "High Risk")
                med = sum(1 for f in all_findings if f.finding_level == "Medium Risk")
            concern = sum(1 for f in all_findings if f.finding_level == "Pattern of Concern")
            ok = sum(1 for f in all_findings if f.finding_level == "No Issue Found")
            score = calculate_score(agent_results)

            # Generate reports
            _log(scan_id, "Generating reports...")
            update_scan_status(scan_id, "running", _prog("report", "Generating reports"))

            html_report = generate_html_report(repo_ctx.name, repo_url, domains, agent_results, scan_id=scan_id)
            html_path = os.path.join("docs", "reports", f"{repo_ctx.name}_report.html")
            os.makedirs(os.path.dirname(html_path), exist_ok=True)
            with open(html_path, "w") as f:
                f.write(html_report)

            md_report = generate_markdown_report(repo_ctx.name, repo_url, domains, agent_results)
            md_path = os.path.join("reports", f"{repo_ctx.name}_report.md")
            os.makedirs(os.path.dirname(md_path), exist_ok=True)
            with open(md_path, "w") as f:
                f.write(md_report)

            # Save to database
            findings_data = []
            for result in agent_results:
                for f in result.findings:
                    findings_data.append({
                        "framework": result.framework,
                        "question_id": f.question_id,
                        "severity": f.finding_level,
                        "judge_model": f.judge_model,
                        "judge_verdict": f.review_verdict,
                        "judge_reasoning": f.judge_reasoning,
                        "judge_confidence": f.judge_confidence,
                        "file_evidence_count": len(f.evidence),
                    })
            save_findings(scan_id, findings_data)

            # Record intelligence corpus — evidence patterns, accuracy, remediations
            _log(scan_id, "--- Product Improvements from this scan ---")
            domain_str = ", ".join(d.domain for d in domains)
            patterns_added = 0
            accuracy_updated = 0
            remediations_improved = 0
            novel_findings = 0
            fp_reasons_learned = 0

            for result in agent_results:
                for f in result.findings:
                    # Count novel wildcard findings
                    if f.question_id.endswith("-NOVEL") and f.finding_level != "No Issue Found":
                        novel_findings += 1
                        _log(scan_id, f"  [NEW QUESTION] {result.framework}: {f.category} — auto-added to question library")

                    if f.review_verdict and f.review_verdict not in ("NOT REVIEWED", ""):
                        try:
                            # Evidence file patterns
                            evidence_files = [e.file_path for e in f.evidence] if f.evidence else []
                            if evidence_files:
                                record_evidence_patterns(
                                    result.framework, f.question_id,
                                    evidence_files, f.review_verdict, domain_str,
                                )
                                patterns_added += len(evidence_files)

                            # Question-level accuracy with FP reasoning
                            fp_reason = ""
                            if f.review_verdict == "POSSIBLE FALSE POSITIVE" and f.judge_reasoning:
                                fp_reason = f.judge_reasoning[:200]
                                fp_reasons_learned += 1
                            record_question_accuracy(
                                result.framework, f.question_id,
                                f.review_verdict, domain_str, fp_reason,
                            )
                            accuracy_updated += 1

                            # Store improved remediations from Gemini
                            improved = getattr(f, "improved_remediation", "")
                            if improved:
                                store_remediation(
                                    result.framework, f.question_id,
                                    improved, domain_str,
                                    quality="specific", source="gemini",
                                )
                                remediations_improved += 1
                        except Exception:
                            pass  # non-critical

            _log(scan_id, f"  [CORPUS] {patterns_added} evidence file patterns recorded")
            _log(scan_id, f"  [ACCURACY] {accuracy_updated} question accuracy rates updated")
            if fp_reasons_learned:
                _log(scan_id, f"  [FP INTEL] {fp_reasons_learned} false-positive reasons learned from Gemini")
            if remediations_improved:
                _log(scan_id, f"  [REMEDIATION] {remediations_improved} remediations improved and stored for reuse")
            if novel_findings:
                _log(scan_id, f"  [DISCOVERY] {novel_findings} novel compliance questions auto-added to library")
            _log(scan_id, f"  System now has better search priority, accuracy data, and remediation quality for future scans")

            # Aggregate token usage across all agents
            total_tokens_in = sum(r.tokens_in for r in agent_results)
            total_tokens_out = sum(r.tokens_out for r in agent_results)
            total_llm_calls = sum(r.llm_calls for r in agent_results)

            duration = time.time() - start_time
            _log(scan_id, f"Scan complete — score {score}, {high} high-risk, {duration:.0f}s, {total_llm_calls} LLM calls, {total_tokens_in+total_tokens_out} tokens")
            update_scan_status(
                scan_id, "complete",
                progress="Scan complete",
                opendocket_score=score,
                finding_high=high,
                finding_medium=med,
                finding_concern=concern,
                finding_ok=ok,
                scan_duration_seconds=duration,
                tokens_in=total_tokens_in,
                tokens_out=total_tokens_out,
                llm_calls=total_llm_calls,
                report_url=f"/reports/{repo_ctx.name}_report.html",
            )

            # Update aggregate stats
            increment_stat("total_scans")
            increment_stat("scans_today")
            increment_stat("scans_this_month")
            increment_stat("total_findings", len(all_findings))
            increment_stat("high_risk_findings", high)
            increment_stat("total_lines_scanned", len(repo_ctx.file_index) * 100)  # estimate
            fp_count = sum(1 for f in all_findings if f.review_verdict == "POSSIBLE FALSE POSITIVE")
            confirmed_count = sum(1 for f in all_findings if f.review_verdict == "CONFIRMED")
            ctx_count = sum(1 for f in all_findings if f.review_verdict == "CONTEXT DEPENDENT")
            increment_stat("judge_false_positives", fp_count)
            increment_stat("judge_confirmed", confirmed_count)
            increment_stat("judge_context_dependent", ctx_count)

        finally:
            cleanup_repo(repo_ctx.path)

    except InterruptedError:
        _log(scan_id, "Scan cancelled by user")
        update_scan_status(
            scan_id, "cancelled",
            progress="Scan cancelled",
            error_message="Cancelled by user",
            scan_duration_seconds=time.time() - start_time,
        )
    except Exception as e:
        _log(scan_id, f"Scan failed: {e}")
        update_scan_status(
            scan_id, "failed",
            progress="Scan failed",
            error_message=str(e),
            scan_duration_seconds=time.time() - start_time,
        )
        increment_stat("total_scans")
        increment_stat("scans_today")
        increment_stat("scans_this_month")
    finally:
        _cancel_flags.pop(scan_id, None)
        if old_key:
            os.environ["ANTHROPIC_API_KEY"] = old_key
        elif api_key and "ANTHROPIC_API_KEY" in os.environ:
            del os.environ["ANTHROPIC_API_KEY"]
        if old_gemini:
            os.environ["GEMINI_API_KEY"] = old_gemini
        elif gemini_key and "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]


@app.route("/api/scan", methods=["POST"])
def start_scan():
    data = request.get_json(silent=True) or {}
    repo_url = data.get("repo_url", "").strip().rstrip("/")
    anthropic_key = (data.get("anthropic_api_key") or data.get("api_key", "")).strip() or None
    gemini_key = data.get("gemini_api_key", "").strip() or None

    if not repo_url:
        return jsonify({"error": "repo_url is required"}), 400

    if not GITHUB_URL_RE.match(repo_url):
        return jsonify({"error": "Invalid GitHub repository URL"}), 400

    is_byok = bool(anthropic_key)

    # Rate limit (skip for BYOK)
    if not is_byok:
        ip = request.remote_addr or "unknown"
        if not _check_rate_limit(ip):
            return jsonify({
                "error": "Rate limit exceeded. 3 scans per hour for public scans. Provide your own API key for unlimited scans."
            }), 429
        # Global cost limits
        limit_err = _check_global_limits()
        if limit_err:
            return jsonify({"error": limit_err, "byok_required": True}), 429

    repo_name = _extract_repo_name(repo_url)

    # Check for cached scan within last 24 hours
    cached = get_recent_scan(repo_name, hours=24)
    if cached and not is_byok:
        return jsonify({
            "scan_id": cached["scan_id"],
            "status": "complete",
            "cached": True,
            "message": f"Using scan from {cached.get('timestamp', 'recently')[:10]}",
            "report_url": cached.get("report_url", ""),
            "repo_name": repo_name,
            "summary": {
                "score": cached.get("opendocket_score", 0),
                "high_risk": cached.get("finding_high", 0),
                "medium_risk": cached.get("finding_medium", 0),
                "frameworks": cached.get("frameworks_triggered", []),
            },
        })

    scan_id = create_scan(repo_url, repo_name, used_byok=is_byok)

    # Set up cancellation flag
    _cancel_flags[scan_id] = threading.Event()

    # Store scan params for restart capability
    _scan_params[scan_id] = {
        "repo_url": repo_url,
        "anthropic_key": anthropic_key,
        "gemini_key": gemini_key,
    }

    thread = threading.Thread(
        target=_run_scan,
        args=(scan_id, repo_url, anthropic_key, gemini_key),
        daemon=True,
    )
    thread.start()

    return jsonify({
        "scan_id": scan_id,
        "status": "queued",
        "repo_name": repo_name,
        "byok": is_byok,
        "gemini_review": bool(gemini_key or os.environ.get("GEMINI_API_KEY")),
    })


@app.route("/api/scan/<scan_id>", methods=["GET"])
def get_scan_status(scan_id):
    scan = get_scan(scan_id)
    if not scan:
        return jsonify({"error": "Scan not found"}), 404

    import json as _json
    progress_raw = scan.get("progress", "")
    progress = {}
    try:
        progress = _json.loads(progress_raw) if progress_raw.startswith("{") else {"step": "", "detail": progress_raw}
    except Exception:
        progress = {"step": "", "detail": str(progress_raw)}

    response = {
        "scan_id": scan["scan_id"],
        "repo_name": scan["repo_name"],
        "status": scan["status"],
        "progress": progress,
    }

    if scan["status"] == "complete":
        response["report_url"] = scan.get("report_url", "")
        response["summary"] = {
            "score": scan.get("opendocket_score", 0),
            "high_risk": scan.get("finding_high", 0),
            "medium_risk": scan.get("finding_medium", 0),
            "concern": scan.get("finding_concern", 0),
            "ok": scan.get("finding_ok", 0),
            "frameworks": scan.get("frameworks_triggered", []),
            "domains": scan.get("domains_detected", []),
            "duration_seconds": scan.get("scan_duration_seconds", 0),
        }
    elif scan["status"] == "failed":
        response["error"] = scan.get("error_message", "Unknown error")
    elif scan["status"] == "cancelled":
        response["error"] = scan.get("error_message", "Cancelled by user")

    return jsonify(response)


@app.route("/api/scan/<scan_id>/stop", methods=["POST"])
def stop_scan(scan_id):
    """Cancel a running scan."""
    scan = get_scan(scan_id)
    if not scan:
        return jsonify({"error": "Scan not found"}), 404
    if scan["status"] not in ("queued", "running"):
        return jsonify({"error": f"Scan is already {scan['status']}"}), 400
    cancel = _cancel_flags.get(scan_id)
    if cancel:
        cancel.set()
        _log(scan_id, "Stop requested by user")
        return jsonify({"ok": True, "message": "Cancellation signal sent"})
    # No cancel flag means thread already finished
    return jsonify({"ok": True, "message": "Scan is no longer running"})


@app.route("/api/scan/<scan_id>/restart", methods=["POST"])
def restart_scan(scan_id):
    """Restart a cancelled or failed scan as a new scan."""
    scan = get_scan(scan_id)
    if not scan:
        return jsonify({"error": "Scan not found"}), 404
    if scan["status"] in ("queued", "running"):
        return jsonify({"error": "Scan is still running — stop it first"}), 400

    # Get original params if available, otherwise use request body
    data = request.get_json(silent=True) or {}
    params = _scan_params.get(scan_id, {})
    repo_url = params.get("repo_url") or data.get("repo_url", "").strip()
    if not repo_url:
        # Reconstruct from repo_name
        repo_name = scan.get("repo_name", "")
        if repo_name:
            repo_url = f"https://github.com/{repo_name}"
        else:
            return jsonify({"error": "Could not determine repo URL"}), 400

    anthropic_key = params.get("anthropic_key") or data.get("anthropic_api_key") or None
    gemini_key = params.get("gemini_key") or data.get("gemini_api_key") or None
    repo_name = _extract_repo_name(repo_url)

    new_scan_id = create_scan(repo_url, repo_name, used_byok=bool(anthropic_key))
    _cancel_flags[new_scan_id] = threading.Event()
    _scan_params[new_scan_id] = {
        "repo_url": repo_url,
        "anthropic_key": anthropic_key,
        "gemini_key": gemini_key,
    }

    thread = threading.Thread(
        target=_run_scan,
        args=(new_scan_id, repo_url, anthropic_key, gemini_key),
        daemon=True,
    )
    thread.start()
    _log(new_scan_id, f"Restarted from scan {scan_id[:8]}...")

    return jsonify({
        "scan_id": new_scan_id,
        "status": "queued",
        "repo_name": repo_name,
        "restarted_from": scan_id,
    })


@app.route("/api/scan/<scan_id>/logs", methods=["GET"])
def get_scan_logs(scan_id):
    """Return the log buffer for a scan."""
    logs = _scan_logs.get(scan_id, [])
    after = int(request.args.get("after", 0))
    log_list = list(logs)
    return jsonify({
        "scan_id": scan_id,
        "total": len(log_list),
        "logs": log_list[after:],
        "next_after": len(log_list),
    })


@app.route("/api/scan/<scan_id>", methods=["DELETE"])
def delete_scan_endpoint(scan_id):
    """Delete a scan, its findings, and report files."""
    scan = get_scan(scan_id)
    if not scan:
        return jsonify({"error": "Scan not found"}), 404
    if scan["status"] in ("queued", "running"):
        return jsonify({"error": "Cannot delete a running scan — stop it first"}), 400

    # Delete report files if they exist
    repo_name = scan.get("repo_name", "").replace("/", "_")
    if repo_name:
        for path in [
            os.path.join("docs", "reports", f"{repo_name}_report.html"),
            os.path.join("reports", f"{repo_name}_report.md"),
        ]:
            if os.path.exists(path):
                os.remove(path)

    # Delete from database
    delete_scan(scan_id)

    # Clean up in-memory state
    _scan_logs.pop(scan_id, None)
    _scan_params.pop(scan_id, None)

    return jsonify({"ok": True, "message": f"Scan {scan_id[:8]}... deleted"})


@app.route("/api/stats", methods=["GET"])
def api_stats():
    # Compute stats from actual scan data — the source of truth
    from scanner.database import _get_conn
    with _get_conn() as conn:
        row = conn.execute("""
            SELECT
                COUNT(*) as total_scans,
                COALESCE(SUM(finding_high), 0) as confirmed_high,
                COALESCE(SUM(finding_high + finding_medium + finding_concern + finding_ok), 0) as total_findings,
                COALESCE(SUM(lines_of_code), 0) as total_lines
            FROM scans WHERE status = 'complete'
        """).fetchone()
        stats = dict(row) if row else {}
    return jsonify({
        "total_scans": stats.get("total_scans", 0),
        "total_lines_scanned": stats.get("total_lines", 0),
        "total_findings": stats.get("total_findings", 0),
        "confirmed_high": stats.get("confirmed_high", 0),
    })


@app.route("/api/ops", methods=["GET"])
def api_ops():
    """Operational dashboard data — performance, tokens, corpus, trends."""
    from scanner.database import _get_conn
    with _get_conn() as conn:
        # Scan performance trends (last 20 scans with duration)
        perf_rows = conn.execute(
            """SELECT repo_name, scan_duration_seconds, tokens_in, tokens_out,
                      llm_calls, finding_high, finding_medium, opendocket_score,
                      timestamp, frameworks_triggered
               FROM scans
               WHERE status = 'complete' AND scan_duration_seconds > 0
               ORDER BY timestamp DESC LIMIT 20"""
        ).fetchall()
        perf = [dict(r) for r in perf_rows]

        # Token usage totals
        token_row = conn.execute(
            """SELECT COALESCE(SUM(tokens_in), 0) as total_in,
                      COALESCE(SUM(tokens_out), 0) as total_out,
                      COALESCE(SUM(llm_calls), 0) as total_calls
               FROM scans WHERE status = 'complete'"""
        ).fetchone()

        # Corpus stats
        corpus_row = conn.execute(
            """SELECT COUNT(*) as total_patterns,
                      COALESCE(SUM(confirmed_count), 0) as total_confirmed,
                      COALESCE(SUM(fp_count), 0) as total_fp,
                      COALESCE(SUM(hit_count), 0) as total_hits
               FROM evidence_patterns"""
        ).fetchone()

        corpus_by_fw = conn.execute(
            """SELECT framework, COUNT(*) as patterns,
                      SUM(confirmed_count) as confirmed, SUM(fp_count) as fp
               FROM evidence_patterns GROUP BY framework
               ORDER BY confirmed DESC"""
        ).fetchall()

        # Event counts (page views, shares, etc.)
        event_rows = conn.execute(
            """SELECT event_type, COUNT(*) as cnt FROM events
               WHERE timestamp > datetime('now', '-30 days')
               GROUP BY event_type"""
        ).fetchall()

        # Waitlist count
        wl_row = conn.execute("SELECT COUNT(*) as cnt FROM waitlist").fetchone()

        # Average scan duration
        avg_row = conn.execute(
            """SELECT AVG(scan_duration_seconds) as avg_dur,
                      MIN(scan_duration_seconds) as min_dur,
                      MAX(scan_duration_seconds) as max_dur
               FROM scans
               WHERE status = 'complete' AND scan_duration_seconds > 0"""
        ).fetchone()

    return jsonify({
        "performance": perf,
        "tokens": {
            "total_in": token_row["total_in"] if token_row else 0,
            "total_out": token_row["total_out"] if token_row else 0,
            "total_calls": token_row["total_calls"] if token_row else 0,
            "total": (token_row["total_in"] + token_row["total_out"]) if token_row else 0,
        },
        "corpus": {
            "total_patterns": corpus_row["total_patterns"] if corpus_row else 0,
            "confirmed": corpus_row["total_confirmed"] if corpus_row else 0,
            "false_positives": corpus_row["total_fp"] if corpus_row else 0,
            "by_framework": [dict(r) for r in corpus_by_fw],
        },
        "duration": {
            "avg": round(avg_row["avg_dur"] or 0, 1) if avg_row else 0,
            "min": round(avg_row["min_dur"] or 0, 1) if avg_row else 0,
            "max": round(avg_row["max_dur"] or 0, 1) if avg_row else 0,
        },
        "engagement": {e["event_type"]: e["cnt"] for e in event_rows},
        "waitlist_count": wl_row["cnt"] if wl_row else 0,
        "visitors": get_visitor_stats(),
        "feedback": get_feedback_stats(),
    })


@app.route("/api/usage", methods=["GET"])
def api_usage():
    stats = get_stats()
    today = stats.get("scans_today", 0)
    month = stats.get("scans_this_month", 0)
    return jsonify({
        "scans_today": today,
        "daily_limit": DAILY_SCAN_LIMIT,
        "scans_this_month": month,
        "monthly_limit": MONTHLY_SCAN_LIMIT,
        "pct_daily": round(today / max(DAILY_SCAN_LIMIT, 1) * 100, 1),
        "pct_monthly": round(month / max(MONTHLY_SCAN_LIMIT, 1) * 100, 1),
    })


@app.route("/api/directory", methods=["GET"])
def api_directory():
    return jsonify(get_directory_with_scores())


@app.route("/api/waitlist", methods=["POST"])
def api_waitlist():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip()
    if not email or "@" not in email:
        return jsonify({"error": "Valid email required"}), 400

    is_new = add_to_waitlist(email, source=data.get("source", "web"))
    return jsonify({"success": True, "new": is_new})


@app.route("/api/recent", methods=["GET"])
def api_recent():
    return jsonify(get_recent_scans())


@app.route("/api/track", methods=["POST"])
def api_track():
    data = request.get_json(silent=True) or {}
    event = data.get("event", "").strip()
    if event not in ("page_view", "share", "report_open", "issue_opened", "email_submitted"):
        return jsonify({"error": "Invalid event type"}), 400
    track_event(event, data.get("repo", ""), data.get("source", ""))
    return jsonify({"ok": True})


@app.route("/api/events", methods=["GET"])
def api_events():
    days = int(request.args.get("days", 7))
    return jsonify(get_event_counts(min(days, 90)))


@app.route("/api/feedback", methods=["POST"])
def api_feedback():
    """Submit human feedback on a finding."""
    data = request.get_json(silent=True) or {}
    scan_id = data.get("scan_id", "").strip()
    framework = data.get("framework", "").strip()
    question_id = data.get("question_id", "").strip()
    verdict = data.get("verdict", "").strip()  # "correct" or "incorrect"
    reason = data.get("reason", "").strip()

    if not all([scan_id, framework, question_id, verdict]):
        return jsonify({"error": "scan_id, framework, question_id, and verdict are required"}), 400
    if verdict not in ("correct", "incorrect"):
        return jsonify({"error": "verdict must be 'correct' or 'incorrect'"}), 400

    feedback_id = save_feedback(scan_id, framework, question_id, verdict, reason)

    # Feed human correction into accuracy tracking (weighted as stronger signal)
    if verdict == "incorrect" and reason:
        record_question_accuracy(
            framework, question_id, "POSSIBLE FALSE POSITIVE",
            domain="", fp_reason=f"[HUMAN] {reason[:200]}",
        )
    elif verdict == "correct":
        record_question_accuracy(
            framework, question_id, "CONFIRMED", domain="",
        )

    return jsonify({"ok": True, "feedback_id": feedback_id})


@app.route("/api/feedback/<scan_id>", methods=["GET"])
def api_get_feedback(scan_id):
    """Get all feedback for a scan."""
    return jsonify(get_feedback_for_scan(scan_id))


@app.route("/api/visitor", methods=["POST"])
def api_visitor():
    """Record a unique visitor. Client generates the ID (privacy-safe)."""
    data = request.get_json(silent=True) or {}
    vid = data.get("visitor_id", "").strip()
    page = data.get("page", "").strip()
    if not vid:
        return jsonify({"error": "visitor_id required"}), 400
    record_visitor(vid, page)
    return jsonify({"ok": True})


@app.route("/api/visitors", methods=["GET"])
def api_visitors():
    """Get visitor metrics."""
    return jsonify(get_visitor_stats())


@app.route("/api/discovered", methods=["GET"])
def api_discovered():
    """Get discovered novel patterns from wildcard scans."""
    fw = request.args.get("framework", "")
    return jsonify(get_discovered_patterns(framework=fw))


@app.route("/api/learning", methods=["GET"])
def api_learning():
    """Consolidated system learning summary — what the system has taught itself."""
    from scanner.database import _get_conn
    with _get_conn() as conn:
        corpus = conn.execute(
            """SELECT COUNT(*) as patterns,
                      COALESCE(SUM(confirmed_count), 0) as confirmed,
                      COALESCE(SUM(fp_count), 0) as fp
               FROM evidence_patterns"""
        ).fetchone()

        accuracy = conn.execute(
            """SELECT COUNT(*) as questions_tracked,
                      COALESCE(SUM(confirmed_count), 0) as total_confirmed,
                      COALESCE(SUM(fp_count), 0) as total_fp
               FROM question_accuracy"""
        ).fetchone()

        fp_reasons = conn.execute(
            """SELECT framework, question_id, common_fp_reasons
               FROM question_accuracy
               WHERE common_fp_reasons != '[]'
               ORDER BY fp_count DESC LIMIT 10"""
        ).fetchall()

        novel = conn.execute(
            """SELECT framework, category, search_hint, occurrences, repos_seen, first_seen
               FROM discovered_patterns ORDER BY last_seen DESC LIMIT 20"""
        ).fetchall()

        remediations = conn.execute(
            """SELECT COUNT(*) as total, SUM(use_count) as total_uses
               FROM remediation_library WHERE quality = 'specific'"""
        ).fetchone()

        feedback = conn.execute(
            """SELECT COUNT(*) as total,
                      SUM(CASE WHEN verdict = 'correct' THEN 1 ELSE 0 END) as correct,
                      SUM(CASE WHEN verdict = 'incorrect' THEN 1 ELSE 0 END) as incorrect
               FROM finding_feedback"""
        ).fetchone()

    # Parse FP reasons
    fp_intel = []
    for r in fp_reasons:
        try:
            reasons = json.loads(r["common_fp_reasons"])
            if reasons:
                fp_intel.append({
                    "framework": r["framework"],
                    "question_id": r["question_id"],
                    "reasons": reasons[:3],
                })
        except (json.JSONDecodeError, TypeError):
            pass

    # Parse novel patterns
    novel_list = []
    for r in novel:
        d = dict(r)
        try:
            d["repos_seen"] = json.loads(d.get("repos_seen", "[]"))
        except (json.JSONDecodeError, TypeError):
            d["repos_seen"] = []
        novel_list.append(d)

    return jsonify({
        "corpus": {
            "evidence_patterns": corpus["patterns"] if corpus else 0,
            "confirmed_signals": corpus["confirmed"] if corpus else 0,
            "fp_signals": corpus["fp"] if corpus else 0,
        },
        "accuracy": {
            "questions_tracked": accuracy["questions_tracked"] if accuracy else 0,
            "total_confirmed": accuracy["total_confirmed"] if accuracy else 0,
            "total_fp": accuracy["total_fp"] if accuracy else 0,
        },
        "fp_intelligence": fp_intel,
        "novel_questions": novel_list,
        "remediations": {
            "stored": remediations["total"] if remediations else 0,
            "times_reused": remediations["total_uses"] if remediations else 0,
        },
        "human_feedback": {
            "total": feedback["total"] if feedback else 0,
            "correct": feedback["correct"] if feedback else 0,
            "incorrect": feedback["incorrect"] if feedback else 0,
        },
    })


@app.route("/api/debug/env", methods=["GET"])
def debug_env():
    return jsonify({
        "anthropic_key_set": bool(os.environ.get("ANTHROPIC_API_KEY")),
        "gemini_key_set": bool(os.environ.get("GEMINI_API_KEY")),
        "database_path": os.path.join("data", "opendocket.db"),
        "daily_limit": DAILY_SCAN_LIMIT,
    })


# Serve static files
@app.route("/")
def serve_index():
    return app.send_static_file("index.html")


@app.route("/reports/<path:filename>")
def serve_report(filename):
    return app.send_static_file(f"reports/{filename}")


@app.route("/methodology.html")
def serve_methodology():
    return app.send_static_file("methodology.html")


@app.route("/privacy.html")
def serve_privacy():
    return app.send_static_file("privacy.html")


@app.route("/dashboard.html")
def serve_dashboard():
    return app.send_static_file("dashboard.html")


@app.route("/logs.html")
def serve_logs():
    return app.send_static_file("logs.html")


def main():
    init_db()
    # Auto-seed if database is empty (first boot on Railway)
    stats = get_stats()
    if stats.get("total_scans", 0) == 0:
        print("[OpenDocket API] Empty database — running seed...")
        try:
            from scanner.seed_database import seed
            seed()
        except Exception as e:
            print(f"[OpenDocket API] Seed failed: {e}")
        # Backfill evidence corpus from existing reports
        try:
            from scanner.backfill_corpus import backfill
            backfill()
        except Exception as e:
            print(f"[OpenDocket API] Corpus backfill failed: {e}")
    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    print(f"[OpenDocket API] Starting on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    main()
