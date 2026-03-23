"""
OpenDocket - Compliance Scanner Entry Point

Accepts a GitHub repository URL, clones it, detects regulatory domains,
and runs compliance agents to produce a legal brief format report.
"""

import argparse
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.repo_fetcher import fetch_and_qualify, cleanup_repo
from scanner.domain_detector import detect_domains
from scanner.compliance_mapper import map_frameworks
from scanner.agents.hipaa_agent import HIPAAAgent
from scanner.agents.soc2_agent import SOC2Agent
from scanner.agents.pci_dss_agent import PCIDSSAgent
from scanner.agents.gdpr_agent import GDPRAgent
from scanner.agents.tcpa_agent import TCPAAgent
from scanner.agents.sox_agent import SOXAgent
from scanner.report_generator import (
    generate_markdown_report,
    generate_html_report,
    generate_failed_gate_report,
    generate_failed_gate_html,
)


AGENTS = {
    "hipaa": HIPAAAgent,
    "soc2": SOC2Agent,
    "pci_dss": PCIDSSAgent,
    "gdpr": GDPRAgent,
    "tcpa": TCPAAgent,
    "sox": SOXAgent,
}


def scan_repo(url: str, output_dir: str = "reports", fmt: str = "markdown",
              frameworks_filter: list[str] | None = None) -> str:
    """Scan a repository and produce a compliance report.

    Returns the path to the generated report file.
    """
    print(f"[OpenDocket] Fetching repository: {url}")
    repo_ctx = fetch_and_qualify(url)

    try:
        # Check qualification
        if not repo_ctx.qualification.qualified:
            print(f"[OpenDocket] Repository does not qualify for scanning.")
            for reason in repo_ctx.qualification.reasons:
                print(f"  - {reason}")

            os.makedirs(output_dir, exist_ok=True)

            if fmt == "html":
                report = generate_failed_gate_html(
                    repo_ctx.name, url,
                    repo_ctx.qualification.reasons,
                    repo_ctx.qualification.stats,
                )
                ext = ".html"
            else:
                report = generate_failed_gate_report(
                    repo_ctx.name, url,
                    repo_ctx.qualification.reasons,
                    repo_ctx.qualification.stats,
                )
                ext = ".md"

            report_path = os.path.join(output_dir, f"{repo_ctx.name}_report{ext}")
            with open(report_path, "w") as f:
                f.write(report)
            print(f"[OpenDocket] Gate failure report written to: {report_path}")
            return report_path

        # Detect domains
        print(f"[OpenDocket] Detecting domains...")
        domains = detect_domains(repo_ctx.path)
        if domains:
            for d in domains:
                print(f"  {d.domain}: {d.confidence}% confidence")
        else:
            print("  No specific domain detected. Running general SOC2 scan.")

        # Map to frameworks
        frameworks = map_frameworks(domains)
        if frameworks_filter:
            frameworks = [f for f in frameworks if f in frameworks_filter]
        if not frameworks:
            frameworks = ["soc2"]  # Default fallback
        print(f"[OpenDocket] Frameworks to scan: {', '.join(frameworks)}")

        # Run agents
        agent_results = []
        for fw in frameworks:
            agent_class = AGENTS.get(fw)
            if agent_class:
                print(f"[OpenDocket] Running {fw.upper()} agent...")
                agent = agent_class()
                result = agent.scan(
                    repo_ctx.path,
                    repo_ctx.file_index,
                    repo_ctx.readme_content,
                )
                agent_results.append(result)

        # Independent review pass (Gemini)
        gemini_key = os.environ.get("GEMINI_API_KEY")
        if gemini_key:
            print(f"[OpenDocket] Running Gemini independent review...")
            try:
                from scanner.agents.base_agent import JudgeAgent
                judge = JudgeAgent(gemini_key)
                repo_context = {
                    "repo_name": repo_ctx.name,
                    "domains": ", ".join(d.domain for d in domains),
                }
                judge.review_all(agent_results, repo_context)
            except Exception as e:
                print(f"[OpenDocket] Gemini review failed: {e}. Continuing without review.")
        else:
            print(f"[OpenDocket] GEMINI_API_KEY not set. Skipping independent review.")

        # Generate report
        os.makedirs(output_dir, exist_ok=True)

        if fmt == "html":
            report = generate_html_report(
                repo_ctx.name, url, domains, agent_results,
            )
            ext = ".html"
        else:
            report = generate_markdown_report(
                repo_ctx.name, url, domains, agent_results,
            )
            ext = ".md"

        report_path = os.path.join(output_dir, f"{repo_ctx.name}_report{ext}")
        with open(report_path, "w") as f:
            f.write(report)
        print(f"[OpenDocket] Report written to: {report_path}")
        return report_path

    finally:
        cleanup_repo(repo_ctx.path)


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


