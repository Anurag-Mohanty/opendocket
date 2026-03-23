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


def main():
    parser = argparse.ArgumentParser(
        description="OpenDocket - Compliance Scanner for Code Repositories"
    )
    parser.add_argument("url", help="GitHub repository URL to scan")
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

    args = parser.parse_args()
    frameworks_filter = None
    if args.frameworks:
        frameworks_filter = [f.strip().lower() for f in args.frameworks.split(",")]

    scan_repo(args.url, args.output, args.format, frameworks_filter)


if __name__ == "__main__":
    main()
