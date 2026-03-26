"""
Base compliance agent that question-specific agents inherit from.

Handles loading question libraries, searching for evidence in code,
and calling the LLM for analysis.
"""

import os
import re
import yaml
from dataclasses import dataclass, field
from anthropic import Anthropic


# Evidence tier classification
TIER_1_EXTENSIONS = {
    '.ts', '.tsx', '.js', '.jsx', '.py',
    '.go', '.rs', '.java', '.php', '.rb',
    '.cs', '.cpp', '.c', '.swift', '.kt',
    '.scala', '.clj', '.ex', '.exs', '.h', '.hpp',
}

TIER_2_EXTENSIONS = {
    '.yml', '.yaml', '.json', '.toml',
    '.env', '.config', '.tf', '.hcl',
    '.xml', '.properties',
}
TIER_2_FILENAMES = {
    'Dockerfile', 'docker-compose.yml',
    'docker-compose.yaml', 'docker-compose.full-stack.yml',
}

TIER_3_EXTENSIONS = {
    '.md', '.mdc', '.txt', '.rst', '.mdx',
    '.html', '.css', '.scss',
}

# Directories that contain non-production code — demote to Tier 3
NON_PRODUCTION_DIRS = {
    'examples', 'example', 'demo', 'demos', 'sample', 'samples',
    'test', 'tests', '__tests__', 'testing', 'test_fixtures',
    'fixtures', 'fixture', 'mock', 'mocks', 'stubs',
    'e2e', 'spec', 'specs', 'sandbox', 'playground',
    'tutorial', 'tutorials', 'docs', 'documentation',
    'stories', 'storybook', '.storybook',
    'benchmark', 'benchmarks', 'perf',
}


def classify_evidence_tier(file_path: str) -> int:
    """Classify a file into evidence tiers: 1=source, 2=config, 3=docs.

    Files under example/test/demo directories are always Tier 3 regardless
    of extension — they are not production code.
    """
    # Check if file is under a non-production directory
    parts = file_path.replace("\\", "/").split("/")
    for part in parts[:-1]:  # exclude filename itself
        if part.lower() in NON_PRODUCTION_DIRS:
            return 3

    basename = os.path.basename(file_path)
    if basename in TIER_2_FILENAMES:
        return 2
    ext = os.path.splitext(file_path)[1].lower()
    if ext in TIER_1_EXTENSIONS:
        return 1
    if ext in TIER_2_EXTENSIONS:
        return 2
    if ext in TIER_3_EXTENSIONS:
        return 3
    # Default: treat unknown as tier 2 (config-like)
    return 2


def calculate_tier_severity(evidence_items: list) -> str:
    """Calculate severity based on evidence tiers. Only Tier 1 supports High Risk."""
    tier1 = [e for e in evidence_items if e.tier == 1]
    tier2 = [e for e in evidence_items if e.tier == 2]
    tier3 = [e for e in evidence_items if e.tier == 3]

    if len(tier1) >= 2:
        return "High Risk"
    elif len(tier1) == 1:
        return "Medium Risk"
    elif len(tier2) >= 2:
        return "Medium Risk"
    elif len(tier2) == 1:
        return "Pattern of Concern"
    elif tier3:
        return "Pattern of Concern"
    else:
        return "No Issue Found"


TIER_LABELS = {1: "SOURCE", 2: "CONFIG", 3: "DOCS"}


@dataclass
class Evidence:
    file_path: str
    line_number: int
    content: str
    match_type: str  # "search_pattern" or "absence_pattern"
    tier: int = 0  # 1=source code, 2=config, 3=docs


@dataclass
class Finding:
    question_id: str
    category: str
    legal_question: str
    regulatory_standard: str
    evidence: list[Evidence]
    finding_level: str  # "High Risk", "Medium Risk", "Pattern of Concern", "No Issue Found"
    finding_text: str
    remediation: str
    review_verdict: str = ""  # "CONFIRMED", "CONTEXT DEPENDENT", "POSSIBLE FALSE POSITIVE", "ADDITIONAL RISK"
    judge_reasoning: str = ""
    judge_confidence: str = ""
    judge_model: str = ""
    remediation_quality: str = ""  # "specific", "generic", "unclear"
    remediation_note: str = ""
    improved_remediation: str = ""  # Gemini-rewritten remediation if original was generic


@dataclass
class AgentResult:
    framework: str
    findings: list[Finding] = field(default_factory=list)


