"""
Convert markdown reports to styled HTML for the web directory.

Reads reports/*.md and produces web/reports/*.html with the OpenDocket
dark theme styling.
"""

import os
import re
import html


def md_to_html(md_content: str, repo_name: str) -> str:
    """Convert a markdown compliance report to styled HTML."""
    lines = md_content.split("\n")
    html_parts = []
    in_table = False
    in_evidence_list = False
    table_rows = []

    for line in lines:
        stripped = line.strip()

        # Skip empty lines but preserve spacing
        if not stripped:
            if in_table:
                in_table = False
                html_parts.append(render_table(table_rows))
                table_rows = []
            if in_evidence_list:
                in_evidence_list = False
                html_parts.append("</ul>")
            html_parts.append("")
            continue

        # Headers
        if stripped.startswith("# "):
            text = html.escape(stripped[2:])
            html_parts.append(f'<h1>{text}</h1>')
            continue
        if stripped.startswith("## "):
            text = html.escape(stripped[3:])
            html_parts.append(f'<h2>{text}</h2>')
            continue
        if stripped.startswith("### "):
            text = html.escape(stripped[4:])
            # Detect finding level for color coding
            css_class = ""
            if any(level in text for level in ["High Risk", "Medium Risk", "Pattern of Concern", "No Issue Found"]):
                if "High Risk" in text:
                    css_class = ' class="high-risk"'
                elif "Medium Risk" in text:
                    css_class = ' class="medium-risk"'
                elif "Pattern of Concern" in text:
                    css_class = ' class="pattern-concern"'
                elif "No Issue Found" in text:
                    css_class = ' class="no-issue"'
            html_parts.append(f'<h3{css_class}>{text}</h3>')
            continue

        # Blockquotes (metadata)
        if stripped.startswith("> "):
            text = process_inline(stripped[2:])
            html_parts.append(f'<p class="meta-line">{text}</p>')
            continue

        # Horizontal rules
        if stripped == "---":
            html_parts.append("<hr>")
            continue

        # Table rows
        if stripped.startswith("|"):
            if stripped.replace("|", "").replace("-", "").replace(" ", "") == "":
                continue  # Skip separator row
            in_table = True
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            table_rows.append(cells)
            continue

        # List items
        if stripped.startswith("- "):
            if not in_evidence_list:
                in_evidence_list = True
                html_parts.append('<ul class="evidence-list">')
            text = process_inline(stripped[2:])
            html_parts.append(f"<li>{text}</li>")
            continue

        # Bold paragraphs (section headers within findings)
        if stripped.startswith("**") and stripped.endswith("**"):
            text = stripped[2:-2]
            # Check for finding level badges
            if "FINDING:" in text:
                css_class = "finding-badge"
                if "High Risk" in text:
                    css_class += " high-risk"
                elif "Medium Risk" in text:
                    css_class += " medium-risk"
                elif "Pattern of Concern" in text:
                    css_class += " pattern-concern"
                elif "No Issue Found" in text:
                    css_class += " no-issue"
                html_parts.append(f'<div class="{css_class}"><strong>{html.escape(text)}</strong></div>')
            elif "DISCLAIMER" in text:
                # Extract disclaimer text
                disclaimer_match = re.match(r'\*\*DISCLAIMER:\*\*\s*(.*)', stripped)
                if disclaimer_match:
                    html_parts.append(f'<div class="disclaimer">{html.escape(disclaimer_match.group(1))}</div>')
                else:
                    html_parts.append(f'<h4>{html.escape(text)}</h4>')
            else:
                html_parts.append(f'<h4>{html.escape(text)}</h4>')
            continue

        # Disclaimer lines
        if stripped.startswith("**DISCLAIMER:**"):
            text = stripped.replace("**DISCLAIMER:**", "").strip()
            html_parts.append(f'<div class="disclaimer">{html.escape(text)}</div>')
            continue

        # Regular paragraphs
        text = process_inline(stripped)
        html_parts.append(f"<p>{text}</p>")

    if in_table:
        html_parts.append(render_table(table_rows))
    if in_evidence_list:
        html_parts.append("</ul>")

    body = "\n".join(html_parts)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OpenDocket Report: {html.escape(repo_name)}</title>
  <style>
    body {{ background: #0d1117; color: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }}
    .report-container {{ max-width: 900px; margin: 0 auto; }}
    h1 {{ color: #58a6ff; border-bottom: 1px solid #21262d; padding-bottom: 12px; font-size: 1.8em; }}
    h2 {{ color: #c9d1d9; margin-top: 32px; border-bottom: 1px solid #21262d; padding-bottom: 8px; }}
    h3 {{ color: #c9d1d9; margin-top: 24px; }}
    h4 {{ color: #8b949e; font-size: 0.9em; text-transform: uppercase; letter-spacing: 0.05em; margin: 16px 0 8px; }}
    hr {{ border: none; border-top: 1px solid #21262d; margin: 24px 0; }}
    .meta-line {{ color: #8b949e; margin: 2px 0; }}
    .disclaimer {{ background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 16px; margin: 16px 0; color: #8b949e; font-size: 0.9em; }}
    a {{ color: #58a6ff; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .back-link {{ margin-bottom: 20px; display: inline-block; }}
    table {{ width: 100%; border-collapse: collapse; margin: 16px 0; }}
    th, td {{ padding: 8px 12px; text-align: left; border: 1px solid #30363d; }}
    th {{ background: #161b22; color: #c9d1d9; }}
    td {{ color: #8b949e; }}
    .evidence-list {{ font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 0.85em; padding-left: 20px; }}
    .evidence-list li {{ margin: 6px 0; }}
    code {{ background: #161b22; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; }}
    .finding-badge {{ padding: 8px 16px; border-radius: 6px; display: inline-block; margin: 12px 0; }}
    .finding-badge.high-risk {{ background: rgba(248,81,73,0.15); color: #f85149; }}
    .finding-badge.medium-risk {{ background: rgba(210,153,34,0.15); color: #d29922; }}
    .finding-badge.pattern-concern {{ background: rgba(88,166,255,0.15); color: #58a6ff; }}
    .finding-badge.no-issue {{ background: rgba(63,185,80,0.15); color: #3fb950; }}
    p {{ margin: 8px 0; }}
  </style>
</head>
<body>
  <div class="report-container">
    <a href="../index.html" class="back-link">&larr; Back to OpenDocket</a>
    {body}
  </div>
</body>
</html>"""


def process_inline(text: str) -> str:
    """Process inline markdown formatting."""
    # Escape HTML first
    text = html.escape(text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Inline code
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text


def render_table(rows: list[list[str]]) -> str:
    """Render a markdown table as HTML."""
    if not rows:
        return ""
    header = rows[0]
    body = rows[1:]

    html_str = '<table>\n<thead><tr>'
    for cell in header:
        html_str += f'<th>{html.escape(cell)}</th>'
    html_str += '</tr></thead>\n<tbody>'
    for row in body:
        html_str += '<tr>'
        for cell in row:
            html_str += f'<td>{html.escape(cell)}</td>'
        html_str += '</tr>\n'
    html_str += '</tbody></table>'
    return html_str


def convert_all():
    """Convert all markdown reports to HTML."""
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    web_reports_dir = os.path.join(os.path.dirname(__file__), "web", "reports")
    os.makedirs(web_reports_dir, exist_ok=True)

    for filename in os.listdir(reports_dir):
        if not filename.endswith(".md"):
            continue

        md_path = os.path.join(reports_dir, filename)
        html_filename = filename.replace(".md", ".html")
        html_path = os.path.join(web_reports_dir, html_filename)

        # Skip if HTML already exists and is newer
        # (for failed_gate_example which was hand-written)
        if filename == "failed_gate_example.md" and os.path.exists(
            os.path.join(web_reports_dir, "failed_gate_example.html")
        ):
            print(f"  Skipping {filename} (hand-written HTML exists)")
            continue

        repo_name = filename.replace("_report.md", "")
        print(f"  Converting {filename} -> {html_filename}")

        with open(md_path, "r") as f:
            md_content = f.read()

        html_content = md_to_html(md_content, repo_name)

        with open(html_path, "w") as f:
            f.write(html_content)

    print("Done converting reports to HTML.")


if __name__ == "__main__":
    convert_all()
