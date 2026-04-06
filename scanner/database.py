"""
Database layer for OpenDocket scan persistence.

Uses SQLite for simplicity. Stores scan metadata, findings,
aggregate stats, and waitlist signups.
"""

import hashlib
import json
import os
import sqlite3
import uuid
from datetime import datetime, timedelta
from contextlib import contextmanager


# Database path — configurable via DATABASE_URL env var.
# SQLite (default): uses file path at data/opendocket.db
# When ready to migrate to Postgres: set DATABASE_URL=postgresql://...
# and swap this module's connection layer.
DATABASE_URL = os.environ.get("DATABASE_URL", "")
DB_PATH = os.environ.get("DB_PATH",
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "opendocket.db"))


def _ensure_db_dir():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


@contextmanager
def _get_conn():
    """Get a database connection. Currently SQLite, migration-ready for Postgres."""
    if DATABASE_URL.startswith("postgresql"):
        raise NotImplementedError(
            "Postgres support planned. Set DATABASE_URL to migrate. "
            "Migration script: scanner/migrate_to_postgres.py (TODO)"
        )
    _ensure_db_dir()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Create tables if they don't exist."""
    with _get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS scans (
                scan_id TEXT PRIMARY KEY,
                repo_url_hash TEXT NOT NULL,
                repo_name TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'queued',
                progress TEXT DEFAULT '',
                domains_detected TEXT DEFAULT '[]',
                frameworks_triggered TEXT DEFAULT '[]',
                lines_of_code INTEGER DEFAULT 0,
                files_scanned INTEGER DEFAULT 0,
                scan_duration_seconds REAL DEFAULT 0,
                opendocket_score INTEGER DEFAULT 0,
                finding_high INTEGER DEFAULT 0,
                finding_medium INTEGER DEFAULT 0,
                finding_concern INTEGER DEFAULT 0,
                finding_ok INTEGER DEFAULT 0,
                findings_total INTEGER DEFAULT 0,
                confirmed_total INTEGER DEFAULT 0,
                used_byok INTEGER DEFAULT 0,
                tokens_in INTEGER DEFAULT 0,
                tokens_out INTEGER DEFAULT 0,
                llm_calls INTEGER DEFAULT 0,
                error_message TEXT,
                report_url TEXT
            );

            CREATE TABLE IF NOT EXISTS findings (
                finding_id TEXT PRIMARY KEY,
                scan_id TEXT NOT NULL,
                framework TEXT NOT NULL,
                question_id TEXT NOT NULL,
                severity TEXT NOT NULL,
                judge_model TEXT DEFAULT '',
                judge_verdict TEXT DEFAULT '',
                judge_reasoning TEXT DEFAULT '',
                judge_confidence TEXT DEFAULT '',
                file_evidence_count INTEGER DEFAULT 0,
                FOREIGN KEY (scan_id) REFERENCES scans(scan_id)
            );

            CREATE TABLE IF NOT EXISTS stats (
                stat_key TEXT PRIMARY KEY,
                stat_value INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS waitlist (
                email TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                source TEXT DEFAULT 'web'
            );

            CREATE TABLE IF NOT EXISTS repo_scan_history (
                repo_name TEXT PRIMARY KEY,
                scan_ids TEXT DEFAULT '[]',
                first_scanned TEXT,
                last_scanned TEXT,
                finding_delta TEXT DEFAULT '{}'
            );

            CREATE TABLE IF NOT EXISTS events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                repo_name TEXT DEFAULT '',
                source TEXT DEFAULT '',
                timestamp TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS evidence_patterns (
                pattern_id INTEGER PRIMARY KEY AUTOINCREMENT,
                framework TEXT NOT NULL,
                question_id TEXT NOT NULL,
                file_glob TEXT NOT NULL,
                code_pattern TEXT DEFAULT '',
                domain TEXT DEFAULT '',
                hit_count INTEGER DEFAULT 0,
                miss_count INTEGER DEFAULT 0,
                confirmed_count INTEGER DEFAULT 0,
                fp_count INTEGER DEFAULT 0,
                last_updated TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS question_accuracy (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                framework TEXT NOT NULL,
                question_id TEXT NOT NULL,
                domain TEXT DEFAULT '',
                confirmed_count INTEGER DEFAULT 0,
                fp_count INTEGER DEFAULT 0,
                context_count INTEGER DEFAULT 0,
                total_scans INTEGER DEFAULT 0,
                common_fp_reasons TEXT DEFAULT '[]',
                last_updated TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS remediation_library (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                framework TEXT NOT NULL,
                question_id TEXT NOT NULL,
                domain TEXT DEFAULT '',
                remediation TEXT NOT NULL,
                source TEXT DEFAULT 'gemini',
                quality TEXT DEFAULT 'specific',
                use_count INTEGER DEFAULT 0,
                last_used TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS finding_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id TEXT NOT NULL,
                framework TEXT NOT NULL,
                question_id TEXT NOT NULL,
                verdict TEXT NOT NULL,
                reason TEXT DEFAULT '',
                submitted_at TEXT NOT NULL,
                FOREIGN KEY (scan_id) REFERENCES scans(scan_id)
            );

            CREATE TABLE IF NOT EXISTS visitors (
                visitor_id TEXT PRIMARY KEY,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL,
                visit_count INTEGER DEFAULT 1,
                pages_viewed TEXT DEFAULT '[]'
            );

            CREATE TABLE IF NOT EXISTS discovered_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                framework TEXT NOT NULL,
                category TEXT NOT NULL,
                search_hint TEXT NOT NULL,
                finding_text TEXT DEFAULT '',
                severity TEXT DEFAULT 'Medium Risk',
                occurrences INTEGER DEFAULT 1,
                repos_seen TEXT DEFAULT '[]',
                status TEXT DEFAULT 'candidate',
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_discovered_fw ON discovered_patterns(framework);
            CREATE INDEX IF NOT EXISTS idx_discovered_status ON discovered_patterns(status);
            CREATE INDEX IF NOT EXISTS idx_feedback_scan ON finding_feedback(scan_id);
            CREATE INDEX IF NOT EXISTS idx_visitors_last ON visitors(last_seen);
            CREATE INDEX IF NOT EXISTS idx_qa_fw_q ON question_accuracy(framework, question_id);
            CREATE INDEX IF NOT EXISTS idx_qa_domain ON question_accuracy(domain);
            CREATE INDEX IF NOT EXISTS idx_remediation_fw_q ON remediation_library(framework, question_id);
            CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
            CREATE INDEX IF NOT EXISTS idx_events_ts ON events(timestamp);
            CREATE INDEX IF NOT EXISTS idx_scans_status ON scans(status);
            CREATE INDEX IF NOT EXISTS idx_scans_repo ON scans(repo_url_hash);
            CREATE INDEX IF NOT EXISTS idx_findings_scan ON findings(scan_id);
            CREATE INDEX IF NOT EXISTS idx_evidence_fw_q ON evidence_patterns(framework, question_id);
        """)

        # Initialize stats if empty
        for key in [
            "total_scans", "total_repos_unique", "total_lines_scanned",
            "total_findings", "high_risk_findings", "judge_false_positives",
            "judge_confirmed", "judge_context_dependent", "judge_additional_risk",
            "scans_today", "scans_this_month",
        ]:
            conn.execute(
                "INSERT OR IGNORE INTO stats (stat_key, stat_value) VALUES (?, 0)",
                (key,),
            )

        # Migrations for existing databases
        for col in ["findings_total", "confirmed_total"]:
            try:
                conn.execute(f"ALTER TABLE scans ADD COLUMN {col} INTEGER DEFAULT 0")
            except Exception:
                pass  # Column already exists


def create_scan(repo_url: str, repo_name: str, used_byok: bool = False) -> str:
    """Create a new scan record. Returns the scan_id."""
    scan_id = str(uuid.uuid4())
    url_hash = hashlib.sha256(repo_url.encode()).hexdigest()
    with _get_conn() as conn:
        conn.execute(
            """INSERT INTO scans (scan_id, repo_url_hash, repo_name, timestamp, status, used_byok)
               VALUES (?, ?, ?, ?, 'queued', ?)""",
            (scan_id, url_hash, repo_name, datetime.utcnow().isoformat(), int(used_byok)),
        )
    return scan_id


def update_scan_status(scan_id: str, status: str, progress: str = "", **kwargs):
    """Update scan status and optional fields."""
    with _get_conn() as conn:
        conn.execute(
            "UPDATE scans SET status = ?, progress = ? WHERE scan_id = ?",
            (status, progress, scan_id),
        )
        for key, value in kwargs.items():
            if key in (
                "domains_detected", "frameworks_triggered", "lines_of_code",
                "files_scanned", "scan_duration_seconds", "opendocket_score",
                "finding_high", "finding_medium", "finding_concern", "finding_ok", "findings_total", "confirmed_total",
                "tokens_in", "tokens_out", "llm_calls",
                "error_message", "report_url",
            ):
                if isinstance(value, (list, dict)):
                    value = json.dumps(value)
                conn.execute(
                    f"UPDATE scans SET {key} = ? WHERE scan_id = ?",
                    (value, scan_id),
                )


def save_findings(scan_id: str, findings_data: list[dict]):
    """Save finding records for a scan."""
    with _get_conn() as conn:
        for f in findings_data:
            conn.execute(
                """INSERT INTO findings (finding_id, scan_id, framework, question_id,
                   severity, judge_model, judge_verdict, judge_reasoning,
                   judge_confidence, file_evidence_count)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    str(uuid.uuid4()),
                    scan_id,
                    f.get("framework", ""),
                    f.get("question_id", ""),
                    f.get("severity", ""),
                    f.get("judge_model", ""),
                    f.get("judge_verdict", ""),
                    f.get("judge_reasoning", ""),
                    f.get("judge_confidence", ""),
                    f.get("file_evidence_count", 0),
                ),
            )


def delete_scan(scan_id: str) -> bool:
    """Delete a scan and its findings. Returns True if found and deleted."""
    with _get_conn() as conn:
        row = conn.execute("SELECT scan_id FROM scans WHERE scan_id = ?", (scan_id,)).fetchone()
        if not row:
            return False
        conn.execute("DELETE FROM findings WHERE scan_id = ?", (scan_id,))
        conn.execute("DELETE FROM scans WHERE scan_id = ?", (scan_id,))
        return True


def get_scan(scan_id: str) -> dict | None:
    """Get a scan record by ID."""
    with _get_conn() as conn:
        row = conn.execute("SELECT * FROM scans WHERE scan_id = ?", (scan_id,)).fetchone()
        if row:
            d = dict(row)
            for json_field in ("domains_detected", "frameworks_triggered"):
                if d.get(json_field):
                    try:
                        d[json_field] = json.loads(d[json_field])
                    except (json.JSONDecodeError, TypeError):
                        pass
            return d
    return None


def get_stats() -> dict:
    """Get aggregate stats."""
    with _get_conn() as conn:
        rows = conn.execute("SELECT stat_key, stat_value FROM stats").fetchall()
        return {row["stat_key"]: row["stat_value"] for row in rows}


def increment_stat(key: str, amount: int = 1):
    """Increment a stat counter."""
    with _get_conn() as conn:
        conn.execute(
            "UPDATE stats SET stat_value = stat_value + ? WHERE stat_key = ?",
            (amount, key),
        )


def add_to_waitlist(email: str, source: str = "web") -> bool:
    """Add email to waitlist. Returns True if new, False if duplicate."""
    with _get_conn() as conn:
        try:
            conn.execute(
                "INSERT INTO waitlist (email, timestamp, source) VALUES (?, ?, ?)",
                (email, datetime.utcnow().isoformat(), source),
            )
            return True
        except sqlite3.IntegrityError:
            return False


def get_directory_with_scores() -> list[dict]:
    """Get all completed scans for the directory."""
    with _get_conn() as conn:
        rows = conn.execute(
            """SELECT scan_id, repo_name, frameworks_triggered, domains_detected,
                      opendocket_score, finding_high, finding_medium, finding_concern,
                      finding_ok, findings_total, confirmed_total, report_url, timestamp, error_message
               FROM scans
               WHERE status = 'complete'
               ORDER BY timestamp DESC"""
        ).fetchall()
        results = []
        for row in rows:
            d = dict(row)
            for jf in ("frameworks_triggered", "domains_detected"):
                if d.get(jf):
                    try:
                        d[jf] = json.loads(d[jf])
                    except (json.JSONDecodeError, TypeError):
                        pass
            results.append(d)
        return results


def track_event(event_type: str, repo_name: str = "", source: str = ""):
    """Track an analytics event. Never stores IP addresses."""
    with _get_conn() as conn:
        conn.execute(
            "INSERT INTO events (event_type, repo_name, source, timestamp) VALUES (?, ?, ?, ?)",
            (event_type, repo_name, source, datetime.utcnow().isoformat()),
        )


def get_event_counts(days: int = 7) -> dict:
    """Get event counts for the last N days."""
    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT event_type, COUNT(*) as cnt FROM events WHERE timestamp > ? GROUP BY event_type",
            (cutoff,),
        ).fetchall()
        counts = {row["event_type"]: row["cnt"] for row in rows}
        # Top repos by views
        repo_rows = conn.execute(
            """SELECT repo_name, COUNT(*) as cnt FROM events
               WHERE timestamp > ? AND event_type = 'report_open' AND repo_name != ''
               GROUP BY repo_name ORDER BY cnt DESC LIMIT 10""",
            (cutoff,),
        ).fetchall()
        counts["top_repos"] = [{"repo": r["repo_name"], "views": r["cnt"]} for r in repo_rows]
        return counts


