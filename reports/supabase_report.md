# OpenDocket Compliance Report: supabase

> **Repository:** https://github.com/supabase/supabase
> **Scan Date:** 2026-03-22
> **Scanner Version:** OpenDocket V1

---

**DISCLAIMER:** OpenDocket identifies risk patterns through automated code analysis. Findings represent potential areas of concern, not legal determinations. This report does not constitute legal advice. Regulatory compliance requires qualified legal and technical assessment. Consult a licensed attorney and certified compliance professional for definitive compliance determination.

---

## Domain Detection

- **Saas** — Confidence: 92.2% (14624 signals, top: auth, organization, plan, team, billing)
- **Ecommerce** — Confidence: 76.5% (3110 signals, top: product, order, catalog, marketplace, warehouse)
- **Fintech** — Confidence: 60.7% (3586 signals, top: card, swift, stripe, payment, transaction)
- **Communication** — Confidence: 46.0% (3150 signals, top: call, sms, twilio, notification, unsubscribe)
- **Healthcare** — Confidence: 40.8% (2766 signals, top: provider, rx, hipaa, hl7, medical)
- **Gdpr** — Confidence: 16.7% (126 signals, top: consent, gdpr, dpo, portability)
- **Sox** — Confidence: 5.9% (13 signals, top: sox)

## Frameworks Analyzed: GDPR, HIPAA, PCI-DSS, SOC2, SOX, TCPA

## Executive Summary

| Finding Level | Count |
|---|---|
| High Risk | 47 |
| Medium Risk | 4 |
| Pattern of Concern | 3 |
| No Issue Found | 2 |

## GDPR Findings

### GDPR-001: Lawful Basis for Processing Personal Data

**LEGAL QUESTION**

Does this system process personal data of EU residents, and if so, is there evidence that a lawful basis for processing under Article 6 GDPR has been identified and implemented for each processing activity?

**REGULATORY STANDARD**

GDPR Article 6 (Lawfulness of Processing)

**EVIDENCE**

- `.claude/skills/telemetry-standards/SKILL.md:61` — `**Never track PII** (emails, names, IPs, etc.) in event properties.`
- `.claude/skills/telemetry-standards/SKILL.md:169` — `- [ ] No PII in event properties (emails, names, IPs, etc.)`
- `.github/instructions/studio-telemetry.instructions.md:46` — `- Never track PII`
- `apps/docs/content/guides/ai.mdx:82` — `name: 'Markprompt: GDPR-Compliant AI Chatbots for Docs and Websites',`
- `apps/docs/content/guides/ai.mdx:84` — `"AI-powered chatbot platform, Markprompt, empowers developers to deliver efficient and GDPR-compliant prompt experiences`
- `apps/docs/content/guides/auth/auth-anonymous.mdx:7` — `[Enable Anonymous Sign-Ins](/dashboard/project/_/auth/providers) to build apps which provide users an authenticated expe`
- `apps/docs/content/guides/auth/auth-web3.mdx:37` — `It defines the wallet address, timestamp, browser location where the sign-in occurred and includes a customizable statem`
- `apps/docs/content/guides/auth/auth-web3.mdx:185` — `Providing a `statement` is required for most Solana wallets and this message will be shown to the user on the consent di`
- `apps/docs/content/guides/auth/oauth-server/getting-started.mdx:57` — `authorization_url_path = "/oauth/consent"`
- `apps/docs/content/guides/auth/oauth-server/getting-started.mdx:139` — `2. Set the **Authorization Path** (e.g., `/oauth/consent`)`

**FINDING: 🔴 High Risk**

The evidence shows this system processes personal data of EU residents through authentication features (emails, passwords, OAuth) and AI chatbot functionality, but no documented lawful basis for processing under GDPR Article 6 was found. While privacy-protective measures exist (PII exclusion from telemetry in .claude/skills/telemetry-standards/SKILL.md:61, GDPR-compliant AI mentions in apps/docs/content/guides/ai.mdx:82), and consent mechanisms are implemented for OAuth flows, there is no evidence of systematic identification and documentation of lawful bases for each personal data processing activity as required by Article 6.

**REMEDIATION DIRECTION**

Conduct a comprehensive data processing audit to identify all personal data processing activities (authentication, user profiles, analytics, AI interactions, etc.) and document the specific Article 6 lawful basis for each (likely consent for optional features, contract performance for service delivery, or legitimate interests for security/fraud prevention). Create a legal basis register mapping each processing purpose to its lawful basis, implement privacy notices explaining these bases to users, and ensure technical controls align with the documented legal bases. Consider adding data processing documentation to your privacy policy or terms of service to demonstrate compliance.

---

### GDPR-002: Consent Collection and Management

**LEGAL QUESTION**

Does the system implement consent collection mechanisms that satisfy the conditions for consent under Article 7, including freely given, specific, informed, and unambiguous indication of the data subject's wishes, with capability to withdraw consent?

**REGULATORY STANDARD**

GDPR Article 7 (Conditions for Consent)

**EVIDENCE**

- `.cursor/rules/studio/queries/RULE.md:139` — `- accepts `UseCustomMutationOptions` (omit `mutationFn`)`
- `.cursor/rules/testing/e2e-studio/RULE.md:117` — `// ✅ Acceptable - waiting for client-side debounce`
- `CONTRIBUTING.md:25` — `- We will always try to accept the first viable PR that resolves the Issue.`
- `CONTRIBUTING.md:27` — `- If you’re submitting a new feature, make sure you have opened a [Discussion](https://github.com/orgs/supabase/discussi`
- `DEVELOPERS.md:172` — `We review PRs in the order of their submission. We try to accept the earliest one that is closest to being ready to merg`
- `LICENSE:135` — `the terms of any separate license agreement you may have executed`
- `LICENSE:144` — `agreed to in writing, Licensor provides the Work (and each`
- `LICENSE:156` — `negligent acts) or agreed to in writing, shall any Contributor be`
- `LICENSE:171` — `of any other Contributor, and only if You agree to indemnify,`
- `LICENSE:197` — `Unless required by applicable law or agreed to in writing, software`

**FINDING: 🔴 High Risk**

No evidence of GDPR Article 7 compliant consent collection mechanisms was found in the analyzed code repository. The evidence consists entirely of generic usage of the word "accept" in documentation, license files, and component descriptions (such as in apps/design-system/content/docs/components/field.mdx:308 and CONTRIBUTING.md:25), with no implementation of consent collection, management, or withdrawal functionality. This represents a risk pattern consistent with non-compliance under GDPR Article 7, which requires systems processing personal data to implement specific consent mechanisms that are freely given, specific, informed, and unambiguous.

**REMEDIATION DIRECTION**

The system needs to implement a comprehensive consent management framework that includes: user-facing consent collection interfaces with clear, specific language about data processing purposes; backend systems to store and track consent status per user and processing purpose; mechanisms for users to easily withdraw consent; and audit trails showing when consent was given, modified, or withdrawn. This should include both UI components for consent collection and API endpoints for consent management operations.

---

### GDPR-003: Right to Erasure Implementation

**LEGAL QUESTION**

Does the system implement the right to erasure (right to be forgotten) under Article 17, allowing data subjects to request deletion of their personal data without undue delay?

**REGULATORY STANDARD**

GDPR Article 17 (Right to Erasure)

**EVIDENCE**

- `apps/design-system/tailwind.config.js:8` — `// purge styles from grid library`
- `apps/docs/DEVELOPERS.md:22` — `4. Visit http://localhost:3001/docs in your browser - don't forget to append the `/docs` to the end`
- `apps/docs/content/errorCodes/authErrorCodes.toml:64` — `description = "PKCE flow state to which the API request relates no longer exists. Flow states expire after a while and a`
- `apps/docs/content/guides/ai/going-to-prod.mdx:114` — `Don't forget to check out the general [Production Checklist](/docs/guides/platform/going-into-prod) to ensure your proje`
- `apps/docs/content/guides/ai/integrations/llamaindex.mdx:49` — `SQLAlchemy requires the connection string to start with `postgresql://` (instead of `postgres://`). Don't forget to rena`
- `apps/docs/content/guides/ai/quickstarts/face-similarity.mdx:47` — `SQLAlchemy requires the connection string to start with `postgresql://` (instead of `postgres://`). Don't forget to rena`
- `apps/docs/content/guides/ai/quickstarts/hello-world.mdx:48` — `SQLAlchemy requires the connection string to start with `postgresql://` (instead of `postgres://`). Don't forget to rena`
- `apps/docs/content/guides/ai/quickstarts/text-deduplication.mdx:48` — `SQLAlchemy requires the connection string to start with `postgresql://` (instead of `postgres://`). Don't forget to rena`
- `apps/docs/content/guides/auth/jwts.mdx:210` — `Make sure that you do not cache this data for longer in your application, as it might make revocation difficult. If you `
- `apps/docs/content/guides/auth/sessions.mdx:64` — `Sessions are not proactively destroyed when you change these settings, but rather the check is enforced whenever a sessi`

**FINDING: 🔴 High Risk**

No evidence found of system implementation for GDPR Article 17 right to erasure functionality. The evidence shows only technical references to data deletion mechanisms (such as delete_user() function in apps/docs/content/guides/database/prisma/prisma-troubleshooting.mdx:215 and session destruction in signout processes), but lacks any user-facing erasure request handling, data subject rights endpoints, or systematic personal data deletion workflows. This represents a risk pattern consistent with non-compliance under GDPR Article 17.

**REMEDIATION DIRECTION**

Implement a comprehensive right to erasure system including: user-facing request mechanisms (API endpoints, UI forms) for data subjects to request deletion; backend processing workflows to identify and delete personal data across all system components within required timeframes; verification and confirmation processes for deletion requests; logging and audit trails for erasure activities; and integration with existing authentication and database systems to ensure complete data removal while maintaining system integrity.

---

### GDPR-004: Data Portability Capability

**LEGAL QUESTION**

Does the system provide data subjects the right to receive their personal data in a structured, commonly used, and machine-readable format, and to transmit that data to another controller, as required under Article 20?

**REGULATORY STANDARD**

GDPR Article 20 (Right to Data Portability)

**EVIDENCE**

- `.agents/skills/vitest/references/advanced-environments.md:146` — `export default <Environment>{`
- `.agents/skills/vitest/references/advanced-environments.md:178` — `export default <Environment>{`
- `.agents/skills/vitest/references/advanced-projects.md:61` — `export default defineConfig({`
- `.agents/skills/vitest/references/advanced-projects.md:132` — `export const sharedConfig = {`
- `.agents/skills/vitest/references/core-config.md:16` — `export default defineConfig({`
- `.agents/skills/vitest/references/core-config.md:32` — `export default defineConfig({`
- `.agents/skills/vitest/references/core-config.md:49` — `export default mergeConfig(viteConfig, defineConfig({`
- `.agents/skills/vitest/references/core-config.md:126` — `export default defineConfig(({ mode }) => ({`
- `.agents/skills/vitest/references/features-context.md:42` — `export const test = base.extend<Fixtures>({`
- `.agents/skills/vitest/references/features-context.md:211` — `export const test = base.extend<{ db: Database }>({`

**FINDING: 🔴 High Risk**

No evidence of data portability functionality was found in the code repository. The evidence consists entirely of testing configuration files and documentation from vitest and testing frameworks, with no implementation of data export, structured data formats, or user-facing data portability features. This represents a risk pattern consistent with non-compliance under GDPR Article 20, which mandates that data subjects must be able to receive their personal data in structured, commonly used, and machine-readable formats.

**REMEDIATION DIRECTION**

Implement a comprehensive data portability system that allows users to request and receive their personal data in structured formats (JSON, CSV, XML). This should include: API endpoints for data export requests, user interface components for initiating data downloads, automated data compilation from all systems storing user data, and secure delivery mechanisms. The system must cover all personal data categories and provide exports in commonly used, machine-readable formats that can be transmitted to other data controllers.

---

### GDPR-005: Privacy by Design Evidence

**LEGAL QUESTION**

Does the system demonstrate evidence of data protection by design and by default, implementing appropriate technical and organizational measures to ensure only necessary personal data is processed, as required under Article 25?

**REGULATORY STANDARD**

GDPR Article 25 (Data Protection by Design and by Default)

**EVIDENCE**

- `.claude/skills/studio-testing/rules/testing-extract-logic.md:28` — `let sanitized = taxIdValue`
- `.claude/skills/studio-testing/rules/testing-extract-logic.md:30` — `sanitized = taxId.vatPrefix + taxIdValue`
- `.claude/skills/studio-testing/rules/testing-extract-logic.md:32` — `submitToApi(sanitized)`
- `.claude/skills/studio-testing/rules/testing-extract-logic.md:46` — `export function sanitizeTaxIdValue({ value, name }: { value: string; name: string }): string {`
- `.claude/skills/studio-testing/rules/testing-extract-logic.md:57` — `import { sanitizeTaxIdValue } from './TaxID.utils'`
- `.claude/skills/studio-testing/rules/testing-extract-logic.md:61` — `const sanitized = sanitizeTaxIdValue({ value: taxIdValue, name: taxIdName })`
- `.claude/skills/studio-testing/rules/testing-extract-logic.md:62` — `submitToApi(sanitized)`
- `.claude/skills/studio-testing/rules/testing-extract-logic.md:70` — `import { sanitizeTaxIdValue } from 'components/.../TaxID.utils'`
- `.claude/skills/studio-testing/rules/testing-extract-logic.md:72` — `describe('sanitizeTaxIdValue', () => {`
- `.claude/skills/studio-testing/rules/testing-extract-logic.md:74` — `expect(sanitizeTaxIdValue({ value: '12345678', name: 'AT VAT' })).toBe('ATU12345678')`

**FINDING: 🔵 Pattern of Concern**

Limited evidence of data protection by design and by default implementation was found in the codebase. While some data sanitization functions exist (sanitizeTaxIdValue in testing-extract-logic.md:46-82) and basic security references appear in UI components, there is insufficient evidence of comprehensive technical and organizational measures to ensure only necessary personal data is processed. The scattered references to encryption, secure transactions, and data redaction guidelines suggest awareness but lack systematic implementation patterns required by the regulatory standard.

**REMEDIATION DIRECTION**

Implement a comprehensive data protection by design framework including: data minimization controls at API endpoints, automated PII detection and masking, role-based access controls with audit logging, and data retention policies with automatic purging. Add privacy impact assessments for new features, establish data processing inventories, and create systematic validation that only necessary personal data fields are collected and processed throughout the application lifecycle.

---

### GDPR-006: Data Breach Detection and Notification

**LEGAL QUESTION**

Does the system implement mechanisms for detecting personal data breaches and notifying the supervisory authority within 72 hours and affected data subjects without undue delay, as required under Articles 33 and 34?

**REGULATORY STANDARD**

GDPR Articles 33 (Notification to Authority); 34 (Communication to Data Subject)

**EVIDENCE**

- `.cursor/rules/studio-useStaticEffectEvent.mdc:23` — `showNotification('Connected!', theme) // `theme` causes unwanted re-runs`
- `.cursor/rules/studio/RULE.md:32` — `- `studio/alerts``
- `.cursor/rules/studio/alerts/RULE.md:2` — `description: "Studio: alert/admonition usage and placement"`
- `.cursor/rules/studio/alerts/RULE.md:8` — `# Studio alerts`
- `.cursor/rules/studio/best-practices/RULE.md:154` — `return <AlertError error={error} subject="Failed to load data" />`
- `.github/workflows/dashboard-pr-reminder.yml:44` — `run: pnpm tsx scripts/actions/find-stale-dashboard-prs.ts | pnpm tsx scripts/actions/send-slack-pr-notification.ts`
- `LICENSE:158` — `incidental, or consequential damages of any character arising as a`
- `SECURITY.md:26` — `- Do not run automated scanners on other customer projects. Running automated scanners can run up costs for our users. A`
- `apps/design-system/__registry__/default/block/chart-composed-actions.tsx:26` — `alert('Opening in Logs Explorer...')`
- `apps/design-system/__registry__/default/block/chart-composed-basic.tsx:25` — `alert('Ta da! You clicked me! 🎉')`

**FINDING: 🔴 High Risk**

No evidence found of GDPR-compliant data breach detection or notification mechanisms in the codebase. The evidence shows only basic UI alerts and notifications (e.g., showNotification calls in .cursor/rules/studio-useStaticEffectEvent.mdc:23 and generic alert components in the design system), but contains no implementation of personal data breach detection systems, automated supervisory authority notification within 72 hours, or data subject notification processes. This represents a risk pattern consistent with non-compliance under GDPR Articles 33 and 34.

**REMEDIATION DIRECTION**

Implement a comprehensive data breach detection and notification system that includes: automated monitoring for unauthorized access to personal data, incident logging and classification mechanisms, automated notification workflows to supervisory authorities within 72 hours of breach detection, and systems for notifying affected data subjects without undue delay when required. The system should include breach assessment capabilities to determine notification thresholds, template management for standardized notifications, and audit trails for compliance documentation.

---

### GDPR-007: Data Retention and Deletion Policies

**LEGAL QUESTION**

Does the system implement data retention policies that limit the storage of personal data to what is necessary for the specified processing purpose, with automated deletion or anonymization when the purpose is fulfilled, consistent with the storage limitation principle under Article 5(1)(e)?

**REGULATORY STANDARD**

GDPR Article 5(1)(e) (Storage Limitation Principle)

**EVIDENCE**

