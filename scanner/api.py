"""
OpenDocket API Server.

Flask backend that powers live scanning from the web.
"""

import os
import re
import sys
import time
import threading
from collections import defaultdict
from datetime import datetime, timedelta

from flask import Flask, jsonify, request
from flask_cors import CORS

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.database import (
    init_db, create_scan, update_scan_status, save_findings,
    get_scan, get_stats, increment_stat, add_to_waitlist,
    get_directory_with_scores, get_recent_scans, get_recent_scan,
    track_event, get_event_counts,
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

        update_scan_status(scan_id, "running", _prog("clone", "Cloning repository"))
        repo_ctx = fetch_and_qualify(repo_url)

        try:
            update_scan_status(scan_id, "running", _prog("qualify", "Running qualification gates"))
            if not repo_ctx.qualification.qualified:
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

            update_scan_status(scan_id, "running", _prog("domain", "Detecting domains and frameworks"))
            domains = detect_domains(repo_ctx.path)

            update_scan_status(
                scan_id, "running", _prog("domain", "Mapping frameworks"),
                domains_detected=[{"domain": d.domain, "confidence": d.confidence} for d in domains],
                files_scanned=len(repo_ctx.file_index),
            )

            frameworks = map_frameworks(domains)
            if not frameworks:
                frameworks = ["soc2"]

            update_scan_status(
                scan_id, "running",
                progress=_prog("scan", f"Starting {len(frameworks)} frameworks", 0, len(frameworks)),
                frameworks_triggered=frameworks,
            )

            agent_results = []
            fw_complete = []
            for i, fw in enumerate(frameworks):
                agent_class = AGENTS.get(fw)
                if agent_class:
                    update_scan_status(
                        scan_id, "running",
                        progress=_prog("scan", f"Running {fw.upper()} agent", i, len(frameworks), fw.upper()),
                    )
                    agent = agent_class()
                    result = agent.scan(repo_ctx.path, repo_ctx.file_index, repo_ctx.readme_content)
                    agent_results.append(result)
                    fw_complete.append(fw.upper())

            # Independent review pass (Gemini)
            g_key = gemini_key or os.environ.get("GEMINI_API_KEY")
            if g_key:
                update_scan_status(scan_id, "running", _prog("judge", "Running Gemini independent review"))
                try:
                    from scanner.agents.base_agent import JudgeAgent
                    judge = JudgeAgent(g_key)
                    repo_ctx_dict = {
                        "repo_name": repo_ctx.name,
                        "domains": ", ".join(d.domain for d in domains),
                    }
                    judge.review_all(agent_results, repo_ctx_dict)
                except Exception as e:
                    print(f"[OpenDocket] Gemini review failed: {e}")
            else:
                update_scan_status(scan_id, "running", _prog("judge", "Skipping (no Gemini key)"))

            # Calculate stats
            all_findings = [f for r in agent_results for f in r.findings]
            high = sum(1 for f in all_findings if f.finding_level == "High Risk")
            med = sum(1 for f in all_findings if f.finding_level == "Medium Risk")
            concern = sum(1 for f in all_findings if f.finding_level == "Pattern of Concern")
            ok = sum(1 for f in all_findings if f.finding_level == "No Issue Found")
            score = calculate_score(agent_results)

            # Generate reports
            update_scan_status(scan_id, "running", _prog("report", "Generating reports"))

            html_report = generate_html_report(repo_ctx.name, repo_url, domains, agent_results)
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

            duration = time.time() - start_time
            update_scan_status(
                scan_id, "complete",
                progress="Scan complete",
                opendocket_score=score,
                finding_high=high,
                finding_medium=med,
                finding_concern=concern,
                finding_ok=ok,
                scan_duration_seconds=duration,
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

    except Exception as e:
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

    return jsonify(response)


@app.route("/api/stats", methods=["GET"])
def api_stats():
    stats = get_stats()
    return jsonify({
        "total_scans": stats.get("total_scans", 0),
        "total_repos": stats.get("total_repos_unique", 0),
        "total_lines_scanned": stats.get("total_lines_scanned", 0),
        "total_findings": stats.get("total_findings", 0),
        "high_risk_found": stats.get("high_risk_findings", 0),
        "judge_overrides": stats.get("judge_false_positives", 0),
        "judge_confirmed": stats.get("judge_confirmed", 0),
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
    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    print(f"[OpenDocket API] Starting on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    main()
