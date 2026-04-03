"""
Backfill the evidence_patterns corpus from existing HTML reports.

Parses each HTML report to extract:
- Question IDs
- Evidence file paths
- Judge verdicts (CONFIRMED / POSSIBLE FALSE POSITIVE / etc.)

Then feeds them into record_evidence_patterns() to seed the corpus
so future scans benefit from learned search priorities.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.database import init_db, record_evidence_patterns

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "reports")

# Map repo names to likely domains for the corpus
REPO_DOMAINS = {
    "hyperswitch": "fintech, payments",
    "medplum": "healthcare",
    "openemr": "healthcare",
    "supabase": "saas",
    "vault": "infrastructure",
    "probo": "saas",
}


def parse_findings_from_html(html_path: str) -> list[dict]:
    """Parse an HTML report and extract findings with evidence + verdicts."""
    with open(html_path, "r", errors="ignore") as f:
        content = f.read()

    findings = []

    # Split by finding sections — each starts with finding-num containing question ID
    # Pattern: <div class="finding-num">HIPAA-001</div> or similar
    # Then evidence-block with file paths, then verdict-label with verdict

    # Find all question IDs and their positions
    qid_pattern = re.compile(r'class="finding-num">(\w+-\d+)')
    evidence_pattern = re.compile(r'class="evidence-block">(.*?)</div>', re.DOTALL)
    verdict_pattern = re.compile(r'class="verdict-label\s+v-(\w+)">(.*?)</div>')

    # Split content into chunks by finding-num
    qid_matches = list(qid_pattern.finditer(content))

    for i, qid_match in enumerate(qid_matches):
        qid = qid_match.group(1)
        start = qid_match.start()
        end = qid_matches[i + 1].start() if i + 1 < len(qid_matches) else len(content)
        chunk = content[start:end]

        # Extract framework from question ID (e.g. HIPAA-001 -> HIPAA)
        framework = qid.rsplit("-", 1)[0] if "-" in qid else qid

        # Extract evidence file paths from this chunk
        # Format: [SOURCE] path/to/file:123 or [CONFIG] path/to/file:456
        file_paths = re.findall(r'\[(?:SOURCE|CONFIG|DOCS)\]\s+([^\s:]+):\d+', chunk)

        # Extract verdict
        verdict_match = verdict_pattern.search(chunk)
        verdict = ""
        if verdict_match:
            v_class = verdict_match.group(1)
            verdict_map = {
                "confirmed": "CONFIRMED",
                "fp": "POSSIBLE FALSE POSITIVE",
                "context": "CONTEXT DEPENDENT",
                "additional": "ADDITIONAL RISK",
            }
            verdict = verdict_map.get(v_class, verdict_match.group(2).strip())

        if file_paths and verdict:
            findings.append({
                "framework": framework,
                "question_id": qid,
                "evidence_files": list(set(file_paths)),  # deduplicate
                "verdict": verdict,
            })

    return findings


def backfill():
    """Backfill evidence corpus from all existing HTML reports."""
    init_db()
    print("[Backfill] Starting corpus backfill from HTML reports...")

    total_patterns = 0
    for filename in sorted(os.listdir(REPORTS_DIR)):
        if not filename.endswith("_report.html"):
            continue
        if filename.startswith("failed_gate"):
            continue

        repo_key = filename.replace("_report.html", "")
        html_path = os.path.join(REPORTS_DIR, filename)
        domain = REPO_DOMAINS.get(repo_key, "")

        print(f"\n[Backfill] Parsing {filename}...")
        findings = parse_findings_from_html(html_path)
        print(f"  Found {len(findings)} findings with evidence + verdicts")

        for f in findings:
            record_evidence_patterns(
                f["framework"], f["question_id"],
                f["evidence_files"], f["verdict"], domain,
            )
            total_patterns += len(f["evidence_files"])

        # Show breakdown
        confirmed = sum(1 for f in findings if f["verdict"] == "CONFIRMED")
        fp = sum(1 for f in findings if f["verdict"] == "POSSIBLE FALSE POSITIVE")
        print(f"  Confirmed: {confirmed}, False Positive: {fp}")

    print(f"\n[Backfill] Complete. {total_patterns} evidence patterns recorded.")

    # Show corpus summary
    from scanner.database import _get_conn
    with _get_conn() as conn:
        row = conn.execute("SELECT COUNT(*) as cnt FROM evidence_patterns").fetchone()
        print(f"  Corpus size: {row['cnt']} unique patterns")
        rows = conn.execute(
            """SELECT framework, COUNT(*) as cnt, SUM(confirmed_count) as confirmed
               FROM evidence_patterns GROUP BY framework ORDER BY cnt DESC"""
        ).fetchall()
        for r in rows:
            print(f"    {r['framework']}: {r['cnt']} patterns, {r['confirmed']} confirmed")


if __name__ == "__main__":
    backfill()