def regenerate_all_html():
    """Regenerate all HTML reports from markdown using current template."""
    import re as _re
    from scanner.agents.base_agent import Finding, Evidence, AgentResult
    from scanner.domain_detector import DomainResult

    reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports")
    html_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "reports")
    os.makedirs(html_dir, exist_ok=True)

    for filename in sorted(os.listdir(reports_dir)):
        if not filename.endswith("_report.md"):
            continue
        key = filename.replace("_report.md", "")
        filepath = os.path.join(reports_dir, filename)
        url = REPO_URLS.get(key, f"https://github.com/unknown/{key}")

        with open(filepath, "r", errors="ignore") as f:
            content = f.read()

        print(f"[Regen] {filename}...")

        if "DOES NOT QUALIFY" in content:
            html_out = generate_failed_gate_html(key, url, ["Failed qualification gates"], {"status": "failed"})
            for name in [f"{key}_report.html", "failed_gate_example.html"] if key == "nocode" else [f"{key}_report.html"]:
                with open(os.path.join(html_dir, name), "w") as f:
                    f.write(html_out)
            print(f"  -> Gate report")
            continue

        # Parse domains
        domains = []
        for m in _re.finditer(r"\*\*(\w+)\*\* — Confidence: ([\d.]+)% \((\d+) signals", content):
            domains.append(DomainResult(domain=m.group(1).lower(), confidence=float(m.group(2)),
                                        signal_count=int(m.group(3)), signals_found=[]))

        # Parse frameworks + findings
        results = []
        cur_result = None
        cur_finding = None

        for line in content.splitlines():
            # Framework header
            fw_m = _re.match(r"^## (\S+) Findings", line)
            if fw_m:
                if cur_finding and cur_result:
                    cur_result.findings.append(cur_finding)
                    cur_finding = None
                if cur_result:
                    results.append(cur_result)
                cur_result = AgentResult(framework=fw_m.group(1))
                continue

            # Finding header
            f_m = _re.match(r"^### ([\w-]+):\s*(.+)", line)
            if f_m and cur_result is not None:
                if cur_finding:
                    cur_result.findings.append(cur_finding)
                cur_finding = Finding(
                    question_id=f_m.group(1), category=f_m.group(2).strip(),
                    legal_question="", regulatory_standard="", evidence=[],
                    finding_level="Medium Risk", finding_text="", remediation="",
                )
                continue

            if cur_finding:
                # Evidence
                ev_m = _re.match(r"- `([^:]+):(\d+)`.*— `(.+)`", line)
                if ev_m:
                    cur_finding.evidence.append(Evidence(
                        file_path=ev_m.group(1), line_number=int(ev_m.group(2)),
                        content=ev_m.group(3), match_type="search_pattern"))
                # Severity
                if "High Risk**" in line:
                    cur_finding.finding_level = "High Risk"
                elif "Medium Risk**" in line:
                    cur_finding.finding_level = "Medium Risk"
                elif "Pattern of Concern**" in line:
                    cur_finding.finding_level = "Pattern of Concern"
                elif "No Issue Found**" in line:
                    cur_finding.finding_level = "No Issue Found"
                # Finding text
                if not cur_finding.finding_text and len(line) > 40 and not line.startswith(("#", "*", "-", "|", ">", "---")):
                    cur_finding.finding_text = line.strip()
                # Remediation
                if "**Remediation" in line:
                    cur_finding.remediation = line.split(":**")[-1].strip() if ":**" in line else ""

        if cur_finding and cur_result:
            cur_result.findings.append(cur_finding)
        if cur_result:
            results.append(cur_result)

        if not results:
            print(f"  -> No findings parsed, skipping")
            continue

        total = sum(len(r.findings) for r in results)
        high = sum(1 for r in results for f in r.findings if f.finding_level == "High Risk")
        print(f"  -> {len(results)} frameworks, {total} findings, {high} high risk")

        html_out = generate_html_report(key, url, domains, results)
        with open(os.path.join(html_dir, f"{key}_report.html"), "w") as f:
            f.write(html_out)
        print(f"  -> HTML written")

    print("[Regen] Done.")


def main():
    parser = argparse.ArgumentParser(
        description="OpenDocket - Compliance Scanner for Code Repositories"
    )
    parser.add_argument("url", nargs="?", help="GitHub repository URL to scan")
    parser.add_argument(
        "--output", "-o", default="reports",
        help="Output directory for reports (default: reports/)"
    )
    parser.add_argument(
        "--format", "-f", choices=["markdown", "html"], default="markdown",
        help="Output format (default: markdown)"
    )
    parser.add_argument(
        "--frameworks", type=str, default=None,
        help="Comma-separated list of frameworks to scan (e.g., hipaa,soc2)"
    )
    parser.add_argument(
        "--regenerate-all", action="store_true",
        help="Regenerate all HTML reports from existing markdown reports"
    )

    args = parser.parse_args()

    if args.regenerate_all:
        regenerate_all_html()
        return

    if not args.url:
        parser.error("url is required unless --regenerate-all is used")

    frameworks_filter = None
    if args.frameworks:
        frameworks_filter = [f.strip().lower() for f in args.frameworks.split(",")]

    scan_repo(args.url, args.output, args.format, frameworks_filter)


if __name__ == "__main__":
    main()
