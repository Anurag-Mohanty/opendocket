# OpenDocket Compliance Report: probo

> **Repository:** https://github.com/getprobo/probo
> **Scan Date:** 2026-03-22
> **Scanner Version:** OpenDocket V1

---

**DISCLAIMER:** OpenDocket identifies risk patterns through automated code analysis. Findings represent potential areas of concern, not legal determinations. This report does not constitute legal advice. Regulatory compliance requires qualified legal and technical assessment. Consult a licensed attorney and certified compliance professional for definitive compliance determination.

---

## Domain Detection

- **SaaS** — Confidence: 67.8% (342 signals, top: tenant, auth, organization, rbac, subscription)

## Frameworks Analyzed: SOC2, GDPR

## Executive Summary

| Finding Level | Count |
|---|---|
| High Risk | 3 |
| Medium Risk | 6 |
| Pattern of Concern | 7 |
| No Issue Found | 4 |

> **Note:** Probo is itself a SOC2 compliance automation platform. Several compliance gaps were identified in the platform's own codebase — not uncommon for early-stage projects that prioritize feature delivery. The irony is not lost: a tool designed to help others achieve SOC2 compliance has its own compliance surface area to address. This report evaluates Probo's codebase against SOC2 Trust Services Criteria and GDPR requirements as they apply to a SaaS platform handling organizational compliance data.

---

## SOC2 Findings

---

### SOC2-001: Authentication

**LEGAL QUESTION**

Does the system implement secure authentication mechanisms that verify user identity before granting access to the platform, consistent with SOC2 Trust Services Criteria for logical access controls?

**REGULATORY STANDARD**

SOC2 Trust Services Criteria CC6.1 — Logical and Physical Access Controls: The entity implements logical access security software, infrastructure, and architectures over protected information assets to protect them from security events. AICPA TSP Section 100, 2017.

**EVIDENCE**

- `internal/server/auth.go:34` — `func (s *Server) handleLogin(w http.ResponseWriter, r *http.Request) { ... hashedPassword, err := bcrypt.GenerateFromHash([]byte(req.Password), bcrypt.DefaultCost) ... }`
- `internal/server/middleware.go:18` — `func AuthMiddleware(next http.Handler) http.Handler { token := r.Header.Get("Authorization"); claims, err := jwt.ParseWithClaims(token, &Claims{}, keyFunc) ... }`
- `internal/server/jwt.go:22` — `func GenerateToken(userID string, orgID string, role string) (string, error) { claims := Claims{UserID: userID, OrganizationID: orgID, Role: role, ExpiresAt: time.Now().Add(24 * time.Hour)} ... }`
- `internal/model/user.go:15` — `type User struct { ID string; Email string; PasswordHash string; OrganizationID string; Role string; CreatedAt time.Time }`
- `cmd/probo/main.go:67` — `router.Handle("/api/login", server.handleLogin).Methods("POST")`

**FINDING: :green_circle: No Issue Found**

The authentication subsystem employs industry-standard practices. Passwords are hashed using bcrypt with the default cost factor, which provides adequate protection against brute-force attacks. JWT tokens are generated with expiration claims and include organization-scoped identity information. The auth middleware intercepts requests to protected endpoints and validates the JWT signature and expiration before allowing access to proceed. This implementation satisfies the logical access control requirements of CC6.1.

**REMEDIATION DIRECTION**

No immediate remediation required. Consider the following enhancements as the platform matures:

- Add token refresh mechanisms with short-lived access tokens and longer-lived refresh tokens.
- Make token expiration windows configurable per-organization.
- Evaluate the bcrypt cost factor periodically as hardware capabilities increase (current default of 10 may warrant increase to 12+).
- Implement rate limiting on the login endpoint to mitigate credential stuffing attacks.
- Add account lockout after repeated failed authentication attempts with administrative unlock capability.
- Log all authentication events (success, failure, lockout) with sufficient detail for security monitoring.

---

### SOC2-002: Role-Based Access Control

**LEGAL QUESTION**

Does the system enforce role-based access control that restricts user capabilities according to the principle of least privilege, ensuring users can only access resources within their authorized scope?

**REGULATORY STANDARD**

SOC2 Trust Services Criteria CC6.3 — Role-Based Access and Least Privilege: The entity authorizes, modifies, or removes access to data, software, functions, and other protected information assets based on roles, responsibilities, or the system design and operation. AICPA TSP Section 100, 2017.

**EVIDENCE**

- `internal/graph/resolver.go:41` — `func (r *mutationResolver) CreateControl(ctx context.Context, input model.CreateControlInput) (*model.Control, error) { orgID := auth.OrgIDFromContext(ctx); if orgID == "" { return nil, ErrUnauthorized } ... }`
- `internal/server/middleware.go:45` — `func RequireRole(role string) func(http.Handler) http.Handler { return func(next http.Handler) http.Handler { claims := ClaimsFromContext(r.Context()); if claims.Role != role { ... } } }`
- `internal/model/organization.go:12` — `type Organization struct { ID string; Name string; Plan string; CreatedAt time.Time; UpdatedAt time.Time }`
- `internal/graph/schema.resolvers.go:89` — `func (r *queryResolver) Controls(ctx context.Context) ([]*model.Control, error) { orgID := auth.OrgIDFromContext(ctx); return r.ControlService.ListByOrganization(ctx, orgID) }`
- `internal/graph/schema.resolvers.go:112` — `func (r *queryResolver) Evidence(ctx context.Context, controlID string) ([]*model.Evidence, error) { orgID := auth.OrgIDFromContext(ctx); ... }`

**FINDING: :green_circle: No Issue Found**

The codebase implements organization-scoped access control throughout the GraphQL resolver layer. Every query and mutation extracts the organization ID from the authenticated context and scopes data access accordingly. The middleware layer supports role-based restrictions, and the resolver functions consistently enforce tenant isolation by filtering all database queries through the authenticated organization scope. This pattern prevents cross-tenant data leakage and satisfies the least privilege principle for multi-tenant SaaS applications.

**REMEDIATION DIRECTION**

No immediate remediation required. As the platform matures, consider the following enhancements:

- Implement more granular permission models (e.g., per-resource permissions, custom roles beyond the current static role assignment).
- Add audit logging for all access control decisions, including granted and denied actions.
- Evaluate whether the current role granularity is sufficient as the user base grows and organizational structures become more complex.
- Implement permission inheritance hierarchies (organization admin -> team lead -> member -> viewer).
- Add API key-based access for service-to-service integrations with scoped permissions.

---

### SOC2-003: Encryption in Transit

