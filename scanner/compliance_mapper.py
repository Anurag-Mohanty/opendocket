"""
Maps detected domains to relevant compliance frameworks.

Uses domain detection results and signal analysis to determine
which compliance frameworks should be scanned.
"""

from scanner.domain_detector import DomainResult

# Domain -> list of applicable frameworks
DOMAIN_FRAMEWORK_MAP: dict[str, list[str]] = {
    "healthcare": ["hipaa", "soc2"],
    "fintech": ["pci_dss", "sox", "soc2", "glba"],
    "saas": ["soc2"],
    "ecommerce": ["soc2", "pci_dss"],
    "communication": ["tcpa", "soc2"],
    "gdpr": ["gdpr"],
    "sox": ["sox"],
    "ccpa": ["ccpa"],
    "coppa": ["coppa"],
    "ferpa": ["ferpa"],
    "glba": ["glba"],
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


def _has_signals(domains: list[DomainResult], signal_set: set) -> bool:
    """Check if any detected domain contains signals from the given set."""
    for domain in domains:
        for signal in domain.signals_found:
            if signal.lower() in signal_set:
                return True
    return False


def map_frameworks(domains: list[DomainResult]) -> list[str]:
    """Given detected domains, return deduplicated list of frameworks to scan.

    Applies cross-cutting rules:
    - Any domain with EU signals -> add GDPR
    - Any domain with SMS signals -> add TCPA
    - Any SaaS/ecommerce/fintech -> add CCPA (broad US applicability)
    - Children signals -> add COPPA
    - Education signals -> add FERPA
    - Financial institution signals -> add GLBA
    """
    frameworks: set[str] = set()

    for domain in domains:
        if domain.confidence >= CONFIDENCE_THRESHOLD:
            for fw in DOMAIN_FRAMEWORK_MAP.get(domain.domain, []):
                frameworks.add(fw)

    # Cross-cutting rules
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
    detected_domains = {d.domain for d in domains if d.confidence >= CONFIDENCE_THRESHOLD}
    if detected_domains & {"saas", "ecommerce", "fintech", "ccpa"}:
        frameworks.add("ccpa")

    return sorted(frameworks)
