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
    "This report does not constitute legal advice. Regulatory compliance "
    "requires qualified legal and technical assessment. Consult a licensed "
    "attorney and certified compliance professional for definitive compliance "
    "determination."
)

FRAMEWORK_META = {
    "HIPAA": {"body": "HHS / OCR", "risk": "Fines up to $1.5M/year per category"},
    "SOC2": {"body": "AICPA", "risk": "Loss of enterprise contracts"},
    "PCI-DSS": {"body": "PCI SSC", "risk": "Fines $5K-$100K/month"},
    "GDPR": {"body": "EU DPAs", "risk": "Up to EUR 20M or 4% turnover"},
    "TCPA": {"body": "FCC", "risk": "$500-$1,500 per violation"},
    "SOX": {"body": "SEC / PCAOB", "risk": "Criminal penalties, delisting"},
}


def calculate_score(agent_results: list[AgentResult]) -> int:
    if not agent_results:
        return 100
    all_findings = [f for r in agent_results for f in r.findings]
    num_frameworks = len(agent_results)
    raw_penalty = 0
    for f in all_findings:
        if f.finding_level == "High Risk":
            raw_penalty += 8
        elif f.finding_level == "Medium Risk":
            raw_penalty += 3
        elif f.finding_level == "Pattern of Concern":
            raw_penalty += 1
    if num_frameworks > 0:
        normalized_penalty = raw_penalty / num_frameworks * 2
    else:
        normalized_penalty = raw_penalty
    return max(0, round(100 - normalized_penalty))


def _severity_class(level: str) -> str:
    return {"High Risk": "high", "Medium Risk": "med",
            "Pattern of Concern": "concern", "No Issue Found": "ok"}.get(level, "")


def _verdict_css(verdict: str) -> str:
    return {"CONFIRMED": "v-confirmed", "CONTEXT DEPENDENT": "v-context",
            "POSSIBLE FALSE POSITIVE": "v-fp", "ADDITIONAL RISK": "v-additional"}.get(verdict, "")


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
    lines.append("## Executive Summary")
    lines.append("")
    lines.append("| Finding Level | Count |")
    lines.append("|---|---|")
    all_findings = [f for r in agent_results for f in r.findings]
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
            lines.append("**LEGAL QUESTION**")
            lines.append("")
            lines.append(finding.legal_question)
            lines.append("")
            lines.append("**REGULATORY STANDARD**")
            lines.append("")
            lines.append(finding.regulatory_standard)
            lines.append("")
            lines.append("**EVIDENCE**")
            lines.append("")
            if finding.evidence:
                for e in finding.evidence[:10]:
                    lines.append(f"- `{e.file_path}:{e.line_number}` — `{e.content[:120]}`")
            else:
                lines.append("- No matching code patterns found.")
            lines.append("")
            emoji = {"High Risk": "🔴", "Medium Risk": "🟠",
                     "Pattern of Concern": "🔵", "No Issue Found": "🟢"}.get(finding.finding_level, "")
            lines.append(f"**FINDING: {emoji} {finding.finding_level}**")
            lines.append("")
            lines.append(finding.finding_text)
            lines.append("")
            lines.append("**REMEDIATION DIRECTION**")
            lines.append("")
            lines.append(finding.remediation)
            lines.append("")
            lines.append("---")
            lines.append("")
    lines.append(f"**DISCLAIMER:** {DISCLAIMER}")
    lines.append("")
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


# ── HTML Report — Complete Light Mode Rewrite ──