def update_repo_history(repo_name: str, scan_id: str):
    """Track scan history for a repo."""
    now = datetime.utcnow().isoformat()
    with _get_conn() as conn:
        row = conn.execute("SELECT * FROM repo_scan_history WHERE repo_name = ?", (repo_name,)).fetchone()
        if row:
            scan_ids = json.loads(row["scan_ids"] or "[]")
            scan_ids.append(scan_id)
            conn.execute(
                "UPDATE repo_scan_history SET scan_ids = ?, last_scanned = ? WHERE repo_name = ?",
                (json.dumps(scan_ids), now, repo_name),
            )
        else:
            conn.execute(
                "INSERT INTO repo_scan_history (repo_name, scan_ids, first_scanned, last_scanned) VALUES (?, ?, ?, ?)",
                (repo_name, json.dumps([scan_id]), now, now),
            )


def compare_scans(scan_id_1: str, scan_id_2: str) -> dict:
    """Compare two scans of the same repo. Returns resolved/new/unchanged."""
    with _get_conn() as conn:
        rows1 = conn.execute("SELECT question_id, severity FROM findings WHERE scan_id = ?", (scan_id_1,)).fetchall()
        rows2 = conn.execute("SELECT question_id, severity FROM findings WHERE scan_id = ?", (scan_id_2,)).fetchall()

    ids1 = {r["question_id"] for r in rows1}
    ids2 = {r["question_id"] for r in rows2}
    high1 = sum(1 for r in rows1 if r["severity"] == "High Risk")
    high2 = sum(1 for r in rows2 if r["severity"] == "High Risk")

    resolved = sorted(ids1 - ids2)
    new = sorted(ids2 - ids1)
    unchanged = sorted(ids1 & ids2)
    improvement = round((high1 - high2) / max(high1, 1) * 100) if high1 > 0 else 0

    return {
        "resolved": resolved,
        "new": new,
        "unchanged": unchanged,
        "improvement": improvement,
        "prev_high": high1,
        "curr_high": high2,
    }


