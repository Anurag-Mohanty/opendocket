# OpenDocket Compliance Report: medplum

> **Repository:** https://github.com/medplum/medplum
> **Scan Date:** 2026-03-22
> **Scanner Version:** OpenDocket V1

---

**DISCLAIMER:** OpenDocket identifies risk patterns through automated code analysis. Findings represent potential areas of concern, not legal determinations. This report does not constitute legal advice. Regulatory compliance requires qualified legal and technical assessment. Consult a licensed attorney and certified compliance professional for definitive compliance determination.

---

## Domain Detection

- **Saas** — Confidence: 92.2% (8540 signals, top: organization, subscription, auth, plan, team)
- **Healthcare** — Confidence: 90.0% (60758 signals, top: patient, fhir, hl7, encounter, medication)
- **Ecommerce** — Confidence: 69.8% (2566 signals, top: order, product, catalog, checkout, marketplace)
- **Fintech** — Confidence: 53.0% (1216 signals, top: transaction, card, payment, stripe, ach)
- **Communication** — Confidence: 41.1% (1361 signals, top: consent, call, messaging, notification, twilio)
- **Gdpr** — Confidence: 14.2% (425 signals, top: consent, gdpr, portability)

## Frameworks Analyzed: GDPR, HIPAA, PCI-DSS, SOC2, SOX, TCPA

## Executive Summary

| Finding Level | Count |
|---|---|
| High Risk | 47 |
| Medium Risk | 6 |
| Pattern of Concern | 3 |
| No Issue Found | 0 |

## GDPR Findings

### GDPR-001: Lawful Basis for Processing Personal Data

**LEGAL QUESTION**

Does this system process personal data of EU residents, and if so, is there evidence that a lawful basis for processing under Article 6 GDPR has been identified and implemented for each processing activity?

**REGULATORY STANDARD**

GDPR Article 6 (Lawfulness of Processing)

**EVIDENCE**

- `SECURITY.md:15` — `- Data Handling - Medplum is in full compliance with GDPR and has support for data deletion.`
- `examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx:470` — `linkId: 'consent-for-treatment',`
- `examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx:471` — `text: 'Consent for Treatment',`
- `examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx:475` — `linkId: 'consent-for-treatment-signature',`
- `examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx:476` — `text: 'I the undersigned patient (or authorized representative, or parent/guardian), consent to and authorize the perfor`
- `examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx:480` — `linkId: 'consent-for-treatment-date',`
- `examples/medplum-chat-demo/data/example/example-data.json:2687` — `"display": "consent overrider"`
- `examples/medplum-chat-demo/data/example/example-data.json:2735` — `"display": "legal guardian consent author"`
- `examples/medplum-chat-demo/data/example/example-data.json:2759` — `"display": "healthcare power of attorney consent author"`
- `examples/medplum-chat-demo/data/example/example-data.json:2763` — `"display": "personal representative consent author"`

**FINDING: 🔴 High Risk**

The system processes personal data of EU residents (as evidenced by patient intake forms and healthcare data handling in examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx), but no evidence was found of documented lawful bases under GDPR Article 6 for each processing activity. While SECURITY.md:15 claims "full compliance with GDPR," this constitutes a risk pattern consistent with non-compliance under GDPR Article 6, as mere consent collection for medical treatment does not establish the required lawful basis documentation for all personal data processing activities.

**REMEDIATION DIRECTION**

The development team must conduct a comprehensive data processing audit to identify all personal data processing activities within the system, then document the specific lawful basis under GDPR Article 6 (such as consent, legitimate interest, or vital interests) for each activity. This documentation should be implemented in code comments, configuration files, or a dedicated privacy configuration module that maps each data processing function to its corresponding lawful basis. Additionally, ensure that consent mechanisms are properly structured to meet GDPR requirements rather than just medical consent standards.

---

### GDPR-002: Consent Collection and Management

**LEGAL QUESTION**

Does the system implement consent collection mechanisms that satisfy the conditions for consent under Article 7, including freely given, specific, informed, and unambiguous indication of the data subject's wishes, with capability to withdraw consent?

**REGULATORY STANDARD**

GDPR Article 7 (Conditions for Consent)

**EVIDENCE**

- `.github/workflows/chromatic.yml:58` — `autoAcceptChanges: 'main'`
- `.github/workflows/madge.yml:76` — `Please fix the listed circular module dependencies so that your PR can be accepted. Thank you!`
- `LICENSE.txt:135` — `the terms of any separate license agreement you may have executed`
- `LICENSE.txt:144` — `agreed to in writing, Licensor provides the Work (and each`
- `LICENSE.txt:156` — `negligent acts) or agreed to in writing, shall any Contributor be`
- `LICENSE.txt:171` — `of any other Contributor, and only if You agree to indemnify,`
- `LICENSE.txt:165` — `9. Accepting Warranty or Additional Liability. While redistributing`
- `LICENSE.txt:167` — `and charge a fee for, acceptance of support, warranty, indemnity,`
- `LICENSE.txt:169` — `License. However, in accepting such obligations, You may act only`
- `LICENSE.txt:174` — `of your accepting any such warranty or additional liability.`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under GDPR Article 7. While medical treatment consent forms are present in examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx (lines 470-488), no evidence was found of GDPR-compliant data processing consent mechanisms that satisfy the requirements for freely given, specific, informed, and unambiguous consent collection, nor any consent withdrawal capabilities for personal data processing activities.

**REMEDIATION DIRECTION**

Implement a comprehensive consent management system that includes: (1) clear consent collection interfaces that separately address data processing purposes beyond medical treatment, (2) granular consent options allowing users to consent to specific data processing activities, (3) plain language explanations of what data is collected and how it's used, (4) easily accessible consent withdrawal mechanisms, and (5) audit trails for all consent decisions. The existing medical treatment consent forms should be supplemented with dedicated GDPR consent flows for data processing activities.

---

### GDPR-003: Right to Erasure Implementation

**LEGAL QUESTION**

Does the system implement the right to erasure (right to be forgotten) under Article 17, allowing data subjects to request deletion of their personal data without undue delay?

**REGULATORY STANDARD**

GDPR Article 17 (Right to Erasure)

**EVIDENCE**

- `examples/medplum-demo-bots/src/adt-transfer-listener/adt-sftp-listener.ts:76` — `stream.destroy();`
- `examples/medplum-demo-bots/src/lab-integration/receive-oru-message.ts:297` — `stream.destroy();`
- `examples/medplum-demo-bots/src/spaces-bots/fhir-visualizer-bot.ts:269` — `6. ❌ Forgetting to aggregate categorical data into counts`
- `packages/agent/src/bytestream.test.ts:101` — `client.destroy();`
- `packages/agent/src/bytestream.test.ts:176` — `client.destroy();`
- `packages/agent/src/bytestream.test.ts:249` — `client.destroy();`
- `packages/agent/src/bytestream.test.ts:326` — `client.destroy();`
- `packages/agent/src/bytestream.test.ts:409` — `client.destroy();`
- `packages/agent/src/hl7.test.ts:1002` — `conn.socket.destroy();`
- `packages/agent/src/hl7.test.ts:1122` — `socket.destroy();`

**FINDING: 🔴 High Risk**

The system shows a risk pattern consistent with non-compliance under GDPR Article 17 (Right to Erasure). While administrative purge functionality exists in packages/app/src/admin/SuperAdminPage.tsx (lines 93-203), no evidence was found of user-accessible data deletion mechanisms that would allow data subjects to request erasure of their personal data without undue delay. The existing purge functionality appears limited to system administrative operations rather than individual data subject rights fulfillment.

**REMEDIATION DIRECTION**

Implement a user-facing data deletion API endpoint and corresponding UI components that allow authenticated data subjects to request deletion of their personal data. This should include mechanisms to verify the requestor's identity, validate erasure requests against legitimate grounds under Article 17, handle cascading deletions across related records, and provide confirmation of successful deletion. Consider implementing soft-delete patterns with audit trails to demonstrate compliance while maintaining data integrity for ongoing legal obligations.

---

### GDPR-004: Data Portability Capability

**LEGAL QUESTION**

Does the system provide data subjects the right to receive their personal data in a structured, commonly used, and machine-readable format, and to transmit that data to another controller, as required under Article 20?

**REGULATORY STANDARD**

GDPR Article 20 (Right to Data Portability)

**EVIDENCE**

- `.github/workflows/scorecard.yml:63` — `# (Optional) Uncomment file_mode if you have a .gitattributes with files marked export-ignore`
- `Dockerfile:7` — `# The archive files are decompressed and extracted into the specified destinations.`
- `Dockerfile:9` — `# See: https://docs.docker.com/reference/dockerfile/#adding-local-tar-archives`
- `eslint.config.mjs:5` — `export default defineConfig(medplumEslintConfig);`
- `examples/foomedical/postcss.config.mjs:21` — `export default config;`
- `examples/foomedical/src/App.tsx:16` — `export function App(): JSX.Element | null {`
- `examples/foomedical/src/Router.tsx:32` — `export function Router(): JSX.Element {`
- `examples/foomedical/src/components/Footer.tsx:7` — `export function Footer(): JSX.Element {`
- `examples/foomedical/src/components/Header.tsx:21` — `export function Header(): JSX.Element {`
- `examples/foomedical/src/components/InfoButton.tsx:7` — `export interface InfoButtonProps {`

**FINDING: 🔴 High Risk**

No evidence found of data portability functionality that would enable data subjects to receive their personal data in a structured, commonly used, and machine-readable format as required under GDPR Article 20. While the repository contains numerous export statements for code modules and components (across files like App.tsx, Router.tsx, and various component files), no data export APIs, user-facing data portability features, or personal data extraction mechanisms were identified. This represents a risk pattern consistent with non-compliance under GDPR Article 20 data portability requirements.

**REMEDIATION DIRECTION**

Implement data portability functionality that allows authenticated users to request and receive their personal data in structured formats (JSON, CSV, XML). This should include: API endpoints for data export requests, user interface components for initiating data exports, mechanisms to package personal data across all system components, and clear documentation of supported export formats. The system should also support transmitting this data directly to other controllers when technically feasible, and maintain audit logs of all portability requests.

---

### GDPR-005: Privacy by Design Evidence

**LEGAL QUESTION**

Does the system demonstrate evidence of data protection by design and by default, implementing appropriate technical and organizational measures to ensure only necessary personal data is processed, as required under Article 25?

**REGULATORY STANDARD**

GDPR Article 25 (Data Protection by Design and by Default)

**EVIDENCE**

- `.github/workflows/scorecard.yml:2` — `# by a third-party and are governed by separate terms of service, privacy`
- `SECURITY.md:70` — `We consider security research conducted under this policy to be authorized and will not pursue or support legal action a`
- `SECURITY.md:13` — `- Encryption - Data is encrypted in transit with TLS 1.2 and 1.3. Data is encrypted at rest with AES.`
- `examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx:504` — `linkId: 'notice-of-privacy-practices',`
- `examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx:505` — `text: 'Notice of Privacy Practices',`
- `examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx:509` — `linkId: 'notice-of-privacy-practices-help',`
- `examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx:510` — `text: 'Sample Hospital Notice of Privacy Practices gives information about how Sample Hospital may use and release prote`
- `examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx:514` — `linkId: 'notice-of-privacy-practices-signature',`
- `examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx:515` — `text: 'I acknowledge the above and that I have received a copy of Sample Hospital’s Notice of Privacy Practices.',`
- `examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx:519` — `linkId: 'notice-of-privacy-practices-date',`

**FINDING: 🟠 Medium Risk**

The evidence shows some privacy-by-design elements including data encryption in transit and at rest (SECURITY.md:13) and data sanitization functions (questionnaire-response.ts:308-446), but lacks comprehensive technical measures for data minimization and purpose limitation as required under GDPR Article 25. While privacy notices are present in patient intake forms, there is insufficient evidence of systematic data protection by design and by default controls throughout the codebase that would ensure only necessary personal data is processed.

**REMEDIATION DIRECTION**

Implement comprehensive data protection by design measures including: automated data minimization controls that limit data collection to stated purposes, retention period enforcement mechanisms, privacy impact assessment integration in development workflows, and systematic access controls that default to minimal data exposure. Add configuration options that enable privacy-protective defaults, implement data pseudonymization where possible, and establish clear data lifecycle management processes that demonstrate compliance with Article 25's requirements for both technical and organizational measures.

---

### GDPR-006: Data Breach Detection and Notification

**LEGAL QUESTION**

Does the system implement mechanisms for detecting personal data breaches and notifying the supervisory authority within 72 hours and affected data subjects without undue delay, as required under Articles 33 and 34?

**REGULATORY STANDARD**

GDPR Articles 33 (Notification to Authority); 34 (Communication to Data Subject)

**EVIDENCE**

- `LICENSE.txt:158` — `incidental, or consequential damages of any character arising as a`
- `README.md:1` — `# [Medplum](https://www.medplum.com) &middot; [![GitHub license](https://img.shields.io/badge/license-Apache-blue.svg)](`
- `SECURITY.md:14` — `- Continuous Monitoring - Independent third-party penetration, threat, and vulnerability testing.`
- `SECURITY.md:27` — `- Continuous Monitoring - We continuously monitor our security and compliance status to ensure there are no lapses.`
- `biome.json:31` — `"suspicious": {`
- `examples/foomedical/README.md:11` — `<img src="https://sonarcloud.io/api/project_badges/measure?project=medplum_foomedical&metric=alert_status&token=3760929a`
- `examples/foomedical/package.json:25` — `"@mantine/notifications": "8.3.18",`
- `examples/foomedical/src/main.tsx:5` — `import { Notifications } from '@mantine/notifications';`
- `examples/foomedical/src/main.tsx:6` — `import '@mantine/notifications/styles.css';`
- `examples/foomedical/src/main.tsx:46` — `<Notifications />`

**FINDING: 🔴 High Risk**

Analysis reveals a risk pattern consistent with non-compliance under GDPR Articles 33 and 34. No evidence was found of automated breach detection mechanisms, breach notification workflows, or systems for notifying supervisory authorities within 72 hours. While the codebase contains basic UI notification components (examples/foomedical/src/pages/QuestionnairePage.tsx:29, examples/foomedical/src/pages/account/Profile.tsx:37) and references continuous monitoring in SECURITY.md:27, these do not constitute the specific data breach detection and notification capabilities required by GDPR.

**REMEDIATION DIRECTION**

Implement a comprehensive data breach detection and notification system that includes: automated monitoring for unauthorized access to personal data, breach classification and risk assessment workflows, automated notification mechanisms to supervisory authorities within 72 hours, and systems for notifying affected data subjects without undue delay. This should include audit logging, breach incident tracking, notification templates, and integration with relevant data protection authorities' reporting systems. Document these processes and ensure they cover both automated detection and manual breach reporting procedures.

---

### GDPR-007: Data Retention and Deletion Policies

**LEGAL QUESTION**

Does the system implement data retention policies that limit the storage of personal data to what is necessary for the specified processing purpose, with automated deletion or anonymization when the purpose is fulfilled, consistent with the storage limitation principle under Article 5(1)(e)?

**REGULATORY STANDARD**

GDPR Article 5(1)(e) (Storage Limitation Principle)

**EVIDENCE**

- `.github/auto_assign.yml:9` — `- mattlong`
- `.github/workflows/build.yml:383` — `retention-days: 30`
- `.github/workflows/codeql-analysis.yml:27` — `- cron: '30 14 * * 4'`
- `.github/workflows/scorecard.yml:73` — `retention-days: 5`
- `.github/workflows/scorecard.yml:13` — `- cron: '22 11 * * 3'`
- `.github/workflows/upgrade-dependencies.yml:17` — `- cron: '0 9 * * 1'`
- `Dockerfile:7` — `# The archive files are decompressed and extracted into the specified destinations.`
- `Dockerfile:9` — `# See: https://docs.docker.com/reference/dockerfile/#adding-local-tar-archives`
- `examples/foomedical/src/pages/ScreeningQuestionnairePage.tsx:1298` — `display: 'I could use a little more help',`
- `examples/foomedical/src/pages/ScreeningQuestionnairePage.tsx:2073` — `display: 'Little interest or pleasure in doing things?',`

**FINDING: 🔴 High Risk**

The evidence reveals a risk pattern consistent with non-compliance under GDPR Article 5(1)(e) storage limitation principle. While some GitHub workflow artifacts show retention policies (30 days in build.yml:383, 5 days in scorecard.yml:73), no evidence was found of comprehensive data retention policies for personal data processed by the healthcare platform itself. The codebase contains medical questionnaire data and patient-related functionality but lacks automated deletion or anonymization mechanisms for personal data when processing purposes are fulfilled.

**REMEDIATION DIRECTION**

