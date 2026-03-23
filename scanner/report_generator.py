"""
Report generator that formats scan results into legal brief format.
Outputs markdown and HTML reports.
"""

import html
from datetime import datetime
from scanner.agents.base_agent import AgentResult, Finding
from scanner.domain_detector import DomainResult


DISCLAIMER = (
    "OpenDocket identifies risk patterns through automated code analysis. "
    "Findings represent potential areas of concern, not legal determinations. "
    "This report does not constitute legal advice."
)

FRAMEWORK_META = {
    "HIPAA": {"body": "HHS / OCR", "risk": "Fines up to $1.5M/year per category", "trend": "Increasing enforcement, record penalties in 2024"},
    "SOC2": {"body": "AICPA", "risk": "Loss of enterprise contracts", "trend": "Mandatory for enterprise SaaS sales"},
    "PCI-DSS": {"body": "PCI SSC", "risk": "Fines $5K-$100K/month", "trend": "v4.0 enforcement accelerating"},
    "GDPR": {"body": "EU DPAs", "risk": "Up to EUR 20M or 4% turnover", "trend": "Cross-border enforcement rising"},
    "TCPA": {"body": "FCC", "risk": "$500-$1,500 per violation", "trend": "Class action filings at record levels"},
    "SOX": {"body": "SEC / PCAOB", "risk": "Criminal penalties, delisting", "trend": "IT controls under increased scrutiny"},
    "CCPA/CPRA": {"body": "CA Privacy Protection Agency", "risk": "$2,500-$7,500/violation + class action", "trend": "CPPA active enforcement since 2023"},
    "COPPA": {"body": "FTC", "risk": "Up to $51,744 per violation", "trend": "FTC actively pursuing children's data cases"},
    "FERPA": {"body": "U.S. Dept. of Education", "risk": "Loss of federal funding", "trend": "Ed-tech vendors under increased scrutiny"},
    "GLBA": {"body": "FTC / Banking Regulators", "risk": "$100K/violation + criminal", "trend": "2023 Safeguards Rule expansion"},
}


def risk_classification(high_count: int) -> tuple[str, str, str]:
    """Return (label, color, description) for risk classification."""
    if high_count == 0:
        return "LOW RISK", "#1A7F37", "No high-severity patterns found"
    elif high_count <= 5:
        return "MODERATE RISK", "#9A6700", f"{high_count} high-severity patterns require attention"
    elif high_count <= 15:
        return "ELEVATED RISK", "#CF222E", f"{high_count} high-severity patterns found — prioritize remediation"
    else:
        return "CRITICAL RISK", "#CF222E", f"{high_count} high-severity patterns found — immediate attention required"


def _severity_class(level: str) -> str:
    return {"High Risk": "high", "Medium Risk": "med",
            "Pattern of Concern": "concern", "No Issue Found": "ok"}.get(level, "")


def _verdict_css(verdict: str) -> str:
    return {"CONFIRMED": "v-confirmed", "CONTEXT DEPENDENT": "v-context",
            "POSSIBLE FALSE POSITIVE": "v-fp", "ADDITIONAL RISK": "v-additional",
            "NOT REVIEWED": "v-context"}.get(verdict, "")


def _select_top_findings(all_findings: list[Finding], n: int = 3) -> list[Finding]:
    """Select top N findings: high risk first, confirmed preferred, spread across frameworks."""
    scored = []
    for f in all_findings:
        s = 0
        if f.finding_level == "High Risk":
            s += 100
        elif f.finding_level == "Medium Risk":
            s += 50
        if f.review_verdict == "CONFIRMED":
            s += 30
        elif f.review_verdict == "ADDITIONAL RISK":
            s += 20
        s += len(f.evidence) * 2  # evidence specificity
        scored.append((s, f))
    scored.sort(key=lambda x: x[0], reverse=True)

    selected = []
    seen_fw = set()
    # First pass: one per framework
    for _, f in scored:
        fw = getattr(f, '_framework', '')
        if fw not in seen_fw and len(selected) < n:
            selected.append(f)
            seen_fw.add(fw)
    # Fill remaining
    for _, f in scored:
        if f not in selected and len(selected) < n:
            selected.append(f)
    return selected[:n]


# ── Markdown Report ──