def get_repo_history(repo_name: str) -> dict | None:
    """Get scan history for a repo."""
    with _get_conn() as conn:
        row = conn.execute("SELECT * FROM repo_scan_history WHERE repo_name = ?", (repo_name,)).fetchone()
        if row:
            d = dict(row)
            d["scan_ids"] = json.loads(d.get("scan_ids", "[]"))
            return d
    return None


def get_recent_scan(repo_name: str, hours: int = 24) -> dict | None:
    """Get a recent completed scan for a repo within the last N hours."""
    cutoff = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
    with _get_conn() as conn:
        row = conn.execute(
            """SELECT * FROM scans
               WHERE repo_name = ? AND status = 'complete' AND timestamp > ?
               ORDER BY timestamp DESC LIMIT 1""",
            (repo_name, cutoff),
        ).fetchone()
        if row:
            d = dict(row)
            for jf in ("domains_detected", "frameworks_triggered"):
                if d.get(jf):
                    try:
                        d[jf] = json.loads(d[jf])
                    except (json.JSONDecodeError, TypeError):
                        pass
            return d
    return None


def get_recent_scans(limit: int = 20) -> list[dict]:
    """Get recent scans for the dashboard."""
    with _get_conn() as conn:
        rows = conn.execute(
            """SELECT scan_id, repo_name, status, timestamp, opendocket_score,
                      finding_high, finding_medium, finding_concern, finding_ok,
                      scan_duration_seconds, frameworks_triggered,
                      tokens_in, tokens_out, llm_calls
               FROM scans
               ORDER BY timestamp DESC
               LIMIT ?""",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]