class BaseComplianceAgent:
    """Base class for compliance scanning agents."""

    def __init__(self, questions_path: str, framework_name: str):
        self.framework_name = framework_name
        with open(questions_path, "r") as f:
            self.config = yaml.safe_load(f)
        self.questions = self.config["questions"]
        self.client = Anthropic()

    def search_codebase(
        self,
        repo_path: str,
        file_index: list[str],
        patterns: list[str],
        max_results: int = 30,
    ) -> list[Evidence]:
        """Search repository files for pattern matches."""
        evidence: list[Evidence] = []
        skip_dirs = {
            "node_modules", ".git", "vendor", "venv", "__pycache__",
            "dist", "build", ".next", "target", "bin", "obj",
        }

        for rel_path in file_index:
            # Skip non-code files for content search
            parts = rel_path.split(os.sep)
            if any(p in skip_dirs for p in parts):
                continue

            filepath = os.path.join(repo_path, rel_path)
            try:
                if os.path.getsize(filepath) > 256 * 1024:
                    continue
                with open(filepath, "r", errors="ignore") as f:
                    lines = f.readlines()
            except (OSError, IOError):
                continue

            tier = classify_evidence_tier(rel_path)
            for pattern in patterns:
                regex = re.compile(re.escape(pattern), re.IGNORECASE)
                for i, line in enumerate(lines, 1):
                    if regex.search(line):
                        evidence.append(Evidence(
                            file_path=rel_path,
                            line_number=i,
                            content=line.strip()[:200],
                            match_type="search_pattern",
                            tier=tier,
                        ))
                        if len(evidence) >= max_results:
                            return evidence

        return evidence

    def check_absence(
        self,
        repo_path: str,
        file_index: list[str],
        patterns: list[str],
    ) -> list[Evidence]:
        """Search for anti-patterns whose presence indicates risk."""
        return self.search_codebase(repo_path, file_index, patterns, max_results=15)

    def analyze_with_llm(
        self,
        question: dict,
        evidence: list[Evidence],
        absence_evidence: list[Evidence],
        readme_content: str,
    ) -> Finding:
        """Use Claude to analyze evidence and produce a finding."""
        evidence_text = ""
        if evidence:
            evidence_text = "EVIDENCE FOUND:\n"
            for e in evidence[:20]:
                label = TIER_LABELS.get(e.tier, "UNKNOWN")
                evidence_text += f"  - [{label}] {e.file_path}:{e.line_number} | {e.content}\n"
        else:
            evidence_text = "NO MATCHING EVIDENCE FOUND for search patterns.\n"

        if absence_evidence:
            evidence_text += "\nANTI-PATTERNS DETECTED:\n"
            for e in absence_evidence[:10]:
                label = TIER_LABELS.get(e.tier, "UNKNOWN")
                evidence_text += f"  - [{label}] {e.file_path}:{e.line_number} | {e.content}\n"

        prompt = f"""You are a compliance analyst producing a legal brief finding. Analyze the following evidence from a code repository.

QUESTION ID: {question['id']}
CATEGORY: {question['category']}

LEGAL QUESTION:
{question['legal_question']}

REGULATORY STANDARD:
{question['regulatory_standard']}

{evidence_text}

README EXCERPT (first 2000 chars):
{readme_content[:2000]}

Based on the evidence, produce a finding. You must output EXACTLY this format:

FINDING_LEVEL: [One of: High Risk / Medium Risk / Pattern of Concern / No Issue Found]

FINDING_TEXT: [2-3 sentences. Never use the word "violation". Instead say "risk pattern consistent with non-compliance under [standard]". Be specific about what was or wasn't found.]

REMEDIATION: [Generate specific, actionable remediation. Requirements:
1. Reference specific files from the evidence where possible — e.g. "In src/auth/session.ts, the session handler does not enforce timeout"
2. Give a concrete code-level recommendation — not "implement X" but "add Y middleware before the route in Z file"
3. If no specific files available, reference the pattern type and typical location
4. Maximum 3 sentences
5. Do NOT start with "Implement" or "Ensure" — these are generic. Start with the specific action.
6. End with the regulatory consequence — one sentence, specific fine range or enforcement action]

Rules:
- If no evidence was found for required controls, that IS a finding (High Risk or Medium Risk)
- If evidence exists but is incomplete, that's Medium Risk or Pattern of Concern
- If anti-patterns were found, elevate the risk level
- Be specific about file paths and line numbers in your finding text
- Never say "violation" - always "risk pattern consistent with non-compliance"
"""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        return self._parse_llm_response(question, evidence, response.content[0].text)

    def _parse_llm_response(
        self,
        question: dict,
        evidence: list[Evidence],
        response_text: str,
    ) -> Finding:
        """Parse the LLM's structured response into a Finding."""
        finding_level = "Medium Risk"
        finding_text = ""
        remediation = ""

        for line in response_text.split("\n"):
            line = line.strip()
            if line.startswith("FINDING_LEVEL:"):
                level = line.replace("FINDING_LEVEL:", "").strip()
                if level in ("High Risk", "Medium Risk", "Pattern of Concern", "No Issue Found"):
                    finding_level = level
            elif line.startswith("FINDING_TEXT:"):
                finding_text = line.replace("FINDING_TEXT:", "").strip()
            elif line.startswith("REMEDIATION:"):
                remediation = line.replace("REMEDIATION:", "").strip()

        # If parsing failed, use the full response
        if not finding_text:
            finding_text = response_text[:500]

        # Cap severity based on evidence tiers — docs alone cannot produce High Risk
        tier_max = calculate_tier_severity(evidence)
        sev_order = ["No Issue Found", "Pattern of Concern", "Medium Risk", "High Risk"]
        if sev_order.index(finding_level) > sev_order.index(tier_max):
            finding_level = tier_max

        return Finding(
            question_id=question["id"],
            category=question["category"],
            legal_question=question["legal_question"].strip(),
            regulatory_standard=question["regulatory_standard"],
            evidence=evidence,
            finding_level=finding_level,
            finding_text=finding_text,
            remediation=remediation,
        )

    def scan(
        self,
        repo_path: str,
        file_index: list[str],
        readme_content: str,
    ) -> AgentResult:
        """Run all questions against the repository."""
        result = AgentResult(framework=self.framework_name)

        for question in self.questions:
            print(f"  Analyzing {question['id']}: {question['category']}...")

            evidence = self.search_codebase(
                repo_path, file_index, question.get("search_patterns", [])
            )
            absence_evidence = self.check_absence(
                repo_path, file_index, question.get("absence_patterns", [])
            )
            finding = self.analyze_with_llm(
                question, evidence, absence_evidence, readme_content
            )
            result.findings.append(finding)

        return result

    def review_findings(self, findings: list[Finding]) -> list[Finding]:
        """Legacy stub — use JudgeAgent instead."""
        return findings


