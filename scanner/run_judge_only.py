"""
Run Gemini independent review on existing findings without rescanning.

Parses markdown reports, runs ONLY the Gemini judge on each finding,
updates the findings with verdicts, and regenerates HTML reports.
Does NOT re-clone repos or re-run Claude — saves API credits.

Usage:
  python scanner/run_judge_only.py              # all reports
  python scanner/run_judge_only.py medplum      # single repo
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.agents.base_agent import Finding, Evidence, AgentResult, JudgeAgent
from scanner.domain_detector import DomainResult
from scanner.report_generator import generate_html_report, generate_failed_gate_html

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
HTML_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "reports")

REPO_URLS = {
    "medplum": "https://github.com/medplum/medplum",
    "openemr": "https://github.com/openemr/openemr",
    "hyperswitch": "https://github.com/juspay/hyperswitch",
    "probo": "https://github.com/getprobo/probo",
    "supabase": "https://github.com/supabase/supabase",
    "vault": "https://github.com/hashicorp/vault",
    "nocode": "https://github.com/kelseyhightower/nocode",
    "failed_gate_example": "https://github.com/kelseyhightower/nocode",
    "formbricks": "https://github.com/formbricks/formbricks",
}


def parse_report(filepath: str) -> tuple[list[DomainResult], list[AgentResult]]:
    """Parse markdown report into structured data for judge review."""
    with open(filepath, "r", errors="ignore") as f:
        content = f.read()

    if "DOES NOT QUALIFY" in content:
        return [], []

    # Parse domains
    domains = []
    for m in re.finditer(r"\*\*(\w+)\*\* — Confidence: ([\d.]+)% \((\d+) signals", content):
        domains.append(DomainResult(
            domain=m.group(1).lower(),
            confidence=float(m.group(2)),
            signal_count=int(m.group(3)),
            signals_found=[],
        ))

    # Parse frameworks + findings
    results = []
    cur_result = None
    cur_finding = None

    for line in content.splitlines():
        # Framework header
        fw_m = re.match(r"^## (\S+) Findings", line)
        if fw_m:
            if cur_finding and cur_result:
                cur_result.findings.append(cur_finding)
                cur_finding = None
            if cur_result:
                results.append(cur_result)
            cur_result = AgentResult(framework=fw_m.group(1))
            continue

        # Finding header
        f_m = re.match(r"^### ([\w-]+):\s*(.+)", line)
        if f_m and cur_result is not None:
            if cur_finding:
                cur_result.findings.append(cur_finding)
            cur_finding = Finding(
                question_id=f_m.group(1),
                category=f_m.group(2).strip(),
                legal_question="",
                regulatory_standard="",
                evidence=[],
                finding_level="Medium Risk",
                finding_text="",
                remediation="",
            )
            continue

        if cur_finding:
            stripped = line.strip()

            # Remediation capture (priority)
            if getattr(cur_finding, '_capture_rem', False):
                if stripped and not stripped.startswith(("#", "---", "|")):
                    cur_finding.remediation = stripped
                    cur_finding._capture_rem = False
                continue

            if "**Remediation" in line or "**REMEDIATION" in line:
                rem = line.split(":**")[-1].strip() if ":**" in line else ""
                if rem and len(rem) > 10:
                    cur_finding.remediation = rem
                else:
                    cur_finding._capture_rem = True
                continue

            # Evidence
            ev_m = re.match(r"- `([^:]+):(\d+)`.*— `(.+)`", line)
            if ev_m:
                cur_finding.evidence.append(Evidence(
                    file_path=ev_m.group(1),
                    line_number=int(ev_m.group(2)),
                    content=ev_m.group(3),
                    match_type="search_pattern",
                ))
                continue

            # Severity
            if "FINDING" in line or ":red_circle:" in line or ":orange_circle:" in line or ":green_circle:" in line or ":yellow_circle:" in line or ":blue_circle:" in line:
                low = line.lower()
                if "high risk" in low or ":red_circle:" in line:
                    cur_finding.finding_level = "High Risk"
                elif "medium risk" in low or ":orange_circle:" in line:
                    cur_finding.finding_level = "Medium Risk"
                elif "pattern of concern" in low or ":yellow_circle:" in line or ":blue_circle:" in line:
                    cur_finding.finding_level = "Pattern of Concern"
                elif "no issue found" in low or ":green_circle:" in line:
                    cur_finding.finding_level = "No Issue Found"
                continue

            # Legal question
            if line.startswith("**") and "?" in line and not cur_finding.legal_question:
                cur_finding.legal_question = line.strip("* \n")
                continue

            # Regulatory standard
            if line.startswith("*") and not line.startswith("**") and ("CFR" in line or "U.S.C." in line or "CC" in line or "Article" in line or "Section" in line):
                cur_finding.regulatory_standard = line.strip("* \n")
                continue

            # Skip headers
            if stripped.startswith(("**LEGAL", "**REGULATORY", "**EVIDENCE", "**FINDING", "---")):
                continue

            # Finding text
            if not cur_finding.finding_text and len(stripped) > 40 and not stripped.startswith(("#", "*", "-", "|", ">")):
                cur_finding.finding_text = stripped

    if cur_finding and cur_result:
        cur_result.findings.append(cur_finding)
    if cur_result:
        results.append(cur_result)

    return domains, results


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    os.makedirs(HTML_DIR, exist_ok=True)

    # Initialize judge
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        print("[ERROR] GEMINI_API_KEY not set. Cannot run judge.")
        print("  Set: export GEMINI_API_KEY=your_key")
        sys.exit(1)

    judge = JudgeAgent(gemini_key)
    if judge.model is None:
        print("[ERROR] Gemini model failed to initialize.")
        sys.exit(1)

    print(f"[Judge] Gemini 1.5 Flash initialized.")

    for filename in sorted(os.listdir(REPORTS_DIR)):
        if not filename.endswith("_report.md"):
            continue

        key = filename.replace("_report.md", "")

        # Filter to single repo if specified
        if target and key != target:
            continue

        filepath = os.path.join(REPORTS_DIR, filename)
        url = REPO_URLS.get(key, f"https://github.com/unknown/{key}")

        with open(filepath, "r") as f:
            content = f.read()

        if "DOES NOT QUALIFY" in content:
            print(f"[Judge] {key}: skipping (failed gate)")
            continue

        print(f"\n[Judge] {key}: parsing findings...")
        domains, results = parse_report(filepath)

        if not results:
            print(f"  -> No findings parsed, skipping")
            continue

        total = sum(len(r.findings) for r in results)
        high = sum(1 for r in results for f in r.findings if f.finding_level == "High Risk")
        print(f"  -> {len(results)} frameworks, {total} findings, {high} high risk")

        # Tag findings with framework
        for result in results:
            for f in result.findings:
                f._framework = result.framework

        # Run Gemini judge
        repo_context = {
            "repo_name": key,
            "domains": ", ".join(d.domain for d in domains),
        }
        print(f"  -> Running Gemini review on {total} findings...")
        judge.review_all(results, repo_context)

        # Count verdicts
        all_findings = [f for r in results for f in r.findings]
        confirmed = sum(1 for f in all_findings if f.review_verdict == "CONFIRMED")
        context = sum(1 for f in all_findings if f.review_verdict == "CONTEXT DEPENDENT")
        fp = sum(1 for f in all_findings if f.review_verdict == "POSSIBLE FALSE POSITIVE")
        additional = sum(1 for f in all_findings if f.review_verdict == "ADDITIONAL RISK")
        improved = sum(1 for f in all_findings if f.improved_remediation)
        print(f"  -> Verdicts: {confirmed} confirmed, {context} context, {fp} false positive, {additional} additional risk")
        print(f"  -> {improved} remediations improved by Gemini")

        # Generate HTML with judge data
        html_out = generate_html_report(key, url, domains, results)
        out_path = os.path.join(HTML_DIR, f"{key}_report.html")
        with open(out_path, "w") as f:
            f.write(html_out)
        print(f"  -> HTML written to {out_path}")

    print(f"\n[Judge] Done.")


if __name__ == "__main__":
    main()