# ── Evidence Pattern Corpus ──

def record_evidence_patterns(framework: str, question_id: str, evidence_files: list[str],
                              verdict: str, domain: str = ""):
    """Record which file patterns produced evidence for a finding.

    Called after each confirmed/FP finding to build the learned corpus.
    Extracts directory-level globs from actual evidence paths.
    """
    now = datetime.utcnow().isoformat()
    is_confirmed = verdict == "CONFIRMED"

    # Extract directory-level globs from evidence paths
    # e.g. "src/auth/session.ts" → "src/auth/**"
    globs = set()
    for fpath in evidence_files:
        parts = fpath.replace("\\", "/").split("/")
        if len(parts) >= 2:
            globs.add("/".join(parts[:2]) + "/**")
        elif len(parts) == 1:
            ext = os.path.splitext(parts[0])[1]
            globs.add(f"*{ext}" if ext else parts[0])

    with _get_conn() as conn:
        for glob in globs:
            row = conn.execute(
                """SELECT pattern_id FROM evidence_patterns
                   WHERE framework = ? AND question_id = ? AND file_glob = ?""",
                (framework, question_id, glob),
            ).fetchone()

            if row:
                if is_confirmed:
                    conn.execute(
                        """UPDATE evidence_patterns
                           SET hit_count = hit_count + 1, confirmed_count = confirmed_count + 1,
                               last_updated = ? WHERE pattern_id = ?""",
                        (now, row["pattern_id"]),
                    )
                else:
                    conn.execute(
                        """UPDATE evidence_patterns
                           SET hit_count = hit_count + 1, fp_count = fp_count + 1,
                               last_updated = ? WHERE pattern_id = ?""",
                        (now, row["pattern_id"]),
                    )
            else:
                conn.execute(
                    """INSERT INTO evidence_patterns
                       (framework, question_id, file_glob, domain,
                        hit_count, confirmed_count, fp_count, last_updated)
                       VALUES (?, ?, ?, ?, 1, ?, ?, ?)""",
                    (framework, question_id, glob, domain,
                     1 if is_confirmed else 0,
                     0 if is_confirmed else 1,
                     now),
                )


