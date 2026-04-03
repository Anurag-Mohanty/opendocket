# Deploy OpenDocket Backend to Railway

## Quick Setup

1. Go to railway.app and sign up (free tier available)
2. New Project > Deploy from GitHub repo
3. Select your opendocket repo
4. Set root directory: `/` (root)
5. Set start command: `python scanner/api.py`
6. Add environment variables:
   - `ANTHROPIC_API_KEY=your_key`
   - `GEMINI_API_KEY=your_key`
   - `PORT=8080`
   - `DAILY_SCAN_LIMIT=200`
   - `MONTHLY_SCAN_LIMIT=2000`
7. Railway will give you a URL like:
   `https://opendocket-production.up.railway.app`
8. Update `API_BASE_URL` in `docs/index.html` to this URL

## Persistent Storage (Required)

The SQLite database must survive deploys. Add a Railway volume:

1. Click on your service in Railway dashboard
2. Go to **Settings** → **Volumes**
3. Click **Add Volume**
4. Set mount path: `/app/data`
5. Size: 1 GB (sufficient for thousands of scans)
6. Redeploy

The `railway.toml` in this repo declares the mount, but you still need
to create the volume in the Railway UI.

### What's stored in /app/data (no repo code):
- Scan metadata, scores, duration (~1KB per scan)
- Findings with judge verdicts (~5KB per scan)
- Evidence pattern corpus for search priority (~100KB)
- Question accuracy rates and FP reasoning (~50KB)
- Discovered patterns and remediation library (~20KB)
- Visitor tracking and feedback (~grows slowly)

Total: ~131KB currently, estimated ~10MB after 1000 scans.

## Scaling Path

SQLite is good up to ~1000 scans/day or ~10K daily visitors.

When you outgrow it:
1. Add Railway Postgres: `railway add --database postgres`
2. Set `DATABASE_URL` env var to the Postgres connection string
3. Run `python scanner/migrate_to_postgres.py` (one-time migration)
4. The app auto-detects `DATABASE_URL` and switches

All SQL in database.py uses standard SQL compatible with both
SQLite and Postgres (no SQLite-specific syntax).