Implement comprehensive data retention policies that cover all personal data types processed by the Medplum platform, not just CI/CD artifacts. Add automated deletion or anonymization workflows triggered when data retention periods expire or processing purposes are fulfilled. Configure data lifecycle management rules in the Clinical Data Repository (CDR) with clear retention schedules based on healthcare regulatory requirements and business purposes. Document retention periods for different data categories and implement monitoring to ensure automated compliance with storage limitation requirements.

---

### GDPR-008: Cross-Border Data Transfer Safeguards

**LEGAL QUESTION**

Does the system implement appropriate safeguards for transfers of personal data to third countries or international organizations, such as Standard Contractual Clauses or adequacy decisions, as required under Chapter V?

**REGULATORY STANDARD**

GDPR Chapter V, Articles 44-49 (Transfers to Third Countries)

**EVIDENCE**

- `.github/workflows/build-deb.yml:67` — `aws-region: ${{ secrets.AWS_REGION }}`
- `.github/workflows/build-deb.yml:67` — `aws-region: ${{ secrets.AWS_REGION }}`
- `.github/workflows/build-helm-charts.yml:44` — `aws-region: ${{ secrets.AWS_REGION }}`
- `.github/workflows/build-helm-charts.yml:44` — `aws-region: ${{ secrets.AWS_REGION }}`
- `.github/workflows/deploy.yml:55` — `aws-region: ${{ secrets.AWS_REGION }}`
- `.github/workflows/deploy.yml:74` — `AWS_REGION: ${{ secrets.AWS_REGION }}`
- `.github/workflows/deploy.yml:55` — `aws-region: ${{ secrets.AWS_REGION }}`
- `.github/workflows/deploy.yml:74` — `AWS_REGION: ${{ secrets.AWS_REGION }}`
- `.github/workflows/publish-meta.yml:29` — `aws-region: ${{ secrets.AWS_REGION }}`
- `.github/workflows/publish-meta.yml:29` — `aws-region: ${{ secrets.AWS_REGION }}`

**FINDING: 🔴 High Risk**

The system demonstrates a risk pattern consistent with non-compliance under GDPR Articles 44-49 regarding cross-border data transfer safeguards. Evidence shows extensive AWS infrastructure deployment across multiple regions (including us-east-1 references in packages/cdk/src/backend.ts:486 and test files), indicating potential transfers of personal data to third countries, but no corresponding Standard Contractual Clauses, adequacy decision documentation, or other Chapter V transfer safeguards were found in the codebase. The healthcare application appears to process clinical data through AWS services without visible implementation of required international transfer protections.

**REMEDIATION DIRECTION**

Implement and document appropriate GDPR Chapter V transfer mechanisms before deploying to AWS regions outside the EEA. This requires either: (1) implementing Standard Contractual Clauses with AWS as the data processor, (2) documenting reliance on adequacy decisions where applicable, or (3) obtaining explicit user consent for transfers with appropriate disclosures. Add configuration files or documentation that clearly specify which transfer safeguards apply to each AWS region deployment, and ensure all cross-border data flows are mapped and legally justified under one of the Chapter V transfer mechanisms.

---

### GDPR-009: Data Protection Impact Assessment Indicators

**LEGAL QUESTION**

Does the system process personal data in a manner likely to result in high risk to data subjects, and if so, is there evidence that a Data Protection Impact Assessment has been considered, as required under Article 35?

**REGULATORY STANDARD**

GDPR Article 35 (Data Protection Impact Assessment)

**EVIDENCE**

- `.gitignore:105` — `# 0x profiling data`
- `LICENSE.txt:57` — `and issue tracking systems that are managed by, or on behalf of, the`
- `examples/medplum-demo-bots/src/bmi-calculation-bot/README.md:21` — `- Allows tracking BMI changes over time`
- `examples/medplum-demo-bots/src/bmi-calculation-bot/README.md:59` — `- **If BMI calculation succeeds**: The bot creates a new BMI observation with the calculated value (allows tracking BMI `
- `examples/medplum-demo-bots/src/bmi-calculation-bot/bmi-calculation-bot.ts:179` — `// Create a new BMI observation (allows tracking BMI over time)`
- `examples/medplum-demo-bots/src/pre-commit-hook-bot-boolean.ts:33` — `* tracking purposes.`
- `examples/medplum-demo-bots/src/pre-commit-hook-bot-boolean.ts:42` — `// Add Medplum identifier to the patient for tracking`
- `examples/medplum-demo-bots/src/pre-commit-hook-bot-resource.ts:17` — `* - Adds bidirectional identifiers for tracking`
- `examples/medplum-demo-bots/src/pre-commit-hook-bot-resource.ts:40` — `* tracking between Medplum and HAPI.`
- `examples/medplum-demo-bots/src/pre-commit-hook-bot-resource.ts:49` — `// Add Medplum identifier to the patient for tracking on HAPI server`

**FINDING: 🔴 High Risk**

The system processes sensitive healthcare data including patient records, BMI calculations, clinical observations, and medical identifiers as evidenced throughout the codebase (examples/medplum-demo-bots/, examples/medplum-patient-intake-demo/, examples/medplum-healthie-importer/). This constitutes high-risk processing of personal health data under GDPR Article 35, yet no evidence of a Data Protection Impact Assessment (DPIA) consideration or documentation was found in the repository. This represents a risk pattern consistent with non-compliance under GDPR Article 35.

**REMEDIATION DIRECTION**

Conduct and document a comprehensive Data Protection Impact Assessment as required by GDPR Article 35 for high-risk data processing activities. The DPIA should evaluate privacy risks associated with processing patient health data, BMI tracking, clinical observations, and cross-system patient identifiers. Document the assessment results, risk mitigation measures, and ongoing monitoring procedures. Include DPIA documentation in the project repository and ensure it's reviewed whenever processing activities change significantly.

---

### GDPR-010: Privacy Policy and Notice Requirements

**LEGAL QUESTION**

Does the system provide transparent information to data subjects about the processing of their personal data, including identity of the controller, purposes of processing, and data subject rights, as required under Articles 13 and 14?

**REGULATORY STANDARD**

GDPR Articles 13 (Information at Collection); 14 (Information Not from Data Subject)

**EVIDENCE**

- `.github/workflows/build-agent.yml:162` — `endpoint: https://eus.codesigning.azure.net/`
- `.github/workflows/publish.yml:288` — `endpoint: https://eus.codesigning.azure.net/`
- `LICENSE.txt:116` — `of the NOTICE file are for informational purposes only and`
- `LICENSE.txt:37` — `copyright notice that is included in or attached to the work`
- `LICENSE.txt:97` — `(b) You must cause any modified files to carry prominent notices`
- `LICENSE.txt:102` — `attribution notices from the Source form of the Work,`
- `LICENSE.txt:103` — `excluding those notices that do not pertain to any part of`
- `LICENSE.txt:106` — `(d) If the Work includes a "NOTICE" text file as part of its`
- `LICENSE.txt:108` — `include a readable copy of the attribution notices contained`
- `LICENSE.txt:109` — `within such NOTICE file, excluding those notices that do not`

**FINDING: 🔴 High Risk**

The code repository shows a risk pattern consistent with non-compliance under GDPR Articles 13 and 14. No privacy policy, data processing notices, or transparent information about data controller identity, processing purposes, or data subject rights were found in the codebase. While the repository contains a healthcare platform (Medplum) that processes personal data through authentication systems and clinical data repositories, the only notices found relate to Apache license attributions in LICENSE.txt rather than GDPR-required transparency information.

**REMEDIATION DIRECTION**

Implement comprehensive privacy notices that clearly identify the data controller, specify purposes for processing personal data, and inform users of their rights under GDPR. Create a privacy policy accessible through the application that covers data collection at the point of capture (Article 13) and when data is obtained from other sources (Article 14). Add privacy notice components to user-facing interfaces, particularly in the Medplum Auth system and any data collection points in the web application.

---

## HIPAA Findings

### HIPAA-001: PHI Identification and Protection

**LEGAL QUESTION**

Does this system collect, store, process, or transmit individually identifiable health information as defined under 45 CFR §160.103, and if so, are adequate technical safeguards in place to protect the confidentiality of such Protected Health Information?

**REGULATORY STANDARD**

HIPAA Privacy Rule 45 CFR §160.103; Security Rule 45 CFR §164.312(a)(1)

**EVIDENCE**

- `.github/labeler.yml:38` — `medications:`
- `.gitignore:23` — `packages/graphiql/public/`
- `.gitignore:23` — `packages/graphiql/public/`
- `README.md:102` — `│   ├── graphiql        # Preconfigured GraphiQL`
- `README.md:102` — `│   ├── graphiql        # Preconfigured GraphiQL`
- `SECURITY.md:23` — `- Security Awareness Training - Our team members are required to go through employee security awareness training coverin`
- `SECURITY.md:57` — `- Social engineering, phishing, or physical attacks against Medplum employees, users, or infrastructure.`
- `SECURITY.md:66` — `Our philosophy on this is aligned with the principles outlined in Troy Hunt's post on "Beg Bounties," which you can read`
- `SECURITY.md:23` — `- Security Awareness Training - Our team members are required to go through employee security awareness training coverin`
- `SECURITY.md:57` — `- Social engineering, phishing, or physical attacks against Medplum employees, users, or infrastructure.`

**FINDING: 🔴 High Risk**

This system exhibits a risk pattern consistent with non-compliance under 45 CFR §160.103 and §164.312(a)(1). Clear evidence shows the system processes Protected Health Information including patient registration, medications, patient-provider messaging, and patient scheduling (examples/foomedical/README.md:25-33). However, no technical safeguards implementation was found in the repository evidence to protect PHI confidentiality as required by HIPAA Security Rule.

**REMEDIATION DIRECTION**

Implement and document technical safeguards required under HIPAA Security Rule §164.312(a)(1) including access controls, audit controls, integrity controls, person authentication, and transmission security. Add encryption at rest and in transit, role-based access controls, audit logging mechanisms, and secure authentication systems. Document these safeguards in the codebase with clear implementation evidence, particularly for the patient data handling components identified in the foomedical example application.

---

### HIPAA-002: Encryption at Rest

**LEGAL QUESTION**

Is electronic Protected Health Information encrypted when stored at rest using methods consistent with NIST Special Publication 800-111, as required for addressable implementation under the HIPAA Security Rule?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.312(a)(2)(iv); NIST SP 800-111

**EVIDENCE**

- `SECURITY.md:13` — `- Encryption - Data is encrypted in transit with TLS 1.2 and 1.3. Data is encrypted at rest with AES.`
- `SECURITY.md:13` — `- Encryption - Data is encrypted in transit with TLS 1.2 and 1.3. Data is encrypted at rest with AES.`
- `SECURITY.md:55` — `- Reports of insecure SSL/TLS ciphers or protocol versions.`
- `SECURITY.md:13` — `- Encryption - Data is encrypted in transit with TLS 1.2 and 1.3. Data is encrypted at rest with AES.`
- `charts/values.yaml:12` — `# type: "azure:keyVaultURL:secretName"`
- `examples/medplum-demo-bots/src/billing-bots/superbill.test.ts:13` — `import { randomUUID } from 'crypto';`
- `examples/medplum-demo-bots/src/epic/epic-query-patient.test.ts:20` — `import { generateKeyPairSync } from 'crypto';`
- `examples/medplum-demo-bots/src/epic/epic-query-patient.ts:6` — `import { createPrivateKey, randomBytes } from 'crypto';`
- `examples/medplum-demo-bots/src/hl7-integration/setup-medplum-agent.test.ts:13` — `import { randomUUID } from 'crypto';`
- `examples/medplum-demo-bots/src/metriport-bots/metriport-consolidated-data-webhook.test.ts:13` — `import { randomUUID } from 'crypto';`

**FINDING: 🟠 Medium Risk**

Risk pattern consistent with non-compliance under HIPAA Security Rule 45 CFR §164.312(a)(2)(iv) and NIST SP 800-111. While SECURITY.md:13 documents that "Data is encrypted at rest with AES," this documentation lacks critical specifics required by NIST SP 800-111, including AES key size (128, 192, or 256-bit), key management procedures, and implementation details. The evidence shows multiple anti-patterns involving base64 encoding in lab integration files (examples/medplum-demo-bots/src/lab-integration/) which may indicate confusion between encoding and encryption methods.

**REMEDIATION DIRECTION**

Update security documentation to specify the exact AES implementation (AES-128, AES-192, or AES-256), document key management procedures including key generation, storage, rotation, and destruction processes as required by NIST SP 800-111. Provide technical implementation details showing how encryption keys are protected and managed. Review the base64 usage in lab integration components to ensure developers understand the distinction between data encoding and encryption. Consider implementing automated compliance checks to verify encryption configurations match documented standards.

---

### HIPAA-003: Encryption in Transit

**LEGAL QUESTION**

Are all transmissions of electronic Protected Health Information encrypted using transport-level security consistent with NIST guidelines, preventing unauthorized access during transmission across electronic communications networks?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.312(e)(1); 45 CFR §164.312(e)(2)(ii)

**EVIDENCE**

- `.github/CODEOWNERS:2` — `# See: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-reposito`
- `.github/workflows/add-issue-to-project.yml:21` — `project-url: https://github.com/orgs/medplum/projects/1`
- `.github/workflows/add-issue-to-project.yml:25` — `project-url: https://github.com/orgs/medplum/projects/3`
- `.github/workflows/build-agent.yml:50` — `registry-url: 'https://registry.npmjs.org'`
- `.github/workflows/build-agent.yml:52` — `# See: https://github.com/actions/cache/blob/cdf6c1fa76f9f475f3d7449005a359c84ca0f306/examples.md#node---npm`
- `.github/workflows/build-agent.yml:93` — `* Taken from https://github.com/dlemstra/code-sign-action`
- `.github/workflows/build-agent.yml:162` — `endpoint: https://eus.codesigning.azure.net/`
- `.github/workflows/build-agent.yml:231` — `registry-url: 'https://registry.npmjs.org'`
- `.github/workflows/build-agent.yml:313` — `registry-url: 'https://registry.npmjs.org'`
- `.github/workflows/build-agent.yml:395` — `registry-url: 'https://registry.npmjs.org'`

**FINDING: 🔴 High Risk**

Analysis reveals a risk pattern consistent with non-compliance under HIPAA Security Rule 45 CFR §164.312(e)(1) and (e)(2)(ii). While the code repository contains numerous HTTPS URLs indicating proper transport-level encryption for external communications, no evidence was found of specific PHI transmission encryption controls or NIST-compliant transport security configurations. Additionally, multiple anti-patterns were detected including unencrypted HTTP endpoints in docker-compose.full-stack.yml (lines 55-57, 92) and build workflows (build.yml:358) that could facilitate unencrypted PHI transmission.

**REMEDIATION DIRECTION**

Implement explicit transport-level encryption controls for all PHI transmissions by configuring TLS 1.2+ with NIST-approved cipher suites across all application endpoints. Replace all HTTP endpoints in configuration files (particularly docker-compose.full-stack.yml and CI/CD workflows) with HTTPS equivalents, and add code documentation demonstrating compliance with NIST SP 800-52 guidelines for secure transport protocols. Establish mandatory HTTPS redirects and disable insecure protocol versions to ensure all PHI transmissions occur over encrypted channels.

---

### HIPAA-004: Access Controls and Authentication

**LEGAL QUESTION**

Does the system implement technical policies and procedures for electronic information systems that maintain electronic Protected Health Information to allow access only to those persons or software programs that have been granted access rights as specified in 45 CFR §164.312(a)(1)?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.312(a)(1); 45 CFR §164.312(a)(2)(i)

**EVIDENCE**

- `.github/labeler.yml:22` — `- packages/server/src/oauth/**/*`
- `.github/labeler.yml:24` — `- packages/server/src/fhir/accesspolicy.ts`
- `.github/workflows/add-issue-to-project.yml:11` — `permissions:`
- `.github/workflows/add-issue-to-project.yml:22` — `github-token: ${{ secrets.MEDPLUM_BOT_GITHUB_ACCESS_TOKEN }}`
- `.github/workflows/add-issue-to-project.yml:26` — `github-token: ${{ secrets.MEDPLUM_BOT_GITHUB_ACCESS_TOKEN }}`
- `.github/workflows/assign-pull-request.yml:7` — `permissions:`
- `.github/workflows/assign-pull-request.yml:14` — `permissions:`
- `.github/workflows/autofix-ci.yml:11` — `permissions:`
- `.github/workflows/autofix-ci.yml:17` — `permissions:`
- `.github/workflows/build-agent.yml:31` — `id-token: write # Required for OIDC authentication with Azure Trusted Signing`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under 45 CFR §164.312(a)(1). While the system references OAuth infrastructure (packages/server/src/oauth/**/*) and an access policy file (packages/server/src/fhir/accesspolicy.ts), no actual implementation details or technical safeguards for restricting access to electronic Protected Health Information are visible in the provided evidence. The presence of authentication-related file references without demonstrable access control mechanisms creates substantial compliance risk.

**REMEDIATION DIRECTION**