_CSS = """*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #1a1a1a; background: #ffffff; }
.top-bar { height: 4px; background: #0052CC; }
.nav { background: #ffffff; border-bottom: 1px solid #d0d7de; padding: 0 40px; height: 48px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; z-index: 200; }
.nav-brand { font-size: 15px; font-weight: 700; color: #1a1a1a; text-decoration: none; display: flex; align-items: center; gap: 8px; }
.nav-brand-shield { width: 20px; height: 24px; background: #0052CC; clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%); display: inline-block; }
.nav-links { display: flex; gap: 24px; }
.nav-links a { font-size: 13px; color: #57606a; text-decoration: none; } .nav-links a:hover { color: #0052CC; }
.action-bar { background: #f6f8fa; border-bottom: 1px solid #d0d7de; padding: 8px 40px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 48px; z-index: 190; }
.action-bar-left { display: flex; gap: 8px; align-items: center; } .action-bar-right { display: flex; gap: 8px; }
.filter-bar { background: #ffffff; border-bottom: 1px solid #d0d7de; padding: 8px 40px; display: flex; align-items: center; gap: 8px; flex-wrap: wrap; position: sticky; top: 96px; z-index: 180; }
.filter-label { font-size: 12px; font-weight: 600; color: #57606a; text-transform: uppercase; letter-spacing: 0.5px; }
.filter-sep { width: 1px; height: 16px; background: #d0d7de; margin: 0 4px; }
.filter-btn { font-size: 12px; padding: 3px 10px; border: 1px solid #d0d7de; background: #ffffff; color: #57606a; cursor: pointer; border-radius: 2px; font-family: inherit; }
.filter-btn:hover { border-color: #0052CC; color: #0052CC; }
.filter-btn.active { background: #0052CC; color: #ffffff; border-color: #0052CC; }
.btn { font-size: 13px; padding: 6px 14px; border: 1px solid #d0d7de; background: #ffffff; color: #1a1a1a; cursor: pointer; border-radius: 2px; font-family: inherit; } .btn:hover { background: #f6f8fa; }
.btn-primary { background: #0052CC; color: #ffffff; border-color: #0052CC; } .btn-primary:hover { background: #0047B3; }
.page { display: grid; grid-template-columns: 220px 1fr; max-width: 1200px; margin: 0 auto; padding: 32px 40px; gap: 40px; }
.sidebar { position: sticky; top: 150px; height: fit-content; }
.sidebar-nav { list-style: none; } .sidebar-nav li { margin-bottom: 4px; }
.sidebar-nav a { font-size: 13px; color: #57606a; text-decoration: none; display: block; padding: 4px 8px; border-radius: 2px; border-left: 2px solid transparent; }
.sidebar-nav a:hover { color: #0052CC; background: #f6f8fa; }
.sidebar-section-label { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: #8c959f; padding: 8px 8px 4px; margin-top: 8px; }
.main { min-width: 0; }
.section { margin-bottom: 40px; scroll-margin-top: 160px; }
.section-heading { font-size: 13px; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase; color: #57606a; border-bottom: 1px solid #d0d7de; padding-bottom: 8px; margin-bottom: 20px; }
.report-header { margin-bottom: 32px; }
.report-eyebrow { font-size: 12px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #57606a; margin-bottom: 8px; }
.report-title { font-size: 26px; font-weight: 700; color: #1a1a1a; margin-bottom: 8px; }
.report-meta { font-size: 13px; color: #57606a; line-height: 1.8; } .report-meta a { color: #0052CC; text-decoration: none; }
.callout { padding: 14px 16px; margin-bottom: 16px; border: 1px solid #d0d7de; border-left-width: 4px; font-size: 13px; line-height: 1.6; color: #1a1a1a; } .callout strong { font-weight: 600; }
.callout-blue { border-left-color: #0052CC; background: #f0f5ff; }
.callout-yellow { border-left-color: #9A6700; background: #fffbe0; }
.scope-list { list-style: none; margin: 8px 0 0 0; } .scope-list li { font-size: 13px; color: #57606a; padding: 3px 0; } .scope-list li::before { content: "\\2717  "; color: #cf222e; font-weight: 700; }
.score-block { display: flex; align-items: center; gap: 20px; padding: 20px 24px; background: #f6f8fa; border: 1px solid #d0d7de; margin-bottom: 24px; }
.score-number { font-size: 52px; font-weight: 700; line-height: 1; }
.score-title { font-size: 16px; font-weight: 600; color: #1a1a1a; margin-bottom: 4px; }
.score-desc { font-size: 13px; color: #57606a; } .score-desc a { color: #0052CC; }
.table { width: 100%; border-collapse: collapse; font-size: 14px; margin-bottom: 20px; }
.table th { text-align: left; padding: 8px 12px; background: #f6f8fa; border: 1px solid #d0d7de; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: #57606a; }
.table td { padding: 10px 12px; border: 1px solid #d0d7de; color: #1a1a1a; vertical-align: top; }
.table tr:nth-child(even) td { background: #f6f8fa; }
.n-high { color: #cf222e; font-weight: 700; } .n-med { color: #9A6700; font-weight: 700; } .n-concern { color: #0052CC; font-weight: 600; } .n-ok { color: #1A7F37; }
.domain-row { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; font-size: 14px; }
.domain-name { width: 130px; font-weight: 500; color: #1a1a1a; }
.domain-bar-wrap { flex: 1; height: 6px; background: #eaeef2; border-radius: 3px; overflow: hidden; }
.domain-bar { height: 100%; background: #0052CC; border-radius: 3px; }
.domain-pct { width: 44px; text-align: right; font-size: 13px; color: #57606a; }
.judge-block { background: #f0f5ff; border: 1px solid #d0d7de; border-left: 4px solid #0052CC; padding: 16px 20px; margin-bottom: 24px; }
.judge-title { font-size: 12px; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase; color: #0052CC; margin-bottom: 12px; }
.judge-stats { display: flex; gap: 32px; flex-wrap: wrap; margin-bottom: 12px; } .judge-stat { text-align: center; }
.judge-stat-n { font-size: 24px; font-weight: 700; display: block; line-height: 1.2; } .judge-stat-l { font-size: 12px; color: #57606a; display: block; }
.j-confirmed { color: #1A7F37; } .j-context { color: #9A6700; } .j-fp { color: #cf222e; } .j-additional { color: #6E40C9; }
.judge-note { font-size: 12px; color: #8c959f; border-top: 1px solid #d0d7de; padding-top: 10px; margin-top: 4px; }
.top-finding { border: 1px solid #d0d7de; border-left: 4px solid #cf222e; background: #fff8f8; padding: 14px 16px; margin-bottom: 10px; }
.top-finding-q { font-size: 14px; font-weight: 600; color: #1a1a1a; margin-bottom: 6px; }
.top-finding-meta { display: flex; gap: 12px; font-size: 12px; color: #57606a; }
.badge { display: inline-block; font-size: 11px; font-weight: 700; letter-spacing: 0.3px; text-transform: uppercase; padding: 2px 8px; border-radius: 2px; }
.badge-high { color: #cf222e; background: #fff0f0; border: 1px solid #cf222e; }
.badge-med { color: #9A6700; background: #fffbe0; border: 1px solid #9A6700; }
.badge-concern { color: #0052CC; background: #f0f5ff; border: 1px solid #0052CC; }
.badge-ok { color: #1A7F37; background: #f0fff4; border: 1px solid #1A7F37; }
.rec-item { display: flex; gap: 16px; padding: 14px 0; border-bottom: 1px solid #d0d7de; } .rec-item:last-child { border-bottom: none; }
.rec-priority { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; min-width: 70px; padding-top: 2px; }
.rec-p-high { color: #cf222e; } .rec-p-med { color: #9A6700; }
.rec-text { font-size: 14px; color: #1a1a1a; line-height: 1.6; } .rec-fw { font-size: 12px; color: #57606a; margin-top: 3px; }
.framework-section { margin-bottom: 36px; scroll-margin-top: 160px; }
.framework-header { background: #f6f8fa; border: 1px solid #d0d7de; border-left: 4px solid #0052CC; padding: 12px 16px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: flex-start; }
.framework-name { font-size: 15px; font-weight: 700; color: #1a1a1a; margin-bottom: 4px; } .framework-meta { font-size: 12px; color: #57606a; }
.framework-count { font-size: 13px; color: #57606a; white-space: nowrap; padding-left: 16px; }
.finding { border: 1px solid #d0d7de; margin-bottom: 8px; page-break-inside: avoid; }
.finding[data-severity="High Risk"] { border-left: 4px solid #cf222e; }
.finding[data-severity="Medium Risk"] { border-left: 4px solid #9A6700; }
.finding[data-severity="Pattern of Concern"] { border-left: 4px solid #0052CC; }
.finding[data-severity="No Issue Found"] { border-left: 4px solid #1A7F37; }
.finding-header { display: flex; align-items: flex-start; justify-content: space-between; padding: 12px 16px; background: #f6f8fa; cursor: pointer; user-select: none; gap: 12px; } .finding-header:hover { background: #eaeef2; }
.finding-left { flex: 1; min-width: 0; }
.finding-num { font-size: 11px; font-family: "SFMono-Regular", Consolas, monospace; color: #8c959f; margin-bottom: 4px; }
.finding-question { font-size: 14px; font-weight: 600; color: #1a1a1a; line-height: 1.4; }
.finding-right { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.chevron { font-size: 12px; color: #57606a; transition: transform 0.15s; display: inline-block; } .finding.open .chevron { transform: rotate(90deg); }
.finding-body { display: none; padding: 20px; border-top: 1px solid #d0d7de; } .finding.open .finding-body { display: block; }
.finding-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 16px; }
.field-label { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: #57606a; margin-bottom: 6px; }
.field-value { font-size: 14px; color: #1a1a1a; line-height: 1.6; } .citation { font-size: 13px; color: #0052CC; font-style: italic; }
.verdict-block { background: #f6f8fa; border: 1px solid #d0d7de; padding: 12px 14px; margin-bottom: 16px; }
.verdict-header { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: #57606a; margin-bottom: 8px; }
.verdict-label { font-size: 12px; font-weight: 700; text-transform: uppercase; white-space: nowrap; }
.v-confirmed { color: #1A7F37; } .v-context { color: #9A6700; } .v-fp { color: #cf222e; } .v-additional { color: #6E40C9; }
.verdict-text { font-size: 13px; color: #57606a; line-height: 1.5; } .verdict-model { font-size: 11px; color: #8c959f; margin-top: 4px; }
.evidence-block { background: #f6f8fa; border: 1px solid #d0d7de; border-left: 3px solid #0052CC; padding: 14px 16px; font-family: "SFMono-Regular", Consolas, monospace; font-size: 13px; color: #1a1a1a; white-space: pre-wrap; overflow-x: auto; margin-bottom: 16px; line-height: 1.5; }
.remediation-block { background: #f0fff4; border: 1px solid #d0d7de; border-left: 3px solid #1A7F37; padding: 14px 16px; font-size: 14px; color: #1a1a1a; line-height: 1.7; }
.questions-footer { border-top: 1px solid #d0d7de; padding: 20px 0; text-align: center; font-size: 13px; color: #57606a; margin-top: 40px; } .questions-footer a { color: #0052CC; }
@media print { .top-bar, .nav, .action-bar, .filter-bar, .sidebar { display: none; } .page { display: block; padding: 0; } .finding-body { display: block !important; } .finding-header { cursor: default; } body { font-size: 12px; } .section { page-break-inside: avoid; } .finding { page-break-inside: avoid; margin-bottom: 12px; } @page { margin: 2cm; } }
@media (max-width: 768px) { .page { grid-template-columns: 1fr; } .sidebar { display: none; } .nav, .action-bar, .filter-bar { padding-left: 16px; padding-right: 16px; } }"""


