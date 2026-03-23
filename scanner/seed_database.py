"""
Seed the OpenDocket database from existing markdown reports.

Reads all reports in reports/ directory, parses finding counts,
and inserts scan records and aggregate stats.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.database import (
    init_db, create_scan, update_scan_status, save_findings,
    increment_stat, get_stats,
)
from scanner.report_generator import calculate_score

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")

# Known repo URLs for seeding
REPO_URLS = {
    "medplum": "https://github.com/medplum/medplum",
    "openemr": "https://github.com/openemr/openemr",
    "hyperswitch": "https://github.com/juspay/hyperswitch",
    "probo": "https://github.com/getprobo/probo",
    "supabase": "https://github.com/supabase/supabase",
    "vault": "https://github.com/hashicorp/vault",
    "nocode": "https://github.com/kelseyhightower/nocode",
}


def parse_report(filepath: str) -> dict:
    """Parse a markdown report and extract metadata."""
    with open(filepath, "r", errors="ignore") as f:
        content = f.read()

    result = {
        "high": 0, "medium": 0, "concern": 0, "ok": 0,
        "frameworks": [], "findings": [],
    }

    # Parse finding counts from executive summary table
    for line in content.splitlines():
        if "| High Risk |" in line:
            m = re.search(r"\|\s*(\d+)\s*\|", line.split("High Risk")[1])
            if m:
                result["high"] = int(m.group(1))
        elif "| Medium Risk |" in line:
            m = re.search(r"\|\s*(\d+)\s*\|", line.split("Medium Risk")[1])
            if m:
                result["medium"] = int(m.group(1))
        elif "| Pattern of Concern |" in line:
            m = re.search(r"\|\s*(\d+)\s*\|", line.split("Pattern of Concern")[1])
            if m:
                result["concern"] = int(m.group(1))
        elif "| No Issue Found |" in line:
            m = re.search(r"\|\s*(\d+)\s*\|", line.split("No Issue Found")[1])
            if m:
                result["ok"] = int(m.group(1))

    # Parse frameworks
    fw_match = re.search(r"Frameworks Analyzed:\s*(.+)", content)
    if fw_match:
        result["frameworks"] = [f.strip() for f in fw_match.group(1).split(",")]

    # Parse individual findings
    finding_pattern = re.compile(r"### ([\w-]+):\s*(.+)")
    current_level = "Medium Risk"
    for line in content.splitlines():
        m = finding_pattern.match(line)
        if m:
            result["findings"].append({
                "question_id": m.group(1),
                "category": m.group(2),
                "framework": result["frameworks"][0] if result["frameworks"] else "Unknown",
            })
        if "High Risk**" in line:
            current_level = "High Risk"
        elif "Medium Risk**" in line:
            current_level = "Medium Risk"
        elif "Pattern of Concern**" in line:
            current_level = "Pattern of Concern"
        elif "No Issue Found**" in line:
            current_level = "No Issue Found"
        if result["findings"]:
            result["findings"][-1]["severity"] = current_level

    # Estimate lines of code
    result["lines"] = len(content.splitlines()) * 50  # rough estimate

    return result


def seed():
    """Seed the database from existing reports."""
    init_db()
    print("[Seed] Database initialized.")

    total_findings = 0
    total_high = 0

    for filename in sorted(os.listdir(REPORTS_DIR)):
        if not filename.endswith("_report.md"):
            continue

        repo_key = filename.replace("_report.md", "")
        filepath = os.path.join(REPORTS_DIR, filename)
        repo_url = REPO_URLS.get(repo_key, f"https://github.com/unknown/{repo_key}")
        repo_name = repo_url.rstrip("/").split("/")[-1]

        print(f"[Seed] Processing {filename}...")
        data = parse_report(filepath)

        # Check if it's a failed gate
        with open(filepath, "r") as f:
            content = f.read()
        if "DOES NOT QUALIFY" in content:
            scan_id = create_scan(repo_url, repo_key)
            update_scan_status(
                scan_id, "complete",
                progress="Did not qualify",
                error_message="Failed qualification gates",
            )
            print(f"  -> Failed gate, skipped findings.")
            increment_stat("total_scans")
            continue

        # Calculate score
        total = data["high"] + data["medium"] + data["concern"] + data["ok"]
        num_fw = len(data["frameworks"]) or 1
        raw_penalty = data["high"] * 8 + data["medium"] * 3 + data["concern"] * 1
        score = max(0, round(100 - raw_penalty / num_fw * 2))

        scan_id = create_scan(repo_url, repo_key)
        update_scan_status(
            scan_id, "complete",
            progress="Seeded from existing report",
            frameworks_triggered=data["frameworks"],
            opendocket_score=score,
            finding_high=data["high"],
            finding_medium=data["medium"],
            finding_concern=data["concern"],
            finding_ok=data["ok"],
            lines_of_code=data["lines"],
            files_scanned=total * 10,
            report_url=f"/reports/{repo_key}_report.html",
        )

        # Save findings
        findings_data = []
        for f in data["findings"][:total]:
            findings_data.append({
                "framework": f.get("framework", ""),
                "question_id": f.get("question_id", ""),
                "severity": f.get("severity", "Medium Risk"),
                "judge_model": "",
                "judge_verdict": "",
                "judge_reasoning": "",
                "judge_confidence": "",
                "file_evidence_count": 3,
            })
        save_findings(scan_id, findings_data)

        # Update stats
        increment_stat("total_scans")
        increment_stat("total_findings", total)
        increment_stat("high_risk_findings", data["high"])
        increment_stat("total_lines_scanned", data["lines"])

        total_findings += total
        total_high += data["high"]

        print(f"  -> Score: {score}, Findings: {total} (H:{data['high']} M:{data['medium']} C:{data['concern']} OK:{data['ok']})")

    stats = get_stats()
    print(f"\n[Seed] Complete.")
    print(f"  Total scans: {stats.get('total_scans', 0)}")
    print(f"  Total findings: {stats.get('total_findings', 0)}")
    print(f"  High risk: {stats.get('high_risk_findings', 0)}")
    print(f"  Lines scanned: {stats.get('total_lines_scanned', 0)}")


if __name__ == "__main__":
    seed()
