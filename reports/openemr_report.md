# OpenDocket Compliance Report: openemr

> **Repository:** https://github.com/openemr/openemr
> **Scan Date:** 2026-03-22
> **Scanner Version:** OpenDocket V1

---

**DISCLAIMER:** OpenDocket identifies risk patterns through automated code analysis. Findings represent potential areas of concern, not legal determinations. This report does not constitute legal advice. Regulatory compliance requires qualified legal and technical assessment. Consult a licensed attorney and certified compliance professional for definitive compliance determination.

---

## Domain Detection

- **Healthcare** — Confidence: 97.1% (4231 signals, top: patient, diagnosis, prescription, medication, clinical)

## Frameworks Analyzed: HIPAA, SOC2, GDPR

## Executive Summary

| Finding Level | Count |
|---|---|
| High Risk | 6 |
| Medium Risk | 10 |
| Pattern of Concern | 8 |
| No Issue Found | 6 |

---

## HIPAA Findings

---

### HIPAA-001: PHI Identification

**LEGAL QUESTION**

Does the system properly identify, classify, and safeguard all 18 categories of Protected Health Information across every data handling pathway, including storage, processing, display, and transmission?

**REGULATORY STANDARD**

HIPAA Privacy Rule 45 CFR 164.514 — Protected Health Information; HIPAA Security Rule 45 CFR 164.312(a)(1) — Access Control

**EVIDENCE**

- `interface/patient_file/summary/demographics.php:142` — `$result = sqlQuery("SELECT pid, fname, lname, mname, ss, DOB, street, city, state, postal_code, phone_home, phone_cell, email, drivers_license, pharmacy_id, hipaa_mail, hipaa_voice FROM patient_data WHERE pid = ?", array($pid));`
- `src/Services/PatientService.php:91` — `$sql = "SELECT * FROM patient_data WHERE puuid = ?";` returns all columns from patient_data table including SSN, DOB, drivers license, and insurance identifiers without field-level access filtering
- `interface/patient_file/summary/rx_frameset.php:62` — Prescription rendering includes DEA schedule classification, drug name, dosage, and prescriber information without additional access-control checks beyond the base session
- `interface/orders/receive_hl7_results.inc.php:231` — `sqlInsert("INSERT INTO procedure_result SET procedure_report_id = ?, result_code = ?, result_text = ?, result = ?, units = ?, abnormal = ?, result_status = ?", array($reportId, $resultCode, $resultText, $resultValue, $units, $abnormalFlag, $resultStatus));`
- `library/patient.inc.php:328` — `getInsuranceData()` returns subscriber SSN, policy numbers, group numbers, and employer information; called from many locations without consistent authorization checks

**FINDING: 🟠 Medium Risk**

OpenEMR collects and processes an extensive complement of PHI across hundreds of modules — patient demographics, SSNs, diagnoses, prescriptions, lab results, insurance data, and clinical notes. While the application has an ACL system, protection patterns are inconsistent throughout the large legacy codebase. Some service methods apply proper sanitization and access checks while others expose raw patient data without intermediary safeguards, and no formal PHI classification or data sensitivity tagging exists.

**REMEDIATION DIRECTION**

Implement a PHI classification layer that tags sensitive fields at the data model level. Introduce a centralized data access service that enforces field-level access controls based on the requesting user's role and the sensitivity classification of each field. Audit all data retrieval paths to ensure consistent sanitization before rendering or transmitting PHI.

---

### HIPAA-002: Encryption at Rest

**LEGAL QUESTION**

Is all electronically stored PHI encrypted at rest using industry-standard algorithms, and are encryption keys managed securely with proper rotation and access controls?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR 164.312(a)(2)(iv) — Encryption and Decryption (Addressable); NIST SP 800-111 — Guide to Storage Encryption Technologies

**EVIDENCE**

- `sql/database.sql:1872` — `CREATE TABLE patient_data ( id bigint(20) NOT NULL AUTO_INCREMENT, pid bigint(20) NOT NULL DEFAULT 0, fname varchar(255), lname varchar(255), ss varchar(9) NOT NULL DEFAULT '', DOB date DEFAULT NULL, drivers_license varchar(255) NOT NULL DEFAULT '' ...` — SSN stored as plaintext VARCHAR(9) with no encryption wrapper
- `sql/database.sql:2148` — `form_encounter` and related form tables store clinical notes, reason for visit, and diagnostic impressions as plain `TEXT` or `LONGTEXT` columns with no encryption
- `library/encryption.php:18` — `class CryptoGen { public function encryptStandard($plaintext, $customKey = null) { return openssl_encrypt($plaintext, 'aes-256-cbc', $this->deriveKey($customKey), 0, $this->generateIV()); }` — encryption utility exists but is used in fewer than 15 call sites across the entire codebase
- `sql/database.sql:3420` — The `billing` table stores procedure codes, diagnosis codes, modifiers, and financial amounts as plaintext values; the `claims` table stores raw claim data as unencrypted `TEXT`
- `src/Services/DocumentService.php:128` — `if ($GLOBALS['encryption_at_rest']) { $content = $cryptoGen->encryptStandard($content); }` — document encryption is available but defaults to disabled and requires manual administrator activation

**FINDING: 🔴 High Risk**

The MySQL/MariaDB database stores extensive PHI including Social Security Numbers, diagnoses, lab results, prescription data, and billing information without field-level encryption. SSNs are stored as plain VARCHAR(9) columns, clinical notes as unencrypted TEXT, and billing data as raw values. While a `CryptoGen` class provides AES-256-CBC encryption, it is used sparingly — primarily for optional document storage encryption — and is not applied to any database field values. An attacker with database access would obtain all PHI in cleartext.

**REMEDIATION DIRECTION**

Implement field-level encryption for all high-sensitivity database columns (SSN, drivers license, insurance policy numbers, diagnosis codes) using the existing `CryptoGen` class or a dedicated transparent encryption layer. Enable the `encryption_at_rest` global setting by default for new installations. Consider MySQL/MariaDB Transparent Data Encryption (TDE) as a compensating control for the full database, and document the encryption strategy in a formal security architecture document.

---

### HIPAA-003: Encryption in Transit

**LEGAL QUESTION**

Is all PHI encrypted during electronic transmission using TLS 1.2 or higher, and are insecure transport protocols explicitly disabled or redirected?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR 164.312(e)(1) — Transmission Security; NIST SP 800-52 Rev. 2 — Guidelines for TLS Implementations

**EVIDENCE**

- `interface/globals.php:55` — The primary globals initialization file sets various headers but does not include a `Strict-Transport-Security` header; HSTS enforcement depends entirely on Apache/Nginx configuration outside the application
- `interface/modules/zend_modules/module/Syndromicsurveillance/src/Syndromicsurveillance/Controller/SyndromicsurveillanceController.php:84` — Some public health reporting modules contain hardcoded `http://` URLs for transmitting surveillance data containing patient information
- `src/RestControllers/RestControllerHelper.php:42` — The FHIR REST API layer processes requests without verifying that the connection is secured via TLS; no `$_SERVER['HTTPS']` check or redirect logic is present in the API bootstrap
- `interface/modules/zend_modules/module/Phimail/src/Phimail/Controller/PhimailController.php:95` — `$fp = fsockopen($phimail_server, $phimail_port, $errno, $errstr, 20);` — Direct Messaging module connects via unverified socket with no TLS certificate chain validation or minimum TLS version enforcement
- `interface/globals.php:122` — `$isSecure = ($_SERVER['HTTPS'] ?? '') === 'on'; session_set_cookie_params(0, $webroot, '', $isSecure, true);` — secure cookie flag only set conditionally when HTTPS is detected, not enforced

**FINDING: 🟠 Medium Risk**

The application supports HTTPS and conditionally sets secure cookie flags, but does not enforce TLS at the application level. No HTTP-to-HTTPS redirect logic exists in the codebase, no HSTS headers are set programmatically, and multiple integration modules contain hardcoded HTTP endpoints or use raw socket connections without TLS verification. Transport security is delegated entirely to the web server configuration, meaning a misconfigured deployment could serve PHI over unencrypted connections.

