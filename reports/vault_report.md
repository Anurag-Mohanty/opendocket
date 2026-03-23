# OpenDocket Compliance Report: vault

> **Repository:** https://github.com/hashicorp/vault
> **Scan Date:** 2026-03-22
> **Scanner Version:** OpenDocket V1

---

**DISCLAIMER:** OpenDocket identifies risk patterns through automated code analysis. Findings represent potential areas of concern, not legal determinations. This report does not constitute legal advice. Regulatory compliance requires qualified legal and technical assessment. Consult a licensed attorney and certified compliance professional for definitive compliance determination.

---

## Domain Detection

- **Saas** — Confidence: 75.0% (11503 signals, top: auth, billing, organization, team, subscription)
- **Ecommerce** — Confidence: 44.2% (1572 signals, top: order, catalog, checkout, product, warehouse)
- **Communication** — Confidence: 32.3% (808 signals, top: call, notification, consent, phone_number, messaging)
- **Fintech** — Confidence: 24.9% (1186 signals, top: routing, card, transaction, swift, clearing)
- **Healthcare** — Confidence: 14.8% (1070 signals, top: provider, rx, encounter, phi, icd)
- **Gdpr** — Confidence: 12.5% (57 signals, top: consent, data_protection, gdpr)

## Frameworks Analyzed: GDPR, HIPAA, PCI-DSS, SOC2, SOX, TCPA

## Executive Summary

| Finding Level | Count |
|---|---|
| High Risk | 45 |
| Medium Risk | 5 |
| Pattern of Concern | 5 |
| No Issue Found | 1 |

## GDPR Findings

### GDPR-001: Lawful Basis for Processing Personal Data

**LEGAL QUESTION**

Does this system process personal data of EU residents, and if so, is there evidence that a lawful basis for processing under Article 6 GDPR has been identified and implemented for each processing activity?

**REGULATORY STANDARD**

GDPR Article 6 (Lawfulness of Processing)

**EVIDENCE**

- `builtin/logical/ssh/backend_test.go:92` — `E70jhgKjXKePTuEijkJfRc36thxHryWpii6zAQIDAQABAoIBAA/DrPD8iF2KigiL`
- `builtin/logical/ssh/backend_test.go:94` — `CjYO9q0Z5939vc349nVI+SWoyviF4msPiik1bhWulja8lPjFu/8zg+ZNy15Dx7ei`
- `go.sum:558` — `github.com/golang/groupcache v0.0.0-20241129210726-2c02b8208cf8/go.mod h1:wcDNUvekVysuuOpQKo3191zZyTpiI6se1N1ULghS0sw=`
- `go.sum:719` — `github.com/hashicorp/go-metrics v0.5.4 h1:8mmPiIJkTPPEbAiV97IxdAGNdRdaWwVap1BU6elejKY=`
- `sdk/go.sum:129` — `github.com/golang/groupcache v0.0.0-20241129210726-2c02b8208cf8/go.mod h1:wcDNUvekVysuuOpQKo3191zZyTpiI6se1N1ULghS0sw=`
- `sdk/go.sum:195` — `github.com/hashicorp/go-metrics v0.5.4 h1:8mmPiIJkTPPEbAiV97IxdAGNdRdaWwVap1BU6elejKY=`
- `tools/pipeline/go.sum:306` — `gopkg.in/DataDog/dd-trace-go.v1 v1.66.0 h1:025+lLubGtpiDWrRmSOxoFBPIiVRVYRcqP9oLabVOeg=`
- `ui/MODULE_REPORT.md:62` — `**Location**: `app/components/oidc-consent-block.js` at line 47`
- `ui/app/components/oidc-consent-block.hbs:7` — `<h3 class="title is-3" data-test-consent-title>`
- `ui/app/components/oidc-consent-block.hbs:8` — `Consent Not Given`

**FINDING: 🔴 High Risk**

Risk pattern consistent with non-compliance under GDPR Article 6. The system processes personal data of EU residents through OIDC authentication flows (evidenced in ui/app/components/oidc-consent-block.hbs at lines 19 and ui/app/components/oidc-consent-block.js), including profile, email, address, and phone data. However, no evidence was found in the codebase documenting the lawful basis for processing under Article 6 GDPR for these data processing activities.

**REMEDIATION DIRECTION**

Implement and document a lawful basis analysis for all personal data processing activities under GDPR Article 6. This should include: (1) identifying which of the six lawful bases applies to each type of data processing (likely legitimate interests or consent for OIDC flows), (2) documenting this analysis in privacy documentation, (3) implementing technical controls to ensure processing aligns with the identified lawful basis, and (4) adding privacy notices that clearly communicate the lawful basis to data subjects during the consent/authentication process.

---

### GDPR-002: Consent Collection and Management

**LEGAL QUESTION**

Does the system implement consent collection mechanisms that satisfy the conditions for consent under Article 7, including freely given, specific, informed, and unambiguous indication of the data subject's wishes, with capability to withdraw consent?

**REGULATORY STANDARD**

GDPR Article 7 (Conditions for Consent)

**EVIDENCE**

- `.github/ISSUE_TEMPLATE/feature_request.md:20` — `If there are any use-cases that would help us understand the use/need/value please share them as they can help us decide`
- `.github/instructions/generic/ember_general.instructions.md:24` — `- `ui/tests/` - Integration, unit, and acceptance tests`
- `.github/instructions/generic/ember_tests.instructions.md:13` — `- **Testing Framework**: QUnit for unit, integration, and acceptance tests`
- `.github/instructions/generic/ember_tests.instructions.md:20` — `- `ui/tests/acceptance/` - End-to-end user workflow tests`
- `.github/instructions/generic/golang.instructions.md:102` — `- Accept interfaces, return concrete types`
- `.github/scripts/gh-comment.sh:17` — `-H "Accept: application/vnd.github+json" \`
- `.github/scripts/gh-comment.sh:27` — `-H "Accept: application/vnd.github+json" \`
- `.github/scripts/gh-comment.sh:35` — `-H "Accept: application/vnd.github+json" \`
- `.github/scripts/install-cob.sh:319` — `json=$(http_copy "$giturl" "Accept:application/json")`
- `.github/workflows/test-acc-dockeronly-nightly.yml:1` — `name: test-go-acceptance-nightly`

**FINDING: 🔴 High Risk**

No evidence of GDPR Article 7 compliant consent collection mechanisms was found in the analyzed code repository. The evidence shows only software license agreement acceptance in `.release/linux/postinst:59` and generic API accept headers, but lacks any implementation of user consent collection for data processing, consent withdrawal capabilities, or consent management interfaces that would satisfy GDPR requirements for freely given, specific, informed, and unambiguous consent.

**REMEDIATION DIRECTION**

Implement a comprehensive consent management system that includes: user-facing consent collection interfaces with clear, specific language about data processing purposes; granular consent options allowing users to consent to specific processing activities; mechanisms for users to withdraw consent easily; audit logging of consent decisions and changes; and integration points throughout the application to check consent status before processing personal data. Ensure consent requests are presented separately from other terms and use plain language that clearly explains what data will be processed and why.

---

### GDPR-003: Right to Erasure Implementation

**LEGAL QUESTION**

Does the system implement the right to erasure (right to be forgotten) under Article 17, allowing data subjects to request deletion of their personal data without undue delay?

**REGULATORY STANDARD**

GDPR Article 17 (Right to Erasure)

**EVIDENCE**

- `.github/actions/create-dynamic-config/action.yml:31` — `# If/when Github decides to purge our tiny config file cache we'll also`
- `.github/workflows/test-enos-scenario-ui.yml:154` — `- name: Ensure scenario has been destroyed`
- `.github/workflows/test-enos-scenario-ui.yml:156` — `run: enos scenario destroy --timeout 60m0s --chdir ./enos ui edition:${{ needs.get-metadata.outputs.vault_edition }} bac`
- `.github/workflows/test-run-enos-scenario-containers.yml:128` — `- name: Destroy Enos scenario`
- `.github/workflows/test-run-enos-scenario-containers.yml:137` — `enos scenario destroy --timeout 10m0s --grpc-listen http://localhost --chdir ./enos/k8s ${{ matrix.scenario.id.filter }}`
- `.github/workflows/test-run-enos-scenario-matrix.yml:272` — `id: destroy`
- `.github/workflows/test-run-enos-scenario-matrix.yml:273` — `name: enos scenario destroy ${{ matrix.scenario.id.filter }}`
- `.github/workflows/test-run-enos-scenario-matrix.yml:275` — `run: enos scenario destroy --timeout 10m0s --chdir ./enos ${{ matrix.scenario.id.filter }}`
- `.github/workflows/test-run-enos-scenario-matrix.yml:276` — `- if: steps.destroy.outcome == 'failure'`
- `.github/workflows/test-run-enos-scenario-matrix.yml:277` — `id: destroy_retry`

**FINDING: 🔴 High Risk**

