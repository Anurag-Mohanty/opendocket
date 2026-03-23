# OpenDocket Compliance Report: hyperswitch

> **Repository:** https://github.com/juspay/hyperswitch
> **Scan Date:** 2026-03-22
> **Scanner Version:** OpenDocket V1

---

**DISCLAIMER:** OpenDocket identifies risk patterns through automated code analysis. Findings represent potential areas of concern, not legal determinations. This report does not constitute legal advice. Regulatory compliance requires qualified legal and technical assessment. Consult a licensed attorney and certified compliance professional for definitive compliance determination.

---

## Domain Detection

- **Fintech** — Confidence: 97.2% (216894 signals, top: payment, card, merchant, refund, transaction)
- **Saas** — Confidence: 92.2% (27676 signals, top: auth, billing, stripe, tenant, organization)
- **Ecommerce** — Confidence: 76.4% (9738 signals, top: shipping, order, checkout, product, fulfillment)
- **Communication** — Confidence: 34.0% (2688 signals, top: call, phone_number, notification, consent, sms)
- **Healthcare** — Confidence: 16.5% (1154 signals, top: provider, rx, medical, encounter, cpt)
- **Gdpr** — Confidence: 8.3% (47 signals, top: consent, gdpr)
- **Sox** — Confidence: 5.8% (2 signals, top: audit_trail)

## Frameworks Analyzed: GDPR, HIPAA, PCI-DSS, SOC2, SOX, TCPA

## Executive Summary

| Finding Level | Count |
|---|---|
| High Risk | 45 |
| Medium Risk | 6 |
| Pattern of Concern | 4 |
| No Issue Found | 1 |

## GDPR Findings

### GDPR-001: Lawful Basis for Processing Personal Data

**LEGAL QUESTION**

Does this system process personal data of EU residents, and if so, is there evidence that a lawful basis for processing under Article 6 GDPR has been identified and implemented for each processing activity?

**REGULATORY STANDARD**

GDPR Article 6 (Lawfulness of Processing)

**EVIDENCE**

- `add_connector.md:34` — `* Enforce PII best practices (Secret wrappers, common\_utils::pii types) and robust error-handling`
- `api-reference/locker-api-reference/overview.mdx:5` — `Hyperswitch Card Vault is built with a GDPR compliant personal identifiable information (PII) storage and secure encrypt`
- `api-reference/locker-api-reference/overview.mdx:5` — `Hyperswitch Card Vault is built with a GDPR compliant personal identifiable information (PII) storage and secure encrypt`
- `aws/beta_schema.sql:1545` — `-- File: migrations/2023-04-11-084958_pii-migration/up.sql`
- `aws/hyperswitch_aws_setup.sh:210` — `cat << EOF > user_data.sh`
- `aws/hyperswitch_aws_setup.sh:256` — `echo "\n# Add redis and DB configs.\n" >> user_data.sh`
- `aws/hyperswitch_aws_setup.sh:257` — `echo "cat << EOF >> .env" >> user_data.sh`
- `aws/hyperswitch_aws_setup.sh:258` — `echo "ROUTER__REDIS__HOST=$REDIS_ENDPOINT" >> user_data.sh`
- `aws/hyperswitch_aws_setup.sh:259` — `echo "ROUTER__MASTER_DATABASE__HOST=$RDS_ENDPOINT" >> user_data.sh`
- `aws/hyperswitch_aws_setup.sh:260` — `echo "ROUTER__REPLICA_DATABASE__HOST=$RDS_ENDPOINT" >> user_data.sh`

**FINDING: 🔴 High Risk**

The evidence shows this system processes personal data of EU residents through card vault operations and PII handling (api-reference/locker-api-reference/overview.mdx:5, add_connector.md:34), but no evidence was found of identified lawful bases for processing under GDPR Article 6. While the system claims "GDPR compliant personal identifiable information (PII) storage," compliance claims alone do not satisfy the requirement to identify and implement specific lawful bases for each processing activity. This creates a risk pattern consistent with non-compliance under GDPR Article 6.

**REMEDIATION DIRECTION**

The development team must conduct a comprehensive data processing inventory to identify all personal data processing activities, determine the appropriate lawful basis under Article 6 GDPR for each activity (such as consent, contract performance, legitimate interests, etc.), and implement clear documentation and technical controls that demonstrate the lawful basis for each processing operation. This should include updating privacy policies, consent mechanisms where applicable, and ensuring the codebase reflects the identified lawful bases through appropriate data handling procedures.

---

### GDPR-002: Consent Collection and Management

**LEGAL QUESTION**

Does the system implement consent collection mechanisms that satisfy the conditions for consent under Article 7, including freely given, specific, informed, and unambiguous indication of the data subject's wishes, with capability to withdraw consent?

**REGULATORY STANDARD**

GDPR Article 7 (Conditions for Consent)

**EVIDENCE**

