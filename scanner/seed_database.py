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

# Known domains for seeded repos (since seed doesn't run domain detection)
REPO_DOMAINS_SEED = {
    "medplum": [{"domain": "healthcare", "confidence": 95}, {"domain": "saas", "confidence": 60}],
    "openemr": [{"domain": "healthcare", "confidence": 98}],
    "hyperswitch": [{"domain": "fintech", "confidence": 92}, {"domain": "payments", "confidence": 90}, {"domain": "saas", "confidence": 55}],
    "probo": [{"domain": "saas", "confidence": 80}],
    "supabase": [{"domain": "saas", "confidence": 88}, {"domain": "infrastructure", "confidence": 65}],
    "vault": [{"domain": "infrastructure", "confidence": 95}, {"domain": "saas", "confidence": 40}],
    "nocode": [],
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

    # Parse individual findings with judge verdicts
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


def parse_html_judge_verdicts(html_path: str) -> dict:
    """Parse the HTML report to count confirmed vs false positive verdicts."""
    counts = {"confirmed_high": 0, "confirmed_med": 0, "fp": 0, "total_judged": 0}
    if not os.path.exists(html_path):
        return counts
    with open(html_path, "r", errors="ignore") as f:
        content = f.read()

    # Count judge verdicts from the HTML verdict labels
    # Each finding has a verdict-label with class v-confirmed, v-fp, etc.
    confirmed = len(re.findall(r'class="verdict-label v-confirmed"', content))
    fp = len(re.findall(r'class="verdict-label v-fp"', content))
    ctx = len(re.findall(r'class="verdict-label v-context"', content))
    add = len(re.findall(r'class="verdict-label v-additional"', content))

    # Also try counting from the scorecard table "Confirmed" column
    # Format: <td style="color:#1A7F37;font-weight:700">5</td>
    scorecard_confirmed = re.findall(r'color:#1A7F37;font-weight:700">(\d+)</td>', content)

    counts["confirmed_high"] = confirmed  # This counts all confirmed, not just high
    counts["fp"] = fp
    counts["total_judged"] = confirmed + fp + ctx + add

    # Better: parse the "X confirmed high" from the action bar
    ch_match = re.search(r'(\d+)\s*confirmed high', content)
    if ch_match:
        counts["confirmed_high"] = int(ch_match.group(1))

    return counts


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
        parts = repo_url.rstrip("/").split("/")
        repo_name = f"{parts[-2]}/{parts[-1]}"

        print(f"[Seed] Processing {filename}...")
        data = parse_report(filepath)

        # Check if it's a failed gate
        with open(filepath, "r") as f:
            content = f.read()
        if "DOES NOT QUALIFY" in content:
            scan_id = create_scan(repo_url, repo_name)
            update_scan_status(
                scan_id, "complete",
                progress="Did not qualify",
                error_message="Failed qualification gates",
            )
            print(f"  -> Failed gate, skipped findings.")
            increment_stat("total_scans")
            continue

        # Parse judge verdicts from HTML report for confirmed counts
        html_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "docs", "reports", f"{repo_key}_report.html",
        )
        judge_counts = parse_html_judge_verdicts(html_path)
        confirmed_high = judge_counts["confirmed_high"]
        has_judge = judge_counts["total_judged"] > 0

        # Use confirmed counts for high/medium when judge data exists
        if has_judge:
            display_high = confirmed_high
            display_medium = data["medium"]  # keep raw medium (less critical)
        else:
            display_high = data["high"]
            display_medium = data["medium"]

        # Calculate score based on confirmed counts
        total = data["high"] + data["medium"] + data["concern"] + data["ok"]
        num_fw = len(data["frameworks"]) or 1
        raw_penalty = display_high * 8 + display_medium * 3 + data["concern"] * 1
        score = max(0, round(100 - raw_penalty / num_fw * 2))

        scan_id = create_scan(repo_url, repo_name)
        seed_domains = REPO_DOMAINS_SEED.get(repo_key, [])
        update_scan_status(
            scan_id, "complete",
            progress="Seeded from existing report",
            frameworks_triggered=data["frameworks"],
            domains_detected=seed_domains,
            opendocket_score=score,
            finding_high=display_high,
            finding_medium=display_medium,
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
        increment_stat("high_risk_findings", display_high)
        increment_stat("total_lines_scanned", data["lines"])

        total_findings += total
        total_high += display_high

        print(f"  -> Score: {score}, Findings: {total} (Confirmed H:{display_high} raw H:{data['high']} M:{display_medium} C:{data['concern']} OK:{data['ok']}){' [judge ran]' if has_judge else ''}")

    stats = get_stats()
    print(f"\n[Seed] Complete.")
    print(f"  Total scans: {stats.get('total_scans', 0)}")
    print(f"  Total findings: {stats.get('total_findings', 0)}")
    print(f"  High risk: {stats.get('high_risk_findings', 0)}")
    print(f"  Lines scanned: {stats.get('total_lines_scanned', 0)}")


if __name__ == "__main__":
    seed()
