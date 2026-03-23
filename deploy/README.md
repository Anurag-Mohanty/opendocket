# Deploying OpenDocket

## Quick Start (Docker)

```bash
docker build -t opendocket .
docker run -p 5001:5001 \
  -e ANTHROPIC_API_KEY=your-key \
  -e GEMINI_API_KEY=your-key \
  -v opendocket-data:/app/data \
  opendocket
```

Visit http://localhost:5001

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Claude API key for primary scanning |
| `GEMINI_API_KEY` | Yes | Gemini API key for independent review |
| `PORT` | No | Server port (default: 5001) |
| `FLASK_DEBUG` | No | Set to "1" for debug mode |

## Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Edit with your keys
source .env
python scanner/api.py
```

## Production Notes

- SQLite database stored at `data/opendocket.db`
- Mount `data/` as a persistent volume
- Rate limit: 3 scans/hour per IP (BYOK unlimited)
- Clone temp files auto-cleaned after each scan
- 500MB clone size limit enforced