class JudgeAgent:
    """
    Independent review agent using Google Gemini.
    Challenges findings from the primary Claude scan.
    Different company, different model = genuine independence.
    """

    def __init__(self, gemini_api_key: str | None = None):
        import google.generativeai as genai
        api_key = gemini_api_key or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("[WARNING] GEMINI_API_KEY not set. Independent review will be skipped.")
            print("  Set GEMINI_API_KEY environment variable to enable Gemini review.")
            self.model = None
            return
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def review_all(self, agent_results: list[AgentResult], repo_context: dict) -> list[AgentResult]:
        """Review all findings across all framework results."""
        if self.model is None:
            # Mark all findings as NOT REVIEWED
            for result in agent_results:
                for finding in result.findings:
                    finding.review_verdict = "NOT REVIEWED"
                    finding.judge_reasoning = "Gemini API key not configured"
                    finding.judge_confidence = ""
                    finding.judge_model = ""
            return agent_results
        for result in agent_results:
            for finding in result.findings:
                print(f"  [Gemini] Reviewing {finding.question_id}...")
                verdict = self._review_single(finding, result.framework, repo_context)
                finding.review_verdict = verdict["verdict"]
                finding.judge_reasoning = verdict["reasoning"]
                finding.judge_confidence = verdict["confidence"]
                finding.judge_model = "gemini-2.5-flash"
                finding.remediation_quality = verdict.get("remediation_quality", "")
                improved = verdict.get("improved_remediation", "")
                if improved:
                    finding.improved_remediation = improved
                    print(f"    -> Remediation improved by Gemini")
        return agent_results

    def _review_single(self, finding: Finding, framework: str, repo_context: dict) -> dict:
        import json as _json

        evidence_summary = ""
        if finding.evidence:
            for e in finding.evidence[:5]:
                label = TIER_LABELS.get(e.tier, "UNKNOWN")
                evidence_summary += f"  - [{label}] {e.file_path}:{e.line_number} | {e.content[:100]}\n"
        else:
            evidence_summary = "  No code evidence was found.\n"

        prompt = f"""You are an independent compliance reviewer.

A primary analysis tool (Claude by Anthropic) has identified the following
compliance risk pattern in a software repository. Your job is to challenge
this finding — look for reasons it might be overstated, a false positive,
or missing important context.

REPOSITORY CONTEXT:
- Repository: {repo_context.get('repo_name', 'unknown')}
- Domains detected: {repo_context.get('domains', 'unknown')}

FINDING FROM PRIMARY ANALYSIS:
- Framework: {framework}
- Question ID: {finding.question_id}
- Category: {finding.category}
- Legal Question: {finding.legal_question[:300]}
- Regulatory Standard: {finding.regulatory_standard}
- Severity: {finding.finding_level}
- Evidence found:
{evidence_summary}
- Primary reasoning: {finding.finding_text[:300]}

YOUR TASK:
Review this finding and assign a definitive verdict. DO NOT default to CONTEXT DEPENDENT — that is the lazy answer. Make a real call.

MANDATORY DECISION RULES — follow these strictly:

If evidence cites PRODUCTION application source code files (.py, .js, .ts, .go, .rs, .java, .php, .rb) AND the pattern is a known compliance risk:
→ verdict = CONFIRMED

If evidence cites only config files (.yaml, .json, .toml, .env), documentation (.md), or test files:
→ verdict = POSSIBLE FALSE POSITIVE

If evidence comes from example/demo/test/sample/tutorial directories (e.g. examples/, demo/, test/, __tests__/, fixtures/, sandbox/):
→ verdict = POSSIBLE FALSE POSITIVE (example code is not production code)

If evidence files are tagged [DOCS] in the evidence list, they are non-production (examples, tests, docs):
→ verdict = POSSIBLE FALSE POSITIVE

If the finding is about infrastructure (network, firewall, cloud config) that cannot be determined from source code:
→ verdict = CONTEXT DEPENDENT

If the primary analysis understated a real risk visible in the evidence:
→ verdict = ADDITIONAL RISK

IMPORTANT: You MUST choose CONFIRMED or POSSIBLE FALSE POSITIVE for at least 70% of findings. CONTEXT DEPENDENT should be rare — only for genuinely infrastructure-dependent findings. If in doubt between CONFIRMED and CONTEXT DEPENDENT, choose CONFIRMED.

Also review and improve the remediation if needed.

Current remediation: {finding.remediation[:300]}
Evidence files: {evidence_summary[:200]}

If the remediation is generic (starts with 'Implement', 'Ensure', 'Consider', or does not reference specific files from evidence), rewrite it to be specific:
- Reference specific file(s) from evidence
- State the exact change needed
- End with the regulatory consequence
- 2-3 sentences max
- Do NOT start with 'Implement' or 'Ensure'

Respond in JSON only. No preamble.

{{"verdict": "CONFIRMED" | "CONTEXT DEPENDENT" | "POSSIBLE FALSE POSITIVE" | "ADDITIONAL RISK", "reasoning": "One sentence explaining your verdict.", "confidence": "HIGH" | "MEDIUM" | "LOW", "remediation_quality": "specific" | "generic", "improved_remediation": "rewritten remediation if generic, or null if already specific"}}

VERDICT DEFINITIONS:
CONFIRMED — Evidence is specific, severity appropriate, well-supported.
CONTEXT DEPENDENT — Genuinely ambiguous, depends on deployment/infrastructure.
POSSIBLE FALSE POSITIVE — Pattern exists but likely does not create regulatory risk in context.
ADDITIONAL RISK — Primary analysis understated this finding."""

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            # Strip markdown code fences
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            result = _json.loads(text.strip())
            improved = result.get("improved_remediation")
            if improved and improved != "null":
                improved = str(improved)
            else:
                improved = ""
            return {
                "verdict": result.get("verdict", "CONTEXT DEPENDENT"),
                "reasoning": result.get("reasoning", "Unable to complete review."),
                "confidence": result.get("confidence", "LOW"),
                "remediation_quality": result.get("remediation_quality", ""),
                "improved_remediation": improved,
            }
        except Exception as e:
            return {
                "verdict": "CONTEXT DEPENDENT",
                "reasoning": f"Independent review could not complete: {str(e)[:100]}",
                "confidence": "LOW",
            }