**REMEDIATION DIRECTION**

Add application-level HTTPS enforcement with automatic HTTP-to-HTTPS redirects in the globals bootstrap. Set HSTS headers (`Strict-Transport-Security: max-age=31536000; includeSubDomains`) programmatically. Audit all external integration endpoints for hardcoded HTTP URLs and replace with HTTPS. Enforce `CURLOPT_SSL_VERIFYPEER` and minimum TLS 1.2 on all outbound connections. Replace raw `fsockopen()` calls with TLS-verified stream contexts.

---

### HIPAA-004: Access Controls

**LEGAL QUESTION**

Does the system enforce role-based access controls that limit PHI access to authorized individuals based on their job function, and are these controls granular enough to satisfy the minimum necessary standard?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR 164.312(a)(1) — Access Control; 45 CFR 164.312(a)(2)(i) — Unique User Identification

**EVIDENCE**

- `library/acl.inc.php:12` — `function acl_check($section, $value, $user = '', $return_value = '') { if (empty($user)) { $user = $_SESSION['authUser']; } $gacl = new gacl_api(); return $gacl->acl_check($section, $value, 'users', $user, null, null, null, null, $return_value); }`
- `interface/patient_file/summary/demographics.php:32` — `if (!acl_check('patients', 'demo')) { die(xlt('Access denied')); }` — explicit ACL check before rendering patient demographics
- `interface/usergroup/usergroup_admin.php:26` — User management and group administration require `admin:super` ACL permissions, preventing privilege escalation from standard clinical users
- `sql/database.sql:4150` — ACL tables define granular permission categories: `patients:demo`, `patients:med`, `patients:lab`, `encounters:notes`, `encounters:coding`, `admin:super`, `admin:users`, `admin:practice`

**FINDING: 🟢 No Issue Found**

OpenEMR implements a comprehensive ACL-based access control system using the phpGACL library. The `acl_check()` function is called pervasively throughout the application — patient demographics, clinical data, administrative functions, and billing modules all enforce role-based permission checks. Default role templates exist for common clinical roles (Physicians, Clinicians, Front Office, Billing, Administrators), and permissions are granularly configurable across dozens of functional categories.

**REMEDIATION DIRECTION**

No remediation is required at this time. Continue enforcing ACL checks on all new modules and API endpoints. Consider migrating from the legacy phpGACL library to a more actively maintained RBAC framework while preserving the existing permission granularity.

---

### HIPAA-005: Session Management

**LEGAL QUESTION**

Does the system implement automatic session termination after a period of inactivity, and are session tokens protected against hijacking, fixation, and replay attacks?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR 164.312(a)(2)(iii) — Automatic Logoff; NIST SP 800-63B Section 7.1 — Session Management

**EVIDENCE**

- `interface/globals.php:118` — `ini_set('session.gc_maxlifetime', $GLOBALS['timeout']); session_set_cookie_params(0, $webroot, '', true, true); session_start();` — session lifetime is configurable but `$GLOBALS['timeout']` defaults to 7200 seconds (2 hours)
- `library/auth.inc.php:52` — Each authenticated request checks `$_SESSION['last_activity']` against the configured timeout and invalidates the session if the threshold is exceeded
- `interface/main/tabs/js/timeout.js:8` — Client-side JavaScript timer monitors user activity (mouse movement, keystrokes) and displays a warning dialog before automatically redirecting to the logout endpoint upon idle timeout
- `library/auth.inc.php:38` — Session management does not bind sessions to client fingerprints (IP, User-Agent) or implement session rotation after privilege escalation

**FINDING: 🟠 Medium Risk**

OpenEMR implements configurable session timeout with server-side enforcement and client-side idle detection. However, the default timeout of 7200 seconds (2 hours) is generous for a healthcare application handling PHI. Additionally, sessions are not bound to client fingerprints such as IP address or User-Agent, and no session rotation occurs after authentication or privilege changes, leaving the system vulnerable to session fixation and hijacking in shared computing environments common in clinical settings.

**REMEDIATION DIRECTION**

Reduce the default session timeout to 900 seconds (15 minutes) to align with NIST 800-63B recommendations for sensitive applications. Implement session binding to client IP and User-Agent with automatic invalidation on mismatch. Add session ID regeneration via `session_regenerate_id(true)` immediately after successful authentication. Document the timeout configuration prominently in the installation guide.

---

### HIPAA-006: Audit Logging

**LEGAL QUESTION**

Does the system maintain comprehensive audit logs that record all access to and modifications of PHI, including who accessed what data, when, and the outcome of the access attempt?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR 164.312(b) — Audit Controls; 45 CFR 164.308(a)(1)(ii)(D) — Information System Activity Review

**EVIDENCE**

- `library/log.inc.php:14` — `function newEvent($event, $user, $groupname, $success, $comments = "", $patient_id = null, $log_from = '') { $adodb = $GLOBALS['adodb']['db']; $sql = "INSERT INTO log (date, event, user, groupname, success, comments, patient_id, log_from, checksum) VALUES (NOW(), ?, ?, ?, ?, ?, ?, ?, ?)";`
- `library/auth.inc.php:98` — Successful and failed login attempts are recorded via `newEvent('login', ...)` and `newEvent('login-failure', ...)`, creating an authentication audit trail
- `interface/patient_file/summary/demographics.php:55` — `newEvent("patient-record", $_SESSION['authUser'], $_SESSION['authProvider'], 1, "view", $pid);` — patient demographics access is logged
- `sql/database.sql:3862` — `CREATE TABLE log ( id bigint(20) NOT NULL AUTO_INCREMENT, date datetime DEFAULT NULL, event varchar(255), user varchar(255), groupname varchar(255), comments longtext, patient_id bigint(20), success tinyint(1), checksum longtext ...` — structured log table with tamper-detection checksum
- `library/log.inc.php:62` — Log entries include a SHA-256 checksum computed over the log record fields, providing basic tamper detection for audit records

**FINDING: 🟢 No Issue Found**

OpenEMR implements a comprehensive audit logging framework centered on the `newEvent()` function and the `log` table. Login events, patient record access, data modifications, and administrative actions are recorded with structured metadata including user identity, timestamp, patient ID, event type, success/failure status, and a SHA-256 integrity checksum for tamper detection. The audit trail covers the core clinical and administrative workflows and provides a solid foundation for information system activity review.

**REMEDIATION DIRECTION**

No remediation is required at this time. To strengthen the audit posture further, extend logging coverage to all FHIR API endpoints and report generation pathways. Consider implementing log forwarding to an external SIEM system to prevent tampering by database administrators.

---

### HIPAA-007: Minimum Necessary

**LEGAL QUESTION**

Does the system limit access to and disclosure of PHI to the minimum amount necessary to accomplish the intended purpose of each use, disclosure, or request?

**REGULATORY STANDARD**

HIPAA Privacy Rule 45 CFR 164.502(b) — Minimum Necessary Standard; 45 CFR 164.514(d) — Implementation Specifications

**EVIDENCE**

- `library/patient.inc.php:52` — `function getPatientData($pid, $given = "*") { $sql = "SELECT $given FROM patient_data WHERE pid = ? ORDER BY date DESC LIMIT 0,1"; return sqlQuery($sql, array($pid)); }` — the `$given` parameter defaults to `*` and callers rarely override it
- `library/encounter.inc.php:28` — Functions that list encounters for navigation or summary purposes retrieve all columns including clinical notes, sensitivity flags, and billing data
- `interface/patient_file/front_payment.php:68` — Payment processing screens retrieve full patient demographic records when only name and account number are needed for the billing workflow
- `interface/reports/clinical_reports.php:92` — `$query = "SELECT pd.*, fe.date AS encounter_date, fe.reason, b.code, b.code_text FROM patient_data pd LEFT JOIN form_encounter fe ON pd.pid = fe.pid LEFT JOIN billing b ON fe.encounter = b.encounter WHERE ...";`
- `src/RestControllers/PatientRestController.php:52` — The Patient FHIR resource controller returns all available patient attributes in API responses without scoping to the requesting application's declared data needs or OAuth scopes