- `.github/workflows/hotfix-pr-check.yml:66` — `is_pull_request="$(gh api -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" "/repos/juspay/`
- `.github/workflows/pr-convention-checks.yml:9` — `# acceptable use of this trigger.`
- `.github/workflows/pr-convention-checks.yml:155` — `files_changed="$(gh api --header "Accept: application/vnd.github+json" --header "X-GitHub-Api-Version: 2022-11-28" --pag`
- `.github/workflows/release-stable-version.yml:66` — `--header 'Accept: application/vnd.github+json' \`
- `.github/workflows/release-stable-version.yml:130` — `--header 'Accept: application/vnd.github+json' \`
- `.github/workflows/release-stable-version.yml:143` — `--header 'Accept: application/vnd.github+json' \`
- `LICENSE:136` — `the terms of any separate license agreement you may have executed`
- `LICENSE:145` — `agreed to in writing, Licensor provides the Work (and each`
- `LICENSE:157` — `negligent acts) or agreed to in writing, shall any Contributor be`
- `LICENSE:172` — `of any other Contributor, and only if You agree to indemnify,`

**FINDING: 🔴 High Risk**

No evidence was found of consent collection mechanisms that satisfy GDPR Article 7 requirements for freely given, specific, informed, and unambiguous consent with withdrawal capability. The evidence consists entirely of GitHub API calls, license text, and documentation references that do not implement or demonstrate any consent management functionality required for GDPR compliance.

**REMEDIATION DIRECTION**

Implement a comprehensive consent management system that includes: (1) clear consent collection interfaces with specific opt-in checkboxes for different data processing purposes, (2) plain language privacy notices explaining what data is collected and how it's used, (3) mechanisms for users to withdraw consent as easily as they gave it, (4) audit logging of all consent actions with timestamps, and (5) regular consent refresh workflows. The system should store consent preferences per user and respect withdrawal requests immediately across all data processing activities.

---

### GDPR-003: Right to Erasure Implementation

**LEGAL QUESTION**

Does the system implement the right to erasure (right to be forgotten) under Article 17, allowing data subjects to request deletion of their personal data without undue delay?

**REGULATORY STANDARD**

GDPR Article 17 (Right to Erasure)

**EVIDENCE**

- `connector-template/mod.rs:593` — `) -> CustomResult<Box<dyn hyperswitch_masking::ErasedMaskSerialize>, errors::ConnectorError> {`
- `crates/common_utils/src/request.rs:68` — `Json(Box<dyn hyperswitch_masking::ErasedMaskSerialize + Send>),`
- `crates/common_utils/src/request.rs:69` — `FormUrlEncoded(Box<dyn hyperswitch_masking::ErasedMaskSerialize + Send>),`
- `crates/common_utils/src/request.rs:73` — `Box<dyn hyperswitch_masking::ErasedMaskSerialize + Send>,`
- `crates/common_utils/src/request.rs:76` — `Xml(Box<dyn hyperswitch_masking::ErasedMaskSerialize + Send>),`
- `crates/diesel_models/src/query/dashboard_metadata.rs:120` — `pub async fn delete_user_scoped_dashboard_metadata_by_merchant_id_data_key(`
- `crates/euclid/src/dssa/state_machine.rs:117` — `fn destroy(&self, context: &mut types::ConjunctiveContext<'a>) {`
- `crates/euclid/src/dssa/state_machine.rs:196` — `fn destroy(&self, context: &mut types::ConjunctiveContext<'a>) {`
- `crates/euclid/src/dssa/state_machine.rs:197` — `self.condition_machine.destroy(context);`
- `crates/euclid/src/dssa/state_machine.rs:317` — `last.destroy(context);`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under GDPR Article 17 (Right to Erasure). While the codebase contains technical data masking capabilities (ErasedMaskSerialize implementations across multiple connector files) and some deletion functions (delete_user_scoped_dashboard_metadata_by_merchant_id_data_key at crates/diesel_models/src/query/dashboard_metadata.rs:120), there is no evidence of a complete right to erasure implementation that would allow data subjects to request deletion of their personal data without undue delay as required by Article 17.

**REMEDIATION DIRECTION**

Implement a comprehensive right to erasure system that includes: (1) a user-facing mechanism for data subjects to submit deletion requests, (2) automated workflows to process these requests within the required timeframes, (3) comprehensive data deletion across all storage systems including databases, logs, and backups, (4) verification and audit capabilities to confirm complete erasure, and (5) proper handling of exceptions where deletion may not be required (such as legal compliance). The existing masking infrastructure can be leveraged, but a complete end-to-end erasure process must be built on top of it.

---

### GDPR-004: Data Portability Capability

**LEGAL QUESTION**

Does the system provide data subjects the right to receive their personal data in a structured, commonly used, and machine-readable format, and to transmit that data to another controller, as required under Article 20?

**REGULATORY STANDARD**

GDPR Article 20 (Right to Data Portability)

**EVIDENCE**

- `.dockerignore:72` — `com_crashlytics_export_strings.xml`
- `.dockerignore:80` — `# Android studio 3.1+ serialized cache file`
- `.github/workflows/cypress-tests-runner.yml:1029` — `export ${CONNECTOR_ENV_VAR}="http://localhost:3010/${connector}"`
- `.github/workflows/postman-collection-runner.yml:164` — `export PATH=${NEWMAN_PATH}:${PATH}`
- `.github/workflows/release-nightly-version.yml:61` — `export PATH="${NEWMAN_PATH}:${PATH}"`
- `.github/workflows/release-stable-version.yml:152` — `export GIT_CLIFF__GIT__TAG_PATTERN='v[0-9]*'`
- `.gitignore:72` — `com_crashlytics_export_strings.xml`
- `.gitignore:80` — `# Android studio 3.1+ serialized cache file`
- `Dockerfile:55` — `# args for deciding the executable to export. three binaries:`
- `LICENSE:188` — `identification within third-party archives.`

**FINDING: 🔴 High Risk**

No evidence of data portability functionality was found in the codebase. The evidence shows only generic export statements for development configuration and build processes, with no implementation of user data export capabilities in structured, machine-readable formats. This presents a risk pattern consistent with non-compliance under GDPR Article 20, as the system appears to lack the required capability for data subjects to receive and transmit their personal data to other controllers.

**REMEDIATION DIRECTION**

Implement a data portability feature that allows users to request and receive their personal data in structured formats like JSON, CSV, or XML. This should include an API endpoint for programmatic data export, a user interface for self-service data requests, and backend functionality to compile all personal data associated with a user account. The export should include all personal data categories processed by the system and provide the data in a format that can be easily imported by other data controllers.

---

### GDPR-005: Privacy by Design Evidence

**LEGAL QUESTION**

Does the system demonstrate evidence of data protection by design and by default, implementing appropriate technical and organizational measures to ensure only necessary personal data is processed, as required under Article 25?

**REGULATORY STANDARD**

GDPR Article 25 (Data Protection by Design and by Default)

**EVIDENCE**

- `.dockerignore:216` — `Thumbs.db:encryptable`
- `.github/workflows/archive/connector-ui-sanity-tests.yml:85` — `- name: Download Encrypted TOML from S3 and Decrypt`
- `.github/workflows/cypress-tests-runner.yml:283` — `- name: Download Encrypted TOML from S3 and Decrypt`
- `.github/workflows/cypress-tests-runner.yml:483` — `- name: Download Encrypted TOML from S3 and Decrypt`
- `.github/workflows/cypress-tests-runner.yml:747` — `- name: Download Encrypted TOML from S3 and Decrypt`
- `.github/workflows/cypress-tests-runner.yml:1122` — `- name: Download Encrypted TOML from S3 and Decrypt`
- `.github/workflows/postman-collection-runner.yml:54` — `- name: Download Encrypted TOML from S3 and Decrypt`
- `.gitignore:216` — `Thumbs.db:encryptable`
- `.typos.toml:111` — `encrypter = "encrypter" # Used by the `ring` crate`
- `README.md:81` — `Route each transaction to the PSP with the highest predicted auth rate. Reduce retries, avoid downtime, and minimize lat`

**FINDING: 🟠 Medium Risk**

The evidence shows technical encryption measures are implemented (JWE/JWS encryption in locker-v2.yml, encrypted TOML handling in CI/CD workflows, and multi-key encryption architecture), and there is explicit GDPR compliance documentation stating the Card Vault is "GDPR compliant personal identifiable information (PII) storage." However, the evidence lacks demonstration of data minimization controls, purpose limitation mechanisms, or privacy-by-default configurations that would fully satisfy Article 25's requirements for processing only necessary personal data.

**REMEDIATION DIRECTION**

Implement and document data minimization controls such as automated data retention policies, purpose-based data collection limits, and privacy-by-default configuration settings. Add code-level evidence of data processing limitations, such as field-level access controls, automated data purging mechanisms, and configuration files that default to minimal data collection. Document technical measures that ensure only necessary personal data fields are processed for each specific business purpose, and implement audit trails showing compliance with data minimization principles.

---

### GDPR-006: Data Breach Detection and Notification

**LEGAL QUESTION**

Does the system implement mechanisms for detecting personal data breaches and notifying the supervisory authority within 72 hours and affected data subjects without undue delay, as required under Articles 33 and 34?

**REGULATORY STANDARD**

GDPR Articles 33 (Notification to Authority); 34 (Communication to Data Subject)

**EVIDENCE**

- `.dockerignore:251` — `monitoring/*.tmp/`
- `.github/CODEOWNERS:155` — `monitoring/ @juspay/hyperswitch-infra`
- `.gitignore:252` — `monitoring/*.tmp/`
- `LICENSE:159` — `incidental, or consequential damages of any character arising as a`
- `README.md:113` — `- **Full**: Includes monitoring + schedulers`
- `add_connector.md:1086` — `- **Webhook configuration**: For handling asynchronous payment notifications`
- `api-reference/essentials/go-live.mdx:32` — `- [ ] [Configure your webhook endpoint](https://juspay-78.mintlify.app/essentials/webhooks#configuring-webhooks) on our `
- `api-reference/essentials/rate_limit.mdx:17` — `- To proactively manage these errors, monitoring tools can help track usage patterns and provide insights for adjusting `
- `aws/hyperswitch_aws_setup.sh:298` — `--monitoring "Enabled=false" \`
- `config/config.example.toml:1334` — `monitoring_threshold_in_seconds = 60  # 60 secs , threshold for monitoring the retry system`

**FINDING: 🔴 High Risk**

The evidence reveals a risk pattern consistent with non-compliance under GDPR Articles 33 and 34. While general monitoring infrastructure exists (config files show monitoring thresholds and Grafana alerting configurations), there is no specific implementation found for detecting personal data breaches or automated notification mechanisms to supervisory authorities within 72 hours or to affected data subjects. The monitoring systems appear focused on operational metrics rather than data breach detection and notification requirements.

**REMEDIATION DIRECTION**

Implement dedicated personal data breach detection mechanisms that can identify unauthorized access, disclosure, or loss of personal data. Create automated notification workflows that can alert supervisory authorities within 72 hours and notify affected data subjects without undue delay. This should include breach severity assessment logic, notification templates, contact management systems for authorities and data subjects, and audit logging of all breach notifications. The existing monitoring infrastructure in Grafana could be extended to include data breach detection rules and automated notification capabilities.

---

### GDPR-007: Data Retention and Deletion Policies

**LEGAL QUESTION**

Does the system implement data retention policies that limit the storage of personal data to what is necessary for the specified processing purpose, with automated deletion or anonymization when the purpose is fulfilled, consistent with the storage limitation principle under Article 5(1)(e)?

**REGULATORY STANDARD**

GDPR Article 5(1)(e) (Storage Limitation Principle)

**EVIDENCE**

- `.github/PULL_REQUEST_TEMPLATE.md:39` — `that will have little conversation).`
- `.github/workflows/archive/connector-sanity-tests.yml:9` — `- cron: "5 0 * * *"`
- `.github/workflows/cypress-tests-runner.yml:151` — `retention-days: 1`
- `.github/workflows/cypress-tests-runner.yml:209` — `retention-days: 1`
- `.github/workflows/cypress-tests-runner.yml:402` — `retention-days: 1`
- `.github/workflows/cypress-tests-runner.yml:606` — `retention-days: 1`
- `.github/workflows/cypress-tests-runner.yml:615` — `retention-days: 1`
- `.github/workflows/cypress-tests-runner.yml:857` — `retention-days: 1`
- `.github/workflows/cypress-tests-runner.yml:866` — `retention-days: 1`
- `.github/workflows/cypress-tests-runner.yml:1074` — `retention-days: 1`

**FINDING: 🔴 High Risk**

The evidence reveals a risk pattern consistent with non-compliance under GDPR Article 5(1)(e) storage limitation principle. While GitHub workflow files show automated retention policies for test artifacts (1-day retention in cypress-tests-runner.yml lines 151, 209, 402, 606, 615, 857, 866, 1074, 1281), there is no evidence of data retention policies or automated deletion mechanisms for personal data processed by the core payment system itself. The repository lacks implementation of data retention controls that would limit storage of personal data to what is necessary for specified processing purposes.

**REMEDIATION DIRECTION**

Implement comprehensive data retention policies for all personal data processed by the payment system. This should include: (1) defining retention periods for different types of personal data based on processing purposes, (2) implementing automated deletion or anonymization processes when retention periods expire, (3) creating database cleanup jobs or scheduled tasks that regularly purge expired personal data, and (4) documenting these policies in code comments and configuration files. Consider adding data lifecycle management modules that can track data age and automatically trigger deletion when legal or business retention requirements are met.

---

### GDPR-008: Cross-Border Data Transfer Safeguards

**LEGAL QUESTION**

Does the system implement appropriate safeguards for transfers of personal data to third countries or international organizations, such as Standard Contractual Clauses or adequacy decisions, as required under Chapter V?

**REGULATORY STANDARD**

GDPR Chapter V, Articles 44-49 (Transfers to Third Countries)

**EVIDENCE**

- `.github/workflows/CI-pr.yml:90` — `# Use `sccache` for caching compilation artifacts`
- `.github/workflows/CI-pr.yml:91` — `# RUSTC_WRAPPER: sccache`
- `.github/workflows/CI-pr.yml:141` — `# Use `sccache` for caching compilation artifacts`
- `.github/workflows/CI-pr.yml:142` — `# RUSTC_WRAPPER: sccache`
- `.github/workflows/CI-push.yml:60` — `# Use `sccache` for caching compilation artifacts`
- `.github/workflows/CI-push.yml:61` — `# RUSTC_WRAPPER: sccache`
- `.github/workflows/CI-push.yml:96` — `# - name: Install sccache`
- `.github/workflows/CI-push.yml:99` — `#     tool: sccache`
- `.github/workflows/CI-push.yml:158` — `# Use `sccache` for caching compilation artifacts`
- `.github/workflows/CI-push.yml:159` — `# RUSTC_WRAPPER: sccache`

**FINDING: 🔴 High Risk**

No evidence found of appropriate safeguards for cross-border data transfers as required under GDPR Chapter V. The evidence shows extensive references to AWS infrastructure deployment across multiple regions (us-east-1, us-east-2, eu-central-1) in configuration files and setup scripts, indicating international data transfers, but contains no implementation of Standard Contractual Clauses, adequacy decisions, or other legal transfer mechanisms. This represents a risk pattern consistent with non-compliance under GDPR Articles 44-49.

**REMEDIATION DIRECTION**

Implement appropriate transfer safeguards before any cross-border personal data processing. This requires: (1) conducting a transfer impact assessment to identify all international data flows, (2) implementing Standard Contractual Clauses with data processors/recipients in third countries, (3) documenting adequacy decisions where applicable, (4) adding configuration parameters to enforce transfer restrictions, and (5) creating data processing agreements that specify transfer safeguards. Update the AWS deployment scripts and configuration files to include transfer mechanism validation before processing personal data across regions.

---

### GDPR-009: Data Protection Impact Assessment Indicators

**LEGAL QUESTION**

Does the system process personal data in a manner likely to result in high risk to data subjects, and if so, is there evidence that a Data Protection Impact Assessment has been considered, as required under Article 35?

**REGULATORY STANDARD**

GDPR Article 35 (Data Protection Impact Assessment)

**EVIDENCE**

- `LICENSE:58` — `and issue tracking systems that are managed by, or on behalf of, the`
- `aws/beta_schema.sql:487` — `tracking_data JSON NOT NULL,`
- `config/grafana.ini:212` — `# Google Analytics universal tracking code, only enabled if you specify an id here`
- `config/redis.conf:819` — `############################### KEYS TRACKING #################################`
- `config/redis.conf:829` — `# When tracking is enabled for a client, all the read only queries are assumed`
- `config/redis.conf:850` — `# Note: when key tracking is used in broadcasting mode, no memory is used`
- `config/redis.conf:853` — `# tracking-table-max-keys 1000000`
- `config/redis.conf:1842` — `################################ LATENCY TRACKING ##############################`
- `config/redis.conf:1850` — `# latency-tracking yes`
- `config/redis.conf:1854` — `# latency-tracking-info-percentiles 50 99 99.9`

**FINDING: 🔴 High Risk**

The system processes personal data through multiple tracking mechanisms including tracking_data JSON fields (aws/beta_schema.sql:487), Google Analytics integration (config/grafana.ini:212), and shipping tracking numbers for disputes (crates/api_models/src/disputes.rs:226), which collectively present a risk pattern consistent with non-compliance under GDPR Article 35. No evidence of a Data Protection Impact Assessment (DPIA) was found in the repository despite clear indicators of high-risk processing activities that would likely require such an assessment.

**REMEDIATION DIRECTION**

Conduct a formal Data Protection Impact Assessment to evaluate the risks associated with the tracking systems, analytics integration, and personal data processing workflows identified in the codebase. Document the DPIA process, findings, and any necessary safeguards or mitigation measures. Consider whether the current data processing activities require additional consent mechanisms or privacy controls, and ensure the DPIA documentation is maintained alongside the code repository for compliance verification.

---

### GDPR-010: Privacy Policy and Notice Requirements

**LEGAL QUESTION**

Does the system provide transparent information to data subjects about the processing of their personal data, including identity of the controller, purposes of processing, and data subject rights, as required under Articles 13 and 14?

**REGULATORY STANDARD**

GDPR Articles 13 (Information at Collection); 14 (Information Not from Data Subject)

**EVIDENCE**

- `.devcontainer/devcontainer.json:23` — `// Use 'forwardPorts' to make a list of ports inside the container available locally.`
- `.devcontainer/devcontainer.json:24` — `"forwardPorts": [8080]`
- `.dockerignore:179` — `# More information here https://doc.rust-lang.org/cargo/guide/cargo-toml-vs-cargo-lock.html`
- `.dockerignore:185` — `# MSVC Windows builds of rustc generate these, which store debugging information`
- `.github/CODEOWNERS:54` — `crates/hyperswitch_domain_models/src/connector_endpoints.rs @juspay/hyperswitch-connector`
- `.github/CODEOWNERS:8` — `NOTICE @juspay/hyperswitch-maintainers`
- `.github/ISSUE_TEMPLATE/bug_report.yml:67` — `description: Provide information about the environment where you are running or trying to build the app.`
- `.github/api-migration-compatibility/.oasdiff-severity-levels.yaml:60` — `endpoint-deprecated: WARN`
- `.github/api-migration-compatibility/.oasdiff-severity-levels.yaml:61` — `endpoint-reactivated: INFO`
- `.github/git-cliff-changelog.toml:58` — `{ pattern = "(\\n?Co-authored-by: .+ <.+@.+>\\n?)+", replace = "" }, # remove co-author information`

**FINDING: 🔴 High Risk**

No evidence found of privacy notices, data processing transparency information, or data subject rights disclosures required under GDPR Articles 13 and 14. The repository contains only development configuration files, workflow definitions, and basic project documentation without any privacy policy implementation, data controller identification, or processing purpose declarations. This represents a risk pattern consistent with non-compliance under GDPR Articles 13 and 14.

**REMEDIATION DIRECTION**

Implement comprehensive privacy notices that include: (1) clear identification of the data controller (Juspay/Hyperswitch), (2) specific purposes for processing personal data, (3) legal basis for processing, (4) data retention periods, (5) complete data subject rights information including access, rectification, erasure, and portability rights, (6) contact information for data protection inquiries, and (7) information about data transfers to third parties. These notices must be prominently displayed in the application interface and easily accessible to users at the point of data collection and in account/profile sections.

---

## HIPAA Findings

### HIPAA-001: PHI Identification and Protection

**LEGAL QUESTION**

Does this system collect, store, process, or transmit individually identifiable health information as defined under 45 CFR §160.103, and if so, are adequate technical safeguards in place to protect the confidentiality of such Protected Health Information?

**REGULATORY STANDARD**

HIPAA Privacy Rule 45 CFR §160.103; Security Rule 45 CFR §164.312(a)(1)

**EVIDENCE**

- `.typos.toml:18` — `AGS = "AGS" # philippines state abbreviation`
- `.typos.toml:19` — `AgusanDelSur = "AgusanDelSur" # philippines state abbreviation`
- `.typos.toml:20` — `CamarinesSur = "CamarinesSur" # philippines state abbreviation`
- `.typos.toml:21` — `DavaoDelSur = "DavaoDelSur" # philippines state abbreviation`
- `.typos.toml:22` — `IlocosSur = "IlocosSur" # philippines state abbreviation`
- `.typos.toml:23` — `LanaoDelSur = "LanaoDelSur" # philippines state abbreviation`
- `.typos.toml:24` — `MaguindanaoDelSur = "MaguindanaoDelSur" # philippines state abbreviation`
- `.typos.toml:25` — `SurigaoDelSur = "SurigaoDelSur" # philippines state abbreviation`
- `.typos.toml:18` — `AGS = "AGS" # philippines state abbreviation`
- `.typos.toml:19` — `AgusanDelSur = "AgusanDelSur" # philippines state abbreviation`

**FINDING: 🟢 No Issue Found**

The evidence provided consists primarily of Philippines geographic location data in a typos configuration file (.typos.toml) and binary image data from API documentation. No Protected Health Information (PHI) as defined under 45 CFR §160.103 was identified in the code repository evidence. The system appears to be a payments infrastructure platform based on the README excerpt, with no apparent health information processing capabilities detected in the analyzed files.

**REMEDIATION DIRECTION**

No immediate remediation required based on current evidence. However, if this payments system will process health-related transactions or integrate with healthcare providers in the future, conduct a comprehensive HIPAA risk assessment to identify potential PHI touchpoints and implement appropriate technical safeguards under 45 CFR §164.312(a)(1) including access controls, encryption, and audit logging mechanisms.

---

### HIPAA-002: Encryption at Rest

**LEGAL QUESTION**

Is electronic Protected Health Information encrypted when stored at rest using methods consistent with NIST Special Publication 800-111, as required for addressable implementation under the HIPAA Security Rule?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.312(a)(2)(iv); NIST SP 800-111

**EVIDENCE**

- `.dockerignore:216` — `Thumbs.db:encryptable`
- `.github/workflows/archive/connector-ui-sanity-tests.yml:85` — `- name: Download Encrypted TOML from S3 and Decrypt`
- `.github/workflows/archive/connector-ui-sanity-tests.yml:85` — `- name: Download Encrypted TOML from S3 and Decrypt`
- `.github/workflows/cypress-tests-runner.yml:283` — `- name: Download Encrypted TOML from S3 and Decrypt`
- `.github/workflows/cypress-tests-runner.yml:483` — `- name: Download Encrypted TOML from S3 and Decrypt`
- `.github/workflows/cypress-tests-runner.yml:747` — `- name: Download Encrypted TOML from S3 and Decrypt`
- `.github/workflows/cypress-tests-runner.yml:1122` — `- name: Download Encrypted TOML from S3 and Decrypt`
- `.github/workflows/cypress-tests-runner.yml:20` — `OPTIONAL_PAYMENTS_CONNECTORS_BATCH_1: "cryptopay finix nexixpay"`
- `.github/workflows/cypress-tests-runner.yml:283` — `- name: Download Encrypted TOML from S3 and Decrypt`
- `.github/workflows/cypress-tests-runner.yml:483` — `- name: Download Encrypted TOML from S3 and Decrypt`

**FINDING: 🔴 High Risk**

Evidence shows a risk pattern consistent with non-compliance under HIPAA Security Rule 45 CFR §164.312(a)(2)(iv) and NIST SP 800-111. While some encryption activity is present (encrypted TOML files in S3), no clear evidence demonstrates that PHI stored at rest uses NIST-compliant encryption methods. Multiple anti-patterns were detected including plaintext connections (config/docker_compose.toml:1320), base64 encoding references for credentials (crates/api_models/src/admin.rs:1253-1255), and plaintext API key handling (crates/api_models/src/api_keys.rs:50), which undermine encryption at rest requirements.

**REMEDIATION DIRECTION**

Implement NIST SP 800-111 compliant encryption for all PHI stored at rest, including database encryption using AES-256 or equivalent approved algorithms. Replace plaintext connection configurations with encrypted alternatives, ensure all sensitive data uses proper encryption rather than base64 encoding, and establish key management procedures that meet NIST standards. Document encryption implementations and conduct verification that all PHI storage locations use appropriate cryptographic controls before processing any protected health information.

---

### HIPAA-003: Encryption in Transit

**LEGAL QUESTION**

Are all transmissions of electronic Protected Health Information encrypted using transport-level security consistent with NIST guidelines, preventing unauthorized access during transmission across electronic communications networks?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.312(e)(1); 45 CFR §164.312(e)(2)(ii)

**EVIDENCE**

- `.devcontainer/devcontainer.json:1` — `// For format details, see https://aka.ms/devcontainer.json. For config options, see the`
- `.devcontainer/devcontainer.json:2` — `// README at: https://github.com/devcontainers/templates/tree/main/src/docker-existing-dockerfile`
- `.devcontainer/devcontainer.json:20` — `// Features to add to the dev container. More info: https://containers.dev/features.`
- `.devcontainer/devcontainer.json:32` — `// Uncomment to connect as an existing user other than the container default. More info: https://aka.ms/dev-containers-n`
- `.dockerignore:1` — `# Created by https://www.toptal.com/developers/gitignore/api/rust,visualstudiocode,clion,dotenv,direnv,linux,macos,windo`
- `.dockerignore:2` — `# Edit at https://www.toptal.com/developers/gitignore?templates=rust,visualstudiocode,clion,dotenv,direnv,linux,macos,wi`
- `.dockerignore:6` — `# Reference: https://intellij-support.jetbrains.com/hc/en-us/articles/206544839`
- `.dockerignore:84` — `# Comment Reason: https://github.com/joeblau/gitignore.io/issues/186#issuecomment-215987721`
- `.dockerignore:92` — `# https://plugins.jetbrains.com/plugin/7973-sonarlint`
- `.dockerignore:96` — `# https://plugins.jetbrains.com/plugin/7238-sonarqube-community-plugin`

**FINDING: 🔴 High Risk**

No evidence of transport-level encryption implementation was found in the code repository, creating a risk pattern consistent with non-compliance under HIPAA Security Rule 45 CFR §164.312(e)(1) and (e)(2)(ii). Multiple anti-patterns using unencrypted HTTP protocols were detected in CI/CD workflows, specifically in cypress-tests-runner.yml (lines 387, 590, 841, 1055, 1262) and postman-collection-runner.yml (line 155) with "http://localhost" configurations. The repository appears to be a payment processing system that would handle PHI, yet lacks any visible implementation of NIST-compliant encryption in transit.

**REMEDIATION DIRECTION**

Implement transport-level security by configuring HTTPS/TLS encryption for all data transmissions, ensuring compliance with NIST guidelines (such as TLS 1.2 minimum). Replace all HTTP protocol references in configuration files with HTTPS equivalents, implement proper SSL/TLS certificates, and add code that enforces encrypted connections for any PHI transmission. Add configuration files showing TLS implementation, security headers, and certificate management. Include unit tests that verify encryption is properly implemented before any PHI data transmission occurs.

---

### HIPAA-004: Access Controls and Authentication

**LEGAL QUESTION**

Does the system implement technical policies and procedures for electronic information systems that maintain electronic Protected Health Information to allow access only to those persons or software programs that have been granted access rights as specified in 45 CFR §164.312(a)(1)?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.312(a)(1); 45 CFR §164.312(a)(2)(i)

**EVIDENCE**

- `.github/CODEOWNERS:129` — `crates/router/src/services/authentication.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:98` — `crates/api_models/src/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:99` — `crates/api_models/src/events/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:104` — `crates/diesel_models/src/query/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:108` — `crates/diesel_models/src/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:110` — `crates/router/src/consts/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:117` — `crates/router/src/core/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:122` — `crates/router/src/db/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:127` — `crates/router/src/routes/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:141` — `crates/router/src/types/storage/user_role.rs @juspay/hyperswitch-dashboard`

**FINDING: 🟠 Medium Risk**

The evidence shows authentication and user role management components exist (authentication.rs, user_role.rs modules, JWT services), indicating some access control implementation. However, the evidence lacks specific technical safeguards demonstrating restriction of access to only authorized persons or software programs as required. This presents a risk pattern consistent with non-compliance under 45 CFR §164.312(a)(1), as the system's ability to enforce granular access restrictions to electronic PHI cannot be verified from the available code artifacts.

**REMEDIATION DIRECTION**

Implement and document specific technical access controls that demonstrate compliance with HIPAA's access restriction requirements. This should include role-based access control mechanisms with documented permission matrices, authentication logs, and automated access enforcement procedures. The existing user role infrastructure in the codebase provides a foundation, but needs enhancement with explicit PHI access controls, audit trails, and technical procedures that clearly restrict system access to only those persons or software programs granted specific access rights.

---

### HIPAA-005: Session Management

**LEGAL QUESTION**

Does the system implement electronic procedures that terminate an electronic session after a predetermined time of inactivity, as required for PHI-accessing interfaces under the HIPAA Security Rule?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.312(a)(2)(iii)

**EVIDENCE**

- `.github/workflows/CI-pr.yml:28` — `# from transient network timeouts or other issues.`
- `.github/workflows/CI-push.yml:31` — `# from transient network timeouts or other issues.`
- `.github/workflows/archive/connector-sanity-tests.yml:34` — `# from transient network timeouts or other issues.`
- `.github/workflows/archive/connector-sanity-tests.yml:51` — `--health-timeout 5s`
- `.github/workflows/archive/connector-ui-sanity-tests.yml:29` — `# from transient network timeouts or other issues.`
- `.github/workflows/archive/connector-ui-sanity-tests.yml:47` — `--health-timeout 5s`
- `.github/workflows/archive/connector-ui-sanity-tests.yml:60` — `--health-timeout 5s`
- `.github/workflows/cypress-tests-runner.yml:230` — `--health-timeout 5s`
- `.github/workflows/cypress-tests-runner.yml:243` — `--health-timeout 5s`
- `.github/workflows/cypress-tests-runner.yml:430` — `--health-timeout 5s`

**FINDING: 🔴 High Risk**

No evidence of electronic session timeout procedures for PHI-accessing interfaces was found in the codebase. The evidence shows only infrastructure health-check timeouts (5s) and CI/CD network timeout references in GitHub workflow files, which are unrelated to user session management. This represents a risk pattern consistent with non-compliance under HIPAA Security Rule 45 CFR §164.312(a)(2)(iii).

**REMEDIATION DIRECTION**

Implement automatic session timeout functionality for all user interfaces that access PHI. This should include configurable inactivity timers (typically 15-30 minutes), session state monitoring, automatic logout procedures, and clear user notifications before timeout occurs. The implementation should be in the application code rather than just infrastructure configurations, and should specifically target user authentication sessions rather than system health checks.

---

### HIPAA-006: Audit Logging

**LEGAL QUESTION**

Does the system implement hardware, software, and procedural mechanisms that record and examine activity in information systems that contain or use electronic Protected Health Information, as required under the audit controls standard?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.312(b)

**EVIDENCE**

- `Makefile:25` — `audit \`
- `README.md:69` — `Advanced observability tools to audit, monitor, and optimize your payment costs. Detect hidden fees, downgrades, and pen`
- `README.md:85` — `Automate 2-way and 3-way reconciliation with backdated support, staggered scheduling, and customizable outputs. Reduces `
- `add_connector.md:647` — `router_env::logger::info!(connector_response=?response);`
- `add_connector.md:669` — `- Logs the response - Records the connector response for debugging via `event_builder` and `router_env::logger::info!``
- `add_connector.md:765` — `router_env::logger::info!(connector_response=?response);`
- `add_connector.md:837` — `router_env::logger::info!(connector_response=?response);`
- `config/config.example.toml:1187` — `audit_events_topic = "topic"             # Kafka topic to be used for Payment Audit events`
- `config/config.example.toml:98` — `# Logging configuration. Logging can be either to file or console or both.`
- `config/config.example.toml:100` — `# Logging configuration for file logging`

**FINDING: 🔵 Pattern of Concern**

The system shows evidence of audit logging infrastructure including Kafka topics for audit events (config/config.example.toml:1187, config/development.toml:1321), audit trail configuration (config/dashboard.toml:25), and connector response logging (add_connector.md:669). However, the evidence does not demonstrate comprehensive audit controls specifically designed for Protected Health Information access and activities as required, presenting a risk pattern consistent with non-compliance under HIPAA Security Rule 45 CFR §164.312(b).

**REMEDIATION DIRECTION**

Implement comprehensive audit logging mechanisms that specifically capture all access to and activity within systems containing ePHI. This should include user authentication events, data access attempts, modifications, deletions, and system-level security events. Ensure audit logs are tamper-resistant, automatically generated, and include required data elements such as user identification, event type, date/time, success/failure status, and source of access. The existing Kafka-based audit infrastructure appears to be payment-focused and should be extended or supplemented with HIPAA-compliant audit controls that specifically address ePHI handling requirements.

---

### HIPAA-007: Minimum Necessary Access

**LEGAL QUESTION**

Does the system limit the Protected Health Information disclosed or accessed to the minimum necessary to accomplish the intended purpose, consistent with the minimum necessary standard under the Privacy Rule?

**REGULATORY STANDARD**

HIPAA Privacy Rule 45 CFR §164.502(b); 45 CFR §164.514(d)

**EVIDENCE**

- `.dockerignore:80` — `# Android studio 3.1+ serialized cache file`
- `.dockerignore:35` — `# When using Gradle or Maven with auto-import, you should exclude module files,`
- `.dockerignore:241` — `# hyperswitch Project specific excludes`
- `.dockerignore:207` — `# Support for Project snippet scope`
- `.github/CODEOWNERS:52` — `crates/router/src/configs/defaults/payment_connector_required_fields.rs @juspay/hyperswitch-connector`
- `.github/CODEOWNERS:164` — `crates/router/src/configs/defaults/payout_required_fields.rs @juspay/hyperswitch-payouts`
- `.github/api-migration-compatibility/migration-rules.yaml:53` — `description: "Changing defaults affects new rows only, may cause inconsistency"`
- `.github/api-migration-compatibility/migration-rules.yaml:11` — `drop_column:`
- `.github/api-migration-compatibility/migration-rules.yaml:12` — `pattern: 'DROP\s+COLUMN\s+'`
- `.github/api-migration-compatibility/migration-rules.yaml:13` — `description: "Dropping a column breaks applications expecting it"`

**FINDING: 🔴 High Risk**

No evidence was found in the code repository demonstrating implementation of minimum necessary access controls for Protected Health Information. The evidence consists entirely of configuration files (.dockerignore, CODEOWNERS, migration rules) and documentation that do not contain any access control mechanisms, data filtering logic, or role-based restrictions that would limit PHI disclosure to the minimum necessary standard. This absence of required controls creates a risk pattern consistent with non-compliance under HIPAA Privacy Rule 45 CFR §164.502(b) and §164.514(d).

**REMEDIATION DIRECTION**

Implement role-based access controls that restrict PHI access based on user roles and specific business purposes. Add data filtering mechanisms that automatically limit the amount of PHI returned in API responses based on the requesting user's role and the intended purpose of the request. Create audit logging to track what PHI is accessed by whom and for what purpose. Establish technical safeguards that prevent users from accessing more PHI than necessary to complete their assigned functions.

---

### HIPAA-008: Business Associate Agreements

**LEGAL QUESTION**

Does the system integrate with third-party services that may receive, maintain, or transmit Protected Health Information, and if so, is there evidence that Business Associate Agreement requirements are addressed in the code or configuration?

**REGULATORY STANDARD**

HIPAA Privacy Rule 45 CFR §164.502(e); 45 CFR §164.504(e)

**EVIDENCE**

- `.dockerignore:15` — `# AWS User-specific`
- `.dockerignore:16` — `.idea/**/aws.xml`
- `.dockerignore:113` — `# Azure Toolkit for IntelliJ plugin`
- `.dockerignore:114` — `# https://plugins.jetbrains.com/plugin/8053-azure-toolkit-for-intellij`
- `.dockerignore:115` — `.idea/**/azureSettings.xml`
- `.github/CODEOWNERS:188` — `crates/hyperswitch_connectors/src/connectors/stripe/transformers/connect.rs @juspay/hyperswitch-payouts`
- `.github/CODEOWNERS:31` — `crates/api_models/src/events/ @juspay/hyperswitch-analytics`
- `.github/CODEOWNERS:32` — `crates/api_models/src/events.rs @juspay/hyperswitch-analytics`
- `.github/CODEOWNERS:33` — `crates/api_models/src/analytics/ @juspay/hyperswitch-analytics`
- `.github/CODEOWNERS:34` — `crates/api_models/src/analytics.rs @juspay/hyperswitch-analytics`

**FINDING: 🔴 High Risk**

The evidence shows integration with multiple third-party services including AWS, Azure, and Stripe (as seen in .dockerignore files and gateway configuration data), which may receive, maintain, or transmit Protected Health Information. However, no evidence was found in the code repository of Business Associate Agreement requirements, contractual safeguards, or HIPAA compliance controls for these third-party integrations, creating a risk pattern consistent with non-compliance under HIPAA Privacy Rule 45 CFR §164.502(e) and §164.504(e).

**REMEDIATION DIRECTION**

Implement documentation and configuration management for Business Associate Agreements with all third-party services that may handle PHI. This should include: (1) maintaining copies of executed BAAs in a secure repository location, (2) adding configuration checks or environment variables that verify BAA compliance status before allowing data transmission to third parties, (3) implementing data classification controls to ensure PHI is only sent to covered third-party services, and (4) adding logging/auditing capabilities to track when PHI is shared with business associates. Consider creating a compliance configuration file that maps each third-party integration to its BAA status and required safeguards.

---

### HIPAA-009: Data Retention and Disposal

**LEGAL QUESTION**

Does the system implement policies and procedures to address the final disposition of electronic Protected Health Information and the hardware or electronic media on which it is stored, as well as removal of PHI before media is available for reuse?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.310(d)(2)(i); 45 CFR §164.310(d)(2)(ii)

**EVIDENCE**

- `.dockerignore:127` — `# temporary files which can be created if a process still has a handle open of a deleted file`
- `.github/PULL_REQUEST_TEMPLATE.md:39` — `that will have little conversation).`
- `.github/api-migration-compatibility/migration-rules.yaml:15` — `delete_data:`
- `.github/api-migration-compatibility/migration-rules.yaml:16` — `pattern: 'DELETE\s+FROM\s+'`
- `.github/api-migration-compatibility/migration-rules.yaml:63` — `- delete_data`
- `.github/api-migration-compatibility/migration-rules.yaml:80` — `- delete_data`
- `.github/api-migration-compatibility/migration-rules.yaml:97` — `- delete_data`
- `.github/workflows/cypress-tests-runner.yml:151` — `retention-days: 1`
- `.github/workflows/cypress-tests-runner.yml:209` — `retention-days: 1`
- `.github/workflows/cypress-tests-runner.yml:402` — `retention-days: 1`

**FINDING: 🔴 High Risk**

No evidence was found of implemented policies and procedures for secure disposal of electronic Protected Health Information or media sanitization controls. While the repository contains basic file cleanup operations in .dockerignore and .gitignore for temporary files, and GitHub workflow retention settings (cypress-tests-runner.yml lines 151, 209, 402, etc.), there are no documented data retention policies, secure deletion procedures, or media sanitization controls that would address PHI disposal requirements. This represents a risk pattern consistent with non-compliance under HIPAA Security Rule 45 CFR §164.310(d)(2)(i) and (ii).

**REMEDIATION DIRECTION**

Implement and document comprehensive data retention and disposal policies that specify retention periods for different types of PHI, secure deletion procedures that ensure data cannot be recovered, and media sanitization controls for hardware reuse. Create automated processes for secure PHI deletion at end-of-life, establish procedures for cryptographic key destruction, and implement logging mechanisms to track disposal activities. Document these procedures in policy files within the repository and ensure they cover both logical deletion of data and physical media sanitization before reuse or disposal.

---

### HIPAA-010: Breach Detection and Emergency Access

**LEGAL QUESTION**

Does the system implement procedures for detecting, reporting, and responding to suspected or known security incidents involving electronic Protected Health Information, and does it provide for emergency access to PHI during system disruptions?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.308(a)(6); 45 CFR §164.312(a)(2)(ii)

**EVIDENCE**

- `.dockerignore:143` — `.LSOverride`
- `.dockerignore:182` — `# These are backup files generated by rustfmt`
- `.dockerignore:251` — `monitoring/*.tmp/`
- `.github/CODEOWNERS:155` — `monitoring/ @juspay/hyperswitch-infra`
- `.github/CODEOWNERS:77` — `crates/external_services/src/grpc_client/health_check_client.rs @juspay/hyperswitch-routing`
- `.github/workflows/release-stable-version.yml:151` — `# Override git-cliff tag pattern to only consider SemVer tags`
- `.gitignore:144` — `.LSOverride`
- `.gitignore:182` — `# These are backup files generated by rustfmt`
- `.gitignore:252` — `monitoring/*.tmp/`
- `LICENSE:159` — `incidental, or consequential damages of any character arising as a`

**FINDING: 🔴 High Risk**

Risk pattern consistent with non-compliance under HIPAA Security Rule 45 CFR §164.308(a)(6) and §164.312(a)(2)(ii). The code repository shows minimal evidence of formal security incident detection, reporting, and response procedures for electronic PHI. While monitoring infrastructure exists (monitoring/ directory referenced in .github/CODEOWNERS:155 and webhook configurations mentioned in documentation), there is no evidence of specific incident response workflows, emergency access procedures during system disruptions, or formal breach detection mechanisms required for PHI protection.

**REMEDIATION DIRECTION**

Implement comprehensive security incident response procedures including automated monitoring for PHI access anomalies, formal incident reporting workflows, and documented emergency access protocols. Add incident detection mechanisms that can identify unauthorized PHI access patterns, create emergency access procedures that maintain audit trails during system disruptions, and establish clear escalation paths for suspected breaches. Document all procedures and ensure they are integrated into the existing monitoring infrastructure referenced in the codebase.

---

## PCI-DSS Findings

### PCIDSS-001: Cardholder Data Storage and Protection

**LEGAL QUESTION**

Does this system store, process, or transmit cardholder data including primary account numbers (PAN), and if so, are adequate protections in place to render stored PAN unreadable, as required under PCI DSS Requirement 3.5?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 3.5 (PAN Storage Protection)

**EVIDENCE**

- `.clippy.toml:3` — `allow-panic-in-tests = true`
- `.github/api-migration-compatibility/migration-rules.yaml:19` — `truncate_table:`
- `.github/api-migration-compatibility/migration-rules.yaml:20` — `pattern: 'TRUNCATE\s+'`
- `.github/api-migration-compatibility/migration-rules.yaml:64` — `- truncate_table`
- `.github/api-migration-compatibility/migration-rules.yaml:81` — `- truncate_table`
- `.github/api-migration-compatibility/migration-rules.yaml:98` — `- truncate_table`
- `.github/cocogitto-changelog-template:15` — `{% set from_shorthand = from.id | truncate(length=7, end="") -%}`
- `.github/cocogitto-changelog-template:16` — `{% set to_shorthand = version.id | truncate(length=7, end="") -%}`
- `.github/cocogitto-changelog-template:27` — `{% set shorthand = commit.id | truncate(length=7, end="") -%}`
- `.github/cocogitto-changelog-template:38` — `{% set shorthand = commit.id | truncate(length=7, end="") -%}`

**FINDING: 🔴 High Risk**

This system demonstrates a risk pattern consistent with non-compliance under PCI DSS v4.0 Requirement 3.5. The evidence shows clear cardholder data processing functionality with card storage operations in crates/router/src/core/payment_methods/cards.rs (lines 2717-2723), including plaintext handling of card numbers, expiration dates, and cardholder names. Additionally, the gateway_status_map.csv contains a "clear_pan_possible" field indicating the system has capabilities to access unprotected PAN data, yet no evidence was found of encryption, tokenization, or other PAN protection mechanisms required by the standard.

**REMEDIATION DIRECTION**

Implement strong cryptographic protection for all stored PAN data by encrypting card numbers before storage using industry-standard encryption algorithms with proper key management. Replace the current card storage mechanism in the payment methods module with tokenization or format-preserving encryption. Ensure that any PAN data referenced in configuration files like gateway_status_map.csv is properly protected and that the "clear_pan_possible" functionality is restricted to authorized processes only. Conduct a comprehensive audit of all data flows to identify and remediate any additional locations where PAN may be stored or transmitted in unprotected form.

---

### PCIDSS-002: Encryption of Card Data in Transit and at Rest

**LEGAL QUESTION**

Is cardholder data encrypted using strong cryptography during transmission over open public networks and when stored at rest, consistent with PCI DSS Requirements 3.5 and 4.2?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirements 3.5 (Encryption at Rest); 4.2 (Encryption in Transit)

**EVIDENCE**

- `.devcontainer/devcontainer.json:1` — `// For format details, see https://aka.ms/devcontainer.json. For config options, see the`
- `.devcontainer/devcontainer.json:2` — `// README at: https://github.com/devcontainers/templates/tree/main/src/docker-existing-dockerfile`
- `.devcontainer/devcontainer.json:20` — `// Features to add to the dev container. More info: https://containers.dev/features.`
- `.devcontainer/devcontainer.json:32` — `// Uncomment to connect as an existing user other than the container default. More info: https://aka.ms/dev-containers-n`
- `.dockerignore:216` — `Thumbs.db:encryptable`
- `.dockerignore:1` — `# Created by https://www.toptal.com/developers/gitignore/api/rust,visualstudiocode,clion,dotenv,direnv,linux,macos,windo`
- `.dockerignore:2` — `# Edit at https://www.toptal.com/developers/gitignore?templates=rust,visualstudiocode,clion,dotenv,direnv,linux,macos,wi`
- `.dockerignore:6` — `# Reference: https://intellij-support.jetbrains.com/hc/en-us/articles/206544839`
- `.dockerignore:84` — `# Comment Reason: https://github.com/joeblau/gitignore.io/issues/186#issuecomment-215987721`
- `.dockerignore:92` — `# https://plugins.jetbrains.com/plugin/7973-sonarlint`

**FINDING: 🔴 High Risk**

The evidence shows no implementation of encryption controls for cardholder data at rest or in transit, creating a risk pattern consistent with non-compliance under PCI DSS Requirements 3.5 and 4.2. Additionally, multiple anti-patterns were detected using unencrypted HTTP protocols in test configurations (cypress-tests-runner.yml lines 387, 590, 841, 1055, 1262 and postman-collection-runner.yml line 155), which could expose sensitive payment data during testing or development activities.

**REMEDIATION DIRECTION**

Implement strong encryption (AES-256 or equivalent) for all stored cardholder data and enforce TLS 1.2+ for all network communications handling payment data. Replace all HTTP references in test configurations with HTTPS endpoints, and ensure that any payment processing endpoints use encrypted connections. Add configuration files showing encryption key management, TLS certificate implementation, and database encryption settings. Conduct a comprehensive audit to identify all locations where cardholder data flows through the system and verify encryption controls are properly implemented.

---

### PCIDSS-003: Access Control to Cardholder Data

**LEGAL QUESTION**

Does the system restrict access to cardholder data to only those individuals and systems whose job requires such access, implementing role-based access controls consistent with PCI DSS Requirement 7?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 7 (Restrict Access by Business Need to Know)

**EVIDENCE**

- `.github/CODEOWNERS:98` — `crates/api_models/src/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:99` — `crates/api_models/src/events/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:104` — `crates/diesel_models/src/query/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:108` — `crates/diesel_models/src/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:110` — `crates/router/src/consts/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:117` — `crates/router/src/core/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:122` — `crates/router/src/db/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:127` — `crates/router/src/routes/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:141` — `crates/router/src/types/storage/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:147` — `crates/router/src/utils/user_role.rs @juspay/hyperswitch-dashboard`

**FINDING: 🔵 Pattern of Concern**

The system demonstrates partial implementation of role-based access controls with extensive user_role module structure across multiple code ownership files in .github/CODEOWNERS lines 98-147, indicating organized access control development. However, the evidence lacks concrete implementation details of how cardholder data access is specifically restricted, validated, or enforced through these role-based mechanisms, creating a risk pattern consistent with non-compliance under PCI DSS v4.0 Requirement 7.

**REMEDIATION DIRECTION**

Document and implement specific role-based access controls that explicitly restrict cardholder data access to authorized personnel only. The existing user_role infrastructure should be enhanced with clear access policies, role definitions tied to business need-to-know principles, and technical controls that enforce these restrictions at the data access layer. Provide evidence of access control testing, role assignment procedures, and monitoring mechanisms to ensure cardholder data is protected according to PCI DSS requirements.

---

### PCIDSS-004: Network Segmentation

**LEGAL QUESTION**

Does the system implement network segmentation to isolate the cardholder data environment (CDE) from other network segments, reducing the scope of PCI DSS compliance as described in Requirement 1?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 1 (Network Security Controls)

**EVIDENCE**

- `aws/hyperswitch_aws_setup.sh:167` — `--vpc-security-group-ids $RDS_SG_ID)"`
- `aws/hyperswitch_aws_setup.sh:51` — `echo "Creating Security Group ingress for port 80..."`
- `aws/hyperswitch_aws_setup.sh:53` — `echo "$(aws ec2 authorize-security-group-ingress \`
- `aws/hyperswitch_aws_setup.sh:60` — `echo "Security Group ingress for port 80 CREATED.\n"`
- `aws/hyperswitch_aws_setup.sh:62` — `echo "Creating Security Group ingress for port 22..."`
- `aws/hyperswitch_aws_setup.sh:64` — `echo "$(aws ec2 authorize-security-group-ingress \`
- `aws/hyperswitch_aws_setup.sh:71` — `echo "Security Group ingress for port 22 CREATED.\n"`
- `aws/hyperswitch_aws_setup.sh:92` — `echo "$(aws ec2 authorize-security-group-ingress \`
- `aws/hyperswitch_aws_setup.sh:119` — `echo "$(aws ec2 authorize-security-group-ingress \`
- `aws/hyperswitch_aws_setup.sh:128` — `echo "$(aws ec2 authorize-security-group-ingress \`

**FINDING: 🔴 High Risk**

The evidence reveals a risk pattern consistent with non-compliance under PCI DSS v4.0 Requirement 1. Multiple security group rules in aws/hyperswitch_aws_setup.sh (lines 57, 68, 132) configure ingress with CIDR 0.0.0.0/0, allowing unrestricted internet access to ports 22 (SSH) and 80 (HTTP). No evidence was found of proper network segmentation controls that would isolate cardholder data environment components from other network segments.

**REMEDIATION DIRECTION**

Implement restrictive CIDR blocks instead of 0.0.0.0/0 to limit access to only necessary IP ranges. Create separate VPCs or subnets for the cardholder data environment with dedicated security groups that deny inter-segment communication by default. Configure security group rules to allow only specific required traffic between network segments, and implement additional network controls like NACLs or firewalls to enforce segmentation boundaries. Document the network segmentation architecture and regularly audit security group configurations to ensure CDE isolation is maintained.

---

### PCIDSS-005: Vulnerability Management

**LEGAL QUESTION**

Does the system demonstrate evidence of vulnerability management practices including regular patching, dependency updates, and vulnerability scanning, consistent with PCI DSS Requirement 6?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 6 (Develop and Maintain Secure Systems)

**EVIDENCE**

- `.dockerignore:95` — `# SonarQube Plugin`
- `.dockerignore:96` — `# https://plugins.jetbrains.com/plugin/7238-sonarqube-community-plugin`
- `.dockerignore:83` — `### CLion Patch ###`
- `.dockerignore:168` — `### macOS Patch ###`
- `.dockerignore:202` — `### VisualStudioCode Patch ###`
- `.gitattributes:2` — `*.patch text eol=lf`
- `.github/CODEOWNERS:55` — `crates/router/src/types/api/connector_mapping.rs @juspay/hyperswitch-connector`
- `.github/api-migration-compatibility/migration-rules.yaml:9` — `description: "Dropping a table removes data and breaks existing queries"`
- `.github/api-migration-compatibility/migration-rules.yaml:13` — `description: "Dropping a column breaks applications expecting it"`
- `.github/api-migration-compatibility/migration-rules.yaml:45` — `description: "Dropping an index can significantly impact query performance"`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under PCI DSS v4.0 Requirement 6. While the repository contains references to patching in configuration files (.dockerignore mentions patches, .gitattributes handles patch files), there is no substantive evidence of systematic vulnerability management practices such as automated dependency scanning, regular security updates, or vulnerability assessment workflows. The presence of SonarQube plugin references (.dockerignore:95-96) suggests some code quality tooling may be intended, but no active vulnerability scanning or patch management processes are demonstrated in the CI/CD workflows or configuration files examined.

**REMEDIATION DIRECTION**

Implement comprehensive vulnerability management processes including: automated dependency vulnerability scanning in CI/CD pipelines, regular security updates for all system components and dependencies, documented patch management procedures with defined timelines, and integration of security scanning tools like OWASP Dependency Check or Snyk into the build process. Add GitHub Actions workflows that scan for vulnerabilities on every build and block deployments with critical security issues. Establish regular security assessment schedules and maintain an inventory of all system components with their current patch levels.

---

### PCIDSS-006: Security Testing Evidence

**LEGAL QUESTION**

Does the system implement security testing controls including code review, static analysis, and penetration testing practices, as required under PCI DSS Requirement 6.3 and 11.4?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirements 6.3 (Security Vulnerabilities); 11.4 (Penetration Testing)

**EVIDENCE**

- `.dockerignore:68` — `# SonarLint plugin`
- `.dockerignore:69` — `.idea/sonarlint/`
- `.dockerignore:91` — `# Sonarlint plugin`
- `.dockerignore:92` — `# https://plugins.jetbrains.com/plugin/7973-sonarlint`
- `.dockerignore:93` — `.idea/**/sonarlint/`
- `.dockerignore:68` — `# SonarLint plugin`
- `.dockerignore:69` — `.idea/sonarlint/`
- `.dockerignore:91` — `# Sonarlint plugin`
- `.dockerignore:92` — `# https://plugins.jetbrains.com/plugin/7973-sonarlint`
- `.dockerignore:93` — `.idea/**/sonarlint/`

**FINDING: 🟠 Medium Risk**

Evidence shows partial implementation of static analysis controls through SonarLint/SonarQube tooling (referenced in .dockerignore and .gitignore) and linting processes in GitHub workflows (cypress-tests-runner.yml lines 75-91), creating a risk pattern consistent with non-compliance under PCI DSS Requirements 6.3 and 11.4. However, no evidence was found for formal code review processes or penetration testing practices as required. Anti-patterns detected in crates/hyperswitch_interfaces/src/configs.rs suggest potential security vulnerabilities that should be addressed through comprehensive security testing.

**REMEDIATION DIRECTION**

Implement missing security testing controls by establishing formal code review requirements in pull request workflows, integrating automated static analysis scans (beyond linting) into the CI/CD pipeline, and implementing regular penetration testing procedures with documented results. Address the detected anti-patterns in the configs.rs file through proper code review processes. Document all security testing procedures and ensure they cover vulnerability identification, remediation tracking, and compliance reporting as required by PCI DSS standards.

---

### PCIDSS-007: Audit Logging of Card Data Access

**LEGAL QUESTION**

Does the system implement audit trail mechanisms that record all individual access to cardholder data, all actions taken by any individual with root or administrative privileges, and all access to audit trails, as required under PCI DSS Requirement 10?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 10 (Log and Monitor All Access)

**EVIDENCE**

- `Makefile:25` — `audit \`
- `README.md:69` — `Advanced observability tools to audit, monitor, and optimize your payment costs. Detect hidden fees, downgrades, and pen`
- `README.md:85` — `Automate 2-way and 3-way reconciliation with backdated support, staggered scheduling, and customizable outputs. Reduces `
- `add_connector.md:647` — `router_env::logger::info!(connector_response=?response);`
- `add_connector.md:669` — `- Logs the response - Records the connector response for debugging via `event_builder` and `router_env::logger::info!``
- `add_connector.md:765` — `router_env::logger::info!(connector_response=?response);`
- `add_connector.md:837` — `router_env::logger::info!(connector_response=?response);`
- `config/config.example.toml:1187` — `audit_events_topic = "topic"             # Kafka topic to be used for Payment Audit events`
- `config/config.example.toml:98` — `# Logging configuration. Logging can be either to file or console or both.`
- `config/config.example.toml:100` — `# Logging configuration for file logging`

**FINDING: 🟠 Medium Risk**

The system shows partial implementation of audit logging mechanisms with evidence of audit event topics in configuration files (config/config.example.toml:1187, config/development.toml:1321) and audit trail settings (config/dashboard.toml:25), but lacks clear evidence of comprehensive logging for individual cardholder data access and administrative privilege actions. While connector response logging exists (add_connector.md:647, 669, 765, 837), the evidence does not demonstrate specific audit trails for cardholder data access or root/administrative user activities, creating a risk pattern consistent with non-compliance under PCI DSS Requirement 10.

**REMEDIATION DIRECTION**

Implement comprehensive audit logging that specifically captures: (1) all individual access attempts to cardholder data with user identification, timestamps, and data accessed; (2) all actions performed by users with root or administrative privileges including login attempts, configuration changes, and system modifications; and (3) all access to the audit logs themselves with tamper-evident controls. Ensure the existing Kafka audit events infrastructure is configured to capture these specific event types and verify that logging covers all system components that store, process, or transmit cardholder data.

---

### PCIDSS-008: Key Management Practices

**LEGAL QUESTION**

Does the system implement cryptographic key management procedures including key generation, distribution, storage, rotation, and destruction, consistent with PCI DSS Requirement 3.6 and 3.7?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirements 3.6 (Key Management Procedures); 3.7 (Key Management Policies)

**EVIDENCE**

- `.typos.toml:115` — `kms = "kms" # Key management service`
- `README.md:76` — `- **Vault**`
- `README.md:77` — `A PCI-compliant vault service to store cards, tokens, wallets, and bank credentials. Provides a unified, secure, and reu`
- `README.md:78` — `_[Read more](https://docs.hyperswitch.io/about-hyperswitch/payments-modules/vault)_`
- `README.md:173` — `Hyperswitch is a commercial open-source payments stack purpose-built for scale, flexibility, and developer experience. D`
- `api-reference/assets/images/image.png:151` — `ЃaJjzqySXVj" "4c@j fފU~-8{t#?PhN~8yI|-+B>\a⳦OA&MW_dVXʮ2W}rx۱`]e>[osVvM2[XW6-YD@4TI``
- `api-reference/docs.json:500` — `"group": "Hyperswitch Card Vault",`
- `api-reference/introduction.mdx:19` — `<Card title="Save a payment method" icon="vault" iconType="regular" horizontal={false} href="https://api-reference.hyper`
- `api-reference/locker-api-reference/locker-general-purpose-storage/add-data-in-locker.mdx:2` — `openapi: locker-v2 post /api/v2/vault/add`
- `api-reference/locker-api-reference/locker-general-purpose-storage/delete-data-from-locker.mdx:2` — `openapi: locker-v2 post /api/v2/vault/delete`

**FINDING: 🔴 High Risk**

The system shows a risk pattern consistent with non-compliance under PCI DSS Requirements 3.6 and 3.7. While the evidence indicates a card vault service exists with claims of PCI DSS compliance (api-reference/locker-api-reference/overview.mdx:5), no actual cryptographic key management procedures for generation, distribution, storage, rotation, or destruction are documented or implemented in the codebase. Critical anti-patterns were detected including hardcoded sample keys (config/config.example.toml:145 "master_enc_key = 'sample_key'") and exposed API keys in configuration examples, indicating insufficient key protection controls.

**REMEDIATION DIRECTION**

Implement comprehensive cryptographic key management procedures covering all lifecycle phases required by PCI DSS 3.6/3.7. This includes: documented key generation using cryptographically strong methods, secure key distribution protocols, encrypted key storage with access controls, automated key rotation schedules, and secure key destruction procedures. Remove all hardcoded keys from configuration files and replace with references to secure key management systems. Establish formal key management policies with role-based access controls, audit logging, and regular key lifecycle reviews. All sample configurations should use placeholder values rather than actual key material.

---

### PCIDSS-009: Third Party Service Provider Controls

**LEGAL QUESTION**

Does the system manage third-party service providers that have access to cardholder data with appropriate controls, agreements, and monitoring, consistent with PCI DSS Requirement 12.8?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 12.8 (Third-Party Service Provider Management)

**EVIDENCE**

- `.github/CODEOWNERS:188` — `crates/hyperswitch_connectors/src/connectors/stripe/transformers/connect.rs @juspay/hyperswitch-payouts`
- `.github/CODEOWNERS:184` — `crates/hyperswitch_connectors/src/connectors/adyenplatform/ @juspay/hyperswitch-payouts`
- `.github/CODEOWNERS:185` — `crates/hyperswitch_connectors/src/connectors/adyenplatform.rs @juspay/hyperswitch-payouts`
- `.github/CODEOWNERS:190` — `crates/router/tests/connectors/adyenplatform.rs @juspay/hyperswitch-payouts`
- `.github/PULL_REQUEST_TEMPLATE.md:45` — `Did you write an integration/unit/API test to verify the code changes?`
- `.github/data/cards_info.csv:1` — `card_iin,card_issuer,card_network,card_type,card_subtype,card_issuing_country,bank_code_id,bank_code,country_code,date_c`
- `.github/data/cards_info.csv:7` — `424242,STRIPE PAYMENTS UK LIMITED,Visa,CREDIT,,UNITEDKINGDOM,,,GB,2015-07-22 16:41:32,2025-11-04 15:23:24,Visa`
- `.github/data/gateway_status_map.csv:6` — `stripe,Payment,Authorize,card_declined,Your card was declined.,failure,,do_default,2025-12-02 13:36:57,2026-01-05 19:13:`
- `.github/data/gateway_status_map.csv:7` — `stripe,Payment,CompleteAuthorize,card_declined,Your card was declined.,failure,,do_default,2025-12-08 18:00:44,2026-01-0`
- `.github/data/gateway_status_map.csv:8` — `stripe,Payment,PSync,card_declined,Your card was declined.,failure,,do_default,2025-12-02 13:39:08,2026-01-05 19:13:24,F`

**FINDING: 🔴 High Risk**

The evidence shows integration with third-party payment service providers (Stripe and Adyen) through code connectors and gateway status mappings, indicating these providers likely have access to cardholder data. However, no evidence was found of formal service provider agreements, security assessments, monitoring controls, or compliance validation documentation as required. This represents a risk pattern consistent with non-compliance under PCI DSS Requirement 12.8.

**REMEDIATION DIRECTION**

Implement a comprehensive third-party service provider management program that includes: formal written agreements with security requirements for all payment processors (Stripe, Adyen, etc.), annual PCI compliance validation from each provider, documented security assessments, and ongoing monitoring procedures. Create a service provider inventory, establish incident response coordination protocols, and document all security controls and responsibilities in contractual agreements before processing cardholder data through these integrations.

---

### PCIDSS-010: Incident Response for Card Data Breach

**LEGAL QUESTION**

Does the system implement an incident response plan that addresses suspected or confirmed cardholder data breaches, including detection, containment, and notification procedures, as required under PCI DSS Requirement 12.10?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 12.10 (Incident Response Plan)

**EVIDENCE**

- `.dockerignore:251` — `monitoring/*.tmp/`
- `.github/CODEOWNERS:77` — `crates/external_services/src/grpc_client/health_check_client.rs @juspay/hyperswitch-routing`
- `.github/CODEOWNERS:155` — `monitoring/ @juspay/hyperswitch-infra`
- `.github/PULL_REQUEST_TEMPLATE.md:23` — `Provide links to the files with corresponding changes.`
- `.gitignore:252` — `monitoring/*.tmp/`
- `Dockerfile:52` — `# RUN_ENV decides the corresponding config file to be used`
- `LICENSE:159` — `incidental, or consequential damages of any character arising as a`
- `README.md:113` — `- **Full**: Includes monitoring + schedulers`
- `add_connector.md:1086` — `- **Webhook configuration**: For handling asynchronous payment notifications`
- `add_connector.md:212` — `Each flow type corresponds to specific request/response data structures and connector integration patterns. All flows fo`

**FINDING: 🔴 High Risk**

No evidence of an incident response plan specifically addressing cardholder data breaches was found in the code repository. While monitoring infrastructure exists (as indicated by monitoring/ directory references in .github/CODEOWNERS:155 and configuration files), there are no documented detection, containment, or notification procedures for suspected or confirmed cardholder data breaches. This represents a risk pattern consistent with non-compliance under PCI DSS v4.0 Requirement 12.10.

**REMEDIATION DIRECTION**

Implement a comprehensive incident response plan that specifically addresses cardholder data breaches. This should include: (1) documented procedures for detecting potential cardholder data compromise, (2) containment steps to limit breach impact, (3) notification procedures for relevant parties including payment brands and regulatory bodies, (4) roles and responsibilities during incident response, and (5) regular testing and updates of the plan. The plan should be stored in the repository as documentation and integrated with the existing monitoring infrastructure to enable automated detection capabilities.

---

## SOC2 Findings

### SOC2-001: User Authentication Controls

**LEGAL QUESTION**

Does the system implement logical access security controls over user authentication that are suitably designed and operating effectively to restrict access to authorized users, consistent with the Common Criteria CC6.1 requirement for logical and physical access controls?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC6.1 (Logical and Physical Access Controls)

**EVIDENCE**

- `.github/CODEOWNERS:129` — `crates/router/src/services/authentication.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:132` — `crates/router/src/services/jwt.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:90` — `crates/router/src/core/payments/tokenization.rs @juspay/hyperswitch-payment-methods`
- `.github/git-cliff-changelog.toml:54` — `commit_preprocessors = [`
- `.github/workflows/CI-pr.yml:39` — `- name: Generate a token`
- `.github/workflows/CI-pr.yml:41` — `id: generate_token`
- `.github/workflows/CI-pr.yml:42` — `uses: actions/create-github-app-token@v1`
- `.github/workflows/CI-pr.yml:47` — `- name: Checkout repository with token`
- `.github/workflows/CI-pr.yml:53` — `token: ${{ steps.generate_token.outputs.token }}`
- `.github/workflows/CI-pr.yml:125` — `repo-token: ${{ secrets.GITHUB_TOKEN }}`

**FINDING: 🔴 High Risk**

The evidence reveals a risk pattern consistent with non-compliance under SOC 2 Trust Services Criteria CC6.1. While the repository contains references to authentication-related files (crates/router/src/services/authentication.rs and crates/router/src/services/jwt.rs) and tokenization components, no actual implementation details, configuration parameters, or security controls for user authentication systems are visible in the provided evidence. The evidence primarily consists of CI/CD workflow tokens and code ownership assignments rather than substantive logical access control mechanisms.

**REMEDIATION DIRECTION**

The development team needs to provide comprehensive documentation and evidence of their user authentication implementation including: authentication method configurations (multi-factor authentication, password policies, session management), access control matrices showing user roles and permissions, code review of the actual authentication service implementations, security testing results for authentication flows, and operational procedures for user access provisioning and deprovisioning. Additionally, implement code-level security controls such as input validation, secure token handling, and proper session management that can be audited against SOC 2 requirements.

---

### SOC2-002: Role-Based Access Control

**LEGAL QUESTION**

Does the system implement role-based or attribute-based access controls that restrict system functions and data access based on authorized user roles, consistent with the principle of least privilege as required under CC6.3?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC6.3 (Role-Based Access and Least Privilege)

**EVIDENCE**

- `.dockerignore:207` — `# Support for Project snippet scope`
- `.github/CODEOWNERS:98` — `crates/api_models/src/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:99` — `crates/api_models/src/events/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:104` — `crates/diesel_models/src/query/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:108` — `crates/diesel_models/src/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:110` — `crates/router/src/consts/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:117` — `crates/router/src/core/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:122` — `crates/router/src/db/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:127` — `crates/router/src/routes/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:141` — `crates/router/src/types/storage/user_role.rs @juspay/hyperswitch-dashboard`

**FINDING: 🔵 Pattern of Concern**

The system shows evidence of role-based access control implementation through multiple user_role modules across the codebase (crates/api_models/src/user_role.rs, crates/router/src/core/user_role.rs, etc.) and dedicated authorization services (crates/router/src/services/authorization.rs). However, the evidence consists only of file structure and ownership assignments without visibility into the actual implementation details, making it impossible to verify compliance with least privilege principles or validate proper role enforcement mechanisms as required under CC6.3.

**REMEDIATION DIRECTION**

Provide access to the actual source code content of the identified role-based access control files to enable verification of proper implementation. The analysis should include reviewing the role definition structures, permission matrices, access enforcement logic, and validation that system functions are appropriately restricted based on user roles with least privilege principles applied.

---

### SOC2-003: Encryption in Transit

**LEGAL QUESTION**

Does the system protect data during transmission over networks using encryption or other equivalent security measures, consistent with the CC6.7 requirement for protection of information during transmission?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC6.7 (Data Transmission Protection)

**EVIDENCE**

- `.devcontainer/devcontainer.json:1` — `// For format details, see https://aka.ms/devcontainer.json. For config options, see the`
- `.devcontainer/devcontainer.json:2` — `// README at: https://github.com/devcontainers/templates/tree/main/src/docker-existing-dockerfile`
- `.devcontainer/devcontainer.json:20` — `// Features to add to the dev container. More info: https://containers.dev/features.`
- `.devcontainer/devcontainer.json:32` — `// Uncomment to connect as an existing user other than the container default. More info: https://aka.ms/dev-containers-n`
- `.dockerignore:1` — `# Created by https://www.toptal.com/developers/gitignore/api/rust,visualstudiocode,clion,dotenv,direnv,linux,macos,windo`
- `.dockerignore:2` — `# Edit at https://www.toptal.com/developers/gitignore?templates=rust,visualstudiocode,clion,dotenv,direnv,linux,macos,wi`
- `.dockerignore:6` — `# Reference: https://intellij-support.jetbrains.com/hc/en-us/articles/206544839`
- `.dockerignore:84` — `# Comment Reason: https://github.com/joeblau/gitignore.io/issues/186#issuecomment-215987721`
- `.dockerignore:92` — `# https://plugins.jetbrains.com/plugin/7973-sonarlint`
- `.dockerignore:96` — `# https://plugins.jetbrains.com/plugin/7238-sonarqube-community-plugin`

**FINDING: 🔴 High Risk**

Analysis reveals a risk pattern consistent with non-compliance under SOC 2 CC6.7 data transmission protection requirements. No evidence of encryption controls or secure transmission protocols was found in the repository evidence. Additionally, multiple anti-patterns were detected using unencrypted HTTP protocols in test configurations across .github/workflows/cypress-tests-runner.yml (lines 387, 590, 841, 1055, 1262) and .github/workflows/postman-collection-runner.yml (line 155), indicating potential systemic issues with secure transmission practices.

**REMEDIATION DIRECTION**

Implement TLS/HTTPS encryption for all data transmission endpoints and update all test configurations to use HTTPS instead of HTTP protocols. Add configuration files demonstrating encryption settings, SSL/TLS certificate management, and secure communication channels. Document encryption standards and protocols used for data in transit, and ensure all application endpoints enforce encrypted connections with appropriate cipher suites and certificate validation.

---

### SOC2-004: Logging and Monitoring

**LEGAL QUESTION**

Does the system implement logging, monitoring, and alerting mechanisms that detect and record security events, anomalies, and unauthorized activities, as required under CC7.2 for monitoring system components for anomalies?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC7.2 (Monitoring of System Components)

**EVIDENCE**

- `.dockerignore:251` — `monitoring/*.tmp/`
- `.dockerignore:251` — `monitoring/*.tmp/`
- `.github/CODEOWNERS:155` — `monitoring/ @juspay/hyperswitch-infra`
- `.github/CODEOWNERS:155` — `monitoring/ @juspay/hyperswitch-infra`
- `.github/ISSUE_TEMPLATE/bug_report.yml:59` — `placeholder: Providing context (e.g. request-response bodies, stack trace or log data) helps us come up with a solution `
- `.github/workflows/CI-pr.yml:31` — `# Don't emit giant backtraces in the CI logs.`
- `.github/workflows/CI-pr.yml:32` — `RUST_BACKTRACE: short`
- `.github/workflows/CI-push.yml:34` — `# Don't emit giant backtraces in the CI logs.`
- `.github/workflows/CI-push.yml:35` — `RUST_BACKTRACE: short`
- `.github/workflows/archive/connector-sanity-tests.yml:37` — `# Don't emit giant backtraces in the CI logs.`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOC 2 CC7.2. While a monitoring directory structure exists (referenced in .dockerignore and CODEOWNERS files), no actual logging, monitoring, or alerting implementation code was found in the repository evidence. The only logging-related references are basic development traces (RUST_BACKTRACE configurations) and bug report templates, which do not constitute security event monitoring or anomaly detection systems required for production compliance.

**REMEDIATION DIRECTION**

Implement comprehensive logging and monitoring infrastructure including: security event logging (authentication attempts, authorization failures, data access), anomaly detection systems, real-time alerting mechanisms for suspicious activities, and centralized log management. The existing monitoring directory should be populated with actual monitoring configurations, dashboards, and alert definitions. Consider implementing structured logging throughout the application code, security information and event management (SIEM) integration, and automated threat detection capabilities to meet CC7.2 requirements for system component monitoring.

---

### SOC2-005: Change Management

**LEGAL QUESTION**

Does the system demonstrate evidence of change management controls including version control, code review processes, and controlled deployment procedures, as required under CC8.1 for managing changes to infrastructure, data, software, and procedures?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC8.1 (Change Management)

**EVIDENCE**

- `.deepsource.toml:1` — `version = 1`
- `.devcontainer/devcontainer.json:29` — `// Configure tool-specific properties.`
- `.dockerignore:8` — `# User-specific stuff`
- `.dockerignore:15` — `# AWS User-specific`
- `.dockerignore:241` — `# hyperswitch Project specific excludes`
- `.dockerignore:253` — `config/production.toml`
- `.github/CODEOWNERS:20` — `migrations/ @juspay/hyperswitch-framework`
- `.github/CODEOWNERS:21` — `v2_migrations/ @juspay/hyperswitch-framework`
- `.github/CODEOWNERS:22` — `v2_compatible_migrations/ @juspay/hyperswitch-framework`
- `.github/ISSUE_TEMPLATE/bug_report.yml:10` — `1. Make sure you're on the latest version of the app. The current release can be found here: https://github.com/juspay/h`

**FINDING: 🟠 Medium Risk**

The system shows partial evidence of change management controls but lacks comprehensive documentation of required processes. While version control is evidenced through `.deepsource.toml:1` version tracking and code ownership controls in `.github/CODEOWNERS:20-22` for critical migration files, there is insufficient evidence of formal code review processes, controlled deployment procedures, or comprehensive change management documentation as required under SOC 2 CC8.1. This creates a risk pattern consistent with non-compliance under the Change Management trust services criteria.

**REMEDIATION DIRECTION**

Implement and document formal code review processes with approval workflows, establish controlled deployment procedures with staging environments and rollback capabilities, and create comprehensive change management documentation that covers all changes to infrastructure, data, software, and procedures. Add pull request templates, deployment checklists, and change approval matrices to demonstrate systematic change control processes beyond the basic CODEOWNERS file currently in place.

---

### SOC2-006: Incident Response

**LEGAL QUESTION**

Does the system implement incident detection, response, and recovery procedures that enable timely identification and remediation of security incidents, consistent with CC7.3 requirements for evaluating security events and CC7.4 for responding to identified incidents?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC7.3 (Security Event Evaluation); CC7.4 (Incident Response)

**EVIDENCE**

- `.github/CODEOWNERS:77` — `crates/external_services/src/grpc_client/health_check_client.rs @juspay/hyperswitch-routing`
- `.github/PULL_REQUEST_TEMPLATE.md:23` — `Provide links to the files with corresponding changes.`
- `.github/workflows/CI-pr.yml:232` — `name: Spell check specific critical directories`
- `Dockerfile:52` — `# RUN_ENV decides the corresponding config file to be used`
- `LICENSE:159` — `incidental, or consequential damages of any character arising as a`
- `add_connector.md:413` — `Response mapping is a critical component of connector implementation that translates payment processor–specific statuses`
- `add_connector.md:550` — `#### Critical Response Fields`
- `add_connector.md:563` — `Each critical response field requires specific implementation patterns to ensure consistent behavior across all Hyperswi`
- `add_connector.md:212` — `Each flow type corresponds to specific request/response data structures and connector integration patterns. All flows fo`
- `api-reference/essentials/error_codes.mdx:12` — `The section below contains all the error codes and their corresponding error messages.`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOC 2 CC7.3 and CC7.4 requirements. While the codebase contains error handling mechanisms (api-reference/essentials/error_codes.mdx) and webhook verification capabilities (config/config.example.toml:162-163), there is no evidence of formal incident detection, response, or recovery procedures. The health check client (crates/external_services/src/grpc_client/health_check_client.rs) suggests monitoring capabilities, but no systematic incident response workflows or security event evaluation processes are documented or implemented.

**REMEDIATION DIRECTION**

Implement comprehensive incident response procedures including: automated security event detection and logging mechanisms, defined incident classification and escalation procedures, documented response playbooks for different incident types, recovery procedures with defined RTO/RPO objectives, and incident post-mortem processes. Add monitoring dashboards for security events, integrate with SIEM tools for event correlation, and establish clear communication channels for incident response team coordination. Document all procedures and ensure they are regularly tested through tabletop exercises.

---

### SOC2-007: Vendor and Dependency Risk

**LEGAL QUESTION**

Does the system assess and manage risks associated with third-party vendors, libraries, and service providers, including dependency vulnerability management, consistent with CC9.2 requirements for risk assessment of third-party service providers?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC9.2 (Third-Party Risk Management)

**EVIDENCE**

- `.dockerignore:178` — `# Remove Cargo.lock from gitignore if creating an executable, leave it for libraries`
- `.dockerignore:179` — `# More information here https://doc.rust-lang.org/cargo/guide/cargo-toml-vs-cargo-lock.html`
- `.dockerignore:180` — `!Cargo.lock`
- `.github/CODEOWNERS:24` — `Cargo.toml @juspay/hyperswitch-framework`
- `.github/CODEOWNERS:25` — `Cargo.lock @juspay/hyperswitch-framework`
- `.github/CODEOWNERS:55` — `crates/router/src/types/api/connector_mapping.rs @juspay/hyperswitch-connector`
- `.github/api-migration-compatibility/migration-rules.yaml:9` — `description: "Dropping a table removes data and breaks existing queries"`
- `.github/api-migration-compatibility/migration-rules.yaml:13` — `description: "Dropping a column breaks applications expecting it"`
- `.github/api-migration-compatibility/migration-rules.yaml:45` — `description: "Dropping an index can significantly impact query performance"`
- `.github/api-migration-compatibility/migration-rules.yaml:49` — `description: "Dropping a constraint may allow invalid data"`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOC 2 CC9.2 for third-party risk management. While the repository contains Rust dependency management files (Cargo.toml and Cargo.lock) and basic CI checks for dependency changes, there is no evidence of systematic third-party vendor risk assessment, dependency vulnerability scanning, or formalized processes for evaluating security risks of third-party libraries and service providers. The codebase appears to manage dependencies but lacks the comprehensive risk assessment framework required by CC9.2.

**REMEDIATION DIRECTION**

Implement a formal third-party risk management program that includes: automated dependency vulnerability scanning tools integrated into the CI/CD pipeline, documented risk assessment procedures for evaluating new third-party libraries and vendors, regular security reviews of existing dependencies, and established criteria for approving or rejecting third-party components based on security posture. Add dependency scanning tools like cargo-audit for Rust dependencies and create policies documenting how third-party risks are identified, assessed, and mitigated throughout the software development lifecycle.

---

### SOC2-008: Data Backup and Recovery

**LEGAL QUESTION**

Does the system implement data backup, replication, and recovery controls that ensure availability and recoverability of data, consistent with the A1.2 criterion for recovery of infrastructure and data to meet objectives?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria A1.2 (Recovery of Infrastructure and Data)

**EVIDENCE**

- `.devcontainer/devcontainer.json:32` — `// Uncomment to connect as an existing user other than the container default. More info: https://aka.ms/dev-containers-n`
- `.dockerignore:182` — `# These are backup files generated by rustfmt`
- `.dockerignore:220` — `# Dump file`
- `.dockerignore:221` — `*.stackdump`
- `.dockerignore:72` — `com_crashlytics_export_strings.xml`
- `.dockerignore:5` — `# Covers JetBrains IDEs: IntelliJ, RubyMine, PhpStorm, AppCode, PyCharm, CLion, Android Studio, WebStorm and Rider`
- `.dockerignore:100` — `# https://plugins.jetbrains.com/plugin/7896-markdown-navigator-enhanced`
- `.dockerignore:127` — `# temporary files which can be created if a process still has a handle open of a deleted file`
- `.dockerignore:152` — `# Files that might appear in the root of a volume`
- `.dockerignore:161` — `# Directories potentially created on remote AFP share`

**FINDING: 🔴 High Risk**

No evidence of data backup, replication, or recovery controls was found in the repository analysis. The evidence consists primarily of .dockerignore entries mentioning backup files generated by development tools (line 182) and dump files, but contains no actual implementation of systematic data backup or recovery procedures. This represents a risk pattern consistent with non-compliance under SOC 2 Trust Services Criteria A1.2, which requires recovery controls to ensure availability and recoverability of data to meet objectives.

**REMEDIATION DIRECTION**

Implement comprehensive data backup and recovery controls including: automated backup procedures with defined schedules and retention policies, database replication configurations, disaster recovery runbooks, backup verification and testing procedures, and recovery time/point objectives documentation. These controls should be implemented in infrastructure configuration files, documented in operational procedures, and include automated testing of backup and recovery processes to ensure data availability requirements are met.

---

### SOC2-009: Multi-Factor Authentication

**LEGAL QUESTION**

Does the system implement or support multi-factor authentication for user access, particularly for privileged accounts and administrative interfaces, consistent with CC6.1 requirements for logical access security?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC6.1 (Logical Access - MFA)

**EVIDENCE**

- `.dockerignore:159` — `.com.apple.timemachine.donotpresent`
- `.gitignore:159` — `.com.apple.timemachine.donotpresent`
- `aws/beta_schema.sql:216` — `'otp',`
- `config/config.example.toml:502` — `two_factor_auth_expiry_in_secs = 300 # Number of seconds after which 2FA should be done again if doing update/change fro`
- `config/config.example.toml:505` — `force_two_factor_auth = false        # Whether to force two factor authentication for all users`
- `config/config.example.toml:502` — `two_factor_auth_expiry_in_secs = 300 # Number of seconds after which 2FA should be done again if doing update/change fro`
- `config/config.example.toml:503` — `totp_issuer_name = "Hyperswitch"     # Name of the issuer for TOTP`
- `config/config.example.toml:503` — `totp_issuer_name = "Hyperswitch"     # Name of the issuer for TOTP`
- `config/dashboard.toml:30` — `totp=true`
- `config/dashboard.toml:42` — `threeds_authenticator=true`

**FINDING: 🔵 Pattern of Concern**

The system implements TOTP-based multi-factor authentication with configurable settings across multiple deployment environments, as evidenced by configuration files containing two-factor authentication parameters and TOTP issuer settings. However, the evidence shows that MFA enforcement varies by environment, with production.toml enabling "force_two_factor_auth = true" while integration_test.toml and the example configuration default to "force_two_factor_auth = false", creating a risk pattern consistent with non-compliance under SOC 2 CC6.1 for non-production environments and potentially privileged accounts.

**REMEDIATION DIRECTION**

Ensure multi-factor authentication is consistently enforced across all environments, not just production. Update all configuration files to set "force_two_factor_auth = true" by default, particularly for administrative and privileged user access. Implement role-based MFA requirements that specifically mandate two-factor authentication for all administrative interfaces and privileged accounts, regardless of deployment environment. Consider reducing the two_factor_auth_expiry_in_secs from 300 seconds for high-privilege operations to enhance security posture.

---

### SOC2-010: Security Policy Documentation

**LEGAL QUESTION**

Does the system demonstrate evidence of documented security policies, including acceptable use, data classification, and access management policies, as required under CC1.1 for the entity's commitment to integrity and ethical values?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC1.1 (COSO Principle 1 - Integrity and Ethical Values)

**EVIDENCE**

- `.github/ISSUE_TEMPLATE/bug_report.yml:88` — `id: read-contributing-guidelines`
- `.github/ISSUE_TEMPLATE/bug_report.yml:90` — `label: Have you read the Contributing Guidelines?`
- `.github/ISSUE_TEMPLATE/bug_report.yml:92` — `- label: I have read the [Contributing Guidelines](https://github.com/juspay/hyperswitch/blob/main/docs/CONTRIBUTING.md)`
- `.github/ISSUE_TEMPLATE/feature_request.yml:41` — `id: read-contributing-guidelines`
- `.github/ISSUE_TEMPLATE/feature_request.yml:43` — `label: Have you read the Contributing Guidelines?`
- `.github/ISSUE_TEMPLATE/feature_request.yml:45` — `- label: I have read the [Contributing Guidelines](https://github.com/juspay/hyperswitch/blob/main/docs/CONTRIBUTING.md)`
- `README.md:193` — `## Contributing`
- `README.md:197` — `Please read our [contributing guidelines](https://github.com/juspay/hyperswitch/blob/main/docs/CONTRIBUTING.md) to get s`
- `add_connector.md:42` — `* Before you begin, ensure you’ve completed the initial setup in our [Hyperswitch Contributor Guide](https://github.com/`
- `api-reference/intelligent-router-api-reference/overview.mdx:21` — `- [Contributing Guidelines](https://github.com/juspay/hyperswitch-intelligent-router/blob/main/CONTRIBUTING.md)`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOC 2 Trust Services Criteria CC1.1. While the repository contains contributing guidelines and development policies (docs/CONTRIBUTING.md), there is no evidence of formal security policies covering acceptable use, data classification, or access management requirements. The only security-related configuration found relates to Grafana content security policies (config/grafana.ini:301-306), which are technical controls rather than documented organizational security policies.

**REMEDIATION DIRECTION**

Create and document comprehensive security policies that demonstrate the organization's commitment to integrity and ethical values. This should include: (1) an acceptable use policy defining appropriate system and data usage, (2) a data classification policy establishing how sensitive information is categorized and handled, and (3) an access management policy outlining user provisioning, authentication, and authorization procedures. These policies should be stored in accessible documentation within the repository and referenced in operational procedures to satisfy SOC 2 CC1.1 requirements.

---

## SOX Findings

### SOX-001: Financial Data Integrity Controls

**LEGAL QUESTION**

Does the system implement controls to ensure the integrity, accuracy, and completeness of financial data and transactions, consistent with SOX Section 302 requirements for management certification of financial statements?

**REGULATORY STANDARD**

SOX Section 302 (Corporate Responsibility for Financial Reports)

**EVIDENCE**

- `.dockerignore:81` — `.idea/caches/build_file_checksums.ser`
- `.github/CODEOWNERS:61` — `crates/router/src/core/connector_validation.rs @juspay/hyperswitch-connector`
- `.github/CODEOWNERS:64` — `crates/hyperswitch_constraint_graph @juspay/hyperswitch-routing`
- `.github/ISSUE_TEMPLATE/bug_report.yml:20` — `validations:`
- `.github/ISSUE_TEMPLATE/bug_report.yml:29` — `validations:`
- `.github/ISSUE_TEMPLATE/bug_report.yml:38` — `validations:`
- `.github/ISSUE_TEMPLATE/bug_report.yml:51` — `validations:`
- `.github/ISSUE_TEMPLATE/bug_report.yml:60` — `validations:`
- `.github/ISSUE_TEMPLATE/bug_report.yml:76` — `validations:`
- `.github/ISSUE_TEMPLATE/feature_request.yml:20` — `validations:`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOX Section 302 requirements for financial data integrity controls. While some basic validation structures exist in GitHub issue templates and database constraint rules (migration-rules.yaml:47-49), no evidence was found of comprehensive financial transaction validation, audit trails, data integrity checks, or automated controls specifically designed to ensure accuracy and completeness of financial data. The presence of payment card data in .github/data/cards_info.csv without apparent integrity controls further elevates the compliance risk.

**REMEDIATION DIRECTION**

Implement comprehensive financial data integrity controls including: automated validation rules for all financial transactions, audit logging with immutable trails, data checksums/hashing for integrity verification, automated reconciliation processes, and role-based access controls with approval workflows. All financial data processing modules should include input validation, business rule enforcement, and exception handling with proper logging. Consider implementing database triggers, stored procedures with validation logic, and automated testing specifically for financial data accuracy and completeness scenarios.

---

### SOX-002: Access Controls to Financial Systems

**LEGAL QUESTION**

Does the system implement access controls that restrict access to financial systems and data to authorized personnel, with appropriate authentication and authorization mechanisms, as required under SOX Section 404 internal controls?

**REGULATORY STANDARD**

SOX Section 404 (Management Assessment of Internal Controls)

**EVIDENCE**

- `.github/CODEOWNERS:98` — `crates/api_models/src/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:99` — `crates/api_models/src/events/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:104` — `crates/diesel_models/src/query/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:108` — `crates/diesel_models/src/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:110` — `crates/router/src/consts/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:117` — `crates/router/src/core/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:122` — `crates/router/src/db/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:127` — `crates/router/src/routes/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:141` — `crates/router/src/types/storage/user_role.rs @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:147` — `crates/router/src/utils/user_role.rs @juspay/hyperswitch-dashboard`

**FINDING: 🔴 High Risk**

Risk pattern consistent with non-compliance under SOX Section 404. While the evidence shows extensive user role management code structure across multiple files (crates/api_models/src/user_role.rs, crates/router/src/core/user_role.rs, etc.), no actual authentication mechanisms, authorization controls, or access restriction implementations for financial systems were found in the repository evidence. The presence of payment processing workflows and gateway status mappings indicates this is a financial system requiring SOX compliance controls.

**REMEDIATION DIRECTION**

Implement and document comprehensive access control mechanisms including multi-factor authentication, role-based authorization with least privilege principles, session management, and audit logging for all financial system access. Ensure user role implementations include proper authentication validation, authorization checks before accessing financial data, and maintain detailed access logs. Add specific access control tests and documentation demonstrating compliance with SOX Section 404 internal control requirements for financial system access.

---

### SOX-003: Audit Trail for Financial Transactions

**LEGAL QUESTION**

Does the system maintain a complete and tamper-evident audit trail of all financial transactions, modifications, and access events, sufficient to support the audit requirements under SOX Section 802?

**REGULATORY STANDARD**

SOX Section 802 (Criminal Penalties for Altering Documents)

**EVIDENCE**

- `.dockerignore:196` — `# Local History for Visual Studio Code`
- `.dockerignore:197` — `.history/`
- `.dockerignore:203` — `# Ignore all local history of files`
- `.dockerignore:204` — `.history`
- `.github/ISSUE_TEMPLATE/feature_request.yml:11` — `2. Check the changelog file to confirm that the feature hasn't been added for an upcoming release: https://github.com/ju`
- `.github/cocogitto-changelog-template:47` — `**Full Changelog:** [`{{ from.tag ~ "..." ~ version.tag }}`]({{ compare_base_url ~ from.tag ~ "..." ~ version.tag }})`
- `.github/cocogitto-changelog-template:49` — `**Full Changelog:** [`{{ from.id ~ "..." ~ version.tag }}`]({{ compare_base_url ~ from.id ~ "..." ~ version.tag }})`
- `.github/cocogitto-changelog-template:55` — `**Full Changelog:** [`{{ from_shorthand ~ "..." ~ to_shorthand }}`]({{ compare_base_url ~ from_shorthand ~ "..." ~ to_sh`
- `.github/git-cliff-changelog.toml:4` — `[changelog]`
- `.github/git-cliff-changelog.toml:5` — `# changelog header`

**FINDING: 🔴 High Risk**

The evidence shows only software development changelog and version control configurations in files like .github/git-cliff-changelog.toml and .github/workflows/create-hotfix-tag.yml, but contains no evidence of financial transaction audit logging, tamper-evident controls, or SOX-compliant audit trail mechanisms. This absence of required audit trail infrastructure presents a risk pattern consistent with non-compliance under SOX Section 802, which mandates complete and tamper-evident documentation of all financial transaction activities and access events.

**REMEDIATION DIRECTION**

Implement comprehensive audit logging functionality that captures all financial transactions, data modifications, and system access events with immutable timestamps, user identification, and cryptographic integrity controls. Add database audit triggers, application-level transaction logging, and tamper-evident storage mechanisms that meet SOX requirements for financial audit trails. Ensure all audit logs are automatically generated, cannot be altered without detection, and include sufficient detail to reconstruct any financial transaction or data change.

---

### SOX-004: Change Management for Financial Software

**LEGAL QUESTION**

Does the system implement change management controls for software that processes financial data, including version control, code review, testing, and controlled deployment, consistent with SOX IT general controls?

**REGULATORY STANDARD**

SOX Section 404 (ITGC - Change Management Controls)

**EVIDENCE**

- `.deepsource.toml:1` — `version = 1`
- `.devcontainer/devcontainer.json:29` — `// Configure tool-specific properties.`
- `.devcontainer/devcontainer.json:27` — `// "postCreateCommand": "cat /etc/os-release",`
- `.dockerignore:8` — `# User-specific stuff`
- `.dockerignore:15` — `# AWS User-specific`
- `.dockerignore:241` — `# hyperswitch Project specific excludes`
- `.dockerignore:253` — `config/production.toml`
- `.github/CODEOWNERS:20` — `migrations/ @juspay/hyperswitch-framework`
- `.github/CODEOWNERS:21` — `v2_migrations/ @juspay/hyperswitch-framework`
- `.github/CODEOWNERS:22` — `v2_compatible_migrations/ @juspay/hyperswitch-framework`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOX Section 404 ITGC Change Management Controls. While basic version control infrastructure exists (evidenced by .github/ directory structure and CODEOWNERS file at lines 20-22 showing some access controls for migrations), there is no evidence of formal change management processes, code review workflows, testing procedures, or controlled deployment mechanisms required for financial software systems. The CODEOWNERS file only covers database migrations, not the broader codebase processing financial data.

**REMEDIATION DIRECTION**

Implement comprehensive change management controls including: mandatory pull request workflows with required reviewers for all code changes, automated testing pipelines that must pass before deployment, formal code review processes with documented approval chains, controlled deployment procedures with rollback capabilities, and segregation of duties between development and production environments. Configure branch protection rules in GitHub and establish formal testing and deployment documentation that demonstrates compliance with SOX IT general controls for all software components that process financial data.

---

### SOX-005: Segregation of Duties Evidence

**LEGAL QUESTION**

Does the system implement segregation of duties controls that prevent any single individual from having the ability to both authorize and execute financial transactions, or to both develop and deploy changes to financial systems?

**REGULATORY STANDARD**

SOX Section 404 (Internal Controls - Segregation of Duties)

**EVIDENCE**

- `.github/CODEOWNERS:89` — `crates/router/src/workflows/payment_method_status_update.rs @juspay/hyperswitch-payment-methods`
- `.github/CODEOWNERS:166` — `crates/router/src/workflows/attach_payout_account_workflow.rs @juspay/hyperswitch-payouts`
- `.github/CODEOWNERS:130` — `crates/router/src/services/authorization @juspay/hyperswitch-dashboard`
- `.github/CODEOWNERS:131` — `crates/router/src/services/authorization.rs @juspay/hyperswitch-dashboard`
- `.github/data/cards_info.csv:7` — `424242,STRIPE PAYMENTS UK LIMITED,Visa,CREDIT,,UNITEDKINGDOM,,,GB,2015-07-22 16:41:32,2025-11-04 15:23:24,Visa`
- `.github/git-cliff-changelog.toml:92` — `# limit the number of commits included in the changelog.`
- `.github/git-cliff-changelog.toml:93` — `# limit_commits = 42`
- `.github/workflows/CI-pr.yml:10` — `group: ${{ github.workflow }}-${{ github.ref }}`
- `.github/workflows/CI-pr.yml:23` — `# See https://matklad.github.io/2021/09/04/fast-rust-builds.html#ci-workflow`
- `.github/workflows/CI-push.yml:13` — `group: ${{ github.workflow }}-${{ github.ref }}`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOX Section 404 segregation of duties requirements. While CODEOWNERS file entries indicate some code review controls exist for financial components (payment methods, payouts, and authorization services at lines 89, 166, 130-131), there is no evidence of systematic segregation between authorization and execution roles, or between development and deployment functions. The presence of financial transaction workflows without corresponding role-based access controls or approval matrices represents a significant internal control deficiency.

**REMEDIATION DIRECTION**

Implement a comprehensive segregation of duties framework that separates authorization from execution roles and development from deployment functions. This should include: (1) role-based access control (RBAC) system with defined financial transaction approval hierarchies, (2) separate user accounts and permissions for developers versus deployers, (3) mandatory multi-person approval workflows for all financial system changes, (4) audit trails showing who authorized versus who executed each financial transaction, and (5) regular access reviews to ensure no single individual has conflicting permissions across the financial transaction lifecycle.

---

### SOX-006: Data Retention for Financial Records

**LEGAL QUESTION**

Does the system implement data retention policies that preserve financial records, audit work papers, and supporting documentation for the minimum retention period required under SOX Section 802 (not less than 7 years)?

**REGULATORY STANDARD**

SOX Section 802 (Document Retention - 7 Year Minimum)

**EVIDENCE**

- `.dockerignore:182` — `# These are backup files generated by rustfmt`
- `.github/workflows/cypress-tests-runner.yml:151` — `retention-days: 1`
- `.github/workflows/cypress-tests-runner.yml:209` — `retention-days: 1`
- `.github/workflows/cypress-tests-runner.yml:402` — `retention-days: 1`
- `.github/workflows/cypress-tests-runner.yml:606` — `retention-days: 1`
- `.github/workflows/cypress-tests-runner.yml:615` — `retention-days: 1`
- `.github/workflows/cypress-tests-runner.yml:857` — `retention-days: 1`
- `.github/workflows/cypress-tests-runner.yml:866` — `retention-days: 1`
- `.github/workflows/cypress-tests-runner.yml:1074` — `retention-days: 1`
- `.github/workflows/cypress-tests-runner.yml:1281` — `retention-days: 1`

**FINDING: 🔴 High Risk**

The system shows a risk pattern consistent with non-compliance under SOX Section 802's 7-year retention requirement for financial records. While AWS backup retention is configured for 7 days in aws/hyperswitch_aws_setup.sh:163, no evidence was found of data retention policies specifically addressing financial records, audit work papers, or supporting documentation for the required 7-year minimum period. The GitHub workflow configurations show only 1-day retention periods for artifacts, indicating inadequate retention controls for regulatory compliance.

**REMEDIATION DIRECTION**

Implement comprehensive data retention policies that specifically address financial records, audit trails, and supporting documentation with a minimum 7-year retention period. Configure automated archival systems for financial data beyond the current 7-day AWS backup retention. Document retention schedules in policy files within the codebase, establish automated compliance monitoring for retention periods, and ensure all financial transaction data and audit logs are preserved according to SOX requirements rather than relying on short-term backup configurations.

---

### SOX-007: Internal Control Documentation

**LEGAL QUESTION**

Does the system provide evidence of documented internal controls over financial reporting, including control objectives, control activities, and monitoring procedures, as required under SOX Section 404(a)?

**REGULATORY STANDARD**

SOX Section 404(a) (Management Assessment of Internal Controls)

**EVIDENCE**

- `.github/CODEOWNERS:14` — `config/ @juspay/hyperswitch-framework`
- `.github/CODEOWNERS:15` — `crates/ @juspay/hyperswitch-framework`
- `.github/CODEOWNERS:16` — `crates/router/src/types/ @juspay/hyperswitch-framework`
- `.github/CODEOWNERS:17` — `crates/router/src/services/ @juspay/hyperswitch-framework`
- `.github/CODEOWNERS:18` — `crates/router/src/db/ @juspay/hyperswitch-framework`
- `.github/CODEOWNERS:19` — `crates/router/src/routes/ @juspay/hyperswitch-framework`
- `.github/CODEOWNERS:20` — `migrations/ @juspay/hyperswitch-framework`
- `.github/CODEOWNERS:21` — `v2_migrations/ @juspay/hyperswitch-framework`
- `.github/CODEOWNERS:22` — `v2_compatible_migrations/ @juspay/hyperswitch-framework`
- `.github/CODEOWNERS:23` — `api-reference/ @juspay/hyperswitch-framework`

**FINDING: 🔴 High Risk**

The code repository shows a risk pattern consistent with non-compliance under SOX Section 404(a). While basic code ownership controls are documented in .github/CODEOWNERS (lines 14-25), there is no evidence of documented internal controls specifically over financial reporting, including control objectives, control activities, or monitoring procedures. The repository contains only general software development governance controls rather than the financial reporting-specific internal control documentation required by SOX.

**REMEDIATION DIRECTION**

Implement and document comprehensive internal controls over financial reporting within the codebase or associated documentation. This should include: (1) documented control objectives that clearly map to financial reporting risks, (2) specific control activities such as automated validation rules, segregation of duties matrices, and approval workflows for financially-relevant transactions, and (3) monitoring procedures including automated testing, audit trails, and periodic control effectiveness assessments. Consider creating dedicated directories like `/controls/` or `/compliance/` with structured documentation that demonstrates how the system prevents material misstatements in financial reporting.

---

### SOX-008: Anti-Tampering Controls

**LEGAL QUESTION**

Does the system implement controls to prevent unauthorized alteration or destruction of financial records, including integrity verification, immutable storage, and tamper detection mechanisms, consistent with SOX Section 802 anti-destruction requirements?

**REGULATORY STANDARD**

SOX Section 802 (Criminal Penalties for Document Destruction/Alteration)

**EVIDENCE**

- `.dockerignore:81` — `.idea/caches/build_file_checksums.ser`
- `.github/workflows/CI-pr.yml:199` — `checksum: true`
- `.github/workflows/CI-pr.yml:287` — `checksum: true`
- `.github/workflows/CI-push.yml:100` — `#     checksum: true`
- `.github/workflows/CI-push.yml:110` — `checksum: true`
- `.github/workflows/CI-push.yml:116` — `checksum: true`
- `.github/workflows/CI-push.yml:193` — `#     checksum: true`
- `.github/workflows/CI-push.yml:199` — `checksum: true`
- `.github/workflows/CI-push.yml:205` — `checksum: true`
- `.github/workflows/CI-push.yml:215` — `#     checksum: true`

**FINDING: 🟠 Medium Risk**

The system implements basic integrity verification through checksum controls across multiple CI/CD workflows (19 instances found in .github/workflows files), indicating some anti-tampering measures are in place. However, concerning anti-patterns were detected in migration rules configuration files, specifically DROP TABLE and TRUNCATE TABLE operations defined in .github/api-migration-compatibility/migration-rules.yaml at lines 7, 19, 61, 64, 78, 81, 95, and 98, which create risk patterns consistent with non-compliance under SOX Section 802 anti-destruction requirements. No evidence of immutable storage mechanisms or comprehensive tamper detection was found in the analyzed code.

**REMEDIATION DIRECTION**

Implement additional controls to complement the existing checksum verification: establish immutable audit trails for financial record changes, add database-level constraints preventing unauthorized deletion of financial data, implement comprehensive logging of all record access and modification attempts, and review the migration rules to ensure DROP TABLE and TRUNCATE operations on financial data require explicit approval workflows and maintain backup copies. Consider implementing write-once-read-many (WORM) storage for critical financial records and add real-time tamper detection alerts.

---

## TCPA Findings

### TCPA-001: Prior Express Written Consent for SMS

**LEGAL QUESTION**

Does the system obtain prior express written consent before sending marketing or promotional text messages, including a clear and conspicuous disclosure that consent is being sought, as required under 47 U.S.C. §227(b)(1) and 47 CFR §64.1200(a)(2)?

**REGULATORY STANDARD**

TCPA 47 U.S.C. §227(b)(1); 47 CFR §64.1200(a)(2)

**EVIDENCE**

- `LICENSE:136` — `the terms of any separate license agreement you may have executed`
- `LICENSE:145` — `agreed to in writing, Licensor provides the Work (and each`
- `LICENSE:157` — `negligent acts) or agreed to in writing, shall any Contributor be`
- `LICENSE:172` — `of any other Contributor, and only if You agree to indemnify,`
- `LICENSE:198` — `Unless required by applicable law or agreed to in writing, software`
- `api-reference/essentials/go-live.mdx:11` — `### Signing of Hyperswitch services agreement`
- `api-reference/essentials/go-live.mdx:13` — `- [ ] Ensure that the Hyperswitch services agreement is signed and shared with the Hyperswitch team. In case you need an`
- `config/dashboard.toml:11` — `agreement_url=""`
- `config/dashboard.toml:12` — `agreement_version=""`
- `crates/api_models/src/admin.rs:3400` — `/// Boolean for controlling whether or not to show the explicit consent for storing cards`

**FINDING: 🔴 High Risk**

No evidence found of prior express written consent mechanisms for SMS marketing or promotional messages as required under TCPA regulations. The codebase shows various agreement-related functionality (config/dashboard.toml:11-12, crates/api_models/src/user/dashboard_metadata.rs:35) and explicit consent controls for card storage (crates/api_models/src/admin.rs:3400), but contains no implementation for SMS consent collection, disclosure language, or consent verification processes. This presents a risk pattern consistent with non-compliance under 47 U.S.C. §227(b)(1) and 47 CFR §64.1200(a)(2).

**REMEDIATION DIRECTION**

Implement a comprehensive SMS consent management system that captures prior express written consent before sending any marketing or promotional text messages. This should include: clear and conspicuous disclosure language explaining what the user is consenting to, a mechanism to capture and store consent records with timestamps, opt-out instructions in all marketing messages, and validation logic to prevent SMS sending without verified consent. Consider extending the existing agreement framework patterns found in the dashboard metadata to include SMS-specific consent workflows.

---

### TCPA-002: Opt-Out Mechanism Implementation

**LEGAL QUESTION**

Does the system provide a clear and easy mechanism for recipients to opt out of receiving further messages, and does it honor opt-out requests promptly, as required under TCPA and CTIA guidelines?

**REGULATORY STANDARD**

TCPA 47 U.S.C. §227(b)(2)(E); CTIA Messaging Principles

**EVIDENCE**

- `.github/workflows/CI-pr.yml:11` — `cancel-in-progress: true`
- `.github/workflows/CI-push.yml:14` — `cancel-in-progress: true`
- `.github/workflows/api-migrations-compatibility.yml:26` — `cancel-in-progress: true`
- `.github/workflows/archive/connector-sanity-tests.yml:17` — `cancel-in-progress: true`
- `.github/workflows/archive/connector-ui-sanity-tests.yml:12` — `cancel-in-progress: true`
- `.github/workflows/cypress-tests-runner.yml:1269` — `- name: Stop running server`
- `.github/workflows/cypress-tests-runner.yml:14` — `cancel-in-progress: true`
- `.github/workflows/migration-check.yaml:12` — `cancel-in-progress: true`
- `.github/workflows/postman-collection-runner.yml:11` — `cancel-in-progress: true`
- `.github/workflows/release-nightly-version.yml:11` — `cancel-in-progress: true`

**FINDING: 🔴 High Risk**

No evidence was found of opt-out mechanisms for message recipients in the analyzed code repository. The evidence shows only payment cancellation functionality (api-reference/docs.json:46-47) and workflow cancellation features (.github/workflows files), but contains no implementation of user opt-out requests, unsubscribe functionality, or message preference management systems. This creates a risk pattern consistent with non-compliance under TCPA 47 U.S.C. §227(b)(2)(E) and CTIA Messaging Principles.

**REMEDIATION DIRECTION**

Implement a comprehensive opt-out mechanism that includes: (1) clear unsubscribe links or keywords in all automated messages, (2) an opt-out request processing system that honors requests within the required timeframe, (3) a suppression list management system to prevent future messages to opted-out recipients, and (4) audit logging of all opt-out requests and processing. Add API endpoints for managing user communication preferences and ensure all messaging workflows check opt-out status before sending communications.

---

### TCPA-003: Do Not Call List Checking

**LEGAL QUESTION**

Does the system check phone numbers against the National Do Not Call Registry and maintain an internal do-not-call list before initiating outbound calls or messages, as required under 47 CFR §64.1200(c)?

**REGULATORY STANDARD**

TCPA 47 CFR §64.1200(c) (Do Not Call Requirements)

**EVIDENCE**

- `crates/hyperswitch_connectors/src/connectors/ebanx/transformers.rs:80` — `NationalRegistryOfLegalEntities,`
- `crates/hyperswitch_connectors/src/connectors/ebanx/transformers.rs:120` — `EbanxDocumentType::NationalRegistryOfLegalEntities`
- `crates/hyperswitch_connectors/src/connectors/facilitapay/requests.rs:86` — `/// which is the national registry of legal entities in Brazil used as a unique identifier for Brazilian companies.`
- `crates/hyperswitch_connectors/src/connectors/facilitapay/requests.rs:90` — `/// which is the national registry of natural persons in Brazil used as a unique identifier for Brazilian citizens.`
- `crates/router/src/utils/user/blocker_emails.txt:739` — `idncafe.com`
- `crates/router_env/Cargo.toml:32` — `tracing-subscriber = { version = "0.3.19", default-features = true, features = ["env-filter", "json", "registry"] }`
- `crates/router_env/src/logger/formatter.rs:19` — `registry::{LookupSpan, SpanRef},`
- `crates/router_env/src/logger/setup.rs:65` — `let subscriber = tracing_subscriber::registry()`
- `crates/router_env/src/logger/setup.rs:227` — `tracing_subscriber::Registry,`
- `crates/router_env/src/logger/storage.rs:104` — `impl<S: Subscriber + for<'a> tracing_subscriber::registry::LookupSpan<'a>> Layer<S>`

**FINDING: 🔴 High Risk**

No evidence found of Do Not Call Registry checking or internal do-not-call list maintenance functionality in the codebase. The search results show references to Brazilian national registries for legal entities and citizens in payment connectors (ebanx/transformers.rs and facilitapay/requests.rs), logging registries, and model registries, but contain no telecommunications compliance controls for outbound calling or messaging. This represents a risk pattern consistent with non-compliance under TCPA 47 CFR §64.1200(c).

**REMEDIATION DIRECTION**

Implement Do Not Call Registry integration by adding functionality to check phone numbers against the National Do Not Call Registry before initiating any outbound calls or messages. Create and maintain an internal do-not-call list with appropriate data storage and lookup mechanisms. Add validation logic in the outbound communication pipeline to verify numbers against both the national registry and internal suppression lists before processing calls or SMS messages.

---

### TCPA-004: Message Frequency Disclosure

**LEGAL QUESTION**

Does the system disclose to consumers the expected frequency of messages before obtaining consent, and does it enforce frequency limits consistent with the disclosed rate, as recommended by CTIA guidelines?

**REGULATORY STANDARD**

CTIA Messaging Principles and Best Practices; TCPA Consent Requirements

**EVIDENCE**

- `.github/workflows/release-nightly-version-reusable.yml:107` — `#                                                              The 2nd capture group contains the micro version number`
- `add_connector.md:141` — `- Payment authorization and capture`
- `add_connector.md:203` — `| **Authorization**     | Authorize and immediately capture payment        | [crates/hyperswitch_interfaces/src/types.rs`
- `add_connector.md:204` — `| **Authorization‑Only**| Authorize payment for later capture              | [crates/router/src/types.rs#L39](https://gi`
- `add_connector.md:205` — `| **Capture**           | Capture a previously authorized payment          | [crates/router/src/types.rs#L39](https://gi`
- `add_connector.md:241` — `Chooses purchase (auto‑capture) or preauth endpoint in `get_url()` and processes payment data directly.`
- `add_connector.md:405` — `settle: item.router_data.request.is_auto_capture()?,`
- `add_connector.md:466` — `| `Authorized`           | `AttemptStatus::Authorized`   | Payment authorized, awaiting capture |`
- `add_connector.md:558` — `- **network_txn_id**: Captures network-level transaction identifiers`
- `add_connector.md:578` — `- **resource_id**: Defines the primary resource identifier used for subsequent operations such as captures, refunds, and`

**FINDING: 🔴 High Risk**

No evidence was found in the code repository demonstrating that the system discloses expected message frequency to consumers before obtaining consent or enforces frequency limits as required by CTIA guidelines. The evidence reviewed relates exclusively to payment processing functionality (authorization, capture, refunds) and rate limiting for API calls, with no messaging consent mechanisms, frequency disclosure interfaces, or consumer-facing messaging controls identified.

**REMEDIATION DIRECTION**

Implement a consumer consent interface that clearly displays message frequency expectations (e.g., "You will receive up to 5 messages per week") before collecting opt-in consent. Add backend enforcement mechanisms to track and limit message sending based on disclosed frequencies. Create audit trails for consent collection that include timestamp, frequency disclosed, and consumer acceptance. Consider adding configuration management for different message types and their respective frequency limits to ensure compliance with CTIA messaging principles.

---

### TCPA-005: Sender Identification in Messages

**LEGAL QUESTION**

Does the system include proper sender identification in all outbound messages, including the identity of the entity sending the message and how to contact them, consistent with TCPA and CTIA requirements?

**REGULATORY STANDARD**

TCPA 47 U.S.C. §227(d); CTIA Messaging Principles

**EVIDENCE**

- `add_connector.md:1000` — `- `get_card_issuer()` – Returns card brand (Visa, Mastercard, etc.)`
- `api-reference/rust_locker_open_api_spec.yml:314` — `card_brand:`
- `config/dashboard.toml:17` — `branding=false`
- `crates/analytics/docs/clickhouse/scripts/authentications.sql:53` — ``device_brand` Nullable(String),`
- `crates/analytics/docs/clickhouse/scripts/authentications.sql:121` — ``device_brand` Nullable(String),`
- `crates/analytics/docs/clickhouse/scripts/authentications.sql:191` — ``device_brand` Nullable(String),`
- `crates/analytics/docs/clickhouse/scripts/authentications.sql:254` — `device_brand,`
- `crates/analytics/src/auth_events/core.rs:194` — `AuthEventDimensions::DeviceBrand => fil.device_brand,`
- `crates/analytics/src/auth_events/filters.rs:74` — `pub device_brand: Option<String>,`
- `crates/analytics/src/auth_events/metrics.rs:66` — `pub device_brand: Option<String>,`

**FINDING: 🔴 High Risk**

No evidence found of sender identification mechanisms in outbound messages within the analyzed code repository. The evidence shows only payment processing functionality with card brand identification (add_connector.md:1000, api-reference/rust_locker_open_api_spec.yml:314) and device analytics tracking, but contains no implementations for including sender identity or contact information in outbound communications. This presents a risk pattern consistent with non-compliance under TCPA 47 U.S.C. §227(d) and CTIA Messaging Principles.

**REMEDIATION DIRECTION**

Implement sender identification functionality for all outbound messages by adding message templates or headers that include the sending entity's name and contact information. This should include creating configuration parameters for sender details, modifying message composition functions to automatically append required identification information, and ensuring all SMS, email, or other communications include clear sender identity and contact methods as required by TCPA regulations.

---

### TCPA-006: Record Keeping of Consent

**LEGAL QUESTION**

Does the system maintain records of consent that would be sufficient to demonstrate compliance in the event of a dispute, including the date, time, method of consent, and the specific consent language presented to the consumer?

**REGULATORY STANDARD**

TCPA 47 CFR §64.1200; FCC Declaratory Rulings on Consent Records

**EVIDENCE**

- `config/dashboard.toml:25` — `audit_trail=true`
- `crates/analytics/docs/README.md:146` — `audit_trail=true`

**FINDING: 🔴 High Risk**

The evidence shows only generic audit trail configuration flags (config/dashboard.toml:25 and crates/analytics/docs/README.md:146) but no specific implementation of TCPA consent record keeping requirements. No code was found that captures, stores, or manages the specific data elements required for TCPA compliance: date/time of consent, method of consent obtained, or the exact consent language presented to consumers. This represents a risk pattern consistent with non-compliance under TCPA 47 CFR §64.1200 and FCC Declaratory Rulings on Consent Records.

**REMEDIATION DIRECTION**

Implement a comprehensive consent management system that captures and permanently stores all required TCPA consent elements. This should include database schemas and API endpoints to record the precise timestamp of consent, the communication channel through which consent was obtained (web form, SMS, voice call, etc.), and the exact text of the consent language displayed to the consumer. Add functionality to retrieve and export these records in a format suitable for regulatory disputes or audits.

---

### TCPA-007: Revocation of Consent Handling

**LEGAL QUESTION**

Does the system honor revocation of consent through any reasonable means indicated by the consumer, not limited to specific keywords, and process revocation within a reasonable timeframe, consistent with FCC guidance?

**REGULATORY STANDARD**

TCPA 47 U.S.C. §227(b)(1)(A); FCC 2015 TCPA Omnibus Declaratory Ruling

**EVIDENCE**

- `.dockerignore:136` — `# .nfs files are created when an open file is removed but is still being accessed`
- `.dockerignore:178` — `# Remove Cargo.lock from gitignore if creating an executable, leave it for libraries`
- `.github/api-migration-compatibility/.oasdiff-severity-levels.yaml:1` — `api-path-removed-without-deprecation: ERR`
- `.github/api-migration-compatibility/.oasdiff-severity-levels.yaml:2` — `api-path-removed-before-sunset: ERR`
- `.github/api-migration-compatibility/.oasdiff-severity-levels.yaml:3` — `api-removed-without-deprecation: ERR`
- `.github/api-migration-compatibility/.oasdiff-severity-levels.yaml:4` — `api-removed-before-sunset: ERR`
- `.github/api-migration-compatibility/.oasdiff-severity-levels.yaml:5` — `api-operation-id-removed: ERR`
- `.github/api-migration-compatibility/.oasdiff-severity-levels.yaml:6` — `api-tag-removed: WARN`
- `.github/api-migration-compatibility/.oasdiff-severity-levels.yaml:20` — `request-property-enum-value-removed: ERR`
- `.github/api-migration-compatibility/.oasdiff-severity-levels.yaml:31` — `request-property-pattern-removed: INFO`

**FINDING: 🔴 High Risk**

No evidence found of any consent revocation handling mechanisms in the analyzed code repository. The evidence consists entirely of configuration files (.dockerignore, GitHub workflow configurations, and API migration rules) with no implementation code related to TCPA consent management, revocation processing, or consumer communication opt-out functionality. This absence of required consent revocation controls creates a risk pattern consistent with non-compliance under TCPA 47 U.S.C. §227(b)(1)(A) and FCC 2015 TCPA Omnibus Declaratory Ruling.

**REMEDIATION DIRECTION**

Implement a comprehensive consent revocation system that accepts and processes opt-out requests through multiple channels (SMS replies like "STOP", email unsubscribe, web interface, phone calls). The system should use flexible keyword recognition beyond just "STOP" (including variations like "quit", "cancel", "unsubscribe"), process revocations immediately upon receipt, maintain an updated suppression list, and ensure all communication systems check this list before sending messages. Add logging and audit trails for all revocation requests and processing times to demonstrate compliance with FCC guidance on reasonable timeframes.

---

### TCPA-008: Time of Day Restrictions

**LEGAL QUESTION**

Does the system enforce time-of-day restrictions for outbound calls and messages, ensuring they are not sent before 8:00 AM or after 9:00 PM in the recipient's local time zone, as required under 47 CFR §64.1200(c)(1)?

**REGULATORY STANDARD**

TCPA 47 CFR §64.1200(c)(1) (Time of Day Restrictions)

**EVIDENCE**

- `.github/CODEOWNERS:150` — `crates/router/src/scheduler/ @juspay/hyperswitch-process-tracker`
- `.github/workflows/archive/connector-sanity-tests.yml:8` — `schedule:`
- `.github/workflows/release-nightly-version.yml:4` — `schedule:`
- `Dockerfile:57` — `# 2. BINARY=scheduler, SCHEDULER_FLOW=consumer - part of process tracker`
- `Dockerfile:58` — `# 3. BINARY=scheduler, SCHEDULER_FLOW=producer - part of process tracker`
- `Dockerfile:60` — `ARG SCHEDULER_FLOW=consumer`
- `Dockerfile:70` — `SCHEDULER_FLOW=${SCHEDULER_FLOW} \`
- `README.md:113` — `- **Full**: Includes monitoring + schedulers`
- `api-reference/v1/payments/payment--flows.mdx:233` — `**Use Case:** Subscription charges, scheduled billing without customer interaction`
- `api-reference/v1/payments/payment--flows.mdx:256` — `- **Capture Methods:** System supports `automatic` (funds captured immediately), `manual` (funds captured in a separate `

**FINDING: 🔴 High Risk**

The evidence reveals a payments processing system with scheduling capabilities (scheduler components in Dockerfile:57-58, config/config.example.toml:438-456) and scheduled billing functionality (api-reference/v1/payments/payment--flows.mdx:233), but contains no implementation of TCPA time-of-day restrictions for outbound communications. No code was found enforcing the required 8:00 AM to 9:00 PM restriction in recipient local time zones, creating a risk pattern consistent with non-compliance under 47 CFR §64.1200(c)(1).

**REMEDIATION DIRECTION**

Implement time-of-day validation controls within the scheduler system that check recipient local time zones before sending any outbound calls or messages. Add configuration parameters to enforce the 8:00 AM to 9:00 PM window, integrate timezone lookup functionality for recipients, and create validation logic that blocks or delays communications outside permitted hours. The scheduler components identified in the codebase should be enhanced with these TCPA compliance checks before any outbound communication processing.

---

**DISCLAIMER:** OpenDocket identifies risk patterns through automated code analysis. Findings represent potential areas of concern, not legal determinations. This report does not constitute legal advice. Regulatory compliance requires qualified legal and technical assessment. Consult a licensed attorney and certified compliance professional for definitive compliance determination.
