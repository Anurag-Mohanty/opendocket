# OpenDocket Architecture

## System Overview

```
User Input (GitHub URL)
       |
       v
  Flask API Server (scanner/api.py)
       |
       v
  Clone + Qualify (scanner/repo_fetcher.py)
       |
       v
  Domain Detection (scanner/domain_detector.py)
       |
       v
  Framework Mapping (scanner/compliance_mapper.py)
       |
       v
  ┌─────────────────────────────────────────┐
  │  Compliance Agents (3 concurrent)       │
  │  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
  │  │ HIPAA   │ │ SOC2    │ │ PCI-DSS │   │
  │  │ Agent   │ │ Agent   │ │ Agent   │   │
  │  └─────────┘ └─────────┘ └─────────┘   │
  │       ↕            ↕           ↕        │
  │    Evidence     Evidence    Evidence     │
  │    Pattern      Pattern     Pattern      │
  │    Corpus       Corpus      Corpus       │
  │  (search priority from previous scans)  │
  │                                         │
  │  Each agent runs:                       │
  │  1. Standard questions (from YAML)      │
  │  2. Discovered questions (auto-added)   │
  │  3. Wildcard pass (novel risk detect)   │
  └─────────────────────────────────────────┘
       |
       v
  ┌─────────────────────────────────────────┐
  │  Gemini Independent Review              │
  │  (5 concurrent workers)                 │
  │                                         │
  │  Each finding challenged as:            │
  │  CONFIRMED | CONTEXT DEPENDENT |        │
  │  POSSIBLE FALSE POSITIVE | ADDITIONAL   │
  └─────────────────────────────────────────┘
       |
       v
  ┌─────────────────────────────────────────┐
  │  Intelligence Recording                 │
  │                                         │
  │  - Evidence file patterns → corpus      │
  │  - Question accuracy rates → tracking   │
  │  - FP reasoning → transparency          │
  │  - Improved remediations → library      │
  │  - Novel patterns → auto-add to YAML    │
  └─────────────────────────────────────────┘
       |
       v
  Report Generation + SQLite Persistence
       |
       v
  HTML Report (with feedback buttons +
               cross-repo confidence context)
```

## Dual Model Architecture

**Claude finds the findings. Gemini challenges them.**

- **Primary scan:** Claude Sonnet 4 (Anthropic, temperature=0) — deterministic analysis of code evidence against regulatory questions
- **Independent review:** Gemini 2.5 Flash (Google, 5 concurrent workers) — challenges each finding for false positives, context dependency, and severity accuracy

This separation means:
1. No single vendor bias in findings
2. False positive detection is structurally independent
3. Deterministic output (temperature=0) ensures scan-to-scan consistency

## Concurrency Model

| Component | Concurrency | Rationale |
|-----------|------------|-----------|
| Framework agents | 3 concurrent (ThreadPoolExecutor) | Agents are stateless, share read-only file index |
| Gemini review | 5 concurrent (ThreadPoolExecutor) | Each review is independent, API supports parallelism |
| Scan threads | 1 per scan (daemon thread) | Scans are long-running, don't block the API |

## Intelligence System

The system improves with every scan through five data stores:

### Evidence Pattern Corpus (`evidence_patterns` table)
- **What:** Directory-level file globs that produced evidence, tagged confirmed/FP
- **How it helps:** Agents search high-confidence paths first; combined with `max_results` early exit, finds evidence faster
- **Key design:** Reorders search, never filters. All files still get searched — no false negatives from corpus bias

### Question Accuracy (`question_accuracy` table)
- **What:** Per-question confirmation/FP rates by domain, with FP reasoning from Gemini
- **How it helps:** Shown in reports as "Confirmed in X% of scans" for reader calibration
- **Key design:** Never injected into Claude's prompts. Readers calibrate; the model evaluates with fresh eyes. This prevents feedback-loop bias.

### Discovered Patterns (`discovered_patterns` table + YAML auto-append)
- **What:** Novel compliance risks found by the wildcard scan
- **How it helps:** Auto-appended to framework YAML files, so the next scan of any repo includes them
- **Key design:** Deduplicated by framework + search hint. Gemini judge still validates quality.

### Remediation Library (`remediation_library` table)
- **What:** Gemini-improved remediations stored per question + domain
- **How it helps:** Future scans get more specific, actionable remediations from the start

### Human Feedback (`finding_feedback` table)
- **What:** User-submitted correct/incorrect verdicts with reasoning
- **How it helps:** Feeds into question accuracy with `[HUMAN]` tag — strongest signal in the corpus

## Data Flow