The development team must implement and document technical access controls that explicitly restrict access to ePHI based on granted access rights. This includes implementing role-based access controls, user authentication mechanisms, and authorization checks within the FHIR access policy module. The OAuth implementation should be configured to enforce granular permissions, and access control policies must be clearly defined and implemented in the accesspolicy.ts file. Additionally, technical documentation demonstrating how these controls prevent unauthorized access to ePHI should be created and maintained.

---

### HIPAA-005: Session Management

**LEGAL QUESTION**

Does the system implement electronic procedures that terminate an electronic session after a predetermined time of inactivity, as required for PHI-accessing interfaces under the HIPAA Security Rule?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.312(a)(2)(iii)

**EVIDENCE**

- `.github/workflows/build-agent.yml:22` — `timeout-minutes: 45`
- `.github/workflows/build-agent.yml:214` — `timeout-minutes: 45`
- `.github/workflows/build-agent.yml:296` — `timeout-minutes: 45`
- `.github/workflows/build-agent.yml:378` — `timeout-minutes: 45`
- `.github/workflows/build-deb.yml:19` — `timeout-minutes: 45`
- `.github/workflows/build-helm-charts.yml:19` — `timeout-minutes: 45`
- `.github/workflows/build.yml:21` — `timeout-minutes: 45`
- `.github/workflows/build.yml:79` — `timeout-minutes: 20`
- `.github/workflows/build.yml:157` — `timeout-minutes: 45`
- `.github/workflows/build.yml:180` — `--health-timeout 5s`

**FINDING: 🔴 High Risk**

The evidence shows only CI/CD pipeline timeout configurations in GitHub workflow files, but no implementation of user session timeout controls for PHI-accessing interfaces. This represents a risk pattern consistent with non-compliance under HIPAA Security Rule 45 CFR §164.312(a)(2)(iii), which requires automatic termination of electronic sessions after predetermined inactivity periods. While Medplum is identified as a healthcare platform handling clinical data, no session management code or configuration was found in the repository evidence.

**REMEDIATION DIRECTION**

Implement automatic session timeout functionality for all user-facing applications that access PHI. This should include configurable inactivity timeouts (typically 15-30 minutes for healthcare applications), automatic session termination when timeouts are reached, and proper session state cleanup. Add session timeout configuration to authentication components, middleware, or application settings, and ensure the timeout values are appropriate for healthcare workflows while meeting HIPAA requirements.

---

### HIPAA-006: Audit Logging

**LEGAL QUESTION**

Does the system implement hardware, software, and procedural mechanisms that record and examine activity in information systems that contain or use electronic Protected Health Information, as required under the audit controls standard?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.312(b)

**EVIDENCE**

- `.vscode/settings.json:24` — `"cSpell.words": ["auditevent", "bullmq", "FHIR", "Fhircast", "Medplum"]`
- `SECURITY.md:7` — `Medplum uses enterprise-grade security and regular audits to ensure you're always protected. We undergo regular penetrat`
- `SECURITY.md:24` — `- Third-Party Audits - Our organization undergoes independent third-party assessments to test our security controls.`
- `charts/templates/backendconfig.yaml:23` — `logging:`
- `examples/medplum-demo-bots/src/resource-usage/resource-usage.ts:70` — `const auditEventCount = counts['AuditEvent'] || 0;`
- `examples/medplum-demo-bots/src/resource-usage/resource-usage.ts:71` — `const totalResourcesMinusAuditEvent = totalResources - auditEventCount;`
- `examples/medplum-demo-bots/src/resource-usage/resource-usage.ts:80` — `['Counted Resources (total excluding AuditEvent)', totalResourcesMinusAuditEvent.toString()],`
- `examples/medplum-demo-bots/src/resource-usage/resource-usage.ts:152` — `'AuditEvent',`
- `examples/medplum-healthie-importer/README.md:147` — `### Error Handling & Logging`
- `examples/medplum-healthie-importer/README.md:149` — `The importer includes comprehensive error handling and logging:`

**FINDING: 🟠 Medium Risk**

The system shows partial implementation of audit logging mechanisms required under HIPAA Security Rule 45 CFR §164.312(b). Evidence shows FHIR AuditEvent resource handling in resource-usage.ts:70-152 and general logging configuration in backendconfig.yaml:23, but lacks comprehensive audit trail implementation for PHI access, modification, and system activity. The evidence demonstrates awareness of audit requirements through enterprise security claims in SECURITY.md:7-24, but specific technical controls for recording and examining PHI-related activities are not sufficiently documented in the codebase.

**REMEDIATION DIRECTION**

Implement comprehensive audit logging that captures all PHI access, creation, modification, and deletion events. This should include detailed audit trails with user identification, timestamps, data accessed, and actions performed. Enhance the existing AuditEvent framework to automatically log all FHIR resource interactions involving PHI. Add audit log review procedures and automated monitoring capabilities. Document the complete audit control implementation including hardware, software, and procedural mechanisms as required by the standard.

---

### HIPAA-007: Minimum Necessary Access

**LEGAL QUESTION**

Does the system limit the Protected Health Information disclosed or accessed to the minimum necessary to accomplish the intended purpose, consistent with the minimum necessary standard under the Privacy Rule?

**REGULATORY STANDARD**

HIPAA Privacy Rule 45 CFR §164.502(b); 45 CFR §164.514(d)

**EVIDENCE**

- `.github/workflows/build-agent.yml:152` — `exclude-azure-cli-credential: true`
- `.github/workflows/build-agent.yml:153` — `exclude-environment-credential: true`
- `.github/workflows/build-agent.yml:154` — `exclude-workload-identity-credential: true`
- `.github/workflows/build-agent.yml:155` — `exclude-managed-identity-credential: true`
- `.github/workflows/build-agent.yml:156` — `exclude-shared-token-cache-credential: true`
- `.github/workflows/build-agent.yml:157` — `exclude-visual-studio-credential: true`
- `.github/workflows/build-agent.yml:158` — `exclude-visual-studio-code-credential: true`
- `.github/workflows/build-agent.yml:159` — `exclude-azure-powershell-credential: false`
- `.github/workflows/build-agent.yml:160` — `exclude-azure-developer-cli-credential: true`
- `.github/workflows/build-agent.yml:161` — `exclude-interactive-browser-credential: true`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under HIPAA Privacy Rule 45 CFR §164.502(b) and §164.514(d). While the repository contains authentication credential exclusions in GitHub workflows and FHIRPath filtering/projection functions in the core packages, there is no evidence of implemented minimum necessary access controls that specifically limit PHI disclosure to the minimum required for intended purposes. The anti-patterns detected in packages/core/src/fhirpath/functions.ts show data filtering and projection capabilities but lack demonstrated integration with minimum necessary access enforcement mechanisms.

**REMEDIATION DIRECTION**

Implement explicit minimum necessary access controls throughout the system by adding role-based data filtering that restricts PHI queries and responses based on user permissions and purpose of use. Add audit logging for all PHI access attempts with justification tracking. Enhance the existing FHIRPath filtering functions to automatically apply minimum necessary restrictions based on the requesting user's role and the specific healthcare workflow context. Document and enforce policies that define what constitutes "minimum necessary" for each user role and use case, then implement these as enforceable technical controls in the API layer.

---

### HIPAA-008: Business Associate Agreements

**LEGAL QUESTION**

Does the system integrate with third-party services that may receive, maintain, or transmit Protected Health Information, and if so, is there evidence that Business Associate Agreement requirements are addressed in the code or configuration?

**REGULATORY STANDARD**

HIPAA Privacy Rule 45 CFR §164.502(e); 45 CFR §164.504(e)

**EVIDENCE**

- `.github/labeler.yml:41` — `- examples/medplum-photon-integration/src/**/*`
- `.github/labeler.yml:43` — `integration:`
- `.github/workflows/build-agent.yml:31` — `id-token: write # Required for OIDC authentication with Azure Trusted Signing`
- `.github/workflows/build-agent.yml:137` — `- name: Login to Azure`
- `.github/workflows/build-agent.yml:139` — `uses: azure/login@a457da9ea143d694b1b9c7c869ebb04ebe844ef5 # v2.3.0`
- `.github/workflows/build-agent.yml:141` — `client-id: ${{ secrets.AZURE_CLIENT_ID }}`
- `.github/workflows/build-agent.yml:142` — `tenant-id: ${{ secrets.AZURE_TENANT_ID }}`
- `.github/workflows/build-agent.yml:143` — `subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}`
- `.github/workflows/build-agent.yml:146` — `- name: Sign executables with Azure Trusted Signing`
- `.github/workflows/build-agent.yml:148` — `uses: azure/trusted-signing-action@fc390cf8ed0f14e248a542af1d838388a47c7a7c # v0.5.10`

**FINDING: 🔴 High Risk**

The evidence shows integration with third-party services including Azure Trusted Signing and authentication services (files .github/workflows/build-agent.yml lines 137-162), and references to "medplum-photon-integration" (.github/labeler.yml line 41), but no evidence of Business Associate Agreement requirements being addressed in code or configuration. This creates a risk pattern consistent with non-compliance under HIPAA Privacy Rule 45 CFR §164.502(e) and §164.504(e), which require covered entities to have compliant business associate agreements before allowing third parties to access PHI.

**REMEDIATION DIRECTION**

Implement documentation and configuration controls that demonstrate BAA compliance for all third-party integrations. This should include: (1) adding configuration files or code comments that reference executed BAAs for each third-party service, (2) implementing runtime checks to ensure only BAA-compliant services can access PHI, (3) creating a registry of approved business associates in the codebase, and (4) adding validation logic that prevents data transmission to services without proper BAA status verification. Consider adding environment variables or configuration flags that explicitly track BAA compliance status for each integration.

---

### HIPAA-009: Data Retention and Disposal

**LEGAL QUESTION**

Does the system implement policies and procedures to address the final disposition of electronic Protected Health Information and the hardware or electronic media on which it is stored, as well as removal of PHI before media is available for reuse?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.310(d)(2)(i); 45 CFR §164.310(d)(2)(ii)

**EVIDENCE**

- `.github/auto_assign.yml:9` — `- mattlong`
- `.github/workflows/build.yml:383` — `retention-days: 30`
- `.github/workflows/scorecard.yml:73` — `retention-days: 5`
- `Dockerfile:7` — `# The archive files are decompressed and extracted into the specified destinations.`
- `Dockerfile:9` — `# See: https://docs.docker.com/reference/dockerfile/#adding-local-tar-archives`
- `biome.json:50` — `"noDelete": "warn"`
- `examples/foomedical/src/pages/ScreeningQuestionnairePage.tsx:1298` — `display: 'I could use a little more help',`
- `examples/foomedical/src/pages/ScreeningQuestionnairePage.tsx:2073` — `display: 'Little interest or pleasure in doing things?',`
- `examples/foomedical/src/pages/ScreeningQuestionnairePage.tsx:2093` — `text: 'Little interest or pleasure in doing things?',`
- `examples/foomedical/src/pages/ScreeningQuestionnairePage.tsx:2312` — `display: 'A little bit',`

**FINDING: 🔴 High Risk**

The evidence reveals a risk pattern consistent with non-compliance under HIPAA Security Rule 45 CFR §164.310(d)(2)(i) and (ii). While the repository contains limited retention policies for CI/CD artifacts (30 days in build.yml:383, 5 days in scorecard.yml:73), there are no comprehensive policies or procedures for the final disposition of electronic PHI or secure media disposal/reuse processes. The presence of patient deduplication logic with deletion capabilities (merge-matching-patients.ts:97-99) indicates PHI handling without documented disposal safeguards.

**REMEDIATION DIRECTION**

Implement comprehensive data retention and disposal policies that specifically address PHI lifecycle management. Create documented procedures for secure deletion of PHI from all storage media, including databases, backups, and temporary files. Establish secure media sanitization protocols before hardware reuse or disposal, with verification procedures. Add audit logging for all PHI deletion operations and implement automated retention enforcement mechanisms that comply with required retention periods before secure disposal.

---

### HIPAA-010: Breach Detection and Emergency Access

**LEGAL QUESTION**

Does the system implement procedures for detecting, reporting, and responding to suspected or known security incidents involving electronic Protected Health Information, and does it provide for emergency access to PHI during system disruptions?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.308(a)(6); 45 CFR §164.312(a)(2)(ii)

**EVIDENCE**

- `.github/workflows/build-agent.yml:65` — `restore-keys: |`
- `.github/workflows/build-agent.yml:240` — `restore-keys: |`
- `.github/workflows/build-agent.yml:322` — `restore-keys: |`
- `.github/workflows/build-agent.yml:404` — `restore-keys: |`
- `.github/workflows/build.yml:47` — `restore-keys: |`
- `.github/workflows/build.yml:101` — `restore-keys: |`
- `.github/workflows/build.yml:209` — `restore-keys: |`
- `.github/workflows/build.yml:311` — `restore-keys: |`
- `.github/workflows/build.yml:411` — `restore-keys: |`
- `.github/workflows/chromatic.yml:34` — `restore-keys: |`

**FINDING: 🔴 High Risk**

No evidence was found of security incident detection, reporting, and response procedures for electronic Protected Health Information, which presents a risk pattern consistent with non-compliance under 45 CFR §164.308(a)(6). Additionally, no emergency access procedures for PHI during system disruptions were identified in the codebase, creating a risk pattern consistent with non-compliance under 45 CFR §164.312(a)(2)(ii). The evidence shows only CI/CD workflow configurations and cache restoration keys, which do not address the required security incident management or emergency access controls.

**REMEDIATION DIRECTION**

Implement a comprehensive security incident detection and response system that includes automated monitoring for suspicious activities involving PHI, incident logging mechanisms, notification procedures for security breaches, and documented response workflows. Additionally, establish emergency access procedures that allow authorized personnel to access PHI during system outages or disruptions while maintaining audit trails. This should include backup authentication methods, emergency user provisioning processes, and clear documentation of when and how emergency access can be invoked.

---

## PCI-DSS Findings

### PCIDSS-001: Cardholder Data Storage and Protection

**LEGAL QUESTION**

Does this system store, process, or transmit cardholder data including primary account numbers (PAN), and if so, are adequate protections in place to render stored PAN unreadable, as required under PCI DSS Requirement 3.5?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 3.5 (PAN Storage Protection)

**EVIDENCE**

- `.github/workflows/scorecard.yml:52` — `# repo_token: ${{ secrets.SCORECARD_TOKEN }}`
- `charts/templates/_helpers.tpl:2` — `Expand the name of the chart.`
- `charts/templates/_helpers.tpl:17` — `We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).`
- `examples/foomedical/src/Router.tsx:6` — `import { MembershipAndBilling } from './pages/account/MembershipAndBilling';`
- `examples/foomedical/src/Router.tsx:66` — `<Route path="membership-and-billing" element={<MembershipAndBilling />} />`
- `examples/foomedical/src/components/SideMenu.tsx:29` — `<span>{item.name}</span>`
- `examples/foomedical/src/components/SideMenu.tsx:34` — `<span>{subItem.name}</span>`
- `examples/foomedical/src/img/landingPage/doctor.jpg:1738` — `D6<|AmmY?2~~vGx{׍ 1cA86D6mn7O#/mr\ ,AmF<s pAnDmmowoG[v-Wǖ 1cA`
- `examples/foomedical/src/img/landingPage/laboratory.jpg:1434` — `T}rR˒+uu]3S0,cVVKcyG ][i\1L|{yzcqm1s &$ZEDB;E-YiHkCNJ((^WԿ1LIInD3oLRxlIzHV1OVGdf$)%A[Y1\!uK6?U#OW/x3aQN/]`
- `examples/foomedical/src/img/landingPage/laboratory.jpg:1749` — `K⇍KQE+"ʳZV1!y஌W^=):oY{LyLMlNwK[kmtV/+O7Kښ]dxIp1pDč~]lyHtmvt,gX5/GXY#d5طضϛCy&l Rĸ*G9yQ[ߠOʬ1lcO4`

**FINDING: 🔴 High Risk**

The evidence shows this system handles cardholder data through a "MembershipAndBilling" component (examples/foomedical/src/pages/account/MembershipAndBilling.tsx:34) and related routing functionality, indicating payment processing capabilities. However, no evidence was found of PAN protection controls such as encryption, tokenization, hashing, or other mechanisms required to render stored Primary Account Numbers unreadable. This represents a risk pattern consistent with non-compliance under PCI DSS v4.0 Requirement 3.5.

**REMEDIATION DIRECTION**

The development team must implement adequate PAN protection controls before any cardholder data storage occurs. This requires: (1) implementing strong cryptographic methods to render any stored PAN unreadable (encryption with proper key management, irreversible hashes with strong cryptographic functions, or tokenization), (2) ensuring PAN is never stored in clear text anywhere in the system, (3) documenting the specific protection methods used, and (4) conducting a comprehensive code review to verify no PAN storage exists without proper protection. If PAN storage is not actually required for business operations, consider eliminating storage entirely and using payment processor tokens instead.

