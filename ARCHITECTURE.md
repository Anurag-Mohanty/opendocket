# OpenDocket Architecture

## System Overview

OpenDocket is a compliance risk analysis tool that scans public GitHub repositories against regulatory frameworks and produces structured reports in legal brief format.

```
User Input (GitHub URL)
       |
       v
  Flask API Server (scanner/api.py)
       |
       v
  Clone + Qualify (scanner/repo_fetcher.py)
       |                    |
       v                    v
  Domain Detection     Qualification Gates
  (scanner/domain_detector.py)     (README, code count, data handling)
       |
       v
  Framework Mapping (scanner/compliance_mapper.py)
       |
       v
  Primary Scan — Claude Sonnet (scanner/agents/*.py)
       |
       v
  Independent Review — Gemini 1.5 Flash (scanner/agents/base_agent.py:JudgeAgent)
       |
       v
  Report Generation (scanner/report_generator.py)
       |
       v
  SQLite Persistence (scanner/database.py)
       |
       v
  HTML + Markdown Reports
```

## Dual Model Architecture

The independent review uses a different model from a different AI company. This is intentional.

**Claude finds the findings. Gemini challenges them.**

If both agree a pattern is high risk, the finding is more credible. If Gemini flags a false positive that Claude missed, you are protected from overstating risk. Independence requires genuine architectural separation.

- **Primary scan:** Claude Sonnet (Anthropic) — analyzes code evidence against each regulatory question
- **Independent review:** Gemini 1.5 Flash (Google) — challenges each finding for false positives, context dependency, and severity accuracy

This separation means:
1. No single vendor bias in findings
2. False positive detection is structurally independent
3. Over time, agreement rates between models produce a calibration score per framework

## Data Flow

### Scan Lifecycle

1. **Queued** — scan_id created, URL validated, rate limit checked
2. **Running: Cloning** — shallow git clone to temp directory
3. **Running: Domain Detection** — signal-based classification across 7 domains
4. **Running: Framework Mapping** — domain-to-framework mapping with cross-cutting rules
5. **Running: Primary Scan** — Claude analyzes evidence for each question per framework
6. **Running: Independent Review** — Gemini challenges each finding
7. **Complete** — reports generated, findings persisted, stats updated

### Clone Management

- All clones use `tempfile.mkdtemp()` with `opendocket_` prefix
- 500MB size gate — repos exceeding this are aborted
- `try/finally` guarantees cleanup via `shutil.rmtree`
- Clone size logged before cleanup

## Database Schema

SQLite database at `data/opendocket.db`.

- **scans** — scan metadata, status, scores, finding counts
- **findings** — individual findings with judge verdicts and confidence
- **stats** — aggregate counters (total scans, findings, judge overrides)
- **waitlist** — email signups for private repo scanning

Key design decision: `repo_url_hash` stores SHA-256 of the URL, never the raw URL. `repo_name` (owner/repo) is stored as public information.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/scan` | POST | Start a new scan |
| `/api/scan/:id` | GET | Get scan status and results |
| `/api/stats` | GET | Aggregate statistics |
| `/api/directory` | GET | Completed scans directory |
| `/api/waitlist` | POST | Email waitlist signup |
| `/api/recent` | GET | Recent scans for dashboard |

## Rate Limiting

- 3 scans per IP per hour for public scans
- BYOK (Bring Your Own Key) scans are unlimited
- Users can provide both Anthropic and Gemini keys
- If only Anthropic key provided: primary scan only, no review
- If both keys provided: full dual-model scan

## Question Library Schema

Each framework has a YAML question library with:

```yaml
framework: HIPAA
questions:
  - id: HIPAA-001
    category: PHI Identification
    legal_question: "..."
    regulatory_standard: "45 CFR §164.312(a)(1)"
    search_patterns: [...]
    absence_patterns: [...]
    evidence_guidance: "..."
```

## Scoring Methodology

OpenDocket Score (0-100, lower = more risk):

```
penalty = (high_risk * 8) + (medium_risk * 3) + (concern * 1)
normalized = penalty / num_frameworks * 2
score = max(0, 100 - normalized)
```

## Key Design Decisions

1. **Light mode UI** — Compliance tools need to feel professional and trustworthy. Dark mode signals developer toy.
2. **No stored code** — Repos are cloned to temp dirs and deleted after scanning. Code never persists.
3. **Dual model independence** — Different company, different model. This is the credibility of the review.
4. **YAML question libraries** — Anyone can contribute questions without touching Python code.
5. **Qualification gates** — Prevents noise from scanning repos with no code or no data handling.