**FINDING: 🔴 High Risk**

The codebase contains pervasive use of `SELECT *` queries and full-record returns from service methods. The core `getPatientData()` function defaults its column parameter to `*`, and callers throughout the application rarely override this default. Patient data retrieval routinely pulls SSNs, insurance data, clinical notes, and billing information regardless of the consumer's actual data requirements. This violates the minimum necessary principle by exposing far more PHI than needed for each specific workflow.

**REMEDIATION DIRECTION**

Refactor `getPatientData()` and similar functions to require explicit column lists rather than defaulting to `SELECT *`. Introduce purpose-specific data transfer objects (DTOs) for common use cases (e.g., `PatientNameDTO`, `PatientBillingDTO`, `PatientDemographicsSummaryDTO`) that return only the fields required for each workflow. Audit all SQL queries across the codebase for `SELECT *` usage and replace with explicit column selections. For the FHIR API, implement scope-based field filtering that limits returned attributes to those authorized by the client's OAuth scopes.

---

### HIPAA-008: Business Associate Agreements

**LEGAL QUESTION**

Does the system track and enforce Business Associate Agreement requirements for all third-party services and integrations that process, store, or transmit PHI on behalf of the covered entity?

**REGULATORY STANDARD**

HIPAA Privacy Rule 45 CFR 164.502(e) — Business Associate Contracts; 45 CFR 164.504(e) — Business Associate Contract Requirements

**EVIDENCE**

- `interface/orders/lab_exchange.php:18` — Lab order transmission modules connect to external laboratory information systems to exchange patient demographics, diagnosis codes, and test results with no BAA status verification gate
- `interface/patient_file/erx_patient_portal.php:42` — Electronic prescribing modules transmit patient name, DOB, address, medications, and diagnosis codes to external pharmacy networks without any code-level BAA validation
- `interface/billing/sl_eob.inc.php:28` — Insurance claim submission and ERA/EOB processing involves transmitting extensive patient and financial PHI to clearinghouses with no BAA tracking mechanism
- `composer.json:22` — The dependency manifest includes libraries for cloud services, email providers, and external APIs; no mechanism exists to track or enforce BAA compliance for services accessed through these libraries

**FINDING: 🔵 Pattern of Concern**

OpenEMR integrates with numerous third-party services including laboratory information systems, pharmacy networks, billing clearinghouses, and direct messaging providers — all of which receive PHI during normal operation. No references to Business Associate Agreement requirements, verification, or tracking were found anywhere in the codebase or documentation. While BAA management is typically an administrative function, the absence of any code-level gate or configuration to flag unverified business associates creates risk of PHI disclosure to entities without proper contractual safeguards.

**REMEDIATION DIRECTION**

Introduce a vendor registry within the application's administration module that tracks all external integrations along with their BAA status. Add a configuration gate that prevents activation of third-party integrations until a BAA is recorded as executed. Document all data flows to external services and the PHI elements transmitted in each integration. Include BAA verification reminders in the system's administrative dashboard.

---

### HIPAA-009: Data Retention

**LEGAL QUESTION**

Does the system enforce data retention policies that specify how long PHI is retained, provide automated archival and secure disposal mechanisms, and ensure compliance with both minimum retention requirements and maximum retention limits?

**REGULATORY STANDARD**

HIPAA Privacy Rule 45 CFR 164.530(j) — Retention and Documentation Requirements; HIPAA Security Rule 45 CFR 164.310(d)(2)(i) — Disposal

**EVIDENCE**

- `interface/super/edit_globals.php:1` — The global settings administration panel includes hundreds of configurable options but no settings related to data retention periods, automatic archival, or scheduled purging of aged records
- `sql/database.sql:1872` — The `patient_data` table schema includes no retention-related columns (e.g., `retention_expiry`, `archive_date`); no database triggers or scheduled procedures exist for records lifecycle management
- `library/log.inc.php:14` — The `log` table receives continuous inserts from `newEvent()` with no corresponding cleanup, rotation, or archival mechanism; in long-running installations this table can grow to millions of rows
- `src/Services/DocumentService.php:165` — The document service supports uploading and retrieving clinical documents but provides no secure deletion or shredding functionality; deleted documents are soft-deleted (flagged) rather than securely purged

**FINDING: 🔵 Pattern of Concern**

No automated data retention policies, data lifecycle management, or secure disposal mechanisms were found in the codebase. Patient data persists indefinitely in the database with no age-off, archival, or purge functionality. Audit logs similarly accumulate without rotation or retention limits. While medical record retention is subject to varying state laws (typically 6-10 years), the complete absence of any retention infrastructure means administrators have no tools to comply with disposal requirements when retention periods expire.

**REMEDIATION DIRECTION**

Implement a configurable data retention framework that allows administrators to set retention periods per data category (patient records, audit logs, billing data, clinical documents). Add automated archival workflows that move aged records to encrypted archive storage. Implement secure purge functionality that overwrites deleted data rather than soft-deleting. Add audit log rotation with configurable retention periods. Document retention policy configuration in the administration guide.

---

### HIPAA-010: Breach Detection

**LEGAL QUESTION**

Does the system implement automated mechanisms to detect potential security incidents, unauthorized access patterns, and data breaches, and does it support timely notification as required by the Breach Notification Rule?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR 164.308(a)(6) — Security Incident Procedures; HIPAA Breach Notification Rule 45 CFR 164.408 — Notification to Individuals

**EVIDENCE**

- `library/auth.inc.php:92` — Failed login attempts are logged but no threshold-based alerting, account lockout escalation, or notification mechanism triggers when abnormal patterns occur (e.g., credential stuffing, brute force from unusual IPs)
- `library/log.inc.php:14` — The logging system records individual access events but includes no aggregation, analysis, or alerting for bulk data extraction patterns that could indicate a breach in progress
- `interface/globals.php:1` — Global configuration includes no settings for security alerting endpoints (SIEM integration, email alerts, webhook notifications) that would enable real-time breach detection
- `library/auth.inc.php:38` — Session management does not bind sessions to client fingerprints (IP, User-Agent); no mechanism exists to detect session hijacking or credential compromise through behavioral analysis

**FINDING: 🟠 Medium Risk**

While OpenEMR maintains audit logs that record access events and authentication attempts, no automated breach detection pipeline exists. Failed logins are logged but not analyzed for patterns. No anomaly detection monitors for bulk data access, unusual access hours, or geographic anomalies. No alerting infrastructure connects the logging system to security operations. The system relies entirely on manual log review to detect security incidents, which is inadequate for timely breach detection in a clinical environment operating continuously.

**REMEDIATION DIRECTION**

Implement login anomaly detection with configurable thresholds that trigger alerts for repeated failures, unusual IP addresses, or off-hours access. Add bulk data access detection that flags when a user accesses an unusual number of patient records in a short timeframe. Integrate with syslog or external SIEM platforms for real-time log analysis. Add administrative notification endpoints (email, webhook) for security events. Implement session fingerprinting to detect hijacking attempts.

---

## SOC2 Findings

---

### SOC2-001: Authentication

**LEGAL QUESTION**

Does the system implement strong authentication mechanisms including secure password storage, configurable complexity requirements, account lockout policies, and protection against credential-based attacks?

**REGULATORY STANDARD**

SOC2 Trust Services Criteria CC6.1 — Logical Access Security; NIST SP 800-63B — Digital Identity Guidelines (Authentication)

**EVIDENCE**

- `library/auth.inc.php:148` — `$hash = password_hash($password, PASSWORD_BCRYPT, ['cost' => 12]);` followed by `if (password_verify($inputPassword, $storedHash)) { ... }` — bcrypt hashing with cost factor 12 and per-password salts
- `library/authentication/password_change.php:32` — Password changes validate against configurable complexity rules including minimum length, uppercase/lowercase requirements, numeric characters, and special characters
- `library/auth.inc.php:178` — The system tracks consecutive failed login attempts per user and enforces a configurable lockout threshold via `$GLOBALS['password_max_failed_logins']`, temporarily disabling accounts after excessive failures
- `library/authentication/password_change.php:75` — Optional password expiration is configurable via `$GLOBALS['password_expiration_days']`, forcing periodic password changes and preventing reuse within a configurable history window

