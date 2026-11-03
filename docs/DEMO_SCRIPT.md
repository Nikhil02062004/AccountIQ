# AccountIQ: Walkthrough Video Demo Script & Recording Checklist
**Duration:** Maximum 10:00 Minutes  
**Presenter:** Sahaj Khunteta  
**Target Audience:** Enterprise Sales Leaders, Account Executives, and Technical Evaluation Panel  

---

## Recording Checklist & Pre-Flight Setup
- [ ] Backend running locally: `python backend/run.py` (Verify `http://127.0.0.1:8000/api/health` returns `healthy`)
- [ ] Frontend running locally: `npm run dev --prefix frontend` (Verify `http://localhost:3000` loads smoothly)
- [ ] Screen resolution set to 1920x1080 (1080p), browser zoom set to 100%
- [ ] Browser tabs prepared:
  1. Tab 1: `http://localhost:3000` (AccountIQ Dashboard loaded on Siemens AG)
  2. Tab 2: `http://127.0.0.1:8000/api/accounts/siemens-ag/export-report` (Printable HTML Dossier)
  3. Tab 3: Official Zscaler Siemens Case Study (`https://www.zscaler.com/customers/siemens`)
- [ ] Microphone tested with crisp audio; no background noise

---

## Timed Video Script (0:00 – 10:00)

### Segment 1: The Business Problem & Account Selection (0:00 – 1:00)
**Screen:** AccountIQ Dashboard — Hero Header & Account Attractiveness Scores  
**Narration:**
> "Hello everyone. Today I'm presenting **AccountIQ**, an evidence-driven Account and Contact Intelligence Platform designed specifically for Zscaler enterprise sales teams.
>
> When an Account Executive prepares to approach a global conglomerate like **Siemens AG**, they face a critical challenge: Siemens is not a cold prospect. It is an existing customer with over 312,000 employees across 190 countries, currently generating €75.9 billion in annual revenue.
>
> Approaching Siemens with a generic pitch will fail. The seller must answer four exact questions: **Why this account, why now, who should we approach first, and what should we say?** 
>
> AccountIQ was built to answer these four questions with zero fluff, zero data fabrication, and 100% verifiable proof."

---

### Segment 2: Siemens Account Overview & Business Triggers (1:00 – 3:00)
**Screen:** Screen 1 (Overview) & Screen 2 (Account Intelligence) — Triggers & Footprint  
**Narration:**
> "Let’s look at the AccountIQ Overview. The platform rates Siemens at **92 out of 100 for Account Attractiveness** and **88 out of 100 for Timing Urgency**.
>
> Why is the timing score so high? If we examine our **Buying Triggers**, three massive corporate events have coincided:
> 1. First, Siemens completed its **$10 billion acquisition of Altair Engineering**. This onboarded massive high-performance computing simulation workloads, multi-cloud clusters, and thousands of engineers into the Siemens Xcelerator ecosystem.
> 2. Second, Siemens commercially launched **Siemens Industrial Copilot** in partnership with Microsoft, rolling out generative AI directly onto factory shopfloors.
> 3. Third, mandatory compliance with the **EU NIS2 Directive and Cyber Resilience Act** is enforcing strict zero-trust remote access controls across Siemens' 200+ global factories.
>
> Every single metric you see here—from the €75.9B revenue to the 312,000 workforce—is directly linked to audited disclosures from the Siemens FY2024 Annual Report."

---

### Segment 3: Technology Stack & Zscaler Expansion Whitespace (3:00 – 5:00)
**Screen:** Screen 2 — Technology Stack Table & Zscaler Whitespace Portfolio Map  
**Narration:**
> "Now let's examine Siemens' current architecture. 
>
> AccountIQ's **Technology Stack** distinguishes between confirmed current deployments, historical tools, and unknowns. 
> 
> As you can see, Siemens has mature deployments of **Zscaler Internet Access (ZIA)** and **Zscaler Private Access (ZPA)**, which phased out their legacy VPNs, as well as **Zscaler Digital Experience (ZDX)**. CIO Hanna Hennig publicly confirmed that Zscaler reduced management costs by 70% and enabled de-mergers and acquisitions in record time.
>
> Furthermore, in May 2022, Siemens and Zscaler announced an OT partnership, embedding the Zscaler App Connector inside Siemens **SCALANCE LPE** industrial hardware.
>
> So where is the expansion whitespace?
> - **Whitespace 1: Cloud Workload Communications.** Connecting Altair's multi-cloud HPC workloads in AWS and Azure without building fragile network-level firewalls.
> - **Whitespace 2: Data Protection (DSPM).** Protecting simulation intellectual property and CAD models from being exfiltrated.
> - **Whitespace 3: AI Application Security.** Providing real-time prompt guardrails for Siemens Industrial Copilot.
> - **Whitespace 4: Scaled OT Zero Trust.** Scaling SCALANCE LPE deployments from initial pilot plants to all 200+ global manufacturing sites."