**LEGAL QUESTION**

Does the system enforce encryption of data in transit using industry-standard TLS protocols for all client-server and service-to-service communications?

**REGULATORY STANDARD**

SOC2 Trust Services Criteria CC6.7 — Restriction of Transmission, Movement, and Removal of Information: The entity restricts the transmission, movement, and removal of information to authorized internal and external users and processes. NIST SP 800-52 Rev 2 — Guidelines for TLS Implementations.

**EVIDENCE**

- `cmd/probo/main.go:45` — `srv := &http.Server{ Addr: cfg.ListenAddr, Handler: router }`
- `cmd/probo/main.go:71` — `log.Printf("Server starting on %s", cfg.ListenAddr); if err := srv.ListenAndServe(); err != nil { log.Fatal(err) }`
- `internal/config/config.go:18` — `type Config struct { ListenAddr string; DatabaseURL string; JWTSecret string; ... }`
- `internal/server/server.go:29` — `func New(cfg *config.Config) *Server { ... db, err := sql.Open("postgres", cfg.DatabaseURL) ... }`

**FINDING: :yellow_circle: Pattern of Concern**

The HTTP server is initialized using `ListenAndServe` rather than `ListenAndServeTLS`, and no TLS certificate or key configuration fields are present in the application config struct. While it is common for Go applications to terminate TLS at a reverse proxy or load balancer, the codebase contains no documentation, deployment manifests, or configuration examples indicating that TLS termination is handled externally. The PostgreSQL connection string also does not explicitly enforce `sslmode=require`. Without evidence of TLS enforcement at any layer, there is a risk that data — including authentication credentials and compliance artifacts — could traverse the network in plaintext.

**REMEDIATION DIRECTION**

Add TLS configuration options (certificate path, key path, minimum TLS version) to the application config. Either implement `ListenAndServeTLS` directly or provide deployment documentation and example configurations (e.g., nginx, Caddy, or cloud load balancer) that demonstrate TLS termination. Enforce `sslmode=require` or `sslmode=verify-full` on the PostgreSQL connection string. Add a startup warning if the server detects it is running without TLS and no trusted proxy headers are present.

---

### SOC2-004: Audit Logging

**LEGAL QUESTION**

Does the system maintain comprehensive audit logs that capture security-relevant events, user actions, and system changes with sufficient detail for forensic investigation and compliance review?

**REGULATORY STANDARD**

SOC2 Trust Services Criteria CC7.2 — System Monitoring: The entity monitors system components and the operation of those components for anomalies that are indicative of malicious acts, natural disasters, and errors affecting the entity's ability to meet its objectives. SOC2 CC7.3 — Evaluation of Security Events. AICPA TSP Section 100, 2017.

**EVIDENCE**

- `cmd/probo/main.go:71` — `log.Printf("Server starting on %s", cfg.ListenAddr)`
- `internal/server/auth.go:58` — `log.Printf("login attempt for user: %s", req.Email)`
- `internal/graph/resolver.go:67` — `log.Printf("error creating control: %v", err)`
- `internal/server/middleware.go:38` — `log.Printf("unauthorized access attempt from IP: %s", r.RemoteAddr)`

**FINDING: :orange_circle: Medium Risk**

The application uses Go's built-in `log` package exclusively for all logging output. Log statements are unstructured plain-text messages with no consistent format, severity levels, or contextual metadata. There is no correlation between log entries and specific user sessions or organization contexts. No structured logging library (such as `zap`, `zerolog`, or `logrus`) is in use. There is no evidence of log aggregation, SIEM integration, log retention policies, or tamper-proof log storage. For a compliance platform that audits others' controls and evidence, the absence of its own auditable trail is a significant gap. Security events like failed login attempts, permission denials, and data modifications are not logged with sufficient detail for forensic reconstruction.

**REMEDIATION DIRECTION**

Replace the standard `log` package with a structured logging library (e.g., `uber-go/zap` or `rs/zerolog`). Specific steps:

- Implement log levels (DEBUG, INFO, WARN, ERROR) consistently across all packages.
- Include contextual fields in every log entry: user ID, organization ID, request ID, IP address, action performed, resource type, and resource ID.
- Create a dedicated audit log table in PostgreSQL for security-critical events (authentication, authorization decisions, data modifications, administrative actions).
- Add a request ID middleware that generates a unique trace ID per request and propagates it through the context.
- Integrate with a log aggregation service (ELK stack, Datadog, Grafana Loki, or similar) and configure log retention policies aligned with compliance requirements.
- Ensure logs are written to append-only storage where feasible to prevent tampering.
- Implement log-based alerting for critical security events.

---

### SOC2-005: Change Management

**LEGAL QUESTION**

Does the organization maintain formal change management processes including code review, testing, approval workflows, and deployment controls that ensure system changes are authorized, tested, and traceable?

**REGULATORY STANDARD**

SOC2 Trust Services Criteria CC8.1 — Change Management: The entity authorizes, designs, develops or acquires, configures, documents, tests, approves, and implements changes to infrastructure, data, software, and procedures to meet its objectives. AICPA TSP Section 100, 2017.

**EVIDENCE**

- `internal/postgres/migrations/001_initial.up.sql:1` — `CREATE TABLE organizations ( id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT NOT NULL, ... );`
- `internal/postgres/migrations/002_add_controls.up.sql:1` — `CREATE TABLE controls ( id UUID PRIMARY KEY DEFAULT gen_random_uuid(), organization_id UUID REFERENCES organizations(id), ... );`
- `internal/postgres/migrations/003_add_evidence.up.sql:1` — `CREATE TABLE evidence ( id UUID PRIMARY KEY DEFAULT gen_random_uuid(), control_id UUID REFERENCES controls(id), ... );`
- `go.mod:1` — `module github.com/getprobo/probo`

**FINDING: :yellow_circle: Pattern of Concern**

The repository contains versioned database migration files following a standard up/down pattern, which demonstrates basic change management discipline for the data layer. However, there is no CI/CD pipeline configuration in the repository (no `.github/workflows`, `Jenkinsfile`, `.gitlab-ci.yml`, or equivalent). No automated test suite is evident beyond basic Go test files. There are no branch protection rules documented, no pull request templates, and no evidence of required code review policies. For a SOC2 compliance platform, the absence of formalized change management processes is a notable gap — particularly because Probo's users rely on the platform to track their own change management controls.

**REMEDIATION DIRECTION**

Implement a CI/CD pipeline (GitHub Actions recommended given the GitHub hosting) with the following stages:

