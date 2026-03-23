# OpenDocket

**OpenDocket is an open-source compliance scanner that identifies regulatory risk patterns in code repositories.** It asks the questions a regulator would ask in court, finds the evidence in your code, and produces a structured report in legal brief format.

## Why OpenDocket Exists

Engineers build software that handles sensitive data every day — patient records, payment information, user credentials — but most teams have no visibility into whether their code patterns align with the regulatory frameworks that govern their domain. Compliance reviews happen late, cost a fortune, and surface issues that could have been caught at the code level months earlier. OpenDocket closes that blind spot by scanning your codebase the way a regulator would review it.

## Compliance Intelligence Directory

OpenDocket maintains a curated directory of compliance scans across healthcare, payments, SaaS, and infrastructure verticals. Browse the [web dashboard](docs/index.html) with industry tabs, a sortable leaderboard, and detailed per-framework findings.

## How to Run It Locally

**Prerequisites:** Python 3.10+, Git, an Anthropic API key.

```bash
# Clone the repo
git clone https://github.com/Anurag-Mohanty/opendocket.git
cd opendocket

# Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Set your Anthropic API key (or add to .env file)
export ANTHROPIC_API_KEY="your-key-here"

# Scan a repository
python scanner/main.py https://github.com/org/repo
```

The scanner will:
1. Clone the target repository
2. Run qualification gates (README quality, code file count, data handling evidence)
3. Detect regulatory domains (healthcare, fintech, SaaS, payments, communications, etc.)
4. Map domains to compliance frameworks (HIPAA, SOC2, PCI-DSS, GDPR, TCPA, SOX)
5. Run framework-specific agents that ask legal questions and find evidence
6. Run an independent review pass that challenges each finding for false positives
7. Output a structured report in legal brief format to `reports/`

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

| Framework | Regulatory Body | Jurisdiction | Risk of Non-Compliance | Questions |
|-----------|----------------|-------------|----------------------|-----------|
| **HIPAA** | HHS / OCR | United States | Fines up to $1.5M/year per category, criminal penalties | 10 |
| **SOC 2** | AICPA | International | Loss of enterprise contracts, audit findings | 10 |
| **PCI-DSS** | PCI Security Standards Council | International | Fines $5K-$100K/month, loss of payment processing | 10 |
| **GDPR** | EU Data Protection Authorities | European Union | Up to EUR 20M or 4% global annual turnover | 10 |
| **TCPA** | FCC | United States | $500-$1,500 per violation, class action exposure | 8 |
| **SOX** | SEC / PCAOB | United States | Criminal penalties, executive liability, delisting | 8 |

## OpenDocket Score

Every scanned repo receives an OpenDocket Score (0-100). Lower score = more risk patterns found.

- **High Risk finding:** -8 points
- **Medium Risk finding:** -3 points
- **Pattern of Concern:** -1 point
- Scores are normalized by framework count so repos scanned against 6 frameworks aren't penalized vs 2.

This is a relative risk pattern index, not a compliance certification. See the full [methodology](docs/methodology.html).

## Dual Model Review

Every finding goes through two analysis passes:
1. **Primary Scan** (Claude Sonnet) — analyzes code evidence against regulatory questions
2. **Independent Review** — challenges each finding as Confirmed, Context Dependent, Possible False Positive, or Additional Risk

This reduces the false positive rate. Neither pass constitutes legal advice.

## Example Reports

| Repository | Domain | Frameworks | High | Med | Score |
|---|---|---|---|---|---|
| [medplum/medplum](reports/medplum_report.md) | Healthcare, SaaS | GDPR, HIPAA, PCI-DSS, SOC2, SOX, TCPA | 47 | 6 | 19 |
| [openemr/openemr](reports/openemr_report.md) | Healthcare | HIPAA, SOC2, GDPR | 6 | 10 | 61 |
| [juspay/hyperswitch](reports/hyperswitch_report.md) | Fintech, SaaS | GDPR, HIPAA, PCI-DSS, SOC2, SOX, TCPA | 45 | 6 | 21 |
| [getprobo/probo](reports/probo_report.md) | SaaS | SOC2, GDPR | 3 | 6 | 72 |
| [kelseyhightower/nocode](reports/failed_gate_example.md) | — | — | Did not qualify | — | N/A |

