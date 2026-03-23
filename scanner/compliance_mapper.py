"""
Maps detected domains to relevant compliance frameworks.

Uses domain detection results and signal analysis to determine
which compliance frameworks should be scanned.
"""

from scanner.domain_detector import DomainResult

# Domain -> list of applicable frameworks
DOMAIN_FRAMEWORK_MAP: dict[str, list[str]] = {
    "healthcare": ["hipaa", "soc2"],
    "fintech": ["pci_dss", "sox", "soc2"],
    "saas": ["soc2"],
    "ecommerce": ["soc2", "pci_dss"],
    "communication": ["tcpa", "soc2"],
    "gdpr": ["gdpr"],
    "sox": ["sox"],
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


def _has_eu_signals(domains: list[DomainResult]) -> bool:
    """Check if any detected domain contains EU-related signals."""
    for domain in domains:
        for signal in domain.signals_found:
            if signal.lower() in EU_SIGNALS:
                return True
    return False


def _has_sms_signals(domains: list[DomainResult]) -> bool:
    """Check if any detected domain contains SMS-related signals."""
    for domain in domains:
        for signal in domain.signals_found:
            if signal.lower() in SMS_SIGNALS:
                return True
    return False


def map_frameworks(domains: list[DomainResult]) -> list[str]:
    """Given detected domains, return deduplicated list of frameworks to scan.

    Applies cross-cutting rules:
    - Any domain with EU signals -> add GDPR
    - Any domain with SMS signals -> add TCPA
    - Healthcare -> HIPAA + GDPR if EU signals
    - Fintech -> PCI-DSS + SOX + GDPR if EU signals
    - SaaS -> SOC2 + GDPR if EU signals
    - Communication -> TCPA
    """
    frameworks: set[str] = set()

    for domain in domains:
        if domain.confidence >= CONFIDENCE_THRESHOLD:
            for fw in DOMAIN_FRAMEWORK_MAP.get(domain.domain, []):
                frameworks.add(fw)

    # Cross-cutting: EU signals trigger GDPR
    if _has_eu_signals(domains):
        frameworks.add("gdpr")

    # Cross-cutting: SMS signals trigger TCPA
    if _has_sms_signals(domains):
        frameworks.add("tcpa")

    return sorted(frameworks)