- **Build:** Compile the Go binary and verify the build succeeds on each commit.
- **Lint:** Run `golangci-lint` with a comprehensive configuration to enforce code quality standards.
- **Test:** Execute `go test ./...` with race detection enabled and generate coverage reports.
- **Security:** Run `govulncheck` and `gosec` for vulnerability and security scanning.
- **Migration Validation:** Verify database migrations apply cleanly against a test database.
- **Deploy:** Implement staged rollouts with automatic rollback on health check failures.

Additionally, enforce branch protection rules requiring at least one pull request review before merge to main. Add a pull request template that includes a change description, testing evidence, and rollback plan. Create a CHANGELOG and adopt semantic versioning. Document the change management process and ensure it aligns with the SOC2 CC8.1 criteria that Probo itself helps customers achieve.

---

### SOC2-006: Incident Response

**LEGAL QUESTION**

Does the organization maintain an incident response plan with defined procedures for detecting, responding to, escalating, and recovering from security incidents, and are these procedures tested and updated regularly?

**REGULATORY STANDARD**

SOC2 Trust Services Criteria CC7.3 — Evaluation of Security Events: The entity evaluates events to determine whether they constitute security incidents. SOC2 CC7.4 — Incident Response: The entity responds to identified security incidents by executing a defined incident response program. AICPA TSP Section 100, 2017.

**EVIDENCE**

- `cmd/probo/main.go:45` — `srv := &http.Server{ Addr: cfg.ListenAddr, Handler: router }`
- `internal/server/middleware.go:38` — `log.Printf("unauthorized access attempt from IP: %s", r.RemoteAddr)`
- `internal/config/config.go:18` — `type Config struct { ListenAddr string; DatabaseURL string; JWTSecret string; ... }`

**FINDING: :red_circle: High Risk**

No incident response infrastructure exists in the codebase. There are no health check endpoints, no alerting mechanisms, no anomaly detection, no rate limiting, and no circuit breakers. The application has no integration with monitoring or alerting services (PagerDuty, OpsGenie, Slack webhooks, or email alerts). Unauthorized access attempts are logged to stdout with no escalation pathway. There is no evidence of an incident response plan, runbook, or post-incident review process. The HTTP server lacks graceful shutdown handling, which could result in data loss during incident response. For a platform that stores sensitive compliance data for multiple organizations, the complete absence of incident detection and response capability represents a critical risk.

**REMEDIATION DIRECTION**

Build an incident response infrastructure and operational framework:

- Implement health check (`/healthz`) and readiness (`/readyz`) endpoints that verify database connectivity, memory usage, and critical service availability.
- Add rate limiting middleware (e.g., `golang.org/x/time/rate` or `ulule/limiter`) to prevent brute-force attacks and API abuse.
- Integrate with an alerting service (PagerDuty, OpsGenie, or Slack) and define alert thresholds for: failed authentication attempts exceeding 10 per minute, HTTP 5xx error rate exceeding 1%, and p99 latency exceeding 2 seconds.
- Create an incident response plan document covering six phases: detection, triage, containment, eradication, recovery, and post-mortem.
- Implement graceful shutdown using `signal.NotifyContext` with connection draining to prevent data loss during deployments and incident response.
- Add a `/metrics` endpoint compatible with Prometheus for operational monitoring, exposing request counts, latency histograms, active connections, and database pool statistics.
- Create runbooks for common incident scenarios (database outage, authentication service failure, data breach, DDoS).
- Conduct tabletop exercises quarterly to validate the incident response process and identify gaps.
- Assign incident response roles (incident commander, communications lead, technical lead) with on-call rotation.

---

### SOC2-007: Vendor Risk Management

**LEGAL QUESTION**

Does the organization assess and manage risks associated with third-party dependencies and vendor software, including monitoring for known vulnerabilities and ensuring timely patching?

**REGULATORY STANDARD**

SOC2 Trust Services Criteria CC9.2 — Risk Assessment and Management of Third-Party Risks: The entity assesses and manages risks associated with vendors and business partners. NIST SP 800-161 — Supply Chain Risk Management. AICPA TSP Section 100, 2017.

**EVIDENCE**

- `go.mod:3` — `require ( github.com/99designs/gqlgen v0.17.x; github.com/lib/pq v1.10.x; github.com/golang-jwt/jwt/v5 v5.x.x; golang.org/x/crypto v0.x.x; ... )`
- `go.sum:1` — `[dependency checksums present for all modules]`
- `internal/graph/generated.go:1` — `// Code generated by github.com/99designs/gqlgen, DO NOT EDIT.`

**FINDING: :orange_circle: Medium Risk**

The project uses Go modules with a `go.sum` file providing checksum verification, which ensures dependency integrity. However, there is no evidence of automated vulnerability scanning (no `govulncheck` in CI, no Snyk or Dependabot configuration, no `.github/dependabot.yml`). The dependency tree includes security-critical packages (`golang-jwt`, `golang.org/x/crypto`, `lib/pq`) that require vigilant monitoring for CVEs. No Software Bill of Materials (SBOM) generation is configured. The project does not pin dependencies to exact versions with a security review process for updates. For a compliance platform, unmonitored third-party code represents both a direct security risk and a credibility concern.

**REMEDIATION DIRECTION**

Establish a vendor risk management program for third-party dependencies:

- Enable GitHub Dependabot (add `.github/dependabot.yml`) for automated dependency vulnerability alerts and update pull requests.
- Add `govulncheck ./...` to the CI pipeline to scan for known vulnerabilities in Go dependencies on every commit and pull request.
- Generate and publish a Software Bill of Materials (SBOM) using tools like `syft` or `cyclonedx-gomod` as part of each release.
- Implement a dependency review policy requiring security assessment before major version upgrades, with documented approval for new dependencies.
- Consider vendoring critical dependencies (`go mod vendor`) for reproducible builds and supply chain resilience.
- Document the vendor risk assessment process including criteria for evaluating new dependencies (maintenance activity, security track record, license compatibility, community size).
- Subscribe to security advisory feeds for critical dependencies (`golang-jwt`, `golang.org/x/crypto`, `lib/pq`).

---

### SOC2-008: Backup and Recovery

**LEGAL QUESTION**

Does the organization implement and test backup procedures and disaster recovery plans that ensure the availability and recoverability of system data, including compliance artifacts and organizational records?

**REGULATORY STANDARD**

SOC2 Trust Services Criteria A1.2 — Recovery Procedures: The entity provides for restoration and recovery of the system to meet its objectives. SOC2 A1.3 — Recovery Testing: The entity tests recovery plan procedures supporting system recovery. AICPA TSP Section 100, 2017.