---

### Segment 4: Contact Intelligence & Buying Committee Mapping (5:00 – 7:00)
**Screen:** Screen 3 (Contact Intelligence) & Screen 4 (Buying Committee Map)  
**Narration:**
> "Now, how do we translate account triggers into actual people? Let's move to **Contact Intelligence**.
>
> Here we have indexed 13 real, verified Siemens stakeholders. We do not invent names or guess private emails. Every person has an official public profile, verified title, and stated public priorities.
>
> Notice the **Buying Committee Map**. This is an interactive relationship graph rendered in real-time. 
> - At the top tier, we have CEO Dr. Roland Busch and newly appointed CTO Peter Koerte.
> - In IT Leadership, we have Global CIO Hanna Hennig, who acts as our Economic Decision-Maker.
> - In Cybersecurity, we have Global Chief Cybersecurity Officer Natalia Oropeza, who chairs the Charter of Trust and acts as our essential Security Approver or Blocker.
> - And in Digital Industries, we have **Frederik Janssen**, CIO of Siemens Digital Industries, and GM Herbert Wegmann.
>
> By clicking any node on this graph, a sales rep immediately sees their stated priorities and exact public quotes."

---

### Segment 5: The Recommended Way In (7:00 – 8:00)
**Screen:** Screen 5 — Recommended Way In (Executive Sales Blueprint)  
**Narration:**
> "This brings us to the centerpiece of AccountIQ: **The Recommended Way In**.
>
> Rather than cold-calling the CEO or asking the global CIO for a meeting, our recommendation engine synthesizes account signals to pinpoint the exact first move:
>
> **Recommended First Contact: Frederik Janssen**, CIO of Siemens Digital Industries.
>
> Why Janssen? Because Janssen heads IT for the exact operating division absorbing the $10B Altair acquisition, and his team co-developed the SCALANCE industrial edge solution. He previously stated that *'the internet is the new corporate network'*. He is an established Zero Trust champion.
>
> AccountIQ generates an evidence-grounded **Conversation Opener Draft**:
> It acknowledges the Altair closing, touches on the challenge of integrating thousands of simulation engineers without building legacy VPN tunnels, and offers a peer-level briefing on extending their existing Zero Trust Exchange to Altair cloud workloads in days.
>
> As our **Second Contact**, we recommend **Natalia Oropeza**, approaching her with an audit and NIS2 posture-validation angle to ensure early cybersecurity alignment."

---

### Segment 6: Architecture, Data Provenance, AI Strategy & Second Company (8:00 – 10:00)
**Screen:** Screen 6 (Evidence Explorer) & Screen 7 (New Research Modal / Live Demo)  
**Narration:**
> "Finally, let's look under the hood at the technical architecture.
>
> In the **Evidence Explorer**, every factual claim is clickable and backed by source URLs, publication dates, and exact text excerpts. Our automated **Data Quality Report** measures a 96.4% verification rate with zero synthetic data. Notice also our conflict resolution mechanism, which flags and preserves divergent reporting boundaries—such as Siemens' continuing versus total employee counts—rather than discarding data.
>
> Under the hood, the backend is built with **FastAPI, Python 3.12, and SQLite**, utilizing clean Pydantic v2 schemas. It runs 100% reliably in a **zero-cost, no-API-key mode** using deterministic extractors, while offering pluggable Gemini free-tier enrichment.
>
> Critically, AccountIQ is **not hardcoded to Siemens**. In Screen 7, I can type in any new company name—such as **ABB Ltd** or **Schneider Electric**—and trigger our multi-stage pipeline. The system enforces strict data isolation: the second company never inherits Siemens contacts or technologies, and missing data is transparently marked UNKNOWN.
>
> We also implement full GDPR Article 17 and Singapore PDPA compliance, including one-click contact deletion and evaluation cleanup endpoints.
>
> In summary: AccountIQ turns complex enterprise data into high-conviction sales momentum, giving Zscaler sellers the trust and evidence they need to win expansion opportunities. Thank you."

---

## Technical Appendix: Demo Checklist for Live Rerun
1. If asked to demo a second company live during the interview:
   - Click "Research Account" in the top header.
   - Enter `ABB Ltd` or `BMW Group`.
   - Watch the pipeline execute steps 1 through 7 in the terminal logs.
   - Click "Open Account Intelligence" and show that the dossier has loaded with zero Siemens overlap.
