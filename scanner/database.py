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


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "opendocket.db")


def _ensure_db_dir():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


@contextmanager
def _get_conn():
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
                used_byok INTEGER DEFAULT 0,
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

            CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
            CREATE INDEX IF NOT EXISTS idx_events_ts ON events(timestamp);
            CREATE INDEX IF NOT EXISTS idx_scans_status ON scans(status);
            CREATE INDEX IF NOT EXISTS idx_scans_repo ON scans(repo_url_hash);
            CREATE INDEX IF NOT EXISTS idx_findings_scan ON findings(scan_id);
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
                "finding_high", "finding_medium", "finding_concern", "finding_ok",
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
            """SELECT repo_name, frameworks_triggered, opendocket_score,
                      finding_high, finding_medium, finding_concern, finding_ok,
                      report_url, timestamp
               FROM scans
               WHERE status = 'complete'
               ORDER BY timestamp DESC"""
        ).fetchall()
        results = []
        for row in rows:
            d = dict(row)
            if d.get("frameworks_triggered"):
                try:
                    d["frameworks_triggered"] = json.loads(d["frameworks_triggered"])
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
                      scan_duration_seconds, frameworks_triggered
               FROM scans
               ORDER BY timestamp DESC
               LIMIT ?""",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]