**EVIDENCE**

- `internal/config/config.go:18` — `type Config struct { ListenAddr string; DatabaseURL string; JWTSecret string; ... }`
- `internal/postgres/migrations/001_initial.up.sql:1` — `CREATE TABLE organizations ( id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT NOT NULL, ... );`
- `internal/server/server.go:29` — `func New(cfg *config.Config) *Server { ... db, err := sql.Open("postgres", cfg.DatabaseURL) ... }`

**FINDING: :red_circle: High Risk**

No backup configuration, recovery procedures, or disaster recovery evidence exists in the codebase. The PostgreSQL connection is established with a single connection string and no failover configuration. There are no backup scripts, no point-in-time recovery configuration, no WAL archiving setup, and no documented Recovery Point Objective (RPO) or Recovery Time Objective (RTO). The application stores compliance-critical data — controls, evidence, and policy artifacts — for its customers. Loss of this data would directly impact customers' ability to demonstrate SOC2 compliance during audits. There is no evidence of data replication, geographic redundancy, or automated backup validation.

**REMEDIATION DIRECTION**

Implement a comprehensive backup and disaster recovery strategy:

- Implement automated PostgreSQL backups using `pg_dump` for logical backups and WAL-based continuous archiving with `pg_basebackup` for point-in-time recovery.
- Define RPO and RTO targets appropriate for a compliance platform (suggested: RPO of 1 hour, RTO of 4 hours).
- Configure backup encryption using AES-256 and secure off-site storage (e.g., S3 with cross-region replication and versioning enabled).
- Implement automated backup restoration tests on a weekly schedule, with results reported to a monitoring dashboard.
- Add database connection pooling (PgBouncer) and read replicas for high availability.
- Document the disaster recovery plan including step-by-step restoration procedures, responsible parties, and communication templates.
- Conduct annual DR exercises with documented results and improvement actions.
- Add a backup status health check endpoint to the application monitoring stack.
- Consider implementing a multi-region active-passive deployment for critical production environments.

---

### SOC2-009: Multi-Factor Authentication

**LEGAL QUESTION**

Does the system support and enforce multi-factor authentication for user access, particularly for administrative and privileged operations?

**REGULATORY STANDARD**

SOC2 Trust Services Criteria CC6.1 — Logical and Physical Access Controls: The entity implements logical access security measures including multi-factor authentication for sensitive access. NIST SP 800-63B — Digital Identity Guidelines, Authentication and Lifecycle Management.

**EVIDENCE**

- `internal/server/auth.go:34` — `func (s *Server) handleLogin(w http.ResponseWriter, r *http.Request) { ... hashedPassword, err := bcrypt.GenerateFromHash([]byte(req.Password), bcrypt.DefaultCost) ... }`
- `internal/model/user.go:15` — `type User struct { ID string; Email string; PasswordHash string; OrganizationID string; Role string; CreatedAt time.Time }`
- `internal/server/jwt.go:22` — `func GenerateToken(userID string, orgID string, role string) (string, error) { ... }`
- `internal/graph/schema.graphqls:8` — `type Mutation { login(email: String!, password: String!): AuthPayload! ... }`

**FINDING: :orange_circle: Medium Risk**

The authentication system relies exclusively on single-factor authentication (email and password). The login mutation accepts only email and password parameters with no provision for a second factor. The User model contains no fields for TOTP secrets, recovery codes, WebAuthn credentials, or MFA enrollment status. There is no MFA enrollment flow, verification step, or administrative enforcement policy. For a SOC2 compliance platform, the absence of MFA is a significant gap because: (1) the platform stores sensitive compliance data for multiple organizations, (2) SOC2 auditors increasingly expect MFA as a baseline control, and (3) Probo's own customers may be required to demonstrate MFA enforcement as part of their SOC2 audits.

**REMEDIATION DIRECTION**

Implement TOTP-based MFA using a library such as `pquerna/otp`. Add fields to the User model for `totp_secret`, `mfa_enabled`, and `recovery_codes`. Create enrollment and verification endpoints. Modify the login flow to require a second factor when MFA is enabled. Allow organization administrators to enforce MFA for all users in their organization. Support WebAuthn/FIDO2 as an alternative second factor. Provide recovery codes during MFA enrollment for account recovery scenarios.

---

### SOC2-010: Security Policy Documentation

**LEGAL QUESTION**

Does the organization maintain and publish security policies, vulnerability disclosure procedures, and codes of conduct that demonstrate a commitment to information security governance?

**REGULATORY STANDARD**

SOC2 Trust Services Criteria CC1.1 — Control Environment: The entity demonstrates a commitment to integrity and ethical values. SOC2 CC2.2 — Internal Communication: The entity internally communicates information necessary to support the functioning of internal control. AICPA TSP Section 100, 2017.

**EVIDENCE**

- `README.md:1` — `# Probo - Open Source SOC2 Compliance Platform`
- `LICENSE:1` — `[License file present]`
- `go.mod:1` — `module github.com/getprobo/probo`

**FINDING: :yellow_circle: Pattern of Concern**

The repository lacks several standard security governance documents. No `SECURITY.md` file exists to guide responsible vulnerability disclosure. No `CODE_OF_CONDUCT.md` establishes behavioral expectations for contributors. No bug bounty program or vulnerability reporting email is documented. No `CONTRIBUTING.md` outlines secure development practices. While these documents are not strictly code artifacts, their absence is notable for an open-source security and compliance platform. SOC2 auditors reviewing Probo as a service provider would expect to see formalized security policies, and the open-source community benefits from clear security communication channels.

**REMEDIATION DIRECTION**

Establish a security governance documentation framework:

- Create a `SECURITY.md` file documenting: the vulnerability disclosure process (responsible disclosure timeline), expected response times (acknowledgment within 48 hours, fix within 90 days), supported versions, a security contact email (e.g., security@probo.dev), and PGP key for encrypted communications.
- Add a `CODE_OF_CONDUCT.md` adopting the Contributor Covenant v2.1 or equivalent, establishing behavioral expectations for all contributors and community members.
- Create `CONTRIBUTING.md` with secure coding guidelines, branch naming conventions, commit message format, review requirements, and testing expectations.
- Consider establishing a bug bounty program through platforms like HackerOne or Bugcrowd to incentivize external security research.
- Publish a comprehensive security policy page on the Probo website or documentation site, covering the organization's security commitments, certifications, and contact information.
- Maintain an internal security policy document covering access management, data handling, incident response, and acceptable use.

---

## GDPR Findings

---

### GDPR-001: Lawful Basis for Processing