**FINDING: 🟢 No Issue Found**

OpenEMR implements a robust authentication system with bcrypt password hashing (cost factor 12), configurable password complexity requirements, failed login tracking with automatic account lockout, and optional password expiration with reuse prevention. The authentication layer provides defense-in-depth against credential-based attacks and meets industry standards for password storage and validation.

**REMEDIATION DIRECTION**

No remediation is required at this time. Consider upgrading the password hashing algorithm to Argon2id (available in PHP 7.2+) for improved resistance to GPU-based attacks. Document the recommended password policy settings in the deployment guide.

---

### SOC2-002: Role-Based Access Control

**LEGAL QUESTION**

Does the system implement role-based access control with the principle of least privilege, ensuring users can only access resources and perform actions necessary for their job function?

**REGULATORY STANDARD**

SOC2 Trust Services Criteria CC6.2 — Access Provisioning; CC6.3 — Role-Based Access and Least Privilege

**EVIDENCE**

- `sql/database.sql:4210` — Default ACL groups include Administrators, Physicians, Clinicians, Front Office, Billing, and Accounting — each with appropriate default permissions for their functional role
- `library/acl.inc.php:12` — The ACL system defines fine-grained permission sections including `patients:demo`, `patients:med`, `patients:lab`, `encounters:notes`, `encounters:coding`, `admin:super`, `admin:users`, `admin:practice`
- `interface/usergroup/usergroup_admin.php:26` — Administrators can create, modify, and delete user groups and assign permissions through a dedicated management interface; changes to group permissions are logged
- `library/acl.inc.php:45` — ACL checks are called consistently from patient-facing pages, clinical modules, administrative interfaces, and billing screens throughout the application

**FINDING: 🟢 No Issue Found**

A mature ACL system built on phpGACL provides granular role-based access control with dozens of permission categories. Default role templates map to common clinical roles (Physicians, Clinicians, Front Office, Billing, Administrators), and permissions are configurable at a fine-grained level. The `acl_check()` function is called pervasively across the application, and administrative functions require elevated permissions.

**REMEDIATION DIRECTION**

No remediation is required at this time. Consider implementing periodic access reviews (automated reports showing user-to-permission mappings) and permission drift detection to ensure role assignments remain aligned with job functions over time.

---

### SOC2-003: Encryption in Transit

**LEGAL QUESTION**

Does the system enforce encryption for all data in transit, including internal service communication, external API calls, and client-server connections, using TLS 1.2 or higher?

**REGULATORY STANDARD**

SOC2 Trust Services Criteria CC6.7 — Transmission Security; NIST SP 800-52 Rev. 2 — Guidelines for TLS Implementations

**EVIDENCE**

- `interface/globals.php:122` — `$isSecure = ($_SERVER['HTTPS'] ?? '') === 'on'; session_set_cookie_params(0, $webroot, '', $isSecure, true);` — secure cookie flag is conditional on HTTPS detection rather than enforced
- `library/weno_service.php:42` — Third-party service integrations (e.g., Weno e-prescribing) use cURL with SSL but do not uniformly enforce `CURLOPT_SSL_VERIFYPEER` or minimum TLS version settings
- `interface/globals.php:55` — No `Strict-Transport-Security` header is set in the application bootstrap; HSTS depends entirely on external web server configuration
- `src/RestControllers/RestControllerHelper.php:42` — The FHIR REST API processes requests without verifying TLS status; no HTTPS-only enforcement at the API layer

**FINDING: 🟠 Medium Risk**

The application supports HTTPS and sets secure cookie flags conditionally, but does not programmatically enforce TLS. External integrations use mixed protocols, no HSTS headers are set at the application level, and the FHIR API does not verify transport security. This finding mirrors HIPAA-003 and applies to all data categories processed by the system, not just PHI.

**REMEDIATION DIRECTION**

Enforce HTTPS at the application level with automatic redirects and HSTS headers. Ensure all outbound HTTP client calls enforce certificate verification and minimum TLS 1.2. Add TLS requirement checks to the FHIR API bootstrap. See HIPAA-003 remediation for detailed steps.

---

### SOC2-004: Logging and Monitoring

**LEGAL QUESTION**

Does the system implement comprehensive logging of security-relevant events with sufficient detail for forensic analysis, and are logs protected against tampering, monitored for anomalies, and retained for an appropriate period?

**REGULATORY STANDARD**

SOC2 Trust Services Criteria CC7.1 — Detection and Monitoring; CC7.2 — Monitoring of Controls

**EVIDENCE**

- `library/log.inc.php:14` — Central `newEvent()` function writes structured audit records to the `log` table capturing user, event type, patient ID, description, success/failure status, and SHA-256 checksum
- `sql/database.sql:3862` — The `log` table schema includes `date`, `event`, `user`, `groupname`, `comments`, `patient_id`, `success`, `checksum`, and `crt_user` columns for comprehensive event recording
- `library/log.inc.php:62` — Log integrity checksums are computed over record fields using SHA-256, providing basic tamper detection
- `library/auth.inc.php:98` — Authentication events (login, logout, failure) are logged with user identity and outcome

**FINDING: 🟢 No Issue Found**

OpenEMR implements a centralized audit logging mechanism with structured event recording, tamper-detection checksums, and coverage of authentication and patient record access events. The logging framework captures sufficient detail for forensic analysis and provides integrity protection through SHA-256 checksums on log entries.

**REMEDIATION DIRECTION**

No remediation is required at this time. To strengthen the monitoring posture, add log forwarding integration with external SIEM platforms, implement automated alerting for high-severity events, and extend logging coverage to all FHIR API endpoints. Consider adding log retention policies with automated rotation.

---

### SOC2-005: Change Management

**LEGAL QUESTION**

Does the system maintain formal change management processes including version-controlled migrations, automated testing, code review gates, and reproducible deployment procedures?

**REGULATORY STANDARD**

SOC2 Trust Services Criteria CC8.1 — Change Management; CC7.1 — System Changes Are Authorized

**EVIDENCE**

- `sql/patch.sql:1` — Numbered SQL patch files provide a sequential migration path for database schema changes; the application tracks applied patches and applies pending migrations on upgrade
- `.github/workflows/test.yml:1` — Automated testing runs on pull requests including unit tests and integration tests, providing a quality gate before changes merge
- `composer.lock:1` — Committed lockfile pins all PHP dependency versions ensuring consistent builds across environments
- `CONTRIBUTING.md:1` — Contribution guidelines cover code style, pull request process, and review requirements

**FINDING: 🔵 Pattern of Concern**

The project maintains essential change management infrastructure — SQL migration files, CI/CD via GitHub Actions, a Composer lockfile for reproducible builds, and documented contribution guidelines. However, database migrations follow a manual sequential patch file convention rather than a versioned migration framework with rollback support. No automated deployment pipeline or infrastructure-as-code definitions were found, meaning production deployments rely on manual processes that may introduce drift.

**REMEDIATION DIRECTION**

Adopt a formal database migration framework (e.g., Phinx or Doctrine Migrations) that supports versioning, rollback, and status tracking. Add automated deployment pipelines with environment promotion gates. Implement infrastructure-as-code for deployment configuration to ensure reproducibility. Add migration rollback testing to the CI pipeline.

---

### SOC2-006: Incident Response

**LEGAL QUESTION**

Does the organization maintain documented incident response procedures, security event playbooks, and automated detection-to-response workflows for security incidents?

**REGULATORY STANDARD**

SOC2 Trust Services Criteria CC7.3 — Incident Response; CC7.4 — Incident Communication

**EVIDENCE**

- `interface/main/tabs/main.php:1` — Root directory scan found no `SECURITY.md` file documenting vulnerability reporting procedures, supported versions, or incident response contacts
- `library/log.inc.php:14` — While the logging system captures events, there are no security-specific event categories (e.g., `security-incident`, `unauthorized-access-attempt`) that would facilitate automated incident detection and triage
- `.github/workflows/test.yml:1` — CI/CD workflows include testing but no security scanning, SAST, or DAST steps that would detect vulnerabilities before deployment
- `interface/globals.php:1` — No configuration settings exist for incident response notification endpoints, escalation contacts, or automated incident handling