---

### PCIDSS-002: Encryption of Card Data in Transit and at Rest

**LEGAL QUESTION**

Is cardholder data encrypted using strong cryptography during transmission over open public networks and when stored at rest, consistent with PCI DSS Requirements 3.5 and 4.2?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirements 3.5 (Encryption at Rest); 4.2 (Encryption in Transit)

**EVIDENCE**

- `.github/CODEOWNERS:2` — `# See: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-reposito`
- `.github/workflows/add-issue-to-project.yml:21` — `project-url: https://github.com/orgs/medplum/projects/1`
- `.github/workflows/add-issue-to-project.yml:25` — `project-url: https://github.com/orgs/medplum/projects/3`
- `.github/workflows/build-agent.yml:50` — `registry-url: 'https://registry.npmjs.org'`
- `.github/workflows/build-agent.yml:52` — `# See: https://github.com/actions/cache/blob/cdf6c1fa76f9f475f3d7449005a359c84ca0f306/examples.md#node---npm`
- `.github/workflows/build-agent.yml:93` — `* Taken from https://github.com/dlemstra/code-sign-action`
- `.github/workflows/build-agent.yml:162` — `endpoint: https://eus.codesigning.azure.net/`
- `.github/workflows/build-agent.yml:231` — `registry-url: 'https://registry.npmjs.org'`
- `.github/workflows/build-agent.yml:313` — `registry-url: 'https://registry.npmjs.org'`
- `.github/workflows/build-agent.yml:395` — `registry-url: 'https://registry.npmjs.org'`

**FINDING: 🔴 High Risk**

Analysis reveals a risk pattern consistent with non-compliance under PCI DSS Requirements 3.5 and 4.2. No evidence of cardholder data encryption at rest or strong cryptography for transmission over public networks was found in the repository. Additionally, multiple anti-patterns were detected including unencrypted HTTP endpoints in production configuration files (docker-compose.full-stack.yml:55-57, 92, 108) and HTTP timestamp services (.github/workflows/build-agent.yml:168, .github/workflows/publish.yml:294).

**REMEDIATION DIRECTION**

Implement strong encryption for cardholder data at rest using AES-256 or equivalent cryptographic standards, and ensure all cardholder data transmission uses TLS 1.2+ with strong cipher suites. Replace all HTTP endpoints with HTTPS equivalents in configuration files, particularly in docker-compose.full-stack.yml for base URLs and health checks. Update timestamp services in GitHub workflows to use HTTPS instead of HTTP. Document encryption key management procedures and ensure proper cryptographic controls are in place throughout the application stack.

---

### PCIDSS-003: Access Control to Cardholder Data

**LEGAL QUESTION**

Does the system restrict access to cardholder data to only those individuals and systems whose job requires such access, implementing role-based access controls consistent with PCI DSS Requirement 7?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 7 (Restrict Access by Business Need to Know)

**EVIDENCE**

- `.github/labeler.yml:24` — `- packages/server/src/fhir/accesspolicy.ts`
- `.github/workflows/add-issue-to-project.yml:11` — `permissions:`
- `.github/workflows/assign-pull-request.yml:7` — `permissions:`
- `.github/workflows/assign-pull-request.yml:14` — `permissions:`
- `.github/workflows/autofix-ci.yml:11` — `permissions:`
- `.github/workflows/autofix-ci.yml:17` — `permissions:`
- `.github/workflows/build-agent.yml:16` — `permissions:`
- `.github/workflows/build-agent.yml:28` — `permissions:`
- `.github/workflows/build-agent.yml:220` — `permissions:`
- `.github/workflows/build-agent.yml:302` — `permissions:`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under PCI DSS v4.0 Requirement 7. While GitHub workflow permissions are configured throughout various workflow files, there is minimal evidence of role-based access controls specifically for cardholder data access. Only one relevant file was identified (packages/server/src/fhir/accesspolicy.ts at line 24), but the actual implementation of role-based restrictions for cardholder data could not be verified from the provided evidence.

**REMEDIATION DIRECTION**

Implement comprehensive role-based access controls that specifically restrict cardholder data access to only authorized personnel based on job function requirements. This should include documented access policies, user role definitions tied to business needs, regular access reviews, and technical controls that enforce these restrictions at the application and data layers. The existing FHIR access policy should be enhanced to include specific cardholder data protection mechanisms, and all access control implementations should be clearly documented and auditable.

---

### PCIDSS-004: Network Segmentation

**LEGAL QUESTION**

Does the system implement network segmentation to isolate the cardholder data environment (CDE) from other network segments, reducing the scope of PCI DSS compliance as described in Requirement 1?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 1 (Network Security Controls)

**EVIDENCE**

- `README.md:115` — `Thanks to [Chromatic](https://www.chromatic.com/) for providing the visual testing platform that helps us review UI chan`
- `charts/templates/backendconfig.yaml:1` — `{{- if and (eq .Values.global.cloudProvider "gcp") (eq .Values.ingress.deploy true) }}`
- `charts/templates/backendconfig.yaml:11` — `name: ingress-security-policy`
- `charts/templates/frontendconfig.yaml:1` — `{{- if and (eq .Values.global.cloudProvider "gcp") (eq .Values.ingress.deploy true) }}`
- `charts/templates/ingress.yaml:1` — `{{- if and (eq .Values.global.cloudProvider "gcp") (eq .Values.ingress.deploy true) }}`
- `charts/templates/ingress.yaml:3` — `kind: Ingress`
- `charts/templates/ingress.yaml:10` — `ingressClassName: "gce"`
- `charts/templates/ingress.yaml:11` — `kubernetes.io/ingress.global-static-ip-name: medplum-external-ip`
- `charts/templates/ingress.yaml:16` — `- host: {{ .Values.ingress.domain }}`
- `charts/templates/ingress.yaml:28` — `{{- if and (eq .Values.global.cloudProvider "azure") (eq .Values.ingress.deploy true) }}`

**FINDING: 🔴 High Risk**

The evidence reveals a risk pattern consistent with non-compliance under PCI DSS v4.0 Requirement 1. While ingress configurations are present in charts/templates/ingress.yaml and related Kubernetes deployment files, there is no evidence of network segmentation controls specifically designed to isolate a cardholder data environment (CDE) from other network segments. The configuration files show standard cloud ingress setups for GCP and Azure but lack the network isolation boundaries required for PCI DSS compliance.

**REMEDIATION DIRECTION**

Implement dedicated network segmentation controls to create a clearly defined CDE boundary. This should include configuring network security groups, VPC isolation, subnet segregation, and firewall rules that restrict traffic flow between the CDE and other network segments. Document the network topology showing segmented zones, implement ingress/egress filtering rules, and ensure that only authorized systems can communicate with the CDE. Consider using Kubernetes network policies, cloud provider security groups, and dedicated VPCs/VNets to achieve proper isolation.

---

### PCIDSS-005: Vulnerability Management

**LEGAL QUESTION**

Does the system demonstrate evidence of vulnerability management practices including regular patching, dependency updates, and vulnerability scanning, consistent with PCI DSS Requirement 6?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 6 (Develop and Maintain Secure Systems)

**EVIDENCE**

- `.github/workflows/build-agent.yml:8` — `workflow_dispatch:`
- `.github/workflows/build-agent.yml:115` — `console.warn('Skipping %s due to error.', signtoolFilename);`
- `.github/workflows/build-deb.yml:11` — `workflow_dispatch:`
- `.github/workflows/build-deb.yml:81` — `--gpg-options="--passphrase-fd 0 --pinentry-mode loopback" \`
- `.github/workflows/build-helm-charts.yml:11` — `workflow_dispatch:`
- `.github/workflows/build.yml:251` — `uses: SonarSource/sonarqube-scan-action@01850e2590cc09ed26831056406ae1525aa41ad5 # master`
- `.github/workflows/build.yml:187` — `--health-cmd "redis-cli ping"`
- `.github/workflows/build.yml:289` — `--health-cmd "redis-cli ping"`
- `.github/workflows/deploy.yml:10` — `workflow_dispatch:`
- `.github/workflows/deploy.yml:70` — `run: ${{ github.event_name == 'workflow_dispatch' && (github.ref == 'refs/heads/main' && './scripts/cicd-deploy.sh --for`

**FINDING: 🔵 Pattern of Concern**

The system shows limited evidence of comprehensive vulnerability management practices required under PCI DSS Requirement 6. While SonarQube scanning is implemented in .github/workflows/build.yml:251 and there's evidence of dependency patching awareness in .github/workflows/prepare-release.yml:33-35 (NPM upgrade for patched version), the evidence lacks systematic vulnerability scanning schedules, automated dependency update processes, or comprehensive patch management workflows across the codebase.

**REMEDIATION DIRECTION**

Implement a comprehensive vulnerability management program by adding automated dependency scanning tools (like Dependabot or Snyk) to GitHub workflows, establish regular vulnerability scanning schedules beyond the current SonarQube integration, create automated patch management workflows for both application dependencies and system components, and document vulnerability remediation timelines and procedures. Consider adding security-focused workflow triggers and dependency update automation to ensure continuous compliance with PCI DSS vulnerability management requirements.

---

### PCIDSS-006: Security Testing Evidence

**LEGAL QUESTION**

Does the system implement security testing controls including code review, static analysis, and penetration testing practices, as required under PCI DSS Requirement 6.3 and 11.4?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirements 6.3 (Security Vulnerabilities); 11.4 (Penetration Testing)

**EVIDENCE**

- `.github/workflows/autofix-ci.yml:28` — `- run: npm run lint:fix`
- `.github/workflows/build.yml:76` — `eslint:`
- `.github/workflows/build.yml:77` — `name: Run eslint`
- `.github/workflows/build.yml:84` — `eslint_errs: ${{ steps.fmt.outputs.eslint_errs }}`
- `.github/workflows/build.yml:106` — `name: Install eslint`
- `.github/workflows/build.yml:121` — `- name: Run eslint`
- `.github/workflows/build.yml:125` — `npm run lint 2> eslint.err > eslint1.err || echo 'failed' > .failed`
- `.github/workflows/build.yml:129` — `echo "eslint_errs<<${delimiter}" >> "${GITHUB_OUTPUT}"`
- `.github/workflows/build.yml:130` — `cat eslint.err >> "${GITHUB_OUTPUT}"`
- `.github/workflows/build.yml:131` — `cat eslint1.err >> "${GITHUB_OUTPUT}"`

**FINDING: 🟠 Medium Risk**

The system implements basic static analysis through ESLint in GitHub workflows (build.yml:76-147 and autofix-ci.yml:28), and shows integration with SonarCloud for code quality analysis per the README badges. However, no evidence was found of penetration testing practices or comprehensive security-focused static analysis tools beyond basic linting. Additionally, multiple security anti-patterns were detected including use of exec() functions and eval() statements across core packages, creating risk patterns consistent with non-compliance under PCI DSS Requirements 6.3 and 11.4.

**REMEDIATION DIRECTION**

Implement comprehensive security testing controls including: (1) Add security-focused static analysis tools like CodeQL, Semgrep, or Snyk to CI/CD pipelines beyond basic ESLint; (2) Establish documented penetration testing procedures and schedule regular assessments; (3) Address security anti-patterns by replacing exec() calls in packages/agent/src/app.ts:67 and packages/cli/src/auth.ts:120 with safer alternatives, and reviewing eval() usage in packages/core/src/fhirlexer/parse.ts; (4) Implement formal code review processes that specifically check for security vulnerabilities before deployment.

---

### PCIDSS-007: Audit Logging of Card Data Access

**LEGAL QUESTION**

Does the system implement audit trail mechanisms that record all individual access to cardholder data, all actions taken by any individual with root or administrative privileges, and all access to audit trails, as required under PCI DSS Requirement 10?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 10 (Log and Monitor All Access)

**EVIDENCE**

- `.vscode/settings.json:24` — `"cSpell.words": ["auditevent", "bullmq", "FHIR", "Fhircast", "Medplum"]`
- `SECURITY.md:7` — `Medplum uses enterprise-grade security and regular audits to ensure you're always protected. We undergo regular penetrat`
- `SECURITY.md:24` — `- Third-Party Audits - Our organization undergoes independent third-party assessments to test our security controls.`
- `charts/templates/backendconfig.yaml:23` — `logging:`
- `examples/medplum-demo-bots/src/resource-usage/resource-usage.ts:70` — `const auditEventCount = counts['AuditEvent'] || 0;`
- `examples/medplum-demo-bots/src/resource-usage/resource-usage.ts:71` — `const totalResourcesMinusAuditEvent = totalResources - auditEventCount;`
- `examples/medplum-demo-bots/src/resource-usage/resource-usage.ts:80` — `['Counted Resources (total excluding AuditEvent)', totalResourcesMinusAuditEvent.toString()],`
- `examples/medplum-demo-bots/src/resource-usage/resource-usage.ts:152` — `'AuditEvent',`
- `examples/medplum-healthie-importer/README.md:147` — `### Error Handling & Logging`
- `examples/medplum-healthie-importer/README.md:149` — `The importer includes comprehensive error handling and logging:`

**FINDING: 🔴 High Risk**

The evidence reveals a risk pattern consistent with non-compliance under PCI DSS v4.0 Requirement 10. While the codebase references AuditEvent resources in examples/medplum-demo-bots/src/resource-usage/resource-usage.ts and general logging configuration in charts/templates/backendconfig.yaml:23, there is no concrete evidence of implemented audit trail mechanisms that specifically record individual access to cardholder data, administrative privilege actions, or audit trail access monitoring as mandated by the standard.

**REMEDIATION DIRECTION**

Implement comprehensive audit logging that captures: (1) all individual access attempts to cardholder data with user identification, timestamps, and data elements accessed; (2) all actions performed by users with root or administrative privileges including login attempts, configuration changes, and system modifications; and (3) all access to audit logs themselves including who viewed, modified, or deleted audit records. Configure automated log generation that cannot be disabled by users, ensure logs are stored securely with integrity protection, and establish real-time monitoring for suspicious access patterns.

---

### PCIDSS-008: Key Management Practices

**LEGAL QUESTION**

Does the system implement cryptographic key management procedures including key generation, distribution, storage, rotation, and destruction, consistent with PCI DSS Requirement 3.6 and 3.7?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirements 3.6 (Key Management Procedures); 3.7 (Key Management Policies)

**EVIDENCE**

- `charts/values.yaml:12` — `# type: "azure:keyVaultURL:secretName"`
- `examples/foomedical/src/img/landingPage/laboratory.jpg:1371` — `~ ]2މ0o^ь$-__&<3D!ǩ9(f6<'MǒϹB\&E\%yVUWdݕnEoeuB>QHqFĦrrrYgE[-XIf[S4-_k揫Q'VSm&	I^N((tV)o-˾Ž.XYeE[-V髄bd`
- `examples/foomedical/src/img/landingPage/laboratory.jpg:1615` — `j¶cMآ!X*%F:RH|#7!ER#	M>0aB%tZ^U{Ҥ1C(BIv+յG|Y~8aoˡg%pVĆɻdeDek,Mr-<U9ߒ2%Lva(]RC+wKC' 8I#'!,WTQg`
- `examples/medplum-demo-bots/src/billing-bots/superbill-pdf.png:624` — `{3,ѣ0jo%jL[#=Ţ'v:Hv64sNK)5aa#'a7ma%M{GOnGKҒY:g37T$*j3A^&	Ql.γU:SU.m@$'2W|5vXiسz'# Z]Th@?}	3m6nFSz`
- `examples/medplum-photon-integration/photon-webhook.png:1561` — `kBD}w|菱敏&#>A㖸)v%vN\sOѭ]E/19~TiتoGkq<Hz_D@D@D@	?OvcdA it*0pԴbtxWwt@(}_ie?|vB(WúB,zAE#KsQ\C!\zme`
- `examples/medplum-photon-integration/photon-webhook.png:430` — `qC%M27']I)O\׎O;ǮsEcIJ:3\_1pNnmzfU+^ϫiV;|VO1'眇1dO^)r9[9̕tv){fzϔoUٷ//º%DEkl~7rOc@f_3+igѬ{z6qnq)Y]`
- `examples/medplum-photon-integration/photon-webhook.png:1466` — `iO w&b_rk(4grR}֔im?x)],a{DB	>Z`e*tv>Sޱ/Į#M!t,o*S3bs[:|fO໎N .ݯ=Gz`6DEKVzV"z\awmr[0\4ޏc"\` ֌%qS`
- `examples/medplum-provider/src/components/ChargeItem/ChargeItemPanel.tsx:77` — `const cptCodeKey = `cpt-${chargeItem.id}-${JSON.stringify(cptCodes?.coding)}`;`
- `examples/medplum-provider/src/components/ChargeItem/ChargeItemPanel.tsx:86` — `key={cptCodeKey}`
- `examples/medplum-smart-on-fhir-demo/src/pages/LaunchPage.tsx:37` — `async function fetchSmartConfiguration(iss: string): Promise<SmartConfiguration> {`