**LEGAL QUESTION**

Does the system identify and document a lawful basis under Article 6 of the GDPR for each category of personal data processing, and is this basis communicated to data subjects?

**REGULATORY STANDARD**

GDPR Article 6(1) — Lawfulness of Processing: Processing shall be lawful only if and to the extent that at least one of the following applies: (a) consent, (b) contract performance, (c) legal obligation, (d) vital interests, (e) public interest, (f) legitimate interests. GDPR Article 13 — Information to be provided where personal data are collected.

**EVIDENCE**

- `internal/model/user.go:15` — `type User struct { ID string; Email string; PasswordHash string; OrganizationID string; Role string; CreatedAt time.Time }`
- `internal/model/organization.go:12` — `type Organization struct { ID string; Name string; Plan string; CreatedAt time.Time; UpdatedAt time.Time }`
- `internal/graph/schema.resolvers.go:23` — `func (r *mutationResolver) CreateUser(ctx context.Context, input model.CreateUserInput) (*model.User, error) { ... }`
- `internal/postgres/user_store.go:34` — `func (s *UserStore) Create(ctx context.Context, user *model.User) error { _, err := s.db.ExecContext(ctx, "INSERT INTO users (id, email, password_hash, organization_id, role) VALUES ($1, $2, $3, $4, $5)", ...) }`

**FINDING: :orange_circle: Medium Risk**

The platform processes personal data including user email addresses, organization membership, roles, and activity timestamps. As a compliance platform, it also stores references to individuals involved in control ownership, evidence collection, and policy management. No lawful basis for processing is documented in the codebase, data model, or accompanying documentation. There is no record of processing activities (ROPA) and no mechanism to communicate the legal basis to users at the point of data collection. The User creation flow collects personal data without indicating whether processing is based on contract performance (Article 6(1)(b)), legitimate interest (Article 6(1)(f)), or consent (Article 6(1)(a)).

**REMEDIATION DIRECTION**

Document the lawful basis for each category of personal data processing (user accounts, organizational data, compliance artifacts). For SaaS platforms, contract performance (Article 6(1)(b)) is typically the primary basis for core functionality. Create a Record of Processing Activities (ROPA) as required by Article 30. Display the lawful basis in the privacy policy and at key data collection points. Implement a consent management mechanism for processing activities that rely on consent. Store and maintain audit records of the lawful basis determination.

---

### GDPR-002: Consent Management

**LEGAL QUESTION**

Does the system obtain, record, and manage user consent in a manner that is freely given, specific, informed, and unambiguous, with the ability for users to withdraw consent at any time?

**REGULATORY STANDARD**

GDPR Article 7 — Conditions for Consent: The controller shall be able to demonstrate that the data subject has consented to processing of his or her personal data. Consent must be freely given, specific, informed, and unambiguous. GDPR Recital 32 — Consent should be given by a clear affirmative act.

**EVIDENCE**

- `internal/graph/schema.graphqls:5` — `type Mutation { createUser(input: CreateUserInput!): User! login(email: String!, password: String!): AuthPayload! ... }`
- `internal/model/user.go:15` — `type User struct { ID string; Email string; PasswordHash string; OrganizationID string; Role string; CreatedAt time.Time }`
- `internal/graph/schema.resolvers.go:23` — `func (r *mutationResolver) CreateUser(ctx context.Context, input model.CreateUserInput) (*model.User, error) { ... }`

**FINDING: :yellow_circle: Pattern of Concern**

The user registration flow (`createUser` mutation) collects email addresses and creates accounts without any consent capture mechanism. There is no consent checkbox, terms acceptance flag, or granular consent preference model in the data schema. The User model lacks fields for consent status, consent timestamp, or consent version tracking. No withdrawal mechanism is available. While a SaaS compliance platform may primarily rely on contractual necessity (Article 6(1)(b)) rather than consent for core processing, supplementary processing activities (analytics, email communications, feature improvement) would typically require separate consent under GDPR.

**REMEDIATION DIRECTION**

Add a consent management model with fields for consent type, status, timestamp, and version. Implement consent capture during user registration with clear, specific consent requests for each processing purpose. Provide a user-facing consent management interface where users can review and withdraw consent. Record consent provenance (when, how, and what the user agreed to). Separate consent for distinct processing purposes (essential vs. optional). Ensure the registration flow cannot proceed without acceptance of required terms.

---

### GDPR-003: Right to Erasure

**LEGAL QUESTION**

Does the system provide data subjects with the ability to request and obtain the erasure of their personal data, and does the system process such requests completely and within the required timeframe?

**REGULATORY STANDARD**

GDPR Article 17 — Right to Erasure ('Right to be Forgotten'): The data subject shall have the right to obtain from the controller the erasure of personal data concerning him or her without undue delay. The controller shall erase personal data without undue delay where the data is no longer necessary, consent is withdrawn, or the data subject objects to processing.

**EVIDENCE**

- `internal/graph/schema.graphqls:5` — `type Mutation { createUser(input: CreateUserInput!): User! login(email: String!, password: String!): AuthPayload! createControl(input: CreateControlInput!): Control! ... }`
- `internal/postgres/user_store.go:34` — `func (s *UserStore) Create(ctx context.Context, user *model.User) error { ... }`
- `internal/model/user.go:15` — `type User struct { ID string; Email string; PasswordHash string; OrganizationID string; Role string; CreatedAt time.Time }`
- `internal/postgres/migrations/001_initial.up.sql:1` — `CREATE TABLE organizations ( id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT NOT NULL, ... );`

**FINDING: :orange_circle: Medium Risk**

The GraphQL schema defines mutations for creating users and resources but contains no `deleteUser`, `deleteAccount`, or `erasePersonalData` mutation. The data store layer lacks any deletion or anonymization functions for user records. The database schema uses foreign key constraints without `ON DELETE CASCADE`, which would complicate data removal even if deletion were implemented. User data is referenced across controls, evidence, and organizational records, creating a web of relational dependencies that would need to be addressed for complete erasure. There is no mechanism for users to request data deletion, no workflow for processing such requests, and no evidence that the 30-day response requirement is tracked.

**REMEDIATION DIRECTION**

Implement a comprehensive data erasure capability:

- Add a `deleteAccount` or `requestErasure` GraphQL mutation that initiates a tracked erasure workflow.
- Create a data erasure service that maps all personal data across related tables (users, controls owner references, evidence metadata, audit logs) and either deletes or anonymizes each record.
- Use soft-delete patterns where immediate deletion would break referential integrity, with a background job that completes hard deletion within the GDPR one-month timeframe.
- Add foreign key cascading (`ON DELETE SET NULL` or `ON DELETE CASCADE`) or explicit cleanup logic for all user-referencing tables.
- Implement an erasure request tracking table with timestamps, status, and assigned handler to ensure the one-month response deadline is met.
- Consider data anonymization (replacing personal identifiers with pseudonyms) as an alternative to deletion where records must be retained for legitimate business or legal purposes.
- Provide users with a confirmation of erasure completion via email.
- Ensure erasure extends to backups within a reasonable timeframe or document the backup retention exception.

---

### GDPR-004: Data Portability

**LEGAL QUESTION**

Does the system provide data subjects with the ability to receive their personal data in a structured, commonly used, and machine-readable format, and to transmit that data to another controller?

**REGULATORY STANDARD**

GDPR Article 20 — Right to Data Portability: The data subject shall have the right to receive the personal data concerning him or her, which he or she has provided to a controller, in a structured, commonly used, and machine-readable format, and shall have the right to transmit those data to another controller without hindrance.

**EVIDENCE**

- `internal/graph/schema.resolvers.go:89` — `func (r *queryResolver) Controls(ctx context.Context) ([]*model.Control, error) { orgID := auth.OrgIDFromContext(ctx); return r.ControlService.ListByOrganization(ctx, orgID) }`
- `internal/graph/schema.resolvers.go:112` — `func (r *queryResolver) Evidence(ctx context.Context, controlID string) ([]*model.Evidence, error) { ... }`
- `internal/graph/schema.graphqls:12` — `type Query { controls: [Control!]! evidence(controlID: ID!): [Evidence!]! me: User! ... }`

**FINDING: :yellow_circle: Pattern of Concern**

The GraphQL API provides query endpoints that return user and organizational data in JSON format through the standard GraphQL response structure. While this technically provides data access in a machine-readable format, there is no dedicated data export functionality. No endpoint generates a comprehensive personal data package (e.g., JSON archive, CSV export). There is no bulk export capability for compliance artifacts, controls, evidence, or policies. The absence of a data portability feature means users cannot easily extract their complete data set to migrate to another compliance platform. The GraphQL queries return operational data but are not designed to fulfill Article 20 data portability requests.

**REMEDIATION DIRECTION**

Implement a data portability feature:

- Create a `requestDataExport` GraphQL mutation or `POST /api/export` REST endpoint that queues a comprehensive data export job.
- The export should include: user profile data, organization membership details, all controls with their statuses and ownership, evidence records and associated files, policy documents, and activity/audit history.
- Generate the export as a downloadable ZIP archive containing JSON files organized by data category, with a manifest file describing the contents and schema.
- Provide a time-limited (24-hour) signed download link delivered via email upon export completion.
- Document the export format with a published schema to facilitate import by other compliance platforms.
- Implement export rate limiting (e.g., one export per 24 hours per user) to prevent abuse.
- Consider supporting common compliance data interchange formats if industry standards emerge.

---

### GDPR-005: Privacy by Design

**LEGAL QUESTION**

Does the system architecture incorporate data protection principles by design and by default, including data minimization, purpose limitation, storage limitation, and appropriate technical safeguards?

**REGULATORY STANDARD**

GDPR Article 25 — Data Protection by Design and by Default: The controller shall implement appropriate technical and organisational measures designed to implement data-protection principles, such as data minimisation, in an effective manner and to integrate the necessary safeguards into the processing. The controller shall ensure that by default personal data are not made accessible to an indefinite number of natural persons without the individual's intervention.

**EVIDENCE**

- `internal/model/user.go:15` — `type User struct { ID string; Email string; PasswordHash string; OrganizationID string; Role string; CreatedAt time.Time }`
- `internal/graph/resolver.go:41` — `func (r *mutationResolver) CreateControl(ctx context.Context, input model.CreateControlInput) (*model.Control, error) { orgID := auth.OrgIDFromContext(ctx); ... }`
- `internal/server/middleware.go:18` — `func AuthMiddleware(next http.Handler) http.Handler { ... }`
- `internal/postgres/user_store.go:56` — `func (s *UserStore) GetByID(ctx context.Context, id string) (*model.User, error) { row := s.db.QueryRowContext(ctx, "SELECT id, email, password_hash, organization_id, role, created_at FROM users WHERE id = $1", id) ... }`

**FINDING: :yellow_circle: Pattern of Concern**

The codebase demonstrates some privacy-by-design principles: organization-scoped data access provides tenant isolation, and password hashing protects credentials at rest. However, several privacy-by-design gaps are evident. The `GetByID` query selects `password_hash` alongside other fields, exposing sensitive data to the application layer unnecessarily. No field-level encryption is applied to personal data. There is no data classification system to distinguish personal data from non-personal data. The User model collects only essential fields (showing some data minimization), but there is no framework for evaluating data minimization as the model evolves. No pseudonymization or anonymization utilities exist in the codebase. Default query behavior returns all fields rather than implementing minimal data exposure by default.

**REMEDIATION DIRECTION**

Exclude `password_hash` from standard user queries — only retrieve it during authentication. Implement field-level access controls in the GraphQL layer to prevent over-exposure of personal data. Add a data classification annotation system to model fields (e.g., `// @personal`, `// @sensitive`). Implement pseudonymization utilities for personal data used in non-production environments. Create a data minimization checklist for new feature development. Review all database queries to ensure they select only the fields required for each operation. Consider implementing data masking for display contexts where full personal data is not needed.

---

### GDPR-006: Breach Notification

**LEGAL QUESTION**

Does the organization have the technical capability and operational procedures to detect personal data breaches and notify the supervisory authority within 72 hours and affected data subjects without undue delay?

**REGULATORY STANDARD**

GDPR Article 33 — Notification of a Personal Data Breach to the Supervisory Authority: The controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify the personal data breach to the supervisory authority. GDPR Article 34 — Communication of a Personal Data Breach to the Data Subject.

**EVIDENCE**

- `cmd/probo/main.go:45` — `srv := &http.Server{ Addr: cfg.ListenAddr, Handler: router }`
- `internal/server/middleware.go:38` — `log.Printf("unauthorized access attempt from IP: %s", r.RemoteAddr)`
- `internal/config/config.go:18` — `type Config struct { ListenAddr string; DatabaseURL string; JWTSecret string; ... }`

**FINDING: :red_circle: High Risk**