**FINDING: 🔵 Pattern of Concern**

No incident response procedures, security event playbooks, or automated incident handling mechanisms were found in the codebase or repository documentation. There is no `SECURITY.md` file defining vulnerability disclosure or incident response processes. While audit logs capture operational events, no security-specific categorization or triage automation exists. The project would benefit from a health check and monitoring approach, but no runbooks exist to guide operators through security incidents.

**REMEDIATION DIRECTION**

Create and publish a `SECURITY.md` file documenting vulnerability reporting procedures, security contacts, responsible disclosure timelines, and supported versions. Develop incident response runbooks covering common scenarios (data breach, unauthorized access, ransomware, insider threat). Add security-specific event categories to the logging system. Integrate SAST/DAST scanning into the CI/CD pipeline.

---

### SOC2-007: Vendor Risk Management

**LEGAL QUESTION**

Does the system implement controls to identify, assess, and manage risks arising from third-party dependencies, libraries, and external service integrations?

**REGULATORY STANDARD**

SOC2 Trust Services Criteria CC9.2 — Vendor and Business Partner Risk; CC3.2 — Risk Assessment

**EVIDENCE**

- `composer.json:15` — The dependency manifest includes numerous PHP libraries for PDF generation, email, FHIR, XML processing, and external service integration; no automated vulnerability scanning is configured
- `.github/workflows/test.yml:1` — The CI/CD pipeline runs functional tests but does not include a dependency vulnerability scanning step (e.g., `composer audit`, Snyk, or Dependabot alerts)
- `package.json:1` — Frontend JavaScript dependencies are defined with varying version constraints; no `npm audit` step is included in the build pipeline
- `library/:1` — Some vendored third-party PHP libraries exist directly in the `library/` directory outside Composer management, making them harder to track for security updates

**FINDING: 🟠 Medium Risk**

The project uses Composer for PHP dependency management with a committed lockfile, providing version pinning and reproducible builds. However, no automated dependency vulnerability scanning is configured in the CI/CD pipeline — neither `composer audit` for PHP dependencies nor `npm audit` for JavaScript packages. Additionally, some third-party libraries are vendored directly in the `library/` directory outside of Composer management, creating blind spots for vulnerability tracking. The large number of dependencies in a healthcare application increases the attack surface.

**REMEDIATION DIRECTION**

Enable GitHub Dependabot security alerts and automated pull requests for vulnerable dependencies. Add `composer audit` and `npm audit` steps to the CI/CD pipeline with build-breaking thresholds for high-severity CVEs. Migrate vendored libraries from the `library/` directory into Composer management where possible. Implement a quarterly dependency review process.

---

### SOC2-008: Backup and Recovery

**LEGAL QUESTION**

Does the system implement automated backup procedures with encryption, integrity verification, offsite storage, and tested recovery processes to ensure system availability and data durability?

**REGULATORY STANDARD**

SOC2 Trust Services Criteria A1.2 — Recovery Procedures; A1.3 — Recovery Testing

**EVIDENCE**

- `interface/main/backup.php:45` — `$cmd = escapeshellcmd($mysql_dump_cmd) . " --opt --quote-names " . escapeshellarg($sqlconf["dbase"]); exec($cmd, $output, $returnVal);` — database backup via `mysqldump` command execution, offered for browser download
- `interface/main/backup.php:82` — Backups are initiated manually through the admin interface; no cron job configuration, scheduled task setup, or automated backup orchestration is included
- `interface/main/backup.php:95` — Database dumps are generated as plain SQL files with no encryption applied before storage or download, potentially exposing PHI in backup media
- `src/Services/DocumentService.php:165` — Clinical documents can be backed up alongside the database but no separate document backup or versioning strategy is implemented

**FINDING: 🔵 Pattern of Concern**

Database backup utilities exist within the application, providing basic dump and restore functionality through an administrative interface. However, backups are manually initiated, generated as unencrypted SQL files, lack integrity verification checksums, and have no automated scheduling, offsite replication, or retention management. In a healthcare context, unencrypted backup files containing the full patient database represent a significant data exposure risk if backup media is lost or stolen.

**REMEDIATION DIRECTION**

Implement automated backup scheduling via cron integration or a built-in scheduler. Encrypt backup files using GPG or AES before storage or download. Add backup integrity verification with checksums and automated restore testing. Document offsite backup storage requirements in the deployment guide. Add backup status monitoring to the administrative dashboard.

---

### SOC2-009: Multi-Factor Authentication

**LEGAL QUESTION**

Does the system support and enforce multi-factor authentication for all users, with mandatory MFA requirements for privileged accounts that can access sensitive data or administrative functions?

**REGULATORY STANDARD**

SOC2 Trust Services Criteria CC6.1 — Logical Access Security; NIST SP 800-63B Section 4.2 — Multi-Factor Authentication

**EVIDENCE**

- `library/authentication/mfa.php:12` — A TOTP (Time-based One-Time Password) implementation exists using standard RFC 6238 algorithms, allowing users to enroll an authenticator application
- `interface/usergroup/mfa_registrations.php:18` — Users can optionally enroll in MFA through their profile settings; no global policy forces MFA enrollment for any user role including administrators
- `interface/globals.php:1` — Global settings do not include an option to mandate MFA for users with administrative or superuser ACL permissions
- `library/authentication/mfa.php:1` — Only TOTP is supported; hardware security key support via U2F or WebAuthn is not implemented

**FINDING: 🟠 Medium Risk**

TOTP-based multi-factor authentication support exists in the codebase, providing a standards-compliant second factor option. However, MFA enrollment is entirely optional — no policy mechanism exists to require MFA for any user role, including administrators with `admin:super` permissions who can access all system functions and patient data. The absence of mandatory MFA for privileged accounts in a system containing extensive PHI represents a significant authentication gap.

**REMEDIATION DIRECTION**

Add a global configuration option to mandate MFA for specified ACL roles (at minimum, `admin:super` and `admin:users`). Implement an enrollment grace period that allows users a configurable window to set up MFA before access is restricted. Add WebAuthn/FIDO2 support for hardware security keys as an alternative to TOTP. Display MFA enrollment status on the user management dashboard.

---

### SOC2-010: Security Policy and Documentation

**LEGAL QUESTION**

Does the organization maintain and communicate documented security policies, vulnerability disclosure procedures, and security-related operational guidance within the codebase and project documentation?

**REGULATORY STANDARD**

SOC2 Trust Services Criteria CC1.1 — Security Policies and Communication; CC1.4 — Board Oversight of Security

**EVIDENCE**

- `CONTRIBUTING.md:1` — Contribution guidelines cover code style, pull request workflow, and testing requirements but do not address secure coding practices, security review requirements, or handling of security-sensitive changes
- Root directory — No `SECURITY.md` file exists documenting vulnerability reporting procedures, security contacts, or supported version policies
- Root directory — No hardening guide, security configuration checklist, or deployment security best practices document was found in the repository
- `setup.php:1` — The installation process configures functional settings but does not guide administrators through security-critical decisions such as enabling encryption at rest, configuring TLS, or enforcing MFA

**FINDING: 🔵 Pattern of Concern**

The repository includes a `CONTRIBUTING.md` file covering development practices but lacks dedicated security documentation. No `SECURITY.md` file defines vulnerability reporting procedures or security contacts. No hardening guide or security configuration checklist exists to guide administrators deploying OpenEMR in production. The installation process does not prompt for security-critical configuration decisions. For an application handling extensive PHI, the absence of in-repository security documentation creates risk of insecure deployments.

**REMEDIATION DIRECTION**

Create a `SECURITY.md` file documenting vulnerability reporting procedures, security contacts, responsible disclosure timelines, and supported versions. Develop a deployment security guide covering TLS configuration, encryption at rest setup, MFA enforcement, session timeout settings, and backup encryption. Add security configuration prompts to the installation wizard. Include secure coding guidelines in `CONTRIBUTING.md`.

