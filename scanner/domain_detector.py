"""
Domain detection for code repositories.

Scans file contents, names, dependencies, and README for signals
that indicate which regulatory domains apply.
"""

import os
import re
from dataclasses import dataclass, field


DOMAIN_SIGNALS: dict[str, list[str]] = {
    "healthcare": [
        "patient", "phi", "ehr", "emr", "fhir", "hl7", "diagnosis",
        "prescription", "rx", "medication", "clinical", "hipaa",
        "provider", "covered_entity", "medical", "health_record",
        "lab_result", "vital_sign", "icd", "cpt", "npi",
        "protected_health_information", "dicom", "radiology",
        "pathology", "allergy", "immunization", "encounter",
    ],
    "fintech": [
        "payment", "transaction", "account_number",
        "pci", "ledger", "wallet", "fraud", "kyc", "aml",
        "plaid", "fintech", "settlement", "clearing",
        "ach", "wire_transfer", "swift", "iban", "merchant",
        "chargeback", "refund", "payout", "credit_card",
        "cardholder", "card_number",
    ],
    "saas": [
        "subscription", "tenant", "saas", "user_data", "billing",
        "stripe", "auth", "rbac", "soc2", "multi_tenant",
        "plan", "pricing", "trial", "onboarding", "workspace",
        "organization", "team", "invite",
    ],
    "ecommerce": [
        "cart", "checkout", "shipping", "inventory",
        "catalog", "sku", "warehouse", "fulfillment",
        "storefront", "marketplace", "add_to_cart",
        "shopping_cart",
    ],
    "communication": [
        "sms", "twilio", "messaging", "phone_number", "tcpa",
        "opt_in", "opt_out", "unsubscribe",
        "voip", "push_notification",
        "prior_express_consent", "do_not_call", "message_frequency",
        "robocall", "autodialer", "short_code",
    ],
    "gdpr": [
        "gdpr", "data_subject", "lawful_basis",
        "dpo", "supervisory_authority", "erasure", "portability",
        "eu_resident", "data_protection",
        "right_to_be_forgotten", "data_controller", "data_processor",
        "privacy_by_design", "cookie_consent", "cookie_banner",
    ],
    "sox": [
        "sox", "financial_statement", "internal_control",
        "segregation_of_duties", "audit_trail", "material_weakness",
        "general_ledger", "sarbanes", "pcaob", "section_302",
        "section_404", "financial_reporting",
    ],
    "ccpa": [
        "california", "ccpa", "cpra", "cppa",
        "do_not_sell", "consumer_rights",
        "privacy_request", "gpc", "sec_gpc",
        "opt_out_sale", "dnsmpi",
    ],
    "coppa": [
        "coppa", "under_13", "age_gate", "parental_consent",
        "kids", "youth",
        "parent_consent", "age_verification",
        "child_privacy", "childrens_privacy",
    ],
    "ferpa": [
        "ferpa", "student", "enrollment",
        "grade", "transcript", "education_record",
        "school", "university", "college",
        "lms", "learning_management",
        "course", "gradebook", "roster",
        "academic_record", "institution",
    ],
    "glba": [
        "glba", "gramm_leach", "safeguards_rule",
        "nonpublic_personal", "npi", "financial_institution",
        "bank", "credit_union", "mortgage",
        "financial_advisor", "broker_dealer",
        "insurance", "investment_advisor",
        "financial_privacy", "customer_financial",
    ],
    "nist_csf": [
        "nist", "csf", "cybersecurity_framework",
        "asset_inventory", "risk_assessment", "incident_response",
        "recovery_plan", "governance_framework",
        "continuous_monitoring", "supply_chain_risk",
        "threat_model", "vulnerability_management",
    ],
    "iso27001": [
        "iso_27001", "iso27001", "isms",
        "annex_a", "information_security",
        "security_management", "iso_27002",
        "certification", "security_policy",
        "security_control",
    ],
    "dora": [
        "dora", "digital_resilience",
        "ict_risk", "operational_resilience",
        "resilience_testing", "threat_led",
        "tlpt", "ict_incident",
    ],
    "psd2": [
        "psd2", "sca", "strong_customer_authentication",
        "3ds", "3d_secure", "threeds",
        "payment_service_provider", "dynamic_linking",
        "transaction_risk_analysis",
    ],
    "bipa": [
        "biometric", "facial_recognition", "fingerprint",
        "iris_scan", "voiceprint", "retina_scan",
        "face_detect", "face_id", "touch_id",
        "face_encoding", "biometric_template",
    ],
    "eu_ai_act": [
        "machine_learning", "neural_network", "deep_learning",
        "model_training", "ai_system", "prediction_model",
        "classification_model", "tensorflow", "pytorch",
        "sklearn", "scikit_learn", "huggingface",
        "transformer", "llm", "inference",
        "training_data", "model_card",
    ],
    "hitrust": [
        "hitrust", "csf_healthcare",
        "hitrust_certification", "hitrust_assessment",
    ],
}

