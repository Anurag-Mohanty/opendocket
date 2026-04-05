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
CONFIDENCE_THRESHOLD = 10.0

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


def _has_signals(domains: list[DomainResult], signal_set: set) -> bool:
    """Check if any detected domain contains signals from the given set."""
    for domain in domains:
        for signal in domain.signals_found:
            if signal.lower() in signal_set:
                return True
    return False


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

    if _has_signals(domains, CHILDREN_SIGNALS):
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
