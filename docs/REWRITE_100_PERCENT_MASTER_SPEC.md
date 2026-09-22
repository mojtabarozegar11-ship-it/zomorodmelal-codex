# Zomorod Melal — 100% Rewrite Master Specification

## دستور اجرایی
این سند مبنای بازنویسی کامل پروژه است. هدف، ایجاد یک سیستم واحد و قابل‌تست است که وب‌سایت و Master Agent را از نظر قراردادها، وضعیت، مأموریت‌ها، محتوا، تحقیق، انتشار، گزارش‌دهی و کنترل‌های عملیاتی یکپارچه کند؛ نه دو پروژه مستقل.

## 1. اصول غیرقابل‌مذاکره
- یک هسته اجرایی؛ یک مدل وضعیت؛ یک قرارداد مأموریت؛ یک Audit Trail.
- Website = Public Experience + Public Content.
- Android/Admin = Control Plane و محل کنترل، تأیید، مشاهده و گزارش.
- هر عملیات حساس باید policy، approval، actor، timestamp، idempotency و audit داشته باشد.
- کلیدهای API، رمزها و credentialها فقط از محیط/secret store خوانده شوند.
- هیچ تاریخ، خبر، پژوهش، نقل‌قول مدیرعامل، نتیجه آزمایش یا سابقه انتشار بدون سند ساخته نشود.
- داده تاریخی بازسازی‌نشده فقط با برچسب reconstructed / backfilled ثبت شود.
- انتشار عمومی از داخل اپ مدیریتی انجام نمی‌شود؛ اپ مدیریتی فقط کنترل عملیات را ارائه می‌کند.
- «آمادگی معماری» با «اثبات production» یکی نیست و تا زمانی که runtime و integration gateها واقعاً اجرا نشده‌اند، وضعیت production-certified اعلام نمی‌شود.

## 2. معماری نهایی

Browser / Search / Social
→ Django Website
→ Site-Agent Bridge
→ Master Agent Runtime
→ Mission Planner
→ Policy / Approval Gateway
→ Capability Executor
→ Validation / Verification
→ Audit / Metrics / State
→ Website / Social / Control Plane

### مرزها
1. presentation: templates/static/public API
2. application: use-cases و service orchestration
3. domain: mission/capability/policy/content/research/business rules
4. infrastructure: DB, filesystem, external providers, social, payments, AI
5. control plane: admin/API/approvals/audit
6. worker/scheduler: recurring jobs، retries، quarantine
7. observability: structured events, health, metrics, reports

## 3. Website
وب‌سایت باید انگلیسی‌محور، چندزبانه، global-first و responsive باشد و فارسی را هم به‌صورت کامل پشتیبانی کند.

20 زبان پایه:
en, fa, es, zh, hi, fr, ar, bn, pt, ru, ur, id, de, ja, mr, te, tr, ta, vi, ko

سطوح اصلی:
- Home
- Agriculture Intelligence
- Agriculture Services
- Weather / Climate
- Research
- Encyclopedia
- Agricultural Economics
- Services
- Enterprise / B2B
- Marketplace architecture
- Studio / Innovation
- Company / About
- CEO Messages / Public newsroom
- Contact / service request
- SEO surfaces, sitemap, robots, structured data

هر سطح باید theme مستقل ولی هم‌خانواده داشته باشد:
- Home: Emerald + Champagne Gold
- Agriculture: Botanical Jade + Copper
- Weather: Jade + Copper
- Services: Sapphire + Platinum
- Marketplace: Obsidian + Luxury Gold
- Research: Midnight Violet + Rose Gold
- Encyclopedia: Ivory + Antique Gold
- Economy: Deep Navy + Bullion Gold
- Studio: Black Glass + Champagne
- Office: Graphite + Executive Bronze
- Architecture: Graphite + Precision Cyan

Accessibility:
- keyboard navigation
- visible focus
- reduced motion
- semantic headings
- contrast-safe tokens
- form labels/errors
- mobile touch targets
- RTL/LTR correctness

SEO:
- canonical
- hreflang architecture
- JSON-LD
- article/service/breadcrumb schemas
- dynamic sitemap
- robots
- clean slugs
- internal linking between services, research and encyclopedia

## 4. Master Agent Runtime

### چرخه اصلی
Observe → Research → Plan → Build → Test → Deploy → Measure → Improve → Repeat