def generate_html_report(
    repo_name: str, repo_url: str,
    domains: list[DomainResult], agent_results: list[AgentResult],
) -> str:
    """Generate a professional light-mode HTML compliance report."""
    scan_date = datetime.now().strftime('%Y-%m-%d')
    all_findings = [f for r in agent_results for f in r.findings]
    score = calculate_score(agent_results)
    high = sum(1 for f in all_findings if f.finding_level == "High Risk")
    med = sum(1 for f in all_findings if f.finding_level == "Medium Risk")
    concern = sum(1 for f in all_findings if f.finding_level == "Pattern of Concern")
    ok = sum(1 for f in all_findings if f.finding_level == "No Issue Found")
    total = len(all_findings)
    fw_names = [r.framework for r in agent_results]
    fw_names_str = ", ".join(fw_names)

    # Score color
    if score >= 70:
        score_color = "#1A7F37"
    elif score >= 40:
        score_color = "#9A6700"
    else:
        score_color = "#cf222e"

    # Scorecard rows
    scorecard_html = ""
    for result in agent_results:
        h = sum(1 for f in result.findings if f.finding_level == "High Risk")
        m = sum(1 for f in result.findings if f.finding_level == "Medium Risk")
        c = sum(1 for f in result.findings if f.finding_level == "Pattern of Concern")
        o = sum(1 for f in result.findings if f.finding_level == "No Issue Found")
        scorecard_html += f'<tr><td style="font-weight:600">{html.escape(result.framework)}</td><td class="n-high">{h}</td><td class="n-med">{m}</td><td class="n-concern">{c}</td><td class="n-ok">{o}</td></tr>\n'

    # Domains with progress bars
    domains_html = ""
    for d in domains:
        pct = min(d.confidence, 100)
        domains_html += (
            f'<div class="domain-row"><span class="domain-name">{html.escape(d.domain.title())}</span>'
            f'<div class="domain-bar-wrap"><div class="domain-bar" style="width:{pct}%"></div></div>'
            f'<span class="domain-pct">{d.confidence}%</span></div>\n'
        )

    # Judge counts
    judge_confirmed = sum(1 for f in all_findings if f.review_verdict == "CONFIRMED")
    judge_context = sum(1 for f in all_findings if f.review_verdict == "CONTEXT DEPENDENT")
    judge_fp = sum(1 for f in all_findings if f.review_verdict == "POSSIBLE FALSE POSITIVE")
    judge_additional = sum(1 for f in all_findings if f.review_verdict == "ADDITIONAL RISK")

    # Top findings
    sev_order = {"High Risk": 0, "Medium Risk": 1, "Pattern of Concern": 2, "No Issue Found": 3}
    sorted_f = sorted(all_findings, key=lambda f: sev_order.get(f.finding_level, 3))
    top_findings_html = ""
    for f in sorted_f[:3]:
        sev_cls = _severity_class(f.finding_level)
        top_findings_html += (
            f'<div class="top-finding"><div class="top-finding-q">{html.escape(f.legal_question[:140])}</div>'
            f'<div class="top-finding-meta"><span class="badge badge-{sev_cls}">{html.escape(f.finding_level)}</span>'
            f'<span>{html.escape(f.question_id)}</span></div></div>\n'
        )

    # Recommendations
    recommendations_html = ""
    for f in sorted_f:
        if f.finding_level == "High Risk" and f.remediation:
            recommendations_html += (
                f'<div class="rec-item"><div class="rec-priority rec-p-high">High</div>'
                f'<div><div class="rec-text">{html.escape(f.remediation)}</div>'
                f'<div class="rec-fw">{html.escape(f.question_id)}</div></div></div>\n'
            )
    for f in sorted_f:
        if f.finding_level == "Medium Risk" and f.remediation:
            recommendations_html += (
                f'<div class="rec-item"><div class="rec-priority rec-p-med">Medium</div>'
                f'<div><div class="rec-text">{html.escape(f.remediation)}</div>'
                f'<div class="rec-fw">{html.escape(f.question_id)}</div></div></div>\n'
            )
    if not recommendations_html:
        recommendations_html = '<p style="color:#57606a">No high or medium risk recommendations.</p>'

    # Framework filter buttons
    fw_filter_btns = ""
    for fw in fw_names:
        cnt = sum(1 for r in agent_results if r.framework == fw for _ in r.findings)
        fw_filter_btns += f'<button class="filter-btn" data-type="fw" onclick="filterFramework(\'{html.escape(fw)}\', this)">{html.escape(fw)} ({cnt})</button>\n'

    # Sidebar links
    sidebar_links = ""
    for fw in fw_names:
        fwid = fw.lower().replace(" ", "-").replace(".", "")
        sidebar_links += f'<li><a href="#{fwid}">{html.escape(fw)}</a></li>\n'

    # Framework sections with findings
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
                    verdict_html += f'<div class="verdict-model">Gemini 1.5 Flash &middot; Confidence: {html.escape(f.judge_confidence)}</div>'
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
<div class="field-label" style="color:#1A7F37">Remediation</div><div class="remediation-block">{html.escape(f.remediation)}</div>
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
<div class="action-bar"><div class="action-bar-left"><span style="font-size:13px;color:#57606a;font-weight:600">{e(repo_name)}</span><span style="font-size:13px;color:#8c959f">&middot; {total} findings &middot; Score: {score}</span></div><div class="action-bar-right"><button class="btn" onclick="expandAll()">Expand all</button><button class="btn" onclick="collapseAll()">Collapse all</button><button class="btn btn-primary" onclick="window.print()">Print / PDF</button></div></div>
<div class="filter-bar"><span class="filter-label">Framework:</span><button class="filter-btn active" data-type="fw" onclick="filterFramework('all', this)">All ({total})</button>{fw_filter_btns}<div class="filter-sep"></div><span class="filter-label">Severity:</span><button class="filter-btn active" data-type="sev" onclick="filterSeverity('all', this)">All</button><button class="filter-btn" data-type="sev" onclick="filterSeverity('High Risk', this)">High ({high})</button><button class="filter-btn" data-type="sev" onclick="filterSeverity('Medium Risk', this)">Medium ({med})</button><button class="filter-btn" data-type="sev" onclick="filterSeverity('Pattern of Concern', this)">Concern ({concern})</button></div>
<div class="page">
<aside class="sidebar"><ul class="sidebar-nav"><li class="sidebar-section-label">Overview</li><li><a href="#summary">Executive Summary</a></li><li><a href="#judge">Independent Review</a></li><li><a href="#recommendations">Recommendations</a></li><li class="sidebar-section-label">Findings</li>{sidebar_links}<li class="sidebar-section-label">About</li><li><a href="../methodology.html">Methodology</a></li><li><a href="../questions.html">Questions</a></li></ul></aside>
<main class="main">
<div class="report-header section" id="header"><div class="report-eyebrow">Compliance Risk Analysis</div><div class="report-title">{e(repo_name)}</div><div class="report-meta"><a href="{e(repo_url)}">{e(repo_url)}</a><br>Scanned {scan_date} &middot; OpenDocket V1<br>Primary: Claude Sonnet (Anthropic) &middot; Review: Gemini 1.5 Flash (Google)</div></div>
<div style="background:#f6f8fa;border:1px solid #d0d7de;padding:12px 16px;margin-bottom:24px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px"><div style="font-size:13px;color:#57606a">Share this report:</div><div style="display:flex;gap:8px"><button class="btn" onclick="navigator.clipboard.writeText(window.location.href).then(()=>{{this.textContent='Copied!';setTimeout(()=>this.textContent='Copy link',2000)}})">Copy link</button><a class="btn" href="https://twitter.com/intent/tweet?text=OpenDocket+compliance+scan+of+{e(repo_name)}:+{high}+high+risk+patterns.+Score:+{score}/100&amp;url=https://opendocket.dev/reports/{e(repo_name)}_report.html" target="_blank">Share on X</a><a class="btn" href="https://github.com/{e(repo_name)}/issues/new?title=OpenDocket+Compliance+Scan+Results&amp;body=OpenDocket+found+{high}+high-risk+compliance+patterns.+Full+report:+https://opendocket.dev/reports/{e(repo_name)}_report.html" target="_blank">Open GitHub Issue</a></div></div>
<div style="background:#f6f8fa;border:1px solid #d0d7de;padding:10px 16px;margin-bottom:24px;font-size:12px;color:#57606a">Add to your README: <code style="background:#eaeef2;padding:2px 6px;border-radius:2px;font-size:11px">[![OpenDocket Score](https://opendocket.dev/badge/{score}.svg)](https://opendocket.dev/reports/{e(repo_name)}_report.html)</code></div>
<div class="callout callout-blue" style="margin-bottom:12px"><strong>Not legal advice.</strong> This report identifies risk patterns through automated code analysis. It is the starting point for a compliance conversation — not the end of one.</div>
<div class="callout callout-yellow" style="margin-bottom:32px"><strong>Scope:</strong> Source code patterns only.<ul class="scope-list"><li>Whether features work as intended (use your test suite)</li><li>Cloud config, network security, deployed infrastructure</li><li>Internal policies, staff training, vendor contracts</li></ul><div style="margin-top:8px;font-size:13px"><strong>Example:</strong> If you send SMS, OpenDocket checks consent handling. It does not check whether the SMS reached the recipient.</div></div>
<div class="section" id="summary"><div class="section-heading">Executive Summary</div><p style="font-size:15px;line-height:1.8;margin-bottom:24px">This analysis identified <strong>{total} findings</strong> across <strong>{e(fw_names_str)}</strong>. Of these, <strong style="color:#cf222e">{high} represent high-severity risk patterns</strong> consistent with potential non-compliance. The OpenDocket Score is {score}/100.</p><div class="score-block"><div class="score-number" style="color:{score_color}">{score}</div><div><div class="score-title">OpenDocket Score</div><div class="score-desc">Lower = more risk patterns. <a href="../methodology.html">How calculated</a></div></div></div><div class="section-heading">Risk Scorecard</div><table class="table"><thead><tr><th>Framework</th><th>High Risk</th><th>Medium</th><th>Concern</th><th>No Issue</th></tr></thead><tbody>{scorecard_html}</tbody></table><div class="section-heading" style="margin-top:24px">Domains Detected</div>{domains_html}</div>
<div class="judge-block section" id="judge"><div class="judge-title">Independent Review — Gemini 1.5 Flash</div><div class="judge-stats"><div class="judge-stat"><span class="judge-stat-n j-confirmed">{judge_confirmed}</span><span class="judge-stat-l">Confirmed</span></div><div class="judge-stat"><span class="judge-stat-n j-context">{judge_context}</span><span class="judge-stat-l">Context dependent</span></div><div class="judge-stat"><span class="judge-stat-n j-fp">{judge_fp}</span><span class="judge-stat-l">Possible false positives</span></div><div class="judge-stat"><span class="judge-stat-n j-additional">{judge_additional}</span><span class="judge-stat-l">Additional risk</span></div></div><div class="judge-note">Primary: Claude Sonnet (Anthropic). Review: Gemini 1.5 Flash (Google). Neither constitutes legal advice.</div></div>
<div class="section" id="top-findings"><div class="section-heading">Top Findings</div>{top_findings_html}</div>
<div class="section" id="recommendations"><div class="section-heading">Recommended Actions</div>{recommendations_html}</div>
<div class="section" id="findings"><div class="section-heading">Detailed Findings</div>{framework_findings_html}</div>
<div class="questions-footer">Findings based on OpenDocket's open source question libraries. <a href="../questions.html">View and contribute</a></div>
</main></div>
<script>
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
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:15px;line-height:1.6;color:#1a1a1a;background:#ffffff}}
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