- `.agents/skills/vitest/references/advanced-vi.md:98` — `await vi.dynamicImportSettled()`
- `.agents/skills/vitest/references/core-hooks.md:30` — `await cleanupMocks()`
- `.agents/skills/vitest/references/core-hooks.md:34` — `## Cleanup Return Pattern`
- `.agents/skills/vitest/references/core-hooks.md:36` — `Return cleanup function from `before*` hooks:`
- `.agents/skills/vitest/references/core-hooks.md:143` — `test('with cleanup', () => {`
- `.agents/skills/vitest/references/core-hooks.md:158` — `### Reusable Cleanup Pattern`
- `.agents/skills/vitest/references/core-hooks.md:236` — `- Return cleanup function from `before*` to avoid `after*` duplication`
- `.agents/skills/vitest/references/features-context.md:25` — `- `onTestFinished(fn)` - Cleanup after test`
- `.agents/skills/vitest/references/features-context.md:47` — `await db.close()        // Cleanup`
- `.agents/skills/vitest/references/features-context.md:230` — `- Return cleanup function from fixtures`

**FINDING: 🔴 High Risk**

No evidence of GDPR-compliant data retention policies or automated deletion mechanisms for personal data was found in the codebase. While the evidence shows numerous cleanup functions and patterns (e.g., `.agents/skills/vitest/references/core-hooks.md:30` with `cleanupMocks()` and `.claude/skills/e2e-studio-tests/SKILL.md:206` describing database resets), these appear to be technical cleanup operations for testing environments rather than business logic implementing data retention policies for personal data. This presents a risk pattern consistent with non-compliance under GDPR Article 5(1)(e) storage limitation requirements.

**REMEDIATION DIRECTION**

Implement comprehensive data retention policies that automatically delete or anonymize personal data when processing purposes are fulfilled. This should include: (1) configurable retention periods for different data types based on legal basis and processing purpose, (2) automated background jobs that regularly scan for and delete expired personal data, (3) data classification systems to identify what constitutes personal data requiring retention limits, and (4) audit logging of all data deletion activities. Consider implementing database-level policies using tools like PostgreSQL's pg_cron extension (mentioned in testing files) for production data lifecycle management, not just test cleanup.

---

### GDPR-008: Cross-Border Data Transfer Safeguards

**LEGAL QUESTION**

Does the system implement appropriate safeguards for transfers of personal data to third countries or international organizations, such as Standard Contractual Clauses or adequacy decisions, as required under Chapter V?

**REGULATORY STANDARD**

GDPR Chapter V, Articles 44-49 (Transfers to Third Countries)

**EVIDENCE**

- `.github/workflows/mirror.yml:28` — `aws-region: us-east-1`
- `LICENSE:77` — `use, offer to sell, sell, import, and otherwise transfer the Work,`
- `apps/design-system/app/fonts/CustomFont-Bold.woff2:99` — `Zơs84UaF8 xx?F~(4	?3̵ h@fB 0C%q㥭z:VͲUvꜽbUN@~#tP^eT}03yPmJ/+Zf{DySLU臓ZIhsccޘEȌ#%qݗܭf[mvoWf*v6`
- `apps/design-system/content/docs/copywriting.mdx:138` — `| "General configuration, domains, ownership, and lifecycle" | "Configure general options, domains, transfers, and proje`
- `apps/design-system/registry/default/example/form-patterns-pagelayout.tsx:344` — `const files = Array.from(e.dataTransfer.files)`
- `apps/design-system/registry/default/example/form-patterns-pagelayout.tsx:57` — `region: z.string().min(1, 'Region is required'),`
- `apps/design-system/registry/default/example/form-patterns-pagelayout.tsx:87` — `region: '',`
- `apps/design-system/registry/default/example/form-patterns-pagelayout.tsx:509` — `name="region"`
- `apps/design-system/registry/default/example/form-patterns-pagelayout.tsx:528` — `<SelectItem_Shadcn_ value="eu-west-1">`
- `apps/design-system/registry/default/example/form-patterns-pagelayout.tsx:529` — `EU West (Ireland)`

**FINDING: 🔴 High Risk**

Risk pattern consistent with non-compliance under GDPR Chapter V Articles 44-49. The system shows evidence of cross-border data transfers to third countries (US regions including us-east-1 and us-west-2 in multiple files), but no safeguards such as Standard Contractual Clauses, adequacy decisions, or transfer impact assessments were found in the codebase. Anti-patterns detected include hardcoded US AWS regions in .github/workflows/mirror.yml:28 and form examples throughout the design system components.

**REMEDIATION DIRECTION**

Implement appropriate transfer safeguards before any personal data processing in third countries. This includes: (1) conducting Transfer Impact Assessments for all third-country transfers, (2) implementing Standard Contractual Clauses with data processors in non-adequate countries, (3) documenting adequacy decisions where applicable, (4) adding configuration options to restrict data processing to adequate jurisdictions, and (5) creating policy documentation that governs cross-border data transfer decisions. Consider defaulting to EU regions and requiring explicit approval for third-country data processing.

---

### GDPR-009: Data Protection Impact Assessment Indicators

**LEGAL QUESTION**

Does the system process personal data in a manner likely to result in high risk to data subjects, and if so, is there evidence that a Data Protection Impact Assessment has been considered, as required under Article 35?

**REGULATORY STANDARD**

GDPR Article 35 (Data Protection Impact Assessment)

**EVIDENCE**

- `.agents/skills/vitest/references/core-expect.md:213` — `- Use context's `expect` in concurrent tests for correct tracking`
- `.claude/skills/telemetry-standards/SKILL.md:3` — `description: PostHog event tracking standards for Supabase Studio. Use when reviewing`
- `.claude/skills/telemetry-standards/SKILL.md:4` — `PRs for telemetry compliance or implementing new event tracking. Covers event naming,`
- `.claude/skills/telemetry-standards/SKILL.md:10` — `Standards for PostHog event tracking in `apps/studio/`. Apply these when`
- `.claude/skills/telemetry-standards/SKILL.md:11` — `reviewing PRs that touch tracking or when implementing new tracking.`
- `.claude/skills/telemetry-standards/SKILL.md:59` — `**Exception:** `_exposed` events for A/B experiment exposure tracking are valid even though they fire on render.`
- `.claude/skills/telemetry-standards/SKILL.md:116` — `4. **Unnecessary view tracking** — events that fire on page load without user interaction`
- `.claude/skills/telemetry-standards/SKILL.md:119` — `When a PR adds user-facing interactions (buttons, forms, toggles, modals) **without** tracking, suggest:`
- `.claude/skills/telemetry-standards/SKILL.md:120` — `- "This adds a user interaction that may benefit from tracking."`
- `.claude/skills/telemetry-standards/SKILL.md:152` — `## Implementing New Tracking`

**FINDING: 🔴 High Risk**

The evidence reveals extensive personal data processing through telemetry and tracking systems (PostHog event tracking standards in `.claude/skills/telemetry-standards/SKILL.md` and studio telemetry instructions in `.github/instructions/studio-telemetry.instructions.md`) that collect user interaction data, but no evidence of a Data Protection Impact Assessment (DPIA) was found in the repository. This creates a risk pattern consistent with non-compliance under GDPR Article 35, which requires DPIAs for processing likely to result in high risk to data subjects.

**REMEDIATION DIRECTION**

Conduct a formal Data Protection Impact Assessment to evaluate the privacy risks associated with the telemetry and user tracking systems. Document this assessment in the repository with clear findings about data processing activities, risk mitigation measures, and safeguards. Additionally, implement privacy-by-design principles in the tracking systems and ensure proper consent mechanisms are in place before collecting personal data through these telemetry systems.

---

### GDPR-010: Privacy Policy and Notice Requirements

**LEGAL QUESTION**

Does the system provide transparent information to data subjects about the processing of their personal data, including identity of the controller, purposes of processing, and data subject rights, as required under Articles 13 and 14?

**REGULATORY STANDARD**

GDPR Articles 13 (Information at Collection); 14 (Information Not from Data Subject)

**EVIDENCE**