### Mission object
هر mission باید حداقل این فیلدها را داشته باشد:
- id
- type
- goal
- source
- priority
- state
- requested_by
- created_at
- started_at
- finished_at
- idempotency_key
- policy
- required_approval
- approval_id
- capabilities
- inputs
- outputs
- validation
- errors
- retries
- quarantine_state
- audit_refs

### State machine
queued → researched → planned → awaiting_approval → executing → validating → completed

خطاها:
executing/validating → failed
failed → retrying
retry limit exceeded → quarantined

عملیات مجاز بدون تأیید فقط:
- health/read-only inspection
- local analysis
- sandbox generation
- test execution
- non-public draft preparation

عملیات تأییدشونده:
- production deploy
- credential changes
- payment/financial side effects
- external account mutations
- public publication where policy requires review
- security boundary changes
- destructive DB operations

## 5. Site-Agent Contract

Public-safe read path:
GET /agent-status/

Internal/control operations:
- site.health
- site.content.audit
- site.seo.audit
- site.performance.audit
- site.accessibility.audit
- site.research.prepare
- site.research.publish
- site.content.prepare
- site.content.publish
- site.release.prepare
- site.release.execute

هر operation باید:
1. schema validation
2. permission check
3. policy check
4. approval resolution
5. idempotency check
6. execution
7. post-condition verification
8. audit event

داخلی بودن endpoint نباید با مخفی‌بودن صرفاً URL فرض شود؛ authorization باید مستقل اعمال شود.

## 6. Research & Knowledge

### Scientific program
Domains:
- agricultural science
- plant research
- plant genetics
- animal genetics
- ornamental plants
- special ornamental animals
- wildlife
- biodiversity
- ecology
- conservation
- molecular biology
- biotechnology
- bioinformatics
- breeding
- propagation
- experimental design
- data analysis
- replication
- research reports

### Evidence rules
- هر ادعای مادی حداقل دو منبع معتبر تا حد امکان.
- ادعاهای کمی باید تاریخ، population/scope و source داشته باشند.
- ادعاهای علی/ژنتیکی/پزشکی/وضعیت حفاظتی باید uncertainty و scope داشته باشند.
- نقل‌قول مستقیم باید source metadata داشته باشد.
- نقل‌قول مستقیم مدیرعامل فقط با record قابل‌ردیابی.
- نتیجه آزمایش بدون experiment record ممنوع.

### Encyclopedia
Entityها:
- Entry
- EntryVersion
- EvidenceSource
- Citation
- EditorialReview
- Concept
- Relationship
- Translation
- PublicationEvent

Publication gate:
draft → evidence_checked → editorial_review → approved → published

## 7. Agricultural Research Blog
Streams:
- research notes
- scientific documentation
- agricultural news
- data briefs
- research reports
- crop/soil
- water/irrigation
- climate/weather
- pest/disease
- agricultural economics
- farm management
- market intelligence
- technology
- policy/regulatory
- case studies
- literature reviews

Daily pipeline:
discover → verify → classify → prioritize → draft → cite → inspect → review → publish/queue → link encyclopedia → graph update → metrics

## 8. Agricultural Economics
Core analyses:
- production economics
- farm management
- enterprise budgeting
- cost/return
- resource allocation
- productivity
- risk
- irrigation economics
- soil/nutrient economics
- labor/mechanization
- technology adoption
- climate resilience
- value chain
- market linkage
- policy economics
- investment/capital budgeting
- sustainability/externalities

Forecasts must be labeled as forecasts. Current numeric data must be dated.

## 9. Business & Revenue

Primary:
- specialized agricultural expert services
- general virtual/digital services
- B2B / Enterprise

Revenue rails:
- pay_per_service
- subscription
- premium
- B2B
- enterprise
- API
- reports_and_data
- custom_projects
- marketplace_commission
- white_label

Payment Core provider-neutral:
- IRR / approved local PSP
- international currencies / legally eligible approved providers
- no hard-coded PSP dependency in domain layer

Physical commerce:
kept behind future extension boundaries: SKU, inventory, warehouse, shipping, returns, supplier, fulfillment.

## 10. Social Publishing
Supported through provider-neutral integration:
Instagram, Facebook, LinkedIn, X, YouTube, TikTok, Threads, Bluesky

Modes:
- draft
- review
- scheduled
- publish
- failed
- retry

Default:
public content starts as draft/review unless explicit policy enables automatic publishing.

## 11. CEO / Company Editorial
Public surfaces only:
Website + Social.

