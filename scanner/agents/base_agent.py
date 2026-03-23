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


@dataclass
class Evidence:
    file_path: str
    line_number: int
    content: str
    match_type: str  # "search_pattern" or "absence_pattern"


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

            for pattern in patterns:
                regex = re.compile(re.escape(pattern), re.IGNORECASE)
                for i, line in enumerate(lines, 1):
                    if regex.search(line):
                        evidence.append(Evidence(
                            file_path=rel_path,
                            line_number=i,
                            content=line.strip()[:200],
                            match_type="search_pattern",
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
                evidence_text += f"  - {e.file_path}:{e.line_number} | {e.content}\n"
        else:
            evidence_text = "NO MATCHING EVIDENCE FOUND for search patterns.\n"

        if absence_evidence:
            evidence_text += "\nANTI-PATTERNS DETECTED:\n"
            for e in absence_evidence[:10]:
                evidence_text += f"  - {e.file_path}:{e.line_number} | {e.content}\n"

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

REMEDIATION: [One paragraph max. Plain English for the engineer. What would need to change.]

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
            raise RuntimeError("GEMINI_API_KEY not set. Independent review requires a Gemini API key.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def review_all(self, agent_results: list[AgentResult], repo_context: dict) -> list[AgentResult]:
        """Review all findings across all framework results."""
        for result in agent_results:
            for finding in result.findings:
                print(f"  [Gemini] Reviewing {finding.question_id}...")
                verdict = self._review_single(finding, result.framework, repo_context)
                finding.review_verdict = verdict["verdict"]
                finding.judge_reasoning = verdict["reasoning"]
                finding.judge_confidence = verdict["confidence"]
                finding.judge_model = "gemini-1.5-flash"
        return agent_results

    def _review_single(self, finding: Finding, framework: str, repo_context: dict) -> dict:
        import json as _json

        evidence_summary = ""
        if finding.evidence:
            for e in finding.evidence[:5]:
                evidence_summary += f"  - {e.file_path}:{e.line_number} | {e.content[:100]}\n"
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
Review this finding critically. Consider:
1. Is the evidence specific enough to support this finding?
2. Could this be a false positive — present but not creating regulatory risk?
3. Is the severity level appropriate, or overstated?
4. Are there deployment or infrastructure factors not visible in code?
5. Is the regulatory citation accurate and applicable?

Respond in JSON only. No preamble.

{{"verdict": "CONFIRMED" | "CONTEXT DEPENDENT" | "POSSIBLE FALSE POSITIVE" | "ADDITIONAL RISK", "reasoning": "One sentence explaining your verdict.", "confidence": "HIGH" | "MEDIUM" | "LOW"}}

VERDICT DEFINITIONS:
CONFIRMED — Evidence is specific, severity appropriate, well-supported.
CONTEXT DEPENDENT — May be valid but depends on deployment/infrastructure not visible in code.
POSSIBLE FALSE POSITIVE — Pattern exists but likely does not create regulatory risk in context.
ADDITIONAL RISK — Primary analysis understated this finding. Risk is more serious."""

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            # Strip markdown code fences
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            result = _json.loads(text.strip())
            return {
                "verdict": result.get("verdict", "CONTEXT DEPENDENT"),
                "reasoning": result.get("reasoning", "Unable to complete review."),
                "confidence": result.get("confidence", "LOW"),
            }
        except Exception as e:
            return {
                "verdict": "CONTEXT DEPENDENT",
                "reasoning": f"Independent review could not complete: {str(e)[:100]}",
                "confidence": "LOW",
            }