- `.cursor/rules/docs/docs-graphql/RULE.md:12` — `The `apps/docs/resources` folder contains the GraphQL endpoint architecture for the docs GraphQL endpoint at `/api/graph`
- `.cursor/rules/docs/docs-graphql/RULE.md:99` — `> The types in `~/__generated__/graphql` for a new endpoint will not exist`
- `.cursor/rules/studio/cards/RULE.md:10` — `- Use cards to group related pieces of information.`
- `.cursor/rules/studio/empty-states/RULE.md:2` — `description: 'Studio: empty state patterns (presentational vs informational vs zero-results vs missing route)'`
- `.cursor/rules/studio/empty-states/RULE.md:15` — `- `apps/design-system/registry/default/example/empty-state-initial-state-informational.tsx``
- `.cursor/rules/studio/empty-states/RULE.md:23` — `- Data-heavy lists: prefer informational empty states that match the list/table layout.`
- `.cursor/rules/testing/e2e-studio/RULE.md:304` — `await waitForApiResponse(page, 'pg-meta', ref, 'optional-endpoint', {`
- `.github/workflows/studio-unit-tests.yml:2` — `# For more information see: https://help.github.com/actions/language-and-framework-guides/using-nodejs-with-github-actio`
- `LICENSE:116` — `of the NOTICE file are for informational purposes only and`
- `LICENSE:182` — `replaced with your own identifying information. (Don't include`

**FINDING: 🔴 High Risk**

No evidence was found in the code repository of privacy notices, data processing disclosures, or data subject rights information required under GDPR Articles 13 and 14. The evidence consists only of technical documentation, licensing notices, and development patterns, with no privacy policy, data collection notices, or transparency mechanisms for users regarding personal data processing. This represents a risk pattern consistent with non-compliance under GDPR Articles 13 and 14.

**REMEDIATION DIRECTION**

Implement comprehensive privacy notices that inform data subjects about data processing activities. This should include creating user-facing privacy policies, in-application notices at data collection points, and clear disclosures about the identity of the data controller (Supabase), purposes of processing, legal bases, data retention periods, and data subject rights (access, rectification, erasure, portability, etc.). These notices should be integrated into the user interface where personal data is collected and easily accessible to users throughout their interaction with the platform.

---

## HIPAA Findings

### HIPAA-001: PHI Identification and Protection

**LEGAL QUESTION**

Does this system collect, store, process, or transmit individually identifiable health information as defined under 45 CFR §160.103, and if so, are adequate technical safeguards in place to protect the confidentiality of such Protected Health Information?

**REGULATORY STANDARD**

HIPAA Privacy Rule 45 CFR §160.103; Security Rule 45 CFR §164.312(a)(1)

**EVIDENCE**

- `.agents/skills/vitest/references/advanced-environments.md:106` — `el.className = 'test'`
- `.agents/skills/vitest/references/advanced-environments.md:107` — `expect(el.className).toBe('test')`
- `.agents/skills/vitest/references/advanced-environments.md:229` — `classNameStrategy: 'non-scoped',`
- `.claude/skills/vercel-composition-patterns/AGENTS.md:863` — `return <footer className='flex'>{children}</footer>`
- `.claude/skills/vercel-composition-patterns/AGENTS.md:812` — `Use `children` for composition instead of `renderX` props. Children are more`
- `.claude/skills/vercel-composition-patterns/SKILL.md:63` — `of renderX props`
- `.claude/skills/vercel-composition-patterns/rules/patterns-children-over-render-props.md:59` — `return <footer className='flex'>{children}</footer>`
- `.claude/skills/vercel-composition-patterns/rules/patterns-children-over-render-props.md:10` — `Use `children` for composition instead of `renderX` props. Children are more`
- `.cursor/rules/studio/best-practices/RULE.md:120` — `<TabsTrigger_Shadcn_ value="overview" className="px-0 pb-0 h-full text-xs data-[state=active]:bg-transparent !shadow-non`
- `.cursor/rules/studio/best-practices/RULE.md:123` — `<TabsTrigger_Shadcn_ value="logs" className="px-0 pb-0 h-full text-xs data-[state=active]:bg-transparent !shadow-none">`

**FINDING: 🟢 No Issue Found**

The evidence provided consists entirely of frontend user interface code, including CSS class names, React component markup, and testing framework configuration files. No individually identifiable health information as defined under 45 CFR §160.103 was identified in any of the examined code paths, and the Supabase platform documentation indicates this is a general-purpose database and API development platform rather than a healthcare-specific system.

**REMEDIATION DIRECTION**

No remediation required based on current evidence. However, if this system will be extended to handle PHI in the future, ensure proper technical safeguards are implemented including access controls, audit controls, integrity controls, person or entity authentication, and transmission security as required under 45 CFR §164.312(a)(1).

---

### HIPAA-002: Encryption at Rest

**LEGAL QUESTION**

Is electronic Protected Health Information encrypted when stored at rest using methods consistent with NIST Special Publication 800-111, as required for addressable implementation under the HIPAA Security Rule?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.312(a)(2)(iv); NIST SP 800-111

**EVIDENCE**

- `apps/design-system/app/fonts/CustomFont-Black.woff2:212` — `"#dWpd?zL+^G§kS[h(ԭ/t!aOuld]F" מ̢!o._->[BkzO8Rf$ZC/XE"usMkmS-hXᝁ]2.0)l[`
- `apps/design-system/app/fonts/CustomFont-BoldItalic.woff2:223` — `1,_nxrc8p}#n,Tj~!H!9^C(?\PXt(骭tREYf\K^Mv+ǝʺKKHP(aTi;u0w;a1TdM(1":Vڦ/1.:TP,*zw=]:G搩OW_cWbX\,I={GZ`
- `apps/design-system/registry/default/example/accordion-demo.tsx:20` — `Yes. It comes with default styles that matches the other components&apos; aesthetic.`
- `apps/design-system/registry/default/example/field-demo.tsx:26` — `<FieldDescription>All transactions are secure and encrypted</FieldDescription>`
- `apps/design-system/registry/default/example/field-demo.tsx:26` — `<FieldDescription>All transactions are secure and encrypted</FieldDescription>`
- `apps/design-system/registry/default/example/select-scrollable.tsx:55` — `<SelectItem_Shadcn_ value="aest">`
- `apps/design-system/registry/default/example/select-scrollable.tsx:56` — `Australian Eastern Standard Time (AEST)`
- `apps/design-system/registry/default/example/toc-demo.tsx:104` — `proper authentication, encryption, and access controls.`
- `apps/design-system/registry/default/example/toc-single-demo.tsx:104` — `proper authentication, encryption, and access controls.`
- `apps/docs/components/AppleSecretGenerator/AppleSecretGenerator.tsx:56` — `const privateKey = await globalThis.crypto.subtle.importKey(`

**FINDING: 🔴 High Risk**

No evidence of encryption at rest implementation consistent with NIST SP 800-111 standards was found in the analyzed code repository. While references to encryption exist in UI components (field-demo.tsx:26, toc-demo.tsx:104) and cryptographic functions for JWT generation are present, these are client-side operations and do not address server-side data storage encryption requirements. The detected anti-patterns showing base64 encoding usage (particularly in AppleSecretGenerator.tsx and workflow files) represent encoding rather than encryption, creating a risk pattern consistent with non-compliance under HIPAA Security Rule 45 CFR §164.312(a)(2)(iv).

**REMEDIATION DIRECTION**

Implement server-side encryption at rest for all stored data using NIST SP 800-111 compliant methods such as AES-256 encryption. This should include database encryption, file system encryption, and proper key management systems. Add configuration files and code documentation demonstrating the encryption implementation, key rotation procedures, and compliance with NIST standards. Replace any base64 encoding used for security purposes with proper encryption algorithms, and ensure all PHI storage locations are identified and encrypted according to the addressable implementation requirements.

---

### HIPAA-003: Encryption in Transit

**LEGAL QUESTION**

Are all transmissions of electronic Protected Health Information encrypted using transport-level security consistent with NIST guidelines, preventing unauthorized access during transmission across electronic communications networks?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.312(e)(1); 45 CFR §164.312(e)(2)(ii)

**EVIDENCE**

- `.agents/skills/vitest/SKILL.md:7` — `source: Generated from https://github.com/vitest-dev/vitest, scripts located at https://github.com/antfu/skills`
- `.agents/skills/vitest/references/advanced-environments.md:263` — `- https://vitest.dev/guide/environment.html`
- `.agents/skills/vitest/references/advanced-projects.md:212` — `apiUrl: 'https://staging.api.com',`
- `.agents/skills/vitest/references/advanced-projects.md:221` — `apiUrl: 'https://api.com',`
- `.agents/skills/vitest/references/advanced-projects.md:299` — `- https://vitest.dev/guide/projects.html`
- `.agents/skills/vitest/references/advanced-type-testing.md:235` — `- https://vitest.dev/guide/testing-types.html`
- `.agents/skills/vitest/references/advanced-type-testing.md:236` — `- https://vitest.dev/api/expect-typeof.html`
- `.agents/skills/vitest/references/advanced-vi.md:248` — `- https://vitest.dev/api/vi.html`
- `.agents/skills/vitest/references/core-cli.md:165` — `- https://vitest.dev/guide/cli.html`
- `.agents/skills/vitest/references/core-config.md:172` — `- https://vitest.dev/guide/#configuring-vitest`

**FINDING: 🔵 Pattern of Concern**

Anti-patterns detected showing unencrypted HTTP connections in development configurations, creating risk patterns consistent with non-compliance under HIPAA Security Rule 45 CFR §164.312(e)(1). Multiple files contain HTTP URLs including localhost configurations in advanced-environments.md:26, advanced-environments.md:87, features-mocking.md:122, and DEVELOPERS.md:89-91. However, production API endpoints in advanced-projects.md:212 and advanced-projects.md:221 properly use HTTPS, and no specific PHI transmission code was identified in the repository.

**REMEDIATION DIRECTION**

Replace all HTTP URLs with HTTPS equivalents throughout the codebase, including development and testing configurations. Implement configuration management that enforces HTTPS-only connections across all environments. Add code review processes to prevent HTTP URLs from being committed to the repository. Ensure any PHI transmission uses TLS 1.2 or higher encryption consistent with NIST guidelines, and consider implementing automated security scanning to detect unencrypted connection patterns.

---

### HIPAA-004: Access Controls and Authentication

**LEGAL QUESTION**

Does the system implement technical policies and procedures for electronic information systems that maintain electronic Protected Health Information to allow access only to those persons or software programs that have been granted access rights as specified in 45 CFR §164.312(a)(1)?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.312(a)(1); 45 CFR §164.312(a)(2)(i)

**EVIDENCE**

- `.agents/skills/vitest/references/core-describe.md:40` — `test('shows login page', () => {})`
- `.agents/skills/vitest/references/features-filtering.md:30` — `vitest -t "login"`
- `.agents/skills/vitest/references/features-filtering.md:183` — `vitest user -t "login" --changed`
- `.claude/settings.json:3` — `"SessionStart": [`
- `.claude/skills/e2e-studio-tests/SKILL.md:72` — `1. **`getByRole` with accessible name** - Most robust, tests accessibility`
- `.claude/skills/e2e-studio-tests/SKILL.md:74` — `page.getByRole('button', { name: 'Save' })`
- `.claude/skills/e2e-studio-tests/SKILL.md:75` — `page.getByRole('button', { name: 'Configure API privileges' })`
- `.claude/skills/e2e-studio-tests/SKILL.md:104` — `element.locator('..').getByRole('button')`
- `.claude/skills/e2e-studio-tests/SKILL.md:111` — `popover.getByRole('combobox')`
- `.claude/skills/e2e-studio-tests/SKILL.md:127` — `page.getByRole('button', { name: 'Configure API privileges' })`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under 45 CFR §164.312(a)(1). While the repository contains references to authentication concepts like login tests and permission-related naming conventions (hasPermission, canEdit), no actual implementation of technical access controls or authentication mechanisms for electronic Protected Health Information systems was found. The evidence consists primarily of test documentation and coding guidelines rather than functional access control implementations.

**REMEDIATION DIRECTION**

Implement comprehensive technical access controls including user authentication systems, role-based access control (RBAC), session management, and authorization mechanisms that restrict access to electronic PHI. This should include actual code implementing login/logout functionality, user role validation, permission checking before data access, and audit logging of access attempts. The current test references and naming conventions need to be backed by functional security controls that enforce the principle of least privilege access to PHI.

---

### HIPAA-005: Session Management

**LEGAL QUESTION**

Does the system implement electronic procedures that terminate an electronic session after a predetermined time of inactivity, as required for PHI-accessing interfaces under the HIPAA Security Rule?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.312(a)(2)(iii)

**EVIDENCE**

- `.agents/skills/vitest/references/advanced-projects.md:133` — `testTimeout: 10000,`
- `.agents/skills/vitest/references/advanced-vi.md:106` — `setTimeout(() => console.log('done'), 1000)`
- `.agents/skills/vitest/references/advanced-vi.md:172` — `}, { timeout: 5000, interval: 100 })`
- `.agents/skills/vitest/references/advanced-vi.md:177` — `{ timeout: 5000 }`
- `.agents/skills/vitest/references/advanced-vi.md:205` — `testTimeout: 10_000,`
- `.agents/skills/vitest/references/advanced-vi.md:206` — `hookTimeout: 10_000,`
- `.agents/skills/vitest/references/core-cli.md:160` — `- Both camelCase (`--testTimeout`) and kebab-case (`--test-timeout`) work`
- `.agents/skills/vitest/references/core-config.md:76` — `// Test timeout in ms`
- `.agents/skills/vitest/references/core-config.md:77` — `testTimeout: 5000,`
- `.agents/skills/vitest/references/core-config.md:79` — `// Hook timeout in ms`

**FINDING: 🔴 High Risk**

No evidence was found of electronic session termination procedures for user interfaces that could access PHI, creating a risk pattern consistent with non-compliance under HIPAA Security Rule 45 CFR §164.312(a)(2)(iii). The evidence shows only test framework timeout configurations in Vitest documentation files (e.g., testTimeout values in .agents/skills/vitest/references/), which are unrelated to user session management. This Supabase platform repository lacks the required automatic session timeout mechanisms for PHI-accessing interfaces.

**REMEDIATION DIRECTION**

Implement automatic session timeout functionality for all user-facing interfaces that could potentially access PHI. This should include configurable inactivity timeouts (typically 15-30 minutes), automatic session termination, and user notification before timeout. Add session management middleware that tracks user activity, monitors idle time, and terminates sessions when predetermined inactivity thresholds are exceeded. Document the timeout policies and ensure they apply consistently across all authentication-required interfaces in the platform.

---

### HIPAA-006: Audit Logging

**LEGAL QUESTION**

Does the system implement hardware, software, and procedural mechanisms that record and examine activity in information systems that contain or use electronic Protected Health Information, as required under the audit controls standard?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.312(b)

**EVIDENCE**

- `.gitignore:141` — `# For self-hosted logs: https://github.com/supabase/supabase/blob/86e3ab20abfdb9c3e666334d3d2f8efeef9ccf2c/docker/docker`
- `apps/docs/app/api/graphql/route.test.ts:3` — `vi.mock('~/lib/logger', async () => {`
- `apps/docs/app/api/graphql/route.test.ts:4` — `const actual = await vi.importActual<typeof import('~/lib/logger')>('~/lib/logger')`
- `apps/docs/app/api/graphql/route.ts:16` — `import { LOGGING_CODES, sendToLogflare } from '~/lib/logger'`
- `apps/docs/app/api/graphql/route.ts:257` — `sendToLogflare(LOGGING_CODES.CONTENT_API_REQUEST_RECEIVED, {`
- `apps/docs/app/api/graphql/route.ts:16` — `import { LOGGING_CODES, sendToLogflare } from '~/lib/logger'`
- `apps/docs/components/AuthSmsProviderConfig/MessageBirdConfig.mdx:22` — `Start by logging into your MessageBird account and verify the mobile number you'll be using to test with [here](https://`
- `apps/docs/components/AuthSmsProviderConfig/TwilioConfig.mdx:57` — `Start by logging into your Twilio account and starting a new project: https://www.twilio.com/console/projects/create`
- `apps/docs/components/AuthSmsProviderConfig/VonageConfig.mdx:18` — `Start by logging into your Vonage Dashboard at https://dashboard.nexmo.com/`
- `apps/docs/components/Navigation/NavigationMenu/NavigationMenu.constants.ts:901` — `{ name: 'Audit Logs', url: '/guides/auth/audit-logs', enabled: authFullSecurityEnabled },`

**FINDING: 🟠 Medium Risk**

Evidence shows partial implementation of audit logging mechanisms with a risk pattern consistent with non-compliance under HIPAA Security Rule 45 CFR §164.312(b). While logging infrastructure exists (sendToLogflare function in apps/docs/app/api/graphql/route.ts:16 and LOGGING_CODES constants), and documentation references audit capabilities (audit logs navigation in NavigationMenu.constants.ts:901 and PGAudit extension at line 1207), there is no concrete evidence that these mechanisms specifically record and examine activity involving electronic Protected Health Information as required by the audit controls standard.

**REMEDIATION DIRECTION**

Implement comprehensive audit logging that specifically captures all access, creation, modification, and deletion of electronic PHI. Configure the existing logging infrastructure (sendToLogflare) to record user authentication events, data access patterns, system configuration changes, and security incidents. Ensure audit logs include required data elements like user identification, event type, date/time, success/failure status, and data accessed. Establish procedures for regular log review and analysis, and document how the PGAudit extension and platform audit logs specifically monitor PHI-related activities.

---

### HIPAA-007: Minimum Necessary Access

**LEGAL QUESTION**

Does the system limit the Protected Health Information disclosed or accessed to the minimum necessary to accomplish the intended purpose, consistent with the minimum necessary standard under the Privacy Rule?

**REGULATORY STANDARD**

HIPAA Privacy Rule 45 CFR §164.502(b); 45 CFR §164.514(d)

**EVIDENCE**

- `.agents/skills/vitest/SKILL.md:15` — `- Smart watch mode: Only reruns affected tests based on module graph`
- `.agents/skills/vitest/SKILL.md:29` — `| Test API | test/it function, modifiers like skip, only, concurrent | [core-test-api](references/core-test-api.md) |`
- `.agents/skills/vitest/references/advanced-environments.md:229` — `classNameStrategy: 'non-scoped',`
- `.agents/skills/vitest/references/advanced-projects.md:195` — `# Exclude project`
- `.agents/skills/vitest/references/advanced-type-testing.md:32` — `// Only type check`
- `.agents/skills/vitest/references/advanced-type-testing.md:33` — `only: false,`
- `.agents/skills/vitest/references/advanced-type-testing.md:199` — `# Type tests only`
- `.agents/skills/vitest/references/advanced-type-testing.md:200` — `vitest --typecheck.only`
- `.agents/skills/vitest/references/advanced-type-testing.md:226` — `- Use `.test-d.ts` for type-only tests`
- `.agents/skills/vitest/references/advanced-vi.md:117` — `vi.runOnlyPendingTimers()`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under HIPAA Privacy Rule 45 CFR §164.502(b) and §164.514(d). No specific Protected Health Information (PHI) access controls or minimum necessary restrictions were found in the codebase. The only references to "minimum" or "only" access patterns relate to testing frameworks and development tools rather than healthcare data protection mechanisms.

**REMEDIATION DIRECTION**

Implement role-based access controls that limit PHI disclosure to the minimum necessary for each user's job function. Add data filtering mechanisms that restrict query results based on user permissions and purpose of access. Create audit logging for all PHI access attempts and establish documentation of minimum necessary determinations for different user roles and access scenarios. Consider implementing field-level security controls that automatically mask or exclude unnecessary PHI elements from API responses and database queries.

---

### HIPAA-008: Business Associate Agreements

**LEGAL QUESTION**

Does the system integrate with third-party services that may receive, maintain, or transmit Protected Health Information, and if so, is there evidence that Business Associate Agreement requirements are addressed in the code or configuration?

**REGULATORY STANDARD**

HIPAA Privacy Rule 45 CFR §164.502(e); 45 CFR §164.504(e)

**EVIDENCE**

- `.agents/skills/vitest/SKILL.md:27` — `| Configuration | Vitest and Vite config integration, defineConfig usage | [core-config](references/core-config.md) |`
- `.agents/skills/vitest/references/advanced-projects.md:30` — `name: 'integration',`
- `.agents/skills/vitest/references/advanced-projects.md:31` — `include: ['tests/integration/**/*.test.ts'],`
- `.agents/skills/vitest/references/advanced-projects.md:190` — `vitest --project integration`
- `.agents/skills/vitest/references/core-config.md:152` — `name: 'integration',`
- `.agents/skills/vitest/references/core-config.md:153` — `include: ['tests/integration/**/*.test.ts'],`
- `.agents/skills/vitest/references/core-expect.md:213` — `- Use context's `expect` in concurrent tests for correct tracking`
- `.agents/skills/vitest/references/features-coverage.md:171` — `## CI Integration`
- `.agents/skills/vitest/references/features-filtering.md:109` — `test('slow test', { tags: ['slow', 'integration'] }, () => {})`
- `.agents/skills/vitest/references/features-filtering.md:125` — `tags: ['db', 'slow', 'integration'],`

**FINDING: 🔴 High Risk**

The evidence shows integration with third-party services including PostHog event tracking (as documented in .claude/skills/telemetry-standards/SKILL.md) and multiple system integrations referenced throughout the Vitest configuration files. However, no evidence was found of Business Associate Agreement (BAA) requirements being addressed in the code or configuration for these third-party integrations. This creates a risk pattern consistent with non-compliance under HIPAA Privacy Rule 45 CFR §164.502(e) and §164.504(e), which require covered entities to ensure BAAs are in place before PHI can be disclosed to business associates.

**REMEDIATION DIRECTION**

Implement a systematic approach to identify all third-party services that may receive, maintain, or transmit PHI, starting with the documented PostHog integration and any other external services. Create configuration management processes that enforce BAA validation before enabling third-party integrations. Add code comments or configuration flags that document BAA compliance status for each integration, and establish a review process to ensure new third-party integrations cannot process PHI without proper BAA coverage being verified and documented in the system.

---

### HIPAA-009: Data Retention and Disposal

**LEGAL QUESTION**

Does the system implement policies and procedures to address the final disposition of electronic Protected Health Information and the hardware or electronic media on which it is stored, as well as removal of PHI before media is available for reuse?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.310(d)(2)(i); 45 CFR §164.310(d)(2)(ii)

**EVIDENCE**

- `.agents/skills/vitest/references/advanced-environments.md:156` — `delete globalThis.myGlobal`
- `.agents/skills/vitest/references/advanced-vi.md:98` — `await vi.dynamicImportSettled()`
- `.agents/skills/vitest/references/core-hooks.md:30` — `await cleanupMocks()`
- `.agents/skills/vitest/references/core-hooks.md:34` — `## Cleanup Return Pattern`
- `.agents/skills/vitest/references/core-hooks.md:36` — `Return cleanup function from `before*` hooks:`
- `.agents/skills/vitest/references/core-hooks.md:143` — `test('with cleanup', () => {`
- `.agents/skills/vitest/references/core-hooks.md:158` — `### Reusable Cleanup Pattern`
- `.agents/skills/vitest/references/core-hooks.md:236` — `- Return cleanup function from `before*` to avoid `after*` duplication`
- `.agents/skills/vitest/references/features-context.md:54` — `await db.deleteUser(user.id)`
- `.agents/skills/vitest/references/features-context.md:25` — `- `onTestFinished(fn)` - Cleanup after test`

**FINDING: 🔴 High Risk**

The evidence reveals a risk pattern consistent with non-compliance under HIPAA Security Rule 45 CFR §164.310(d)(2)(i) and (ii). While the repository contains numerous references to data cleanup and deletion operations in testing contexts (such as `.agents/skills/vitest/references/core-hooks.md` and database cleanup patterns), no evidence was found of formal policies, procedures, or implementation for the final disposition of electronic Protected Health Information or secure media sanitization before reuse. The identified cleanup operations appear limited to development and testing scenarios rather than production PHI disposal requirements.

**REMEDIATION DIRECTION**

Implement comprehensive data retention and disposal policies that specifically address PHI final disposition. This should include: automated secure deletion procedures for PHI when retention periods expire, documented media sanitization processes before hardware reuse or disposal, audit logging of all PHI disposal activities, and technical controls to ensure complete data removal from storage media. Consider implementing cryptographic erasure techniques and establishing clear procedures for both logical data deletion and physical media destruction when appropriate.

---

### HIPAA-010: Breach Detection and Emergency Access

**LEGAL QUESTION**

Does the system implement procedures for detecting, reporting, and responding to suspected or known security incidents involving electronic Protected Health Information, and does it provide for emergency access to PHI during system disruptions?

**REGULATORY STANDARD**

HIPAA Security Rule 45 CFR §164.308(a)(6); 45 CFR §164.312(a)(2)(ii)

**EVIDENCE**

- `.agents/skills/vitest/references/advanced-vi.md:35` — `fn.mockRestore()  // Restore original (for spies)`
- `.agents/skills/vitest/references/advanced-vi.md:126` — `// Restore`
- `.agents/skills/vitest/references/advanced-vi.md:217` — `vi.restoreAllMocks() // Restore originals (spies)`
- `.agents/skills/vitest/references/core-config.md:109` — `// Restore mocks between tests`
- `.agents/skills/vitest/references/core-config.md:110` — `restoreMocks: true,`
- `.agents/skills/vitest/references/features-context.md:137` — `Override fixtures per project:`
- `.agents/skills/vitest/references/features-context.md:162` — `Override fixture for specific suite:`
- `.agents/skills/vitest/references/features-mocking.md:51` — `// Restore original`
- `.agents/skills/vitest/references/features-mocking.md:52` — `spy.mockRestore()`
- `.agents/skills/vitest/references/features-mocking.md:181` — `vi.useRealTimers() // Restore`

**FINDING: 🔴 High Risk**

No evidence was found of security incident detection, reporting, or response procedures for electronic Protected Health Information. Additionally, no emergency access procedures for PHI during system disruptions were identified in the codebase. The evidence consists entirely of testing framework documentation related to mock restoration in Vitest files and a single backup button telemetry reference, which do not constitute the required security incident management or emergency access controls. This presents a risk pattern consistent with non-compliance under HIPAA Security Rule 45 CFR §164.308(a)(6) and §164.312(a)(2)(ii).

**REMEDIATION DIRECTION**

Implement comprehensive security incident detection and response procedures including automated monitoring for PHI breaches, incident logging and alerting systems, documented response workflows, and reporting mechanisms to appropriate parties. Additionally, establish emergency access procedures that allow authorized personnel to access PHI during system outages while maintaining audit trails and access controls. These should include break-glass access protocols, emergency user provisioning procedures, and documentation of all emergency access events for subsequent review.

---

## PCI-DSS Findings

### PCIDSS-001: Cardholder Data Storage and Protection

**LEGAL QUESTION**

Does this system store, process, or transmit cardholder data including primary account numbers (PAN), and if so, are adequate protections in place to render stored PAN unreadable, as required under PCI DSS Requirement 3.5?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 3.5 (PAN Storage Protection)

**EVIDENCE**

- `.claude/skills/e2e-studio-tests/SKILL.md:80` — `page.getByTestId('table-editor-side-panel')`
- `.claude/skills/e2e-studio-tests/SKILL.md:135` — `// Good - scoped to side panel`
- `.claude/skills/e2e-studio-tests/SKILL.md:136` — `const sidePanel = page.getByTestId('table-editor-side-panel')`
- `.claude/skills/e2e-studio-tests/SKILL.md:137` — `const toggle = sidePanel.getByRole('switch')`
- `.claude/skills/studio-testing/SKILL.md:89` — `For the complete guide with all rules expanded: `AGENTS.md``
- `.claude/skills/vercel-composition-patterns/SKILL.md:89` — `For the complete guide with all rules expanded: `AGENTS.md``
- `.cursor/rules/studio/best-practices/RULE.md:95` — `<UserSettingsPanel />`
- `.cursor/rules/studio/best-practices/RULE.md:107` — `├── UserPanel.tsx`
- `.cursor/rules/studio/best-practices/RULE.md:128` — `const PanelTab = ({ value, children }: { value: string; children: ReactNode }) => (`
- `.cursor/rules/studio/forms/RULE.md:2` — `description: "Studio: form patterns (page layouts + side panels) and react-hook-form conventions"`

**FINDING: 🟢 No Issue Found**

The evidence searched does not contain any cardholder data storage, processing, or transmission functionality. The repository appears to be the Supabase open-source project focused on database platform development, with evidence showing only UI testing patterns, form components, and development tooling. No primary account numbers (PAN) or payment card processing code was identified in the analyzed files.

**REMEDIATION DIRECTION**

No remediation required at this time. However, if this system will be extended to handle payment card data in the future, ensure PCI DSS Requirement 3.5 compliance by implementing strong cryptography and security protocols to render stored PAN unreadable, such as encryption with proper key management or tokenization systems.

---

### PCIDSS-002: Encryption of Card Data in Transit and at Rest

**LEGAL QUESTION**

Is cardholder data encrypted using strong cryptography during transmission over open public networks and when stored at rest, consistent with PCI DSS Requirements 3.5 and 4.2?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirements 3.5 (Encryption at Rest); 4.2 (Encryption in Transit)

**EVIDENCE**

- `.agents/skills/vitest/SKILL.md:7` — `source: Generated from https://github.com/vitest-dev/vitest, scripts located at https://github.com/antfu/skills`
- `.agents/skills/vitest/references/advanced-environments.md:263` — `- https://vitest.dev/guide/environment.html`
- `.agents/skills/vitest/references/advanced-projects.md:212` — `apiUrl: 'https://staging.api.com',`
- `.agents/skills/vitest/references/advanced-projects.md:221` — `apiUrl: 'https://api.com',`
- `.agents/skills/vitest/references/advanced-projects.md:299` — `- https://vitest.dev/guide/projects.html`
- `.agents/skills/vitest/references/advanced-type-testing.md:235` — `- https://vitest.dev/guide/testing-types.html`
- `.agents/skills/vitest/references/advanced-type-testing.md:236` — `- https://vitest.dev/api/expect-typeof.html`
- `.agents/skills/vitest/references/advanced-vi.md:248` — `- https://vitest.dev/api/vi.html`
- `.agents/skills/vitest/references/core-cli.md:165` — `- https://vitest.dev/guide/cli.html`
- `.agents/skills/vitest/references/core-config.md:172` — `- https://vitest.dev/guide/#configuring-vitest`

**FINDING: 🔴 High Risk**

Analysis reveals a risk pattern consistent with non-compliance under PCI DSS Requirements 3.5 and 4.2. No evidence was found demonstrating encryption of cardholder data at rest or in transit using strong cryptography. Additionally, multiple anti-patterns were detected including unencrypted HTTP URLs in development configurations (.agents/skills/vitest/references/advanced-environments.md:26, features-mocking.md:122) and base64 encoding of sensitive keys in GitHub workflows (.github/workflows/docs-sync-auto-troubleshooting.yml:41).

**REMEDIATION DIRECTION**

Implement strong encryption (AES-256 minimum) for all cardholder data at rest in databases and file systems. Ensure all cardholder data transmission occurs over encrypted channels (TLS 1.2+ with strong cipher suites). Replace all HTTP URLs with HTTPS equivalents in production configurations. Remove base64 encoding of private keys in CI/CD pipelines and implement proper secrets management. Conduct a comprehensive audit to identify all locations where cardholder data is processed, stored, or transmitted to ensure complete cryptographic protection coverage.

---

### PCIDSS-003: Access Control to Cardholder Data

**LEGAL QUESTION**

Does the system restrict access to cardholder data to only those individuals and systems whose job requires such access, implementing role-based access controls consistent with PCI DSS Requirement 7?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 7 (Restrict Access by Business Need to Know)

**EVIDENCE**

- `.claude/skills/e2e-studio-tests/SKILL.md:72` — `1. **`getByRole` with accessible name** - Most robust, tests accessibility`
- `.claude/skills/e2e-studio-tests/SKILL.md:74` — `page.getByRole('button', { name: 'Save' })`
- `.claude/skills/e2e-studio-tests/SKILL.md:75` — `page.getByRole('button', { name: 'Configure API privileges' })`
- `.claude/skills/e2e-studio-tests/SKILL.md:104` — `element.locator('..').getByRole('button')`
- `.claude/skills/e2e-studio-tests/SKILL.md:111` — `popover.getByRole('combobox')`
- `.claude/skills/e2e-studio-tests/SKILL.md:127` — `page.getByRole('button', { name: 'Configure API privileges' })`
- `.claude/skills/e2e-studio-tests/SKILL.md:137` — `const toggle = sidePanel.getByRole('switch')`
- `.claude/skills/e2e-studio-tests/SKILL.md:141` — `const roleSection = popover.getByText('Anonymous (anon)', { exact: true })`
- `.claude/skills/studio-testing/rules/testing-component-tests-ui-only.md:52` — `await userEvent.click(screen.getByRole('button'))`
- `.claude/skills/studio-testing/rules/testing-component-tests-ui-only.md:66` — `await userEvent.click(screen.getByRole('button'))`

**FINDING: 🟠 Medium Risk**

The evidence shows permission-based access controls are implemented in the codebase, with functions like `useAsyncCheckPermissions`, `canUpdateColumns`, `canDelete`, and conditional rendering based on permission checks (lines 45-46, 175, 187, 239-240 in .cursor/rules/studio/best-practices/RULE.md). However, no specific evidence was found demonstrating role-based access controls specifically for cardholder data protection, creating a risk pattern consistent with non-compliance under PCI DSS Requirement 7.

**REMEDIATION DIRECTION**

Implement and document role-based access controls specifically for cardholder data access. Create distinct roles with minimum necessary privileges for cardholder data handling, ensure all cardholder data access points use role-based validation (not just generic permissions), and add audit logging for cardholder data access attempts. The existing permission framework appears suitable but needs cardholder-data-specific implementation and documentation to demonstrate compliance with the "need to know" principle.

---

### PCIDSS-004: Network Segmentation

**LEGAL QUESTION**

Does the system implement network segmentation to isolate the cardholder data environment (CDE) from other network segments, reducing the scope of PCI DSS compliance as described in Requirement 1?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 1 (Network Security Controls)

**EVIDENCE**

- `.claude/skills/studio-testing/rules/testing-exhaustive-permutations.md:4` — `impactDescription: catches edge cases and regressions in business logic`
- `apps/docs/app/guides/functions/[[...slug]]/page.tsx:12` — `const FunctionsGuidePage = async (props: { params: Promise<Params> }) => {`
- `apps/docs/app/guides/functions/[[...slug]]/page.tsx:25` — `export default FunctionsGuidePage`
- `apps/docs/app/guides/integrations/[[...slug]]/page.tsx:12` — `const IntegrationsGuidePage = async (props: { params: Promise<Params> }) => {`
- `apps/docs/app/guides/integrations/[[...slug]]/page.tsx:25` — `export default IntegrationsGuidePage`
- `apps/docs/components/Navigation/NavigationMenu/NavigationMenu.constants.ts:1965` — `name: 'Bandwidth & Storage Egress',`
- `apps/docs/components/Navigation/NavigationMenu/NavigationMenu.constants.ts:2637` — `name: 'Egress',`
- `apps/docs/components/Navigation/NavigationMenu/NavigationMenu.constants.ts:2638` — `url: '/guides/platform/manage-your-usage/egress' as `/${string}`,`
- `apps/docs/content/guides/ai/hugging-face.mdx:35` — `- [Image segmentation](https://huggingface.co/tasks/image-segmentation)`
- `apps/docs/content/guides/auth/auth-captcha.mdx:186` — `To test locally, you will need to add localhost to the domain allowlist as per the [Cloudflare docs](https://developers.`

**FINDING: 🔴 High Risk**

The code repository shows a risk pattern consistent with non-compliance under PCI DSS v4.0 Requirement 1. No evidence of network segmentation controls, firewall configurations, or cardholder data environment (CDE) isolation was found in the examined codebase. While some IP-based access controls are documented in authentication hooks (apps/docs/content/guides/auth/auth-hooks/before-user-created-hook.mdx:346-417), these appear to be application-level controls rather than network segmentation infrastructure required for CDE isolation.

**REMEDIATION DIRECTION**

Implement proper network segmentation architecture to isolate any cardholder data environment from other network segments. This requires deploying network firewalls, configuring network access control lists (ACLs), and establishing secure network zones with restricted communication paths. Document the network topology, firewall rules, and segmentation controls in your infrastructure-as-code or network configuration files. If this system does not process, store, or transmit cardholder data, clearly document the scope exclusion to reduce PCI DSS compliance requirements.

---

### PCIDSS-005: Vulnerability Management

**LEGAL QUESTION**

Does the system demonstrate evidence of vulnerability management practices including regular patching, dependency updates, and vulnerability scanning, consistent with PCI DSS Requirement 6?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 6 (Develop and Maintain Secure Systems)

**EVIDENCE**

- `.agents/skills/vitest/SKILL.md:30` — `| Describe API | describe/suite for grouping tests and nested suites | [core-describe](references/core-describe.md) |`
- `.agents/skills/vitest/references/advanced-vi.md:234` — `// Partial mock typing`
- `.agents/skills/vitest/references/core-describe.md:3` — `description: describe/suite for grouping tests into logical blocks`
- `.agents/skills/vitest/references/core-expect.md:214` — `- `toThrow` requires wrapping sync code in a function`
- `.agents/skills/vitest/references/features-filtering.md:203` — `- Tags provide semantic test grouping`
- `.claude/skills/e2e-studio-tests/SKILL.md:110` — `// Could consider scoping down the container or filtering the combobox more specifically`
- `.claude/skills/studio-error-handling/SKILL.md:26` — `| `ErrorMatcher.tsx`                    | Component — reads `errorType`, looks up mapping, renders         |`
- `.claude/skills/studio-error-handling/SKILL.md:27` — `| `error-mappings.tsx`                  | `Record<KnownErrorType, { id, Troubleshooting: ComponentType }>` |`
- `.claude/skills/studio-error-handling/SKILL.md:28` — `| `errorMappings/ConnectionTimeout.tsx` | Reference troubleshooting component                              |`
- `.claude/skills/studio-error-handling/SKILL.md:47` — `- Do not put regex patterns in `error-mappings.tsx` — they belong in `data/error-patterns.ts`.`

**FINDING: 🔴 High Risk**

No evidence of vulnerability management practices was found in the code repository. The evidence consists entirely of testing framework documentation, UI component patterns, and development guidelines, with no indication of vulnerability scanning tools, dependency update procedures, security patching processes, or automated security testing. This absence represents a risk pattern consistent with non-compliance under PCI DSS v4.0 Requirement 6, which mandates systematic vulnerability management for systems handling cardholder data.

**REMEDIATION DIRECTION**

Implement comprehensive vulnerability management practices including: automated dependency vulnerability scanning (tools like Snyk, OWASP Dependency Check), regular security patching procedures with documented schedules, integration of security testing into CI/CD pipelines, and maintenance of a vulnerability remediation workflow. Add configuration files for these tools to the repository and establish documented procedures for addressing identified vulnerabilities within required timeframes per PCI DSS requirements.

---

### PCIDSS-006: Security Testing Evidence

**LEGAL QUESTION**

Does the system implement security testing controls including code review, static analysis, and penetration testing practices, as required under PCI DSS Requirement 6.3 and 11.4?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirements 6.3 (Security Vulnerabilities); 11.4 (Penetration Testing)

**EVIDENCE**

- `.agents/skills/vitest/references/core-cli.md:39` — `Run tests that import specific files (useful with lint-staged):`
- `.agents/skills/vitest/references/core-cli.md:159` — `- Use `--run` flag to ensure single run (important for lint-staged)`
- `.agents/skills/vitest/references/core-describe.md:119` — `## Parameterized Suites`
- `.agents/skills/vitest/references/core-test-api.md:122` — `## Parameterized Tests`
- `.agents/skills/vitest/references/features-filtering.md:59` — `Useful with lint-staged:`
- `.agents/skills/vitest/references/features-filtering.md:62` — `// .lintstagedrc.js`
- `.agents/skills/vitest/references/features-snapshots.md:158` — `escapeString: false,`
- `.claude/skills/studio-testing/rules/testing-component-tests-ui-only.md:64` — `test('closes on Escape key', async () => {`
- `.claude/skills/studio-testing/rules/testing-component-tests-ui-only.md:67` — `await userEvent.keyboard('{Escape}')`
- `.claude/skills/studio-testing/rules/testing-e2e-shared-features.md:15` — `- Mouse/click interactions AND keyboard shortcuts (Tab, Enter, Escape, Arrow keys)`

**FINDING: 🟠 Medium Risk**

The repository demonstrates partial security testing controls with evidence of unit testing frameworks (Vitest) and some security-aware testing practices including XSS payload testing referenced in `.claude/skills/studio-testing/rules/testing-exhaustive-permutations.md:19` and input sanitization testing in `.claude/skills/studio-testing/rules/testing-extract-logic.md`. However, no evidence of formal static code analysis tools, structured code review processes, or penetration testing procedures was found, creating a risk pattern consistent with non-compliance under PCI DSS Requirements 6.3 and 11.4. Additionally, multiple instances of potentially unsafe code patterns were detected, including `dangerouslySetInnerHTML` usage in production files and `innerHTML` manipulation.

**REMEDIATION DIRECTION**

Implement a comprehensive security testing program that includes: (1) automated static application security testing (SAST) tools integrated into the CI/CD pipeline to catch vulnerabilities like the detected unsafe DOM manipulation patterns, (2) formal code review requirements with security checklists before production deployment, and (3) documented penetration testing procedures with regular execution schedules. Address the identified anti-patterns by replacing `dangerouslySetInnerHTML` with safer alternatives and implementing proper input sanitization for all dynamic content rendering.

---

### PCIDSS-007: Audit Logging of Card Data Access

**LEGAL QUESTION**

Does the system implement audit trail mechanisms that record all individual access to cardholder data, all actions taken by any individual with root or administrative privileges, and all access to audit trails, as required under PCI DSS Requirement 10?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 10 (Log and Monitor All Access)

**EVIDENCE**

- `.gitignore:141` — `# For self-hosted logs: https://github.com/supabase/supabase/blob/86e3ab20abfdb9c3e666334d3d2f8efeef9ccf2c/docker/docker`
- `apps/design-system/app/fonts/CustomFont-Medium.woff2:123` — `(\Z]o˙OFCk:v3hyG_% 71J}?ąrm&o]{+M͔*^8~=ELkDag5`;fגjq/EiQVp_w؞\9,mI?[;s70VSg 3ob;1ɓ|H52ז,Lm6lAA}8C>peu`
- `apps/design-system/content/docs/components/chart.mdx:431` — `Use `labelKey` and `nameKey` to use a custom key for the tooltip label and name.`
- `apps/design-system/content/docs/components/chart.mdx:449` — `| `labelKey`      | string                   | The config or data key to use for the label. |`
- `apps/design-system/content/docs/components/chart.mdx:461` — `To use a custom key for tooltip label and names, use the `labelKey` and `nameKey` props.`
- `apps/design-system/content/docs/components/chart.mdx:485` — `<ChartTooltip content={<ChartTooltipContent labelKey="visitors" nameKey="browser" />} />`
- `apps/design-system/registry/default/example/chart-tooltip-demo.tsx:134` — `labelKey?: string`
- `apps/docs/app/api/graphql/route.test.ts:3` — `vi.mock('~/lib/logger', async () => {`
- `apps/docs/app/api/graphql/route.test.ts:4` — `const actual = await vi.importActual<typeof import('~/lib/logger')>('~/lib/logger')`
- `apps/docs/app/api/graphql/route.ts:16` — `import { LOGGING_CODES, sendToLogflare } from '~/lib/logger'`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under PCI DSS v4.0 Requirement 10. While the codebase contains references to logging infrastructure (apps/docs/app/api/graphql/route.ts:257 with sendToLogflare function) and audit-related documentation navigation elements (apps/docs/components/Navigation/NavigationMenu/NavigationMenu.constants.ts:901, 1207, 2439), there is no concrete evidence of implemented audit trail mechanisms that specifically record individual access to cardholder data, administrative privilege actions, or audit trail access monitoring as mandated by the standard.

**REMEDIATION DIRECTION**

Implement comprehensive audit logging that captures: (1) all individual access attempts and actions involving cardholder data with user identification, timestamps, and data elements accessed; (2) all actions performed by users with root or administrative privileges including authentication attempts, privilege escalations, and system configuration changes; (3) all access to audit logs themselves including who accessed them and when. Ensure logs are tamper-evident, stored securely, and include sufficient detail for forensic analysis. The existing logging infrastructure in the GraphQL route could serve as a foundation, but needs expansion to cover all PCI DSS-required events with appropriate data classification and retention policies.

---

### PCIDSS-008: Key Management Practices

**LEGAL QUESTION**

Does the system implement cryptographic key management procedures including key generation, distribution, storage, rotation, and destruction, consistent with PCI DSS Requirement 3.6 and 3.7?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirements 3.6 (Key Management Procedures); 3.7 (Key Management Policies)

**EVIDENCE**

- `apps/design-system/app/fonts/CustomFont-Black.woff2:212` — `"#dWpd?zL+^G§kS[h(ԭ/t!aOuld]F" מ̢!o._->[BkzO8Rf$ZC/XE"usMkmS-hXᝁ]2.0)l[`
- `apps/docs/app/api/revalidate/route.utils.ts:27` — `const overrideKeys = process.env.DOCS_REVALIDATION_OVERRIDE_KEYS?.split(/\s*,\s*/) ?? []`
- `apps/docs/app/api/revalidate/route.utils.ts:28` — `if (basicKeys.length === 0 && overrideKeys.length === 0) {`
- `apps/docs/app/api/revalidate/route.utils.ts:37` — `if (overrideKeys.includes(token)) {`
- `apps/docs/components/AuthSmsProviderConfig/AuthSmsProviderConfig.tsx:24` — `const AuthSmsProviderConfig = () => {`
- `apps/docs/components/AuthSmsProviderConfig/AuthSmsProviderConfig.tsx:89` — `export default AuthSmsProviderConfig`
- `apps/docs/components/AuthSmsProviderConfig/MessageBirdConfig.mdx:2` — `import { CostWarning } from './AuthSmsProviderConfig.Warnings'`
- `apps/docs/components/AuthSmsProviderConfig/TextLocalConfig.mdx:2` — `import { CostWarning } from './AuthSmsProviderConfig.Warnings'`
- `apps/docs/components/AuthSmsProviderConfig/TwilioConfig.mdx:2` — `import { CostWarning } from './AuthSmsProviderConfig.Warnings'`
- `apps/docs/components/AuthSmsProviderConfig/VonageConfig.mdx:2` — `import { CostWarning } from './AuthSmsProviderConfig.Warnings'`

**FINDING: 🔴 High Risk**

The evidence reveals significant risk patterns consistent with non-compliance under PCI DSS Requirements 3.6 and 3.7. While the system implements a Vault secrets management system (evidenced in apps/docs/content/guides/ai/automatic-embeddings.mdx), critical anti-patterns were detected including hardcoded API keys in design system examples (apps/design-system/registry/default/example/form-patterns-pagelayout.tsx:67 and form-patterns-sidepanel.tsx:64) and direct environment variable access for sensitive keys without proper key management controls (apps/docs/app/api/ai/docs/route.ts:35-37). No evidence was found of formal cryptographic key generation, rotation, or destruction procedures required by PCI DSS.

**REMEDIATION DIRECTION**

Implement a comprehensive cryptographic key management system that covers the full lifecycle: key generation using cryptographically secure methods, secure distribution mechanisms, encrypted storage with access controls, automated rotation schedules, and secure destruction procedures. Remove all hardcoded API keys from the codebase and replace with secure vault retrievals. Establish formal policies and procedures documenting key management practices, including role-based access controls for key operations. Integrate all key operations with the existing Vault system and implement audit logging for all key lifecycle events to ensure PCI DSS compliance.

---

### PCIDSS-009: Third Party Service Provider Controls

**LEGAL QUESTION**

Does the system manage third-party service providers that have access to cardholder data with appropriate controls, agreements, and monitoring, consistent with PCI DSS Requirement 12.8?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 12.8 (Third-Party Service Provider Management)

**EVIDENCE**

- `.agents/skills/vitest/SKILL.md:40` — `| Coverage | Code coverage with V8 or Istanbul providers | [features-coverage](references/features-coverage.md) |`
- `.agents/skills/vitest/SKILL.md:27` — `| Configuration | Vitest and Vite config integration, defineConfig usage | [core-config](references/core-config.md) |`
- `.agents/skills/vitest/references/advanced-environments.md:210` — `provider: 'playwright',`
- `.agents/skills/vitest/references/advanced-projects.md:119` — `provider: 'playwright',`
- `.agents/skills/vitest/references/advanced-projects.md:30` — `name: 'integration',`
- `.agents/skills/vitest/references/advanced-projects.md:31` — `include: ['tests/integration/**/*.test.ts'],`
- `.agents/skills/vitest/references/advanced-projects.md:190` — `vitest --project integration`
- `.agents/skills/vitest/references/advanced-vi.md:148` — `vi.stubEnv('API_KEY', 'test')`
- `.agents/skills/vitest/references/core-cli.md:89` — `--coverage.provider v8    # Use v8 provider`
- `.agents/skills/vitest/references/core-config.md:87` — `provider: 'v8', // or 'istanbul'`

**FINDING: 🔴 High Risk**

No evidence found of third-party service provider management controls, agreements, or monitoring mechanisms as required by PCI DSS Requirement 12.8. The repository contains only testing framework configuration files related to Vitest and coverage providers (V8, Istanbul, Playwright) in the .agents/skills/vitest/ directory, with no documentation or implementation of vendor management processes, due diligence procedures, or monitoring controls for third-party services that may access cardholder data. This represents a risk pattern consistent with non-compliance under PCI DSS v4.0 Requirement 12.8.

**REMEDIATION DIRECTION**

Implement a comprehensive third-party service provider management program that includes: formal written agreements with all service providers that handle cardholder data, documented due diligence processes for vetting providers' PCI DSS compliance status, regular monitoring and assessment procedures for ongoing compliance verification, and maintenance of an inventory of all third-party services with access to cardholder data environments. Create policies and procedures documents that define roles, responsibilities, and processes for managing these relationships throughout their lifecycle.

---

### PCIDSS-010: Incident Response for Card Data Breach

**LEGAL QUESTION**

Does the system implement an incident response plan that addresses suspected or confirmed cardholder data breaches, including detection, containment, and notification procedures, as required under PCI DSS Requirement 12.10?

**REGULATORY STANDARD**

PCI DSS v4.0 Requirement 12.10 (Incident Response Plan)

**EVIDENCE**

- `.cursor/rules/studio-useStaticEffectEvent.mdc:23` — `showNotification('Connected!', theme) // `theme` causes unwanted re-runs`
- `.cursor/rules/studio/RULE.md:32` — `- `studio/alerts``
- `.cursor/rules/studio/alerts/RULE.md:2` — `description: "Studio: alert/admonition usage and placement"`
- `.cursor/rules/studio/alerts/RULE.md:8` — `# Studio alerts`
- `.cursor/rules/studio/best-practices/RULE.md:154` — `return <AlertError error={error} subject="Failed to load data" />`
- `.cursor/rules/testing/e2e-studio/RULE.md:303` — `// ✅ Good - don't fail if API doesn't respond`
- `.github/instructions/studio-telemetry.instructions.md:15` — `3. **Feature-flagged rollouts without outcome tracking.** If a flag gates new behavior, there should be telemetry on bot`
- `.github/workflows/dashboard-pr-reminder.yml:44` — `run: pnpm tsx scripts/actions/find-stale-dashboard-prs.ts | pnpm tsx scripts/actions/send-slack-pr-notification.ts`
- `LICENSE:158` — `incidental, or consequential damages of any character arising as a`
- `SECURITY.md:26` — `- Do not run automated scanners on other customer projects. Running automated scanners can run up costs for our users. A`

**FINDING: 🔴 High Risk**

No evidence of a comprehensive incident response plan for cardholder data breaches was found in the repository. While the codebase contains basic notification mechanisms (showNotification calls, alert functions) and a general security reporting process in SECURITY.md with a 5-day response commitment, these do not constitute the formal incident response procedures required for suspected or confirmed card data breaches. This presents a risk pattern consistent with non-compliance under PCI DSS Requirement 12.10.

**REMEDIATION DIRECTION**

Implement a comprehensive incident response plan that specifically addresses cardholder data breaches. This should include documented procedures for detection (monitoring and alerting systems), containment (isolation protocols and access restrictions), assessment (breach scope determination), notification (internal escalation and external reporting to card brands/acquirers), and recovery processes. The plan should be stored in the repository as formal documentation with clear roles, responsibilities, and timelines that go beyond the general 5-day security response window currently documented.

---

## SOC2 Findings

### SOC2-001: User Authentication Controls

**LEGAL QUESTION**

Does the system implement logical access security controls over user authentication that are suitably designed and operating effectively to restrict access to authorized users, consistent with the Common Criteria CC6.1 requirement for logical and physical access controls?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC6.1 (Logical and Physical Access Controls)

**EVIDENCE**

- `.agents/skills/vitest/references/core-describe.md:40` — `test('shows login page', () => {})`
- `.agents/skills/vitest/references/features-filtering.md:30` — `vitest -t "login"`
- `.agents/skills/vitest/references/features-filtering.md:183` — `vitest user -t "login" --changed`
- `.claude/skills/vercel-composition-patterns/SKILL.md:6` — `designing reusable APIs. Triggers on tasks involving compound components,`
- `.claude/skills/vercel-composition-patterns/SKILL.md:28` — `- Designing flexible component APIs`
- `.cursor/rules/docs/docs-embeddings-generation/RULE.md:47` — `- Uses GitHub App authentication for access`
- `.cursor/rules/docs/docs-embeddings-generation/RULE.md:68` — `- **`page_section`** table: Stores individual sections with embeddings, token counts`
- `.cursor/rules/studio/styling/RULE.md:2` — `description: "Studio: styling rules (Tailwind + semantic tokens + typography/focus utilities)"`
- `.cursor/rules/studio/styling/RULE.md:11` — `- Do not hardcode Tailwind color tokens; use our semantic classes:`
- `.github/workflows/authorize-vercel-deploys.yml:49` — `VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}`

**FINDING: 🔴 High Risk**

The evidence reveals a risk pattern consistent with non-compliance under SOC 2 CC6.1 logical access controls requirements. While the repository contains references to login functionality in test files (.agents/skills/vitest/references/core-describe.md:40 and features-filtering.md:30), no actual authentication control implementation code was found. The evidence shows only token management for CI/CD workflows (.github/workflows/ files) and references to external authentication systems, but lacks substantive user authentication logic, access control mechanisms, or security validation routines within the application codebase itself.

**REMEDIATION DIRECTION**

Implement comprehensive user authentication controls including secure login/logout functions, session management, password policies, multi-factor authentication capabilities, and role-based access controls. The codebase should include authentication middleware, input validation, secure credential storage mechanisms, and access authorization checks. Additionally, ensure that authentication-related security controls are properly tested beyond the basic login page tests currently present, and document the authentication architecture to demonstrate compliance with logical access control requirements.

---

### SOC2-002: Role-Based Access Control

**LEGAL QUESTION**

Does the system implement role-based or attribute-based access controls that restrict system functions and data access based on authorized user roles, consistent with the principle of least privilege as required under CC6.3?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC6.3 (Role-Based Access and Least Privilege)

**EVIDENCE**

- `.agents/skills/vitest/references/advanced-environments.md:229` — `classNameStrategy: 'non-scoped',`
- `.agents/skills/vitest/references/core-describe.md:186` — `- Hooks are scoped to their suite and nested suites`
- `.agents/skills/vitest/references/core-hooks.md:56` — `## Scoped Hooks`
- `.agents/skills/vitest/references/features-context.md:101` — `## Scoped Fixtures`
- `.agents/skills/vitest/references/features-context.md:103` — `### File Scope`
- `.agents/skills/vitest/references/features-context.md:115` — `{ scope: 'file' }`
- `.agents/skills/vitest/references/features-context.md:120` — `### Worker Scope`
- `.agents/skills/vitest/references/features-context.md:130` — `{ scope: 'worker' }`
- `.agents/skills/vitest/references/features-context.md:160` — `## Scoped Values per Suite`
- `.agents/skills/vitest/references/features-context.md:170` — `test.scoped({ environment: 'production' })`

**FINDING: 🔴 High Risk**

No evidence of role-based or attribute-based access controls was found in the code repository analysis. While the README indicates Supabase includes "Authentication and Authorization" features, the evidence provided consists entirely of testing framework configuration files (Vitest) and test scoping mechanisms, with no actual implementation of user role management, permission matrices, or access control enforcement mechanisms. This creates a risk pattern consistent with non-compliance under SOC 2 CC6.3.

**REMEDIATION DIRECTION**

Implement a comprehensive role-based access control (RBAC) system that includes: user role definitions and assignments, permission matrices mapping roles to specific system functions and data access levels, middleware or interceptors that enforce access controls at the application layer, and audit logging of access decisions. The system should default to denying access and require explicit permission grants based on assigned user roles, following the principle of least privilege. Consider leveraging Supabase's existing auth features mentioned in the README to build proper RBAC controls.

---

### SOC2-003: Encryption in Transit

**LEGAL QUESTION**

Does the system protect data during transmission over networks using encryption or other equivalent security measures, consistent with the CC6.7 requirement for protection of information during transmission?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC6.7 (Data Transmission Protection)

**EVIDENCE**

- `.agents/skills/vitest/SKILL.md:7` — `source: Generated from https://github.com/vitest-dev/vitest, scripts located at https://github.com/antfu/skills`
- `.agents/skills/vitest/references/advanced-environments.md:263` — `- https://vitest.dev/guide/environment.html`
- `.agents/skills/vitest/references/advanced-projects.md:212` — `apiUrl: 'https://staging.api.com',`
- `.agents/skills/vitest/references/advanced-projects.md:221` — `apiUrl: 'https://api.com',`
- `.agents/skills/vitest/references/advanced-projects.md:299` — `- https://vitest.dev/guide/projects.html`
- `.agents/skills/vitest/references/advanced-type-testing.md:235` — `- https://vitest.dev/guide/testing-types.html`
- `.agents/skills/vitest/references/advanced-type-testing.md:236` — `- https://vitest.dev/api/expect-typeof.html`
- `.agents/skills/vitest/references/advanced-vi.md:248` — `- https://vitest.dev/api/vi.html`
- `.agents/skills/vitest/references/core-cli.md:165` — `- https://vitest.dev/guide/cli.html`
- `.agents/skills/vitest/references/core-config.md:172` — `- https://vitest.dev/guide/#configuring-vitest`

**FINDING: 🔵 Pattern of Concern**

The evidence shows mixed encryption practices that present a risk pattern consistent with non-compliance under SOC 2 CC6.7. While HTTPS URLs are used in production configurations (staging.api.com, api.com, api.prod.com), multiple instances of unencrypted HTTP protocols were detected in development and test environments across vitest configuration files and developer documentation at lines 26, 87, 122, 126 in .agents/skills/vitest/references/ and lines 89-91, 156 in DEVELOPERS.md. The repository lacks explicit evidence of comprehensive data transmission encryption policies or controls.

**REMEDIATION DIRECTION**

Implement a consistent encryption-in-transit policy that mandates HTTPS for all environments, including development and testing. Update all HTTP references in configuration files to use HTTPS or implement local TLS certificates for development environments. Add explicit documentation of encryption requirements and configure automated checks to prevent HTTP usage in any environment that handles sensitive data. Consider implementing HSTS headers and certificate pinning for additional transmission security.

---

### SOC2-004: Logging and Monitoring

**LEGAL QUESTION**

Does the system implement logging, monitoring, and alerting mechanisms that detect and record security events, anomalies, and unauthorized activities, as required under CC7.2 for monitoring system components for anomalies?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC7.2 (Monitoring of System Components)

**EVIDENCE**

- `.agents/skills/vitest/SKILL.md:31` — `| Expect API | Assertions with toBe, toEqual, matchers and asymmetric matchers | [core-expect](references/core-expect.md`
- `.agents/skills/vitest/references/core-expect.md:3` — `description: Assertions with matchers, asymmetric matchers, and custom matchers`
- `.agents/skills/vitest/references/core-expect.md:103` — `## Asymmetric Matchers`
- `.claude/skills/e2e-studio-tests/SKILL.md:180` — `### View trace`
- `.claude/skills/e2e-studio-tests/SKILL.md:183` — `cd e2e/studio && pnpm exec playwright show-trace <path-to-trace.zip>`
- `.cursor/rules/studio-useStaticEffectEvent.mdc:23` — `showNotification('Connected!', theme) // `theme` causes unwanted re-runs`
- `.cursor/rules/studio/RULE.md:32` — `- `studio/alerts``
- `.cursor/rules/studio/alerts/RULE.md:2` — `description: "Studio: alert/admonition usage and placement"`
- `.cursor/rules/studio/alerts/RULE.md:8` — `# Studio alerts`
- `.cursor/rules/studio/best-practices/RULE.md:154` — `return <AlertError error={error} subject="Failed to load data" />`

**FINDING: 🔴 High Risk**

The evidence reveals a risk pattern consistent with non-compliance under SOC 2 CC7.2. While references to logging infrastructure exist (gitignore entries for Supabase logs and Sentry configuration at lines 141 and 153-154), no actual implementation of security event logging, monitoring, or alerting mechanisms was found in the codebase. The discovered evidence primarily consists of testing frameworks, UI alerts, and development tooling rather than security monitoring controls required for anomaly detection.

**REMEDIATION DIRECTION**

Implement comprehensive security logging and monitoring infrastructure including: security event logging for authentication failures, unauthorized access attempts, and privilege escalations; automated anomaly detection systems that monitor system components for unusual patterns; real-time alerting mechanisms that notify security teams of potential threats; and centralized log management with appropriate retention policies. Configure monitoring dashboards and establish incident response procedures triggered by security alerts.

---

### SOC2-005: Change Management

**LEGAL QUESTION**

Does the system demonstrate evidence of change management controls including version control, code review processes, and controlled deployment procedures, as required under CC8.1 for managing changes to infrastructure, data, software, and procedures?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC8.1 (Change Management)

**EVIDENCE**

- `.agents/skills/vitest/SKILL.md:6` — `version: "2026.1.28"`
- `.agents/skills/vitest/SKILL.md:13` — `- Vite-native: Uses Vite's transformation pipeline for fast HMR-like test updates`
- `.agents/skills/vitest/references/advanced-environments.md:23` — `// Environment-specific options`
- `.agents/skills/vitest/references/advanced-environments.md:236` — `## Fixing External Dependencies`
- `.agents/skills/vitest/references/advanced-projects.md:162` — `## Project-Specific Dependencies`
- `.agents/skills/vitest/references/advanced-projects.md:164` — `Each project can have different dependencies inlined:`
- `.agents/skills/vitest/references/advanced-projects.md:185` — `## Running Specific Projects`
- `.agents/skills/vitest/references/advanced-projects.md:188` — `# Run specific project`
- `.agents/skills/vitest/references/advanced-projects.md:293` — `- Run specific projects with `--project` flag`
- `.agents/skills/vitest/references/advanced-projects.md:210` — `name: 'staging',`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOC 2 CC8.1 change management requirements. While the repository contains testing framework documentation with version identifiers (.agents/skills/vitest/SKILL.md:6), there is no evidence of formal change management controls including version control systems, code review processes, or controlled deployment procedures. The evidence primarily consists of test configuration examples and CLI documentation rather than actual change management infrastructure or procedural controls.

**REMEDIATION DIRECTION**

Implement comprehensive change management controls including: establishing a formal version control system (Git) with branch protection rules requiring code reviews before merges, implementing automated CI/CD pipelines with approval gates for deployments to staging and production environments, creating documented procedures for change approval and rollback processes, and maintaining audit trails of all changes to infrastructure, software, and procedures. Document these processes and ensure they cover all system components referenced in the codebase.

---

### SOC2-006: Incident Response

**LEGAL QUESTION**

Does the system implement incident detection, response, and recovery procedures that enable timely identification and remediation of security incidents, consistent with CC7.3 requirements for evaluating security events and CC7.4 for responding to identified incidents?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC7.3 (Security Event Evaluation); CC7.4 (Incident Response)

**EVIDENCE**

- `.claude/skills/studio-testing/SKILL.md:30` — `| 1        | Logic Extraction | CRITICAL | `testing-` |`
- `.claude/skills/studio-testing/SKILL.md:31` — `| 2        | Test Coverage    | CRITICAL | `testing-` |`
- `.claude/skills/studio-testing/SKILL.md:37` — `### 1. Logic Extraction (CRITICAL)`
- `.claude/skills/studio-testing/SKILL.md:42` — `### 2. Test Coverage (CRITICAL)`
- `.claude/skills/studio-testing/rules/testing-e2e-shared-features.md:4` — `impactDescription: ensures critical shared features work across deployment targets`
- `.claude/skills/studio-testing/rules/testing-exhaustive-permutations.md:3` — `impact: CRITICAL`
- `.claude/skills/studio-testing/rules/testing-extract-logic.md:3` — `impact: CRITICAL`
- `.claude/skills/vercel-composition-patterns/AGENTS.md:47` — `**Impact: CRITICAL (prevents unmaintainable component variants)**`
- `.claude/skills/vercel-composition-patterns/rules/architecture-avoid-boolean-props.md:3` — `impact: CRITICAL`
- `.cursor/rules/studio/RULE.md:32` — `- `studio/alerts``

**FINDING: 🔴 High Risk**

The code repository shows a risk pattern consistent with non-compliance under SOC 2 CC7.3 and CC7.4 requirements. While some alert mechanisms exist (studio/alerts rules in .cursor/rules/studio/alerts/RULE.md and error handling patterns), there is no evidence of formal incident detection, response, or recovery procedures for security events. The SECURITY.md file only contains vulnerability disclosure procedures with a 5-day response commitment, but lacks systematic incident response workflows or security event evaluation capabilities required by the Trust Services Criteria.

**REMEDIATION DIRECTION**

Implement comprehensive incident response procedures including: automated security event detection and logging systems, defined incident classification and escalation procedures, documented response workflows for different incident types, and recovery/remediation tracking mechanisms. Add security monitoring capabilities that can evaluate events in real-time and trigger appropriate response actions. Establish incident response team roles, communication procedures, and post-incident review processes to ensure timely identification and remediation of security incidents beyond just vulnerability disclosures.

---

### SOC2-007: Vendor and Dependency Risk

**LEGAL QUESTION**

Does the system assess and manage risks associated with third-party vendors, libraries, and service providers, including dependency vulnerability management, consistent with CC9.2 requirements for risk assessment of third-party service providers?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC9.2 (Third-Party Risk Management)

**EVIDENCE**

- `.agents/skills/vitest/SKILL.md:30` — `| Describe API | describe/suite for grouping tests and nested suites | [core-describe](references/core-describe.md) |`
- `.agents/skills/vitest/references/advanced-vi.md:234` — `// Partial mock typing`
- `.agents/skills/vitest/references/core-cli.md:115` — `## Package.json Scripts`
- `.agents/skills/vitest/references/core-describe.md:3` — `description: describe/suite for grouping tests into logical blocks`
- `.agents/skills/vitest/references/core-describe.md:3` — `description: describe/suite for grouping tests into logical blocks`
- `.agents/skills/vitest/references/core-expect.md:214` — `- `toThrow` requires wrapping sync code in a function`
- `.agents/skills/vitest/references/features-coverage.md:146` — `## Package.json Scripts`
- `.agents/skills/vitest/references/features-filtering.md:203` — `- Tags provide semantic test grouping`
- `.claude/skills/e2e-studio-tests/SKILL.md:110` — `// Could consider scoping down the container or filtering the combobox more specifically`
- `.claude/skills/studio-error-handling/SKILL.md:26` — `| `ErrorMatcher.tsx`                    | Component — reads `errorType`, looks up mapping, renders         |`

**FINDING: 🔴 High Risk**

No evidence of third-party vendor risk assessment or dependency vulnerability management processes was found in the code repository. The evidence shows only testing framework documentation and UI component patterns, with no security controls, vendor evaluation procedures, or dependency scanning mechanisms present. This represents a risk pattern consistent with non-compliance under SOC 2 CC9.2 requirements for systematic third-party risk management.

**REMEDIATION DIRECTION**

Implement a comprehensive third-party risk management program including: dependency vulnerability scanning tools (like npm audit, Snyk, or OWASP Dependency-Check) integrated into the CI/CD pipeline; vendor security assessment procedures with documented evaluation criteria; regular dependency updates and patch management processes; and maintain an inventory of all third-party libraries, services, and vendors with associated risk ratings. Document these processes and ensure they are consistently applied across all system components.

---

### SOC2-008: Data Backup and Recovery

**LEGAL QUESTION**

Does the system implement data backup, replication, and recovery controls that ensure availability and recoverability of data, consistent with the A1.2 criterion for recovery of infrastructure and data to meet objectives?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria A1.2 (Recovery of Infrastructure and Data)

**EVIDENCE**

- `.agents/skills/vitest/GENERATION.md:4` — `- **Git SHA:** `4a7321e10672f00f0bb698823a381c2cc245b8f7``
- `.agents/skills/vitest/SKILL.md:19` — `- Snapshot testing, mocking, and spy utilities`
- `.agents/skills/vitest/SKILL.md:39` — `| Snapshots | Snapshot testing with toMatchSnapshot and inline snapshots | [features-snapshots](references/features-snap`
- `.agents/skills/vitest/SKILL.md:10` — `Vitest is a next-generation testing framework powered by Vite. It provides a Jest-compatible API with native ESM, TypeSc`
- `.agents/skills/vitest/SKILL.md:42` — `| Concurrency | Concurrent tests, parallel execution, sharding | [features-concurrency](references/features-concurrency.`
- `.agents/skills/vitest/SKILL.md:50` — `| Environments | Test environments: node, jsdom, happy-dom, custom | [advanced-environments](references/advanced-environ`
- `.agents/skills/vitest/references/advanced-environments.md:146` — `export default <Environment>{`
- `.agents/skills/vitest/references/advanced-environments.md:178` — `export default <Environment>{`
- `.agents/skills/vitest/references/advanced-environments.md:3` — `description: Configure environments like jsdom, happy-dom for browser APIs`
- `.agents/skills/vitest/references/advanced-environments.md:12` — `- `happy-dom` - Faster alternative to jsdom`

**FINDING: 🔴 High Risk**

No evidence of data backup, replication, or recovery controls was found in the code repository. The evidence consists entirely of testing framework configuration files (Vitest) in `.agents/skills/vitest/` directory, which relate to development testing rather than production data protection systems. This absence of backup and recovery implementation creates a risk pattern consistent with non-compliance under SOC 2 Trust Services Criteria A1.2.

**REMEDIATION DIRECTION**

Implement comprehensive data backup and recovery controls including automated backup schedules, data replication mechanisms, disaster recovery procedures, and recovery time/point objectives. Document backup retention policies, test recovery procedures regularly, and maintain backup integrity verification processes. Consider implementing database-level backups, file system snapshots, and cross-region replication given this appears to be a Supabase-related project handling production data.

---

### SOC2-009: Multi-Factor Authentication

**LEGAL QUESTION**

Does the system implement or support multi-factor authentication for user access, particularly for privileged accounts and administrative interfaces, consistent with CC6.1 requirements for logical access security?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC6.1 (Logical Access - MFA)

**EVIDENCE**

- `.agents/skills/vitest/references/features-snapshots.md:187` — `resolveSnapshotPath: (testPath, snapExtension) => {`
- `.agents/skills/vitest/references/features-snapshots.md:187` — `resolveSnapshotPath: (testPath, snapExtension) => {`
- `apps/design-system/__registry__/index.tsx:965` — `"input-otp-demo": {`
- `apps/design-system/__registry__/index.tsx:966` — `name: "input-otp-demo",`
- `apps/design-system/__registry__/index.tsx:968` — `registryDependencies: ["input-otp"],`
- `apps/design-system/__registry__/index.tsx:969` — `component: React.lazy(() => import("@/registry/default/example/input-otp-demo")),`
- `apps/design-system/__registry__/index.tsx:971` — `files: ["registry/default/example/input-otp-demo.tsx"],`
- `apps/design-system/__registry__/index.tsx:976` — `"input-otp-pattern": {`
- `apps/design-system/__registry__/index.tsx:977` — `name: "input-otp-pattern",`
- `apps/design-system/__registry__/index.tsx:979` — `registryDependencies: ["input-otp"],`

**FINDING: 🟠 Medium Risk**

The evidence shows OTP (One-Time Password) input components in the design system registry (apps/design-system/__registry__/index.tsx lines 965-1001), indicating UI elements for potential MFA implementation. However, no actual authentication logic, MFA enforcement policies, or administrative access controls were found in the repository evidence. This creates a risk pattern consistent with non-compliance under SOC 2 CC6.1, as the presence of UI components alone does not demonstrate functional multi-factor authentication implementation.

**REMEDIATION DIRECTION**

Implement complete MFA functionality beyond just UI components. This should include backend authentication services that enforce MFA for all user accounts (especially privileged/administrative accounts), integration with MFA providers (TOTP, SMS, hardware tokens), session management that validates second factors, and administrative policies that mandate MFA usage. Document the MFA implementation and provide evidence of enforcement mechanisms, particularly for administrative interfaces and privileged account access.

---

### SOC2-010: Security Policy Documentation

**LEGAL QUESTION**

Does the system demonstrate evidence of documented security policies, including acceptable use, data classification, and access management policies, as required under CC1.1 for the entity's commitment to integrity and ethical values?

**REGULATORY STANDARD**

SOC 2 Trust Services Criteria CC1.1 (COSO Principle 1 - Integrity and Ethical Values)

**EVIDENCE**

- `.github/pull_request_template.md:1` — `## I have read the [CONTRIBUTING.md](https://github.com/supabase/supabase/blob/master/CONTRIBUTING.md) file.`
- `.github/workflows/external-pr-comment.yml:20` — `Thanks for contributing to Supabase! ❤️ Our team will review your PR.`
- `.prettierignore:18` — `apps/docs/CONTRIBUTING.md`
- `CONTRIBUTING.md:1` — `# CONTRIBUTING.md`
- `CONTRIBUTING.md:3` — `Thank you for contributing to Supabase! We’re a big, exciting open source project and we’d love to have you contribute! `
- `CONTRIBUTING.md:11` — `To ensure a positive and inclusive environment, please read our [code of conduct](https://github.com/supabase/.github/bl`
- `CONTRIBUTING.md:11` — `To ensure a positive and inclusive environment, please read our [code of conduct](https://github.com/supabase/.github/bl`
- `DEVELOPERS.md:31` — `To ensure a positive and inclusive environment, please read our [code of conduct](https://github.com/supabase/.github/bl`
- `SECURITY.md:2` — `Canonical: https://supabase.com/.well-known/security.txt`
- `SECURITY.md:2` — `Canonical: https://supabase.com/.well-known/security.txt`

**FINDING: 🔴 High Risk**

The code repository shows a risk pattern consistent with non-compliance under SOC 2 CC1.1, as no documented security policies for acceptable use, data classification, or access management were identified in the evidence. While the repository contains contributing guidelines (CONTRIBUTING.md), code of conduct references, and a security contact file (SECURITY.md), these do not constitute the formal security policy documentation required for demonstrating organizational commitment to integrity and ethical values under the Trust Services Criteria.

**REMEDIATION DIRECTION**

The organization needs to create and maintain formal, documented security policies that specifically address acceptable use of systems and data, data classification standards, and access management procedures. These policies should be stored in accessible locations within the repository (such as a /policies or /security-policies directory) and referenced in the main README or contributing documentation. The policies must go beyond basic contributing guidelines to establish clear security expectations, data handling requirements, and access control standards that demonstrate organizational commitment to integrity and ethical values.

---

## SOX Findings

### SOX-001: Financial Data Integrity Controls

**LEGAL QUESTION**

Does the system implement controls to ensure the integrity, accuracy, and completeness of financial data and transactions, consistent with SOX Section 302 requirements for management certification of financial statements?

**REGULATORY STANDARD**

SOX Section 302 (Corporate Responsibility for Financial Reports)

**EVIDENCE**

- `.agents/skills/vitest/references/core-hooks.md:89` — `// Wrap each test in database transaction`
- `.agents/skills/vitest/references/core-hooks.md:91` — `await db.beginTransaction()`
- `.claude/skills/studio-testing/rules/testing-component-tests-ui-only.md:21` — `validation that happens to live inside a component. Extract that logic into a`
- `.claude/skills/telemetry-standards/SKILL.md:134` — `connectionMethod: 'transaction_pooler',`
- `.cursor/rules/docs/docs-embeddings-generation/RULE.md:15` — `2. **Processing content** into structured sections with checksums`
- `.cursor/rules/docs/docs-embeddings-generation/RULE.md:57` — `- Checksum for change detection`
- `.cursor/rules/docs/docs-embeddings-generation/RULE.md:60` — `3. **Change Detection**: Compares checksums against existing database records`
- `.cursor/rules/docs/docs-embeddings-generation/RULE.md:67` — `- **`page`** table: Stores page metadata, content, checksum, version`
- `.cursor/rules/studio/best-practices/RULE.md:407` — `### Avoid type casting, prefer validation with zod`
- `.cursor/rules/studio/best-practices/RULE.md:431` — `// handle validation errors`

**FINDING: 🔴 High Risk**

The evidence reveals a risk pattern consistent with non-compliance under SOX Section 302 requirements for financial data integrity controls. While basic database transaction controls are present (.agents/skills/vitest/references/core-hooks.md:91), there is no evidence of comprehensive financial data validation, audit trails, access controls, or data completeness verification mechanisms that would be required for SOX compliance. The repository appears to be a general-purpose development platform (Supabase) without specific financial reporting controls or safeguards for financial transaction integrity.

**REMEDIATION DIRECTION**

Implement comprehensive financial data integrity controls including: data validation schemas specifically for financial transactions using tools like Zod (referenced but not implemented for financial data), audit logging for all financial data modifications with immutable timestamps and user attribution, role-based access controls for financial data access, automated data completeness checks and reconciliation processes, and transaction rollback capabilities with proper error handling. Additionally, establish formal procedures for management certification of financial data accuracy and implement automated controls testing to ensure ongoing compliance with SOX Section 302 requirements.

---

### SOX-002: Access Controls to Financial Systems

**LEGAL QUESTION**

Does the system implement access controls that restrict access to financial systems and data to authorized personnel, with appropriate authentication and authorization mechanisms, as required under SOX Section 404 internal controls?

**REGULATORY STANDARD**

SOX Section 404 (Management Assessment of Internal Controls)

**EVIDENCE**

- `.agents/skills/vitest/references/features-context.md:215` — `// admin-test.ts`
- `.agents/skills/vitest/references/features-context.md:218` — `export const test = dbTest.extend<{ admin: User }>({`
- `.agents/skills/vitest/references/features-context.md:219` — `admin: async ({ db }, use) => {`
- `.agents/skills/vitest/references/features-context.md:220` — `const admin = await db.createAdmin()`
- `.agents/skills/vitest/references/features-context.md:221` — `await use(admin)`
- `.claude/skills/e2e-studio-tests/SKILL.md:72` — `1. **`getByRole` with accessible name** - Most robust, tests accessibility`
- `.claude/skills/e2e-studio-tests/SKILL.md:74` — `page.getByRole('button', { name: 'Save' })`
- `.claude/skills/e2e-studio-tests/SKILL.md:75` — `page.getByRole('button', { name: 'Configure API privileges' })`
- `.claude/skills/e2e-studio-tests/SKILL.md:104` — `element.locator('..').getByRole('button')`
- `.claude/skills/e2e-studio-tests/SKILL.md:111` — `popover.getByRole('combobox')`

**FINDING: 🔴 High Risk**

The evidence shows a risk pattern consistent with non-compliance under SOX Section 404 internal controls requirements. While the codebase contains test fixtures for admin user creation (`.agents/skills/vitest/references/features-context.md:219-220`) and references to API privileges configuration, no actual authentication mechanisms, authorization controls, or access restriction implementations for financial systems were found in the repository evidence. The README indicates this is a Supabase platform with authentication capabilities, but the specific access controls protecting financial data are not evident in the code samples provided.

**REMEDIATION DIRECTION**

Implement comprehensive access control mechanisms including multi-factor authentication, role-based authorization with principle of least privilege, session management, and audit logging for all financial system access. Document and codify user provisioning/deprovisioning procedures, establish regular access reviews, and ensure all financial data operations require proper authentication tokens and authorization checks before execution.

---

### SOX-003: Audit Trail for Financial Transactions

**LEGAL QUESTION**

Does the system maintain a complete and tamper-evident audit trail of all financial transactions, modifications, and access events, sufficient to support the audit requirements under SOX Section 802?

**REGULATORY STANDARD**

SOX Section 802 (Criminal Penalties for Altering Documents)

**EVIDENCE**

- `.agents/skills/vitest/references/advanced-vi.md:33` — `fn.mockClear()    // Clear call history`
- `.agents/skills/vitest/references/advanced-vi.md:34` — `fn.mockReset()    // Clear history + implementation`
- `.agents/skills/vitest/references/advanced-vi.md:215` — `vi.clearAllMocks()   // Clear all mock call history`
- `.agents/skills/vitest/references/features-mocking.md:211` — `fn.mockClear()       // Clear call history`
- `.agents/skills/vitest/references/features-mocking.md:212` — `fn.mockReset()       // Clear history + implementation`
- `.claude/skills/studio-testing/rules/testing-exhaustive-permutations.md:18` — `- Edge cases (timestamps with colons, special characters, boundary values)`
- `.claude/skills/studio-testing/rules/testing-exhaustive-permutations.md:41` — `test('handles timestamp with colons in value', () => {`
- `.claude/skills/studio-testing/rules/testing-exhaustive-permutations.md:79` — `test('detects timestamp', () => { ... })      // multiple formats -> timestamptz`
- `.gitignore:75` — `# Optional REPL history`
- `.gitignore:76` — `.node_repl_history`

**FINDING: 🔴 High Risk**

The evidence reveals a risk pattern consistent with non-compliance under SOX Section 802. While timestamping functionality exists in design system components (apps/design-system/__registry__/default/block/chart-composed-*.tsx), no evidence was found of comprehensive audit trail mechanisms for financial transactions, modifications, or access events. Additionally, the presence of mock clearing functions (mockClear(), mockReset()) in testing frameworks (.agents/skills/vitest/references/) and history clearing capabilities (.gitignore references to .node_repl_history) indicates potential anti-patterns that could undermine audit trail integrity.

**REMEDIATION DIRECTION**

Implement a comprehensive audit logging system that captures all financial transactions, data modifications, and user access events with immutable timestamps and tamper-evident mechanisms. Remove or restrict any functionality that allows clearing of operational logs or audit trails in production environments. Ensure audit logs are stored separately from application data with appropriate access controls, retention policies, and integrity verification mechanisms to meet SOX compliance requirements.

---

### SOX-004: Change Management for Financial Software

**LEGAL QUESTION**

Does the system implement change management controls for software that processes financial data, including version control, code review, testing, and controlled deployment, consistent with SOX IT general controls?

**REGULATORY STANDARD**

SOX Section 404 (ITGC - Change Management Controls)

**EVIDENCE**

- `.agents/skills/vitest/SKILL.md:6` — `version: "2026.1.28"`
- `.agents/skills/vitest/SKILL.md:13` — `- Vite-native: Uses Vite's transformation pipeline for fast HMR-like test updates`
- `.agents/skills/vitest/references/advanced-environments.md:23` — `// Environment-specific options`
- `.agents/skills/vitest/references/advanced-environments.md:236` — `## Fixing External Dependencies`
- `.agents/skills/vitest/references/advanced-projects.md:162` — `## Project-Specific Dependencies`
- `.agents/skills/vitest/references/advanced-projects.md:164` — `Each project can have different dependencies inlined:`
- `.agents/skills/vitest/references/advanced-projects.md:185` — `## Running Specific Projects`
- `.agents/skills/vitest/references/advanced-projects.md:188` — `# Run specific project`
- `.agents/skills/vitest/references/advanced-projects.md:293` — `- Run specific projects with `--project` flag`
- `.agents/skills/vitest/references/advanced-projects.md:210` — `name: 'staging',`

**FINDING: 🔴 High Risk**

The evidence shows only testing framework documentation (Vitest) but no actual implementation of SOX-required change management controls for financial software. While testing capabilities exist with environment-specific configurations (staging and production references in advanced-projects.md:210-219), there is no evidence of version control systems, formal code review processes, or controlled deployment procedures. This creates a risk pattern consistent with non-compliance under SOX Section 404 IT General Controls for change management.

**REMEDIATION DIRECTION**

Implement comprehensive change management controls including: (1) formal version control system with branch protection and merge approval requirements, (2) mandatory code review process with documented approval workflows, (3) automated testing pipelines that must pass before deployment, and (4) controlled deployment procedures with segregation of duties between development, testing, and production environments. Document all procedures and maintain audit trails of changes to financial data processing systems.

---

### SOX-005: Segregation of Duties Evidence

**LEGAL QUESTION**

Does the system implement segregation of duties controls that prevent any single individual from having the ability to both authorize and execute financial transactions, or to both develop and deploy changes to financial systems?

**REGULATORY STANDARD**

SOX Section 404 (Internal Controls - Segregation of Duties)

**EVIDENCE**

- `.agents/skills/vitest/references/features-concurrency.md:73` — `Limit concurrent tests:`
- `.agents/skills/vitest/references/features-coverage.md:45` — `// Thresholds`
- `.agents/skills/vitest/references/features-coverage.md:46` — `thresholds: {`
- `.agents/skills/vitest/references/features-coverage.md:95` — `## Thresholds`
- `.agents/skills/vitest/references/features-coverage.md:97` — `Fail tests if coverage is below threshold:`
- `.agents/skills/vitest/references/features-coverage.md:101` — `thresholds: {`
- `.agents/skills/vitest/references/features-coverage.md:102` — `// Global thresholds`
- `.agents/skills/vitest/references/features-coverage.md:108` — `// Per-file thresholds`
- `.agents/skills/vitest/references/features-coverage.md:111` — `// Auto-update thresholds (for gradual improvement)`
- `.agents/skills/vitest/references/features-coverage.md:201` — `- Set thresholds to enforce minimum coverage`

**FINDING: 🔴 High Risk**

No evidence of segregation of duties controls was found in the code repository to prevent single individuals from both authorizing and executing financial transactions or from both developing and deploying financial system changes. The evidence shows only testing workflows (.github/workflows/ai-tests.yml, .github/workflows/authorize-vercel-deploys.yml) and code coverage thresholds, but lacks any access control mechanisms, approval workflows, or role-based restrictions that would enforce segregation of duties. This represents a risk pattern consistent with non-compliance under SOX Section 404 requirements for internal controls.

**REMEDIATION DIRECTION**

Implement role-based access controls and multi-person approval workflows for all financial operations and system changes. Create separate roles for transaction authorization vs. execution, and for development vs. deployment activities. Add approval gates in CI/CD pipelines requiring different individuals to approve code changes before deployment to production financial systems. Document these controls with clear role definitions and establish audit trails for all financial system access and modifications.

---

### SOX-006: Data Retention for Financial Records

**LEGAL QUESTION**

Does the system implement data retention policies that preserve financial records, audit work papers, and supporting documentation for the minimum retention period required under SOX Section 802 (not less than 7 years)?

**REGULATORY STANDARD**

SOX Section 802 (Document Retention - 7 Year Minimum)

**EVIDENCE**

- `.agents/skills/vitest/references/features-coverage.md:122` — `/* v8 ignore next -- @preserve */`
- `.agents/skills/vitest/references/features-coverage.md:127` — `/* v8 ignore start -- @preserve */`
- `.agents/skills/vitest/references/features-coverage.md:129` — `/* v8 ignore stop -- @preserve */`
- `.agents/skills/vitest/references/features-coverage.md:135` — `/* istanbul ignore next -- @preserve */`
- `.agents/skills/vitest/references/features-coverage.md:138` — `/* istanbul ignore if -- @preserve */`
- `.agents/skills/vitest/references/features-coverage.md:144` — `Note: `@preserve` keeps comments through esbuild.`
- `.agents/skills/vitest/references/features-coverage.md:202` — `- Use `@preserve` comment to keep ignore hints`
- `.claude/skills/studio-error-handling/SKILL.md:46` — `- Do not pass `error.message` to `ErrorMatcher` — pass the full `error` object so the class is preserved.`
- `.claude/skills/telemetry-standards/SKILL.md:28` — `- `backup_button_clicked``
- `.claude/skills/telemetry-standards/SKILL.md:33` — `- `click_backup_button` → `backup_button_clicked` (wrong order)`

**FINDING: 🔴 High Risk**

No evidence of data retention policies for financial records, audit work papers, or supporting documentation was found in the codebase. The only retention-related configurations discovered are GitHub workflow artifacts with 1-7 day retention periods (.github/workflows/studio-e2e-test.yml:105, .github/workflows/studio-unit-tests.yml:76), which fall far short of SOX requirements. This presents a risk pattern consistent with non-compliance under SOX Section 802, which mandates minimum 7-year retention for financial records and audit documentation.

**REMEDIATION DIRECTION**

Implement a comprehensive data retention policy system that automatically preserves financial records, audit trails, and supporting documentation for at least 7 years. This should include database-level retention policies, automated archival processes, and configuration management to ensure compliance with SOX Section 802. The system should also include audit logging to demonstrate retention policy enforcement and prevent premature deletion of regulated financial data.

---

### SOX-007: Internal Control Documentation

**LEGAL QUESTION**

Does the system provide evidence of documented internal controls over financial reporting, including control objectives, control activities, and monitoring procedures, as required under SOX Section 404(a)?

**REGULATORY STANDARD**

SOX Section 404(a) (Management Assessment of Internal Controls)

**EVIDENCE**

- `.agents/skills/vitest/SKILL.md:3` — `description: Vitest fast unit testing framework powered by Vite with Jest-compatible API. Use when writing tests, mockin`
- `.agents/skills/vitest/SKILL.md:10` — `Vitest is a next-generation testing framework powered by Vite. It provides a Jest-compatible API with native ESM, TypeSc`
- `.agents/skills/vitest/references/features-concurrency.md:141` — `Control test order:`
- `.agents/skills/vitest/references/features-snapshots.md:196` — `- Commit snapshot files to version control`
- `.claude/skills/e2e-studio-tests/SKILL.md:224` — `The test framework automatically resets the database when running `pnpm run e2e`. This matches CI behavior.`
- `.claude/skills/telemetry-standards/SKILL.md:4` — `PRs for telemetry compliance or implementing new event tracking. Covers event naming,`
- `.cursor/rules/docs/docs-embeddings-generation/RULE.md:8` — `# Documentation Embeddings Generation System`
- `.cursor/rules/docs/docs-embeddings-generation/RULE.md:12` — `The documentation embeddings generation system processes various documentation sources and uploads their metadata to a d`
- `.cursor/rules/docs/docs-embeddings-generation/RULE.md:14` — `1. **Discovering content sources** from multiple types of documentation`
- `.cursor/rules/docs/docs-embeddings-generation/RULE.md:36` — `- Processes `.mdx` files from guides and documentation`

**FINDING: 🔴 High Risk**

No evidence of documented internal controls over financial reporting was found in the code repository. The evidence shows only technical documentation, testing frameworks (Vitest), and development processes, but lacks any documentation of control objectives, control activities, or monitoring procedures required for financial reporting systems. This presents a risk pattern consistent with non-compliance under SOX Section 404(a) Management Assessment of Internal Controls.

**REMEDIATION DIRECTION**

Implement comprehensive internal control documentation that includes: (1) clearly defined control objectives for financial reporting processes, (2) documented control activities such as authorization procedures, segregation of duties, and approval workflows, (3) monitoring procedures and review processes, and (4) regular assessment and testing protocols. This documentation should be maintained in version control alongside technical documentation and include references to specific code components that implement these controls.

---

### SOX-008: Anti-Tampering Controls

**LEGAL QUESTION**

Does the system implement controls to prevent unauthorized alteration or destruction of financial records, including integrity verification, immutable storage, and tamper detection mechanisms, consistent with SOX Section 802 anti-destruction requirements?

**REGULATORY STANDARD**

SOX Section 802 (Criminal Penalties for Document Destruction/Alteration)

**EVIDENCE**

- `.cursor/rules/docs/docs-embeddings-generation/RULE.md:15` — `2. **Processing content** into structured sections with checksums`
- `.cursor/rules/docs/docs-embeddings-generation/RULE.md:57` — `- Checksum for change detection`
- `.cursor/rules/docs/docs-embeddings-generation/RULE.md:60` — `3. **Change Detection**: Compares checksums against existing database records`
- `.cursor/rules/docs/docs-embeddings-generation/RULE.md:67` — `- **`page`** table: Stores page metadata, content, checksum, version`
- `.github/workflows/studio-e2e-test.yml:77` — `key: ${{ runner.os }}-nextjs-${{ hashFiles('pnpm-lock.yaml') }}-${{ hashFiles('apps/studio/**/*.js', 'apps/studio/**/*.j`
- `.github/workflows/studio-e2e-test.yml:80` — `${{ runner.os }}-nextjs-${{ hashFiles('pnpm-lock.yaml') }}-`
- `.gitignore:81` — `# Yarn Integrity file`
- `.gitignore:82` — `.yarn-integrity`
- `apps/docs/app/api/ai/docs/route.ts:59` — `const useAltSearchIndex = !isFeatureEnabled('search:fullIndex')`
- `apps/docs/app/api/ai/docs/route.ts:61` — `useAltSearchIndex,`

**FINDING: 🔴 High Risk**

The evidence reveals a risk pattern consistent with non-compliance under SOX Section 802 anti-destruction requirements. While basic checksum mechanisms for change detection exist in documentation processing (.cursor/rules/docs/docs-embeddings-generation/RULE.md:57-67), there is no evidence of comprehensive integrity verification, immutable storage controls, or tamper detection mechanisms for financial records. The anti-patterns detected include multiple instances of data deletion operations (apps/docs/content/guides/auth/auth-anonymous.mdx:365, apps/docs/content/guides/cron/quickstart.mdx:237) without corresponding tamper-evident logging or authorization controls.

**REMEDIATION DIRECTION**

Implement a comprehensive anti-tampering framework that includes: (1) cryptographic integrity verification using digital signatures or hash chains for all financial records, (2) immutable storage mechanisms such as append-only logs or blockchain-based storage, (3) tamper detection systems that log all access attempts and modifications with timestamps and user identification, (4) access controls that prevent unauthorized deletion or modification of financial records, and (5) automated monitoring and alerting for any attempts to alter or destroy financial data. All deletion operations should be replaced with logical deletion (marking records as inactive) while preserving the original data for audit purposes.

---

## TCPA Findings

### TCPA-001: Prior Express Written Consent for SMS

**LEGAL QUESTION**

Does the system obtain prior express written consent before sending marketing or promotional text messages, including a clear and conspicuous disclosure that consent is being sought, as required under 47 U.S.C. §227(b)(1) and 47 CFR §64.1200(a)(2)?

**REGULATORY STANDARD**

TCPA 47 U.S.C. §227(b)(1); 47 CFR §64.1200(a)(2)

**EVIDENCE**

- `LICENSE:135` — `the terms of any separate license agreement you may have executed`
- `LICENSE:144` — `agreed to in writing, Licensor provides the Work (and each`
- `LICENSE:156` — `negligent acts) or agreed to in writing, shall any Contributor be`
- `LICENSE:171` — `of any other Contributor, and only if You agree to indemnify,`
- `LICENSE:197` — `Unless required by applicable law or agreed to in writing, software`
- `apps/design-system/registry/default/example/checkbox-with-text.tsx:17` — `You agree to our Terms of Service and Privacy Policy.`
- `apps/docs/content/guides/auth/auth-web3.mdx:37` — `It defines the wallet address, timestamp, browser location where the sign-in occurred and includes a customizable statem`
- `apps/docs/content/guides/auth/auth-web3.mdx:185` — `Providing a `statement` is required for most Solana wallets and this message will be shown to the user on the consent di`
- `apps/docs/content/guides/auth/oauth-server/getting-started.mdx:57` — `authorization_url_path = "/oauth/consent"`
- `apps/docs/content/guides/auth/oauth-server/getting-started.mdx:139` — `2. Set the **Authorization Path** (e.g., `/oauth/consent`)`

**FINDING: 🔴 High Risk**

No evidence found of TCPA-compliant prior express written consent mechanisms for SMS marketing or promotional messages. The codebase contains general consent patterns for OAuth authorization flows (apps/docs/content/guides/auth/oauth-server/getting-started.mdx) and web3 wallet authentication statements, but lacks any SMS-specific consent collection, opt-in workflows, or TCPA-required disclosures. This represents a risk pattern consistent with non-compliance under 47 U.S.C. §227(b)(1) and 47 CFR §64.1200(a)(2).

**REMEDIATION DIRECTION**

Implement a compliant SMS consent collection system that includes: (1) clear and conspicuous disclosure that consent is being sought for marketing text messages, (2) explicit opt-in mechanism (not pre-checked boxes), (3) disclosure of message frequency and data rates, (4) clear instructions for opting out, and (5) persistent storage of consent records with timestamps. Add SMS consent workflow components to the design system and document the implementation in the authentication guides alongside existing OAuth consent patterns.

---

### TCPA-002: Opt-Out Mechanism Implementation

**LEGAL QUESTION**

Does the system provide a clear and easy mechanism for recipients to opt out of receiving further messages, and does it honor opt-out requests promptly, as required under TCPA and CTIA guidelines?

**REGULATORY STANDARD**

TCPA 47 U.S.C. §227(b)(2)(E); CTIA Messaging Principles

**EVIDENCE**

- `.agents/skills/vitest/references/core-cli.md:94` — `--bail <n>                # Stop after n failures`
- `.agents/skills/vitest/references/core-config.md:115` — `// Stop after first failure`
- `.agents/skills/vitest/references/features-concurrency.md:230` — `Stop after first failure:`
- `.agents/skills/vitest/references/features-concurrency.md:233` — `vitest --bail 1    # Stop after 1 failure`
- `.agents/skills/vitest/references/features-concurrency.md:234` — `vitest --bail      # Stop on first failure (same as --bail 1)`
- `.agents/skills/vitest/references/features-coverage.md:129` — `/* v8 ignore stop -- @preserve */`
- `.claude/skills/vercel-composition-patterns/AGENTS.md:132` — `<Composer.CancelEdit />`
- `.claude/skills/vercel-composition-patterns/AGENTS.md:532` — `<CancelButton />`
- `.claude/skills/vercel-composition-patterns/AGENTS.md:603` — `<CancelButton />`
- `.claude/skills/vercel-composition-patterns/AGENTS.md:672` — `<CancelButton />`

**FINDING: 🔴 High Risk**

No evidence of TCPA-compliant opt-out mechanisms was found in the codebase. The evidence shows only generic UI cancellation components and test configuration options unrelated to message opt-out functionality. This presents a risk pattern consistent with non-compliance under TCPA 47 U.S.C. §227(b)(2)(E) and CTIA Messaging Principles, which require clear opt-out mechanisms and prompt processing of opt-out requests.

**REMEDIATION DIRECTION**

Implement a comprehensive opt-out system that includes: (1) clear opt-out instructions in all messages (e.g., "Reply STOP to opt out"), (2) automated processing of opt-out keywords like "STOP", "UNSUBSCRIBE", etc., (3) immediate removal of opted-out recipients from messaging lists, (4) confirmation messages acknowledging opt-out requests, and (5) database tables to track opt-out status with proper indexing for quick lookups before sending messages. Ensure the opt-out mechanism is prominent, easy to use, and processes requests within the timeframes required by TCPA regulations.

---

### TCPA-003: Do Not Call List Checking

**LEGAL QUESTION**

Does the system check phone numbers against the National Do Not Call Registry and maintain an internal do-not-call list before initiating outbound calls or messages, as required under 47 CFR §64.1200(c)?

**REGULATORY STANDARD**

TCPA 47 CFR §64.1200(c) (Do Not Call Requirements)

**EVIDENCE**

- `.cursor/rules/studio/charts/RULE.md:14` — `- `apps/design-system/__registry__/default/block/chart-composed-demo.tsx``
- `.cursor/rules/studio/charts/RULE.md:15` — `- `apps/design-system/__registry__/default/block/chart-composed-basic.tsx``
- `.cursor/rules/studio/charts/RULE.md:16` — `- `apps/design-system/__registry__/default/block/chart-composed-states.tsx``
- `.cursor/rules/studio/charts/RULE.md:17` — `- `apps/design-system/__registry__/default/block/chart-composed-metrics.tsx``
- `.cursor/rules/studio/charts/RULE.md:18` — `- `apps/design-system/__registry__/default/block/chart-composed-actions.tsx``
- `.cursor/rules/studio/charts/RULE.md:19` — `- `apps/design-system/__registry__/default/block/chart-composed-table.tsx``
- `.cursor/rules/studio/empty-states/RULE.md:14` — `- `apps/design-system/registry/default/example/empty-state-presentational-icon.tsx``
- `.cursor/rules/studio/empty-states/RULE.md:15` — `- `apps/design-system/registry/default/example/empty-state-initial-state-informational.tsx``
- `.cursor/rules/studio/empty-states/RULE.md:16` — `- `apps/design-system/registry/default/example/empty-state-zero-items-table.tsx``
- `.cursor/rules/studio/empty-states/RULE.md:17` — `- `apps/design-system/registry/default/example/data-grid-empty-state.tsx``

**FINDING: 🔴 High Risk**

No evidence of Do Not Call Registry checking or internal do-not-call list maintenance was found in the codebase. The evidence consists entirely of design system components (charts, forms, tables, layout examples) and README documentation for the Supabase platform, with no telecommunications functionality, phone number validation, or outbound calling capabilities present. This represents a risk pattern consistent with non-compliance under 47 CFR §64.1200(c) if this system is intended to perform outbound calling or messaging functions.

**REMEDIATION DIRECTION**

If this system performs outbound calls or SMS messaging, implement mandatory Do Not Call Registry checking before any outbound communication attempts. This should include: (1) integration with the National Do Not Call Registry API to validate phone numbers, (2) maintenance of an internal suppression list with add/remove functionality, (3) automatic blocking of communications to numbers on either list, and (4) logging of all DNC checks for audit purposes. If this system does not perform outbound communications, document this clearly to establish the system's scope and exempt status.

---

### TCPA-004: Message Frequency Disclosure

**LEGAL QUESTION**

Does the system disclose to consumers the expected frequency of messages before obtaining consent, and does it enforce frequency limits consistent with the disclosed rate, as recommended by CTIA guidelines?

**REGULATORY STANDARD**

CTIA Messaging Principles and Best Practices; TCPA Consent Requirements

**EVIDENCE**

- `.agents/skills/vitest/references/features-snapshots.md:8` — `Snapshot tests capture output and compare against stored references.`
- `.agents/skills/vitest/references/features-snapshots.md:158` — `escapeString: false,`
- `.claude/skills/studio-testing/rules/testing-component-tests-ui-only.md:11` — `logic that cannot be captured by testing utility functions alone.`
- `.claude/skills/studio-testing/rules/testing-component-tests-ui-only.md:64` — `test('closes on Escape key', async () => {`
- `.claude/skills/studio-testing/rules/testing-component-tests-ui-only.md:67` — `await userEvent.keyboard('{Escape}')`
- `.claude/skills/studio-testing/rules/testing-e2e-shared-features.md:15` — `- Mouse/click interactions AND keyboard shortcuts (Tab, Enter, Escape, Arrow keys)`
- `.claude/skills/studio-testing/rules/testing-e2e-shared-features.md:52` — `test('Escape clears highlight', async ({ page }) => {`
- `.claude/skills/studio-testing/rules/testing-e2e-shared-features.md:54` — `await getFilterBarInput(page).press('Escape')`
- `.claude/skills/telemetry-standards/SKILL.md:55` — `- Generic "viewed" or "seen" events — already captured by pageview events`
- `.cursor/rules/studio-useStaticEffectEvent.mdc:41` — `const syncApiPrivileges = useStaticEffectEvent(() => {`

**FINDING: 🔴 High Risk**

No evidence found of TCPA-compliant message frequency disclosure or enforcement mechanisms in the analyzed code repository. The evidence consists entirely of UI testing components, design system elements, and general application infrastructure without any messaging consent flows, frequency disclosures, or rate limiting controls. This represents a risk pattern consistent with non-compliance under TCPA consent requirements and CTIA Messaging Principles.

**REMEDIATION DIRECTION**

Implement a comprehensive messaging consent system that includes: (1) clear frequency disclosure forms that specify expected message volume (e.g., "up to 5 messages per week"), (2) explicit opt-in consent capture before any messaging begins, (3) rate limiting mechanisms to enforce disclosed frequency limits, and (4) audit logging of all consent events and message send rates. Consider adding these components to your authentication flow or user preferences system, ensuring compliance documentation is maintained alongside the technical implementation.

---

### TCPA-005: Sender Identification in Messages

**LEGAL QUESTION**

Does the system include proper sender identification in all outbound messages, including the identity of the entity sending the message and how to contact them, consistent with TCPA and CTIA requirements?

**REGULATORY STANDARD**

TCPA 47 U.S.C. §227(d); CTIA Messaging Principles

**EVIDENCE**

- `.agents/skills/vitest/references/advanced-type-testing.md:125` — `## Branded Types`
- `.agents/skills/vitest/references/advanced-type-testing.md:128` — `type UserId = number & { __brand: 'UserId' }`
- `.agents/skills/vitest/references/advanced-type-testing.md:129` — `type PostId = number & { __brand: 'PostId' }`
- `apps/design-system/__registry__/default/block/chart-composed-basic.tsx:51` — `color: 'hsl(var(--brand-default))',`
- `apps/design-system/app/(app)/page.tsx:33` — `<div className="flex items-center justify-start min-h-[24px] gap-3 text-brand">`
- `apps/design-system/app/(app)/page.tsx:47` — `<div className="flex items-center justify-start min-h-[24px] text-brand">`
- `apps/design-system/components/copy-button.tsx:74` — `{hasCopied ? <Check className="h-3 w-3 text-brand-600" /> : <Copy className="h-3 w-3" />}`
- `apps/design-system/components/mdx-components.tsx:88` — `'text-foreground underline decoration-1 decoration-foreground-muted underline-offset-4 transition-colors hover:decoratio`
- `apps/design-system/content/docs/tailwind-classes.mdx:19` — `- `brand``
- `apps/design-system/content/docs/tailwind-classes.mdx:158` — `### Brand`

**FINDING: 🔴 High Risk**

No evidence of sender identification mechanisms was found in the codebase that would satisfy TCPA requirements for outbound messages. The evidence shows only UI branding and styling elements (such as brand colors and text styling in design system files), but contains no message templates, sender information fields, contact details, or messaging infrastructure that would include required sender identification. This represents a risk pattern consistent with non-compliance under TCPA 47 U.S.C. §227(d) and CTIA Messaging Principles.

**REMEDIATION DIRECTION**

Implement sender identification in all outbound message templates and messaging systems. This should include: (1) Clear identification of the sending entity/business name in message content, (2) Contact information such as phone number, email, or physical address, (3) Standardized message headers or footers containing this information, and (4) Configuration systems to ensure sender identification is automatically included in all outbound communications. Review existing messaging workflows to ensure compliance before any messages are sent to users.

---

### TCPA-006: Record Keeping of Consent

**LEGAL QUESTION**

Does the system maintain records of consent that would be sufficient to demonstrate compliance in the event of a dispute, including the date, time, method of consent, and the specific consent language presented to the consumer?

**REGULATORY STANDARD**

TCPA 47 CFR §64.1200; FCC Declaratory Rulings on Consent Records

**EVIDENCE**

- No matching code patterns found.

**FINDING: 🔴 High Risk**

No evidence found of TCPA consent record-keeping mechanisms within the analyzed code repository. The search patterns returned no matching evidence for systems that capture, store, or maintain records of consumer consent including required elements such as date, time, method of consent, and specific consent language. This absence represents a risk pattern consistent with non-compliance under TCPA 47 CFR §64.1200 and FCC Declaratory Rulings on Consent Records.

**REMEDIATION DIRECTION**

Implement a comprehensive consent management system that captures and stores all required TCPA consent elements in a structured database. This should include creating database schemas to store consent timestamps, the exact method of consent collection (web form, SMS, voice, etc.), the complete consent language presented to consumers, and unique identifiers linking consent to specific phone numbers. Additionally, implement audit trails and data retention policies to ensure these records remain accessible for potential disputes or regulatory inquiries.

---

### TCPA-007: Revocation of Consent Handling

**LEGAL QUESTION**

Does the system honor revocation of consent through any reasonable means indicated by the consumer, not limited to specific keywords, and process revocation within a reasonable timeframe, consistent with FCC guidance?

**REGULATORY STANDARD**

TCPA 47 U.S.C. §227(b)(1)(A); FCC 2015 TCPA Omnibus Declaratory Ruling

**EVIDENCE**

- `.agents/skills/vitest/references/core-cli.md:94` — `--bail <n>                # Stop after n failures`
- `.agents/skills/vitest/references/core-config.md:115` — `// Stop after first failure`
- `.agents/skills/vitest/references/features-concurrency.md:230` — `Stop after first failure:`
- `.agents/skills/vitest/references/features-concurrency.md:233` — `vitest --bail 1    # Stop after 1 failure`
- `.agents/skills/vitest/references/features-concurrency.md:234` — `vitest --bail      # Stop on first failure (same as --bail 1)`
- `.agents/skills/vitest/references/features-coverage.md:129` — `/* v8 ignore stop -- @preserve */`
- `.claude/skills/studio-testing/SKILL.md:39` — `- `testing-extract-logic` - Remove logic from components into `.utils.ts` files`
- `.claude/skills/studio-testing/rules/testing-extract-logic.md:10` — `Remove as much logic from components as possible. Put it in co-located`
- `.claude/skills/telemetry-standards/SKILL.md:18` — `opened, clicked, submitted, created, removed, updated, intended, evaluated, added,`
- `.cursor/rules/docs/docs-embeddings-generation/RULE.md:63` — `6. **Cleanup**: Removes outdated pages using version tracking`

**FINDING: 🔴 High Risk**

No evidence found of TCPA consent revocation handling mechanisms in the codebase. The evidence shows only generic system operations like test failures, component removal, and event listener cleanup, but contains no telecommunications-specific consent management, opt-out processing, or revocation handling code. This represents a risk pattern consistent with non-compliance under TCPA 47 U.S.C. §227(b)(1)(A) and FCC 2015 TCPA Omnibus Declaratory Ruling requirements.

**REMEDIATION DIRECTION**

Implement a comprehensive consent revocation system that: 1) Accepts revocation requests through multiple channels (SMS replies, web interface, phone calls) without requiring specific keywords, 2) Processes revocation requests immediately or within industry-standard timeframes (typically within 24-48 hours), 3) Maintains audit logs of all revocation requests and processing timestamps, 4) Automatically updates contact preferences across all communication systems, and 5) Provides confirmation to consumers when revocation is processed. The system should recognize common opt-out language like "STOP", "UNSUBSCRIBE", "REMOVE", and natural language requests.