def get_priority_globs(framework: str, question_id: str, limit: int = 10) -> list[dict]:
    """Get the highest-signal file globs for a question, ordered by confirmation rate.

    Returns globs where evidence was most often confirmed (not FP),
    so agents can search these paths first.
    """
    with _get_conn() as conn:
        rows = conn.execute(
            """SELECT file_glob, hit_count, confirmed_count, fp_count,
                      CAST(confirmed_count AS REAL) / MAX(hit_count, 1) as confirm_rate
               FROM evidence_patterns
               WHERE framework = ? AND question_id = ? AND confirmed_count > 0
               ORDER BY confirm_rate DESC, confirmed_count DESC
               LIMIT ?""",
            (framework, question_id, limit),
        ).fetchall()
        return [dict(r) for r in rows]


# ── Question Accuracy Tracking ──

def record_question_accuracy(framework: str, question_id: str, verdict: str,
                              domain: str = "", fp_reason: str = ""):
    """Track per-question confirmation/FP rates by domain.

    Called after each judged finding. Aggregates accuracy data
    so reports can show confidence context to readers.
    """
    now = datetime.utcnow().isoformat()

    with _get_conn() as conn:
        row = conn.execute(
            """SELECT id, common_fp_reasons FROM question_accuracy
               WHERE framework = ? AND question_id = ? AND domain = ?""",
            (framework, question_id, domain),
        ).fetchone()

        if row:
            if verdict == "CONFIRMED":
                conn.execute(
                    """UPDATE question_accuracy
                       SET confirmed_count = confirmed_count + 1, total_scans = total_scans + 1,
                           last_updated = ? WHERE id = ?""",
                    (now, row["id"]),
                )
            elif verdict == "POSSIBLE FALSE POSITIVE":
                reasons = json.loads(row["common_fp_reasons"] or "[]")
                if fp_reason and fp_reason not in reasons:
                    reasons.append(fp_reason)
                    if len(reasons) > 10:
                        reasons = reasons[-10:]
                conn.execute(
                    """UPDATE question_accuracy
                       SET fp_count = fp_count + 1, total_scans = total_scans + 1,
                           common_fp_reasons = ?, last_updated = ? WHERE id = ?""",
                    (json.dumps(reasons), now, row["id"]),
                )
            elif verdict == "CONTEXT DEPENDENT":
                conn.execute(
                    """UPDATE question_accuracy
                       SET context_count = context_count + 1, total_scans = total_scans + 1,
                           last_updated = ? WHERE id = ?""",
                    (now, row["id"]),
                )
        else:
            reasons = json.dumps([fp_reason] if fp_reason else [])
            conn.execute(
                """INSERT INTO question_accuracy
                   (framework, question_id, domain, confirmed_count, fp_count,
                    context_count, total_scans, common_fp_reasons, last_updated)
                   VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?)""",
                (framework, question_id, domain,
                 1 if verdict == "CONFIRMED" else 0,
                 1 if verdict == "POSSIBLE FALSE POSITIVE" else 0,
                 1 if verdict == "CONTEXT DEPENDENT" else 0,
                 reasons, now),
            )