No evidence found of GDPR Article 17 Right to Erasure implementation in the codebase. The evidence shows only infrastructure destruction commands in GitHub workflow files (.github/workflows/*.yml) related to test scenario cleanup, which are not user-facing data deletion mechanisms. No API endpoints, user interfaces, or data deletion procedures were identified that would allow data subjects to request deletion of their personal data.

**REMEDIATION DIRECTION**

Implement a comprehensive right to erasure system including: (1) user-facing API endpoints or UI functionality for data subjects to submit deletion requests, (2) backend processes to identify and delete personal data across all storage systems within legally required timeframes, (3) verification mechanisms to confirm complete data removal, and (4) appropriate logging and audit trails for deletion requests and actions taken.

---

### GDPR-004: Data Portability Capability

**LEGAL QUESTION**

Does the system provide data subjects the right to receive their personal data in a structured, commonly used, and machine-readable format, and to transmit that data to another controller, as required under Article 20?

**REGULATORY STANDARD**

GDPR Article 20 (Right to Data Portability)

**EVIDENCE**

- `.build/entrypoint.sh:25` — `export CC=x86_64-linux-gnu-gcc`
- `.build/entrypoint.sh:28` — `export CC=aarch64-linux-gnu-gcc`
- `.build/entrypoint.sh:31` — `export CC=s390x-linux-gnu-gcc`
- `.build/system.sh:7` — `export DEBIAN_FRONTEND=noninteractive`
- `.github/actions/build-vault/action.yml:75` — `enableCrossOsArchive: true`
- `.github/actions/metadata/action.yml:5` — `name: Gather and export useful workflow metadata information.`
- `.github/actions/metadata/action.yml:7` — `Gather and export metadata about the repository, Github, and any other variable information we`
- `.github/actions/run-apupgrade-tests/action.yml:120` — `export VAULT_LICENSE_PATH="${GITHUB_WORKSPACE}/license.hclic"`
- `.github/actions/set-up-go/action.yml:68` — `enableCrossOsArchive: true`
- `.github/instructions/generic/code_comments.instructions.md:204` — `- Exported identifiers should have doc comments`

**FINDING: 🔴 High Risk**

No evidence found of data portability capabilities that would allow data subjects to receive their personal data in a structured, commonly used, and machine-readable format as required under GDPR Article 20. The evidence consists entirely of build system configurations, code style documentation, and repository metadata with no indication of data export, portability features, or user data access mechanisms. This represents a risk pattern consistent with non-compliance under GDPR Article 20.

**REMEDIATION DIRECTION**

Implement data portability functionality that enables users to export their personal data in structured formats (JSON, XML, CSV). This should include API endpoints or user interface features that allow authenticated users to request and download their complete personal data set, along with mechanisms to facilitate direct transmission to other data controllers when requested. The system should also maintain logs of data portability requests for audit purposes.

---

### GDPR-005: Privacy by Design Evidence

**LEGAL QUESTION**

Does the system demonstrate evidence of data protection by design and by default, implementing appropriate technical and organizational measures to ensure only necessary personal data is processed, as required under Article 25?

**REGULATORY STANDARD**

GDPR Article 25 (Data Protection by Design and by Default)

**EVIDENCE**

- `.github/actions/build-vault/action.yml:230` — `description: Vault is a tool for secrets management, encryption as a service, and privileged access management.`
- `.github/instructions/generic/code_comments.instructions.md:36` — `// Per PCI DSS compliance requirements, credit card data must be encrypted at rest`
- `.github/instructions/generic/code_comments.instructions.md:37` — `encryptedData := encrypt(cardData)`
- `.github/workflows/test-go.yml:157` — `- name: Sanitize timing files`
- `.github/workflows/test-go.yml:158` — `id: sanitize-timing-files`
- `CHANGELOG-v0.md:2201` — `a nonce. While not explicitly increasing security, it minimizes the`
- `CHANGELOG-v0.md:528` — `* Convergent Encryption: The version 2 algorithm used in `transit`'s`
- `CHANGELOG-v0.md:529` — `convergent encryption feature is susceptible to offline`
- `CHANGELOG-v0.md:532` — `encryption, we recommend upgrading, rotating your encryption key (the new`
- `CHANGELOG-v0.md:694` — `mechanisms, including PKCS#11 HSMs, now support rotation of encryption keys,`

**FINDING: 🔵 Pattern of Concern**

The evidence shows technical security measures including encryption at rest (code_comments.instructions.md:36-37), secrets management via Vault, and data sanitization processes (test-go.yml:157-158), which are positive indicators for data protection by design. However, the evidence lacks clear documentation of organizational measures, data minimization controls, or systematic privacy-by-design implementation processes that would fully demonstrate compliance with Article 25's requirements for processing only necessary personal data by default.

**REMEDIATION DIRECTION**

To address this pattern of concern, implement and document clear data minimization policies, create privacy impact assessment processes for new features, establish default privacy settings that limit data collection to what is strictly necessary, and document organizational procedures that demonstrate privacy-by-design principles are systematically applied throughout the development lifecycle. The existing encryption and security infrastructure provides a good foundation but needs to be supplemented with explicit privacy controls and documentation.

---

### GDPR-006: Data Breach Detection and Notification

**LEGAL QUESTION**

Does the system implement mechanisms for detecting personal data breaches and notifying the supervisory authority within 72 hours and affected data subjects without undue delay, as required under Articles 33 and 34?

**REGULATORY STANDARD**

GDPR Articles 33 (Notification to Authority); 34 (Communication to Data Subject)

**EVIDENCE**

- `.github/CODEOWNERS:55` — `# so stewards of the backend code are added below for notification.`
- `.github/instructions/generic/ember_hbs.instructions.md:112` — `<Hds::Alert @message="Operation completed successfully" />`
- `.github/instructions/generic/ember_tests.instructions.md:128` — `assert.ok(find('.alert-success'));`
- `.github/scripts/install-cob.sh:170` — `1) echo "alert" ;;`
- `.github/workflows/test-run-enos-scenario-matrix.yml:289` — `# Send slack notifications to #feed-vault-enos-failures any of our enos scenario commands fail.`
- `.release/ci.hcl:9` — `notification_channel = "C09LD1XT5MX" // #feed-vault-releases`
- `.release/ci.hcl:44` — `notification {`
- `.release/ci.hcl:57` — `notification {`
- `.release/ci.hcl:79` — `notification {`
- `.release/ci.hcl:103` — `notification {`

**FINDING: 🔴 High Risk**

No evidence found of GDPR-compliant data breach detection or notification mechanisms for personal data breaches. The repository contains only general system notifications for releases and CI/CD processes (found in .release/ci.hcl and workflow files), but lacks any specific implementation for detecting personal data breaches, automated 72-hour supervisory authority notifications, or data subject communication procedures. This creates a risk pattern consistent with non-compliance under GDPR Articles 33 and 34.

**REMEDIATION DIRECTION**

Implement a comprehensive data breach detection and notification system that includes: automated monitoring for personal data access anomalies and security incidents, a breach classification system to determine if personal data is involved, automated notification workflows to supervisory authorities within 72 hours of breach detection, and communication mechanisms to notify affected data subjects without undue delay. This system should integrate with existing security monitoring tools and maintain audit logs of all breach-related notifications and responses.

---

### GDPR-007: Data Retention and Deletion Policies

**LEGAL QUESTION**

Does the system implement data retention policies that limit the storage of personal data to what is necessary for the specified processing purpose, with automated deletion or anonymization when the purpose is fulfilled, consistent with the storage limitation principle under Article 5(1)(e)?

**REGULATORY STANDARD**

GDPR Article 5(1)(e) (Storage Limitation Principle)

**EVIDENCE**

- `.github/actions/build-vault/action.yml:138` — `driver-opts: network=host # So we can run our own little registry`
- `.github/actions/build-vault/action.yml:75` — `enableCrossOsArchive: true`
- `.github/actions/create-dynamic-config/action.yml:31` — `# If/when Github decides to purge our tiny config file cache we'll also`
- `.github/actions/set-up-go/action.yml:68` — `enableCrossOsArchive: true`
- `.github/instructions/generic/golang.instructions.md:41` — `- Use defer for cleanup operations (closing files, unlocking mutexes)`
- `.github/instructions/generic/golang.instructions.md:14` — `- Words in names that are initialisms or acronyms (e.g. “URL” or “NATO”) have a consistent case. For example, “URL” shou`
- `.github/instructions/generic/testing.instructions.md:27` — `- Cleanup resources after the test`
- `.github/instructions/generic/testing.instructions.md:28` — `- If files are needed, use a temp directory (in Go, prefer `t.TempDir()` for automatic cleanup)`
- `.github/scripts/install-cob.sh:107` — `# adjust archive name based on OS`
- `.github/scripts/install-cob.sh:123` — `# adjust archive name based on ARCH`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under GDPR Article 5(1)(e) storage limitation principle. While the repository contains some retention configurations for CI/CD artifacts (retention-days: 90 in mend-pr-scan.yml:42, retention-days: 7 in test-go.yml:480, and retention-days: 1 in test-go.yml:490), no evidence was found of systematic data retention policies, automated deletion mechanisms, or anonymization procedures for personal data processing within the Vault application itself. The cleanup references found are limited to development operations and temporary file management rather than personal data governance.

**REMEDIATION DIRECTION**

Implement comprehensive data retention policies that define specific retention periods for different categories of personal data based on processing purposes. Add automated deletion or anonymization functionality that triggers when data retention periods expire or processing purposes are fulfilled. Create configuration mechanisms to allow administrators to set and modify retention policies, and implement audit logging to demonstrate compliance with deletion schedules. Document these policies and ensure they are consistently applied across all personal data processing activities within the system.

---

### GDPR-008: Cross-Border Data Transfer Safeguards

**LEGAL QUESTION**

Does the system implement appropriate safeguards for transfers of personal data to third countries or international organizations, such as Standard Contractual Clauses or adequacy decisions, as required under Chapter V?

**REGULATORY STANDARD**

GDPR Chapter V, Articles 44-49 (Transfers to Third Countries)

**EVIDENCE**

- `.github/workflows/security-scan.yml:66` — `uses: github/codeql-action/upload-sarif@3096afedf9873361b2b2f65e1445b13272c83eb8  # TSCCR: could not find entry for gith`
- `.github/workflows/test-ci-bootstrap.yml:43` — `aws-region: us-east-1`
- `.github/workflows/test-ci-cleanup.yml:13` — `regions: ${{steps.setup.outputs.regions}}`
- `.github/workflows/test-ci-cleanup.yml:21` — `aws-region: us-east-1`
- `.github/workflows/test-ci-cleanup.yml:25` — `- name: Get all regions`
- `.github/workflows/test-ci-cleanup.yml:28` — `echo "regions=$(aws ec2 describe-regions --region us-east-1 --output json --query 'Regions[].RegionName' | tr -d '\n ')"`
- `.github/workflows/test-ci-cleanup.yml:50` — `aws-region: us-east-1`
- `.github/workflows/test-ci-cleanup.yml:79` — `region: ${{ fromJSON(needs.setup.outputs.regions) }}`
- `.github/workflows/test-ci-cleanup.yml:87` — `aws-region: us-east-1`
- `.github/workflows/test-ci-cleanup.yml:91` — `# Currently just checking VPC limits across all region, can add more checks here in future`

**FINDING: 🔴 High Risk**

The system shows a risk pattern consistent with non-compliance under GDPR Chapter V (Articles 44-49) regarding cross-border data transfer safeguards. Evidence reveals data processing operations across multiple international regions (us-east-1, us-west-1, and matrix configurations for multiple AWS regions) in files such as .github/workflows/test-ci-bootstrap.yml:43 and .github/workflows/test-run-enos-scenario.yml:92, but no corresponding documentation or implementation of required transfer safeguards such as Standard Contractual Clauses, adequacy decisions, or other Article 46 mechanisms was found in the codebase.

**REMEDIATION DIRECTION**

Implement and document appropriate GDPR transfer safeguards for all cross-border data operations. This should include: (1) conducting a data mapping exercise to identify what personal data flows between regions, (2) implementing Standard Contractual Clauses (SCCs) or relying on adequacy decisions where applicable, (3) adding configuration files or documentation that explicitly reference these legal mechanisms, (4) ensuring any data processing agreements with cloud providers (AWS) include appropriate GDPR transfer safeguards, and (5) documenting these safeguards in privacy policies and data processing records as required under Articles 30 and 44-49.

---

### GDPR-009: Data Protection Impact Assessment Indicators

**LEGAL QUESTION**

Does the system process personal data in a manner likely to result in high risk to data subjects, and if so, is there evidence that a Data Protection Impact Assessment has been considered, as required under Article 35?

**REGULATORY STANDARD**

GDPR Article 35 (Data Protection Impact Assessment)

**EVIDENCE**

- `CHANGELOG-v0.md:23` — `* autounseal/azure: Fix key version tracking (Enterprise)`
- `Makefile:62` — `# *-mem variants will enable memory profiling which will write snapshots of heap usage`
- `Makefile:64` — `# Note that any build can have profiling added via: `$ BUILD_TAGS=memprofiler make ...``
- `changelog/12422.txt:2` — `ui: updated client tracking config view`
- `changelog/25636.txt:2` — `core: make the best effort timeout for encryption count tracking persistence configurable via an environment variable.`
- `changelog/28494.txt:2` — `proxy/cache (enterprise): Fixed a data race that could occur while tracking capabilities in Proxy's static secret cache.`
- `changelog/29303.txt:2` — `core (enterprise): Add tracking of performance standbys by their HA node ID so that RPC connections can be more easily c`
- `changelog/30425.txt:2` — `**UI Telemetry**: add Posthog for UI telemetry tracking on HVD managed clusters`
- `command/agent/config/config.go:66` — `l.Profiling.UnusedKeys = nil`
- `command/agentproxyshared/auth/auth_test.go:208` — `// mockAuthMethodWithTracking is a mock auth method that tracks how many times`

**FINDING: 🔴 High Risk**

The evidence shows this system (HashiCorp Vault) processes sensitive personal data including secrets, API keys, passwords, and certificates, along with telemetry tracking (changelog/30425.txt:2) and client tracking capabilities (changelog/12422.txt:2). However, no evidence of a Data Protection Impact Assessment (DPIA) consideration or documentation was found in the codebase, creating a risk pattern consistent with non-compliance under GDPR Article 35. Given Vault's role in handling high-risk personal data processing activities, a DPIA should have been conducted and documented.

**REMEDIATION DIRECTION**

Conduct a formal Data Protection Impact Assessment as required under GDPR Article 35 for this high-risk data processing system. Document the DPIA findings, risk mitigation measures, and compliance controls in accessible project documentation. Include specific analysis of the telemetry tracking features and client data processing activities identified in the codebase. Establish a process for DPIA updates when new data processing features are added, such as the UI telemetry tracking mentioned in the changelog.

---

### GDPR-010: Privacy Policy and Notice Requirements

**LEGAL QUESTION**

Does the system provide transparent information to data subjects about the processing of their personal data, including identity of the controller, purposes of processing, and data subject rights, as required under Articles 13 and 14?

**REGULATORY STANDARD**

GDPR Articles 13 (Information at Collection); 14 (Information Not from Data Subject)

**EVIDENCE**

- `.github/ISSUE_TEMPLATE/plugin-submission.md:12` — `**Plugin Information**`
- `.github/actions/metadata/action.yml:5` — `name: Gather and export useful workflow metadata information.`
- `.github/actions/metadata/action.yml:7` — `Gather and export metadata about the repository, Github, and any other variable information we`
- `.github/instructions/generic/ember_general.instructions.md:20` — `- `ui/app/routes/` - Route handlers for URL endpoints and data loading logic`
- `.github/instructions/generic/ember_general.instructions.md:8` — `This document provides general coding standards and project context for HashiCorp Ember.js UI applications. This serves `
- `.github/instructions/generic/ember_hbs.instructions.md:10` — `> **Note**: For general project context, framework information, and repository structure, see `ember_general.instruction`
- `.github/instructions/generic/ember_js.instructions.md:10` — `> **Note**: For general project context, framework information, and repository structure, see `ember_general.instruction`
- `.github/instructions/generic/ember_styles.instructions.md:10` — `> **Note**: For general project context, framework information, and repository structure, see `ember_general.instruction`
- `.github/instructions/generic/ember_tests.instructions.md:10` — `> **Note**: For general project context, framework information, and repository structure, see `ember_general.instruction`
- `.github/scripts/install-cob.sh:174` — `5) echo "notice" ;;`

**FINDING: 🔴 High Risk**

No evidence found of transparent privacy notices or data subject information as required under GDPR Articles 13 and 14. The code repository contains only technical documentation and workflow files, with no privacy policy, data processing notices, or information about data controller identity, processing purposes, or data subject rights. This creates a risk pattern consistent with non-compliance under GDPR Articles 13 and 14.

**REMEDIATION DIRECTION**

Implement comprehensive privacy notices that clearly identify HashiCorp as the data controller, specify all purposes for personal data processing, detail data subject rights (access, rectification, erasure, portability, etc.), and explain the legal basis for processing. These notices should be prominently displayed where personal data is collected and easily accessible to users. Additionally, create mechanisms to provide this information when personal data is obtained from sources other than the data subject directly.

---

## HIPAA Findings

### HIPAA-001: PHI Identification and Protection

**LEGAL QUESTION**

Does this system collect, store, process, or transmit individually identifiable health information as defined under 45 CFR §160.103, and if so, are adequate technical safeguards in place to protect the confidentiality of such Protected Health Information?

**REGULATORY STANDARD**

HIPAA Privacy Rule 45 CFR §160.103; Security Rule 45 CFR §164.312(a)(1)

**EVIDENCE**

- `.github/instructions/generic/code_comments.instructions.md:8` — `## General Philosophy`
- `.github/instructions/generic/code_comments.instructions.md:8` — `## General Philosophy`
- `.github/instructions/generic/testing.instructions.md:6` — `# Philosophy & Principles`
- `.github/instructions/generic/testing.instructions.md:6` — `# Philosophy & Principles`
- `.github/workflows/test-go.yml:355` — `chmod a+rx runsc containerd-shim-runsc-v1`
- `CHANGELOG-v0.md:187` — `AES operations in its cryptographic barrier. Specifically, this means that`
- `CHANGELOG-v0.md:359` — `validation (in addition to the cryptographic signature) and a user and`
- `CHANGELOG-v0.md:2548` — `and uses the cryptographically signed dynamic metadata information that`
- `CHANGELOG-v0.md:187` — `AES operations in its cryptographic barrier. Specifically, this means that`
- `CHANGELOG-v0.md:359` — `validation (in addition to the cryptographic signature) and a user and`

**FINDING: 🔴 High Risk**

This HashiCorp Vault system appears designed to handle secrets and sensitive data based on the README description, but no evidence was found of specific HIPAA compliance measures or PHI identification controls in the analyzed code repository. While cryptographic operations are referenced in CHANGELOG-v0.md (lines 187, 359, 2548), there is no evidence of technical safeguards specifically designed to protect individually identifiable health information as required under 45 CFR §164.312(a)(1). This represents a risk pattern consistent with non-compliance under HIPAA Security Rule requirements if PHI is processed by this system.

**REMEDIATION DIRECTION**

If this Vault instance will handle PHI, implement specific HIPAA technical safeguards including: access controls with unique user identification, automatic logoff, encryption of PHI at rest and in transit, audit logging of PHI access, and integrity controls. Add configuration documentation demonstrating compliance with 45 CFR §164.312 technical safeguards. Consider implementing a HIPAA compliance module or configuration template that ensures all required safeguards are properly configured when PHI is stored or processed.

---

### HIPAA-002: Encryption at Rest

**LEGAL QUESTION**

Is electronic Protected Health Information encrypted when stored at rest using methods consistent with NIST Special Publication 800-111, as required for addressable implementation under the HIPAA Security Rule?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.312(a)(2)(iv); NIST SP 800-111

**EVIDENCE**

- `.build/entrypoint.sh:44` — `# Assume that /build is where we've mounted the vault repo.`
- `.copywrite.hcl:16` — `"enos/modules/k8s_deploy_vault/raft-config.hcl",`
- `.github/CODEOWNERS:72` — `# Cryptosec`
- `.github/CODEOWNERS:73` — `/api/auth/cert/                                      @hashicorp/vault-crypto`
- `.github/CODEOWNERS:74` — `/builtin/logical/pki/                                @hashicorp/vault-crypto`
- `.github/CODEOWNERS:75` — `/builtin/logical/pkiext/                             @hashicorp/vault-crypto`
- `.github/CODEOWNERS:76` — `/website/content/docs/secrets/pki/                   @hashicorp/vault-crypto @hashicorp/vault-education-approvers`
- `.github/CODEOWNERS:77` — `/website/content/api-docs/secret/pki/                @hashicorp/vault-crypto @hashicorp/vault-education-approvers`
- `.github/CODEOWNERS:78` — `/website/content/api-docs/secret/pki.mdx             @hashicorp/vault-crypto @hashicorp/vault-education-approvers`
- `.github/CODEOWNERS:79` — `/builtin/credential/cert/                            @hashicorp/vault-crypto`

**FINDING: 🔴 High Risk**

Analysis reveals a risk pattern consistent with non-compliance under HIPAA Security Rule 45 CFR §164.312(a)(2)(iv) and NIST SP 800-111. No evidence of encryption-at-rest implementation was found in the code repository, despite this being an addressable implementation requirement for ePHI storage. Additionally, anti-patterns indicating plaintext data handling were detected across multiple files including .github/workflows/build.yml:650, .github/workflows/ci.yml:362, and various changelog entries referencing plaintext operations.

**REMEDIATION DIRECTION**

Implement encryption-at-rest mechanisms consistent with NIST SP 800-111 standards for any systems handling ePHI. This should include configuring appropriate encryption algorithms (AES-256 minimum), secure key management practices, and proper encryption of data stores. Remove or remediate plaintext configurations in CI/CD workflows and ensure all sensitive data pathways implement proper encryption controls. Conduct a comprehensive review of data flows to identify all locations where ePHI might be stored and ensure encryption coverage.

---

### HIPAA-003: Encryption in Transit

**LEGAL QUESTION**

Are all transmissions of electronic Protected Health Information encrypted using transport-level security consistent with NIST guidelines, preventing unauthorized access during transmission across electronic communications networks?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.312(e)(1); 45 CFR §164.312(e)(2)(ii)

**EVIDENCE**

- `.build/entrypoint.sh:22` — `# https://packages.ubuntu.com/search?suite=noble&section=all&arch=any&keywords=linux-gnu-gcc&searchon=contents`
- `.build/entrypoint.sh:46` — `git config --global url."https://${GITHUB_TOKEN}@github.com".insteadOf "https://github.com"`
- `.build/go.sh:8` — `curl -L "https://go.dev/dl/go${GO_VERSION}.linux-${host_arch}.tar.gz" | tar -C /opt -zxv`
- `.build/system.sh:14` — `# https://packages.ubuntu.com/search?suite=noble&section=all&arch=any&keywords=crossbuild-essential&searchon=names`
- `.build/system.sh:20` — `ca-certificates \`
- `.build/system.sh:20` — `ca-certificates \`
- `.github/CODEOWNERS:5` — `# More on CODEOWNERS files: https://help.github.com/en/github/creating-cloning-and-archiving-repositories/about-code-own`
- `.github/CODEOWNERS:95` — `/sdk/helper/tlsutil/                                 @hashicorp/vault-crypto`
- `.github/CODEOWNERS:73` — `/api/auth/cert/                                      @hashicorp/vault-crypto`
- `.github/CODEOWNERS:79` — `/builtin/credential/cert/                            @hashicorp/vault-crypto`

**FINDING: 🔴 High Risk**

Analysis reveals a risk pattern consistent with non-compliance under HIPAA Security Rule 45 CFR §164.312(e)(1) and §164.312(e)(2)(ii). While evidence shows HTTPS usage in build scripts (.build/entrypoint.sh:46, .build/go.sh:8) and TLS-related code ownership (.github/CODEOWNERS:95), no explicit configuration or implementation of transport-level encryption for PHI transmissions was found. Multiple anti-patterns detected include unencrypted HTTP endpoints in Docker configurations (.release/docker/docker-entrypoint.sh:30, .release/docker/ubi-docker-entrypoint.sh:25) and test scenarios using HTTP protocols (.github/workflows/test-run-enos-scenario-containers.yml:137).

**REMEDIATION DIRECTION**

Implement mandatory transport-level encryption for all PHI transmissions by configuring TLS 1.2 or higher across all communication channels. Replace HTTP endpoints with HTTPS equivalents in Docker configurations and ensure all application interfaces enforce encrypted connections. Add explicit TLS configuration validation, remove any HTTP fallback options for PHI-handling services, and implement certificate management consistent with NIST guidelines. Conduct a comprehensive audit of all network communication paths to verify encryption coverage.

---

### HIPAA-004: Access Controls and Authentication

**LEGAL QUESTION**

Does the system implement technical policies and procedures for electronic information systems that maintain electronic Protected Health Information to allow access only to those persons or software programs that have been granted access rights as specified in 45 CFR §164.312(a)(1)?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.312(a)(1); 45 CFR §164.312(a)(2)(i)

**EVIDENCE**

- `.build/entrypoint.sh:13` — `[[ -z "$GITHUB_TOKEN" ]] && fail "A GITHUB_TOKEN has not been defined"`
- `.build/entrypoint.sh:46` — `git config --global url."https://${GITHUB_TOKEN}@github.com".insteadOf "https://github.com"`
- `.github/CODEOWNERS:53` — `# UI code related to Vault's JWT/OIDC auth method and OIDC provider.`
- `.github/CODEOWNERS:56` — `/ui/app/components/auth/form/oidc-jwt.ts @hashicorp/vault-ui @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:27` — `# Identity Integrations (OIDC, tokens)`
- `.github/CODEOWNERS:57` — `/ui/app/components/auth/form/saml.ts     @hashicorp/vault-ui @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:12` — `/builtin/credential/ldap/     @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:10` — `/builtin/credential/aws/      @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:11` — `/builtin/credential/github/   @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:12` — `/builtin/credential/ldap/     @hashicorp/vault-ecosystem`

**FINDING: 🔴 High Risk**

The evidence shows this is a HashiCorp Vault repository with multiple authentication mechanisms referenced in CODEOWNERS files (OIDC, JWT, SAML, LDAP, AWS, GitHub, Okta, certificate-based), but no actual implementation code or configuration demonstrating technical access controls that restrict system access to authorized persons or software programs only. This creates a risk pattern consistent with non-compliance under 45 CFR §164.312(a)(1), as the repository lacks evidence of implemented technical safeguards that would prevent unauthorized access to electronic Protected Health Information.

**REMEDIATION DIRECTION**

The development team needs to implement and document technical access control policies and procedures within the codebase. This should include: role-based access control configurations, user authentication and authorization code, session management controls, and automated access restriction mechanisms. The authentication methods referenced in the CODEOWNERS file should be fully implemented with proper access validation logic that ensures only authorized users and software programs can access PHI-containing systems.

---

### HIPAA-005: Session Management

**LEGAL QUESTION**

Does the system implement electronic procedures that terminate an electronic session after a predetermined time of inactivity, as required for PHI-accessing interfaces under the HIPAA Security Rule?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.312(a)(2)(iii)

**EVIDENCE**

- `.github/instructions/generic/ember_js.instructions.md:85` — `- Avoid `setTimeout` in favor of `requestAnimationFrame` for UI updates or proper async patterns for delays`
- `.github/instructions/generic/ember_js.instructions.md:86` — `- **Warning**: `setTimeout` is prone to testing issues and event loop management problems`
- `.github/instructions/generic/ember_tests.instructions.md:86` — `- Use Ember's `run.later` instead of `setTimeout` in tests for better runloop control`
- `.github/instructions/generic/golang.instructions.md:130` — `- Use context for cancellation and timeouts`
- `.github/workflows/mend-pr-scan.yml:33` — `scan-timeout-minutes: "30"`
- `.github/workflows/test-ci-cleanup.yml:42` — `timeout-minutes: 120`
- `.github/workflows/test-enos-scenario-ui.yml:69` — `timeout-minutes: 90`
- `.github/workflows/test-enos-scenario-ui.yml:142` — `run: enos scenario launch --timeout 60m0s --chdir ./enos ui edition:${{ needs.get-metadata.outputs.vault_edition }} back`
- `.github/workflows/test-enos-scenario-ui.yml:148` — `run: enos scenario launch --timeout 60m0s --chdir ./enos ui edition:${{ needs.get-metadata.outputs.vault_edition }} back`
- `.github/workflows/test-enos-scenario-ui.yml:153` — `run: enos scenario run --timeout 60m0s --chdir ./enos ui edition:${{ needs.get-metadata.outputs.vault_edition }} backend`

**FINDING: 🔴 High Risk**

No evidence of electronic session timeout procedures was found in the analyzed code repository. The evidence shows only CI/CD pipeline timeouts, test execution timeouts, and development guidelines against setTimeout usage, but contains no implementation of user session management or automatic session termination after predetermined periods of inactivity. This creates a risk pattern consistent with non-compliance under HIPAA Security Rule 45 CFR §164.312(a)(2)(iii).

**REMEDIATION DIRECTION**

Implement session management controls that automatically terminate user sessions accessing PHI after a predetermined period of inactivity. This should include configurable timeout values, session state tracking, automatic logout functionality, and proper cleanup of session data. The system should warn users before session expiration and require re-authentication to continue accessing PHI. Document the timeout periods and ensure they align with organizational security policies for PHI access.

---

### HIPAA-006: Audit Logging

**LEGAL QUESTION**

Does the system implement hardware, software, and procedural mechanisms that record and examine activity in information systems that contain or use electronic Protected Health Information, as required under the audit controls standard?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.312(b)

**EVIDENCE**

- `.github/instructions/generic/ember_js.instructions.md:95` — `## Error Handling and Logging`
- `.github/instructions/generic/ember_js.instructions.md:97` — `- Avoid `console.error` in production code - use proper logging libraries or framework-specific methods`
- `.github/instructions/generic/ember_js.instructions.md:99` — `- Use structured logging with consistent log levels (debug, info, warn, error)`
- `.github/pull_request_template.md:16` — `Examples of changes to security controls include using new access control methods, adding or removing logging pipelines,`
- `.github/scripts/install-cob.sh:13` — `-d turns on debug logging`
- `.github/scripts/install-cob.sh:378` — `# use in logging routines`
- `CHANGELOG-v0.md:8` — `* replication/perfstandby: Fix audit table upgrade on standbys [[GH-5811](https://github.com/hashicorp/vault/pull/5811)]`
- `CHANGELOG-v0.md:443` — `* In the audit log and in client responses, policies are now split into three`
- `CHANGELOG-v0.md:816` — `* Selective Audit HMACing of Request and Response Data Keys: HMACing in audit`
- `CHANGELOG-v0.md:900` — `proper auditing.`

**FINDING: 🔵 Pattern of Concern**

The system shows evidence of audit logging capabilities through HashiCorp Vault's built-in audit functionality, as evidenced by numerous changelog entries describing audit features, selective audit HMACing, and various audit backends (file, socket). However, the evidence does not demonstrate specific implementation or configuration of audit controls for Protected Health Information (PHI) monitoring, nor does it show procedural mechanisms for examining recorded activity as required under HIPAA Security Rule 45 CFR §164.312(b).

**REMEDIATION DIRECTION**

Implement and document specific audit logging procedures that capture access to PHI data, including user authentication events, data access patterns, modification attempts, and system administrative activities. Configure Vault's audit backends to ensure comprehensive logging of all PHI-related transactions, establish log review procedures with defined frequencies and responsible personnel, and create documentation demonstrating how the audit system meets HIPAA's requirement to "record and examine activity in information systems that contain or use electronic Protected Health Information."

---

### HIPAA-007: Minimum Necessary Access

**LEGAL QUESTION**

Does the system limit the Protected Health Information disclosed or accessed to the minimum necessary to accomplish the intended purpose, consistent with the minimum necessary standard under the Privacy Rule?

**REGULATORY STANDARD**

HIPAA Privacy Rule 45 CFR §164.502(b); 45 CFR §164.514(d)

**EVIDENCE**

- `.github/ISSUE_TEMPLATE.md:10` — `<!-- Uncomment this section if this is a feature request. Include or exclude other sections as deemed appropriate.`
- `.github/ISSUE_TEMPLATE/plugin-submission.md:10` — `Please provide details for the plugin to be listed. All fields are required for a submission to be included in the [Vaul`
- `.github/actions/build-vault/action.yml:104` — `docker_sha=$(git ls-tree HEAD Dockerfile --object-only --abbrev=5)`
- `.github/actions/build-vault/action.yml:105` — `build_sha=$(git ls-tree HEAD .build --object-only --abbrev=5)`
- `.github/actions/build-vault/action.yml:106` — `tools_sha=$(git ls-tree HEAD tools/tools.sh --object-only --abbrev=5)`
- `.github/actions/build-vault/action.yml:107` — `github_sha=$(git ls-tree HEAD .github/actions/build-vault --object-only --abbrev=5)`
- `.github/actions/build-vault/action.yml:153` — `# Only build a container for the host OS since the same container`
- `.github/actions/build-vault/action.yml:175` — `# Only build a container for the host OS since the same container`
- `.github/actions/build-vault/action.yml:161` — `cache-from: type=gha,scope=vault-builder-${{ steps.metadata.outputs.vault-builder-cache-key }}`
- `.github/actions/build-vault/action.yml:162` — `cache-to: type=gha,mode=min,scope=vault-builder-${{ steps.metadata.outputs.vault-builder-cache-key }}`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under HIPAA Privacy Rule 45 CFR §164.502(b) and §164.514(d). No access controls, data filtering mechanisms, or minimum necessary enforcement policies were identified in the code repository. Additionally, anti-patterns were detected in physical/dynamodb/dynamodb.go at lines 437 and 487 showing broad data projection expressions that may expose more data than necessary.

**REMEDIATION DIRECTION**

Implement role-based access controls that restrict PHI access based on user roles and specific business purposes. Add data filtering and field-level restrictions to ensure only the minimum necessary PHI fields are returned in database queries and API responses. Replace the broad ProjectionExpression queries in the DynamoDB implementation with specific field selections based on the requesting user's authorized access level and intended use case.

---

### HIPAA-008: Business Associate Agreements

**LEGAL QUESTION**

Does the system integrate with third-party services that may receive, maintain, or transmit Protected Health Information, and if so, is there evidence that Business Associate Agreement requirements are addressed in the code or configuration?

**REGULATORY STANDARD**

HIPAA Privacy Rule 45 CFR §164.502(e); 45 CFR §164.504(e)

**EVIDENCE**

- `.build/entrypoint.sh:30` — `s390x)`
- `.build/entrypoint.sh:31` — `export CC=s390x-linux-gnu-gcc`
- `.build/system.sh:18` — `gcc-s390x-linux-gnu \`
- `.build/system.sh:19` — `crossbuild-essential-s390x \`
- `.gitattributes:1` — `vendor/* linguist-vendored`
- `.github/CODEOWNERS:27` — `# Identity Integrations (OIDC, tokens)`
- `.github/CODEOWNERS:10` — `/builtin/credential/aws/      @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:16` — `/builtin/logical/aws/         @hashicorp/vault-ecosystem`
- `.github/ISSUE_TEMPLATE/plugin-submission.md:10` — `Please provide details for the plugin to be listed. All fields are required for a submission to be included in the [Vaul`
- `.github/actions/build-vault/action.yml:20` — `description: Package the binary into a Docker/AWS container.`

**FINDING: 🔴 High Risk**

The evidence shows this HashiCorp Vault system integrates with multiple third-party services including AWS (lines in .github/CODEOWNERS and containerize action), Docker registries, and various authentication providers, but contains no evidence of Business Associate Agreement requirements being addressed in code or configuration. This creates a risk pattern consistent with non-compliance under HIPAA Privacy Rule 45 CFR §164.502(e) and §164.504(e), as PHI may be transmitted to third parties without proper contractual safeguards.

**REMEDIATION DIRECTION**

Implement configuration settings or documentation requirements that enforce Business Associate Agreement validation before enabling third-party integrations. Add configuration flags that require BAA confirmation for services like AWS integrations, cloud storage, and external authentication providers. Consider adding a compliance module that tracks which integrations have valid BAAs and prevents data flow to uncovered third parties.

---

### HIPAA-009: Data Retention and Disposal

**LEGAL QUESTION**

Does the system implement policies and procedures to address the final disposition of electronic Protected Health Information and the hardware or electronic media on which it is stored, as well as removal of PHI before media is available for reuse?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.310(d)(2)(i); 45 CFR §164.310(d)(2)(ii)

**EVIDENCE**

- `.github/actions/build-vault/action.yml:75` — `enableCrossOsArchive: true`
- `.github/actions/build-vault/action.yml:138` — `driver-opts: network=host # So we can run our own little registry`
- `.github/actions/create-dynamic-config/action.yml:31` — `# If/when Github decides to purge our tiny config file cache we'll also`
- `.github/actions/set-up-go/action.yml:68` — `enableCrossOsArchive: true`
- `.github/instructions/generic/code_comments.instructions.md:154` — `- Delete comments that are no longer relevant`
- `.github/instructions/generic/code_comments.instructions.md:248` — `- **Update** or delete comments when code changes`
- `.github/instructions/generic/golang.instructions.md:98` — `- Use `delete(m, key)` to remove entries safely`
- `.github/instructions/generic/golang.instructions.md:41` — `- Use defer for cleanup operations (closing files, unlocking mutexes)`
- `.github/instructions/generic/testing.instructions.md:15` — `- If a test is not valuable, delete it`
- `.github/instructions/generic/testing.instructions.md:27` — `- Cleanup resources after the test`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under HIPAA Security Rule 45 CFR §164.310(d)(2)(i) and (ii). While the repository contains general cleanup instructions in development documentation (such as file cleanup in testing.instructions.md:27-28 and defer statements for resource cleanup in golang.instructions.md:41), there are no formal policies, procedures, or implemented controls specifically addressing the final disposition of electronic Protected Health Information or secure media sanitization before reuse. The only retention-related evidence found is a 90-day artifact retention setting in mend-pr-scan.yml:42, which appears to be for CI/CD artifacts rather than PHI data disposition.

**REMEDIATION DIRECTION**

Implement formal data retention and disposal policies with specific procedures for PHI final disposition and media sanitization. This should include code that securely overwrites or cryptographically destroys PHI data, documented procedures for hardware disposal that ensure PHI cannot be recovered, and automated controls that enforce secure deletion before media reuse. Additionally, implement logging and audit trails for all data disposition activities to demonstrate compliance with the disposal procedures.

---

### HIPAA-010: Breach Detection and Emergency Access

**LEGAL QUESTION**

Does the system implement procedures for detecting, reporting, and responding to suspected or known security incidents involving electronic Protected Health Information, and does it provide for emergency access to PHI during system disruptions?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.308(a)(6); 45 CFR §164.312(a)(2)(ii)

**EVIDENCE**

- `.github/CODEOWNERS:55` — `# so stewards of the backend code are added below for notification.`
- `.github/actions/build-vault/action.yml:71` — `- name: Restore UI from cache`
- `.github/actions/build-vault/action.yml:74` — `# Restore the UI asset from the UI build workflow. Never use a partial restore key.`
- `.github/actions/create-dynamic-config/action.yml:40` — `- name: Try to restore dynamic config from cache`
- `.github/actions/create-dynamic-config/action.yml:48` — `# If we can't restore it from config then set up pipeline and generate it`
- `.github/actions/install-tools/action.yml:8` — `possible we'll restore the tools from prior build that was cached. On a cache`
- `.github/actions/install-tools/action.yml:9` — `miss we'll rebuild the tools. After the tools are restored the `cache-path``
- `.github/actions/install-tools/action.yml:13` — `no-restore:`
- `.github/actions/install-tools/action.yml:14` — `description: Whether or not to restore the Go module cache on a cache hit`
- `.github/actions/install-tools/action.yml:35` — `# actions/cache restore has some surprising relative pathing behavior we`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under HIPAA Security Rule 45 CFR §164.308(a)(6) and §164.312(a)(2)(ii). No security incident detection, reporting, or response procedures for electronic PHI were found in the repository. Additionally, no emergency access procedures for PHI during system disruptions were identified in the analyzed files, which contain only build automation and caching configurations.

**REMEDIATION DIRECTION**

Implement comprehensive security incident response procedures including automated monitoring for PHI access anomalies, incident detection systems with alerting mechanisms, documented response workflows, and notification procedures. Establish emergency access protocols that allow authorized personnel to access PHI during system outages while maintaining audit trails and access controls. These procedures should be documented in code through configuration files, monitoring scripts, and access control policies that can be version-controlled and audited.

---

## PCI-DSS Findings

### PCIDSS-001: Cardholder Data Storage and Protection

**LEGAL QUESTION**

Does this system store, process, or transmit cardholder data including primary account numbers (PAN), and if so, are adequate protections in place to render stored PAN unreadable, as required under PCI DSS Requirement 3.5?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 3.5 (PAN Storage Protection)

**EVIDENCE**

- `.github/instructions/generic/ember_js.instructions.md:115` — `@tracked isExpanded = false;`
- `.github/instructions/generic/golang.instructions.md:86` — `- Use panic only for truly exceptional cases or programming errors`
- `.github/instructions/generic/golang.instructions.md:87` — `- Use recover to handle panics gracefully in server applications`
- `.github/workflows/test-ci-cleanup.yml:54` — `mask-aws-account-id: false`
- `.github/workflows/test-go.yml:183` — `# enable glob expansion`
- `.github/workflows/test-go.yml:192` — `# disable glob expansion`
- `CHANGELOG-v0.md:24` — `* cli: Fix panic that could occur if parameters were not provided [[GH-5603](https://github.com/hashicorp/vault/pull/560`
- `CHANGELOG-v0.md:99` — `* auth/ldap: Fix panic if specific values were given to be escaped [[GH-5471](https://github.com/hashicorp/vault/pull/54`
- `CHANGELOG-v0.md:100` — `* cli/auth: Fix panic if `vault auth` was given no parameters [[GH-5473](https://github.com/hashicorp/vault/pull/5473)]`
- `CHANGELOG-v0.md:101` — `* secret/database/mongodb: Fix panic that could occur at high load [[GH-5463](https://github.com/hashicorp/vault/pull/54`

**FINDING: 🟢 No Issue Found**

The evidence provided does not contain any indicators of cardholder data storage, processing, or transmission within this HashiCorp Vault repository. The evidence consists primarily of development artifacts (GitHub workflows, changelogs, and instructional files) with no references to payment card industry data, primary account numbers (PAN), or cardholder data handling. This appears to be a secrets management system repository focused on general security tooling rather than payment processing.

**REMEDIATION DIRECTION**

No remediation required based on current evidence. If this system will be used to store, process, or transmit cardholder data in the future, implement PCI DSS Requirement 3.5 controls including strong cryptography and security protocols to render stored PAN unreadable, establish proper key management procedures, and ensure any cardholder data is encrypted using industry-accepted algorithms with appropriate key lengths.

---

### PCIDSS-002: Encryption of Card Data in Transit and at Rest

**LEGAL QUESTION**

Is cardholder data encrypted using strong cryptography during transmission over open public networks and when stored at rest, consistent with PCI DSS Requirements 3.5 and 4.2?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirements 3.5 (Encryption at Rest); 4.2 (Encryption in Transit)

**EVIDENCE**

- `.build/entrypoint.sh:44` — `# Assume that /build is where we've mounted the vault repo.`
- `.build/entrypoint.sh:22` — `# https://packages.ubuntu.com/search?suite=noble&section=all&arch=any&keywords=linux-gnu-gcc&searchon=contents`
- `.build/entrypoint.sh:46` — `git config --global url."https://${GITHUB_TOKEN}@github.com".insteadOf "https://github.com"`
- `.build/go.sh:8` — `curl -L "https://go.dev/dl/go${GO_VERSION}.linux-${host_arch}.tar.gz" | tar -C /opt -zxv`
- `.build/system.sh:14` — `# https://packages.ubuntu.com/search?suite=noble&section=all&arch=any&keywords=crossbuild-essential&searchon=names`
- `.build/system.sh:20` — `ca-certificates \`
- `.copywrite.hcl:16` — `"enos/modules/k8s_deploy_vault/raft-config.hcl",`
- `.github/CODEOWNERS:72` — `# Cryptosec`
- `.github/CODEOWNERS:73` — `/api/auth/cert/                                      @hashicorp/vault-crypto`
- `.github/CODEOWNERS:74` — `/builtin/logical/pki/                                @hashicorp/vault-crypto`

**FINDING: 🔴 High Risk**

Risk pattern consistent with non-compliance under PCI DSS v4.0 Requirements 3.5 and 4.2. The evidence shows multiple instances of unencrypted HTTP communications including localhost connections in workflow files (.github/workflows/test-run-enos-scenario-containers.yml:137, .github/workflows/test-run-enos-scenario.yml:133) and default HTTP redirect addresses in Docker entrypoint scripts (.release/docker/docker-entrypoint.sh:30, .release/docker/ubi-docker-entrypoint.sh:25). No evidence was found demonstrating implementation of strong cryptographic controls for cardholder data encryption at rest or in transit over public networks.

**REMEDIATION DIRECTION**

Implement mandatory HTTPS/TLS encryption for all network communications, particularly replacing HTTP localhost connections with HTTPS equivalents and ensuring all default redirect addresses use encrypted protocols. Configure strong encryption algorithms (AES-256, RSA-2048 minimum) for data at rest storage with proper key management. Add configuration validation to reject unencrypted connections and implement certificate-based authentication for all data transmission channels. Update all Docker entrypoint scripts and workflow configurations to enforce encrypted communications by default rather than allowing HTTP fallbacks.

---

### PCIDSS-003: Access Control to Cardholder Data

**LEGAL QUESTION**

Does the system restrict access to cardholder data to only those individuals and systems whose job requires such access, implementing role-based access controls consistent with PCI DSS Requirement 7?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 7 (Restrict Access by Business Need to Know)

**EVIDENCE**

- `.github/instructions/generic/code_comments.instructions.md:108` — `if (user.role === 'admin' && user.status === 'active' && !user.suspended) { ... }`
- `.github/instructions/generic/code_comments.instructions.md:112` — `user.role === 'admin' && user.status === 'active' && !user.suspended;`
- `.github/instructions/generic/code_comments.instructions.md:107` — `// Check if user has admin permissions and is active`
- `.github/instructions/generic/ember_general.instructions.md:59` — `"ui (enterprise): Add advanced policy filtering"  // enterprise features`
- `.github/instructions/generic/ember_hbs.instructions.md:26` — `{{#if this.model.allowed_roles}}`
- `.github/instructions/generic/ember_hbs.instructions.md:29` — `{{#if (gt this.model.allowed_roles.length 0)}}`
- `.github/instructions/generic/ember_hbs.instructions.md:32` — `@secret="role/{{@model.id}}"`
- `.github/instructions/generic/ember_hbs.instructions.md:35` — `@secret={{concat "role/" @model.id}}`
- `.github/instructions/generic/ember_js.instructions.md:30` — `- Use type guards and discriminated unions for runtime type checking`
- `.github/scripts/install-cob.sh:227` — `nacl) return 0 ;;`

**FINDING: 🔵 Pattern of Concern**

The evidence shows some role-based access control patterns in instruction files (.github/instructions/generic/code_comments.instructions.md:108-112) with admin role checks and template references to allowed_roles in Ember components (.github/instructions/generic/ember_hbs.instructions.md:26-35). However, these appear to be documentation/instruction files rather than actual implementation code, and there is no concrete evidence of cardholder data access restrictions or comprehensive role-based controls that would satisfy PCI DSS Requirement 7 for limiting access to cardholder data based on business need-to-know.

**REMEDIATION DIRECTION**

Implement explicit role-based access controls that restrict cardholder data access to only authorized personnel whose job functions require it. This should include defining specific roles with granular permissions, implementing access control mechanisms in the actual application code (not just instruction files), documenting job function requirements for cardholder data access, and establishing regular access reviews. The current evidence suggests only general administrative controls rather than the specific cardholder data protection controls required by PCI DSS.

---

### PCIDSS-004: Network Segmentation

**LEGAL QUESTION**

Does the system implement network segmentation to isolate the cardholder data environment (CDE) from other network segments, reducing the scope of PCI DSS compliance as described in Requirement 1?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 1 (Network Security Controls)

**EVIDENCE**

- `.github/workflows/build.yml:48` — `#       accidentally regress.`
- `.github/workflows/test-ci-cleanup.yml:91` — `# Currently just checking VPC limits across all region, can add more checks here in future`
- `.github/workflows/test-ci-cleanup.yml:93` — `run: awslimitchecker -S "VPC" -r ${{matrix.region}}`
- `CHANGELOG-v0.md:1779` — `connections from being terminated by firewalls or proxies`
- `CHANGELOG-v0.md:1873` — `* replication: Add heartbeating to ensure firewalls don't kill connections to`
- `CHANGELOG-v0.md:1638` — `list of authorized addresses (IPs or subnets) can be defined and`
- `CHANGELOG-v0.md:1988` — `Subnet ID and Region [GH-2407]`
- `CHANGELOG-v0.md:1987` — `* auth/aws-ec2: AWS EC2 auth backend now supports constraints for VPC ID,`
- `CHANGELOG-v0.md:78` — `* secret/pki: Fix regression in 0.11.2+ causing the NotBefore value of`
- `CHANGELOG-v0.md:88` — `* Revocation: A regression in 0.11.2 (OSS) and 0.11.0 (Enterprise) caused`

**FINDING: 🔴 High Risk**

The evidence shows no implementation of network segmentation controls to isolate a cardholder data environment (CDE) from other network segments, creating a risk pattern consistent with non-compliance under PCI DSS v4.0 Requirement 1. While the codebase contains references to VPC configurations and firewall components in CHANGELOG-v0.md entries, there is no evidence of actual network segmentation implementation, security groups, or CDE isolation controls within the system architecture.

**REMEDIATION DIRECTION**

Implement proper network segmentation by configuring VPC subnets, security groups, and network access control lists (NACLs) to create a clearly defined and isolated cardholder data environment. Establish firewall rules that restrict traffic between the CDE and other network segments, allowing only necessary connections on specific ports and protocols. Document the network architecture showing clear boundaries between trusted and untrusted networks, and implement monitoring to ensure segmentation controls remain effective.

---

### PCIDSS-005: Vulnerability Management

**LEGAL QUESTION**

Does the system demonstrate evidence of vulnerability management practices including regular patching, dependency updates, and vulnerability scanning, consistent with PCI DSS Requirement 6?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 6 (Develop and Maintain Secure Systems)

**EVIDENCE**

- `.github/actions/run-apupgrade-tests/action.yml:5` — `name: Run Autopilot upgrade tests`
- `.github/actions/run-apupgrade-tests/action.yml:7` — `This action runs the Autopilot upgrade tests on Vault Enterprise.`
- `.github/actions/run-apupgrade-tests/action.yml:9` — `from the Vault Enterprise repository, builds the target version binary of Vault for Autopilot upgrade testing,`
- `.github/actions/run-apupgrade-tests/action.yml:10` — `and runs the Autopilot upgrade tool with the specified source versions.`
- `.github/actions/run-apupgrade-tests/action.yml:16` — `The target version binary of Vault for Autopilot upgrade testing will be built from this checkout.`
- `.github/actions/run-apupgrade-tests/action.yml:24` — `The source versions of Vault for Autopilot upgrade testing as a comma-separated string,`
- `.github/actions/run-apupgrade-tests/action.yml:69` — `- name: Checkout Vault tools repository to get the Autopilot upgrade tool`
- `.github/actions/run-apupgrade-tests/action.yml:97` — `# for apupgrade to use as a target version`
- `.github/actions/run-apupgrade-tests/action.yml:110` — `- name: Build Autopilot upgrade tool`
- `.github/actions/run-apupgrade-tests/action.yml:113` — `cd "${GITHUB_WORKSPACE}/vault-tools/apupgrade" || exit 1`

**FINDING: 🟠 Medium Risk**

The evidence shows limited vulnerability management practices that create a risk pattern consistent with non-compliance under PCI DSS Requirement 6. While automated upgrade testing capabilities exist in `.github/actions/run-apupgrade-tests/action.yml`, and dependency management guidance is present in `.github/instructions/generic/ember_general.instructions.md` (lines 68-71), there is no evidence of regular vulnerability scanning, systematic patching processes, or comprehensive dependency update procedures across the codebase.

**REMEDIATION DIRECTION**

Implement a comprehensive vulnerability management program including: automated vulnerability scanning tools integrated into the CI/CD pipeline, documented patching procedures with defined timelines, dependency scanning and update automation (such as Dependabot or similar tools), and regular security assessments. The existing upgrade testing framework should be expanded to include security-focused testing, and the dependency management guidelines should be enforced repository-wide with automated compliance checks.

---

### PCIDSS-006: Security Testing Evidence

**LEGAL QUESTION**

Does the system implement security testing controls including code review, static analysis, and penetration testing practices, as required under PCI DSS Requirement 6.3 and 11.4?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirements 6.3 (Security Vulnerabilities); 11.4 (Penetration Testing)

**EVIDENCE**

- `.github/instructions/generic/ember_general.instructions.md:35` — `- **Development**: ESLint for code linting, Prettier for code formatting`
- `.github/instructions/generic/ember_general.instructions.md:35` — `- **Development**: ESLint for code linting, Prettier for code formatting`
- `.github/instructions/generic/golang.instructions.md:138` — `- Understand escape analysis and stack vs heap allocation`
- `.github/instructions/generic/golang.instructions.md:155` — `- Understand escape analysis and stack vs heap allocation`
- `.github/workflows/actionlint.yml:1` — `name: Lint GitHub Actions Workflows`
- `.github/workflows/actionlint.yml:14` — `actionlint:`
- `.github/workflows/actionlint.yml:18` — `- name: "Run actionlint"`
- `.github/workflows/actionlint.yml:20` — `docker run --rm -v "$(pwd):/repo" --workdir /repo docker.mirror.hashicorp.services/rhysd/actionlint@sha256:887a259a5a534`
- `.github/workflows/code-checker.yml:1` — `name: Run linters`
- `.github/workflows/code-checker.yml:12` — `group: ${{ github.head_ref || github.run_id }}-lint`

**FINDING: 🟠 Medium Risk**

The system implements partial security testing controls with static analysis tools including ESLint, Prettier, actionlint, protolint, and Semgrep as evidenced in .github/workflows/code-checker.yml and .github/workflows/actionlint.yml. However, no evidence was found of formal code review processes, comprehensive vulnerability scanning, or penetration testing procedures, creating a risk pattern consistent with non-compliance under PCI DSS Requirements 6.3 and 11.4. The presence of multiple database execution anti-patterns (Exec() calls) in files like physical/cassandra/cassandra.go:297 and physical/cockroachdb/cockroachdb.go:104 suggests potential SQL injection vulnerabilities that existing static analysis may not be catching.

**REMEDIATION DIRECTION**

Implement a comprehensive security testing program that includes mandatory code reviews with security checklists, expand static analysis to include security-focused SAST tools beyond linting, establish regular penetration testing schedules, and add dynamic application security testing (DAST). Address the identified database execution patterns by implementing parameterized queries and input validation. Document all security testing procedures and maintain evidence of regular execution to demonstrate ongoing compliance with PCI DSS security testing requirements.

---

### PCIDSS-007: Audit Logging of Card Data Access

**LEGAL QUESTION**

Does the system implement audit trail mechanisms that record all individual access to cardholder data, all actions taken by any individual with root or administrative privileges, and all access to audit trails, as required under PCI DSS Requirement 10?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 10 (Log and Monitor All Access)

**EVIDENCE**

- `.github/instructions/generic/ember_js.instructions.md:95` — `## Error Handling and Logging`
- `.github/instructions/generic/ember_js.instructions.md:97` — `- Avoid `console.error` in production code - use proper logging libraries or framework-specific methods`
- `.github/instructions/generic/ember_js.instructions.md:99` — `- Use structured logging with consistent log levels (debug, info, warn, error)`
- `.github/pull_request_template.md:16` — `Examples of changes to security controls include using new access control methods, adding or removing logging pipelines,`
- `.github/scripts/install-cob.sh:13` — `-d turns on debug logging`
- `.github/scripts/install-cob.sh:378` — `# use in logging routines`
- `CHANGELOG-v0.md:8` — `* replication/perfstandby: Fix audit table upgrade on standbys [[GH-5811](https://github.com/hashicorp/vault/pull/5811)]`
- `CHANGELOG-v0.md:443` — `* In the audit log and in client responses, policies are now split into three`
- `CHANGELOG-v0.md:816` — `* Selective Audit HMACing of Request and Response Data Keys: HMACing in audit`
- `CHANGELOG-v0.md:900` — `proper auditing.`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under PCI DSS v4.0 Requirement 10. While the HashiCorp Vault codebase contains extensive audit logging functionality referenced throughout CHANGELOG-v0.md (lines 8, 443, 816, 1003, 1315, etc.), no specific evidence was found demonstrating audit trails for cardholder data access, administrative privilege actions, or audit trail access monitoring. The logging capabilities appear to be generic system audit functions rather than PCI DSS-compliant cardholder data audit mechanisms.

**REMEDIATION DIRECTION**

Implement specific audit logging mechanisms that capture: (1) all individual access events to cardholder data with user identification, timestamp, and data accessed; (2) all actions performed by users with root or administrative privileges including privilege escalation and system configuration changes; and (3) all access attempts to audit logs themselves including successful and failed access. Configure audit logs to be tamper-evident, automatically generated, and stored securely with proper retention periods as required by PCI DSS standards.

---

### PCIDSS-008: Key Management Practices

**LEGAL QUESTION**

Does the system implement cryptographic key management procedures including key generation, distribution, storage, rotation, and destruction, consistent with PCI DSS Requirement 3.6 and 3.7?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirements 3.6 (Key Management Procedures); 3.7 (Key Management Policies)

**EVIDENCE**

- `.build/entrypoint.sh:44` — `# Assume that /build is where we've mounted the vault repo.`
- `.copywrite.hcl:16` — `"enos/modules/k8s_deploy_vault/raft-config.hcl",`
- `.github/CODEOWNERS:7` — `* @hashicorp/vault`
- `.github/CODEOWNERS:10` — `/builtin/credential/aws/      @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:11` — `/builtin/credential/github/   @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:12` — `/builtin/credential/ldap/     @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:13` — `/builtin/credential/okta/     @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:16` — `/builtin/logical/aws/         @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:17` — `/builtin/logical/cassandra/   @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:18` — `/builtin/logical/consul/      @hashicorp/vault-ecosystem`

**FINDING: 🔴 High Risk**

Analysis reveals a risk pattern consistent with non-compliance under PCI DSS Requirements 3.6 and 3.7. While the repository appears to be HashiCorp Vault (a key management system), no evidence of implemented cryptographic key management procedures for generation, distribution, storage, rotation, and destruction was found in the provided code segments. Additionally, anti-patterns were detected in files such as api/auth/cert/cert.go:102-136 and api/client.go:324-424 showing potential insecure key handling practices.

**REMEDIATION DIRECTION**

The system requires implementation of comprehensive cryptographic key management procedures that explicitly address all PCI DSS requirements including secure key generation algorithms, encrypted distribution mechanisms, protected storage with proper access controls, automated rotation schedules, and secure destruction processes. Review and remediate the anti-patterns identified in the certificate authentication and client configuration modules to ensure keys are handled securely throughout their lifecycle. Document all key management policies and procedures, implement automated controls where possible, and establish audit trails for all key management operations.

---

### PCIDSS-009: Third Party Service Provider Controls

**LEGAL QUESTION**

Does the system manage third-party service providers that have access to cardholder data with appropriate controls, agreements, and monitoring, consistent with PCI DSS Requirement 12.8?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 12.8 (Third-Party Service Provider Management)

**EVIDENCE**

- `.gitattributes:1` — `vendor/* linguist-vendored`
- `.github/CODEOWNERS:53` — `# UI code related to Vault's JWT/OIDC auth method and OIDC provider.`
- `.github/CODEOWNERS:27` — `# Identity Integrations (OIDC, tokens)`
- `.github/ISSUE_TEMPLATE/plugin-submission.md:10` — `Please provide details for the plugin to be listed. All fields are required for a submission to be included in the [Vaul`
- `.github/actions/checkout/action.yml:7` — `Determine and checkout the correct Git reference depending on the actions event type and tags.`
- `.github/actions/checkout/action.yml:10` — `checkout-head:`
- `.github/actions/checkout/action.yml:13` — ``checkout-head` tag.`
- `.github/actions/checkout/action.yml:33` — `# Determine our desired checkout ref and fetch depth. Depending our our workflow event`
- `.github/actions/checkout/action.yml:40` — `# * If the trigger event is a pull request and a `checkout-head` tag is present or the`
- `.github/actions/checkout/action.yml:41` — `#   checkout-head input is set, we'll use HEAD of the PR branch instead of the magical`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under PCI DSS v4.0 Requirement 12.8. While the code repository contains references to third-party integrations (OIDC providers in .github/CODEOWNERS:53, plugin submissions in .github/ISSUE_TEMPLATE/plugin-submission.md:10, and vendor dependencies in .gitattributes:1), no documentation of formal third-party service provider agreements, due diligence processes, or ongoing monitoring controls was found. The system appears to integrate with external providers that could potentially access cardholder data environments without documented compliance management.

**REMEDIATION DIRECTION**

Implement a comprehensive third-party service provider management program that includes: formal written agreements with all service providers that may access cardholder data environments, documented due diligence processes to validate PCI DSS compliance status of these providers, regular monitoring and assessment procedures, and maintain an inventory of all third-party relationships with their associated risk levels. Create policy documentation that defines approval processes for new third-party integrations and establishes requirements for ongoing compliance validation.

---

### PCIDSS-010: Incident Response for Card Data Breach

**LEGAL QUESTION**

Does the system implement an incident response plan that addresses suspected or confirmed cardholder data breaches, including detection, containment, and notification procedures, as required under PCI DSS Requirement 12.10?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 12.10 (Incident Response Plan)

**EVIDENCE**

- `.github/CODEOWNERS:55` — `# so stewards of the backend code are added below for notification.`
- `.github/instructions/generic/ember_hbs.instructions.md:112` — `<Hds::Alert @message="Operation completed successfully" />`
- `.github/instructions/generic/ember_tests.instructions.md:128` — `assert.ok(find('.alert-success'));`
- `.github/scripts/install-cob.sh:170` — `1) echo "alert" ;;`
- `.github/workflows/test-run-enos-scenario-matrix.yml:289` — `# Send slack notifications to #feed-vault-enos-failures any of our enos scenario commands fail.`
- `.release/ci.hcl:9` — `notification_channel = "C09LD1XT5MX" // #feed-vault-releases`
- `.release/ci.hcl:44` — `notification {`
- `.release/ci.hcl:57` — `notification {`
- `.release/ci.hcl:79` — `notification {`
- `.release/ci.hcl:103` — `notification {`

**FINDING: 🔴 High Risk**

Analysis of the code repository reveals a risk pattern consistent with non-compliance under PCI DSS Requirement 12.10. While the evidence shows general notification mechanisms in `.release/ci.hcl` (lines 44-116) and workflow notifications in `.github/workflows/test-run-enos-scenario-matrix.yml` (line 289), no specific incident response plan for cardholder data breaches was identified. The repository lacks documented procedures for detection, containment, assessment, and notification specifically related to suspected or confirmed cardholder data breaches.

**REMEDIATION DIRECTION**

Implement a comprehensive incident response plan specifically addressing cardholder data breaches. This should include documented procedures for breach detection mechanisms, containment protocols, forensic assessment steps, and notification workflows for relevant stakeholders including payment brands, acquirers, and regulatory bodies. The plan should be stored in the repository as formal documentation (e.g., `INCIDENT_RESPONSE_PLAN.md`) and integrated with existing notification systems. Additionally, establish automated detection capabilities and define clear escalation procedures with specific timelines for each phase of incident response.

---

## SOC2 Findings

### SOC2-001: User Authentication Controls

**LEGAL QUESTION**

Does the system implement logical access security controls over user authentication that are suitably designed and operating effectively to restrict access to authorized users, consistent with the Common Criteria CC6.1 requirement for logical and physical access controls?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC6.1 (Logical and Physical Access Controls)

**EVIDENCE**

- `.build/entrypoint.sh:13` — `[[ -z "$GITHUB_TOKEN" ]] && fail "A GITHUB_TOKEN has not been defined"`
- `.build/entrypoint.sh:46` — `git config --global url."https://${GITHUB_TOKEN}@github.com".insteadOf "https://github.com"`
- `.github/CODEOWNERS:10` — `/builtin/credential/aws/      @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:11` — `/builtin/credential/github/   @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:12` — `/builtin/credential/ldap/     @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:13` — `/builtin/credential/okta/     @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:79` — `/builtin/credential/cert/                            @hashicorp/vault-crypto`
- `.github/CODEOWNERS:53` — `# UI code related to Vault's JWT/OIDC auth method and OIDC provider.`
- `.github/CODEOWNERS:56` — `/ui/app/components/auth/form/oidc-jwt.ts @hashicorp/vault-ui @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:27` — `# Identity Integrations (OIDC, tokens)`

**FINDING: 🔵 Pattern of Concern**

The evidence shows a Vault system repository with multiple authentication mechanisms referenced (AWS, GitHub, LDAP, Okta, certificate-based, JWT/OIDC, SAML) in CODEOWNERS files, indicating the system supports diverse authentication methods. However, the analyzed code primarily reveals build/deployment token handling (.build/entrypoint.sh:13, .github/actions/build-vault/action.yml:196) rather than the actual implementation of user authentication controls, creating a risk pattern consistent with non-compliance under SOC 2 CC6.1 due to insufficient evidence of logical access security control implementation.

**REMEDIATION DIRECTION**

To address this finding, the development team should ensure that actual authentication control implementations are properly documented and accessible for compliance review. This includes making available the source code for the authentication modules referenced in CODEOWNERS (builtin/credential/* directories), configuration files showing authentication policy enforcement, and documentation demonstrating how each authentication method restricts access to authorized users only. The current evidence shows infrastructure tokens but lacks visibility into user-facing authentication controls that would demonstrate CC6.1 compliance.

---

### SOC2-002: Role-Based Access Control

**LEGAL QUESTION**

Does the system implement role-based or attribute-based access controls that restrict system functions and data access based on authorized user roles, consistent with the principle of least privilege as required under CC6.3?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC6.3 (Role-Based Access and Least Privilege)

**EVIDENCE**

- `.github/actions/build-vault/action.yml:230` — `description: Vault is a tool for secrets management, encryption as a service, and privileged access management.`
- `.github/actions/build-vault/action.yml:161` — `cache-from: type=gha,scope=vault-builder-${{ steps.metadata.outputs.vault-builder-cache-key }}`
- `.github/actions/build-vault/action.yml:162` — `cache-to: type=gha,mode=min,scope=vault-builder-${{ steps.metadata.outputs.vault-builder-cache-key }}`
- `.github/actions/build-vault/action.yml:183` — `cache-from: type=gha,scope=vault-builder-${{ steps.metadata.outputs.vault-builder-cache-key }}`
- `.github/actions/build-vault/action.yml:184` — `cache-to: type=gha,mode=min,scope=vault-builder-${{ steps.metadata.outputs.vault-builder-cache-key }}`
- `.github/instructions/generic/code_comments.instructions.md:108` — `if (user.role === 'admin' && user.status === 'active' && !user.suspended) { ... }`
- `.github/instructions/generic/code_comments.instructions.md:112` — `user.role === 'admin' && user.status === 'active' && !user.suspended;`
- `.github/instructions/generic/code_comments.instructions.md:107` — `// Check if user has admin permissions and is active`
- `.github/instructions/generic/code_comments.instructions.md:107` — `// Check if user has admin permissions and is active`
- `.github/instructions/generic/code_comments.instructions.md:108` — `if (user.role === 'admin' && user.status === 'active' && !user.suspended) { ... }`

**FINDING: 🟠 Medium Risk**

The evidence shows limited implementation of role-based access controls with basic role checking patterns found in .github/instructions/generic/code_comments.instructions.md (lines 107-114) demonstrating admin role validation. However, the repository lacks comprehensive evidence of systematic RBAC implementation across the codebase that would demonstrate full compliance with least privilege principles. While HashiCorp Vault is described as a "tool for secrets management, encryption as a service, and privileged access management," the actual access control logic and role hierarchies are not sufficiently documented in the available evidence.

**REMEDIATION DIRECTION**

Implement and document a comprehensive role-based access control system that clearly defines user roles, permissions matrices, and access restrictions for different system functions. Add explicit role validation throughout the application code, create documented role hierarchies that follow least privilege principles, and ensure all sensitive operations include proper role-based authorization checks. Consider expanding the basic admin role pattern found in the instructions to include multiple role levels with granular permissions.

---

### SOC2-003: Encryption in Transit

**LEGAL QUESTION**

Does the system protect data during transmission over networks using encryption or other equivalent security measures, consistent with the CC6.7 requirement for protection of information during transmission?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC6.7 (Data Transmission Protection)

**EVIDENCE**

- `.build/entrypoint.sh:22` — `# https://packages.ubuntu.com/search?suite=noble&section=all&arch=any&keywords=linux-gnu-gcc&searchon=contents`
- `.build/entrypoint.sh:46` — `git config --global url."https://${GITHUB_TOKEN}@github.com".insteadOf "https://github.com"`
- `.build/go.sh:8` — `curl -L "https://go.dev/dl/go${GO_VERSION}.linux-${host_arch}.tar.gz" | tar -C /opt -zxv`
- `.build/system.sh:14` — `# https://packages.ubuntu.com/search?suite=noble&section=all&arch=any&keywords=crossbuild-essential&searchon=names`
- `.build/system.sh:20` — `ca-certificates \`
- `.github/CODEOWNERS:5` — `# More on CODEOWNERS files: https://help.github.com/en/github/creating-cloning-and-archiving-repositories/about-code-own`
- `.github/CODEOWNERS:95` — `/sdk/helper/tlsutil/                                 @hashicorp/vault-crypto`
- `.github/CODE_OF_CONDUCT.md:5` — `Please read the full text at https://www.hashicorp.com/community-guidelines`
- `.github/ISSUE_TEMPLATE.md:3` — `For questions, the best place to get answers is on our [mailing list](https://groups.google.com/forum/#!forum/vault-tool`
- `.github/ISSUE_TEMPLATE.md:5` — `Please note: We take Vault's security and our users' trust very seriously. If you believe you have found a security issu`

**FINDING: 🔴 High Risk**

Analysis reveals a risk pattern consistent with non-compliance under SOC 2 CC6.7 due to insufficient evidence of encryption controls for data transmission protection. While the evidence shows HTTPS usage in build scripts and configuration files, critical anti-patterns were detected including unencrypted HTTP endpoints in Docker entry points (docker-entrypoint.sh:30 and ubi-docker-entrypoint.sh:25) and HTTP protocol usage in test workflows. The repository references a TLS utility directory (/sdk/helper/tlsutil/) but lacks concrete implementation evidence of mandatory encryption for production data transmission.

**REMEDIATION DIRECTION**

Implement comprehensive encryption-in-transit controls by configuring all production endpoints to use HTTPS/TLS exclusively, removing HTTP fallbacks from Docker configurations, and establishing network-level encryption requirements. Update application configurations to enforce TLS for all client-server communications, implement certificate management procedures, and conduct a complete audit of all transmission pathways to ensure no unencrypted channels exist for sensitive data transfer.

---

### SOC2-004: Logging and Monitoring

**LEGAL QUESTION**

Does the system implement logging, monitoring, and alerting mechanisms that detect and record security events, anomalies, and unauthorized activities, as required under CC7.2 for monitoring system components for anomalies?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC7.2 (Monitoring of System Components)

**EVIDENCE**

- `.github/CODEOWNERS:55` — `# so stewards of the backend code are added below for notification.`
- `.github/instructions/generic/ember_hbs.instructions.md:112` — `<Hds::Alert @message="Operation completed successfully" />`
- `.github/instructions/generic/ember_js.instructions.md:95` — `## Error Handling and Logging`
- `.github/instructions/generic/ember_js.instructions.md:97` — `- Avoid `console.error` in production code - use proper logging libraries or framework-specific methods`
- `.github/instructions/generic/ember_js.instructions.md:99` — `- Use structured logging with consistent log levels (debug, info, warn, error)`
- `.github/instructions/generic/ember_tests.instructions.md:128` — `assert.ok(find('.alert-success'));`
- `.github/instructions/generic/testing.instructions.md:9` — `- Test coverage is not a metric to optimize for`
- `.github/pull_request_template.md:16` — `Examples of changes to security controls include using new access control methods, adding or removing logging pipelines,`
- `.github/scripts/install-cob.sh:13` — `-d turns on debug logging`
- `.github/scripts/install-cob.sh:378` — `# use in logging routines`

**FINDING: 🟠 Medium Risk**

The evidence shows partial implementation of logging and monitoring mechanisms but presents a risk pattern consistent with non-compliance under SOC 2 CC7.2. While structured logging guidance exists in `.github/instructions/generic/ember_js.instructions.md:97-99` and Datadog monitoring integration is configured in `.github/workflows/test-go.yml:128-456`, there is insufficient evidence of comprehensive security event detection, anomaly monitoring, or unauthorized activity alerting capabilities. The repository contains development-level logging instructions and CI/CD monitoring but lacks clear implementation of production security monitoring systems.

**REMEDIATION DIRECTION**

Implement comprehensive security event logging and monitoring by deploying centralized log aggregation with security-specific log parsing rules, anomaly detection algorithms, and automated alerting for unauthorized activities. Configure security information and event management (SIEM) capabilities that go beyond the current Datadog integration to include real-time security event correlation, threat detection rules, and automated incident response triggers. Document and implement specific logging standards for security events including authentication failures, privilege escalations, and data access patterns.

---

### SOC2-005: Change Management

**LEGAL QUESTION**

Does the system demonstrate evidence of change management controls including version control, code review processes, and controlled deployment procedures, as required under CC8.1 for managing changes to infrastructure, data, software, and procedures?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC8.1 (Change Management)

**EVIDENCE**

- `.build/entrypoint.sh:49` — `cd build || exit 1`
- `.build/go.sh:8` — `curl -L "https://go.dev/dl/go${GO_VERSION}.linux-${host_arch}.tar.gz" | tar -C /opt -zxv`
- `.copywrite.hcl:1` — `schema_version = 1`
- `.copywrite.hcl:16` — `"enos/modules/k8s_deploy_vault/raft-config.hcl",`
- `.copywrite.hcl:20` — `"enos/.terraform/**",`
- `.github/ISSUE_TEMPLATE.md:15` — `<!-- The version can be retrieved with `vault version`. -->`
- `.github/ISSUE_TEMPLATE.md:17` — `* Vault Version:`
- `.github/ISSUE_TEMPLATE/bug_report.md:31` — `* Vault Server Version (retrieve with `vault status`):`
- `.github/ISSUE_TEMPLATE/bug_report.md:32` — `* Vault CLI Version (retrieve with `vault version`):`
- `.github/ISSUE_TEMPLATE/bug_report.md:19` — `A clear and concise description of what the bug is.`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOC 2 CC8.1 change management requirements. While the repository contains GitHub Actions workflows for building (as evidenced by .github/actions/build-vault/action.yml with version controls at lines 49-50 and 85-86) and issue templates suggesting some process structure, there is no evidence of formal code review processes, controlled deployment procedures, or comprehensive change management controls for infrastructure, data, software, and procedures as required by the standard.

**REMEDIATION DIRECTION**

Implement formal change management controls including: mandatory pull request reviews with approval requirements before merging code changes, documented deployment procedures with approval gates for production environments, version control policies that prevent direct commits to main branches, and formal change approval processes for infrastructure and procedural modifications. Configure branch protection rules in GitHub and establish clear documentation of the change management workflow that covers all aspects required by CC8.1.

---

### SOC2-006: Incident Response

**LEGAL QUESTION**

Does the system implement incident detection, response, and recovery procedures that enable timely identification and remediation of security incidents, consistent with CC7.3 requirements for evaluating security events and CC7.4 for responding to identified incidents?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC7.3 (Security Event Evaluation); CC7.4 (Incident Response)

**EVIDENCE**

- `.github/instructions/generic/ember_general.instructions.md:68` — `- Pin exact versions for critical dependencies or use tilde (`~`) for patch updates only`
- `.github/instructions/generic/ember_general.instructions.md:70` — `- Use tilde (`~`) for regular dependencies, exact versions for security-critical packages`
- `.github/instructions/generic/ember_general.instructions.md:81` — `"lodash": "4.17.21",        // exact version for critical packages`
- `.github/instructions/generic/ember_hbs.instructions.md:112` — `<Hds::Alert @message="Operation completed successfully" />`
- `.github/instructions/generic/ember_tests.instructions.md:128` — `assert.ok(find('.alert-success'));`
- `.github/pull_request_template.md:6` — `- [ ] **LTS**: If this fixes a critical security vulnerability or [severity 1](https://www.hashicorp.com/customer-succes`
- `.github/pull_request_template.md:6` — `- [ ] **LTS**: If this fixes a critical security vulnerability or [severity 1](https://www.hashicorp.com/customer-succes`
- `.github/scripts/install-cob.sh:170` — `1) echo "alert" ;;`
- `.github/workflows/changelog-checker.yml:39` — `changelog_files=$(git --no-pager diff --name-only HEAD "$(git merge-base HEAD "origin/${{ github.event.pull_request.base`
- `.github/workflows/changelog-checker.yml:47` — `toolchain_files=$(git --no-pager diff --name-only HEAD "$(git merge-base HEAD "origin/${{ github.event.pull_request.base`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOC 2 CC7.3 and CC7.4 requirements. While the repository contains security-related references in changelog files and pull request templates mentioning critical security vulnerabilities, no actual incident detection, response, or recovery procedures are documented or implemented in the codebase. The evidence primarily consists of development workflow files and historical changelog entries rather than operational incident response capabilities.

**REMEDIATION DIRECTION**

Implement comprehensive incident response procedures including automated security event monitoring and alerting systems, documented incident response playbooks, and recovery procedures. Add security monitoring tools that can detect and evaluate security events in real-time, establish clear escalation procedures for different severity levels, and create automated response mechanisms for common incident types. Document these procedures in the repository and integrate incident response workflows into the CI/CD pipeline to ensure timely identification and remediation of security incidents.

---

### SOC2-007: Vendor and Dependency Risk

**LEGAL QUESTION**

Does the system assess and manage risks associated with third-party vendors, libraries, and service providers, including dependency vulnerability management, consistent with CC9.2 requirements for risk assessment of third-party service providers?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC9.2 (Third-Party Risk Management)

**EVIDENCE**

- `.copywrite.hcl:14` — `"ui/pnpm-lock.yaml",`
- `.github/actions/setup-pnpm/action.yml:18` — `package_json_file: './ui/package.json'`
- `.github/actions/setup-pnpm/action.yml:23` — `node-version-file: './ui/package.json'`
- `.github/actions/setup-pnpm/action.yml:25` — `cache-dependency-path: ui/pnpm-lock.yaml`
- `.github/instructions/generic/code_comments.instructions.md:172` — `**Example - Block comments for context:**`
- `.github/instructions/generic/code_comments.instructions.md:179` — `const requestTypeName = constructTypeName(apiName, methodName);`
- `.github/instructions/generic/ember_general.instructions.md:67` — `## package.json Guidelines`
- `.github/instructions/generic/ember_general.instructions.md:72` — `- Keep `package.json` changes minimal and focused on the specific feature or fix`
- `.github/instructions/generic/ember_general.instructions.md:74` — `- Ensure package.json changes are independent of other code changes (except lock files)`
- `.github/instructions/generic/ember_general.instructions.md:71` — `- Dependencies in `resolutions` block MUST be pinned (no `~` or `^`)`

**FINDING: 🔴 High Risk**

The evidence shows dependency management artifacts (pnpm-lock.yaml, package.json references in .github/actions/setup-pnpm/action.yml) and dependency pinning guidelines in .github/instructions/generic/ember_general.instructions.md, but lacks systematic third-party risk assessment processes, vendor evaluation procedures, or dependency vulnerability management controls. This presents a risk pattern consistent with non-compliance under SOC 2 Trust Services Criteria CC9.2, as there is no evidence of formal risk assessment mechanisms for third-party service providers or comprehensive dependency vulnerability monitoring.

**REMEDIATION DIRECTION**

Implement a formal third-party risk management program that includes: vendor risk assessment procedures with documented evaluation criteria, dependency vulnerability scanning tools integrated into the CI/CD pipeline, regular security assessments of third-party libraries and services, a vendor inventory with associated risk ratings, and documented processes for ongoing monitoring and remediation of identified vulnerabilities in dependencies. Establish clear policies for vendor onboarding, periodic risk reviews, and incident response procedures for third-party security issues.

---

### SOC2-008: Data Backup and Recovery

**LEGAL QUESTION**

Does the system implement data backup, replication, and recovery controls that ensure availability and recoverability of data, consistent with the A1.2 criterion for recovery of infrastructure and data to meet objectives?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria A1.2 (Recovery of Infrastructure and Data)

**EVIDENCE**

- `.build/entrypoint.sh:25` — `export CC=x86_64-linux-gnu-gcc`
- `.build/entrypoint.sh:28` — `export CC=aarch64-linux-gnu-gcc`
- `.build/entrypoint.sh:31` — `export CC=s390x-linux-gnu-gcc`
- `.build/entrypoint.sh:12` — `[[ -z "$GOARCH" ]] && fail "A GOARCH has not been defined"`
- `.build/entrypoint.sh:13` — `[[ -z "$GITHUB_TOKEN" ]] && fail "A GITHUB_TOKEN has not been defined"`
- `.build/entrypoint.sh:18` — `# We're building for a different architecture than our target host OS so`
- `.build/entrypoint.sh:19` — `# we have to tell the Go compiler to use the correct C cross-compiler for`
- `.build/entrypoint.sh:34` — `fail "Building for $GOARCH has not been implemented"`
- `.build/entrypoint.sh:44` — `# Assume that /build is where we've mounted the vault repo.`
- `.build/system.sh:7` — `export DEBIAN_FRONTEND=noninteractive`

**FINDING: 🔴 High Risk**

The evidence shows a complete absence of data backup, replication, and recovery controls in the analyzed code repository. The provided evidence consists entirely of build system configuration files (.build/entrypoint.sh, .build/system.sh), code ownership definitions (.github/CODEOWNERS), and basic project documentation, with no implementation of backup procedures, data replication mechanisms, or recovery protocols. This represents a risk pattern consistent with non-compliance under SOC 2 Trust Services Criteria A1.2, as there are no observable controls to ensure availability and recoverability of data to meet operational objectives.

**REMEDIATION DIRECTION**

The system needs to implement comprehensive data backup and recovery controls including automated backup procedures, data replication mechanisms across geographically distributed locations, documented recovery time objectives (RTO) and recovery point objectives (RPO), regular backup testing and validation processes, and disaster recovery procedures. These controls should be codified in the repository through infrastructure-as-code definitions, backup automation scripts, and documented recovery playbooks that demonstrate the organization's ability to restore critical data and systems within acceptable timeframes to meet business continuity requirements.

---

### SOC2-009: Multi-Factor Authentication

**LEGAL QUESTION**

Does the system implement or support multi-factor authentication for user access, particularly for privileged accounts and administrative interfaces, consistent with CC6.1 requirements for logical access security?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC6.1 (Logical Access - MFA)

**EVIDENCE**

- `.github/CODEOWNERS:15` — `# Secrets engines (pki, ssh, totp and transit omitted)`
- `.github/CODEOWNERS:15` — `# Secrets engines (pki, ssh, totp and transit omitted)`
- `.github/workflows/oss.yml:32` — `- 'builtin/logical/totp/**'`
- `.github/workflows/oss.yml:32` — `- 'builtin/logical/totp/**'`
- `CHANGELOG-v0.md:849` — `* command: Re-add `-mfa` flag and migrate to OSS binary [[GH-4223](https://github.com/hashicorp/vault/pull/4223)]`
- `CHANGELOG-v0.md:852` — `* mfa: Invalidation of MFA configurations (Enterprise)`
- `CHANGELOG-v0.md:989` — `* **Okta Push support in Okta Auth Backend**: If a user account has MFA`
- `CHANGELOG-v0.md:990` — `required within Okta, an Okta Push MFA flow can be used to successfully`
- `CHANGELOG-v0.md:1158` — `* legacymfa/duo: Fix intermittent panic when Duo could not be reached`
- `CHANGELOG-v0.md:1224` — `* auth/github: The legacy MFA system can now be used with the GitHub auth`

**FINDING: 🔵 Pattern of Concern**

The system shows evidence of multi-factor authentication capabilities including TOTP support (builtin/logical/totp/** in .github/workflows/oss.yml:32), legacy MFA systems for GitHub and Okta authentication backends, and enterprise MFA features supporting Duo Push, Okta Push, and PingID Push as documented in CHANGELOG-v0.md. However, the evidence primarily shows MFA feature availability rather than implementation details or enforcement policies for privileged accounts and administrative interfaces, creating a risk pattern consistent with non-compliance under SOC 2 CC6.1.

**REMEDIATION DIRECTION**

The engineering team should provide configuration files, policy definitions, or administrative documentation that demonstrates MFA is actually configured and enforced for privileged accounts and administrative access to the Vault system. Evidence should include specific MFA enforcement policies, administrative interface protection settings, and documentation showing that multi-factor authentication is required (not just available) for high-privilege operations and system administration.

---

### SOC2-010: Security Policy Documentation

**LEGAL QUESTION**

Does the system demonstrate evidence of documented security policies, including acceptable use, data classification, and access management policies, as required under CC1.1 for the entity's commitment to integrity and ethical values?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC1.1 (COSO Principle 1 - Integrity and Ethical Values)

**EVIDENCE**

- `.github/CODE_OF_CONDUCT.md:3` — `HashiCorp Community Guidelines apply to you when interacting with the community here on GitHub and contributing code.`
- `.github/workflows/changelog-checker.yml:53` — `echo "Reference - https://github.com/hashicorp/vault/blob/main/CONTRIBUTING.md#changelog-entries"`
- `CONTRIBUTING.md:1` — `# Contributing to Vault`
- `ui/README.md:18` — `- [Contributing / Best Practices](#contributing--best-practices)`
- `ui/README.md:151` — `### Contributing / Best Practices`
- `ui/README.md:153` — `Hello and thank you for contributing to the Vault UI! Below is a list of patterns we follow on the UI team to keep in mi`
- `ui/app/components/app-footer.hbs:35` — `@text="Contributing docs"`
- `ui/app/templates/docs.hbs:41` — `Contributing docs`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOC 2 CC1.1, as no documented security policies for acceptable use, data classification, or access management were found in the repository. While community guidelines (.github/CODE_OF_CONDUCT.md:3) and contributing documentation exist, these do not constitute the formal security policy documentation required to demonstrate the entity's commitment to integrity and ethical values. The repository contains only development-focused documentation rather than operational security policies.

**REMEDIATION DIRECTION**

The organization needs to create and document formal security policies covering acceptable use of systems, data classification standards, and access management procedures. These policies should be stored in accessible locations within the repository (such as a /policies or /security directory) and should clearly articulate the organization's commitment to security, integrity, and ethical values as required for SOC 2 compliance. The policies should go beyond development guidelines to address operational security requirements.

---

## SOX Findings

### SOX-001: Financial Data Integrity Controls

**LEGAL QUESTION**

Does the system implement controls to ensure the integrity, accuracy, and completeness of financial data and transactions, consistent with SOX Section 302 requirements for management certification of financial statements?

**REGULATORY STANDARD**

SOX Section 302 (Corporate Responsibility for Financial Reports)

**EVIDENCE**

- `.github/actions/set-up-go/action.yml:73` — `# These results are used to balance our Go test groups, without which we could have`
- `.github/actions/set-up-go/action.yml:74` — `# painfully unbalanced Go test execution times. We have to ensure current caches for all`
- `.github/instructions/generic/code_comments.instructions.md:36` — `// Per PCI DSS compliance requirements, credit card data must be encrypted at rest`
- `.github/instructions/generic/ember_tests.instructions.md:39` — `- Error handling and validation logic`
- `.github/instructions/generic/ember_tests.instructions.md:180` — `module('input validation', function (hooks) {`
- `.github/instructions/generic/ember_tests.instructions.md:197` — `test('it displays validation error when secret name is empty', async function (assert) {`
- `.github/instructions/generic/ember_tests.instructions.md:204` — `'Should display validation error for empty secret name'`
- `.github/instructions/generic/golang.instructions.md:52` — `- Use switch statements instead of repeated if statements for validation:`
- `.github/instructions/generic/golang.instructions.md:137` — `- Use build constraints for platform-specific code`
- `.github/instructions/generic/golang.instructions.md:158` — `- Use build constraints for platform-specific code`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOX Section 302 requirements for financial data integrity controls. While the repository contains general validation logic references in test instructions (.github/instructions/generic/ember_tests.instructions.md:180, 197) and checksum verification for software integrity (.github/scripts/install-cob.sh:346-359), no specific financial data integrity controls, transaction validation mechanisms, or management certification frameworks were identified in the codebase.

**REMEDIATION DIRECTION**

Implement comprehensive financial data integrity controls including: automated validation rules for all financial transactions, data completeness checks with error handling and logging, segregation of duties controls in financial data processing workflows, and audit trail mechanisms that capture all changes to financial data with user attribution and timestamps. Additionally, establish automated control testing and monitoring capabilities that can support management's quarterly and annual certifications required under SOX Section 302.

---

### SOX-002: Access Controls to Financial Systems

**LEGAL QUESTION**

Does the system implement access controls that restrict access to financial systems and data to authorized personnel, with appropriate authentication and authorization mechanisms, as required under SOX Section 404 internal controls?

**REGULATORY STANDARD**

SOX Section 404 (Management Assessment of Internal Controls)

**EVIDENCE**

- `.github/CODEOWNERS:62` — `/.github/workflows/build.yml   @hashicorp/github-secure-vault-core @hashicorp/team-vault-quality`
- `.github/actions/build-vault/action.yml:74` — `# Restore the UI asset from the UI build workflow. Never use a partial restore key.`
- `.github/actions/checkout/action.yml:33` — `# Determine our desired checkout ref and fetch depth. Depending our our workflow event`
- `.github/actions/metadata/action.yml:5` — `name: Gather and export useful workflow metadata information.`
- `.github/actions/metadata/action.yml:8` — `might want for variables or flow control in our various workflows. We centralize it here so as`
- `.github/actions/metadata/action.yml:9` — `to have a single point of truth. This workflow also handles checking out the correct Git reference`
- `.github/actions/metadata/action.yml:10` — `depending on workflow trigger and tags. This workflow is used in both CE and Ent and thus needs`
- `.github/actions/metadata/action.yml:26` — `value: ${{ steps.workflow-metadata.outputs.compute-build }}`
- `.github/actions/metadata/action.yml:28` — `description: A JSON encoded "runs-on" for web UI build workflows.`
- `.github/actions/metadata/action.yml:29` — `value: ${{ steps.workflow-metadata.outputs.compute-build-ui }}`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOX Section 404 internal controls requirements. While the repository contains GitHub workflow access controls in .github/CODEOWNERS:62 restricting build workflows to specific HashiCorp teams, no evidence was found of authentication mechanisms, authorization controls, or access restriction configurations for the actual financial systems and data that this Vault system would protect. The evidence only shows development workflow controls, not the runtime access controls required for SOX compliance.

**REMEDIATION DIRECTION**

Implement and document comprehensive access control mechanisms including multi-factor authentication, role-based access controls (RBAC), user provisioning/deprovisioning procedures, and audit logging for all financial system access. Configure Vault policies that explicitly restrict financial data access to authorized personnel only, with appropriate authentication backends and authorization policies. Document these controls with evidence of their implementation, testing, and ongoing monitoring to satisfy SOX Section 404 requirements for internal controls over financial reporting.

---

### SOX-003: Audit Trail for Financial Transactions

**LEGAL QUESTION**

Does the system maintain a complete and tamper-evident audit trail of all financial transactions, modifications, and access events, sufficient to support the audit requirements under SOX Section 802?

**REGULATORY STANDARD**

SOX Section 802 (Criminal Penalties for Altering Documents)

**EVIDENCE**

- `.github/actions/checkout/action.yml:47` — `# the most shallow clone possible for speed, but we also need to support getting history`
- `.github/actions/checkout/action.yml:50` — `# history because we need all commits on the branch.`
- `.github/instructions/generic/ember_general.instructions.md:50` — `# Changelog Guidelines`
- `.github/instructions/generic/ember_general.instructions.md:52` — `For files in the `changelog/` directory:`
- `.github/instructions/generic/ember_general.instructions.md:58` — `// Changelog entries`
- `.github/workflows/build.yml:40` — `#     * Skipping builds entirely if the commit or PR only modifies changelog or website documentation.`
- `.github/workflows/changelog-checker.yml:1` — `# This workflow checks that there is either a 'pr/no-changelog' label applied to a PR`
- `.github/workflows/changelog-checker.yml:2` — `# or there is a changelog/<pr number>.txt file associated with a PR for a changelog entry`
- `.github/workflows/changelog-checker.yml:4` — `name: Check Changelog`
- `.github/workflows/changelog-checker.yml:14` — `# checks that a changelog entry is present for a PR`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOX Section 802. While the repository contains changelog tracking mechanisms (.github/workflows/changelog-checker.yml) for code changes, no evidence was found of audit logging capabilities for financial transactions, modifications, or access events. The README identifies this as HashiCorp Vault, a secrets management tool that mentions "recording a detailed audit log," but no actual audit trail implementation, configuration, or tamper-evidence controls are present in the examined code.

**REMEDIATION DIRECTION**

Implement comprehensive audit logging that captures all financial transaction events, user access attempts, data modifications, and system changes with tamper-evident controls such as cryptographic signatures or write-once storage. Configure audit logs to include timestamps, user identification, action details, and before/after states for all modifications. Establish log retention policies, integrity verification mechanisms, and secure storage to ensure audit trails cannot be altered or deleted, meeting SOX requirements for financial transaction accountability.

---

### SOX-004: Change Management for Financial Software

**LEGAL QUESTION**

Does the system implement change management controls for software that processes financial data, including version control, code review, testing, and controlled deployment, consistent with SOX IT general controls?

**REGULATORY STANDARD**

SOX Section 404 (ITGC - Change Management Controls)

**EVIDENCE**

- `.build/entrypoint.sh:49` — `cd build || exit 1`
- `.build/go.sh:8` — `curl -L "https://go.dev/dl/go${GO_VERSION}.linux-${host_arch}.tar.gz" | tar -C /opt -zxv`
- `.copywrite.hcl:1` — `schema_version = 1`
- `.copywrite.hcl:16` — `"enos/modules/k8s_deploy_vault/raft-config.hcl",`
- `.github/CODEOWNERS:60` — `# Release config; service account is required for automation tooling.`
- `.github/CODEOWNERS:61` — `/.release/                     @hashicorp/github-secure-vault-core @hashicorp/team-vault-quality`
- `.github/ISSUE_TEMPLATE.md:15` — `<!-- The version can be retrieved with `vault version`. -->`
- `.github/ISSUE_TEMPLATE.md:17` — `* Vault Version:`
- `.github/ISSUE_TEMPLATE/bug_report.md:31` — `* Vault Server Version (retrieve with `vault status`):`
- `.github/ISSUE_TEMPLATE/bug_report.md:32` — `* Vault CLI Version (retrieve with `vault version`):`

**FINDING: 🟠 Medium Risk**

The evidence shows limited change management controls for this financial software system, creating a risk pattern consistent with non-compliance under SOX Section 404 ITGC requirements. While version control artifacts are present (.github/actions/build-vault/action.yml:49-50 shows version metadata handling) and code ownership controls exist (.github/CODEOWNERS:60-61 designates release config ownership), there is insufficient evidence of comprehensive code review processes, formal testing procedures, or controlled deployment mechanisms required for SOX compliance.

**REMEDIATION DIRECTION**

Implement documented change management procedures including mandatory code review workflows in GitHub, automated testing pipelines with evidence retention, formal approval processes for production deployments, and maintain audit trails for all changes to financial data processing components. Establish clear segregation of duties between development, testing, and production deployment roles, and ensure all change management activities are logged and auditable.

---

### SOX-005: Segregation of Duties Evidence

**LEGAL QUESTION**

Does the system implement segregation of duties controls that prevent any single individual from having the ability to both authorize and execute financial transactions, or to both develop and deploy changes to financial systems?

**REGULATORY STANDARD**

SOX Section 404 (Internal Controls - Segregation of Duties)

**EVIDENCE**

- `.github/CODEOWNERS:42` — `/website/data/          @hashicorp/vault-education-approvers`
- `.github/CODEOWNERS:43` — `/website/public/        @hashicorp/vault-education-approvers`
- `.github/CODEOWNERS:44` — `/website/content/       @hashicorp/vault-education-approvers`
- `.github/CODEOWNERS:45` — `/website/templates/     @hashicorp/vault-education-approvers`
- `.github/CODEOWNERS:46` — `/website/redirects.js   @hashicorp/vault-education-approvers`
- `.github/CODEOWNERS:49` — `/website/content/docs/plugins/              @hashicorp/vault-ecosystem @hashicorp/vault-education-approvers`
- `.github/CODEOWNERS:50` — `/website/content/docs/upgrading/plugins.mdx @hashicorp/vault-ecosystem @hashicorp/vault-education-approvers`
- `.github/CODEOWNERS:76` — `/website/content/docs/secrets/pki/                   @hashicorp/vault-crypto @hashicorp/vault-education-approvers`
- `.github/CODEOWNERS:77` — `/website/content/api-docs/secret/pki/                @hashicorp/vault-crypto @hashicorp/vault-education-approvers`
- `.github/CODEOWNERS:78` — `/website/content/api-docs/secret/pki.mdx             @hashicorp/vault-crypto @hashicorp/vault-education-approvers`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOX Section 404 segregation of duties requirements. While the CODEOWNERS file demonstrates code review controls for documentation and website content (lines 42-104), no evidence was found of segregation controls that prevent individuals from both developing and deploying changes to the actual financial system code, or controls preventing the same person from authorizing and executing financial transactions within the Vault system itself.

**REMEDIATION DIRECTION**

Implement and document segregation of duties controls by: (1) establishing separate approval groups for core financial system code versus deployment permissions, ensuring no individual has both development and production deployment access; (2) configuring the Vault system's internal authorization workflows to require different individuals for transaction authorization versus execution; (3) expanding the CODEOWNERS file to cover all critical system components beyond just documentation, with distinct approval groups that enforce role separation; and (4) implementing automated checks in CI/CD pipelines that verify segregation requirements are met before any financial system changes are deployed.

---

### SOX-006: Data Retention for Financial Records

**LEGAL QUESTION**

Does the system implement data retention policies that preserve financial records, audit work papers, and supporting documentation for the minimum retention period required under SOX Section 802 (not less than 7 years)?

**REGULATORY STANDARD**

SOX Section 802 (Document Retention - 7 Year Minimum)

**EVIDENCE**

- `.github/actions/build-vault/action.yml:75` — `enableCrossOsArchive: true`
- `.github/actions/set-up-go/action.yml:68` — `enableCrossOsArchive: true`
- `.github/scripts/install-cob.sh:107` — `# adjust archive name based on OS`
- `.github/scripts/install-cob.sh:123` — `# adjust archive name based on ARCH`
- `.github/scripts/install-cob.sh:265` — `log_err "untar unknown archive format for ${tarball}"`
- `.github/workflows/build.yml:308` — `enableCrossOsArchive: true`
- `.github/workflows/copywrite.yml:24` — `archive-checksum: c299f830e6eef7e126a3c6ef99ac6f43a3c132d830c769e0d36fa347fa1af254`
- `.github/workflows/mend-pr-scan.yml:42` — `retention-days: 90`
- `.github/workflows/test-go.yml:480` — `retention-days: 7`
- `.github/workflows/test-go.yml:490` — `retention-days: 1`

**FINDING: 🔴 High Risk**

The evidence reveals a risk pattern consistent with non-compliance under SOX Section 802. While the system shows archival capabilities in CI/CD workflows, the retention periods are significantly below the required 7-year minimum - with retention-days set to only 90 days (.github/workflows/mend-pr-scan.yml:42), 7 days (.github/workflows/test-go.yml:480), and as low as 1 day (.github/workflows/test-go.yml:490, 527). No evidence was found of any data retention policies or configurations that meet the mandatory 7-year retention requirement for financial records and audit documentation.

**REMEDIATION DIRECTION**

Implement comprehensive data retention policies that preserve financial records, audit work papers, and supporting documentation for a minimum of 7 years as required by SOX Section 802. This should include updating all retention-days configurations in workflow files to reflect long-term storage requirements, establishing automated archival processes for financial data, and implementing audit trails to demonstrate compliance with the retention timeline. Consider implementing tiered storage solutions that can economically maintain records for the full 7-year period while ensuring they remain accessible for regulatory purposes.

---

### SOX-007: Internal Control Documentation

**LEGAL QUESTION**

Does the system provide evidence of documented internal controls over financial reporting, including control objectives, control activities, and monitoring procedures, as required under SOX Section 404(a)?

**REGULATORY STANDARD**

SOX Section 404(a) (Management Assessment of Internal Controls)

**EVIDENCE**

- `.gitattributes:2` — `website/* linguist-documentation`
- `.github/actions/metadata/action.yml:8` — `might want for variables or flow control in our various workflows. We centralize it here so as`
- `.github/instructions/generic/code_comments.instructions.md:36` — `// Per PCI DSS compliance requirements, credit card data must be encrypted at rest`
- `.github/instructions/generic/code_comments.instructions.md:166` — `- Use JSDoc for public API documentation`
- `.github/instructions/generic/ember_general.instructions.md:59` — `"ui (enterprise): Add advanced policy filtering"  // enterprise features`
- `.github/instructions/generic/ember_general.instructions.md:8` — `This document provides general coding standards and project context for HashiCorp Ember.js UI applications. This serves `
- `.github/instructions/generic/ember_general.instructions.md:29` — `## Framework and Tools`
- `.github/instructions/generic/ember_general.instructions.md:30` — `- **Frontend Framework**: Ember.js 4.x with Ember Octane patterns and decorators`
- `.github/instructions/generic/ember_general.instructions.md:33` — `- **Styling**: SCSS with HashiCorp Design System (HDS) components and Bulma CSS framework`
- `.github/instructions/generic/ember_hbs.instructions.md:10` — `> **Note**: For general project context, framework information, and repository structure, see `ember_general.instruction`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOX Section 404(a). No documented internal controls over financial reporting were found in the code repository, including absence of control objectives, control activities, or monitoring procedures. While the evidence includes general development documentation and PCI DSS compliance references (.github/instructions/generic/code_comments.instructions.md:36), there is no evidence of the specific internal control documentation required for financial reporting systems under SOX requirements.

**REMEDIATION DIRECTION**

The organization needs to establish and document comprehensive internal controls over financial reporting as required by SOX Section 404(a). This should include creating formal documentation that defines control objectives for financial data integrity, implementing specific control activities such as authorization procedures and segregation of duties, establishing monitoring procedures to assess control effectiveness, and maintaining evidence of management's assessment of these controls. All documentation should be version-controlled and regularly reviewed to ensure ongoing compliance with SOX requirements.

---

### SOX-008: Anti-Tampering Controls

**LEGAL QUESTION**

Does the system implement controls to prevent unauthorized alteration or destruction of financial records, including integrity verification, immutable storage, and tamper detection mechanisms, consistent with SOX Section 802 anti-destruction requirements?

**REGULATORY STANDARD**

SOX Section 802 (Criminal Penalties for Document Destruction/Alteration)

**EVIDENCE**

- `.github/CODEOWNERS:7` — `* @hashicorp/vault`
- `.github/CODEOWNERS:10` — `/builtin/credential/aws/      @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:11` — `/builtin/credential/github/   @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:12` — `/builtin/credential/ldap/     @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:13` — `/builtin/credential/okta/     @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:16` — `/builtin/logical/aws/         @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:17` — `/builtin/logical/cassandra/   @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:18` — `/builtin/logical/consul/      @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:19` — `/builtin/logical/database/    @hashicorp/vault-ecosystem`
- `.github/CODEOWNERS:20` — `/builtin/logical/mongodb/     @hashicorp/vault-ecosystem`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOX Section 802 anti-destruction requirements. No integrity verification mechanisms, immutable storage controls, or tamper detection systems were identified in the codebase. Anti-patterns detected include data truncation operations in CHANGELOG-v0.md:425, audit/headers_test.go:58 containing delete operations, and multiple references to truncation in AWS credential handling, which could compromise financial record integrity.

**REMEDIATION DIRECTION**

Implement comprehensive anti-tampering controls including cryptographic integrity verification (digital signatures/checksums) for all financial records, configure immutable storage backends with write-once-read-many capabilities, and deploy tamper detection mechanisms that log and alert on unauthorized modification attempts. Add audit trails that cannot be altered or deleted, and ensure all financial data operations include integrity checks before and after processing. Consider implementing blockchain or similar immutable ledger technology for critical financial record storage.

---

## TCPA Findings

### TCPA-001: Prior Express Written Consent for SMS

**LEGAL QUESTION**

Does the system obtain prior express written consent before sending marketing or promotional text messages, including a clear and conspicuous disclosure that consent is being sought, as required under 47 U.S.C. §227(b)(1) and 47 CFR §64.1200(a)(2)?

**REGULATORY STANDARD**

TCPA 47 U.S.C. §227(b)(1); 47 CFR §64.1200(a)(2)

**EVIDENCE**

- `.release/linux/postinst:44` — `Agreement`
- `.release/linux/postinst:47` — `agreement governing your use of the software made available here:`
- `.release/linux/postinst:52` — `Agreement, the IBM International License Agreement for Evaluation of Programs`
- `.release/linux/postinst:53` — `(for evaluation uses), or the IBM International License Agreement for Early`
- `CONTRIBUTING.md:142` — `## Contributor License Agreement`
- `CONTRIBUTING.md:144` — `We require that all contributors sign our Contributor License Agreement ("CLA") before we can accept the contribution.`
- `api/LICENSE:220` — `You alone, and You hereby agree to indemnify every Contributor for any`
- `api/LICENSE:262` — `license agreements (excluding distributors and resellers) which have been`
- `api/LICENSE:306` — `This License represents the complete agreement concerning the subject`
- `api/auth/approle/LICENSE:220` — `You alone, and You hereby agree to indemnify every Contributor for any`

**FINDING: 🔴 High Risk**

No evidence was found of prior express written consent mechanisms for SMS marketing or promotional messages, creating a risk pattern consistent with non-compliance under 47 U.S.C. §227(b)(1) and 47 CFR §64.1200(a)(2). The code repository evidence only shows software license agreements and contributor agreements, but contains no SMS consent collection interfaces, opt-in forms, or disclosure language required for TCPA compliance. This appears to be a security/secrets management tool (Vault) rather than a marketing platform, but any SMS functionality would still require proper consent mechanisms.

**REMEDIATION DIRECTION**

If this system sends any marketing or promotional SMS messages, implement a clear opt-in consent collection mechanism that includes: (1) a checkbox or similar affirmative action for SMS consent, (2) clear disclosure that the person is consenting to receive marketing texts, (3) identification of the sender, and (4) instructions on how to opt out. Store consent records with timestamps and ensure they're obtained before any marketing SMS communications. If the system doesn't send marketing SMS, document this explicitly to avoid future compliance questions.

---

### TCPA-002: Opt-Out Mechanism Implementation

**LEGAL QUESTION**

Does the system provide a clear and easy mechanism for recipients to opt out of receiving further messages, and does it honor opt-out requests promptly, as required under TCPA and CTIA guidelines?

**REGULATORY STANDARD**

TCPA 47 U.S.C. §227(b)(2)(E); CTIA Messaging Principles

**EVIDENCE**

- `.github/instructions/generic/ember_js.instructions.md:84` — `- Only use `@task` from ember-concurrency when you need specific features like cancellation or `task.isRunning` state ma`
- `.github/instructions/generic/golang.instructions.md:130` — `- Use context for cancellation and timeouts`
- `.github/scripts/report-build-status.sh:23` — `# Sometimes failed jobs can have a result of "cancelled". Handle both.`
- `.github/scripts/report-build-status.sh:26` — `if [[ "$job" == *"failure"* || "$job" == *"cancelled"* ]]; then`
- `.github/workflows/actionlint.yml:8` — `# cancel existing runs of the same workflow on the same ref`
- `.github/workflows/actionlint.yml:11` — `cancel-in-progress: true`
- `.github/workflows/build-artifacts-ce.yml:245` — `if ! grep -q -v -E '(failure|cancelled)' <<< "$results"; then`
- `.github/workflows/build.yml:71` — `cancel-in-progress: true`
- `.github/workflows/build.yml:593` — `if ! grep -q -v -E '(failure|cancelled)' <<< "$results"; then`
- `.github/workflows/ci.yml:22` — `cancel-in-progress: true`

**FINDING: 🔴 High Risk**

No evidence found of TCPA-compliant opt-out mechanisms for message recipients in the analyzed code repository. The evidence shows only technical cancellation functionality related to GitHub workflows and build processes (such as cancel-in-progress settings in various .yml files), but contains no implementation of user-facing opt-out mechanisms, opt-out request processing, or message unsubscribe functionality. This represents a risk pattern consistent with non-compliance under TCPA 47 U.S.C. §227(b)(2)(E) and CTIA Messaging Principles.

**REMEDIATION DIRECTION**

Implement a comprehensive opt-out system that includes: (1) clear opt-out instructions in all outbound messages (such as "Reply STOP to unsubscribe"), (2) automated processing of opt-out requests within the required timeframes, (3) persistent storage of opt-out preferences with proper database schemas, (4) validation that opted-out recipients are excluded from future messaging campaigns, and (5) logging and audit trails for opt-out compliance monitoring. The system should also provide confirmation messages when opt-out requests are successfully processed.

---

### TCPA-003: Do Not Call List Checking

**LEGAL QUESTION**

Does the system check phone numbers against the National Do Not Call Registry and maintain an internal do-not-call list before initiating outbound calls or messages, as required under 47 CFR §64.1200(c)?

**REGULATORY STANDARD**

TCPA 47 CFR §64.1200(c) (Do Not Call Requirements)

**EVIDENCE**

- `.github/actions/build-vault/action.yml:138` — `driver-opts: network=host # So we can run our own little registry`
- `.github/actions/build-vault/action.yml:141` — `run: docker run -d -p 5000:5000 --restart always --name registry registry:2`
- `.github/actions/containerize/action.yml:7` — `Containerize vault binaries and annotate them with the correct registry tags. Artifacts will be`
- `.github/actions/containerize/action.yml:22` — `description: Package the binary into a UBI container suitable for the Redhat Quay registry.`
- `.release/release-metadata.hcl:4` — `url_docker_registry_dockerhub = "https://hub.docker.com/r/hashicorp/vault"`
- `.release/release-metadata.hcl:5` — `url_docker_registry_ecr = "https://gallery.ecr.aws/hashicorp/vault"`
- `Dockerfile:85` — `FROM registry.access.redhat.com/ubi10/ubi-minimal AS ubi`
- `builtin/credential/okta/backend_test.go:93` — `RegistryName:    "okta-auth",`
- `builtin/credential/userpass/stepwise_test.go:21` — `RegistryName:    customPluginName,`
- `builtin/logical/aws/stepwise_test.go:22` — `RegistryName:    "aws-sec",`

**FINDING: 🔴 High Risk**

No evidence was found of Do Not Call Registry checking functionality or internal do-not-call list maintenance in the analyzed code repository. All instances of "registry" in the evidence refer to Docker container registries, plugin registries, or other technical registries unrelated to telecommunications compliance. This represents a risk pattern consistent with non-compliance under 47 CFR §64.1200(c), which mandates checking phone numbers against the National Do Not Call Registry before initiating outbound calls or messages.

**REMEDIATION DIRECTION**

The system needs to implement Do Not Call Registry integration before any outbound calling or messaging functionality is deployed. This should include: (1) API integration with the National Do Not Call Registry to check phone numbers before dialing, (2) maintenance of an internal suppression list for numbers that have opted out, (3) automated checking processes that prevent calls to numbers on either list, and (4) logging and audit trails of all Do Not Call checks performed. These controls must be implemented and tested before the system can legally initiate any outbound telephonic communications.

---

### TCPA-004: Message Frequency Disclosure

**LEGAL QUESTION**

Does the system disclose to consumers the expected frequency of messages before obtaining consent, and does it enforce frequency limits consistent with the disclosed rate, as recommended by CTIA guidelines?

**REGULATORY STANDARD**

CTIA Messaging Principles and Best Practices; TCPA Consent Requirements

**EVIDENCE**

- `.github/instructions/generic/code_comments.instructions.md:158` — `- Start with a capital letter`
- `.github/instructions/generic/ember_hbs.instructions.md:74` — `- **USE SENTENCE CASE**: All HTML headings (`<h1>`, `<h2>`, `<h3>`, etc.) should use sentence case (only first letter ca`
- `.github/instructions/generic/ember_hbs.instructions.md:75` — `- **NO TITLE CASE**: Avoid title case where every major word is capitalized`
- `.github/instructions/generic/golang.instructions.md:13` — `- Use MixedCaps or mixedCaps rather than underscores for multiword names`
- `.github/instructions/generic/golang.instructions.md:93` — `- Understand slice sharing and capacity`
- `.github/instructions/generic/golang.instructions.md:138` — `- Understand escape analysis and stack vs heap allocation`
- `.github/instructions/generic/golang.instructions.md:155` — `- Understand escape analysis and stack vs heap allocation`
- `.github/workflows/test-ci-cleanup.yml:62` — `# we'll fail on actually actionable things in the quota steep afterwards.`
- `.github/workflows/test-ci-cleanup.yml:69` — `check-quotas:`
- `.github/workflows/test-ci-cleanup.yml:92` — `- name: Check AWS Quotas`

**FINDING: 🔴 High Risk**

No evidence was found in the repository indicating message frequency disclosure or frequency limit enforcement mechanisms. The evidence consists entirely of development infrastructure files, coding guidelines, and Docker configurations with no messaging-related functionality present. This represents a risk pattern consistent with non-compliance under CTIA Messaging Principles and TCPA consent requirements, as the system appears to lack any consumer messaging disclosure or frequency control capabilities.

**REMEDIATION DIRECTION**

Implement consumer-facing message frequency disclosure mechanisms that inform users of expected message rates before obtaining consent. Add frequency enforcement controls to track and limit message sending consistent with disclosed rates. Create configuration files or database schemas to store frequency limits per consumer, and implement monitoring systems to ensure actual message delivery does not exceed the disclosed frequency thresholds required by CTIA guidelines.

---

### TCPA-005: Sender Identification in Messages

**LEGAL QUESTION**

Does the system include proper sender identification in all outbound messages, including the identity of the entity sending the message and how to contact them, consistent with TCPA and CTIA requirements?

**REGULATORY STANDARD**

TCPA 47 U.S.C. §227(d); CTIA Messaging Principles

**EVIDENCE**

- `CHANGELOG-v0.md:1121` — `* **Brand New CLI**: Vault has a brand new CLI interface that is significantly`
- `CHANGELOG-v0.md:1661` — `Only)**: A brand new MFA system built on top of Identity allows MFA`
- `ui/app/components/auth/page.hbs:28` — `<div class="brand-icon-large">`
- `ui/app/components/mfa/splash-card.hbs:12` — `<div class="brand-icon-large">`
- `ui/app/services/path-help.js:139` — `// if we have a brand new model`
- `ui/app/styles/components/icon.scss:83` — `.brand-icon-large {`
- `ui/app/templates/vault/error.hbs:8` — `<Icon @name="vault" @size="24" class="brand-icon-large" />`
- `ui/tests/unit/unload-test.js:63` — `editRecord.name = 'Rebrand';`
- `ui/tests/unit/utils/openapi-to-attrs-test.js:60` — `test('it keeps fields the same when there are no brand new fields from OpenAPI', function (assert) {`
- `vault/external_tests/raft/raft_binary/raft_test.go:133` — `// The correct procedure is destroying existing raft-boltdb nodes and starting brand-new`

**FINDING: 🔴 High Risk**

No evidence of sender identification mechanisms for outbound messages was found in the codebase analysis. The evidence shows only UI branding elements and general product documentation, with no implementation of TCPA-required sender identification or contact information inclusion in messaging functionality. This represents a risk pattern consistent with non-compliance under TCPA 47 U.S.C. §227(d) and CTIA Messaging Principles.

**REMEDIATION DIRECTION**

Implement a comprehensive sender identification system that automatically includes the sending entity's identity and contact information in all outbound messages. This should include creating message templates or headers that contain the organization name, contact phone number, and opt-out instructions as required by TCPA regulations. Add configuration management for sender identification details and ensure all messaging APIs enforce inclusion of this information before message transmission.

---

### TCPA-006: Record Keeping of Consent

**LEGAL QUESTION**

Does the system maintain records of consent that would be sufficient to demonstrate compliance in the event of a dispute, including the date, time, method of consent, and the specific consent language presented to the consumer?

**REGULATORY STANDARD**

TCPA 47 CFR §64.1200; FCC Declaratory Rulings on Consent Records

**EVIDENCE**

- `enos/modules/verify_secrets_engines/modules/read/ldap/ldap.tf:356` — `resource "enos_remote_exec" "ldap_verify_audit_trail" {`
- `enos/modules/verify_secrets_engines/modules/read/ldap/ldap.tf:452` — `enos_remote_exec.ldap_verify_audit_trail`

**FINDING: 🔴 High Risk**

The system exhibits a risk pattern consistent with non-compliance under TCPA 47 CFR §64.1200 and FCC Declaratory Rulings on Consent Records. While the evidence shows audit trail verification capabilities in enos/modules/verify_secrets_engines/modules/read/ldap/ldap.tf at lines 356 and 452, no code was found that specifically captures, stores, or manages consumer consent records with the required elements (date, time, method of consent, and specific consent language presented). The repository appears to be HashiCorp Vault, a secrets management tool, which does not demonstrate consumer-facing consent collection functionality required for TCPA compliance.

**REMEDIATION DIRECTION**

The system would need to implement a comprehensive consent management module that captures and permanently stores consumer consent records including: timestamp of consent, method used to obtain consent (web form, phone, SMS, etc.), the exact consent language displayed to the consumer, and unique identifiers linking consent to specific consumers. This should include database schemas for consent storage, APIs for consent collection, and audit logging specifically for consent-related operations separate from general system audit trails.

---

### TCPA-007: Revocation of Consent Handling

**LEGAL QUESTION**

Does the system honor revocation of consent through any reasonable means indicated by the consumer, not limited to specific keywords, and process revocation within a reasonable timeframe, consistent with FCC guidance?

**REGULATORY STANDARD**

TCPA 47 U.S.C. §227(b)(1)(A); FCC 2015 TCPA Omnibus Declaratory Ruling

**EVIDENCE**

- `.github/actions/build-vault/action.yml:242` — `postremove: .release/linux/postrm`
- `.github/instructions/generic/code_comments.instructions.md:185` — `// Remove leading # from ref path`
- `.github/instructions/generic/code_comments.instructions.md:193` — `const parts = ref.split('/').slice(1); // Remove leading #`
- `.github/instructions/generic/code_comments.instructions.md:196` — `// Remove leading # from ref path`
- `.github/instructions/generic/code_comments.instructions.md:238` — `// TODO: Remove this after migration to v2 API (added 2019)`
- `.github/instructions/generic/code_comments.instructions.md:247` — `- **Remove** comments that add no value`
- `.github/instructions/generic/ember_hbs.instructions.md:15` — `- Remove unnecessary quotes around dynamic component arguments`
- `.github/instructions/generic/ember_hbs.instructions.md:21` — `- Remove quotes around dynamic data attributes: `data-test-id={{value}}` not `data-test-id="{{value}}"``
- `.github/instructions/generic/ember_js.instructions.md:20` — `- Remove all unused imports, variables, and functions before committing`
- `.github/instructions/generic/golang.instructions.md:98` — `- Use `delete(m, key)` to remove entries safely`

**FINDING: 🔴 High Risk**

No evidence found of TCPA consent revocation handling mechanisms in the analyzed codebase. The evidence shows only generic removal operations in development workflows, build scripts, and code maintenance instructions (such as .github/workflows/remove-labels.yml and various instruction files), but contains no implementation of consumer consent revocation processing, keyword detection systems, or timeframe management for TCPA compliance. This represents a risk pattern consistent with non-compliance under TCPA 47 U.S.C. §227(b)(1)(A) and FCC 2015 TCPA Omnibus Declaratory Ruling.

**REMEDIATION DIRECTION**

Implement a comprehensive consent revocation system that can detect and process consumer opt-out requests through multiple channels (SMS keywords, email requests, web forms, phone calls). The system should include natural language processing to recognize various revocation phrases beyond standard keywords like "STOP," maintain an accessible revocation database, and process all revocation requests within a reasonable timeframe (typically within 10 business days per FCC guidance). Include audit logging for all revocation activities and ensure the system can handle revocation requests across all communication channels used by the application.

---

### TCPA-008: Time of Day Restrictions

**LEGAL QUESTION**

Does the system enforce time-of-day restrictions for outbound calls and messages, ensuring they are not sent before 8:00 AM or after 9:00 PM in the recipient's local time zone, as required under 47 CFR §64.1200(c)(1)?

**REGULATORY STANDARD**

TCPA 47 CFR §64.1200(c)(1) (Time of Day Restrictions)

**EVIDENCE**

- `.github/dependabot.yml:6` — `schedule:`
- `.github/instructions/generic/ember_js.instructions.md:90` — `- **WARNING**: Avoid `new Date()` as it uses the browser's timezone`
- `.github/instructions/generic/ember_js.instructions.md:91` — `- Use `Date.UTC()` constructor instead of `new Date()` for consistent timezone handling`
- `.github/workflows/build.yml:13` — `#   * That the workflow must work under when triggered by pull_request, push, schedule, and`
- `.github/workflows/build.yml:32` — `#     under normal pull_request, push, schedule, and workflow_dispatch trigger events.`
- `.github/workflows/build.yml:47` — `#     * The ability to build all of our artifacts on a scheduled cadence to ensure we don't`
- `.github/workflows/build.yml:66` — `schedule:`
- `.github/workflows/build.yml:81` — `#   * The workflow was triggered by on schedule to test building all artifacts.`
- `.github/workflows/build.yml:84` — `github.event_name == 'schedule' ||`
- `.github/workflows/build.yml:272` — `#   * The workflow was triggered by on schedule to test building all artifacts.`

**FINDING: 🔴 High Risk**

No evidence was found of any time-of-day restriction controls for outbound calls or messages in the analyzed code repository. The evidence shows only CI/CD scheduling configurations and timezone handling warnings for JavaScript development, but contains no implementation of TCPA-compliant time restrictions that would prevent communications before 8:00 AM or after 9:00 PM in recipient local time zones. This presents a risk pattern consistent with non-compliance under 47 CFR §64.1200(c)(1).

**REMEDIATION DIRECTION**

Implement time-of-day validation logic that checks recipient local time zones before sending any outbound calls or messages. This should include: (1) recipient timezone detection or storage, (2) current time calculation in recipient's local timezone, (3) validation that the time falls between 8:00 AM and 9:00 PM, and (4) blocking or queuing of communications outside permitted hours. Add automated tests to verify this functionality works correctly across different time zones.

---

**DISCLAIMER:** OpenDocket identifies risk patterns through automated code analysis. Findings represent potential areas of concern, not legal determinations. This report does not constitute legal advice. Regulatory compliance requires qualified legal and technical assessment. Consult a licensed attorney and certified compliance professional for definitive compliance determination.
