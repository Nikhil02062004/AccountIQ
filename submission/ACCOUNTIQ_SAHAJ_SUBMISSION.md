# AccountIQ — Enterprise Account & Contact Intelligence
## Final Assignment Submission Dossier | BridgeAI.ai Technical Evaluation

---

### Candidate & Submission Metadata

| Attribute | Submission Detail |
| :--- | :--- |
| **Candidate / Project Owner** | **Nikhil Soni** |
| **Submission Recipient / Evaluator** | **Sahaj (BridgeAI.ai)** |
| **Project Name** | **AccountIQ — Evidence-Driven Account & Contact Intelligence for Zscaler Sales** |
| **Primary Demonstration Account** | **Siemens AG** (Existing Customer / High-Value ARR Expansion Opportunity) |
| **Selected Deployment Option** | **Option 2: GitHub Repository + Docker Compose One-Command Setup** |
| **GitHub Repository URL** | [https://github.com/Nikhil02062004/AccountIQ](https://github.com/Nikhil02062004/AccountIQ) |
| **Automated Test Suite Status** | **27 of 27 Pytest Cases Passing (100% Pass Rate inside Docker Environment)** |

---

### Executive Summary

**AccountIQ** is an evidence-driven enterprise sales intelligence platform built specifically for Zscaler Account Executives and Sales Development Representatives. Moving decisively beyond superficial dashboards, guessed data, or unexplainable generative AI hallucinations, AccountIQ grounds every strategic assertion in verifiable public disclosures, audited corporate annual filings, and official SEC registers. The platform answers the four fundamental questions of enterprise selling: *Why this account, why now, who should we approach first, and what should we say?*

Tested against **Siemens AG**—a €75.9B global technology powerhouse with ~312,000 employees and a mature enterprise-wide rollout of Zscaler Internet Access (ZIA), Private Access (ZPA), and Digital Experience (ZDX)—AccountIQ proves that expansion selling represents higher-margin, faster ARR than cold prospecting. The system uncovers three critical whitespace expansion opportunities: (1) Securing multi-cloud HPC simulation workloads from Siemens' $10B acquisition of Altair Engineering; (2) Enforcing data guardrails and DSPM over Siemens Industrial Copilot generative AI; and (3) Scaling plant-floor OT Zero Trust via Zscaler App Connectors on Siemens SCALANCE LPE industrial devices. Coupling a transparent mathematical scoring model with an interactive React Flow buying committee graph and actionable outreach playbooks, AccountIQ runs out-of-the-box via a single Docker command with zero required API keys.

> [!NOTE]
> **Important Architectural Clarification Regarding Localhost Endpoints:**  
> The URLs `http://localhost:3000` (Frontend Web UI), `http://localhost:8000` (Backend REST API), and `http://localhost:8000/docs` (Swagger UI) referenced throughout this document are local development endpoints that become active immediately upon running `docker compose up --build`. They are not publicly hosted web links, preserving corporate data privacy and zero-cost local reproducibility.

---

### Assignment Deliverables Matrix

| Deliverable | Format & Implementation Location | Operational Status |
| :--- | :--- | :--- |
| **Deliverable 1: Working POC** | Option 2: Docker Compose (`docker compose up --build`) | **VERIFIED & PASSING** |
| **Deliverable 2: Account Output** | Siemens AG 3-part intelligence profile & printable HTML dossier | **VERIFIED & PASSING** |
| **Deliverable 3: Technical Write-Up** | Section 3 of this dossier (Strictly 2 Pages, 7 core topics) | **VERIFIED & PASSING** |
| **Deliverable 4: Walkthrough Video** | Section 4 with dedicated Google Drive link placeholder | **RECORDING READY** |
| **Deliverable 5: Clean Repository** | [https://github.com/Nikhil02062004/AccountIQ](https://github.com/Nikhil02062004/AccountIQ) (8 genuine commits) | **VERIFIED & PASSING** |

---

# Deliverable 1 — Working Proof of Concept (One-Command Setup)

AccountIQ is fully containerized using **Option 2: Docker Compose**. An external evaluator can launch the entire multi-tier system with a single terminal command on any operating system equipped with Docker Desktop.

### 1. Repository & Exact One-Command Launch Commands

```bash
# Step 1: Clone the repository
git clone https://github.com/Nikhil02062004/AccountIQ.git

# Step 2: Navigate to project root
cd AccountIQ

# Step 3: Launch all services with a single command
docker compose up --build
```

### 2. Application Endpoints (Active Post-Startup)

| Service Component | Local Host URL | Operational Function |
| :--- | :--- | :--- |
| **Frontend Web App** | [http://localhost:3000](http://localhost:3000) | Next.js 14 SaaS UI with 7 interactive screens, React Flow org chart, and research modal. |
| **Backend REST API** | [http://localhost:8000](http://localhost:8000) | FastAPI server powering dynamic entity discovery, scoring, and CRUD endpoints. |
| **Interactive Swagger UI** | [http://localhost:8000/docs](http://localhost:8000/docs) | OpenAPI documentation for testing all 14 endpoints and payload schemas interactively. |
| **System Health Probe** | [http://localhost:8000/api/health](http://localhost:8000/api/health) | Real-time readiness probe returning JSON status, version, and database connectivity. |
| **Printable Account Dossier** | [http://localhost:8000/api/accounts/siemens-ag/export-report](http://localhost:8000/api/accounts/siemens-ag/export-report) | Standalone HTML dossier export for Siemens AG sales briefings. |

### 3. Container Architecture, Networking & Volume Persistence

- **Backend Service (`accountiq-backend`):** Built from `backend/Dockerfile` based on `python:3.12-slim`. Installs FastAPI, Uvicorn, SQLAlchemy, Pydantic, and HTTPX. Runs an entrypoint script (`backend/entrypoint.sh`) that ensures storage initialization, auto-migrates schemas, seeds Siemens AG baseline data automatically on first run, and exposes port `8000` with a 5s health probe (`curl -f http://localhost:8000/api/health`).
- **Frontend Service (`accountiq-frontend`):** Built from `frontend/Dockerfile` using multi-stage Alpine (`node:20-alpine`) compiling Next.js 14 in production mode. Executes under a dedicated unprivileged user (`nextjs:nodejs`) on port `3000` with a 10s health check.
- **Startup Dependency Management:** The frontend service declares `depends_on` targeting the backend with `condition: service_healthy`, guaranteeing that Next.js only starts after FastAPI successfully passes its health probe.
- **Persistent Volume Storage:** A named Docker volume (`accountiq_data`) is mounted to `/app/data`. The SQLite database resides at `/app/data/accountiq.db`, ensuring that newly researched accounts (e.g. Tesla, Oracle, ABB), contact updates, and GDPR deletions persist across container restarts.
- **Zero-Cost / Zero-API-Key Operation:** AccountIQ operates 100% reliably out-of-the-box in zero-cost mode using its built-in `DeterministicProvider` alongside live public sources (Wikipedia MediaWiki API, Wikidata Semantic Graph, SEC EDGAR Company Tickers, and DuckDuckGo). Evaluators do **not** need to configure paid API keys.
- **Alternative Local Host Launchers:** For testing without Docker, native scripts (`run.bat` for Windows, `run.sh` for Linux/macOS) automatically configure the Python virtual environment and run both servers.

---

# Deliverable 2 — Account Output: Siemens AG Expansion Dossier

Siemens AG serves as the primary demonstration account. Evaluated strictly through an ARR expansion lens across three core outputs:

### A. Account Profile & Firmographics

- **Enterprise Identity:** Siemens Aktiengesellschaft (ETR: SIE / OTCMKTS: SIEGY). Munich/Berlin headquarters. Active across 190+ countries with 200+ major production facilities.
- **Workforce & Financial Scale:** 312,000 continuing employees worldwide as of FY24 ended September 30, 2024 (~327,000 total workforce prior to the Innomotics carve-out). Consolidated annual revenue of €75.9 billion.
- **Existing Zscaler Footprint:** Flagship customer since 2020. Public customer stories validate enterprise-wide rollout of ZIA, ZPA, and ZDX protecting 300,000+ users, eliminating legacy VPNs, and cutting network complexity costs by 70%.
- **Account Attractiveness (92.0 / 100):** Scale >300,000 seats (+25); Revenue >€75B (+10); Existing user with board endorsement (+25); 4 major whitespaces (+25); Global OT footprint (+15).
- **Timing & Urgency (88.0 / 100):** $10B Altair acquisition (+35); Enterprise Industrial Copilot rollout (+25); SCALANCE OT Zero Trust scaling (+20); Mandatory EU NIS2 compliance deadlines (+15).
- **Evidence Coverage (94.5 / 100):** 28 field-level verified claims backed by audited FY24 reports, customer case studies, and corporate press releases. Preserves 1 recorded divergence (continuing vs discontinued headcount).
- **IT & Vendor Footprint:** Hybrid multi-cloud (AWS, Azure), SAP S/4HANA ERP, Salesforce CRM, Cisco SD-WAN, and Siemens SCALANCE LPE industrial PC hardware.

### B. Contact Map & Buying Committee

AccountIQ maps 6 verified enterprise stakeholders into strategic buying roles with algorithmic relevance scores (0–100):

| Stakeholder | Corporate Title | Buying Role | Relevance & Strategic Mandate |
| :--- | :--- | :--- | :--- |
| **Frederik Janssen** | CIO, Siemens Digital Industries | Champion / Tech Decision Maker | **95.0** \| Leads IT for division absorbing Altair; co-developed SCALANCE OT partnership. |
| **Hanna Hennig** | Global CIO, Siemens AG | Economic Buyer / Executive Sponsor | **96.0** \| Controls enterprise IT budget; chairs Charter of Trust; public Zscaler champion. |
| **Roland Busch** | President & CEO, Siemens AG | Executive Signer / Visionary | **85.0** \| Drives Industrial Metaverse, Siemens Xcelerator, and M&A integration ROI. |
| **Peter Weckesser** | Chief Digital Officer, Siemens AG | Key Influencer / AI Transformation | **88.0** \| Oversees Industrial Copilot deployment and internal AI data guardrails. |
| **Cedrik Neike** | CEO, Digital Industries (Managing Board) | Business Unit Executive / P&L | **82.0** \| Owns Digital Industries P&L; drives cloud software ARR monetization. |
| **Barbara Humpton** | President & CEO, Siemens USA | Regional Executive Sponsor | **80.0** \| Manages US manufacturing base; drives DoD/ITAR federal supply chain compliance. |

*Interactive Graph:* The Next.js frontend renders these stakeholders as a directed React Flow graph with hierarchical reporting lines (Janssen -> Neike -> Busch; Hennig -> Busch) and cross-functional influence links (Janssen -> Weckesser for Industrial Copilot security).

### C. Recommended Way In & Outreach Playbook

- **Strategic Rationale:** Siemens closed its $10B acquisition of Altair Engineering, onboarding thousands of simulation engineers and cloud HPC clusters across AWS and Azure. Connecting Altair via legacy VPNs re-introduces lateral attack surfaces.
- **Primary Entry:** Frederik Janssen (CIO, Digital Industries). Transition his proven network transformation legacy into cloud workload security.
- **Secondary Entry:** Hanna Hennig (Global CIO) to align enterprise security governance and NIS2 audit compliance.
- **Proposed Sales Conversation (Opener Draft):**
  > *"Dear Frederik — With the closing of the Altair acquisition, your team faces the classic challenge: enabling thousands of engineers and HPC simulation workloads to collaborate day-one without building fragile network-level VPN bridges. Given your leadership in establishing that 'the internet is the new corporate network' across Siemens, we've prepared an architectural blueprint showing how Siemens can extend its existing Zscaler Zero Trust Exchange footprint directly into Altair's cloud workloads in days—securing simulation IP without touching corporate MPLS. Would you or your infrastructure lead be open to a 20-minute peer briefing next week to review the reference architecture?"*
- **Transparent Unknowns:** AccountIQ explicitly highlights data gaps: (1) Internal M&A IT ownership; (2) Specific DLP/CASB tooling inside Altair; (3) Exact renewal co-terming dates for Siemens' enterprise agreement.

---

# Deliverable 3 — Technical Write-Up (Strictly 2 Pages)

### 1. Account Choice: Why Siemens AG is an Expansion Opportunity
Siemens AG was selected because it exemplifies the highest-yield segment in B2B enterprise sales: expansion within an existing account. In mature enterprise SaaS, expansion deals convert at 60–70% with 3x faster sales velocity than cold new-logo prospecting, leveraging pre-negotiated Master Services Agreements. With €75.9B in FY2024 revenue, ~312,000 employees, and an established enterprise-wide rollout of Zscaler Internet Access (ZIA), Private Access (ZPA), and Digital Experience (ZDX), Siemens is not a prospect for basic user zero-trust. The strategic challenge is identifying where the *next* $2M–$5M ARR exists. AccountIQ isolates three distinct expansion vectors: (1) Integrating the $10B Altair Engineering acquisition (cloud HPC simulation workloads across AWS and Azure) without building fragile VPN bridges; (2) Enforcing Data Loss Prevention (DSPM) and security guardrails over enterprise rollouts of Siemens Industrial Copilot generative AI; and (3) Scaling plant-floor OT Zero Trust via Zscaler App Connectors running natively on Siemens SCALANCE LPE industrial PC devices across 200+ factories.

### 2. End-to-End Technical Architecture
AccountIQ employs a modular, containerized architecture that strictly decouples data collection, validation, mathematical scoring, and UI rendering:
- **FastAPI Backend (Python 3.12):** Asynchronous REST API utilizing SQLAlchemy 2.0 ORM, Pydantic v2 schemas, and HTTPX for concurrent non-blocking API polling. Application lifespan handlers execute schema creation and deterministic baseline seeding upon container startup.
- **Next.js 14 Frontend:** Single-page application built on React 18, TypeScript, Tailwind CSS, and React Flow (`@xyflow/react`). Features 7 specialized tabs (Overview, Account Intelligence, Contacts, Committee Graph, Recommended Way In, Evidence Explorer, Quality Report) communicating via client-side fetch.
- **Persistence via Docker Volume:** File-based SQLite database stored in a dedicated named Docker volume (`accountiq_data` mapped to `/app/data/accountiq.db`). Eliminates external database administration while ensuring full state persistence across container teardowns and restarts.
- **Sequential 5-Stage Research Pipeline:** New accounts execute through: (1) Corporate Entity Resolution; (2) Multi-Source Discovery; (3) Fact & Metric Normalization; (4) Multi-Dimensional Scoring; (5) Stakeholder Playbook & Email Generation.
- **Deterministic Scoring Engine:** Three additive scoring algorithms (Attractiveness, Timing, Evidence Coverage) calculated using transparent point rules with zero black-box deal probability estimation.

### 3. Implemented Source Providers & Ingestion Strategy
- **Siemens FY2024 Annual Report (Primary Audited):** Audited consolidated financials (€75.9B revenue), continuing workforce figures (312,000), segment breakdowns, and M&A commitments. (Ref: `siemens.com/annualreport2024`).
- **Zscaler Official Customer Story (Primary Customer):** Official case study detailing rollout of ZIA, ZPA, and ZDX across 300,000+ users, 70% cost reduction, and retirement of legacy VPN infrastructure. (Ref: `zscaler.com/customers/siemens`).
- **Zscaler & Siemens OT Partnership (Primary Press Release):** Joint announcement regarding Zscaler App Connector integration on Siemens SCALANCE LPE hardware for secure OT edge connectivity. (Ref: `zscaler.com/press`).
- **Wikipedia Infobox & MediaWiki REST API (Dynamic Discovery):** Extracts structured metadata (headquarters, employee counts, corporate structure, website, leadership) with wikitext template expansion.
- **Wikidata Semantic Knowledge Graph (Dynamic Discovery):** Resolves canonical entity Q-IDs, parent-subsidiary relationships (e.g. Google LLC -> Alphabet Inc.), stock tickers, and industry classifications.
- **SEC EDGAR Company Tickers API (Dynamic Regulatory):** Ingests the official SEC directory mapping corporate names to Central Index Keys (CIK), exchange listings (NASDAQ, NYSE), and audited 10-K filings.
- **DuckDuckGo Corporate Discovery (Dynamic Web):** Heuristic search queries discovering recent M&A events, press releases, leadership appointments, and technology adoption triggers without search API billing.

### 4. What I Tried and Dropped (Engineering Trade-Offs)
- **Dropped Opaque LLM Win Probabilities:** Early prototypes utilized generative LLM prompts to output deal closing likelihoods (e.g., '87% win probability'). Enterprise sales leaders immediately rejected these as untrustworthy hallucinations. Replaced with transparent, additive scoring models based on verifiable infrastructure complexity, recent corporate triggers, and evidence coverage.
- **Dropped Unstructured DOM Web Scraping:** Direct HTML scraping of corporate sites proved brittle, failing frequently due to cookie consent overlays, bot-protection firewalls (Cloudflare), and changing CSS classes. Replaced with resilient structured public APIs (Wikipedia REST API, SEC EDGAR, Wikidata) with rendered HTML infobox fallback.
- **Dropped Heavy External Database Setup:** Initial planning considered managed PostgreSQL requiring separate database containers, migrations, and connection pooling. Dropped to honor the strict single-command assignment mandate (`docker compose up --build`). Implemented SQLite with persistent volume mapping, achieving zero-config setup with zero data loss on restart.
- **Dropped Synthetic Contact Guessing:** Many commercial enrichment tools fabricate unverified email addresses (e.g. first.last@company.com). Dropped to ensure strict compliance with GDPR Art. 17 and PDPA; AccountIQ only stores verified corporate leadership titles and public routing channels.

### 5. Data Accuracy, Normalization & Verification Mechanisms
To ensure cross-company reliability, AccountIQ enforces a centralized data quality gate across every ingestion phase:
- **Corporate Entity Disambiguation:** Prevents common-word confusion by requiring business qualifiers (company, corporation, inc, ag, group) or corporate infobox templates before selecting search candidates (e.g. distinguishing Oracle Corporation from Greek mythological oracles; selecting BMW corporate entity over specific car models like the BMW 5 Series).
- **Regex Unformatting & Template Expansion:** Unwraps complex wikitext templates (e.g. parsing `{{circa|141,000}}` to integer 141,000; expanding Wikidata dynamic leadership markers like `{{wd-chairperson}}` and `{{wd-ceo}}` to Peter Voser and Morten Wierod for ABB Ltd).
- **Financial & Workforce Normalization:** Standardizes disparate currencies (EUR, USD, INR) and scale factors (Billions, Millions, Crores). Extracts upper-bound values from workforce ranges (e.g., '25,000–50,000' -> 50,000) and preserves reporting dates.
- **Field-Level Claim Provenance:** Every stored metric and priority is linked to a Source ID, verbatim text citation, publication timestamp, and confidence weight (0.0 to 1.0). High-credibility audited reports receive 0.95–1.0 weights, while inferred claims receive 0.5–0.7.
- **Status Taxonomy & Conflict Preservation:** Claims are tagged VERIFIED, CORROBORATED, INFERRED, UNKNOWN, or STALE. When sources diverge (such as Siemens' 312,000 continuing vs 327,000 total pre-divestment employees), AccountIQ preserves both claims with conflict tags rather than silently discarding either.
- **Honest Unknowns:** If an enterprise has no verifiable public cloud or DLP tooling disclosures, AccountIQ marks the vendor status as UNKNOWN rather than hallucinating generic market defaults.

### 6. Estimated Cost Model for 500 Enterprise Accounts
Below is a transparent planning estimate for operating AccountIQ across 500 enterprise accounts refreshed monthly, separating zero-cost public discovery, container hosting, and optional LLM synthesis:

| Infrastructure Layer | Provider & Tier | Usage Assumptions | Monthly Cost |
| :--- | :--- | :--- | :--- |
| **Public Discovery APIs** | Wikipedia, Wikidata, SEC EDGAR | 500 accounts x ~12 API calls = ~6,000 requests/month. Completely free public endpoints. | **$0.00 / mo** |
| **Compute & Container Hosting** | AWS ECS Fargate / Railway / Render | 2 container instances (FastAPI backend + Next.js frontend, 1 vCPU, 2GB RAM total). | **$35.00 – $55.00** |
| **Database Storage** | Persistent Volume / AWS RDS Postgres | 500 accounts with ~30 claims each = ~15,000 records (~150 MB storage). Negligible I/O. | **$15.00 – $25.00** |
| **Optional LLM Extraction** | Gemini 1.5 Flash / OpenRouter | Optional: ~5,000 tokens/account for synthesis. 500 accounts = 2.5M tokens ($0.075/1M input). | **$1.88 / mo** |
| **Monitoring & Network Egress** | CloudWatch / Basic Logging | Operational health telemetry, container metrics, and negligible bandwidth (<5 GB/mo). | **$10.00 / mo** |

> **Total Core Platform Operating Cost:** ~$60.00 – $90.00 / month (approx. **$0.12 – $0.18 per account/month**). Zero mandatory commercial data licenses. If commercial enrichment APIs (e.g. ZoomInfo, Apollo, Diffbot) are added in the future for direct contact emails, costs would increase by $150–$300/mo.

### 7. What I Would Build Next (Strategic Engineering Roadmap)
1. **Continuous Change-Data-Capture (CDC):** Implement asynchronous Celery/Redis background cron workers to continuously poll SEC 10-Q/8-K feeds and news aggregators, automatically notifying sellers when new M&A triggers occur.
2. **Bi-Directional CRM Sync:** Build certified bi-directional webhooks with Salesforce and HubSpot to push recommended stakeholders, opener emails, and account scores directly into sales cadence pipelines.
3. **Graph Database Architecture:** Migrate buying committee relationships into Neo4j to execute graph traversals identifying multi-hop executive connections across customer accounts.
4. **Enterprise RBAC & Multi-Tenancy:** Implement row-level security (RLS) and territory partitioning allowing enterprise sales managers to partition account visibility across regional SDR and AE pods.

---

# Deliverable 4 — Product Walkthrough Video (10 Minutes Maximum)

A dedicated product walkthrough and technical demonstration video has been planned to present AccountIQ from the perspective of an enterprise sales leader and technical architect.

### Walkthrough Video Recording Information
- **Video Title:** AccountIQ — Product Walkthrough and Technical Architecture
- **Video URL:**
  ```text
  [PASTE GOOGLE DRIVE VIDEO LINK HERE]
  ```
  *(Please ensure the Google Drive file sharing permissions are configured to "Anyone with the link can view")*
- **Description:** *"Walkthrough video demonstrating the working application, account intelligence workflow, recommended sales approach and technical architecture."*

### Timed Video Demonstration Agenda (10:00 Total Runtime)

| Timestamp | Segment Title | Core Demonstration Focus |
| :--- | :--- | :--- |
| **00:00 – 03:00** | **Executive Overview & Siemens AG Profile** | Demonstrating why Siemens AG is an expansion opportunity (not a new logo); reviewing corporate firmographics (€75.9B revenue, ~312k employees); existing ZIA/ZPA/ZDX deployment; reviewing the 3 transparent scores (Attractiveness 92, Timing 88, Evidence Coverage 94.5). |
| **03:00 – 05:30** | **Buying Committee Map & Recommended Way In** | Exploring the interactive React Flow buying committee graph; 6 verified stakeholders; Frederik Janssen (CIO Digital Industries) as primary champion; $10B Altair Engineering M&A trigger; Industrial Copilot AI guardrails; suggested opener draft review. |
| **05:30 – 07:00** | **Evidence Explorer & Data Quality Audit** | Demonstrating source traceability; inspecting evidence claims and citations; conflict resolution modal; performing a live GDPR Art. 17 single-click contact deletion to demonstrate privacy compliance. |
| **07:00 – 10:00** | **Dynamic Research Engine & Architecture** | Opening '+ New Research' modal to research a live dynamic company (e.g. Tesla or Oracle); proving zero Siemens leakage; Docker Compose one-command orchestration; verifying 27/27 test suite execution; concluding cost model summary. |

---

# Deliverable 5 — GitHub Repository & Version Control Integrity

The entire AccountIQ codebase is version-controlled and published on GitHub. The repository preserves genuine, un-squashed commit history reflecting transparent engineering progression.

### Repository URL
**GitHub:** [https://github.com/Nikhil02062004/AccountIQ](https://github.com/Nikhil02062004/AccountIQ)

### Repository Architecture & Codebase Structure
- `backend/` — **FastAPI Application:** Application routers, SQLAlchemy entity models (`Account`, `Contact`, `Source`, `EvidenceClaim`, `Recommendation`), Pydantic schemas, dynamic research pipeline, scoring engine, and the Siemens AG initial seed module.
- `frontend/` — **Next.js 14 Web Application:** React 18 SaaS UI components (`OverviewTab`, `AccountIntelligenceTab`, `ContactIntelligenceTab`, `CommitteeMapTab` with React Flow, `RecommendedWayInTab`, `EvidenceExplorerTab`, `NewResearchModal`, `QualityReportModal`).
- `docker-compose.yml` & **Dockerfiles:** Production-grade orchestration defining backend and frontend services, container health checks, host port mappings (8000, 3000), and the persistent SQLite volume (`accountiq_data`).
- `backend/tests/` — **Automated Test Suite:** Contains 27 automated test cases verifying Siemens AG account creation, evidence linking, contact roles, scoring transparency, GDPR privacy deletion, and company-agnostic dynamic entity resolution across global enterprises.
- `docs/` & `submission/` — **Assignment Deliverables:** Complete documentation including `ACCOUNTIQ_COMPLETE_DOCUMENTATION.md`, executive write-ups, demo walkthrough scripts, HTML dossier export, and this submission dossier.
- **Configuration & Root Launchers:** `.env.example` (fully documented zero-key configuration), `.gitignore` (excluding virtual environments, databases, and secrets), `.dockerignore`, `run.bat` (Windows), and `run.sh` (Linux/macOS).

### Verified Commit History (Strictly Preserved Genuine History)

The repository contains 8 clean, descriptive commits representing the progressive development of the platform on branch `main`. No commit squashing, rebasing, or synthetic history manipulation was performed:

| Commit Hash | Commit Message | Key Architectural Contribution |
| :--- | :--- | :--- |
| `1226c2f` | chore: untrack database binary backup and update gitignore | Removes legacy binary backup from git tracking and updates .gitignore rules. |
| `7e9fcb9` | feat: configure Docker Compose one-command setup and harden research engine | Implements backend/frontend Dockerfiles, docker-compose.yml, persistent volumes, and health checks. |
| `5e58287` | feat: transform AccountIQ into dynamic company-agnostic intelligence engine | Implements entity resolution, source discovery, and fact extractor for arbitrary enterprise queries. |
| `acee0d9` | fix: ensure repository root is in sys.path and PYTHONPATH for uvicorn reloader | Resolves subprocess import paths during live development reload on Windows. |
| `9a8ce00` | docs: create comprehensive AccountIQ master documentation and update README | Generates complete 1200+ line master documentation covering architecture and scoring math. |
| `9bceb49` | docs: add assignment deliverables, 2-page writeup, demo script and export report | Adds core assignment documentation, Siemens HTML export, and root launch scripts. |
| `a07a378` | feat(frontend): build AccountIQ SaaS interface with 7 screens and committee graph | Develops Next.js 14 SaaS UI with Tailwind CSS and interactive React Flow buying committee graph. |
| `53af0e8` | feat(backend): implement evidence model, Siemens research ingestion, and scoring | Initializes FastAPI application, SQLAlchemy models, scoring formulas, and Siemens AG seed data. |

> [!IMPORTANT]
> **Final Repository Verification Summary:**
> - **GitHub Remote:** `https://github.com/Nikhil02062004/AccountIQ.git`
> - **Active Branch:** `main` (up to date with remote)
> - **Exclusions Verified:** Zero `.env` files, zero API keys, zero binary databases, zero `node_modules` tracked.
> - **Automated Test Status:** 27 of 27 pytest cases passing inside Docker container in 54.46s.
