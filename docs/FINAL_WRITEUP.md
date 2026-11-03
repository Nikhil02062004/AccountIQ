# AccountIQ: Account and Contact Intelligence Platform for Zscaler
**Executive Assignment Write-Up — by Sahaj Khunteta**  
*Main Account: Siemens AG (Existing Customer / High-Value Expansion Opportunity)*  

---

### 1. Account Choice & Business Justification
Siemens AG was evaluated as an **expansion opportunity**, not a new logo prospect. With ~312,000 employees globally (FY24 continuing operations) and €75.9B in revenue, Siemens is an existing flagship customer that deployed **Zscaler Internet Access (ZIA)**, **Private Access (ZPA)**, and **Digital Experience (ZDX)**. The account was selected because recent catalysts created high-urgency whitespace: Siemens' **$10B acquisition of Altair Engineering** (closed early 2025), commercial scaling of **Siemens Industrial Copilot** (GenAI), and mandatory **EU NIS2** compliance deadlines for 200+ global factories. This presents immediate expansion demand for **Zscaler Workload Communications**, **Data Protection (DSPM)**, and **Zero Trust for OT**.

### 2. Problem Framing: Why This Account, Why Now, Who to Approach, What to Say
Enterprise sales representatives waste hundreds of hours reading disjointed annual reports and CRM records. AccountIQ solves this by unifying account-level triggers with contact-level mandates:
- **Why This Account:** Massive scale (300k+ seats), proven zero-trust validation at the board level, and 4 unlocked product whitespaces.
- **Why Now:** $10B Altair HPC simulation workloads require zero-trust onboarding day-one without building fragile VPN interconnects.
- **Who to Approach First:** **Frederik Janssen**, CIO of Siemens Digital Industries (operational champion who previously coined *"the internet is the new corporate network"* and heads IT for the division absorbing Altair).
- **What to Say:** A peer-level architectural proposal on extending existing Zscaler Zero Trust Exchange directly into Altair's multi-cloud workloads and HPC clusters in days.

### 3. Reusable System Architecture
AccountIQ is structured into clean, decoupled layers to ensure complete isolation across accounts:
1. **Source Registry & Connectors:** Ingests official annual reports, press releases, leadership registries, and SEC filings.
2. **Deterministic & LLM Extraction Engine:** Extracts structured facts with Pydantic v2 schemas. Built with a `BaseLLMProvider` abstraction supporting zero-cost offline deterministic execution, optional Gemini API free tier, and OpenRouter.
3. **Evidence Validation & Provenance Engine:** Audits every claim with source URLs, publication timestamps, confidence weights (0.0–1.0), and verification status (`VERIFIED`, `CORROBORATED`, `INFERRED`, `UNKNOWN`, `STALE`). Preserves conflicting metrics (e.g., 312k continuing vs 327k total employees).
4. **Scoring Engine:** Transparent, rules-based weighted scoring for Attractiveness (92/100), Timing (88/100), Evidence Coverage (94.5/100), and Stakeholder Relevance (98/100).
5. **Interactive Frontend:** Next.js, Tailwind CSS, and React Flow for interactive buying committee visualization.

### 4. Data Sources & Selection Rationale
Sources were prioritized strictly by authority:
1. *Siemens Annual Report FY2024:* Audited baseline for €75.9B revenue and 312,000 continuing workforce.
2. *Zscaler Official Siemens Customer Story & Video:* Primary documentation of ZIA, ZPA, and ZDX adoption, 70% cost reduction, and leadership quotes from Hanna Hennig and Frederik Janssen.
3. *Zscaler & Siemens OT Partnership Press Release (May 26, 2022):* Primary evidence of SCALANCE LPE industrial edge zero-trust integration.
4. *Siemens Corporate Management Directory:* Official Managing Board appointments (Peter Koerte as CTO/CSO, Veronika Bienert as CFO).
5. *Siemens & Altair Acquisition Filing (Oct 30, 2024):* Verified $10B transaction details and HPC software scope.

### 5. What Was Attempted and Dropped
- **Dropped LLM-Generated Deal Probabilities:** Arbitrary percentages (e.g., "78% win probability") lack empirical ground truth. Replaced with an audited, rules-based *Account Attractiveness & Timing Score*.
- **Dropped Heuristic Email Guessing:** Synthesizing guessed email patterns (e.g. `first.last@siemens.com`) violates enterprise trust and privacy compliance. Contacts display *Verified Public Profiles* and corporate routing channels only.
- **Dropped Monolithic Single-File Design:** Initially considered a single-file script; separated into modular FastAPI backend and Next.js frontend to allow independent testing, automated schema generation, and headless API reuse.