**FINDING: 🔴 High Risk**

Risk pattern consistent with non-compliance under PCI DSS Requirements 3.6 and 3.7. No evidence of formal cryptographic key management procedures for generation, distribution, storage, rotation, or destruction was found in the repository. Multiple anti-patterns were detected including hardcoded API keys and secrets in source code (examples/foomedical/src/config.ts:8, examples/medplum-demo-bots/src/eligibility-check-opkit.ts:24) and private key handling in bot implementations without apparent secure key management controls.

**REMEDIATION DIRECTION**

Implement comprehensive cryptographic key management procedures including automated key generation, secure distribution mechanisms, encrypted storage with proper access controls, scheduled rotation policies, and secure destruction processes. Remove all hardcoded keys and secrets from source code and migrate to a proper secrets management system (the Azure Key Vault reference in charts/values.yaml:12 suggests infrastructure exists but implementation is incomplete). Establish formal key management policies documenting the entire key lifecycle, implement proper key escrow procedures, and ensure all cryptographic operations follow documented procedures with audit trails for key management activities.

---

### PCIDSS-009: Third Party Service Provider Controls

**LEGAL QUESTION**

Does the system manage third-party service providers that have access to cardholder data with appropriate controls, agreements, and monitoring, consistent with PCI DSS Requirement 12.8?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 12.8 (Third-Party Service Provider Management)

**EVIDENCE**

- `.github/labeler.yml:41` — `- examples/medplum-photon-integration/src/**/*`
- `.github/labeler.yml:43` — `integration:`
- `.github/workflows/autofix-ci.yml:21` — `- uses: actions/checkout@8e8c483db84b4bee98b60c0593521ed34d9990e8 # v6.0.1`
- `.github/workflows/build-agent.yml:33` — `- name: Checkout repository`
- `.github/workflows/build-agent.yml:34` — `uses: actions/checkout@8e8c483db84b4bee98b60c0593521ed34d9990e8 # v6.0.1`
- `.github/workflows/build-agent.yml:224` — `- name: Checkout repository`
- `.github/workflows/build-agent.yml:225` — `uses: actions/checkout@8e8c483db84b4bee98b60c0593521ed34d9990e8 # v6.0.1`
- `.github/workflows/build-agent.yml:306` — `- name: Checkout repository`
- `.github/workflows/build-agent.yml:307` — `uses: actions/checkout@8e8c483db84b4bee98b60c0593521ed34d9990e8 # v6.0.1`
- `.github/workflows/build-agent.yml:388` — `- name: Checkout repository`

**FINDING: 🔴 High Risk**

The code repository shows extensive use of third-party services (GitHub Actions, SonarCloud, Coveralls, npm packages) but contains no evidence of third-party service provider management controls, agreements, or monitoring mechanisms as required. While the evidence shows third-party integrations throughout .github/workflows files and external service badges in the README, there are no visible vendor management policies, service provider agreements, or monitoring controls for these third parties that may have access to or process cardholder data. This presents a risk pattern consistent with non-compliance under PCI DSS Requirement 12.8.

**REMEDIATION DIRECTION**

Implement a comprehensive third-party service provider management program that includes: documented agreements with all service providers that handle cardholder data (including cloud services, CI/CD platforms, and monitoring tools), regular security assessments of these providers, contractual requirements for PCI DSS compliance where applicable, and ongoing monitoring of third-party access to cardholder data environments. Create a formal vendor inventory and risk assessment process, and ensure all third-party integrations include appropriate security controls and audit trails.

---

### PCIDSS-010: Incident Response for Card Data Breach

**LEGAL QUESTION**

Does the system implement an incident response plan that addresses suspected or confirmed cardholder data breaches, including detection, containment, and notification procedures, as required under PCI DSS Requirement 12.10?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 12.10 (Incident Response Plan)

**EVIDENCE**

- `LICENSE.txt:158` — `incidental, or consequential damages of any character arising as a`
- `README.md:1` — `# [Medplum](https://www.medplum.com) &middot; [![GitHub license](https://img.shields.io/badge/license-Apache-blue.svg)](`
- `SECURITY.md:14` — `- Continuous Monitoring - Independent third-party penetration, threat, and vulnerability testing.`
- `SECURITY.md:27` — `- Continuous Monitoring - We continuously monitor our security and compliance status to ensure there are no lapses.`
- `charts/values.yaml:55` — `allowPrivilegeEscalation: false`
- `examples/foomedical/README.md:11` — `<img src="https://sonarcloud.io/api/project_badges/measure?project=medplum_foomedical&metric=alert_status&token=3760929a`
- `examples/foomedical/package.json:25` — `"@mantine/notifications": "8.3.18",`
- `examples/foomedical/src/main.tsx:5` — `import { Notifications } from '@mantine/notifications';`
- `examples/foomedical/src/main.tsx:6` — `import '@mantine/notifications/styles.css';`
- `examples/foomedical/src/main.tsx:46` — `<Notifications />`

**FINDING: 🔴 High Risk**

No evidence of a formal incident response plan addressing cardholder data breaches was found in the code repository. While SECURITY.md:14 and SECURITY.md:27 reference continuous monitoring capabilities, there is no documentation of detection, containment, or notification procedures specifically for suspected or confirmed cardholder data breaches. This represents a risk pattern consistent with non-compliance under PCI DSS v4.0 Requirement 12.10.

**REMEDIATION DIRECTION**

The organization must develop and document a comprehensive incident response plan that specifically addresses cardholder data breach scenarios. This plan should include detailed procedures for breach detection (automated monitoring, alerting mechanisms), containment steps (isolation of affected systems, access controls), and notification requirements (timelines for notifying card brands, acquirers, and relevant parties). The plan should be documented in the repository's security documentation and include clear escalation paths, roles and responsibilities, and communication templates for breach scenarios.

---

## SOC2 Findings

### SOC2-001: User Authentication Controls

**LEGAL QUESTION**

Does the system implement logical access security controls over user authentication that are suitably designed and operating effectively to restrict access to authorized users, consistent with the Common Criteria CC6.1 requirement for logical and physical access controls?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC6.1 (Logical and Physical Access Controls)

**EVIDENCE**

- `.github/labeler.yml:22` — `- packages/server/src/oauth/**/*`
- `.github/workflows/add-issue-to-project.yml:22` — `github-token: ${{ secrets.MEDPLUM_BOT_GITHUB_ACCESS_TOKEN }}`
- `.github/workflows/add-issue-to-project.yml:26` — `github-token: ${{ secrets.MEDPLUM_BOT_GITHUB_ACCESS_TOKEN }}`
- `.github/workflows/build-agent.yml:31` — `id-token: write # Required for OIDC authentication with Azure Trusted Signing`
- `.github/workflows/build-agent.yml:137` — `- name: Login to Azure`
- `.github/workflows/build-agent.yml:139` — `uses: azure/login@a457da9ea143d694b1b9c7c869ebb04ebe844ef5 # v2.3.0`
- `.github/workflows/build-agent.yml:31` — `id-token: write # Required for OIDC authentication with Azure Trusted Signing`
- `.github/workflows/build-agent.yml:146` — `- name: Sign executables with Azure Trusted Signing`
- `.github/workflows/build-agent.yml:148` — `uses: azure/trusted-signing-action@fc390cf8ed0f14e248a542af1d838388a47c7a7c # v0.5.10`
- `.github/workflows/build-agent.yml:162` — `endpoint: https://eus.codesigning.azure.net/`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOC 2 CC6.1. While the README indicates the system includes "Medplum Auth" with OAuth, OpenID, and SMART-on-FHIR capabilities, the code repository evidence lacks concrete implementation details of logical access controls for user authentication. The only authentication-related evidence found pertains to GitHub workflow automation tokens and Azure signing processes (.github/workflows/build-agent.yml:22, 31, 139), not user-facing authentication controls required for restricting system access to authorized users.

**REMEDIATION DIRECTION**

The development team needs to provide evidence of implemented user authentication controls including: authentication middleware or handlers, user session management, access control lists or role-based permissions, password policies, multi-factor authentication capabilities, and login/logout functionality. Code files should demonstrate how the system validates user credentials, manages user sessions, and enforces access restrictions. Documentation of the OAuth/OpenID implementation mentioned in the README should be accompanied by actual source code that shows these authentication mechanisms are properly implemented and configured.

---

### SOC2-002: Role-Based Access Control

**LEGAL QUESTION**

Does the system implement role-based or attribute-based access controls that restrict system functions and data access based on authorized user roles, consistent with the principle of least privilege as required under CC6.3?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC6.3 (Role-Based Access and Least Privilege)

**EVIDENCE**

- `.github/labeler.yml:24` — `- packages/server/src/fhir/accesspolicy.ts`
- `.github/workflows/add-issue-to-project.yml:11` — `permissions:`
- `.github/workflows/assign-pull-request.yml:7` — `permissions:`
- `.github/workflows/assign-pull-request.yml:14` — `permissions:`
- `.github/workflows/autofix-ci.yml:11` — `permissions:`
- `.github/workflows/autofix-ci.yml:17` — `permissions:`
- `.github/workflows/build-agent.yml:16` — `permissions:`
- `.github/workflows/build-agent.yml:28` — `permissions:`
- `.github/workflows/build-agent.yml:220` — `permissions:`
- `.github/workflows/build-agent.yml:302` — `permissions:`

**FINDING: 🟠 Medium Risk**

Evidence shows partial implementation of access controls with GitHub workflow permissions configurations across multiple files and reference to an access policy module at packages/server/src/fhir/accesspolicy.ts. However, the evidence lacks sufficient detail to demonstrate comprehensive role-based access controls implementing least privilege principles as required, creating a risk pattern consistent with non-compliance under SOC 2 CC6.3.

**REMEDIATION DIRECTION**

The development team should provide detailed documentation and code review of the FHIR access policy implementation to demonstrate how user roles are defined, how permissions are mapped to specific system functions and data access, and how the principle of least privilege is enforced throughout the application. Additionally, expand access control implementation beyond GitHub workflows to cover all application components, ensuring that each user role has only the minimum permissions necessary to perform their authorized functions.

---

### SOC2-003: Encryption in Transit

**LEGAL QUESTION**

Does the system protect data during transmission over networks using encryption or other equivalent security measures, consistent with the CC6.7 requirement for protection of information during transmission?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC6.7 (Data Transmission Protection)

**EVIDENCE**

- `.github/CODEOWNERS:2` — `# See: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-reposito`
- `.github/workflows/add-issue-to-project.yml:21` — `project-url: https://github.com/orgs/medplum/projects/1`
- `.github/workflows/add-issue-to-project.yml:25` — `project-url: https://github.com/orgs/medplum/projects/3`
- `.github/workflows/build-agent.yml:50` — `registry-url: 'https://registry.npmjs.org'`
- `.github/workflows/build-agent.yml:52` — `# See: https://github.com/actions/cache/blob/cdf6c1fa76f9f475f3d7449005a359c84ca0f306/examples.md#node---npm`
- `.github/workflows/build-agent.yml:93` — `* Taken from https://github.com/dlemstra/code-sign-action`
- `.github/workflows/build-agent.yml:162` — `endpoint: https://eus.codesigning.azure.net/`
- `.github/workflows/build-agent.yml:231` — `registry-url: 'https://registry.npmjs.org'`
- `.github/workflows/build-agent.yml:313` — `registry-url: 'https://registry.npmjs.org'`
- `.github/workflows/build-agent.yml:395` — `registry-url: 'https://registry.npmjs.org'`

**FINDING: 🔵 Pattern of Concern**

Evidence shows mixed implementation of encryption in transit controls, with a risk pattern consistent with non-compliance under SOC 2 CC6.7. While HTTPS URLs are used for external services like GitHub, npm registry, and production endpoints, several anti-patterns were detected including HTTP-only configurations in development environments (docker-compose.full-stack.yml:55-57, 92) and HTTP timestamp services in production workflows (.github/workflows/build-agent.yml:168, .github/workflows/publish.yml:294). The SECURITY.md file references SSL/TLS cipher concerns, indicating awareness of transmission security requirements.

**REMEDIATION DIRECTION**

Replace all HTTP endpoints with HTTPS equivalents, particularly the Microsoft timestamp service URLs in the code signing workflows and the localhost healthcheck endpoints in development configurations. Update docker-compose configurations to use HTTPS for all base URLs, even in development environments, or clearly document that these are development-only configurations that should never be used in production. Consider implementing TLS termination at the container level for consistent encryption across all environments.

---

### SOC2-004: Logging and Monitoring

**LEGAL QUESTION**

Does the system implement logging, monitoring, and alerting mechanisms that detect and record security events, anomalies, and unauthorized activities, as required under CC7.2 for monitoring system components for anomalies?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC7.2 (Monitoring of System Components)

**EVIDENCE**

- `.vscode/settings.json:24` — `"cSpell.words": ["auditevent", "bullmq", "FHIR", "Fhircast", "Medplum"]`
- `README.md:1` — `# [Medplum](https://www.medplum.com) &middot; [![GitHub license](https://img.shields.io/badge/license-Apache-blue.svg)](`
- `README.md:1` — `# [Medplum](https://www.medplum.com) &middot; [![GitHub license](https://img.shields.io/badge/license-Apache-blue.svg)](`
- `SECURITY.md:7` — `Medplum uses enterprise-grade security and regular audits to ensure you're always protected. We undergo regular penetrat`
- `SECURITY.md:24` — `- Third-Party Audits - Our organization undergoes independent third-party assessments to test our security controls.`
- `SECURITY.md:14` — `- Continuous Monitoring - Independent third-party penetration, threat, and vulnerability testing.`
- `SECURITY.md:27` — `- Continuous Monitoring - We continuously monitor our security and compliance status to ensure there are no lapses.`
- `SECURITY.md:14` — `- Continuous Monitoring - Independent third-party penetration, threat, and vulnerability testing.`
- `SECURITY.md:27` — `- Continuous Monitoring - We continuously monitor our security and compliance status to ensure there are no lapses.`
- `charts/templates/backendconfig.yaml:23` — `logging:`

**FINDING: 🔴 High Risk**

The evidence reveals a risk pattern consistent with non-compliance under SOC 2 CC7.2, as no substantive logging, monitoring, or alerting mechanisms for security events are implemented in the codebase. While SECURITY.md mentions "continuous monitoring" at lines 14 and 27, the repository lacks actual implementation of audit event logging, security event detection, or anomaly monitoring capabilities. The only logging-related evidence found is basic application logging configuration in charts/templates/backendconfig.yaml:23 and UI notification components, which do not constitute security monitoring controls.

**REMEDIATION DIRECTION**

Implement comprehensive security event logging throughout the application, including audit trails for authentication, authorization, data access, and system changes. Add monitoring services that can detect anomalous behavior patterns, unauthorized access attempts, and security-relevant system events. Configure alerting mechanisms that notify security personnel of potential incidents in real-time. Ensure all security events are logged with sufficient detail (timestamps, user identification, actions performed, resources accessed) and stored in a centralized, tamper-evident logging system that supports compliance reporting and incident investigation.

---

### SOC2-005: Change Management

**LEGAL QUESTION**

Does the system demonstrate evidence of change management controls including version control, code review processes, and controlled deployment procedures, as required under CC8.1 for managing changes to infrastructure, data, software, and procedures?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC8.1 (Change Management)

**EVIDENCE**

- `.github/labeler.yml:1` — `dependencies:`
- `.github/labeler.yml:23` — `- packages/server/src/scim/**/*`
- `.github/labeler.yml:46` — `- packages/ccda/src/**/*`
- `.github/labeler.yml:58` — `- packages/ccda/src/**/*`
- `.github/labeler.yml:69` — `- packages/cdk/src/**/*`
- `.github/labeler.yml:71` — `- terraform/**/*`
- `.github/workflows/add-issue-to-project.yml:19` — `- uses: actions/add-to-project@31b3f3ccdc584546fc445612dec3f38ff5edb41c # v0.5.0`
- `.github/workflows/add-issue-to-project.yml:23` — `- uses: actions/add-to-project@31b3f3ccdc584546fc445612dec3f38ff5edb41c # v0.5.0`
- `.github/workflows/add-issue-to-project.yml:7` — `pull_request_target:`
- `.github/workflows/assign-pull-request.yml:4` — `pull_request_target:`

**FINDING: 🔵 Pattern of Concern**

Evidence shows partial implementation of change management controls with GitHub Actions workflows present in `.github/workflows/` directory indicating automated CI/CD processes, and labeler configuration in `.github/labeler.yml` suggesting some level of pull request management. However, the evidence lacks clear demonstration of mandatory code review processes, approval gates, or controlled deployment procedures that would satisfy the comprehensive change management requirements under SOC 2 CC8.1.

**REMEDIATION DIRECTION**

Implement and document mandatory code review processes with required approvals before merging changes. Add branch protection rules requiring pull request reviews and status checks. Establish clear deployment approval workflows with evidence of authorized personnel sign-offs for production deployments. Document change management procedures covering infrastructure, data, software, and procedural changes with appropriate approval matrices and audit trails.