def generate_markdown_report(
    repo_name: str, repo_url: str,
    domains: list[DomainResult], agent_results: list[AgentResult],
) -> str:
    lines = []
    lines.append(f"# OpenDocket Compliance Report: {repo_name}")
    lines.append("")
    lines.append(f"> **Repository:** {repo_url}")
    lines.append(f"> **Scan Date:** {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"> **Scanner Version:** OpenDocket V1")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"**DISCLAIMER:** {DISCLAIMER}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Domain Detection")
    lines.append("")
    for d in domains:
        lines.append(f"- **{d.domain.title()}** — Confidence: {d.confidence}% "
                     f"({d.signal_count} signals, top: {', '.join(d.signals_found[:5])})")
    lines.append("")
    fw_names = [r.framework for r in agent_results]
    lines.append(f"## Frameworks Analyzed: {', '.join(fw_names)}")
    lines.append("")
    all_findings = [f for r in agent_results for f in r.findings]
    high = sum(1 for f in all_findings if f.finding_level == "High Risk")
    label, _, desc = risk_classification(high)
    lines.append(f"## Risk Pattern Index: {label}")
    lines.append(f"{desc}")
    lines.append("")
    lines.append("| Finding Level | Count |")
    lines.append("|---|---|")
    for level in ("High Risk", "Medium Risk", "Pattern of Concern", "No Issue Found"):
        count = sum(1 for f in all_findings if f.finding_level == level)
        lines.append(f"| {level} | {count} |")
    lines.append("")
    for result in agent_results:
        lines.append(f"## {result.framework} Findings")
        lines.append("")
        for finding in result.findings:
            lines.append(f"### {finding.question_id}: {finding.category}")
            lines.append("")
            lines.append(f"**{finding.legal_question}**")
            lines.append("")
            lines.append(f"*{finding.regulatory_standard}*")
            lines.append("")
            if finding.evidence:
                for e in finding.evidence[:10]:
                    lines.append(f"- `{e.file_path}:{e.line_number}` — `{e.content[:120]}`")
            else:
                lines.append("- No matching code patterns found.")
            lines.append("")
            emoji = {"High Risk": "🔴", "Medium Risk": "🟠",
                     "Pattern of Concern": "🔵", "No Issue Found": "🟢"}.get(finding.finding_level, "")
            lines.append(f"**{emoji} {finding.finding_level}**")
            lines.append("")
            lines.append(finding.finding_text)
            lines.append("")
            if finding.remediation:
                lines.append(f"**Remediation:** {finding.remediation}")
                lines.append("")
            lines.append("---")
            lines.append("")
    lines.append(f"**DISCLAIMER:** {DISCLAIMER}")
    return "\n".join(lines)


def generate_failed_gate_report(
    repo_name: str, repo_url: str, reasons: list[str], stats: dict,
) -> str:
    lines = []
    lines.append(f"# OpenDocket Qualification Report: {repo_name}")
    lines.append("")
    lines.append(f"> **Repository:** {repo_url}")
    lines.append(f"> **Scan Date:** {datetime.now().strftime('%Y-%m-%d')}")
    lines.append("")
    lines.append("---")
    lines.append(f"**DISCLAIMER:** {DISCLAIMER}")
    lines.append("---")
    lines.append("")
    lines.append("## Qualification Result: DOES NOT QUALIFY FOR SCANNING")
    lines.append("")
    for reason in reasons:
        lines.append(f"- {reason}")
    lines.append("")
    for key, value in stats.items():
        lines.append(f"- **{key}:** {value}")
    lines.append("")
    lines.append(f"**DISCLAIMER:** {DISCLAIMER}")
    return "\n".join(lines)


# Keep calculate_score for backward compat but it's deprecated
def calculate_score(agent_results: list[AgentResult]) -> int:
    if not agent_results:
        return 100
    all_findings = [f for r in agent_results for f in r.findings]
    high = sum(1 for f in all_findings if f.finding_level == "High Risk")
    label, _, _ = risk_classification(high)
    return {"LOW RISK": 95, "MODERATE RISK": 65, "ELEVATED RISK": 30, "CRITICAL RISK": 10}.get(label, 50)


# ── CSS for light-mode reports ──
_CSS = """*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #0D1117; background: #F4F5F7; }
a { color: #0052CC; text-decoration: none; } a:hover { text-decoration: underline; }
.top-bar { height: 4px; background: #0052CC; }
.nav { background: #FFFFFF; box-shadow: 0 1px 0 #EAEEF2; padding: 0 40px; height: 48px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 200; }
.nav-brand { font-size: 15px; font-weight: 700; color: #1a1a1a; text-decoration: none; display: flex; align-items: center; gap: 8px; }
.nav-brand-shield { width: 20px; height: 24px; background: #0052CC; clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%); display: inline-block; }
.nav-links { display: flex; gap: 24px; } .nav-links a { font-size: 13px; color: #57606a; text-decoration: none; } .nav-links a:hover { color: #0052CC; }
.action-bar { background: #f6f8fa; border-bottom: 1px solid #d0d7de; padding: 8px 40px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 48px; z-index: 190; }
.action-bar-left { display: flex; gap: 8px; align-items: center; } .action-bar-right { display: flex; gap: 8px; }
.btn { font-size: 13px; padding: 6px 14px; border: 1px solid #d0d7de; background: #fff; color: #1a1a1a; cursor: pointer; border-radius: 2px; font-family: inherit; } .btn:hover { background: #f6f8fa; }
.btn-primary { background: #0052CC; color: #fff; border-color: #0052CC; } .btn-primary:hover { background: #0047B3; }
/* Tabs */
.tab-bar { display: flex; gap: 0; border-bottom: 1px solid #d0d7de; padding: 0 40px; background: #fff; position: sticky; top: 96px; z-index: 180; }
.tab-btn { padding: 10px 20px; font-size: 14px; font-weight: 500; color: #57606a; border: none; background: none; cursor: pointer; border-bottom: 2px solid transparent; font-family: inherit; }
.tab-btn:hover { color: #1a1a1a; } .tab-btn.active { color: #0052CC; border-bottom-color: #0052CC; font-weight: 600; }
.tab-panel { display: none; } .tab-panel.active { display: block; }
/* Filter bar inside findings tab */
.filter-bar { background: #fff; border-bottom: 1px solid #d0d7de; padding: 8px 0; display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }
.filter-label { font-size: 12px; font-weight: 600; color: #57606a; text-transform: uppercase; letter-spacing: 0.5px; }
.filter-sep { width: 1px; height: 16px; background: #d0d7de; margin: 0 4px; }
.filter-btn { font-size: 12px; padding: 3px 10px; border: 1px solid #d0d7de; background: #fff; color: #57606a; cursor: pointer; border-radius: 2px; font-family: inherit; }
.filter-btn:hover { border-color: #0052CC; color: #0052CC; } .filter-btn.active { background: #0052CC; color: #fff; border-color: #0052CC; }
/* Layout */
.page { max-width: 960px; margin: 0 auto; padding: 32px 40px; }
.section { margin-bottom: 24px; scroll-margin-top: 160px; background: #FFFFFF; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); padding: 24px; }
.section-heading { font-size: 13px; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase; color: #57606a; border-bottom: 1px solid #d0d7de; padding-bottom: 8px; margin-bottom: 20px; }
.report-header { margin-bottom: 32px; }
.report-eyebrow { font-size: 12px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #57606a; margin-bottom: 8px; }
.report-title { font-size: 26px; font-weight: 700; color: #1a1a1a; margin-bottom: 8px; }
.report-meta { font-size: 13px; color: #57606a; line-height: 1.8; } .report-meta a { color: #0052CC; }
.callout { padding: 14px 16px; margin-bottom: 16px; border: 1px solid #d0d7de; border-left-width: 4px; font-size: 13px; line-height: 1.6; color: #1a1a1a; } .callout strong { font-weight: 600; }
.callout-blue { border-left-color: #0052CC; background: #f0f5ff; }
.callout-yellow { border-left-color: #9A6700; background: #fffbe0; }
.callout-amber { border-left-color: #9A6700; background: #fffbe0; }
/* Risk index */
.risk-index { display: flex; align-items: center; gap: 16px; padding: 20px 24px; background: #f6f8fa; border: 1px solid #d0d7de; margin-bottom: 24px; }
.risk-label { font-size: 20px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
.risk-desc { font-size: 14px; color: #57606a; }
/* Tables */
.table { width: 100%; border-collapse: collapse; font-size: 14px; margin-bottom: 20px; }
.table th { text-align: left; padding: 8px 12px; background: #f6f8fa; border: 1px solid #d0d7de; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: #57606a; }
.table td { padding: 10px 12px; border: 1px solid #d0d7de; color: #1a1a1a; vertical-align: top; } .table tr:nth-child(even) td { background: #f6f8fa; }
.n-high { color: #cf222e; font-weight: 700; } .n-med { color: #9A6700; font-weight: 700; } .n-concern { color: #0052CC; font-weight: 600; } .n-ok { color: #1A7F37; }
/* Domain bars */
.domain-row { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; font-size: 14px; }
.domain-name { width: 130px; font-weight: 500; } .domain-bar-wrap { flex: 1; height: 6px; background: #eaeef2; border-radius: 3px; overflow: hidden; }
.domain-bar { height: 100%; background: #0052CC; border-radius: 3px; } .domain-pct { width: 44px; text-align: right; font-size: 13px; color: #57606a; }
/* Judge */
.judge-block { background: #F3EEFF; border: 1px solid #D0D7DE; border-left: 4px solid #6E40C9; padding: 16px 20px; margin-bottom: 24px; }
.judge-title { font-size: 12px; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase; color: #6E40C9; margin-bottom: 12px; }
.judge-stats { display: flex; gap: 32px; flex-wrap: wrap; margin-bottom: 12px; } .judge-stat { text-align: center; }
.judge-stat-n { font-size: 24px; font-weight: 700; display: block; line-height: 1.2; } .judge-stat-l { font-size: 12px; color: #57606a; display: block; }
.j-confirmed { color: #1A7F37; } .j-context { color: #9A6700; } .j-fp { color: #cf222e; } .j-additional { color: #6E40C9; }
.judge-note { font-size: 12px; color: #8c959f; border-top: 1px solid #d0d7de; padding-top: 10px; margin-top: 4px; }
/* Top findings */
.top-finding { border: 1px solid #d0d7de; border-left: 4px solid #cf222e; background: #fff8f8; padding: 14px 16px; margin-bottom: 10px; }
.top-finding-q { font-size: 14px; font-weight: 600; color: #1a1a1a; margin-bottom: 6px; line-height: 1.5; }
.top-finding-meta { display: flex; gap: 12px; font-size: 12px; color: #57606a; flex-wrap: wrap; }
.badge { display: inline-block; font-size: 11px; font-weight: 700; letter-spacing: 0.3px; text-transform: uppercase; padding: 2px 8px; border-radius: 2px; }
.badge-high { color: #cf222e; background: #fff0f0; border: 1px solid #cf222e; }
.badge-med { color: #9A6700; background: #fffbe0; border: 1px solid #9A6700; }
.badge-concern { color: #0052CC; background: #f0f5ff; border: 1px solid #0052CC; }
.badge-ok { color: #1A7F37; background: #f0fff4; border: 1px solid #1A7F37; }
/* Recs */
.rec-item { display: flex; gap: 16px; padding: 14px 0; border-bottom: 1px solid #d0d7de; } .rec-item:last-child { border-bottom: none; }
.rec-priority { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; min-width: 70px; padding-top: 2px; }
.rec-p-high { color: #cf222e; } .rec-p-med { color: #9A6700; }
.rec-text { font-size: 14px; color: #1a1a1a; line-height: 1.6; } .rec-fw { font-size: 12px; color: #57606a; margin-top: 3px; }
/* Framework sections */
.framework-section { margin-bottom: 36px; scroll-margin-top: 160px; }
.framework-header { background: #0D1117; color: #FFFFFF; border: none; padding: 12px 16px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: flex-start; }
.framework-name { font-size: 15px; font-weight: 700; color: #FFFFFF; margin-bottom: 4px; } .framework-meta { font-size: 12px; color: #8B949E; }
.framework-count { font-size: 13px; color: #8B949E; white-space: nowrap; padding-left: 16px; }
/* Finding cards */
.finding { border: 1px solid #D0D7DE; margin-bottom: 8px; page-break-inside: avoid; background: #FFFFFF; box-shadow: 0 1px 3px rgba(0,0,0,0.06); border-radius: 4px; overflow: hidden; }
.finding[data-severity="High Risk"] { border-left: 4px solid #cf222e; }
.finding[data-severity="Medium Risk"] { border-left: 4px solid #9A6700; }
.finding[data-severity="Pattern of Concern"] { border-left: 4px solid #0052CC; }
.finding[data-severity="No Issue Found"] { border-left: 4px solid #1A7F37; }
.finding-header { display: flex; align-items: flex-start; justify-content: space-between; padding: 12px 16px; background: #FAFBFC; cursor: pointer; user-select: none; gap: 12px; transition: background 0.15s; } .finding-header:hover { background: #F0F1F3; }
.finding[data-severity="High Risk"] .finding-header { background: #FFF5F5; } .finding[data-severity="High Risk"] .finding-header:hover { background: #FFECEC; }
.finding[data-severity="Medium Risk"] .finding-header { background: #FFF8F0; }
.finding[data-severity="Pattern of Concern"] .finding-header { background: #F0F5FF; }
.finding-left { flex: 1; min-width: 0; } .finding-num { font-size: 11px; font-family: "SFMono-Regular", Consolas, monospace; color: #8c959f; margin-bottom: 4px; }
.finding-question { font-size: 14px; font-weight: 600; color: #1a1a1a; line-height: 1.4; }
.finding-right { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.chevron { font-size: 12px; color: #57606a; transition: transform 0.15s; } .finding.open .chevron { transform: rotate(90deg); }
.finding-body { display: none; padding: 20px; border-top: 1px solid #d0d7de; } .finding.open .finding-body { display: block; }
.finding-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 16px; }
.field-label { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: #57606a; margin-bottom: 6px; }
.field-value { font-size: 14px; color: #1a1a1a; line-height: 1.6; } .citation { font-size: 13px; color: #0052CC; font-style: italic; }
.verdict-block { background: #f6f8fa; border: 1px solid #d0d7de; padding: 12px 14px; }
.verdict-header { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: #57606a; margin-bottom: 8px; }
.verdict-label { font-size: 12px; font-weight: 700; text-transform: uppercase; }
.v-confirmed { color: #1A7F37; } .v-context { color: #9A6700; } .v-fp { color: #cf222e; } .v-additional { color: #6E40C9; }
.verdict-text { font-size: 13px; color: #57606a; margin-top: 4px; } .verdict-model { font-size: 11px; color: #8c959f; margin-top: 4px; }
.evidence-block { background: #0D1117; border: 1px solid #30363D; border-left: 3px solid #0052CC; padding: 14px 16px; font-family: "SFMono-Regular", Consolas, monospace; font-size: 13px; color: #E6EDF3; white-space: pre-wrap; overflow-x: auto; margin-bottom: 16px; line-height: 1.5; }
.remediation-block { background: #f0fff4; border: 1px solid #d0d7de; border-left: 3px solid #1A7F37; padding: 14px 16px; font-size: 14px; color: #1a1a1a; line-height: 1.7; }
.questions-footer { border-top: 1px solid #d0d7de; padding: 20px 0; text-align: center; font-size: 13px; color: #57606a; margin-top: 40px; } .questions-footer a { color: #0052CC; }
@media print { .top-bar, .nav, .action-bar, .tab-bar { display: none; } .tab-panel { display: block !important; } .finding-body { display: block !important; } body { font-size: 12px; } .finding { page-break-inside: avoid; } @page { margin: 2cm; } }
@media (max-width: 768px) { .page { padding: 20px 16px; } .nav, .action-bar { padding-left: 16px; padding-right: 16px; } .tab-bar { padding: 0 16px; } .finding-grid { grid-template-columns: 1fr; } }"""


# ── Methodology tab static content ──
_METHODOLOGY_TAB = """
<div class="section">
<div class="section-heading">What This Analysis Covers</div>
<p style="margin-bottom:16px">OpenDocket scans source code patterns — specifically whether code handles regulated data in compliance-aware ways. It searches for evidence of encryption, access controls, consent mechanisms, audit logging, and other patterns that regulators look for.</p>
</div>
<div class="section">
<div class="section-heading">What It Does Not Cover</div>
<ul style="padding-left:20px;margin-bottom:16px;font-size:14px;line-height:2;color:#57606a">
<li>Only public repository content is analyzed</li>
<li>Files in .gitignore are not scanned</li>
<li>Infrastructure, deployment, and cloud configuration are outside scope</li>
<li>Operational policies and procedures are outside scope</li>
<li>This analysis covers code at time of scan — changes after scan date are not reflected</li>
</ul>
</div>
<div class="section">
<div class="section-heading">Legal Limitations</div>
<ul style="padding-left:20px;margin-bottom:16px;font-size:14px;line-height:2;color:#57606a">
<li><strong>This report is not defensible in court</strong></li>
<li>It does not constitute legal advice</li>
<li>It does not satisfy regulatory audit requirements</li>
<li>To obtain a defensible compliance assessment, engage a licensed compliance attorney and certified auditor</li>
<li>OpenDocket provides directional guidance only</li>
</ul>
</div>
<div class="section">
<div class="section-heading">How Findings Are Generated</div>
<ul style="padding-left:20px;margin-bottom:16px;font-size:14px;line-height:2;color:#57606a">
<li>Primary analysis by Claude Sonnet (Anthropic)</li>
<li>Independent review by Gemini 2.5 Flash (Google)</li>
<li>Question libraries are open source and community-maintained</li>
<li>All questions cite regulatory source text</li>
<li>Questions have not been validated by a licensed attorney</li>
</ul>
</div>
<div class="section">
<div class="section-heading">How to Use This Report</div>
<ul style="padding-left:20px;margin-bottom:16px;font-size:14px;line-height:2;color:#1a1a1a">
<li>Share with your engineering lead for remediation planning</li>
<li>Share with your attorney as a starting point for compliance review</li>
<li>Re-scan after remediation to track progress</li>
<li><strong>Do not present this as proof of compliance</strong></li>
</ul>
</div>"""


def generate_html_report(
    repo_name: str, repo_url: str,
    domains: list[DomainResult], agent_results: list[AgentResult],
) -> str:
    """Generate a professional light-mode HTML compliance report with tabs."""
    scan_date = datetime.now().strftime('%Y-%m-%d')
    all_findings = [f for r in agent_results for f in r.findings]
    # Tag findings with framework for top-finding selection
    for result in agent_results:
        for f in result.findings:
            f._framework = result.framework
    high = sum(1 for f in all_findings if f.finding_level == "High Risk")
    med = sum(1 for f in all_findings if f.finding_level == "Medium Risk")
    concern = sum(1 for f in all_findings if f.finding_level == "Pattern of Concern")
    ok = sum(1 for f in all_findings if f.finding_level == "No Issue Found")
    total = len(all_findings)
    fw_names = [r.framework for r in agent_results]
    fw_names_str = ", ".join(fw_names)

    # Risk classification (replaces score)
    risk_label, risk_color, risk_desc = risk_classification(high)

    # Executive summary paragraph (generated, not template)
    top_fw_by_high = []
    for r in agent_results:
        h = sum(1 for f in r.findings if f.finding_level == "High Risk")
        if h > 0:
            top_fw_by_high.append((h, r.framework))
    top_fw_by_high.sort(reverse=True)
    top_fw_names = ", ".join(fw for _, fw in top_fw_by_high[:3]) if top_fw_by_high else fw_names_str

    exec_para = (
        f"This analysis identified {total} compliance risk patterns across {fw_names_str}. "
        f"Of these, {high} are classified as high-severity — patterns consistent with potential non-compliance "
        f"that regulators actively investigate. "
    )
    if high > 0:
        exec_para += f"The most serious gaps were found in {top_fw_names}. "
        if any(fw in top_fw_names for fw in ["HIPAA", "GDPR", "PCI-DSS"]):
            exec_para += "Without remediation, these patterns could expose the organization to regulatory enforcement, financial penalties, and reputational damage."
        else:
            exec_para += "These patterns should be prioritized for remediation before production deployment."

    # Consequence table — ALL frameworks with high risk findings
    consequence_html = ""
    for h_count, fw in top_fw_by_high:
        meta = FRAMEWORK_META.get(fw, {})
        consequence_html += (
            f'<tr><td style="font-weight:600">{html.escape(fw)} <span style="color:#CF222E;font-size:12px">({h_count} high)</span></td>'
            f'<td>{html.escape(meta.get("body", ""))}</td>'
            f'<td style="color:#CF222E;font-weight:600">{html.escape(meta.get("risk", ""))}</td>'
            f'<td>{html.escape(meta.get("trend", ""))}</td></tr>\n'
        )

    # Scorecard rows
    scorecard_html = ""
    for result in agent_results:
        h = sum(1 for f in result.findings if f.finding_level == "High Risk")
        m = sum(1 for f in result.findings if f.finding_level == "Medium Risk")
        c = sum(1 for f in result.findings if f.finding_level == "Pattern of Concern")
        o = sum(1 for f in result.findings if f.finding_level == "No Issue Found")
        scorecard_html += f'<tr><td style="font-weight:600">{html.escape(result.framework)}</td><td class="n-high">{h}</td><td class="n-med">{m}</td><td class="n-concern">{c}</td><td class="n-ok">{o}</td></tr>\n'

    # Domains
    domains_html = ""
    for d in domains:
        pct = min(d.confidence, 100)
        domains_html += f'<div class="domain-row"><span class="domain-name">{html.escape(d.domain.title())}</span><div class="domain-bar-wrap"><div class="domain-bar" style="width:{pct}%"></div></div><span class="domain-pct">{d.confidence}%</span></div>\n'

    # Judge counts
    judge_confirmed = sum(1 for f in all_findings if f.review_verdict == "CONFIRMED")
    judge_context = sum(1 for f in all_findings if f.review_verdict == "CONTEXT DEPENDENT")
    judge_fp = sum(1 for f in all_findings if f.review_verdict == "POSSIBLE FALSE POSITIVE")
    judge_additional = sum(1 for f in all_findings if f.review_verdict == "ADDITIONAL RISK")

    # Top 3 findings (cross-framework, confirmed preferred)
    top3 = _select_top_findings(all_findings, 3)
    top_findings_html = ""
    for f in top3:
        sev_cls = _severity_class(f.finding_level)
        first_ev = f"{f.evidence[0].file_path}:{f.evidence[0].line_number}" if f.evidence else "No specific file cited"
        verdict_tag = f' &middot; Review: {html.escape(f.review_verdict)}' if f.review_verdict else ""
        top_findings_html += (
            f'<div class="top-finding"><div class="top-finding-q">{html.escape(f.legal_question)}</div>'
            f'<div class="top-finding-meta"><span class="badge badge-{sev_cls}">{html.escape(f.finding_level)}</span>'
            f'<span>{html.escape(getattr(f, "_framework", ""))}</span>'
            f'<span>{html.escape(f.question_id)}</span>'
            f'<span>{html.escape(first_ev)}</span>{verdict_tag}</div>'
            f'<div style="font-size:13px;color:#57606a;margin-top:8px">{html.escape(f.remediation[:200]) if f.remediation else ""}</div>'
            f'</div>\n'
        )

    # Recommendations (high risk first, then medium)
    sev_order = {"High Risk": 0, "Medium Risk": 1, "Pattern of Concern": 2, "No Issue Found": 3}
    sorted_f = sorted(all_findings, key=lambda f: sev_order.get(f.finding_level, 3))
    recommendations_html = ""
    for f in sorted_f:
        if f.finding_level == "High Risk" and f.remediation:
            recommendations_html += (
                f'<div class="rec-item"><div class="rec-priority rec-p-high">High</div>'
                f'<div><div class="rec-text">{html.escape(f.remediation)}</div>'
                f'<div class="rec-fw">{html.escape(getattr(f, "_framework", ""))} &middot; {html.escape(f.question_id)}</div></div></div>\n'
            )
    for f in sorted_f:
        if f.finding_level == "Medium Risk" and f.remediation:
            recommendations_html += (
                f'<div class="rec-item"><div class="rec-priority rec-p-med">Medium</div>'
                f'<div><div class="rec-text">{html.escape(f.remediation)}</div>'
                f'<div class="rec-fw">{html.escape(getattr(f, "_framework", ""))} &middot; {html.escape(f.question_id)}</div></div></div>\n'
            )
    if not recommendations_html:
        recommendations_html = '<p style="color:#57606a">No high or medium risk recommendations.</p>'

    # Framework filter buttons (for findings tab)
    fw_filter_btns = ""
    for fw in fw_names:
        cnt = sum(1 for r in agent_results if r.framework == fw for _ in r.findings)
        fw_filter_btns += f'<button class="filter-btn" data-type="fw" onclick="filterFramework(\'{html.escape(fw)}\', this)">{html.escape(fw)} ({cnt})</button>\n'

    # Framework findings
    framework_findings_html = ""
    finding_num = 0
    for result in agent_results:
        meta = FRAMEWORK_META.get(result.framework, {})
        fwid = result.framework.lower().replace(" ", "-").replace(".", "")
        cnt = len(result.findings)
        framework_findings_html += f'<div class="framework-section" id="{fwid}" data-framework="{html.escape(result.framework)}">\n'
        framework_findings_html += (
            f'<div class="framework-header"><div><div class="framework-name">{html.escape(result.framework)}</div>'
            f'<div class="framework-meta">{html.escape(meta.get("body", ""))} &middot; {html.escape(meta.get("risk", ""))}</div></div>'
            f'<div class="framework-count">{cnt} findings</div></div>\n'
        )
        for f in result.findings:
            finding_num += 1
            sev_cls = _severity_class(f.finding_level)
            fid = f"f{finding_num}"
            ev_text = ""
            if f.evidence:
                for e in f.evidence[:8]:
                    ev_text += f"{html.escape(e.file_path)}:{e.line_number}  {html.escape(e.content[:100])}\n"
            else:
                ev_text = "No matching code patterns found.\n"
            verdict_html = ""
            if f.review_verdict:
                v_cls = _verdict_css(f.review_verdict)
                verdict_html = f'<div class="verdict-block"><div class="verdict-header">Independent Review</div><div class="verdict-label {v_cls}">{html.escape(f.review_verdict)}</div>'
                if f.judge_reasoning:
                    verdict_html += f'<div class="verdict-text">{html.escape(f.judge_reasoning)}</div>'
                if f.judge_confidence:
                    verdict_html += f'<div class="verdict-model">Gemini 2.5 Flash &middot; Confidence: {html.escape(f.judge_confidence)}</div>'
                verdict_html += '</div>'
            framework_findings_html += f'''<div class="finding" id="f-{fid}" data-framework="{html.escape(result.framework)}" data-severity="{html.escape(f.finding_level)}">
<div class="finding-header" onclick="toggleFinding('{fid}')">
<div class="finding-left"><div class="finding-num">{html.escape(f.question_id)}</div><div class="finding-question">{html.escape(f.legal_question[:130])}</div></div>
<div class="finding-right"><span class="badge badge-{sev_cls}">{html.escape(f.finding_level)}</span><span class="chevron">&#8250;</span></div>
</div>
<div class="finding-body">
<div class="finding-grid"><div><div class="field-label">Regulatory Standard</div><div class="citation">{html.escape(f.regulatory_standard)}</div></div><div>{verdict_html}</div></div>
<div class="field-label">Evidence</div><div class="evidence-block">{ev_text}</div>
<div class="field-label">Finding</div><div class="field-value" style="margin-bottom:16px">{html.escape(f.finding_text)}</div>
<div class="field-label" style="color:#1A7F37">Remediation</div><div class="remediation-block">{html.escape(f.improved_remediation if f.improved_remediation else f.remediation)}</div>{'<div style="font-size:12px;color:#0052CC;font-style:italic;margin-top:4px">Remediation refined by Gemini review</div>' if f.improved_remediation else ''}
</div></div>\n'''
        framework_findings_html += '</div>\n'

    e = html.escape
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width">
<title>OpenDocket — {e(repo_name)}</title>
<style>{_CSS}</style>
</head>
<body>
<div class="top-bar"></div>
<nav class="nav"><a href="../index.html" class="nav-brand"><span class="nav-brand-shield"></span> OpenDocket</a><div class="nav-links"><a href="../index.html">Directory</a><a href="../dashboard.html">Dashboard</a><a href="../methodology.html">Methodology</a><a href="../questions.html">Questions</a></div></nav>
<div class="action-bar"><div class="action-bar-left"><span style="font-size:13px;color:#57606a;font-weight:600">{e(repo_name)}</span><span style="font-size:13px;color:#8c959f">&middot; {total} findings &middot; {e(risk_label)}</span></div><div class="action-bar-right"><button class="btn" onclick="expandAll()">Expand all</button><button class="btn" onclick="collapseAll()">Collapse all</button><button class="btn btn-primary" onclick="window.print()">Print / PDF</button></div></div>
<div class="tab-bar"><button class="tab-btn active" onclick="showTab('overview',this)">Overview</button><button class="tab-btn" onclick="showTab('findings',this)">Findings</button><button class="tab-btn" onclick="showTab('methodology',this)">Methodology &amp; Limitations</button></div>
<div class="page">
<div class="report-header"><div class="report-eyebrow">Compliance Risk Analysis</div><div class="report-title">{e(repo_name)}</div><div class="report-meta"><a href="{e(repo_url)}">{e(repo_url)}</a><br>Scanned {scan_date} &middot; OpenDocket V1 &middot; Primary: Claude Sonnet &middot; Review: Gemini 2.5 Flash</div></div>

<!-- TAB 1: OVERVIEW -->
<div class="tab-panel active" id="tab-overview">
<div class="callout callout-amber" style="margin-bottom:24px;padding:20px 24px"><div style="font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;color:#9A6700;margin-bottom:12px">Important Limitations of This Report</div><div style="font-size:13px;line-height:1.8"><strong>This report is not legal advice and is not defensible in court.</strong> It provides directional guidance only. To obtain a defensible compliance assessment, engage a licensed attorney and certified auditor.<br><br><strong>Scope limitations:</strong> Only public repository content was analyzed. Infrastructure configuration, deployment settings, operational policies, vendor contracts, and staff training are outside scope.<br><br><strong>A true compliance audit</strong> would also review: vendor contracts and BAAs, staff training records, incident response procedures, physical security controls, and system audit logs — none of which are visible in source code.</div></div>
<div class="section" id="summary"><div class="section-heading">Risk Assessment</div><p style="font-size:15px;line-height:1.8;margin-bottom:24px">{e(exec_para)}</p>
<div class="risk-index"><div class="risk-label" style="color:{risk_color}">{e(risk_label)}</div><div class="risk-desc">{e(risk_desc)}</div></div>
{'<div class="section-heading">What This Means If Unaddressed</div><table class="table"><thead><tr><th>Framework</th><th>Regulatory Body</th><th>Max Penalty</th><th>Enforcement Trend</th></tr></thead><tbody>' + consequence_html + '</tbody></table>' if consequence_html else ''}
<div class="section-heading">Top Findings</div>{top_findings_html}
<div class="judge-block"><div class="judge-title">Independent Review — Gemini 2.5 Flash</div><div class="judge-stats"><div class="judge-stat"><span class="judge-stat-n j-confirmed">{judge_confirmed}</span><span class="judge-stat-l">Confirmed</span></div><div class="judge-stat"><span class="judge-stat-n j-context">{judge_context}</span><span class="judge-stat-l">Context dependent</span></div><div class="judge-stat"><span class="judge-stat-n j-fp">{judge_fp}</span><span class="judge-stat-l">Possible false positives</span></div><div class="judge-stat"><span class="judge-stat-n j-additional">{judge_additional}</span><span class="judge-stat-l">Additional risk</span></div></div><div class="judge-note">Primary: Claude Sonnet (Anthropic). Review: Gemini 2.5 Flash (Google). Neither constitutes legal advice.</div></div>
<div class="section-heading">Recommended Actions</div>{recommendations_html}
<div class="section-heading" style="margin-top:32px">Risk Scorecard</div><table class="table"><thead><tr><th>Framework</th><th>High Risk</th><th>Medium</th><th>Concern</th><th>No Issue</th></tr></thead><tbody>{scorecard_html}</tbody></table>
<div class="section-heading" style="margin-top:24px">Domains Detected</div>{domains_html}
</div></div>

<!-- TAB 2: FINDINGS -->
<div class="tab-panel" id="tab-findings">
<div class="filter-bar"><span class="filter-label">Framework:</span><button class="filter-btn active" data-type="fw" onclick="filterFramework('all',this)">All ({total})</button>{fw_filter_btns}<div class="filter-sep"></div><span class="filter-label">Severity:</span><button class="filter-btn active" data-type="sev" onclick="filterSeverity('all',this)">All</button><button class="filter-btn" data-type="sev" onclick="filterSeverity('High Risk',this)">High ({high})</button><button class="filter-btn" data-type="sev" onclick="filterSeverity('Medium Risk',this)">Medium ({med})</button><button class="filter-btn" data-type="sev" onclick="filterSeverity('Pattern of Concern',this)">Concern ({concern})</button></div>
{framework_findings_html}
</div>

<!-- TAB 3: METHODOLOGY -->
<div class="tab-panel" id="tab-methodology">
{_METHODOLOGY_TAB}
</div>

<div class="questions-footer">Findings based on OpenDocket's open source question libraries. <a href="../questions.html">View and contribute</a></div>
</div>
<script>
function showTab(name,btn){{document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));document.getElementById('tab-'+name).classList.add('active');document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));btn.classList.add('active')}}
function toggleFinding(id){{document.getElementById('f-'+id).classList.toggle('open')}}
function expandAll(){{document.querySelectorAll('.finding').forEach(f=>f.classList.add('open'))}}
function collapseAll(){{document.querySelectorAll('.finding').forEach(f=>f.classList.remove('open'))}}
let aFw='all',aSev='all';
function filterFramework(fw,btn){{aFw=fw;document.querySelectorAll('[data-type=fw]').forEach(b=>b.classList.remove('active'));btn.classList.add('active');applyF()}}
function filterSeverity(sev,btn){{aSev=sev;document.querySelectorAll('[data-type=sev]').forEach(b=>b.classList.remove('active'));btn.classList.add('active');applyF()}}
function applyF(){{document.querySelectorAll('.finding').forEach(f=>{{const ok=(aFw==='all'||f.dataset.framework===aFw)&&(aSev==='all'||f.dataset.severity===aSev);f.style.display=ok?'':'none'}});document.querySelectorAll('.framework-section').forEach(s=>{{s.style.display=(aFw==='all'||s.dataset.framework===aFw)?'':'none'}})}}
fetch('/api/track',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{event:'report_open',repo:'{e(repo_name)}',source:document.referrer||'direct'}})}}).catch(()=>{{}});
</script>
</body>
</html>"""


def generate_failed_gate_html(
    repo_name: str, repo_url: str, reasons: list[str], stats: dict,
) -> str:
    reasons_html = "".join(f"<li>{html.escape(r)}</li>\n" for r in reasons)
    stats_html = "".join(
        f"<li><strong>{html.escape(str(k))}:</strong> {html.escape(str(v))}</li>\n"
        for k, v in stats.items()
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width">
<title>OpenDocket: {html.escape(repo_name)} (Did Not Qualify)</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:15px;line-height:1.6;color:#1a1a1a;background:#fff}}
a{{color:#0052CC;text-decoration:none}}
.top-bar{{height:4px;background:#0052CC}}
.nav{{background:#fff;border-bottom:1px solid #d0d7de;padding:0 40px;height:48px;display:flex;align-items:center;justify-content:space-between}}
.nav-brand{{font-size:15px;font-weight:700;color:#1a1a1a;text-decoration:none;display:flex;align-items:center;gap:8px}}
.nav-brand-shield{{width:20px;height:24px;background:#0052CC;clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);display:inline-block}}
.nav-links a{{font-size:13px;color:#57606a;text-decoration:none;margin-left:24px}}
.container{{max-width:800px;margin:40px auto;padding:0 40px}}
h1{{font-size:24px;font-weight:700;color:#cf222e;border-bottom:1px solid #d0d7de;padding-bottom:16px;margin-bottom:24px}}
.meta{{color:#57606a;font-size:13px;margin-bottom:24px}}
.disclaimer{{background:#f6f8fa;border:1px solid #d0d7de;border-left:4px solid #0052CC;padding:16px 20px;margin-bottom:24px;font-size:13px;color:#57606a}}
.gate-fail{{background:#fff8f8;border:1px solid #d0d7de;border-left:4px solid #cf222e;padding:24px;margin-bottom:24px}}
.gate-fail h2{{font-size:18px;margin-bottom:12px;color:#cf222e}}
.gate-fail ul{{padding-left:20px;margin:12px 0}}.gate-fail li{{margin-bottom:8px;font-size:14px}}
@media print{{.nav{{display:none}}body{{font-size:12px}}}}
</style>
</head>
<body>
<div class="top-bar"></div>
<nav class="nav"><a href="../index.html" class="nav-brand"><span class="nav-brand-shield"></span> OpenDocket</a><div class="nav-links"><a href="../index.html">Directory</a><a href="../methodology.html">Methodology</a></div></nav>
<div class="container">
<h1>Qualification Report: {html.escape(repo_name)}</h1>
<div class="meta">Repository: <a href="{html.escape(repo_url)}">{html.escape(repo_url)}</a> &middot; {datetime.now().strftime('%Y-%m-%d')}</div>
<div class="disclaimer">{html.escape(DISCLAIMER)}</div>
<div class="gate-fail"><h2>Does Not Qualify for Scanning</h2><p>This repository did not meet the minimum criteria for a meaningful compliance scan.</p><h3 style="margin-top:16px;font-size:14px">Failed Gates</h3><ul>{reasons_html}</ul><h3 style="margin-top:16px;font-size:14px">Repository Statistics</h3><ul>{stats_html}</ul></div>
<p style="font-size:14px;color:#57606a">To qualify: README with 10+ meaningful lines, 10+ code files, evidence of data handling.</p>
</div>
</body>
</html>"""
