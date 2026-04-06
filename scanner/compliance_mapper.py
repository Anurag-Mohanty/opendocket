"""
Maps detected domains to relevant compliance frameworks.

Uses domain detection results and signal analysis to determine
which compliance frameworks should be scanned.
"""

from scanner.domain_detector import DomainResult

# Domain -> list of applicable frameworks
DOMAIN_FRAMEWORK_MAP: dict[str, list[str]] = {
    "healthcare": ["hipaa", "soc2", "hitrust"],
    "fintech": ["pci_dss", "sox", "soc2", "glba"],
    "saas": ["soc2", "nist_csf", "iso27001"],
    "ecommerce": ["soc2", "pci_dss"],
    "communication": ["tcpa", "soc2"],
    "gdpr": ["gdpr"],
    "sox": ["sox"],
    "ccpa": ["ccpa"],
    "coppa": ["coppa"],
    "ferpa": ["ferpa"],
    "glba": ["glba"],
    "nist_csf": ["nist_csf"],
    "iso27001": ["iso27001"],
    "dora": ["dora"],
    "psd2": ["psd2"],
    "bipa": ["bipa"],
    "eu_ai_act": ["eu_ai_act"],
    "hitrust": ["hitrust"],
}

# Minimum confidence to trigger a framework scan
# Higher threshold reduces false triggers from repos that merely reference
# compliance frameworks (e.g. a compliance platform listing "HIPAA" in its UI)
CONFIDENCE_THRESHOLD = 30.0

# Signals that indicate EU presence (triggers GDPR)
EU_SIGNALS = {
    "gdpr", "eu_resident", "data_subject", "dpo", "supervisory_authority",
    "erasure", "portability", "lawful_basis", "personal_data",
    "data_protection", "right_to_be_forgotten", "data_controller",
    "data_processor", "privacy_by_design", "cookie_consent", "cookie_banner",
    "eu-west", "eu-central", "frankfurt", "ireland", "eu_region",
    "standard_contractual_clauses", "scc",
}

# Signals that indicate SMS/telephony (triggers TCPA)
SMS_SIGNALS = {
    "sms", "twilio", "phone_number", "opt_in", "opt_out",
    "prior_express_consent", "do_not_call", "message_frequency",
    "short_code", "10dlc", "tcpa",
}

# Signals that indicate children's data (triggers COPPA)
CHILDREN_SIGNALS = {
    "coppa", "children", "child", "minor", "under_13", "age_gate",
    "parental_consent", "kids", "youth", "parent_consent", "age_verification",
    "guardian",
}

# Signals that indicate education (triggers FERPA)
EDUCATION_SIGNALS = {
    "ferpa", "student", "enrollment", "transcript", "education_record",
    "lms", "learning_management", "gradebook", "roster", "academic_record",
}

# Signals that indicate financial institutions (triggers GLBA)
FINANCIAL_SIGNALS = {
    "glba", "gramm_leach", "safeguards_rule", "nonpublic_personal", "npi",
    "financial_institution", "credit_union", "mortgage", "broker_dealer",
    "investment_advisor", "financial_privacy",
}

# Biometric signals (triggers BIPA)
BIOMETRIC_SIGNALS = {
    "biometric", "fingerprint", "facial_recognition", "face_detect",
    "iris_scan", "voiceprint", "retina", "face_id", "touch_id",
    "face_encoding", "biometric_template",
}

# AI/ML signals (triggers EU AI Act)
AI_SIGNALS = {
    "machine_learning", "neural_network", "deep_learning", "model_training",
    "ai_system", "tensorflow", "pytorch", "sklearn", "scikit_learn",
    "huggingface", "transformer", "llm", "inference", "training_data",
    "prediction_model", "classification_model",
}

# EU fintech signals (triggers DORA + PSD2)
EU_FINTECH_SIGNALS = {
    "dora", "psd2", "sca", "3ds", "3d_secure", "strong_customer_authentication",
    "digital_resilience", "ict_risk", "esma", "eba",
}