---

### SOC2-006: Incident Response

**LEGAL QUESTION**

Does the system implement incident detection, response, and recovery procedures that enable timely identification and remediation of security incidents, consistent with CC7.3 requirements for evaluating security events and CC7.4 for responding to identified incidents?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC7.3 (Security Event Evaluation); CC7.4 (Incident Response)

**EVIDENCE**

- `LICENSE.txt:158` — `incidental, or consequential damages of any character arising as a`
- `README.md:1` — `# [Medplum](https://www.medplum.com) &middot; [![GitHub license](https://img.shields.io/badge/license-Apache-blue.svg)](`
- `SECURITY.md:64` — `However, we believe in recognizing and rewarding valuable security research. For novel, verifiable vulnerabilities with `
- `charts/values.yaml:55` — `allowPrivilegeEscalation: false`
- `examples/foomedical/README.md:11` — `<img src="https://sonarcloud.io/api/project_badges/measure?project=medplum_foomedical&metric=alert_status&token=3760929a`
- `examples/foomedical/src/pages/GetCarePage.tsx:3` — `import { Alert, Loader } from '@mantine/core';`
- `examples/foomedical/src/pages/GetCarePage.tsx:70` — `<Alert variant="outline" color="red" title="Schedule unavailable" icon={<IconInfoCircle />}>`
- `examples/foomedical/src/pages/GetCarePage.tsx:72` — `</Alert>`
- `examples/foomedical/src/pages/GetCarePage.tsx:82` — `<Alert variant="outline" color="red" title="Booking failed" icon={<IconInfoCircle />}>`
- `examples/foomedical/src/pages/GetCarePage.tsx:84` — `</Alert>`

**FINDING: 🔴 High Risk**

The evidence reveals a risk pattern consistent with non-compliance under SOC 2 CC7.3 and CC7.4 requirements. No systematic incident detection, response, or recovery procedures were identified in the codebase. While SECURITY.md:64 references a security research reward program and examples contain basic UI alert components for user notifications, there is no evidence of automated security event monitoring, incident classification procedures, escalation workflows, or formal incident response documentation required for SOC 2 compliance.

**REMEDIATION DIRECTION**

Implement comprehensive incident response capabilities including: automated security event detection and logging systems, formal incident classification and escalation procedures, documented response workflows with defined roles and responsibilities, incident tracking and case management systems, and recovery procedures with defined RTO/RPO objectives. Additionally, establish security event monitoring dashboards, alerting mechanisms for security incidents, and regular testing of incident response procedures to ensure timely identification and remediation of security events.

---

### SOC2-007: Vendor and Dependency Risk

**LEGAL QUESTION**

Does the system assess and manage risks associated with third-party vendors, libraries, and service providers, including dependency vulnerability management, consistent with CC9.2 requirements for risk assessment of third-party service providers?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC9.2 (Third-Party Risk Management)

**EVIDENCE**

- `.gitattributes:23` — `package-lock.json -diff`
- `.gitattributes:24` — `package-lock.json linguist-generated=true`
- `.github/labeler.yml:3` — `- any-glob-to-any-file: 'package-lock.json'`
- `.github/workflows/build-agent.yml:204` — `echo "MEDPLUM_VERSION=$(node -p "require('./package.json').version")" >> $GITHUB_ENV`
- `.github/workflows/build-agent.yml:274` — `echo "MEDPLUM_VERSION=$(node -p "require('./package.json').version")" >> $GITHUB_ENV`
- `.github/workflows/build-agent.yml:356` — `echo "MEDPLUM_VERSION=$(node -p "require('./package.json').version")" >> $GITHUB_ENV`
- `.github/workflows/build-agent.yml:438` — `echo "MEDPLUM_VERSION=$(node -p "require('./package.json').version")" >> $GITHUB_ENV`
- `.github/workflows/build-agent.yml:64` — `key: ${{ runner.os }}-build-agent-${{ env.cache-name }}-${{ hashFiles('**/package-lock.json') }}`
- `.github/workflows/build-agent.yml:239` — `key: ${{ runner.os }}-build-agent-${{ env.cache-name }}-${{ hashFiles('**/package-lock.json') }}`
- `.github/workflows/build-agent.yml:321` — `key: ${{ runner.os }}-build-agent-${{ env.cache-name }}-${{ hashFiles('**/package-lock.json') }}`

**FINDING: 🔴 High Risk**

The evidence reveals no systematic third-party vendor risk assessment or dependency vulnerability management processes, creating a risk pattern consistent with non-compliance under SOC 2 CC9.2. While package management files (package-lock.json) are present in build workflows, there is no evidence of vulnerability scanning, dependency risk assessment procedures, or vendor evaluation frameworks. The OpenSSF Best Practices badge in the README suggests some security awareness, but lacks the structured third-party risk management controls required by the standard.

**REMEDIATION DIRECTION**

Implement a comprehensive third-party risk management program including: automated dependency vulnerability scanning tools integrated into CI/CD pipelines, documented vendor risk assessment procedures for all service providers, regular security assessments of critical dependencies, and establishment of criteria for evaluating and monitoring third-party risks. Add dependency check workflows to GitHub Actions that fail builds on high-severity vulnerabilities, maintain an inventory of all third-party services with associated risk ratings, and create formal vendor management policies that address security requirements and ongoing monitoring obligations.

---

### SOC2-008: Data Backup and Recovery

**LEGAL QUESTION**

Does the system implement data backup, replication, and recovery controls that ensure availability and recoverability of data, consistent with the A1.2 criterion for recovery of infrastructure and data to meet objectives?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria A1.2 (Recovery of Infrastructure and Data)

**EVIDENCE**

- `.github/auto_assign.yml:11` — `- ThatOneBro`
- `.github/labeler.yml:2` — `- changed-files:`
- `.github/labeler.yml:6` — `- changed-files:`
- `.github/labeler.yml:13` — `- changed-files:`
- `.github/labeler.yml:19` — `- changed-files:`
- `.github/labeler.yml:28` — `- changed-files:`
- `.github/labeler.yml:33` — `- changed-files:`
- `.github/labeler.yml:39` — `- changed-files:`
- `.github/labeler.yml:44` — `- changed-files:`
- `.github/labeler.yml:56` — `- changed-files:`

**FINDING: 🔴 High Risk**

No evidence of data backup, replication, or recovery controls was found in the code repository. The evidence consists entirely of GitHub workflow configuration files (.github/workflows/build-agent.yml, .github/workflows/autofix-ci.yml) that show build caching mechanisms and basic CI/CD processes, but contain no backup strategies, disaster recovery procedures, or data replication configurations. This presents a risk pattern consistent with non-compliance under SOC 2 Trust Services Criteria A1.2, which requires recovery controls to ensure availability and recoverability of data.

**REMEDIATION DIRECTION**

Implement comprehensive data backup and recovery controls including: automated backup schedules for all critical data stores, database replication configurations, disaster recovery runbooks, backup verification procedures, and recovery time/point objectives (RTO/RPO) documentation. Add infrastructure-as-code configurations that define backup policies, cross-region replication for critical systems, and automated recovery testing procedures. Document these controls in your repository with clear procedures for data recovery scenarios.

---

### SOC2-009: Multi-Factor Authentication

**LEGAL QUESTION**

Does the system implement or support multi-factor authentication for user access, particularly for privileged accounts and administrative interfaces, consistent with CC6.1 requirements for logical access security?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC6.1 (Logical Access - MFA)

**EVIDENCE**