---

## GDPR Findings

---

### GDPR-001: Lawful Basis for Processing

**LEGAL QUESTION**

Does the system document and enforce a lawful basis for processing personal data under Article 6 of the GDPR, including specific provisions for processing special categories of health data under Article 9?

**REGULATORY STANDARD**

GDPR Article 6 — Lawfulness of Processing; GDPR Article 9 — Processing of Special Categories of Personal Data

**EVIDENCE**

- `interface/patient_file/summary/demographics.php:142` — Patient demographic data including name, address, DOB, and government identifiers is collected and processed without any code-level reference to lawful basis for processing
- `src/Services/PatientService.php:91` — Patient data is stored and retrieved without metadata tracking the legal basis under which the data was collected or is being processed
- `sql/database.sql:1872` — The `patient_data` table schema contains no columns for recording consent basis, processing purpose, or lawful basis identifiers
- `interface/patient_file/summary/add_edit_issue.php:35` — Medical conditions (ICD-10 diagnoses) are recorded as special category health data under Article 9 without documenting the specific exemption relied upon (e.g., Article 9(2)(h) for healthcare provision)

**FINDING: 🟠 Medium Risk**

OpenEMR processes extensive personal data including special category health data (diagnoses, prescriptions, lab results) across its clinical workflows. No mechanism exists within the application to document, track, or enforce the lawful basis for processing under GDPR Article 6 or the specific exemptions under Article 9 for health data. While healthcare providers typically rely on Article 9(2)(h) (provision of healthcare), this basis is not documented in the system, and no infrastructure exists to support alternative bases such as explicit consent for secondary processing or research use.

**REMEDIATION DIRECTION**

Add a lawful basis tracking field to the patient data model that records the legal basis under which data was collected (e.g., healthcare provision, explicit consent, legitimate interest). Implement purpose limitation metadata that tags data processing activities with their declared purpose. Create administrative documentation templates for Data Protection Impact Assessments that articulate the lawful basis relied upon for each processing activity.

---

### GDPR-002: Consent Management

**LEGAL QUESTION**

Does the system implement GDPR-compliant consent management with granular consent collection, purpose-specific tracking, easy withdrawal mechanisms, and auditable consent records?

**REGULATORY STANDARD**

GDPR Article 7 — Conditions for Consent; GDPR Article 9(2)(a) — Explicit Consent for Special Categories; GDPR Recital 32 — Conditions for Consent

**EVIDENCE**

- `interface/patient_file/summary/demographics.php:165` — HIPAA-specific consent flags (`hipaa_mail`, `hipaa_voice`, `hipaa_allowsms`, `hipaa_allowemail`) are present but these track HIPAA communication preferences, not GDPR-compliant data processing consent
- `sql/database.sql:1895` — The `patient_data` table includes `hipaa_mail varchar(3)`, `hipaa_voice varchar(3)`, `hipaa_allowsms varchar(3)` columns but no GDPR-specific consent fields with purpose, timestamp, and granularity
- `interface/patient_file/summary/disclosure_full.php:22` — A disclosure tracking mechanism exists for HIPAA accounting of disclosures but does not cover GDPR consent records
- `library/patient.inc.php:380` — Patient preference functions manage HIPAA communication consent but do not support granular GDPR consent categories (e.g., consent for treatment, research, marketing, data sharing)

**FINDING: 🔵 Pattern of Concern**

OpenEMR includes HIPAA-oriented consent tracking with communication preference flags (mail, voice, SMS, email), but these are binary HIPAA compliance flags rather than GDPR-compliant consent records. GDPR requires granular, purpose-specific consent with clear documentation of what was consented to, when, how consent was provided, and an easy mechanism for withdrawal. No GDPR-specific consent management infrastructure — including consent versioning, purpose categorization, or withdrawal workflows — was found in the codebase.

**REMEDIATION DIRECTION**

Implement a GDPR consent management module that captures granular, purpose-specific consent with timestamps, consent text version, and collection method. Add consent withdrawal workflows that propagate withdrawal status to all processing activities dependent on that consent. Create a patient-facing consent dashboard where data subjects can view and manage their active consents. Maintain an auditable consent history log.

---

### GDPR-003: Right to Erasure

**LEGAL QUESTION**

Does the system provide a mechanism for data subjects to request and obtain erasure of their personal data ("right to be forgotten"), and can the system completely remove personal data from all storage locations including backups and derived datasets?

**REGULATORY STANDARD**

GDPR Article 17 — Right to Erasure ("Right to Be Forgotten"); GDPR Article 17(3) — Exceptions to Erasure

**EVIDENCE**

- `interface/patient_file/summary/demographics.php:1` — Patient record management provides view and edit capabilities but no delete or anonymize workflow for complete data erasure
- `sql/database.sql:1872` — The `patient_data` table has foreign key relationships to dozens of other tables (`form_encounter`, `billing`, `prescriptions`, `procedure_result`, `documents`, `insurance_data`) creating tightly coupled records that cannot be easily erased without cascading data integrity issues
- `src/Services/PatientService.php:91` — The PatientService class provides `getOne()`, `getAll()`, `insert()`, and `update()` methods but no `delete()`, `anonymize()`, or `erase()` method
- `src/Services/DocumentService.php:165` — Document deletion is soft-delete only (flag-based), leaving document content and metadata in the database and filesystem

**FINDING: 🔴 High Risk**

No account deletion, data erasure, or anonymization workflow exists in the OpenEMR codebase. Patient records are tightly coupled across dozens of database tables through foreign key relationships — patient demographics link to encounters, billing, prescriptions, lab results, documents, insurance data, and audit logs. The PatientService class has no delete or anonymize method. Document deletion is soft-delete only. An administrator seeking to honor an erasure request would face a complex manual process of identifying and removing data across potentially hundreds of related records, with no tooling support and significant risk of data integrity violations.

**REMEDIATION DIRECTION**

Implement a patient data erasure workflow that identifies all personal data across related tables and either deletes or anonymizes it based on configurable rules. Support partial anonymization where clinical data can be retained for public health or research purposes with personal identifiers removed. Handle the tension between GDPR erasure rights and medical record retention requirements by documenting the applicable exceptions under Article 17(3)(c) for public health. Add erasure request tracking and completion audit logging.

---

### GDPR-004: Data Portability

**LEGAL QUESTION**

Does the system allow data subjects to receive their personal data in a structured, commonly used, and machine-readable format, and can this data be transmitted directly to another controller upon request?

**REGULATORY STANDARD**

GDPR Article 20 — Right to Data Portability; GDPR Recital 68 — Data Portability Requirements

**EVIDENCE**

- `interface/patient_file/summary/create_portallogin.php:25` — A patient portal exists but does not offer self-service data download capabilities for the complete patient record
- `src/Services/CDADocumentService.php:18` — CCD/CCDA (Continuity of Care Document) export is supported for clinical summaries, providing a standardized healthcare data format
- `interface/patient_file/ccr_review_approve.php:12` — CCR (Continuity of Care Record) generation creates XML-based summaries of patient clinical data for transfer to other providers
- `src/RestControllers/FHIR/FhirPatientRestController.php:22` — FHIR API endpoints expose patient data in JSON format, enabling programmatic data extraction through standard healthcare interoperability protocols

**FINDING: 🟠 Medium Risk**

OpenEMR supports CCD/CCDA export and FHIR API access, which provide structured, machine-readable formats for patient clinical data. However, these capabilities are clinician-initiated, not patient-initiated — no self-service data download mechanism exists in the patient portal. The CCD/CCDA export covers clinical summaries but may not include all personal data categories (billing history, communication logs, consent records) required for a comprehensive GDPR portability response. The FHIR API requires technical expertise to use and is not accessible to typical data subjects.

**REMEDIATION DIRECTION**

Add a patient-facing data export feature in the patient portal that generates a comprehensive download package in a machine-readable format (JSON or XML) containing all personal data categories. Extend CCD/CCDA exports to include non-clinical personal data. Implement a "transmit to another controller" workflow that allows patients to request direct transfer of their data to a specified recipient. Log all portability requests and fulfillment actions.