def _has_signals(domains: list[DomainResult], signal_set: set, min_count: int = 3) -> bool:
    """Check if detected domains contain enough signals from the given set.

    Requires min_count distinct signal matches to reduce false triggers from
    repos that merely reference compliance terms (e.g. a compliance platform
    listing framework names in its UI without actually processing that data).
    """
    matched = set()
    for domain in domains:
        for signal in domain.signals_found:
            if signal.lower() in signal_set:
                matched.add(signal.lower())
    return len(matched) >= min_count


def map_frameworks(domains: list[DomainResult]) -> list[str]:
    """Given detected domains, return deduplicated list of frameworks to scan.

    Applies cross-cutting rules for broad-applicability frameworks.
    """
    frameworks: set[str] = set()

    for domain in domains:
        if domain.confidence >= CONFIDENCE_THRESHOLD:
            for fw in DOMAIN_FRAMEWORK_MAP.get(domain.domain, []):
                frameworks.add(fw)

    detected_domains = {d.domain for d in domains if d.confidence >= CONFIDENCE_THRESHOLD}

    # Cross-cutting rules — existing
    if _has_signals(domains, EU_SIGNALS):
        frameworks.add("gdpr")

    if _has_signals(domains, SMS_SIGNALS):
        frameworks.add("tcpa")

    if _has_signals(domains, CHILDREN_SIGNALS, min_count=5):
        frameworks.add("coppa")

    if _has_signals(domains, EDUCATION_SIGNALS):
        frameworks.add("ferpa")

    if _has_signals(domains, FINANCIAL_SIGNALS):
        frameworks.add("glba")

    # CCPA applies broadly to SaaS, ecommerce, fintech with US users
    if detected_domains & {"saas", "ecommerce", "fintech", "ccpa"}:
        frameworks.add("ccpa")

    # Cross-cutting rules — new frameworks
    # NIST CSF + ISO 27001 apply to any substantial software with security controls
    if detected_domains & {"saas", "fintech", "healthcare", "ecommerce"}:
        frameworks.add("nist_csf")
        frameworks.add("iso27001")

    # DORA + PSD2 for EU fintech
    if detected_domains & {"fintech", "ecommerce"} and _has_signals(domains, EU_FINTECH_SIGNALS):
        frameworks.add("dora")
        frameworks.add("psd2")
    # PSD2 also for any payment processing
    if detected_domains & {"fintech"} and _has_signals(domains, {"psd2", "sca", "3ds", "3d_secure"}):
        frameworks.add("psd2")

    # HITRUST for healthcare
    if "healthcare" in detected_domains:
        frameworks.add("hitrust")

    # BIPA for biometric data
    if _has_signals(domains, BIOMETRIC_SIGNALS):
        frameworks.add("bipa")

    # EU AI Act for ML/AI systems
    if _has_signals(domains, AI_SIGNALS):
        frameworks.add("eu_ai_act")

    return sorted(frameworks)


# Framework descriptions for the relevance gate prompt
FRAMEWORK_DESCRIPTIONS = {
    "hipaa": "HIPAA — applies when the system stores/processes/transmits Protected Health Information (PHI) like patient records, diagnoses, prescriptions",
    "soc2": "SOC2 — applies to any SaaS or cloud service that stores customer data and needs to demonstrate security controls",
    "pci_dss": "PCI-DSS — applies when the system stores, processes, or transmits credit card/payment card data",
    "gdpr": "GDPR — applies when the system processes personal data of EU residents (names, emails, behavioral data, etc.)",
    "tcpa": "TCPA — applies when the system sends SMS messages, makes automated phone calls, or manages telemarketing communications",
    "sox": "SOX — applies when the system processes financial reporting data, general ledger entries, or internal controls over financial statements",
    "ccpa": "CCPA/CPRA — applies when the system collects personal information from California residents (broadly applicable to consumer-facing SaaS)",
    "coppa": "COPPA — applies when the system knowingly collects data from children under 13 (age-gated apps, educational platforms for kids)",
    "ferpa": "FERPA — applies when the system processes student education records (grades, transcripts, enrollment) for educational institutions",
    "glba": "GLBA — applies when the system is operated by a financial institution (bank, credit union, broker) handling customer financial data",
    "nist_csf": "NIST CSF — applies to systems that need a cybersecurity governance framework (common for SaaS, fintech, healthcare)",
    "iso27001": "ISO 27001 — applies to systems implementing an information security management system (common for enterprise SaaS)",
    "dora": "DORA — applies to EU financial entities and their ICT service providers for digital operational resilience",
    "psd2": "PSD2 — applies to payment service providers in the EU that handle Strong Customer Authentication (3DS, SCA)",
    "bipa": "BIPA — applies when the system collects or stores biometric identifiers (fingerprints, facial recognition, iris scans)",
    "eu_ai_act": "EU AI Act — applies when the system IS an AI/ML system making predictions or classifications that affect people",
    "hitrust": "HITRUST — applies to healthcare systems that need a comprehensive security certification framework",
}