- `.github/workflows/build-deb.yml:56` — `uses: ruby/setup-ruby@cf7216d52fba1017929b4d7162fabe2b30af5b49 # v1.262.0`
- `charts/templates/deployment.yaml:46` — `imagePullPolicy: IfNotPresent`
- `examples/foomedical/src/img/landingPage/laboratory.jpg:1565` — `P'F	Y<$0㩋,UqK*L"<d㶆/*8Qh4O"So~N=.̌o*E}Iwd$ta̇ CaOO,LXLLilad}VOUHQC0mK.o,W	]ƶxHE#M!2/B=WϮUdԻ[.S=O)sѼ؅³^`
- `examples/medplum-demo-bots/src/billing-bots/superbill-pdf.png:1521` — `''kbp Mc:wD8"#q&e Z9>f>KQT:Ƥq/K5xVC@iMEM8%ōK7ہXdK!DUOx|9/;BnNbg  K6"yܺIie&g4A\0MWߺG +ߌ3_U7b˔8hK70!pau`
- `examples/medplum-demo-bots/src/vital/vital.test.ts:260` — `id: '42fa4b3b-0b3b-4b3b-8b3b-2b3b3b3b3b3b',`
- `examples/medplum-mso-demo/public/how-it-works.png:966` — `uQ~}>cl^K8/_ޯІ%B-~+o'}ҮGX-._EB'8SF`Oٯ*	wjgfVZ5HM<GIx۶m}~ϙ"`1MFaBϹu~̤}̙>IGca,x{QFgut".#X%=+^ds`
- `examples/medplum-mso-demo/public/how-it-works.png:1309` — `Jp]2eF&9Bq6ak= 8\"a#2pN)<?">&c֮] ns1sgwb`{hF$Cb"^@#()\yaf.c-|wĮv|k@98aS?cq`IPPsTd8W[v,9⥋va`
- `examples/medplum-photon-integration/photon-webhook.png:933` — `s(RzRU2F|$R]˧+z,|ɡyT]3??pBrýYC(MMx͚52eJEH_oi_f}Q﹈lT-nZpǱܻPõF@7bU`
- `examples/medplum-provider/src/components/pharmacy/DoseSpotPharmacyDialog.tsx:4` — `import { useDoseSpotPharmacySearch } from '@medplum/dosespot-react';`
- `examples/medplum-provider/src/components/pharmacy/DoseSpotPharmacyDialog.tsx:16` — `export function DoseSpotPharmacyDialog(props: PharmacyDialogBaseProps): JSX.Element {`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOC 2 Trust Services Criteria CC6.1. No multi-factor authentication implementation or configuration was found in the examined code repository files. While the README indicates "Medplum Auth" provides identity solutions using OAuth and OpenID, the specific evidence provided contains only deployment configurations, image files, UI components, and test files with no MFA-related authentication controls, particularly concerning given this is a healthcare platform handling sensitive data.

**REMEDIATION DIRECTION**

Implement multi-factor authentication controls throughout the system, especially for administrative and privileged accounts. This should include configuring MFA in the authentication service, adding MFA enforcement in deployment configurations, implementing MFA requirements in the OAuth/OpenID authentication flows mentioned in the documentation, and ensuring all administrative interfaces require second-factor authentication. Documentation and configuration files should clearly demonstrate MFA implementation and enforcement policies.

---

### SOC2-010: Security Policy Documentation

**LEGAL QUESTION**

Does the system demonstrate evidence of documented security policies, including acceptable use, data classification, and access management policies, as required under CC1.1 for the entity's commitment to integrity and ethical values?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC1.1 (COSO Principle 1 - Integrity and Ethical Values)

**EVIDENCE**

- `README.md:17` — `- [Contributing](#contributing)`
- `README.md:23` — `## Contributing`
- `README.md:28` — `limited scope -- it's our entire product. Our [Contributing documentation](https://medplum.com/docs/contributing) has`
- `README.md:49` — `Did you learn how to do something using Medplum that wasn't obvious on your first try? By contributing your new knowledg`
- `README.md:67` — `**Ready to get started writing code?** Follow the [local setup instructions](https://www.medplum.com/docs/contributing/l`
- `packages/app/README.md:44` — `For more information, refer to the [Developer Instructions](https://www.medplum.com/docs/contributing/run-the-stack).`
- `packages/cdk/README.md:16` — `See [Developer Setup](https://www.medplum.com/docs/contributing) for cloning the repository and installing dependencies.`
- `packages/docs/blog/2025-05-15-so-youre-thinking-about-forking.md:31` — `| **Talent attraction**   | Engineers prefer contributing to widely‑used projects; recruiting for a niche fork is toughe`
- `packages/docs/blog/2025-06-09-security-reports.md:44` — `This email is our day-to-day tactic, but it's based on our official strategy, which is documented for anyone to see in o`
- `packages/docs/docs/api/react/index.mdx:9` — `We're adding new components all the time, and [we welcome PRs!](../contributing)`

**FINDING: 🔴 High Risk**

The evidence reveals a risk pattern consistent with non-compliance under SOC 2 CC1.1. While the repository contains extensive contributing guidelines and developer documentation, there is no evidence of formal security policies including acceptable use policies, data classification policies, or access management policies. The evidence shows only development contribution processes and a brief mention of a responsible disclosure policy in packages/docs/blog/2025-06-09-security-reports.md:44, but no comprehensive security policy framework required for demonstrating organizational commitment to integrity and ethical values.

**REMEDIATION DIRECTION**

The organization needs to create and document formal security policies covering acceptable use of systems and data, data classification standards, and access management procedures. These policies should be stored in accessible locations within the repository (such as a dedicated security or policies directory) and referenced in the main README.md. The policies must go beyond development practices to address organizational security governance, user responsibilities, data handling requirements, and access control principles that demonstrate the entity's commitment to integrity and ethical values as required by the trust services criteria.

---

## SOX Findings

### SOX-001: Financial Data Integrity Controls

**LEGAL QUESTION**

Does the system implement controls to ensure the integrity, accuracy, and completeness of financial data and transactions, consistent with SOX Section 302 requirements for management certification of financial statements?

**REGULATORY STANDARD**

SOX Section 302 (Corporate Responsibility for Financial Reports)

**EVIDENCE**

- `.github/workflows/publish-meta.yml:63` — `# Check if asset already exists in S3 (idempotent check)`
- `docker-compose.full-stack.yml:18` — `- 'default_transaction_isolation=REPEATABLE READ'`
- `examples/foomedical/src/pages/ScreeningQuestionnairePage.tsx:1062` — `code: 'financialStrain',`
- `examples/foomedical/src/pages/ScreeningQuestionnairePage.tsx:1063` — `display: 'Financial Strain',`
- `examples/foomedical/src/pages/ScreeningQuestionnairePage.tsx:1067` — `linkId: '/supplementalQuestions/financialStrain',`
- `examples/foomedical/src/pages/ScreeningQuestionnairePage.tsx:1068` — `text: 'Financial Strain',`
- `examples/foomedical/src/pages/ScreeningQuestionnairePage.tsx:1096` — `linkId: '/supplementalQuestions/financialStrain/11',`
- `examples/medplum-chat-demo/data/example/example-data.json:2602` — `"display": "Anatomic pathologist (occupation)"`
- `examples/medplum-demo-bots/src/billing-bots/superbill-test-data.ts:7` — `type: 'transaction',`
- `examples/medplum-demo-bots/src/billing-bots/superbill.test.ts:81` — `type: 'transaction',`

**FINDING: 🔴 High Risk**

Analysis reveals a risk pattern consistent with non-compliance under SOX Section 302 requirements for financial data integrity controls. While the evidence shows database transaction isolation settings (docker-compose.full-stack.yml:18) and references to financial transaction processing (examples/medplum-demo-bots/src/dft-transfer-listener/dft-transfer-bot.ts:5), there is no evidence of comprehensive financial data validation controls, audit trails, access controls, or automated integrity checks specifically designed for financial reporting accuracy and completeness as required for management certification.

**REMEDIATION DIRECTION**

Implement comprehensive financial data integrity controls including: automated validation rules for financial transactions, audit logging for all financial data modifications, role-based access controls for financial systems, data completeness checks, reconciliation processes, and automated testing of financial calculation accuracy. Additionally, establish documented procedures for financial data governance, implement change management controls for financial reporting systems, and create monitoring dashboards to track data integrity metrics that support SOX 302 management certification requirements.

---

### SOX-002: Access Controls to Financial Systems

**LEGAL QUESTION**

Does the system implement access controls that restrict access to financial systems and data to authorized personnel, with appropriate authentication and authorization mechanisms, as required under SOX Section 404 internal controls?

**REGULATORY STANDARD**

SOX Section 404 (Management Assessment of Internal Controls)

**EVIDENCE**

- `.github/workflows/add-issue-to-project.yml:11` — `permissions:`
- `.github/workflows/assign-pull-request.yml:7` — `permissions:`
- `.github/workflows/assign-pull-request.yml:14` — `permissions:`
- `.github/workflows/autofix-ci.yml:11` — `permissions:`
- `.github/workflows/autofix-ci.yml:17` — `permissions:`
- `.github/workflows/build-agent.yml:16` — `permissions:`
- `.github/workflows/build-agent.yml:28` — `permissions:`
- `.github/workflows/build-agent.yml:220` — `permissions:`
- `.github/workflows/build-agent.yml:302` — `permissions:`
- `.github/workflows/build-agent.yml:384` — `permissions:`

**FINDING: 🔴 High Risk**

The evidence shows only GitHub workflow permission configurations and AWS role assumptions, but no financial system access controls, authentication mechanisms, or authorization frameworks specifically protecting financial data. This creates a risk pattern consistent with non-compliance under SOX Section 404, as the system lacks demonstrable access controls restricting financial systems to authorized personnel only.

**REMEDIATION DIRECTION**

Implement proper financial system access controls including: role-based access control (RBAC) configurations that specifically restrict financial data access, multi-factor authentication requirements for financial system users, documented authorization matrices showing who can access what financial data, audit logging of all financial system access attempts, and segregation of duties controls that prevent unauthorized financial data manipulation. These controls should be coded into the application layer, not just the CI/CD pipeline level.

---

### SOX-003: Audit Trail for Financial Transactions

**LEGAL QUESTION**

Does the system maintain a complete and tamper-evident audit trail of all financial transactions, modifications, and access events, sufficient to support the audit requirements under SOX Section 802?

**REGULATORY STANDARD**

SOX Section 802 (Criminal Penalties for Altering Documents)

**EVIDENCE**

- `.github/workflows/build-agent.yml:168` — `timestamp-rfc3161: http://timestamp.acs.microsoft.com`
- `.github/workflows/build-agent.yml:169` — `timestamp-digest: SHA256`
- `.github/workflows/publish-meta.yml:72` — `--cache-control "public, max-age=31536000, immutable"`
- `.github/workflows/publish.yml:294` — `timestamp-rfc3161: http://timestamp.acs.microsoft.com`
- `.github/workflows/publish.yml:295` — `timestamp-digest: SHA256`
- `.vscode/settings.json:24` — `"cSpell.words": ["auditevent", "bullmq", "FHIR", "Fhircast", "Medplum"]`
- `SECURITY.md:7` — `Medplum uses enterprise-grade security and regular audits to ensure you're always protected. We undergo regular penetrat`
- `SECURITY.md:24` — `- Third-Party Audits - Our organization undergoes independent third-party assessments to test our security controls.`
- `examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx:190` — `linkId: 'medical-history',`
- `examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx:191` — `text: 'Medical History',`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOX Section 802. While the repository contains RFC3161 timestamping configurations in GitHub workflows (.github/workflows/build-agent.yml:168-169 and .github/workflows/publish.yml:294-295) and references to audit events in code (auditevent in .vscode/settings.json:24), there is no evidence of a comprehensive audit trail system for financial transactions, modifications, or access events. The medical history and patient intake examples found are healthcare-related data points, not financial transaction audit controls required by SOX.

**REMEDIATION DIRECTION**

Implement a complete audit logging system that captures all financial transactions, data modifications, and user access events with tamper-evident controls. This should include cryptographic integrity protection, immutable log storage, detailed transaction metadata (user, timestamp, before/after values), and retention policies that meet SOX requirements. Ensure the audit system covers all financial data flows, not just the code deployment timestamping that currently exists.

---

### SOX-004: Change Management for Financial Software

**LEGAL QUESTION**

Does the system implement change management controls for software that processes financial data, including version control, code review, testing, and controlled deployment, consistent with SOX IT general controls?

**REGULATORY STANDARD**

SOX Section 404 (ITGC - Change Management Controls)

**EVIDENCE**

- `.github/labeler.yml:1` — `dependencies:`
- `.github/labeler.yml:23` — `- packages/server/src/scim/**/*`
- `.github/labeler.yml:46` — `- packages/ccda/src/**/*`
- `.github/labeler.yml:58` — `- packages/ccda/src/**/*`
- `.github/labeler.yml:69` — `- packages/cdk/src/**/*`
- `.github/workflows/add-issue-to-project.yml:19` — `- uses: actions/add-to-project@31b3f3ccdc584546fc445612dec3f38ff5edb41c # v0.5.0`
- `.github/workflows/add-issue-to-project.yml:23` — `- uses: actions/add-to-project@31b3f3ccdc584546fc445612dec3f38ff5edb41c # v0.5.0`
- `.github/workflows/add-issue-to-project.yml:7` — `pull_request_target:`
- `.github/workflows/assign-pull-request.yml:4` — `pull_request_target:`
- `.github/workflows/autofix-ci.yml:24` — `node-version: '24'`

**FINDING: 🟠 Medium Risk**

Evidence shows GitHub Actions workflows for automated processes (autofix-ci.yml, build-agent.yml) and pull request handling, but lacks clear documentation of comprehensive change management controls required for financial data processing software. While version control infrastructure exists through GitHub, the repository does not demonstrate formal code review requirements, testing procedures, or controlled deployment processes that would satisfy SOX IT general control requirements for change management.

**REMEDIATION DIRECTION**

Implement and document formal change management procedures including: mandatory code review requirements through GitHub branch protection rules, automated testing workflows that must pass before deployment, formal approval processes for production deployments, and clear separation of duties between development and production environments. Add documentation describing the complete software development lifecycle process, testing requirements, and deployment controls to demonstrate compliance with SOX Section 404 IT general controls for change management.

---

### SOX-005: Segregation of Duties Evidence

**LEGAL QUESTION**

Does the system implement segregation of duties controls that prevent any single individual from having the ability to both authorize and execute financial transactions, or to both develop and deploy changes to financial systems?

**REGULATORY STANDARD**

SOX Section 404 (Internal Controls - Segregation of Duties)

**EVIDENCE**

- `.github/workflows/build-agent.yml:8` — `workflow_dispatch:`
- `.github/workflows/build-deb.yml:11` — `workflow_dispatch:`
- `.github/workflows/build-helm-charts.yml:11` — `workflow_dispatch:`
- `.github/workflows/build.yml:3` — `# see https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#concurrency`
- `.github/workflows/build.yml:2` — `# Limit a single job to run at a time for a given branch/PR to save resources and speed up CI`
- `.github/workflows/build.yml:128` — `delimiter="$(openssl rand -hex 8)"`
- `.github/workflows/build.yml:129` — `echo "eslint_errs<<${delimiter}" >> "${GITHUB_OUTPUT}"`
- `.github/workflows/build.yml:132` — `echo "${delimiter}" >> "${GITHUB_OUTPUT}"`
- `.github/workflows/codeql-analysis.yml:1` — `# For most projects, this workflow file will not need changing; you simply need`
- `.github/workflows/codeql-analysis.yml:14` — `# see https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#concurrency`

**FINDING: 🔴 High Risk**

Risk pattern consistent with non-compliance under SOX Section 404 segregation of duties requirements. The evidence shows multiple GitHub workflows with `workflow_dispatch` triggers (build-agent.yml:8, build-deb.yml:11, build-helm-charts.yml:11, deploy.yml:10, prepare-release.yml:4) allowing manual execution, and a deployment workflow (deploy.yml:70) that can force deployments to production when triggered manually from the main branch. No evidence was found of approval mechanisms, role-based restrictions, or segregation controls that would prevent a single developer from both developing code changes and deploying them to production systems.

**REMEDIATION DIRECTION**

Implement branch protection rules requiring pull request approvals from different individuals than the code author. Add required reviewers for deployment workflows, particularly for the deploy.yml workflow. Remove or restrict workflow_dispatch triggers for production deployments, replacing them with approval-gated processes. Implement role-based access controls in GitHub that separate development permissions from deployment permissions, ensuring no single user can both commit code and execute production deployments.

---

### SOX-006: Data Retention for Financial Records

**LEGAL QUESTION**

Does the system implement data retention policies that preserve financial records, audit work papers, and supporting documentation for the minimum retention period required under SOX Section 802 (not less than 7 years)?

**REGULATORY STANDARD**

SOX Section 802 (Document Retention - 7 Year Minimum)

**EVIDENCE**

- `.github/workflows/build-deb.yml:79` — `--preserve-versions \`
- `.github/workflows/build.yml:383` — `retention-days: 30`
- `.github/workflows/publish-meta.yml:72` — `--cache-control "public, max-age=31536000, immutable"`
- `.github/workflows/scorecard.yml:73` — `retention-days: 5`
- `Dockerfile:7` — `# The archive files are decompressed and extracted into the specified destinations.`
- `Dockerfile:9` — `# See: https://docs.docker.com/reference/dockerfile/#adding-local-tar-archives`
- `Dockerfile:8` — `# We do this to preserve the folder structure in a single layer.`
- `charts/.helmignore:13` — `# Common backup files`
- `examples/foomedical/src/img/homePage/better-sleep.svg:4` — `viewBox="0 0 511.998 511.998" style="enable-background:new 0 0 511.998 511.998;" xml:space="preserve">`
- `examples/foomedical/src/img/homePage/doctor.svg:4` — `viewBox="0 0 512 512" style="enable-background:new 0 0 512 512;" xml:space="preserve">`

**FINDING: 🔴 High Risk**

Risk pattern consistent with non-compliance under SOX Section 802 detected. The codebase lacks any implementation of data retention policies for financial records, audit work papers, or supporting documentation meeting the 7-year minimum requirement. While GitHub workflow files show artifact retention periods of only 30 days (.github/workflows/build.yml:383) and 5 days (.github/workflows/scorecard.yml:73), no evidence exists of systems or policies preserving financial data for the required 7-year period.

**REMEDIATION DIRECTION**

Implement comprehensive data retention policies and technical controls specifically for financial records and audit documentation. This should include database-level retention settings, automated archival processes, and policy documentation that explicitly addresses SOX Section 802 requirements. Configure retention periods of at least 7 years for all financial data, audit logs, and supporting documentation. Consider implementing immutable storage solutions and automated compliance monitoring to ensure ongoing adherence to retention requirements.

---

### SOX-007: Internal Control Documentation

**LEGAL QUESTION**

Does the system provide evidence of documented internal controls over financial reporting, including control objectives, control activities, and monitoring procedures, as required under SOX Section 404(a)?

**REGULATORY STANDARD**

SOX Section 404(a) (Management Assessment of Internal Controls)

**EVIDENCE**

- `.github/labeler.yml:24` — `- packages/server/src/fhir/accesspolicy.ts`
- `.github/labeler.yml:55` — `compliance:`
- `.github/labeler.yml:5` — `documentation:`
- `.github/workflows/build-deb.yml:82` — `--cache-control="max-age=300" \`
- `.github/workflows/publish-meta.yml:72` — `--cache-control "public, max-age=31536000, immutable"`
- `.github/workflows/publish-meta.yml:129` — `--cache-control "no-cache"`
- `.github/workflows/publish-meta.yml:134` — `--cache-control "no-cache"`
- `.github/workflows/publish-meta.yml:139` — `--cache-control "no-cache"`
- `.github/workflows/scorecard.yml:3` — `# policy, and support documentation.`
- `.github/workflows/scorecard.yml:3` — `# policy, and support documentation.`

**FINDING: 🔴 High Risk**

The code repository shows a risk pattern consistent with non-compliance under SOX Section 404(a). While basic compliance infrastructure exists (evidenced by .github/labeler.yml:55 referencing "compliance" and access policy files like packages/server/src/fhir/accesspolicy.ts), no documented internal controls over financial reporting were found. The repository lacks evidence of formal control objectives, control activities, or monitoring procedures specifically designed for financial reporting processes as mandated by SOX 404(a).

**REMEDIATION DIRECTION**

Implement and document a comprehensive internal controls framework for financial reporting. Create formal documentation that includes: (1) clearly defined control objectives for financial data accuracy and completeness, (2) specific control activities such as segregation of duties, authorization procedures, and data validation controls, and (3) monitoring procedures including regular testing and evaluation of control effectiveness. Establish a dedicated controls documentation directory with version control, and ensure all financial reporting processes have corresponding control documentation that can be audited and verified.

---

### SOX-008: Anti-Tampering Controls

**LEGAL QUESTION**

Does the system implement controls to prevent unauthorized alteration or destruction of financial records, including integrity verification, immutable storage, and tamper detection mechanisms, consistent with SOX Section 802 anti-destruction requirements?

**REGULATORY STANDARD**

SOX Section 802 (Criminal Penalties for Document Destruction/Alteration)

**EVIDENCE**

- `.github/workflows/build-agent.yml:64` — `key: ${{ runner.os }}-build-agent-${{ env.cache-name }}-${{ hashFiles('**/package-lock.json') }}`
- `.github/workflows/build-agent.yml:73` — `- name: Set repo hash`
- `.github/workflows/build-agent.yml:75` — `# This forces git shorthash to match between @medplum/agent and @medplum/core`
- `.github/workflows/build-agent.yml:78` — `echo "MEDPLUM_GIT_SHORTHASH=$(git rev-parse --short=7 HEAD)" >> $GITHUB_ENV`
- `.github/workflows/build-agent.yml:239` — `key: ${{ runner.os }}-build-agent-${{ env.cache-name }}-${{ hashFiles('**/package-lock.json') }}`
- `.github/workflows/build-agent.yml:248` — `- name: Set repo hash`
- `.github/workflows/build-agent.yml:250` — `# This forces git shorthash to match between @medplum/agent and @medplum/core`
- `.github/workflows/build-agent.yml:253` — `echo "MEDPLUM_GIT_SHORTHASH=$(git rev-parse --short=7 HEAD)" >> $GITHUB_ENV`
- `.github/workflows/build-agent.yml:321` — `key: ${{ runner.os }}-build-agent-${{ env.cache-name }}-${{ hashFiles('**/package-lock.json') }}`
- `.github/workflows/build-agent.yml:330` — `- name: Set repo hash`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOX Section 802 anti-destruction requirements. While the code repository demonstrates basic integrity controls through Git hash tracking in build workflows (.github/workflows/build-agent.yml lines 78, 253, 335, 417), no evidence was found of comprehensive anti-tampering controls for financial records, including immutable storage mechanisms, tamper detection systems, or integrity verification specifically for financial data. The presence of data truncation operations in multiple files (packages/core/src/fhirmapper/transform.test.ts:65, packages/app/src/admin/db/ColumnStatistics.test.tsx:768) raises additional concerns about potential unauthorized alteration of records.

**REMEDIATION DIRECTION**

Implement comprehensive financial record protection controls including: (1) immutable audit logging with cryptographic integrity verification for all financial data operations, (2) tamper detection mechanisms that monitor and alert on unauthorized access attempts to financial records, (3) role-based access controls specifically governing financial record modifications, and (4) backup and retention policies that prevent unauthorized destruction of financial documents. Replace any data truncation operations affecting financial records with secure archival processes that maintain complete audit trails while meeting regulatory retention requirements.

---

## TCPA Findings

### TCPA-001: Prior Express Written Consent for SMS

**LEGAL QUESTION**

Does the system obtain prior express written consent before sending marketing or promotional text messages, including a clear and conspicuous disclosure that consent is being sought, as required under 47 U.S.C. §227(b)(1) and 47 CFR §64.1200(a)(2)?

**REGULATORY STANDARD**

TCPA 47 U.S.C. §227(b)(1); 47 CFR §64.1200(a)(2)

**EVIDENCE**

- `LICENSE.txt:135` — `the terms of any separate license agreement you may have executed`
- `LICENSE.txt:144` — `agreed to in writing, Licensor provides the Work (and each`
- `LICENSE.txt:156` — `negligent acts) or agreed to in writing, shall any Contributor be`
- `LICENSE.txt:171` — `of any other Contributor, and only if You agree to indemnify,`
- `NOTICE:15` — `Unless required by applicable law or agreed to in writing, software`
- `examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx:470` — `linkId: 'consent-for-treatment',`
- `examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx:471` — `text: 'Consent for Treatment',`
- `examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx:475` — `linkId: 'consent-for-treatment-signature',`
- `examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx:476` — `text: 'I the undersigned patient (or authorized representative, or parent/guardian), consent to and authorize the perfor`
- `examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx:480` — `linkId: 'consent-for-treatment-date',`

**FINDING: 🔴 High Risk**

No evidence found of prior express written consent mechanisms for SMS marketing or promotional messages as required under TCPA regulations. The codebase contains medical treatment consent forms in examples/foomedical/src/pages/PatientIntakeQuestionnairePage.tsx and general consent references in JSON data, but lacks any SMS-specific consent collection, disclosure language, or opt-in mechanisms that would satisfy 47 U.S.C. §227(b)(1) and 47 CFR §64.1200(a)(2) requirements. This presents a risk pattern consistent with non-compliance under TCPA regulations for any SMS marketing functionality.

**REMEDIATION DIRECTION**

Implement a comprehensive SMS consent collection system that includes: (1) clear and conspicuous disclosure language explaining that consent is being sought for marketing text messages, (2) opt-in mechanisms that capture express written consent before sending any promotional SMS, (3) database fields to store and track consent status per user, and (4) validation logic to prevent SMS marketing to users without proper consent. The consent flow should be separate from medical treatment consent and specifically address SMS marketing communications with appropriate legal disclaimers about message frequency and data rates.

---

### TCPA-002: Opt-Out Mechanism Implementation

**LEGAL QUESTION**

Does the system provide a clear and easy mechanism for recipients to opt out of receiving further messages, and does it honor opt-out requests promptly, as required under TCPA and CTIA guidelines?

**REGULATORY STANDARD**

TCPA 47 U.S.C. §227(b)(2)(E); CTIA Messaging Principles

**EVIDENCE**

- `.github/workflows/autofix-ci.yml:5` — `cancel-in-progress: true`
- `.github/workflows/build-agent.yml:5` — `cancel-in-progress: true`
- `.github/workflows/build-deb.yml:5` — `cancel-in-progress: true`
- `.github/workflows/build-helm-charts.yml:5` — `cancel-in-progress: true`
- `.github/workflows/build.yml:6` — `cancel-in-progress: true`
- `.github/workflows/codeql-analysis.yml:17` — `cancel-in-progress: true`
- `.github/workflows/deploy.yml:5` — `cancel-in-progress: false`
- `.github/workflows/madge.yml:5` — `cancel-in-progress: true`
- `.github/workflows/staging.yml:5` — `cancel-in-progress: false`
- `LICENSE.txt:161` — `work stoppage, computer failure or malfunction, or any and all`

**FINDING: 🔴 High Risk**

No evidence was found in the codebase of opt-out mechanisms for message recipients, creating a risk pattern consistent with non-compliance under TCPA 47 U.S.C. §227(b)(2)(E) and CTIA Messaging Principles. The evidence shows only system-level cancellation controls (GitHub workflow cancellations, Docker restart policies) and application UI cancel buttons, but no messaging opt-out functionality for end users. This healthcare platform appears to lack the required clear and easy mechanism for recipients to stop receiving messages.

**REMEDIATION DIRECTION**

Implement a comprehensive opt-out system that includes: (1) clear opt-out instructions in all outbound messages (e.g., "Reply STOP to opt out"), (2) database tables to track recipient opt-out preferences, (3) API endpoints to process and honor opt-out requests, (4) automated message filtering to prevent sending to opted-out recipients, and (5) confirmation messages when opt-out requests are processed. Ensure opt-out requests are honored immediately and that the mechanism is prominently displayed in all messaging interfaces.

---

### TCPA-003: Do Not Call List Checking

**LEGAL QUESTION**

Does the system check phone numbers against the National Do Not Call Registry and maintain an internal do-not-call list before initiating outbound calls or messages, as required under 47 CFR §64.1200(c)?

**REGULATORY STANDARD**

TCPA 47 CFR §64.1200(c) (Do Not Call Requirements)

**EVIDENCE**

- `.github/workflows/build-agent.yml:50` — `registry-url: 'https://registry.npmjs.org'`
- `.github/workflows/build-agent.yml:231` — `registry-url: 'https://registry.npmjs.org'`
- `.github/workflows/build-agent.yml:313` — `registry-url: 'https://registry.npmjs.org'`
- `.github/workflows/build-agent.yml:395` — `registry-url: 'https://registry.npmjs.org'`
- `.github/workflows/build-deb.yml:37` — `registry-url: 'https://registry.npmjs.org'`
- `.github/workflows/build-helm-charts.yml:30` — `registry-url: 'https://registry.npmjs.org'`
- `.github/workflows/build.yml:39` — `registry-url: 'https://registry.npmjs.org'`
- `.github/workflows/build.yml:93` — `registry-url: 'https://registry.npmjs.org'`
- `.github/workflows/build.yml:201` — `registry-url: 'https://registry.npmjs.org'`
- `.github/workflows/build.yml:303` — `registry-url: 'https://registry.npmjs.org'`

**FINDING: 🔴 High Risk**

No evidence found of National Do Not Call Registry checking or internal do-not-call list functionality in the codebase, creating a risk pattern consistent with non-compliance under 47 CFR §64.1200(c). The evidence only shows NPM package registry references in CI/CD workflows, which are unrelated to telecommunications compliance requirements. Given that Medplum is a healthcare platform that may send patient communications or notifications via phone, the absence of TCPA-required do-not-call checking mechanisms presents significant regulatory risk.

**REMEDIATION DIRECTION**

Implement National Do Not Call Registry checking functionality by integrating with the FTC's Do Not Call Registry API or a third-party compliance service before initiating any outbound calls or SMS messages. Create and maintain an internal suppression list database table to track opt-out requests from users. Add validation logic in the communication workflow code to check both the national registry and internal suppression list before placing calls or sending messages. Ensure all outbound communication modules include these compliance checks as mandatory steps that cannot be bypassed.

---

### TCPA-004: Message Frequency Disclosure

**LEGAL QUESTION**

Does the system disclose to consumers the expected frequency of messages before obtaining consent, and does it enforce frequency limits consistent with the disclosed rate, as recommended by CTIA guidelines?

**REGULATORY STANDARD**

CTIA Messaging Principles and Best Practices; TCPA Consent Requirements

**EVIDENCE**

- `.github/workflows/build-deb.yml:49` — `RECAPTCHA_SITE_KEY: '__RECAPTCHA_SITE_KEY__'`
- `.github/workflows/build.yml:74` — `RECAPTCHA_SITE_KEY: '__RECAPTCHA_SITE_KEY__'`
- `.github/workflows/build.yml:432` — `RECAPTCHA_SITE_KEY: '__RECAPTCHA_SITE_KEY__'`
- `.github/workflows/deploy.yml:85` — `RECAPTCHA_SITE_KEY: ${{ secrets.RECAPTCHA_SITE_KEY }}`
- `.github/workflows/publish.yml:90` — `RECAPTCHA_SITE_KEY: '__RECAPTCHA_SITE_KEY__'`
- `.github/workflows/staging.yml:53` — `RECAPTCHA_SITE_KEY: '__RECAPTCHA_SITE_KEY__'`
- `.github/workflows/staging.yml:85` — `RECAPTCHA_SITE_KEY: ${{ secrets.STAGING_RECAPTCHA_SITE_KEY }}`
- `biome.json:63` — `"useMediaCaption": "warn",`
- `charts/values.yaml:60` — `capabilities:`
- `docker-compose.full-stack.yml:73` — `MEDPLUM_RECAPTCHA_SITE_KEY: '6LfHdsYdAAAAAC0uLnnRrDrhcXnziiUwKd8VtLNq'`

**FINDING: 🔴 High Risk**

No evidence found of message frequency disclosure or enforcement mechanisms in the code repository. The evidence consists entirely of RECAPTCHA configuration keys and unrelated system files, with no implementation of TCPA-compliant messaging controls, frequency limits, or consumer disclosure mechanisms. This represents a risk pattern consistent with non-compliance under CTIA Messaging Principles and TCPA consent requirements.

**REMEDIATION DIRECTION**

Implement a comprehensive messaging compliance system that includes: (1) user-facing disclosure forms showing expected message frequency before consent collection, (2) database schema to store user consent with disclosed frequency rates, (3) rate limiting mechanisms that enforce the disclosed frequency limits, and (4) logging systems to track message sending patterns for compliance auditing. The system should present clear frequency expectations (e.g., "up to 5 messages per week") during signup and technically enforce these limits in the messaging infrastructure.

---

### TCPA-005: Sender Identification in Messages

**LEGAL QUESTION**

Does the system include proper sender identification in all outbound messages, including the identity of the entity sending the message and how to contact them, consistent with TCPA and CTIA requirements?

**REGULATORY STANDARD**

TCPA 47 U.S.C. §227(d); CTIA Messaging Principles

**EVIDENCE**

- `examples/medplum-eligibility-demo/data/core/core-data.json:329` — `"display": "Brand Name Prescription Drug"`
- `examples/medplum-eligibility-demo/data/core/core-data.json:449` — `"display": "Brand Name Prescription Drug - Formulary"`
- `examples/medplum-eligibility-demo/data/core/core-data.json:453` — `"display": "Brand Name Prescription Drug - Non-Formulary"`
- `examples/medplum-photon-integration/src/photon-types.d.ts:159` — `brandName?: string;`
- `examples/medplum-provider/src/pages/getstarted/GetStartedPage.tsx:25` — `IconBrandDiscord,`
- `examples/medplum-provider/src/pages/getstarted/GetStartedPage.tsx:570` — `<IconBrandDiscord size={24} color="var(--icon-secondary)" />`
- `examples/medplum-valueset-selector/src/pages/HomePage.tsx:15` — `"id": "rxnorm-branded-drugs",`
- `examples/medplum-valueset-selector/src/pages/HomePage.tsx:16` — `"url": "http://example.org/fhir/ValueSet/rxnorm-branded-drugs",`
- `examples/medplum-valueset-selector/src/pages/HomePage.tsx:18` — `"name": "RxNormBrandedDrugs",`
- `examples/medplum-valueset-selector/src/pages/HomePage.tsx:19` — `"title": "RxNorm Branded Drug Components",`

**FINDING: 🔴 High Risk**

No evidence found of sender identification mechanisms in outbound messages within the analyzed code repository. The evidence shows only branding-related references for UI components, drug classifications, and platform identity rather than message sender identification functionality. This represents a risk pattern consistent with non-compliance under TCPA 47 U.S.C. §227(d) and CTIA Messaging Principles, which require proper sender identification and contact information in all outbound communications.

**REMEDIATION DIRECTION**

Implement sender identification functionality for all outbound messages by adding required fields such as sender name, organization identity, and contact information (phone number, email, or physical address). Create message templates or wrapper functions that automatically include this identification data before sending any communications. Establish configuration settings to manage sender contact details and ensure they are consistently applied across all messaging channels. Add validation to prevent messages from being sent without proper sender identification.

---

### TCPA-006: Record Keeping of Consent

**LEGAL QUESTION**

Does the system maintain records of consent that would be sufficient to demonstrate compliance in the event of a dispute, including the date, time, method of consent, and the specific consent language presented to the consumer?

**REGULATORY STANDARD**

TCPA 47 CFR §64.1200; FCC Declaratory Rulings on Consent Records

**EVIDENCE**

- `packages/server/src/migrations/schema/v1.ts:773` — `await client.query(`CREATE TABLE IF NOT EXISTS "Consent_History" (`
- `packages/server/src/migrations/schema/v14.ts:154` — `await client.query('CREATE INDEX ON "Consent_History" ("id")');`
- `packages/server/src/migrations/schema/v14.ts:155` — `await client.query('CREATE INDEX ON "Consent_History" ("lastUpdated")');`
- `packages/server/src/migrations/schema/v42.ts:707` — `'CREATE INDEX CONCURRENTLY IF NOT EXISTS "Consent_sourceReference_idx" ON "Consent" ("sourceReference")'`

**FINDING: 🔴 High Risk**

The system shows database schema evidence of consent tracking tables ("Consent_History" at packages/server/src/migrations/schema/v1.ts:773 and "Consent" table with sourceReference indexing at v42.ts:707), but lacks visible implementation of the specific data fields required by TCPA compliance. No evidence was found of systematic capture of date/time stamps, consent method documentation, or preservation of the exact consent language presented to consumers, creating a risk pattern consistent with non-compliance under TCPA 47 CFR §64.1200 and FCC Declaratory Rulings on Consent Records.

**REMEDIATION DIRECTION**

The development team needs to implement comprehensive consent record fields within the existing Consent and Consent_History tables to capture: (1) precise timestamp of consent collection, (2) method of consent (web form, SMS, voice, etc.), (3) the exact consent language/script shown to the consumer, (4) consumer contact information, and (5) any consent withdrawal records. Additionally, implement data retention policies ensuring these records are preserved and easily retrievable for regulatory inquiries or disputes, with proper indexing for efficient lookup by consumer identifier and date ranges.

---

### TCPA-007: Revocation of Consent Handling

**LEGAL QUESTION**

Does the system honor revocation of consent through any reasonable means indicated by the consumer, not limited to specific keywords, and process revocation within a reasonable timeframe, consistent with FCC guidance?

**REGULATORY STANDARD**

TCPA 47 U.S.C. §227(b)(1)(A); FCC 2015 TCPA Omnibus Declaratory Ruling

**EVIDENCE**

- `.github/workflows/codeql-analysis.yml:63` — `# If this step fails, then you should remove it and run the build manually (see below)`
- `.github/workflows/codeql-analysis.yml:70` — `# ✏️ If the Autobuild fails above, remove it and uncomment the following three lines`
- `.github/workflows/prepare-release.yml:33` — `# Upgrade to a patched version; this should be removed after Node has a tagged`
- `.github/workflows/scorecard.yml:26` — `# `publish_results: true` only works when run from the default branch. conditional can be removed if disabled.`
- `.github/workflows/upgrade-dependencies.yml:37` — `# Upgrade to a patched version; this should be removed after Node has a tagged`
- `LICENSE.txt:161` — `work stoppage, computer failure or malfunction, or any and all`
- `docker-compose.full-stack.yml:4` — `restart: unless-stopped # for production usage, consider using 'always'`
- `docker-compose.full-stack.yml:31` — `restart: unless-stopped # for production usage, consider 'always'`
- `docker-compose.full-stack.yml:44` — `restart: unless-stopped`
- `docker-compose.full-stack.yml:101` — `restart: unless-stopped`

**FINDING: 🔴 High Risk**

No evidence found of any consent revocation handling mechanisms in the analyzed code repository. The search results contain only generic code comments about removing technical elements (build steps, Docker containers, data properties) and unrelated medical occupation displays, but reveal no implementation of TCPA-compliant consent revocation processing, keyword detection systems, or automated revocation workflows. This absence of required controls represents a risk pattern consistent with non-compliance under TCPA 47 U.S.C. §227(b)(1)(A) and FCC 2015 TCPA Omnibus Declaratory Ruling.

**REMEDIATION DIRECTION**

Implement a comprehensive consent revocation system that monitors for revocation requests through multiple channels (SMS replies, email responses, web forms, phone calls). The system should use flexible natural language processing to detect revocation intent beyond specific keywords (e.g., "STOP", "UNSUBSCRIBE", "REMOVE ME", "NO MORE"). Build automated workflows to process revocation requests within 24-48 hours maximum, maintain revocation logs with timestamps, and ensure revoked consent is immediately honored across all communication channels. Include testing frameworks to verify revocation handling works correctly under various scenarios.

---

### TCPA-008: Time of Day Restrictions

**LEGAL QUESTION**

Does the system enforce time-of-day restrictions for outbound calls and messages, ensuring they are not sent before 8:00 AM or after 9:00 PM in the recipient's local time zone, as required under 47 CFR §64.1200(c)(1)?

**REGULATORY STANDARD**

TCPA 47 CFR §64.1200(c)(1) (Time of Day Restrictions)

**EVIDENCE**

- `.github/workflows/codeql-analysis.yml:26` — `schedule:`
- `.github/workflows/scorecard.yml:12` — `schedule:`
- `.github/workflows/upgrade-dependencies.yml:14` — `schedule:`
- `examples/foomedical/README.md:85` — `The "Get Care" page is configured to search for availability with service-type "office-visit". Configure your practition`
- `examples/foomedical/README.md:88` — `"resourceType": "Schedule",`
- `examples/foomedical/src/pages/GetCarePage.tsx:6` — `import { Document, Scheduler, useMedplum } from '@medplum/react';`
- `examples/foomedical/src/pages/GetCarePage.tsx:16` — `const [schedule, loading] = useSearchOne('Schedule');`
- `examples/foomedical/src/pages/GetCarePage.tsx:19` — `if (!schedule) {`
- `examples/foomedical/src/pages/GetCarePage.tsx:33` — `const findUrl = medplum.fhirUrl('Schedule', schedule.id, '$find');`
- `examples/foomedical/src/pages/GetCarePage.tsx:67` — `if (!schedule) {`

**FINDING: 🔴 High Risk**

No evidence found of time-of-day restrictions for outbound calls and messages in the codebase, creating a risk pattern consistent with non-compliance under 47 CFR §64.1200(c)(1). While scheduling functionality exists in examples/foomedical/src/pages/GetCarePage.tsx and appointment reminder systems are present in examples/medplum-demo-bots/src/appointment-bots/, none of the discovered code implements the required 8:00 AM to 9:00 PM recipient local time zone restrictions for TCPA-regulated communications. The evidence shows only general scheduling features and workflow automation without TCPA-specific time controls.

**REMEDIATION DIRECTION**

Implement time-of-day validation controls that check recipient local time zones before sending any outbound calls or messages. This should include: (1) recipient timezone detection/storage, (2) validation logic that prevents communications outside 8:00 AM - 9:00 PM windows, (3) queuing mechanisms to defer messages until permitted hours, and (4) integration of these controls into all outbound communication pathways including the appointment reminder bots and any other messaging systems. The existing scheduling infrastructure in the codebase could be extended to support these TCPA compliance requirements.

---

**DISCLAIMER:** OpenDocket identifies risk patterns through automated code analysis. Findings represent potential areas of concern, not legal determinations. This report does not constitute legal advice. Regulatory compliance requires qualified legal and technical assessment. Consult a licensed attorney and certified compliance professional for definitive compliance determination.