App does not host the public editorial experience.

Required metadata:
- author
- publication timestamp
- content type
- source record
- language
- translation relationship
- approval record
- canonical URL

## 12. Android Control Plane
The mobile app is not a second public website.

Core screens:
- system status
- missions
- approvals
- agent registry
- policies
- execution history
- errors/quarantine
- research queue
- editorial queue
- social queue
- financial approvals
- deployment approvals
- emergency stop
- audit log
- configuration status

Strong authentication required for privileged actions.

## 13. Data Model
Canonical models should be normalized around:
- Organization
- User/Role
- Capability
- Policy
- Mission
- MissionStep
- Approval
- Execution
- AuditEvent
- ErrorRecord
- ContentItem
- ContentVersion
- EvidenceSource
- Citation
- ResearchProject
- ResearchFinding
- Service
- ServiceRequest
- Quote
- Order/Checkout
- PaymentAttempt
- SocialAccount
- SocialPost
- PublicationEvent
- MetricSnapshot
- HealthCheck

Every externally-effectful object needs:
created_at, updated_at, actor/context, status, and idempotency where applicable.

## 14. Reliability
- transactional boundaries around state changes
- atomic writes
- explicit retry policy
- exponential backoff
- dead-letter/quarantine
- idempotent commands
- timeout budget
- circuit breaking around unstable providers
- health probes
- structured logs
- audit correlation IDs
- rollback preparation for reversible changes

## 15. Security
- deny-by-default permissions
- least privilege
- strong admin authentication
- CSRF protection
- secure cookies
- strict host/origin policy
- HSTS in production
- secrets outside source
- no secret echo in UI
- external AI disabled until explicitly configured
- separate read/public paths from mutation paths
- destructive operations approval-gated
- complete audit trail

## 16. Testing
Required layers:
1. import/compile checks
2. unit tests
3. model/ORM tests
4. API contract tests
5. permission/policy tests
6. mission state-machine tests
7. idempotency/replay tests
8. retry/quarantine tests
9. content/evidence validation tests
10. localization tests
11. SEO tests
12. accessibility tests
13. integration tests with provider mocks
14. cPanel packaging/layout tests
15. browser E2E when browser runtime is available
16. production smoke tests after actual deployment

A green offline test suite is not equivalent to real external-provider verification.

## 17. Scheduler
Cadences:
- nightly bug/health sweep
- weekly system upgrade
- monthly product/site/app review
- continuous content/research loop under configured policy
- economics intelligence loop

All recurring tasks must create traceable mission records, not hidden side effects.

## 18. Self-Improvement
Self-improvement is controlled evolution, not unrestricted self-destruction.

Pipeline:
inspect → identify gap → generate change package → sandbox → test → validation → approval (when required) → controlled deploy → post-check → record

No direct credential exfiltration, uncontrolled destructive migration, or unreviewed production security weakening.

## 19. Deployment
Canonical Django root contains:
manage.py
config/
apps/
templates/
static/
requirements*.txt
passenger_wsgi.py

For cPanel:
- Application Root = directory containing manage.py
- Startup = passenger_wsgi.py
- Entry point = application

Before production:
- install dependencies
- run migrations
- collectstatic
- create admin
- configure secrets/env
- verify hostname/SSL
- run health endpoint
- run smoke tests
- verify logs

## 20. Definition of Done
The rewrite is complete only when:
- one canonical Django tree exists
- one canonical runtime contract exists
- website and agent communicate through one bridge
- mission lifecycle is deterministic
- privileged actions are approval-gated
- evidence gate blocks unsupported public research
- public editorial remains on website/social
- mobile is control plane
- secrets are externalized
- automated tests cover critical paths
- actual deployment smoke tests have evidence
- no orphan runtime is authoritative
- docs and code agree
- completion status is based on executed evidence, not declared percentages

## 21. Canonical implementation target
The implementation should be simplified rather than multiplied. Duplicate legacy modules should be retired only after call-site analysis and replacement verification. The runtime must expose one authoritative path for:
mission creation → policy → execution → validation → audit.

## 22. Rewrite acceptance evidence
Required artifacts:
- architecture map
- module ownership map
- dependency map
- database schema report
- API contract report
- security report
- test report
- deployment report
- runtime health report
- public-content boundary report
- evidence/encyclopedia validation report
- final release manifest

This document is a specification, not a claim that all gates have already been proven.