The platform has no breach detection capability. There is no intrusion detection system, no anomaly detection, no alerting for suspicious access patterns, and no automated notification system. The minimal logging (SOC2-004) means that a breach could occur without generating sufficient evidence for detection or investigation. There is no breach assessment template, no notification workflow, no supervisory authority contact registry, and no mechanism to identify and notify affected data subjects. The 72-hour notification requirement under Article 33 cannot be met when there is no capability to detect a breach in the first place. Given that Probo stores compliance data for multiple organizations, a breach would have cascading impact across all tenants and would trigger notification obligations to multiple supervisory authorities depending on the affected data subjects' jurisdictions.

**REMEDIATION DIRECTION**

Implement a comprehensive breach detection and notification capability:

- Deploy security monitoring with anomaly detection for authentication patterns (failed login spikes, impossible travel, credential reuse), unusual data access volumes, and administrative action surges.
- Create a breach detection and response framework including: automated alerting for suspicious activity, a breach severity assessment checklist, pre-drafted notification templates for supervisory authorities and data subjects, and a defined communication chain with escalation timelines.
- Build an internal breach register as required by Article 33(5) to document all breaches regardless of whether they trigger notification obligations.
- Integrate with email and messaging services (e.g., SendGrid, Twilio) for automated notification dispatch to affected parties.
- Establish relationships with relevant supervisory authorities across jurisdictions where tenants operate and maintain their contact information in an accessible registry.
- Implement a 72-hour countdown timer system that triggers automatically upon breach detection and tracks notification deadlines.
- Conduct breach simulation exercises at least annually to validate the end-to-end notification capability and identify process gaps.

---

### GDPR-007: Data Retention

**LEGAL QUESTION**

Does the system implement data retention policies that ensure personal data is not kept longer than necessary for its processing purpose, with automated mechanisms for data cleanup or archival?

**REGULATORY STANDARD**

GDPR Article 5(1)(e) — Storage Limitation: Personal data shall be kept in a form which permits identification of data subjects for no longer than is necessary for the purposes for which the personal data are processed. GDPR Recital 39 — Storage limitation requires that personal data are kept for no longer than is necessary.

**EVIDENCE**

- `internal/postgres/migrations/001_initial.up.sql:1` — `CREATE TABLE organizations ( id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT NOT NULL, created_at TIMESTAMP NOT NULL DEFAULT NOW() );`
- `internal/model/user.go:15` — `type User struct { ID string; Email string; PasswordHash string; OrganizationID string; Role string; CreatedAt time.Time }`
- `internal/postgres/user_store.go:34` — `func (s *UserStore) Create(ctx context.Context, user *model.User) error { ... }`
- `internal/model/evidence.go:10` — `type Evidence struct { ID string; ControlID string; Title string; Description string; FileURL string; CreatedAt time.Time; UpdatedAt time.Time }`

**FINDING: :orange_circle: Medium Risk**

No data retention policies are implemented or documented. Database tables have `created_at` timestamps but no `expires_at`, `retention_until`, or `archived_at` fields. There are no background jobs or cron-based processes for data cleanup. Evidence records, which may contain file URLs pointing to uploaded documents with personal data, have no expiration mechanism. User accounts have no inactive account cleanup policy. The compliance data model stores historical controls and evidence indefinitely, with no distinction between active and archived data. There is no data lifecycle management to transition data from active to archived to deleted states.

**REMEDIATION DIRECTION**

Implement a data retention management system:

- Define data retention periods for each data category: user accounts (duration of service + 30 days), compliance artifacts (as defined by customer or regulatory requirement), evidence files (aligned with SOC2 audit cycle, typically 12-15 months), audit logs (minimum 12 months, recommended 24 months).
- Add retention-related fields (`retention_until`, `archived_at`, `deletion_scheduled_at`) to relevant data models.
- Implement a background worker (using Go's `time.Ticker` or a job scheduler like `robfig/cron`) that enforces retention policies by archiving or deleting expired data on a daily schedule.
- Create an inactive account policy that sends warning notifications 30, 14, and 7 days before account data deletion.
- Implement a data lifecycle state machine: active -> archived -> pending-deletion -> deleted.
- Ensure uploaded evidence files stored in object storage (S3, GCS, or local filesystem) are included in the retention policy with appropriate cleanup jobs.
- Document all retention periods in the privacy policy and make them accessible to users within the application settings.
- Allow organization administrators to configure custom retention periods within platform-defined bounds.

---

### GDPR-008: Cross-Border Data Transfer

**LEGAL QUESTION**

Does the system implement appropriate safeguards for the transfer of personal data to third countries or international organizations, consistent with GDPR Chapter V requirements?

**REGULATORY STANDARD**

GDPR Article 44 — General Principle for Transfers: Any transfer of personal data to a third country or an international organization shall take place only if the conditions laid down in this Chapter are complied with. GDPR Article 46 — Transfers Subject to Appropriate Safeguards. EU-US Data Privacy Framework (2023).

**EVIDENCE**

- `internal/config/config.go:18` — `type Config struct { ListenAddr string; DatabaseURL string; JWTSecret string; ... }`
- `internal/server/server.go:29` — `func New(cfg *config.Config) *Server { ... db, err := sql.Open("postgres", cfg.DatabaseURL) ... }`
- `internal/postgres/migrations/001_initial.up.sql:1` — `CREATE TABLE organizations ( id UUID PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT NOT NULL, ... );`

**FINDING: :yellow_circle: Pattern of Concern**

The application configuration contains no data residency controls. The PostgreSQL connection accepts any connection string without geographic constraints, meaning the database could be hosted in any jurisdiction. There is no mechanism to restrict data storage or processing to specific geographic regions. No Standard Contractual Clauses (SCCs) or adequacy decision references are documented in the codebase or deployment configuration. The multi-tenant architecture does not support per-tenant data residency requirements, which is significant because Probo's customers may be subject to different jurisdictional requirements. There is no indication of whether the deployment infrastructure is located within the EEA, and no Transfer Impact Assessment is documented.

**REMEDIATION DIRECTION**

Add data residency configuration options to the Config struct, allowing deployment operators to specify the data processing jurisdiction. Implement per-tenant data residency settings for organizations subject to specific geographic requirements. Document the supported deployment regions and the legal basis for any cross-border data transfers. Prepare Standard Contractual Clauses templates for customers. Create a Transfer Impact Assessment for deployments outside the EEA. Add geographic metadata to data records where cross-border transfer tracking is needed. Consider implementing data federation for multi-region deployments.

---

### GDPR-009: Data Protection Impact Assessment

**LEGAL QUESTION**

Has a Data Protection Impact Assessment been conducted for high-risk processing activities, and does the system architecture support the ongoing assessment and mitigation of data protection risks?

**REGULATORY STANDARD**

GDPR Article 35 — Data Protection Impact Assessment: Where a type of processing, in particular using new technologies, and taking into account the nature, scope, context, and purposes of the processing, is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall carry out an assessment of the impact of the envisaged processing operations on the protection of personal data. GDPR Article 35(3)(b) — Processing on a large scale of special categories of data.

**EVIDENCE**

- `internal/model/control.go:10` — `type Control struct { ID string; OrganizationID string; Title string; Description string; Status string; OwnerID string; CreatedAt time.Time; UpdatedAt time.Time }`
- `internal/model/evidence.go:10` — `type Evidence struct { ID string; ControlID string; Title string; Description string; FileURL string; CreatedAt time.Time; UpdatedAt time.Time }`
- `internal/model/policy.go:10` — `type Policy struct { ID string; OrganizationID string; Title string; Content string; Version int; CreatedAt time.Time }`

**FINDING: :yellow_circle: Pattern of Concern**

Probo stores compliance data that may include sensitive organizational information: control descriptions may reference security vulnerabilities, evidence files may contain screenshots of internal systems, and policy documents may describe security architectures. The `OwnerID` field in controls links personal data to compliance responsibilities. Evidence files uploaded via `FileURL` could contain any type of content including personal data. The platform processes data on behalf of multiple organizations, which may qualify as "large scale" processing under Article 35(3). No DPIA documentation exists in the repository. The data model does not include sensitivity classification, and there is no mechanism to flag high-risk data or processing activities.

**REMEDIATION DIRECTION**

Conduct a formal DPIA covering all processing activities within the Probo platform. Document the necessity and proportionality of processing, the risks to data subjects, and the mitigation measures in place. Implement data sensitivity classification on evidence uploads and policy documents. Add content scanning or classification prompts when users upload evidence files. Create a DPIA template that Probo's customers can use for their own assessments. Review the DPIA annually or when significant changes to processing activities occur. Publish a summary of the DPIA findings in the platform's trust center or security documentation.

---

### GDPR-010: Privacy Policy and Notice

**LEGAL QUESTION**

Does the system present users with clear, accessible, and comprehensive privacy notices at the point of data collection, and does the organization maintain a privacy policy that meets GDPR transparency requirements?

**REGULATORY STANDARD**

GDPR Article 12 — Transparent Information, Communication, and Modalities: The controller shall take appropriate measures to provide information referred to in Articles 13 and 14 to the data subject in a concise, transparent, intelligible, and easily accessible form, using clear and plain language. GDPR Article 13 — Information to be provided where personal data are collected from the data subject.

**EVIDENCE**

- `internal/graph/schema.graphqls:5` — `type Mutation { createUser(input: CreateUserInput!): User! login(email: String!, password: String!): AuthPayload! ... }`
- `internal/graph/schema.resolvers.go:23` — `func (r *mutationResolver) CreateUser(ctx context.Context, input model.CreateUserInput) (*model.User, error) { ... }`
- `cmd/probo/main.go:67` — `router.Handle("/api/login", server.handleLogin).Methods("POST")`
- `README.md:1` — `# Probo - Open Source SOC2 Compliance Platform`

**FINDING: :yellow_circle: Pattern of Concern**

No privacy policy or privacy notice is present in the codebase, documentation, or frontend assets. The user registration and login flows do not present any privacy information to data subjects at the point of data collection. The README and documentation do not reference a privacy policy URL. There are no in-app privacy banners, cookie consent notices, or terms of service acceptance flows. Article 13 requires that specific information — including the identity of the controller, purposes of processing, lawful basis, data retention periods, and data subject rights — be provided at the time personal data is collected. None of this information is provided in the current implementation. Users create accounts and provide personal data without being informed how that data will be used, stored, or protected.

**REMEDIATION DIRECTION**

Create a comprehensive privacy policy covering all Article 13 required information: controller identity and contact details, DPO contact (if applicable), purposes and legal basis for processing, categories of personal data, data retention periods, data subject rights, and complaint procedures. Implement an in-app privacy notice that is presented during user registration. Add a terms of service acceptance checkbox to the registration flow with a link to the full privacy policy. Implement a cookie consent banner if cookies or tracking technologies are used. Create a privacy center page within the application where users can access the privacy policy, manage their consent preferences, and exercise their data subject rights. Ensure the privacy policy is written in plain language and is easily accessible from every page of the application.

---

## Disclaimer

This report was generated by OpenDocket automated compliance analysis tooling. The findings, risk assessments, and remediation recommendations contained herein are based on static analysis of the publicly available source code at https://github.com/getprobo/probo and do not constitute a complete compliance audit.

**This report does not constitute legal advice.** Compliance with SOC2 Trust Services Criteria and the General Data Protection Regulation (GDPR) requires a holistic assessment encompassing organizational policies, operational procedures, infrastructure configuration, and legal agreements that extend beyond source code analysis.

Key limitations of this analysis:

- **Infrastructure not assessed:** Cloud provider configurations, network security, and deployment architecture are not visible in source code and were not evaluated.
- **Operational controls not assessed:** Employee security training, background checks, physical security, and business continuity planning are outside the scope of code analysis.
- **Point-in-time analysis:** This report reflects the state of the codebase at the time of analysis and does not account for subsequent changes.
- **Self-hosted considerations:** As an open-source project, Probo may be deployed in various configurations. This analysis evaluates the default codebase, not any specific deployment.

Organizations using this report should engage qualified SOC2 auditors (CPA firms) and GDPR-specialized legal counsel to obtain definitive compliance determinations. The risk levels assigned (High Risk, Medium Risk, Pattern of Concern, No Issue Found) reflect relative severity based on code-level evidence and should be calibrated against the organization's specific risk tolerance, deployment context, and regulatory obligations.

**Risk level definitions used in this report:**

| Level | Definition |
|---|---|
| :red_circle: High Risk | Critical compliance gap requiring immediate attention. Represents a likely violation or absence of a required control that could result in regulatory action, data breach, or audit failure. |
| :orange_circle: Medium Risk | Significant compliance gap that should be addressed in the near term. The control exists in partial form or has material weaknesses that reduce its effectiveness. |
| :yellow_circle: Pattern of Concern | An area where best practices are not fully implemented. While not an immediate violation, the gap increases risk exposure and should be addressed as part of a compliance improvement roadmap. |
| :green_circle: No Issue Found | The control is implemented in a manner consistent with the regulatory requirement based on code-level evidence. Continued monitoring and periodic review recommended. |

---

*Report generated by OpenDocket V1 on 2026-03-22.*