# File extensions to scan for signals
CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rb",
    ".php", ".cs", ".rs", ".swift", ".kt", ".scala", ".c", ".cpp",
    ".h", ".hpp", ".yaml", ".yml", ".json", ".xml", ".toml",
    ".md", ".txt", ".cfg", ".conf", ".ini", ".env.example",
}

# Files to skip
SKIP_DIRS = {
    "node_modules", ".git", "vendor", "venv", ".venv", "__pycache__",
    "dist", "build", ".next", ".nuxt", "target", "bin", "obj",
    ".tox", ".mypy_cache", ".pytest_cache", "coverage",
}

MAX_FILE_SIZE = 512 * 1024  # 512KB


@dataclass
class DomainResult:
    domain: str
    confidence: float
    signal_count: int
    signals_found: list[str] = field(default_factory=list)


def detect_domains(repo_path: str) -> list[DomainResult]:
    """Detect regulatory domains from repository contents.

    Returns a list of DomainResult sorted by confidence descending.
    """
    signal_hits: dict[str, dict[str, int]] = {
        domain: {} for domain in DOMAIN_SIGNALS
    }
    total_files_scanned = 0

    for root, dirs, files in os.walk(repo_path):
        # Skip non-code directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in CODE_EXTENSIONS and filename.lower() not in (
                "readme", "readme.md", "readme.rst", "readme.txt",
                "package.json", "requirements.txt", "gemfile",
                "go.mod", "cargo.toml", "pom.xml", "build.gradle",
            ):
                continue

            filepath = os.path.join(root, filename)
            try:
                if os.path.getsize(filepath) > MAX_FILE_SIZE:
                    continue
                with open(filepath, "r", errors="ignore") as f:
                    content = f.read().lower()
            except (OSError, IOError):
                continue

            total_files_scanned += 1

            # Also check the filename itself
            content_to_scan = content + " " + filename.lower()

            for domain, signals in DOMAIN_SIGNALS.items():
                for signal in signals:
                    pattern = re.compile(
                        r'(?:^|[^a-z])' + re.escape(signal) + r'(?:[^a-z]|$)',
                        re.IGNORECASE
                    )
                    matches = pattern.findall(content_to_scan)
                    if matches:
                        signal_hits[domain][signal] = (
                            signal_hits[domain].get(signal, 0) + len(matches)
                        )

    results = []
    for domain, hits in signal_hits.items():
        if not hits:
            continue

        total_signals = len(DOMAIN_SIGNALS[domain])
        unique_signals_found = len(hits)
        total_hit_count = sum(hits.values())

        # Confidence based on: signal diversity and hit density
        diversity_score = unique_signals_found / total_signals
        density_score = min(1.0, total_hit_count / max(1, total_files_scanned * 2))

        confidence = round(
            (diversity_score * 0.7 + density_score * 0.3) * 100, 1
        )
        confidence = min(confidence, 99.0)

        if confidence >= 5.0:
            results.append(DomainResult(
                domain=domain,
                confidence=confidence,
                signal_count=total_hit_count,
                signals_found=sorted(hits.keys(), key=lambda s: hits[s], reverse=True),
            ))

    results.sort(key=lambda r: r.confidence, reverse=True)
    return results