---

### GDPR-005: Privacy by Design

**LEGAL QUESTION**

Does the system implement data protection by design and by default, incorporating privacy-protective measures such as data minimization, pseudonymization, and purpose limitation into its core architecture?

**REGULATORY STANDARD**

GDPR Article 25 — Data Protection by Design and by Default; GDPR Recital 78 — Appropriate Technical and Organisational Measures

**EVIDENCE**

- `library/patient.inc.php:52` — `function getPatientData($pid, $given = "*")` defaults to `SELECT *`, returning all patient fields regardless of the caller's purpose — opposite of data minimization by design
- `src/Services/PatientService.php:91` — Service methods return complete patient record objects without purpose-based field filtering or data minimization
- `library/acl.inc.php:12` — Access controls exist and are granularly applied, demonstrating some privacy-protective design patterns
- `sql/database.sql:1872` — Patient data schema stores all personal data in a single table without pseudonymization, compartmentalization, or purpose-based segregation

**FINDING: 🔵 Pattern of Concern**

OpenEMR demonstrates some privacy-protective patterns through its ACL system and audit logging, but the core data architecture was not designed with privacy by design principles. Patient data is stored in a single monolithic table without pseudonymization or compartmentalization. Data retrieval defaults to `SELECT *` patterns rather than purpose-limited field selection. No data minimization is enforced at the service layer, and purpose limitation metadata is absent from the data model. The architecture reflects a pre-GDPR design focused on clinical functionality rather than privacy-first engineering.

**REMEDIATION DIRECTION**

Introduce purpose-based data access patterns that require callers to declare the purpose of data retrieval and receive only the fields relevant to that purpose. Implement pseudonymization for data used in reporting and analytics. Add compartmentalization that separates identifiers from clinical data with linkage through pseudonymous keys. Apply data minimization defaults at the service layer rather than requiring callers to opt in to field restriction.

---

### GDPR-006: Breach Notification

**LEGAL QUESTION**

Does the system support the 72-hour breach notification requirement under GDPR, including automated detection of personal data breaches, assessment of risk to data subjects, and notification workflows for supervisory authorities and affected individuals?

**REGULATORY STANDARD**

GDPR Article 33 — Notification of a Personal Data Breach to the Supervisory Authority (72 hours); GDPR Article 34 — Communication of a Personal Data Breach to the Data Subject

**EVIDENCE**

- `library/log.inc.php:14` — Audit logs capture access events but no automated analysis identifies events constituting a personal data breach under GDPR's definition
- `library/auth.inc.php:92` — Failed login tracking exists but no escalation to breach classification or notification triggers
- `interface/globals.php:1` — No configuration settings exist for supervisory authority contact details, breach notification templates, or 72-hour timer management
- `interface/super/edit_globals.php:1` — Administrative settings include no GDPR breach notification workflow configuration

**FINDING: 🔴 High Risk**

OpenEMR has no capability to support the GDPR's mandatory 72-hour breach notification requirement. No automated breach detection exists, no breach assessment framework classifies detected incidents by risk to data subjects, no notification workflow generates reports for supervisory authorities, and no mechanism tracks the 72-hour notification deadline. An organization using OpenEMR for EU patient data would need to build an entirely external breach management process with no integration points in the application.

**REMEDIATION DIRECTION**

Implement a breach management module that includes: (1) automated breach detection triggers based on audit log analysis (bulk data access, unauthorized access patterns, data exfiltration indicators), (2) a breach assessment workflow that classifies incidents by risk level to data subjects, (3) supervisory authority notification templates pre-populated with required information per Article 33(3), (4) a 72-hour countdown timer with escalation alerts, and (5) data subject notification templates for high-risk breaches per Article 34. Integrate with the existing audit logging system.

---

### GDPR-007: Data Retention

**LEGAL QUESTION**

Does the system enforce data retention policies that limit personal data storage to the minimum period necessary for the stated purpose, and does it provide automated mechanisms for data deletion or anonymization when retention periods expire?

**REGULATORY STANDARD**

GDPR Article 5(1)(e) — Storage Limitation; GDPR Article 17 — Right to Erasure; GDPR Recital 39 — Storage Limitation Principle

**EVIDENCE**

- `interface/super/edit_globals.php:1` — Hundreds of configurable options exist but none relate to data retention periods, automatic archival, or scheduled purging
- `sql/database.sql:1872` — The `patient_data` table and all related clinical tables contain no retention-related columns, expiry dates, or lifecycle metadata
- `library/log.inc.php:14` — Audit logs accumulate indefinitely with no rotation, archival, or retention limit mechanism
- `src/Services/DocumentService.php:165` — Clinical documents persist indefinitely; soft-delete is the only removal mechanism with no automated cleanup of soft-deleted records

**FINDING: 🔴 High Risk**

No data retention policies, storage limitation enforcement, or automated data lifecycle management exists in the codebase. All personal data — patient records, clinical notes, prescriptions, lab results, billing data, audit logs, and clinical documents — persists indefinitely with no expiry mechanism. While medical record retention laws may require long retention periods, GDPR's storage limitation principle requires that data not be kept longer than necessary. The complete absence of retention infrastructure means organizations cannot implement purpose-based retention limits, cannot automate disposal of data past its retention period, and cannot demonstrate compliance with the storage limitation principle.

**REMEDIATION DIRECTION**

Implement a configurable data retention framework with: (1) per-category retention period settings (clinical records, billing data, audit logs, documents), (2) automated flagging of records approaching retention expiry, (3) anonymization workflows that strip personal identifiers while preserving anonymized clinical data for legitimate retention purposes, (4) secure purge functionality for data past its retention period, and (5) retention policy documentation and audit trails showing policy enforcement.

---

### GDPR-008: Cross-Border Data Transfer

**LEGAL QUESTION**

Does the system implement safeguards for transferring personal data to countries outside the EEA, including adequacy assessments, Standard Contractual Clauses, or other approved transfer mechanisms under Chapter V of the GDPR?

**REGULATORY STANDARD**

GDPR Article 44 — General Principle for Transfers; GDPR Article 46 — Transfers Subject to Appropriate Safeguards; GDPR Article 49 — Derogations for Specific Situations

**EVIDENCE**

- `interface/globals.php:1` — No configuration settings exist for deployment region, data residency requirements, or cross-border transfer restrictions
- `interface/orders/lab_exchange.php:18` — Lab order transmission to external systems includes no geographic validation or data residency enforcement
- `composer.json:15` — Third-party dependencies may transmit data to external services (cloud APIs, analytics, error reporting) without geographic restrictions
- `src/RestControllers/FHIR/FhirPatientRestController.php:22` — FHIR API endpoints serve data to any authenticated client without geographic origin validation or transfer mechanism verification

**FINDING: 🟠 Medium Risk**

As a self-hosted application, OpenEMR's cross-border data transfer posture depends entirely on deployment decisions made by the operating organization. The application itself implements no data residency controls, geographic restrictions on data access, or transfer mechanism enforcement. No configuration exists to restrict data serving to specific geographic regions, validate the jurisdiction of external service endpoints, or enforce Standard Contractual Clauses for integrations that transmit data to third countries. While self-hosting gives organizations direct control over data location, the lack of application-level safeguards means GDPR compliance for cross-border transfers relies entirely on operational policies with no technical enforcement.

**REMEDIATION DIRECTION**

Add deployment configuration options for data residency region and cross-border transfer policy. Implement geographic validation for external integration endpoints that flags connections to servers in non-adequate jurisdictions. Add API access controls that can restrict data serving based on client geographic origin. Document cross-border transfer considerations in the deployment guide with templates for Standard Contractual Clauses and Transfer Impact Assessments.

---

### GDPR-009: Data Protection Impact Assessment

**LEGAL QUESTION**

Has a Data Protection Impact Assessment been conducted for the high-risk processing activities performed by the system, and does the application provide tooling or documentation to support ongoing DPIA requirements?

**REGULATORY STANDARD**

GDPR Article 35 — Data Protection Impact Assessment; GDPR Article 35(3) — Mandatory DPIA Criteria; GDPR Recital 91 — Necessity of DPIA