---

### TCPA-008: Time of Day Restrictions

**LEGAL QUESTION**

Does the system enforce time-of-day restrictions for outbound calls and messages, ensuring they are not sent before 8:00 AM or after 9:00 PM in the recipient's local time zone, as required under 47 CFR §64.1200(c)(1)?

**REGULATORY STANDARD**

TCPA 47 CFR §64.1200(c)(1) (Time of Day Restrictions)

**EVIDENCE**

- `.github/dependabot.yml:5` — `schedule:`
- `.github/workflows/ai-tests.yml:12` — `schedule:`
- `.github/workflows/dashboard-pr-reminder.yml:4` — `schedule:`
- `.github/workflows/docs-last-changed.yml:4` — `schedule:`
- `.github/workflows/docs-lint-v2-scheduled.yml:1` — `name: '[Docs] Lint v2 (scheduled)'`
- `.github/workflows/docs-lint-v2-scheduled.yml:3` — `schedule:`
- `.github/workflows/docs-mgmt-api-update.yml:4` — `schedule:`
- `.github/workflows/docs-tests-smoke.yml:7` — `schedule:`
- `.github/workflows/publish_image.yml:5` — `schedule:`
- `.github/workflows/publish_image.yml:28` — `type=sha,prefix={{date 'YYYY.MM.DD'}}-sha-,enable=${{ github.event_name == 'schedule' }}`

**FINDING: 🔴 High Risk**

No evidence found of time-of-day restrictions for outbound calls and messages in the code repository, creating a risk pattern consistent with non-compliance under 47 CFR §64.1200(c)(1). While the repository contains numerous scheduling configurations in GitHub workflow files and references to timezone handling (apps/design-system/registry/default/example/select-scrollable.tsx:15), there are no implementations that enforce the required 8:00 AM to 9:00 PM restriction in recipient local time zones for communications.

**REMEDIATION DIRECTION**

Implement time-of-day validation logic that checks recipient local time zones before sending any outbound calls or messages. This should include: (1) timezone detection or storage for each recipient, (2) validation functions that prevent communications before 8:00 AM or after 9:00 PM in the recipient's local time, (3) queue management to defer messages that fall outside permitted hours, and (4) comprehensive logging of time-based restrictions. Consider integrating this validation into your existing scheduling infrastructure referenced throughout the workflow files.

---

**DISCLAIMER:** OpenDocket identifies risk patterns through automated code analysis. Findings represent potential areas of concern, not legal determinations. This report does not constitute legal advice. Regulatory compliance requires qualified legal and technical assessment. Consult a licensed attorney and certified compliance professional for definitive compliance determination.