### Scan Lifecycle

1. **Queued** — scan_id created, URL validated, rate limit checked, cancellation flag set
2. **Running: Clone** — shallow git clone to temp directory (500MB limit, 300s timeout)
3. **Running: Qualify** — README quality, code file count, data handling evidence
4. **Running: Domain** — signal-based classification, framework mapping
5. **Running: Scan** — 3 concurrent agents, each running standard + discovered + wildcard questions
6. **Running: Judge** — 5 concurrent Gemini workers reviewing all findings
7. **Running: Report** — HTML + markdown generation, intelligence corpus recording
8. **Complete** — findings persisted, stats updated, report URL stored

### Cancellation

- Each scan has a `threading.Event` cancellation flag
- `_cancelled()` checked between every major step
- Stop endpoint sets the flag; scan thread exits at next checkpoint
- Orphaned scans (thread killed by deploy) are force-cancelled on next stop request

### Clone Management

- All clones use `tempfile.mkdtemp()` with `opendocket_` prefix
- 500MB size gate — repos exceeding this are aborted
- `try/finally` guarantees cleanup via `shutil.rmtree`
- No repo code is ever persisted

## Database Schema

SQLite database at `data/opendocket.db` (persistent volume on Railway).

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `scans` | Scan metadata | status, score, findings counts, tokens, duration |
| `findings` | Per-question results | severity, judge verdict/reasoning/confidence |
| `evidence_patterns` | Learned file path priorities | framework, question_id, file_glob, hit/confirmed/fp counts |
| `question_accuracy` | Per-question confirmation rates | framework, question_id, domain, confirmed/fp/context counts, FP reasons |
| `discovered_patterns` | Novel patterns from wildcard | framework, category, search_hint, occurrences, repos_seen |
| `remediation_library` | Gemini-improved remediations | framework, question_id, domain, remediation text, use_count |
| `finding_feedback` | Human corrections | scan_id, question_id, verdict, reason |
| `visitors` | Unique visitor tracking | visitor_id (random UUID), visit_count, pages_viewed |
| `events` | Analytics events | event_type, repo_name, timestamp |
| `stats` | Aggregate counters | stat_key, stat_value |
| `waitlist` | Email signups | email, timestamp |

### Scaling Path

SQLite handles ~1000 scans/day. When outgrowing it:
1. Set `DATABASE_URL=postgresql://...`
2. Run migration script
3. App auto-detects and switches

## API Design

### Core Scan Flow
- `POST /api/scan` — start scan, returns scan_id
- `GET /api/scan/:id` — poll for status + progress JSON
- `POST /api/scan/:id/stop` — cancel running scan
- `POST /api/scan/:id/restart` — restart as new scan
- `DELETE /api/scan/:id` — delete scan + findings (preserves intelligence)
- `GET /api/scan/:id/logs` — incremental log stream (poll with `?after=N`)

### Intelligence
- `GET /api/learning` — full system learning summary
- `GET /api/discovered` — novel patterns found by wildcard
- `POST /api/feedback` — submit human correction on a finding

### Operations
- `GET /api/ops` — dashboard data (performance, tokens, corpus, visitors)
- `GET /api/visitors` — unique visitor metrics
- `GET /api/stats` — computed from scan data (not stale counters)

## Rate Limiting

- 3 scans per IP per hour for public scans
- BYOK (Bring Your Own Key) scans are unlimited
- Daily limit: 200 scans (configurable via `DAILY_SCAN_LIMIT`)
- Monthly limit: 2000 scans (configurable via `MONTHLY_SCAN_LIMIT`)

## Token Tracking

Every Claude API call tracks `input_tokens` and `output_tokens`. Aggregated per scan and stored in the `scans` table. Visible in the operations dashboard for cost monitoring.

## Key Design Decisions

1. **Temperature 0** — deterministic LLM output for consistent findings across scan runs
2. **No stored code** — repos are cloned to temp dirs and deleted after scanning
3. **Dual model independence** — different company, different model = genuine independence
4. **Intelligence informs readers, not models** — accuracy data shown in reports for human calibration, never fed into Claude's prompts to avoid confirmation bias
5. **Self-expanding questions** — wildcard scan + auto-YAML-append means the system teaches itself new compliance checks
6. **Scan deletion preserves intelligence** — deleting a scan removes it from the directory but keeps all learned patterns, accuracy data, and discovered questions
7. **YAML question libraries** — anyone can contribute questions without touching Python code; the system also contributes its own via wildcard discoveries
8. **Persistent volume** — Railway volume at `/app/data` ensures database survives deploys
