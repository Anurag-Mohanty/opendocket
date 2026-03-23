"""
Generate static demo reports for the five target repositories.

This script clones each repo, runs the full scanner pipeline, and
saves both markdown and HTML reports to the reports/ and web/reports/
directories.

Usage:
    export ANTHROPIC_API_KEY="your-key"
    python generate_reports.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scanner.main import scan_repo
from scanner.repo_fetcher import fetch_and_qualify, cleanup_repo
from scanner.domain_detector import detect_domains
from scanner.compliance_mapper import map_frameworks
from scanner.agents.hipaa_agent import HIPAAAgent
from scanner.agents.soc2_agent import SOC2Agent
from scanner.report_generator import (
    generate_markdown_report,
    generate_html_report,
    generate_failed_gate_report,
    generate_failed_gate_html,
)

REPOS = [
    {
        "url": "https://github.com/medplum/medplum",
        "name": "medplum",
        "description": "Healthcare platform claiming HIPAA and SOC2",
    },
    {
        "url": "https://github.com/openemr/openemr",
        "name": "openemr",
        "description": "Full EHR system, no explicit compliance claims",
    },
    {
        "url": "https://github.com/juspay/hyperswitch",
        "name": "hyperswitch",
        "description": "Payments orchestrator claiming PCI-DSS",
    },
    {
        "url": "https://github.com/getprobo/probo",
        "name": "probo",
        "description": "Open source SOC2 compliance platform",
    },
    {
        "url": "https://github.com/kelseyhightower/nocode",
        "name": "nocode",
        "description": "Toy repo to test qualification gate failure",
    },
]


def generate_all():
    os.makedirs("reports", exist_ok=True)
    os.makedirs("web/reports", exist_ok=True)

    for repo_info in REPOS:
        url = repo_info["url"]
        name = repo_info["name"]
        print(f"\n{'='*60}")
        print(f"Processing: {name} ({url})")
        print(f"{'='*60}")

        try:
            # Generate markdown report
            scan_repo(url, "reports", "markdown")

            # Generate HTML report
            scan_repo(url, "web/reports", "html")

        except Exception as e:
            print(f"Error processing {name}: {e}")
            import traceback
            traceback.print_exc()

    print("\nDone! Reports saved to reports/ and web/reports/")


if __name__ == "__main__":
    generate_all()