def get_question_accuracy(framework: str, question_id: str) -> dict:
    """Get accuracy stats for a question across all domains."""
    with _get_conn() as conn:
        row = conn.execute(
            """SELECT SUM(confirmed_count) as confirmed, SUM(fp_count) as fp,
                      SUM(context_count) as context, SUM(total_scans) as total
               FROM question_accuracy
               WHERE framework = ? AND question_id = ?""",
            (framework, question_id),
        ).fetchone()
        if not row or not row["total"]:
            return {"confirmed": 0, "fp": 0, "context": 0, "total": 0,
                    "confirm_rate": 0, "fp_reasons": []}

        total = row["total"]
        confirmed = row["confirmed"] or 0

        reason_rows = conn.execute(
            """SELECT common_fp_reasons FROM question_accuracy
               WHERE framework = ? AND question_id = ? AND common_fp_reasons != '[]'""",
            (framework, question_id),
        ).fetchall()
        all_reasons = []
        for r in reason_rows:
            try:
                all_reasons.extend(json.loads(r["common_fp_reasons"]))
            except (json.JSONDecodeError, TypeError):
                pass
        unique_reasons = list(dict.fromkeys(all_reasons))[:5]

        return {
            "confirmed": confirmed,
            "fp": row["fp"] or 0,
            "context": row["context"] or 0,
            "total": total,
            "confirm_rate": round(confirmed / max(total, 1) * 100),
            "fp_reasons": unique_reasons,
        }


def get_cross_repo_confidence(framework: str, question_id: str, domain: str = "") -> dict:
    """Get cross-repo finding correlation — how often this question is confirmed
    in repos with similar domain profiles."""
    with _get_conn() as conn:
        overall = conn.execute(
            """SELECT SUM(confirmed_count) as confirmed, SUM(total_scans) as total
               FROM question_accuracy WHERE framework = ? AND question_id = ?""",
            (framework, question_id),
        ).fetchone()

        domain_row = None
        if domain:
            primary_domain = domain.split(",")[0].strip()
            domain_row = conn.execute(
                """SELECT confirmed_count, fp_count, total_scans
                   FROM question_accuracy
                   WHERE framework = ? AND question_id = ? AND domain LIKE ?""",
                (framework, question_id, f"%{primary_domain}%"),
            ).fetchone()

        result = {
            "overall_confirmed": (overall["confirmed"] or 0) if overall else 0,
            "overall_total": (overall["total"] or 0) if overall else 0,
            "overall_rate": 0,
        }
        if result["overall_total"] > 0:
            result["overall_rate"] = round(result["overall_confirmed"] / result["overall_total"] * 100)

        if domain_row:
            dtotal = domain_row["total_scans"] or 0
            result["domain_confirmed"] = domain_row["confirmed_count"] or 0
            result["domain_total"] = dtotal
            result["domain_rate"] = round((domain_row["confirmed_count"] or 0) / max(dtotal, 1) * 100)

        return result


# ── Remediation Library ──

def store_remediation(framework: str, question_id: str, remediation: str,
                       domain: str = "", quality: str = "specific", source: str = "gemini"):
    """Store an improved remediation for future reuse."""
    now = datetime.utcnow().isoformat()
    with _get_conn() as conn:
        row = conn.execute(
            """SELECT id FROM remediation_library
               WHERE framework = ? AND question_id = ? AND domain = ?""",
            (framework, question_id, domain),
        ).fetchone()
        if row:
            conn.execute(
                """UPDATE remediation_library
                   SET remediation = ?, quality = ?, source = ?,
                       use_count = use_count + 1, last_used = ?
                   WHERE id = ?""",
                (remediation, quality, source, now, row["id"]),
            )
        else:
            conn.execute(
                """INSERT INTO remediation_library
                   (framework, question_id, domain, remediation, source, quality, use_count, last_used)
                   VALUES (?, ?, ?, ?, ?, ?, 1, ?)""",
                (framework, question_id, domain, remediation, source, quality, now),
            )


