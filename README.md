# OpenDocket

**OpenDocket is an open-source compliance scanner that identifies regulatory risk patterns in code repositories.** It asks the questions a regulator would ask in court, finds the evidence in your code, and produces a structured report in legal brief format.

**Live at [opendocket.dev](https://opendocket.dev)**

## Why OpenDocket Exists

Engineers build software that handles sensitive data every day — patient records, payment information, user credentials — but most teams have no visibility into whether their code patterns align with the regulatory frameworks that govern their domain. Compliance reviews happen late, cost a fortune, and surface issues that could have been caught at the code level months earlier. OpenDocket closes that blind spot by scanning your codebase the way a regulator would review it.

## What Makes It Different

- **Self-improving** — every scan teaches the system new compliance patterns, evidence locations, and false-positive signals. The question library grows automatically.
- **Dual model review** — Claude finds the findings, Gemini challenges them. Two companies, two models, genuine independence.
- **Cross-repo intelligence** — reports show "Confirmed in X% of scans" per finding, so readers can calibrate confidence based on data from all previous scans.
- **Human feedback loop** — each finding has a "correct / incorrect" button. Human corrections are the strongest signal in the accuracy corpus.

## How It Works

1. **Clone & qualify** — clones the repo, runs qualification gates (code count, data handling evidence)
2. **Domain detection** — signal-based classification (healthcare, fintech, SaaS, payments, etc.)
3. **Framework mapping** — maps domains to compliance frameworks (HIPAA, PCI-DSS, SOC2, etc.)
4. **Compliance agents** — 3 concurrent agents run legal questions against the code, finding evidence in specific files and line numbers. Includes a wildcard pass that catches novel risks the standard questions miss.
5. **Gemini independent review** — 5 concurrent workers challenge every finding as Confirmed, Context Dependent, Possible False Positive, or Additional Risk
6. **Intelligence recording** — evidence patterns, question accuracy rates, FP reasoning, improved remediations, and novel questions all feed back into the corpus
7. **Report generation** — structured HTML report with cross-repo confidence context per finding

## Live Scanning

Visit [opendocket.dev](https://opendocket.dev), paste a public GitHub URL, and get a compliance report. 3 free scans per hour, no account required. Bring your own API keys for unlimited scans.

Features:
- **Stop / restart** scans from the UI
- **Real-time logs** at `/logs.html?scan_id=...` showing progress, corpus intelligence, and product improvements
- **Delete & rescan** to clear cached results
- **Feedback buttons** on each finding in the report

## How to Run Locally

**Prerequisites:** Python 3.10+, Git, an Anthropic API key.

```bash
# Clone the repo
git clone https://github.com/Anurag-Mohanty/opendocket.git
cd opendocket

# Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Set your API keys
export ANTHROPIC_API_KEY="your-key-here"
export GEMINI_API_KEY="your-gemini-key-here"  # optional, enables independent review

# Scan a repository (CLI)
python scanner/main.py https://github.com/org/repo

# Or run the web server
python scanner/api.py
# Then open http://localhost:8080
```

### Command Line Options

```bash
# Output as HTML with collapsible cards and severity filters
python scanner/main.py https://github.com/org/repo --format html

# Scan with only specific frameworks
python scanner/main.py https://github.com/org/repo --frameworks hipaa,soc2,gdpr

# Custom output directory
python scanner/main.py https://github.com/org/repo --output ./my-reports
```

## Supported Compliance Frameworks

| Framework | Regulatory Body | Risk of Non-Compliance | Base Questions | Self-Expanding |
|-----------|----------------|----------------------|----------------|----------------|
| **HIPAA** | HHS / OCR | Fines up to $1.5M/year per category | 10 | Yes |
| **SOC 2** | AICPA | Loss of enterprise contracts | 10 | Yes |
| **PCI-DSS** | PCI Security Standards Council | Fines $5K-$100K/month | 10 | Yes |
| **GDPR** | EU Data Protection Authorities | Up to EUR 20M or 4% turnover | 10 | Yes |
| **TCPA** | FCC | $500-$1,500 per violation | 8 | Yes |
| **SOX** | SEC / PCAOB | Criminal penalties, delisting | 8 | Yes |
| **CCPA/CPRA** | CA Privacy Protection Agency | $2,500-$7,500/violation | 10 | Yes |
| **COPPA** | FTC | Up to $51,744 per violation | 8 | Yes |
| **FERPA** | U.S. Dept. of Education | Loss of federal funding | 8 | Yes |
| **GLBA** | FTC / Banking Regulators | $100K/violation + criminal | 8 | Yes |

**Self-expanding:** Each framework's question library grows automatically. The wildcard scan discovers novel compliance patterns, and they're auto-added to the YAML files for future scans.

## Intelligence System

OpenDocket gets smarter with every scan through four learning mechanisms:

### 1. Evidence Pattern Corpus
Tracks which file paths produce confirmed vs false-positive evidence per question. Agents use this to search high-confidence paths first, finding evidence faster.

### 2. Question Accuracy Tracking
Per-question confirmation/FP rates by domain. Shown in reports as "Confirmed in X% of scans (N repos)" so readers can calibrate — but never fed into Claude's prompts to avoid feedback-loop bias.

### 3. Self-Expanding Question Library
The wildcard pass asks Claude "what did the standard questions miss?" Novel findings with a search hint are auto-appended to the framework YAML. The next scan of any repo runs the new question automatically.

### 4. Remediation Library
Gemini-improved remediations are stored per question+domain. Future scans for the same question type get more specific, actionable remediations from the start.

### 5. Human Feedback
Each finding in a report has "Is this accurate?" buttons. Human corrections feed into the accuracy corpus with the strongest signal weight.

## Dual Model Review

Every finding goes through two analysis passes:
1. **Primary Scan** (Claude Sonnet, temperature=0) — analyzes code evidence against regulatory questions with deterministic output
2. **Independent Review** (Gemini 2.5 Flash, 5 concurrent workers) — challenges each finding as Confirmed, Context Dependent, Possible False Positive, or Additional Risk

This reduces the false positive rate. Neither pass constitutes legal advice.

## Operations Dashboard

The dashboard at `/dashboard.html` shows:
- **Unique visitors** (total, today, week, returning)
- **Scan performance** (duration trends, token usage per scan)
- **Evidence corpus** breakdown by framework with signal strength
- **System learning** (patterns learned, novel questions discovered, FP intelligence, remediation reuse)
- **Human feedback** stats (correct vs incorrect)

## Project Structure

```
opendocket/
├── README.md
├── ARCHITECTURE.md
├── Dockerfile
├── railway.toml                     # Railway deployment with persistent volume
├── scanner/
│   ├── api.py                       # Flask API server with all endpoints
│   ├── main.py                      # CLI entry point
│   ├── database.py                  # SQLite persistence + intelligence corpus
│   ├── repo_fetcher.py              # Clone management + qualification
│   ├── domain_detector.py           # Signal-based domain detection
│   ├── compliance_mapper.py         # Domain-to-framework mapping
│   ├── report_generator.py          # HTML + markdown report generation
│   ├── seed_database.py             # Seed DB from existing reports
│   ├── backfill_corpus.py           # Backfill intelligence corpus from HTML reports
│   ├── agents/
│   │   ├── base_agent.py            # Base agent + JudgeAgent + wildcard scan
│   │   ├── hipaa_agent.py           # HIPAA framework runner
│   │   ├── soc2_agent.py            # SOC2 framework runner
│   │   ├── pci_dss_agent.py         # PCI-DSS framework runner
│   │   ├── gdpr_agent.py            # GDPR framework runner
│   │   ├── tcpa_agent.py            # TCPA framework runner
│   │   ├── sox_agent.py             # SOX framework runner
│   │   ├── ccpa_agent.py            # CCPA/CPRA framework runner
│   │   ├── coppa_agent.py           # COPPA framework runner
│   │   ├── ferpa_agent.py           # FERPA framework runner
│   │   └── glba_agent.py            # GLBA framework runner
│   └── config/
│       ├── hipaa_questions.yaml     # 10+ HIPAA legal questions (self-expanding)
│       ├── soc2_questions.yaml      # 10+ SOC2 legal questions
│       ├── pci_dss_questions.yaml   # 10+ PCI-DSS legal questions
│       ├── gdpr_questions.yaml      # 10+ GDPR legal questions
│       ├── tcpa_questions.yaml      # 8+ TCPA legal questions
│       ├── sox_questions.yaml       # 8+ SOX legal questions
│       ├── ccpa_questions.yaml      # 10+ CCPA/CPRA legal questions
│       ├── coppa_questions.yaml     # 8+ COPPA legal questions
│       ├── ferpa_questions.yaml     # 8+ FERPA legal questions
│       └── glba_questions.yaml      # 8+ GLBA legal questions
├── docs/
│   ├── index.html                   # Landing page + scan UI + directory
│   ├── dashboard.html               # Operations dashboard
│   ├── logs.html                    # Real-time scan log viewer
│   ├── styles.css                   # Design system
│   ├── methodology.html             # Scoring methodology
│   ├── questions.html               # Question library reference
│   ├── privacy.html                 # Privacy policy
│   └── reports/                     # Generated HTML reports
├── reports/                         # Generated markdown reports
├── data/                            # SQLite database (persistent volume)
├── deploy/
│   └── railway_deploy.md            # Deployment instructions
└── requirements.txt
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/scan` | POST | Start a new scan |
| `/api/scan/:id` | GET | Scan status + progress |
| `/api/scan/:id` | DELETE | Delete a scan and its data |
| `/api/scan/:id/stop` | POST | Cancel a running scan |
| `/api/scan/:id/restart` | POST | Restart a cancelled/failed scan |
| `/api/scan/:id/logs` | GET | Real-time scan log stream |
| `/api/stats` | GET | Aggregate statistics |
| `/api/ops` | GET | Operations dashboard data |
| `/api/directory` | GET | Completed scans directory |
| `/api/feedback` | POST | Submit finding feedback |
| `/api/feedback/:id` | GET | Get feedback for a scan |
| `/api/visitor` | POST | Record unique visitor |
| `/api/visitors` | GET | Visitor metrics |
| `/api/discovered` | GET | Novel patterns discovered |
| `/api/learning` | GET | System learning summary |
| `/api/recent` | GET | Recent scans |
| `/api/events` | GET | Event analytics |
| `/api/track` | POST | Track analytics event |
| `/api/waitlist` | POST | Email waitlist signup |
| `/api/usage` | GET | Rate limit usage |

## How to Contribute

### Adding a New Framework

1. **Create a question library** at `scanner/config/<framework>_questions.yaml`
2. **Create an agent** at `scanner/agents/<framework>_agent.py`
3. **Register in api.py** — add the agent to the `AGENTS` dictionary
4. **Add domain signals** to `scanner/domain_detector.py`
5. **Update the mapper** in `scanner/compliance_mapper.py`
6. **Submit a PR** with example output from at least one real repo

### Improving Question Libraries

Question libraries live in `scanner/config/` as YAML files. Each question has a legal question, regulatory citation, search patterns, and absence patterns. The system also auto-discovers and adds questions through the wildcard scan — check `[Discovered]` entries in the YAMLs for patterns the system taught itself.

## Deployment

See [deploy/railway_deploy.md](deploy/railway_deploy.md) for Railway setup with persistent storage.

**Key requirement:** Attach a persistent volume at `/app/data` so the SQLite database (scan data + intelligence corpus) survives deploys. SQLite handles ~1000 scans/day. Migration path to Postgres is built in via `DATABASE_URL` env var.

## Roadmap

| Version | Milestone | Status |
|---------|-----------|--------|
| **V1** | Static reports, 6 frameworks, compliance directory, dual model review | Done |
| **V1.5** | Live scanning, 10 frameworks, self-improving intelligence, operations dashboard | Done |
| **V2** | Private repo scanning, GitHub OAuth | Planned |
| **V3** | PR-level scanning, CI/CD integration | Planned |
| **V4** | RAG-powered compliance intelligence | Planned |
| **V5** | Attorney marketplace | Planned |
| **V6** | Compliance badge program | Planned |
| **V7** | Enterprise tier with SSO | Planned |

## License and Copyright

The OpenDocket scanner, question libraries, and web interface are released under the MIT License. Copyright 2026 OpenDocket contributors.

Note: The OpenDocket findings database and accumulated scan pattern data are proprietary and not covered by the MIT License.

See [LICENSE](LICENSE) for details.

## Disclaimer

OpenDocket identifies risk patterns through automated code analysis. Findings represent potential areas of concern, not legal determinations. This report does not constitute legal advice. Regulatory compliance requires qualified legal and technical assessment. Consult a licensed attorney and certified compliance professional for definitive compliance determination.