def filter_frameworks_by_relevance(
    frameworks: list[str],
    repo_name: str,
    readme_content: str,
    file_index: list[str],
    domains: list[DomainResult],
    log_fn=None,
) -> list[str]:
    """Use Claude to evaluate whether each triggered framework genuinely applies.

    Sends a single prompt with all candidate frameworks and the repo context.
    Claude returns only the frameworks that are genuinely relevant — filtering
    out frameworks that triggered due to the repo merely referencing compliance
    terms (e.g. a compliance platform listing "HIPAA" in its UI).

    Returns the filtered list of framework keys.
    """
    import os

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key or len(frameworks) <= 2:
        # Skip gate if no API key or very few frameworks (not worth the call)
        return frameworks

    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
    except Exception:
        return frameworks

    # Build context
    readme_excerpt = (readme_content or "")[:1500]
    sample_files = "\n".join(file_index[:80])
    domain_summary = ", ".join(
        f"{d.domain} ({d.confidence}%)" for d in domains[:8]
    )
    framework_list = "\n".join(
        f"- {fw}: {FRAMEWORK_DESCRIPTIONS.get(fw, fw)}"
        for fw in frameworks
    )

    prompt = f"""You are evaluating which compliance frameworks genuinely apply to a software repository.

REPOSITORY: {repo_name}

README (excerpt):
{readme_excerpt}

DETECTED DOMAINS: {domain_summary}

SAMPLE FILES:
{sample_files}

CANDIDATE FRAMEWORKS:
{framework_list}

TASK: For each candidate framework, decide if it GENUINELY applies to this codebase.

Key distinction: A compliance management platform that HELPS OTHERS manage HIPAA compliance is NOT itself subject to HIPAA — unless it also stores/processes actual PHI. Similarly, a platform that lists "COPPA" as a supported framework doesn't need COPPA compliance unless it collects children's data.

Ask yourself for each framework:
- Does this codebase actually handle the regulated data type? (PHI, payment cards, children's data, etc.)
- Or does it merely reference the framework name in UI/docs/config?

Return ONLY the framework keys that genuinely apply, one per line. No explanations, no bullets, just the framework keys like:
soc2
gdpr
ccpa"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=256,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )
        response_text = response.content[0].text.strip()

        # Parse response — each line should be a framework key
        approved = []
        for line in response_text.splitlines():
            fw = line.strip().lower().replace("-", "_")
            if fw in frameworks:
                approved.append(fw)

        if log_fn:
            removed = [fw for fw in frameworks if fw not in approved]
            log_fn(f"[RELEVANCE GATE] Claude approved {len(approved)}/{len(frameworks)} frameworks")
            if removed:
                log_fn(f"[RELEVANCE GATE] Filtered out: {', '.join(fw.upper() for fw in removed)} (not relevant to this codebase)")

        # Safety: always keep at least soc2 if nothing was approved
        if not approved:
            approved = ["soc2"]

        return sorted(approved)

    except Exception as e:
        if log_fn:
            log_fn(f"[RELEVANCE GATE] Skipped — {e}")
        return frameworks