def get_best_remediation(framework: str, question_id: str, domain: str = "") -> str | None:
    """Get the best stored remediation — prefers domain-specific, then any."""
    with _get_conn() as conn:
        if domain:
            primary_domain = domain.split(",")[0].strip()
            row = conn.execute(
                """SELECT remediation FROM remediation_library
                   WHERE framework = ? AND question_id = ? AND domain LIKE ?
                   AND quality = 'specific'
                   ORDER BY use_count DESC LIMIT 1""",
                (framework, question_id, f"%{primary_domain}%"),
            ).fetchone()
            if row:
                return row["remediation"]

        row = conn.execute(
            """SELECT remediation FROM remediation_library
               WHERE framework = ? AND question_id = ? AND quality = 'specific'
               ORDER BY use_count DESC LIMIT 1""",
            (framework, question_id),
        ).fetchone()
        return row["remediation"] if row else None


# ── Discovered Patterns (from wildcard scans) ──

def store_discovered_pattern(framework: str, category: str, search_hint: str,
                              finding_text: str = "", severity: str = "Medium Risk",
                              repo_name: str = ""):
    """Store a novel pattern discovered by the wildcard scan.

    Deduplicates by matching framework + search_hint (fuzzy).
    Tracks how many repos independently surfaced this pattern.
    Patterns seen in 3+ repos become 'promoted' candidates for
    addition to the question library.
    """
    now = datetime.utcnow().isoformat()
    hint_lower = search_hint.lower().strip()

    with _get_conn() as conn:
        # Check for existing similar pattern (same framework, similar hint)
        rows = conn.execute(
            """SELECT id, search_hint, repos_seen, occurrences FROM discovered_patterns
               WHERE framework = ? AND status != 'rejected'""",
            (framework,),
        ).fetchall()

        for row in rows:
            existing_hint = row["search_hint"].lower().strip()
            # Match if hints overlap significantly (substring match)
            if hint_lower in existing_hint or existing_hint in hint_lower:
                repos = json.loads(row["repos_seen"] or "[]")
                if repo_name and repo_name not in repos:
                    repos.append(repo_name)
                new_occ = row["occurrences"] + 1
                # Auto-promote if seen in 3+ different repos
                conn.execute(
                    """UPDATE discovered_patterns
                       SET occurrences = ?, repos_seen = ?, last_seen = ?,
                           status = 'active' WHERE id = ?""",
                    (new_occ, json.dumps(repos), now, row["id"]),
                )
                return

        # New pattern — add immediately and auto-add to question library
        repos = json.dumps([repo_name] if repo_name else [])
        conn.execute(
            """INSERT INTO discovered_patterns
               (framework, category, search_hint, finding_text, severity,
                occurrences, repos_seen, status, first_seen, last_seen)
               VALUES (?, ?, ?, ?, ?, 1, ?, 'active', ?, ?)""",
            (framework, category, search_hint, finding_text, severity,
             repos, now, now),
        )
        _auto_add_question(framework, search_hint, category, finding_text, severity)


def _auto_add_question(framework: str, search_hint: str, category: str,
                        finding_text: str, severity: str):
    """Auto-append a discovered pattern as a new question to the framework YAML."""
    import yaml as _yaml

    # Map framework name to YAML file
    fw_lower = framework.lower().replace("-", "_")
    config_dir = os.path.join(os.path.dirname(__file__), "config")
    yaml_path = os.path.join(config_dir, f"{fw_lower}_questions.yaml")

    if not os.path.exists(yaml_path):
        print(f"  [Auto-add] YAML not found: {yaml_path}")
        return

    try:
        with open(yaml_path, "r") as f:
            config = _yaml.safe_load(f)

        questions = config.get("questions", [])
        existing_ids = {q["id"] for q in questions}

        # Generate next ID
        max_num = 0
        prefix = framework.upper().replace("_", "") + "-"
        for qid in existing_ids:
            if qid.startswith(prefix):
                try:
                    num = int(qid.replace(prefix, ""))
                    max_num = max(max_num, num)
                except ValueError:
                    pass
        new_id = f"{prefix}{max_num + 1:03d}"

        # Check dedup — don't add if search_hint already exists in any question's patterns
        all_patterns = set()
        for q in questions:
            for p in q.get("search_patterns", []):
                all_patterns.add(p.lower())
        if search_hint.lower() in all_patterns:
            print(f"  [Auto-add] Pattern '{search_hint}' already in {framework} library")
            return

        new_question = {
            "id": new_id,
            "category": f"[Discovered] {category}",
            "legal_question": finding_text or f"Does this system have adequate controls for {category}?",
            "regulatory_standard": config.get("full_name", framework),
            "search_patterns": [search_hint],
            "absence_patterns": [],
        }

        questions.append(new_question)
        config["questions"] = questions

        with open(yaml_path, "w") as f:
            _yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        print(f"  [Auto-add] Added {new_id} to {framework}: {category} (hint: {search_hint})")
    except Exception as e:
        print(f"  [Auto-add] Failed for {framework}: {e}")