### 6. Data Validation & Accuracy Audit
Claims were verified against primary sources:
- **Total Claims Extracted:** 28 | **Directly Verified:** 22 (78.6%) | **Corroborated:** 5 (17.9%) | **Inferred:** 1 (3.5%) | **Unknown:** 1 | **Fabricated:** 0 (0.0%).
- **Verification Rate:** 96.4% across verified/corroborated evidence.
- **Preserved Conflicts:** Flagged employee count divergence (312,000 continuing vs 327,000 total before divestments) with explanatory metadata rather than discarding either metric.

### 7. Limitations & Unknowns
1. **Contract Expirations:** Exact renewal dates and co-terming terms for Siemens' master Zscaler enterprise agreement are confidential and marked `UNKNOWN`.
2. **Altair Legacy DLP:** Incumbent data loss prevention vendors inside Altair's legacy environments are unconfirmed from public records.
3. **M&A IT Program Ownership:** Whether Altair integration is managed by a temporary transitional M&A office or line IT under Frederik Janssen requires primary sales qualification.

---

### 8. Estimated Cost Model to Run on 500 Enterprise Accounts

*Assumptions:* 500 enterprise accounts analyzed annually; quarterly refreshes (2,000 runs/yr); ~15 public documents and filings per account; ~12 buying committee contacts per account.

| Cost Component | Low Estimate (Batch / Free-Tier) | Base Estimate (Hybrid Model) | High Estimate (Enterprise API Tier) |
| :--- | :--- | :--- | :--- |
| **LLM Enrichment** | **$0** (Deterministic + Gemini Free) | **$180 / yr** ($0.09/acct via Gemini Flash) | **$1,200 / yr** ($0.60/acct via GPT-4o-mini) |
| **Search / Data APIs** | **$0** (Public RSS, SEC EDGAR, Direct) | **$500 / yr** (Tavily/SerpAPI developer tier) | **$3,000 / yr** (Enterprise search & news API) |
| **Hosting & Compute** | **$120 / yr** (Single VM / Render/Railway) | **$360 / yr** (AWS ECS Fargate + RDS SQLite/Postgres) | **$1,200 / yr** (Multi-AZ AWS ECS + Aurora Serverless) |
| **Storage & Backups** | **$12 / yr** (S3 Standard / EBS) | **$48 / yr** (Encrypted S3 + Snapshots) | **$120 / yr** (Encrypted multi-region S3) |
| **TOTAL ESTIMATED COST** | **$132 / year** ($0.26 / account) | **$1,088 / year** ($2.18 / account) | **$5,520 / year** ($11.04 / account) |

*Pricing Sources:* AWS Public Pricing (Nov 2024), Google Cloud Gemini API Pricing (Nov 2024), OpenAI API Pricing (Nov 2024).

---

### 9. Privacy, Governance & Regulatory Compliance
Personal data handling strictly complies with **GDPR (EU 2016/679)** and **Singapore PDPA (2012)**:
- **Lawful Basis:** Legitimate interests (GDPR Art. 6(1)(f)) for business-to-business sales intelligence; public professional directory indexing.
- **Data Minimization:** No personal home addresses, personal cell numbers, or private emails are collected or stored.
- **Right to Erasure (Art. 17):** Implemented `DELETE /api/contacts/{id}` and `DELETE /api/accounts/{id}/cleanup-contacts` allowing immediate purging of contact records upon assessment completion.
- **No Scraping or Harassment:** Zero login-protected scraping, zero unsolicited messaging, and zero representation as Zscaler employees.

### 10. Roadmap: What to Build Next
1. **Real-time SEC EDGAR & 10-K Ingestion Webhooks:** Automatically trigger pipeline reruns upon new 10-Q/10-K or 8-K filings.
2. **Salesforce & HubSpot Bi-directional Sync:** Push recommended first contacts, outreach angles, and whitespace directly into CRM lead fields.
3. **Zscaler Partner Tech Ecosystem Mapping:** Automatically detect mutual deployments of CrowdStrike, Microsoft Entra ID, and AWS to build pre-integrated co-selling motions.

### 11. Where AI Coding Assistants Helped
- Generating structured Pydantic schemas and SQLAlchemy ORM models from complex enterprise data specifications.
- Rapid scaffolding of React Flow graph layouts and custom SVG node connectors.
- Writing comprehensive Pytest unit tests for edge-case validation and isolation checks.

### 12. Where Human Judgment & Manual Validation Were Essential
- Discerning that Siemens is an **existing customer** and reframing the strategic posture from cold prospecting to high-margin expansion.
- Investigating the true organizational reporting lines between Corporate CIO Hanna Hennig, Digital Industries CIO Frederik Janssen, and Chief Cybersecurity Officer Natalia Oropeza.
- Fact-checking the $10B Altair acquisition date and verifying the SCALANCE LPE industrial hardware integration from primary press releases.