## Project Structure

```
opendocket/
├── README.md
├── scanner/
│   ├── main.py                     # Entry point - accepts GitHub URL
│   ├── repo_fetcher.py             # Clones and reads repo contents
│   ├── domain_detector.py          # Signal-based domain detection
│   ├── compliance_mapper.py        # Maps domains to frameworks
│   ├── report_generator.py         # Formats output + score calculation
│   ├── agents/
│   │   ├── base_agent.py           # Base agent with LLM analysis + review
│   │   ├── hipaa_agent.py          # HIPAA framework runner
│   │   ├── soc2_agent.py           # SOC2 framework runner
│   │   ├── pci_dss_agent.py        # PCI-DSS framework runner
│   │   ├── gdpr_agent.py           # GDPR framework runner
│   │   ├── tcpa_agent.py           # TCPA framework runner
│   │   └── sox_agent.py            # SOX framework runner
│   └── config/
│       ├── hipaa_questions.yaml    # 10 HIPAA legal questions
│       ├── soc2_questions.yaml     # 10 SOC2 legal questions
│       ├── pci_dss_questions.yaml  # 10 PCI-DSS legal questions
│       ├── gdpr_questions.yaml     # 10 GDPR legal questions
│       ├── tcpa_questions.yaml     # 8 TCPA legal questions
│       └── sox_questions.yaml      # 8 SOX legal questions
├── reports/                        # Pre-generated markdown reports
├── docs/
│   ├── index.html                  # Directory + leaderboard + frameworks
│   ├── styles.css                  # Professional minimal design system
│   ├── methodology.html            # Scoring methodology
│   ├── privacy.html                # Privacy policy
│   └── reports/                    # Generated HTML reports
├── .env.example                    # API key template
└── requirements.txt
```

## How to Contribute

### Adding a Repo to the Directory

1. Fork the repo and run a scan: `python scanner/main.py https://github.com/org/repo --format html`
2. Copy the markdown report to `reports/` and HTML to `docs/reports/`
3. Add a card to `docs/index.html` in the appropriate industry tab
4. Submit a PR with the report files and updated index

### Adding a New Framework

1. **Create a question library** at `scanner/config/<framework>_questions.yaml`
2. **Create an agent** at `scanner/agents/<framework>_agent.py`
3. **Register in main.py** — add the agent to the `AGENTS` dictionary
4. **Add domain signals** to `scanner/domain_detector.py`
5. **Update the mapper** in `scanner/compliance_mapper.py`
6. **Submit a PR** with example output from at least one real repo

### Improving Question Libraries

Question libraries live in `scanner/config/` as YAML files. Each question has a legal question, regulatory citation, search patterns, absence patterns, and evidence guidance. Add questions, refine patterns, or improve guidance and submit a PR.

## Roadmap

| Version | Milestone | Status |
|---------|-----------|--------|
| **V1** | Static reports, 6 frameworks, compliance directory, dual model review | Done |
| **V2** | Live GitHub scanning with OAuth | Planned |
| **V3** | PR and branch report delivery | Planned |
| **V4** | Dual model review automated pipeline | Planned |
| **V5** | Attorney marketplace | Planned |
| **V6** | Compliance badge program | Planned |
| **V7** | Private repo enterprise tier | Planned |

## Featured In

*Coming soon — placeholder for press mentions and community coverage.*

## License and Copyright

The OpenDocket scanner, question libraries, and web interface are released under the MIT License. Copyright 2026 OpenDocket contributors.

The MIT License permits use, modification, and distribution including commercial use, provided the copyright notice is retained.

Note: The OpenDocket findings database and accumulated scan pattern data are proprietary and not covered by the MIT License.

See [LICENSE](LICENSE) for details.

## Disclaimer

OpenDocket identifies risk patterns through automated code analysis. Findings represent potential areas of concern, not legal determinations. This report does not constitute legal advice. Regulatory compliance requires qualified legal and technical assessment. Consult a licensed attorney and certified compliance professional for definitive compliance determination.