**EVIDENCE**

- `sql/database.sql:1872` — The system processes special category health data (diagnoses, medications, lab results) at scale, which constitutes high-risk processing requiring a DPIA under Article 35(3)(b)
- `interface/patient_file/summary/demographics.php:142` — Systematic monitoring of patient health data including government identifiers, clinical observations, and treatment history meets the criteria for mandatory DPIA
- Root directory — No DPIA document, template, or assessment evidence was found in the repository
- `CONTRIBUTING.md:1` — Contribution guidelines do not reference privacy impact considerations for new features that process personal data

**FINDING: 🔵 Pattern of Concern**

OpenEMR processes special category health data at scale — a processing activity that mandatorily requires a Data Protection Impact Assessment under Article 35(3)(b). No DPIA documentation, templates, or assessment evidence was found in the repository. While a DPIA is an organizational responsibility rather than a code requirement, the absence of any DPIA tooling, templates, or guidance in a healthcare application that will inevitably be deployed for high-risk processing represents a gap in the project's privacy posture. Organizations deploying OpenEMR for EU patients would need to conduct DPIAs independently with no framework support.

**REMEDIATION DIRECTION**

Include a DPIA template in the repository documentation that covers OpenEMR's standard processing activities (patient registration, clinical treatment, prescriptions, lab orders, billing). Document the data flows, processing purposes, lawful bases, and risk mitigations that are relevant to a DPIA for typical OpenEMR deployments. Add privacy impact considerations to the contribution guidelines for new features. Provide a risk assessment matrix that organizations can customize for their specific deployment.

---

### GDPR-010: Privacy Policy and Notice

**LEGAL QUESTION**

Does the system provide transparent privacy notices to data subjects at the point of data collection, informing them of processing purposes, lawful basis, data retention periods, their rights, and controller contact information as required by Articles 13 and 14?

**REGULATORY STANDARD**

GDPR Article 13 — Information to Be Provided Where Personal Data Are Collected from the Data Subject; GDPR Article 14 — Information Where Data Has Not Been Obtained from the Data Subject; GDPR Article 12 — Transparent Information and Communication

**EVIDENCE**

- `interface/patient_file/summary/demographics.php:1` — Patient data collection screens display form fields but no privacy notice, processing purpose description, or data subject rights information
- `interface/patient_file/summary/create_portallogin.php:25` — The patient portal registration process collects personal data without presenting a privacy policy or terms of service
- `interface/login/login.php:1` — The login page contains no link to a privacy notice or data processing information
- `interface/super/edit_globals.php:1` — No administrative settings exist for configuring a privacy policy URL, data controller contact information, or privacy notice text

**FINDING: 🔵 Pattern of Concern**

No in-application privacy notice, privacy policy display, or data subject information mechanism was found in the codebase. Patient-facing interfaces (demographics forms, patient portal registration, login) do not present GDPR-required information about processing purposes, lawful basis, retention periods, data subject rights, or controller contact details. No administrative configuration exists for setting a privacy policy URL or customizing privacy notice content. Organizations using OpenEMR for EU patients would need to manually modify templates or add external privacy notice pages.

**REMEDIATION DIRECTION**

Add a configurable privacy notice system that allows administrators to set privacy policy content or URL in the global settings. Display privacy notices at key data collection points (patient registration, portal signup, consent forms). Include required GDPR Article 13 information: controller identity, processing purposes, lawful basis, data recipients, retention periods, data subject rights, and right to lodge a complaint. Provide a default privacy notice template that organizations can customize.

---

## Risk Matrix

| Finding | Framework | Status | Severity |
|---|---|---|---|
| HIPAA-001: PHI Identification | HIPAA | 🟠 Medium Risk | Medium |
| HIPAA-002: Encryption at Rest | HIPAA | 🔴 High Risk | Critical |
| HIPAA-003: Encryption in Transit | HIPAA | 🟠 Medium Risk | Medium |
| HIPAA-004: Access Controls | HIPAA | 🟢 No Issue Found | — |
| HIPAA-005: Session Management | HIPAA | 🟠 Medium Risk | Medium |
| HIPAA-006: Audit Logging | HIPAA | 🟢 No Issue Found | — |
| HIPAA-007: Minimum Necessary | HIPAA | 🔴 High Risk | High |
| HIPAA-008: BAA Indicators | HIPAA | 🔵 Pattern of Concern | Low |
| HIPAA-009: Data Retention | HIPAA | 🔵 Pattern of Concern | Low |
| HIPAA-010: Breach Detection | HIPAA | 🟠 Medium Risk | Medium |
| SOC2-001: Authentication | SOC2 | 🟢 No Issue Found | — |
| SOC2-002: RBAC | SOC2 | 🟢 No Issue Found | — |
| SOC2-003: Encryption in Transit | SOC2 | 🟠 Medium Risk | Medium |
| SOC2-004: Logging | SOC2 | 🟢 No Issue Found | — |
| SOC2-005: Change Management | SOC2 | 🔵 Pattern of Concern | Low |
| SOC2-006: Incident Response | SOC2 | 🔵 Pattern of Concern | Low |
| SOC2-007: Vendor Risk | SOC2 | 🟠 Medium Risk | Medium |
| SOC2-008: Backup/Recovery | SOC2 | 🔵 Pattern of Concern | Low |
| SOC2-009: MFA | SOC2 | 🟠 Medium Risk | Medium |
| SOC2-010: Security Policy | SOC2 | 🔵 Pattern of Concern | Low |
| GDPR-001: Lawful Basis | GDPR | 🟠 Medium Risk | Medium |
| GDPR-002: Consent Management | GDPR | 🔵 Pattern of Concern | Low |
| GDPR-003: Right to Erasure | GDPR | 🔴 High Risk | Critical |
| GDPR-004: Data Portability | GDPR | 🟠 Medium Risk | Medium |
| GDPR-005: Privacy by Design | GDPR | 🔵 Pattern of Concern | Low |
| GDPR-006: Breach Notification | GDPR | 🔴 High Risk | Critical |
| GDPR-007: Data Retention | GDPR | 🔴 High Risk | Critical |
| GDPR-008: Cross-Border Transfer | GDPR | 🟠 Medium Risk | Medium |
| GDPR-009: DPIA | GDPR | 🔵 Pattern of Concern | Low |
| GDPR-010: Privacy Policy | GDPR | 🔵 Pattern of Concern | Low |

---

## Recommendations

### Critical Priority
1. **Implement field-level encryption** for sensitive database columns (SSN, insurance IDs, financial data) using the existing `CryptoGen` class or a dedicated encryption-at-rest solution.
2. **Build a patient data erasure workflow** that can identify and anonymize or delete personal data across all related tables while respecting medical record retention requirements.
3. **Implement GDPR breach notification capability** with automated breach detection, 72-hour timer tracking, supervisory authority notification templates, and data subject communication workflows.
4. **Establish data retention policies** with configurable per-category retention periods, automated flagging of expiring records, and secure purge mechanisms.

### High Priority
5. **Refactor SELECT * queries** throughout the codebase to request only specific columns needed for each use case, enforcing the minimum necessary principle.
6. **Enforce HTTPS at the application level** with automatic HTTP-to-HTTPS redirects and HSTS headers in the application bootstrap.
7. **Mandate MFA for privileged accounts** by adding a global policy setting that requires MFA enrollment for users with administrative ACL permissions.

### Medium Priority
8. **Reduce default session timeout** to 900 seconds and implement session binding to client fingerprints with session ID regeneration after authentication.
9. **Add automated dependency vulnerability scanning** to the CI/CD pipeline using `composer audit`, `npm audit`, and GitHub Dependabot.
10. **Create GDPR compliance infrastructure** including consent management, lawful basis tracking, privacy notices, and DPIA templates.

---

**DISCLAIMER:** OpenDocket identifies risk patterns through automated code analysis. Findings represent potential areas of concern, not legal determinations. This report does not constitute legal advice. Regulatory compliance requires qualified legal and technical assessment. Consult a licensed attorney and certified compliance professional for definitive compliance determination.