def get_discovered_patterns(framework: str = "", status: str = "") -> list[dict]:
    """Get discovered patterns, optionally filtered by framework/status."""
    with _get_conn() as conn:
        query = "SELECT * FROM discovered_patterns WHERE 1=1"
        params = []
        if framework:
            query += " AND framework = ?"
            params.append(framework)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY occurrences DESC, last_seen DESC"
        rows = conn.execute(query, params).fetchall()
        results = []
        for r in rows:
            d = dict(r)
            try:
                d["repos_seen"] = json.loads(d.get("repos_seen", "[]"))
            except (json.JSONDecodeError, TypeError):
                pass
            results.append(d)
        return results


# ── Finding Feedback ──

def save_feedback(scan_id: str, framework: str, question_id: str,
                   verdict: str, reason: str = "") -> int:
    """Save human feedback on a finding. Returns the feedback ID."""
    now = datetime.utcnow().isoformat()
    with _get_conn() as conn:
        cursor = conn.execute(
            """INSERT INTO finding_feedback
               (scan_id, framework, question_id, verdict, reason, submitted_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (scan_id, framework, question_id, verdict, reason, now),
        )
        return cursor.lastrowid


def get_feedback_for_scan(scan_id: str) -> list[dict]:
    """Get all feedback for a scan."""
    with _get_conn() as conn:
        rows = conn.execute(
            """SELECT * FROM finding_feedback WHERE scan_id = ?
               ORDER BY submitted_at DESC""",
            (scan_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def get_feedback_stats() -> dict:
    """Get aggregate feedback stats."""
    with _get_conn() as conn:
        row = conn.execute(
            """SELECT COUNT(*) as total,
                      SUM(CASE WHEN verdict = 'incorrect' THEN 1 ELSE 0 END) as incorrect,
                      SUM(CASE WHEN verdict = 'correct' THEN 1 ELSE 0 END) as correct
               FROM finding_feedback"""
        ).fetchone()
        return dict(row) if row else {"total": 0, "incorrect": 0, "correct": 0}


# ── Visitor Tracking ──

def record_visitor(visitor_id: str, page: str = ""):
    """Record a unique visitor. Privacy-safe: ID is a random client-generated hash."""
    now = datetime.utcnow().isoformat()
    with _get_conn() as conn:
        row = conn.execute(
            "SELECT visitor_id, pages_viewed FROM visitors WHERE visitor_id = ?",
            (visitor_id,),
        ).fetchone()
        if row:
            pages = json.loads(row["pages_viewed"] or "[]")
            if page and page not in pages:
                pages.append(page)
                if len(pages) > 20:
                    pages = pages[-20:]
            conn.execute(
                """UPDATE visitors SET last_seen = ?, visit_count = visit_count + 1,
                   pages_viewed = ? WHERE visitor_id = ?""",
                (now, json.dumps(pages), visitor_id),
            )
        else:
            conn.execute(
                """INSERT INTO visitors (visitor_id, first_seen, last_seen, visit_count, pages_viewed)
                   VALUES (?, ?, ?, 1, ?)""",
                (visitor_id, now, now, json.dumps([page] if page else [])),
            )


def get_visitor_stats() -> dict:
    """Get visitor metrics."""
    with _get_conn() as conn:
        total = conn.execute("SELECT COUNT(*) as cnt FROM visitors").fetchone()
        today = conn.execute(
            "SELECT COUNT(*) as cnt FROM visitors WHERE last_seen > datetime('now', '-1 day')"
        ).fetchone()
        week = conn.execute(
            "SELECT COUNT(*) as cnt FROM visitors WHERE last_seen > datetime('now', '-7 days')"
        ).fetchone()
        month = conn.execute(
            "SELECT COUNT(*) as cnt FROM visitors WHERE last_seen > datetime('now', '-30 days')"
        ).fetchone()
        returning = conn.execute(
            "SELECT COUNT(*) as cnt FROM visitors WHERE visit_count > 1"
        ).fetchone()
        return {
            "total": total["cnt"] if total else 0,
            "today": today["cnt"] if today else 0,
            "this_week": week["cnt"] if week else 0,
            "this_month": month["cnt"] if month else 0,
            "returning": returning["cnt"] if returning else 0,
        }
