"""
Regenerate all HTML reports from existing markdown reports.

Parses markdown reports into AgentResult/Finding structures
and generates HTML using the current template.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.agents.base_agent import AgentResult, Finding, Evidence
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
}


def parse_md_to_results(filepath: str) -> tuple[list[DomainResult], list[AgentResult]]:
    """Parse a markdown report into DomainResult and AgentResult lists."""
    with open(filepath, "r", errors="ignore") as f:
        content = f.read()

    # Check failed gate
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

    # Parse frameworks and findings
    agent_results = []
    current_fw = None
    current_result = None
    current_finding = None

    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]

        # Framework header: "## HIPAA Findings" or "## FRAMEWORK Findings"
        fw_match = re.match(r"^## (\S+) Findings", line)
        if fw_match:
            if current_result and current_finding:
                current_result.findings.append(current_finding)
                current_finding = None
            if current_result:
                agent_results.append(current_result)
            current_fw = fw_match.group(1)
            current_result = AgentResult(framework=current_fw)
            i += 1
            continue

        # Finding header: "### HIPAA-001: Category Name"
        finding_match = re.match(r"^### ([\w-]+):\s*(.+)", line)
        if finding_match and current_result is not None:
            if current_finding:
                current_result.findings.append(current_finding)
            current_finding = Finding(
                question_id=finding_match.group(1),
                category=finding_match.group(2).strip(),
                legal_question="",
                regulatory_standard="",
                evidence=[],
                finding_level="Medium Risk",
                finding_text="",
                remediation="",
            )
            i += 1
            continue

        if current_finding is not None:
            # Legal question (bold text or after LEGAL QUESTION header)
            if line.startswith("**") and "LEGAL QUESTION" not in line and "FINDING" not in line and "REMEDIATION" not in line and "EVIDENCE" not in line and "REGULATORY" not in line:
                if not current_finding.legal_question:
                    current_finding.legal_question = line.strip("* \n")

            # Regulatory standard
            if line.startswith("*") and not line.startswith("**") and ("CFR" in line or "SOC" in line or "CC" in line or "PCI" in line or "GDPR" in line or "Section" in line or "TCPA" in line):
                current_finding.regulatory_standard = line.strip("* \n")

            # Evidence lines
            if line.startswith("- `") and ":" in line:
                ev_match = re.match(r"- `([^:]+):(\d+)`", line)
                if ev_match:
                    current_finding.evidence.append(Evidence(
                        file_path=ev_match.group(1),
                        line_number=int(ev_match.group(2)),
                        content=line.split("—")[-1].strip().strip("`") if "—" in line else "",
                        match_type="search_pattern",
                    ))

            # Finding level
            if "🔴 High Risk" in line or "**High Risk**" in line:
                current_finding.finding_level = "High Risk"
            elif "🟠 Medium Risk" in line or "**Medium Risk**" in line:
                current_finding.finding_level = "Medium Risk"
            elif "🔵 Pattern of Concern" in line or "**Pattern of Concern**" in line:
                current_finding.finding_level = "Pattern of Concern"
            elif "🟢 No Issue Found" in line or "**No Issue Found**" in line:
                current_finding.finding_level = "No Issue Found"

            # Finding text (line after FINDING level)
            if line and not line.startswith("#") and not line.startswith("**") and not line.startswith("- ") and not line.startswith("*") and not line.startswith("|") and not line.startswith("---") and not line.startswith(">"):
                if current_finding.finding_text == "" and len(line) > 30:
                    current_finding.finding_text = line.strip()

            # Remediation
            if "**Remediation:**" in line or "**REMEDIATION" in line:
                rem_text = line.split(":**")[-1].strip() if ":**" in line else ""
                # Grab next non-empty line if this one is just the header
                if not rem_text and i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].startswith("#") and not lines[i + 1].startswith("---"):
                    rem_text = lines[i + 1].strip()
                current_finding.remediation = rem_text

        i += 1

    # Flush last finding and result
    if current_finding and current_result:
        current_result.findings.append(current_finding)
    if current_result:
        agent_results.append(current_result)

    return domains, agent_results


def main():
    os.makedirs(HTML_DIR, exist_ok=True)
    count = 0

    for filename in sorted(os.listdir(REPORTS_DIR)):
        if not filename.endswith("_report.md"):
            continue

        repo_key = filename.replace("_report.md", "")
        filepath = os.path.join(REPORTS_DIR, filename)
        repo_url = REPO_URLS.get(repo_key, f"https://github.com/unknown/{repo_key}")

        print(f"[Regen] Processing {filename}...")

        with open(filepath, "r") as f:
            content = f.read()

        if "DOES NOT QUALIFY" in content:
            # Failed gate
            reasons = []
            for line in content.splitlines():
                if line.startswith("- ") and "qualifying" not in line.lower():
                    reasons.append(line[2:])
            html_out = generate_failed_gate_html(repo_key, repo_url, reasons[:5], {"status": "failed"})
            out_path = os.path.join(HTML_DIR, f"{repo_key}_report.html")
            with open(out_path, "w") as f:
                f.write(html_out)
            # Also write as failed_gate_example.html if nocode
            if repo_key == "nocode":
                with open(os.path.join(HTML_DIR, "failed_gate_example.html"), "w") as f:
                    f.write(html_out)
            print(f"  -> Failed gate report written")
            count += 1
            continue

        domains, agent_results = parse_md_to_results(filepath)

        if not agent_results:
            print(f"  -> No findings parsed, skipping")
            continue

        total = sum(len(r.findings) for r in agent_results)
        high = sum(1 for r in agent_results for f in r.findings if f.finding_level == "High Risk")
        print(f"  -> Parsed {len(agent_results)} frameworks, {total} findings ({high} high risk)")

        html_out = generate_html_report(repo_key, repo_url, domains, agent_results)
        out_path = os.path.join(HTML_DIR, f"{repo_key}_report.html")
        with open(out_path, "w") as f:
            f.write(html_out)
        print(f"  -> HTML written to {out_path}")
        count += 1

    print(f"\n[Regen] Done. {count} reports generated in {HTML_DIR}/")


if __name__ == "__main__":
    main()
