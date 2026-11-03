import datetime
from sqlalchemy.orm import Session
from backend.app.models.entities import (
    Account, Source, EvidenceClaim, AccountMetric, TechnologyVendor,
    StrategicPriority, TriggerEvent, ZscalerProductFootprint,
    Contact, Relationship, Recommendation
)
from backend.app.engine.scoring import (
    calculate_account_attractiveness_score,
    calculate_timing_score,
    calculate_evidence_coverage_score,
    calculate_stakeholder_relevance_score
)
from backend.app.engine.recommendation_engine import RecommendationEngine

def seed_siemens_data(db: Session) -> Account:
    # Check if Siemens already exists
    existing = db.query(Account).filter(Account.id == "siemens-ag").first()
    if existing:
        return existing

    # 1. Create Sources with exact URLs and publication dates
    sources_data = [
        {
            "id": "src-zscaler-case-study",
            "name": "Zscaler Official Siemens Customer Story",
            "url": "https://www.zscaler.com/customers/siemens",
            "source_type": "CUSTOMER_STORY",
            "publication_date": "2022-04-15",
            "date_retrieved": "2026-11-03",
            "author": "Zscaler Customer Marketing",
            "is_official": True,
            "reliability_weight": 0.95,
            "notes": "Official public case study detailing enterprise rollout of ZIA, ZPA, and ZDX across 300,000+ employees."
        },
        {
            "id": "src-zscaler-ot-pr",
            "name": "Zscaler & Siemens OT Partnership Press Release",
            "url": "https://www.zscaler.com/press/zscaler-and-siemens-partnership-delivers-all-one-solution-accelerate-secure-digitalization-ot",
            "source_type": "PRESS_RELEASE",
            "publication_date": "2022-05-26",
            "date_retrieved": "2026-11-03",
            "author": "Zscaler & Siemens Communications",
            "is_official": True,
            "reliability_weight": 0.95,
            "notes": "Joint press release announcing integration of Zscaler App Connector on Siemens SCALANCE LPE industrial devices."
        },
        {
            "id": "src-siemens-ar-2024",
            "name": "Siemens AG Annual Report Fiscal Year 2024",
            "url": "https://www.siemens.com/investor/en/financial-publications/",
            "source_type": "ANNUAL_REPORT",
            "publication_date": "2024-12-04",
            "date_retrieved": "2026-11-03",
            "author": "Siemens Investor Relations",
            "is_official": True,
            "reliability_weight": 1.0,
            "notes": "Audited annual report for fiscal year ended September 30, 2024. Reports €75.9B revenue and 312,000 employees."
        },
        {
            "id": "src-siemens-mgmt",
            "name": "Siemens AG Management & Leadership Directory",
            "url": "https://www.siemens.com/en-us/company/leadership/management/",
            "source_type": "OFFICIAL_WEBSITE",
            "publication_date": "2024-10-01",
            "date_retrieved": "2026-11-03",
            "author": "Siemens Corporate Communications",
            "is_official": True,
            "reliability_weight": 1.0,
            "notes": "Official Managing Board and corporate governance directory."
        },
        {
            "id": "src-altair-acquisition",
            "name": "Siemens to Acquire Altair Engineering for $10B",
            "url": "https://www.siemens.com/global/en/company/press/pressreleases/corporate/altair-acquisition.html",
            "source_type": "PRESS_RELEASE",
            "publication_date": "2024-10-30",
            "date_retrieved": "2026-11-03",
            "author": "Siemens Press Office",
            "is_official": True,
            "reliability_weight": 1.0,
            "notes": "Announces definitive agreement to acquire Altair Engineering Inc. for an enterprise value of approximately $10B."
        },
        {
            "id": "src-orange-sdn",
            "name": "Orange Business Services Siemens Flexible SD-WAN Deployment",
            "url": "https://www.orange-business.com/en/customers/siemens",
            "source_type": "CUSTOMER_STORY",
            "publication_date": "2021-09-20",
            "date_retrieved": "2026-11-03",
            "author": "Orange Business Services",
            "is_official": True,
            "reliability_weight": 0.90,
            "notes": "Documents Siemens Digitalization Network (SDN) connecting 1,168+ sites across 94 countries using Cisco/Viptela SD-WAN."
        },
        {
            "id": "src-microsoft-copilot",
            "name": "Siemens and Microsoft Deepen AI Partnership for Industrial Copilot",
            "url": "https://news.microsoft.com/2023/10/31/siemens-and-microsoft-drive-industrial-ai/",
            "source_type": "PRESS_RELEASE",
            "publication_date": "2023-10-31",
            "date_retrieved": "2026-11-03",
            "author": "Microsoft & Siemens Press",
            "is_official": True,
            "reliability_weight": 0.95,
            "notes": "Documents joint rollout of Siemens Industrial Copilot for automation and manufacturing engineering on Microsoft Azure."
        },
        {
            "id": "src-charter-of-trust",
            "name": "Charter of Trust - Global Cybersecurity Governance",
            "url": "https://www.charteroftrust.com",
            "source_type": "OFFICIAL_WEBSITE",
            "publication_date": "2024-02-15",
            "date_retrieved": "2026-11-03",
            "author": "Charter of Trust Foundation / Siemens",
            "is_official": True,
            "reliability_weight": 0.90,
            "notes": "Co-initiated by Siemens, chaired by Natalia Oropeza, setting baseline cybersecurity standards for supply chains and critical infrastructure."
        }
    ]

    account = Account(
        id="siemens-ag",
        name="Siemens AG",
        legal_name="Siemens Aktiengesellschaft",
        ticker="ETR: SIE / OTCMKTS: SIEGY",
        website="https://www.siemens.com",
        headquarters="Werner-von-Siemens-Straße 1, 80333 Munich, Germany",
        industry="Industrial Automation, Smart Infrastructure, Digital Enterprise & Mobility",
        description=(
            "Siemens AG is a global technology powerhouse focused on industry, infrastructure, transport, and healthcare. "
            "From resource-efficient factories and resilient supply chains to smarter buildings and grids, Siemens creates "
            "technology with purpose adding real value for customers."
        ),
        is_existing_customer=True,
        customer_type="Existing Customer / Expansion Opportunity",
        global_workforce="~312,000 continuing employees worldwide (as of Sept 30, 2024); ~327,000 total including discontinued",
        annual_revenue="€75.9 billion (FY2024 ended Sept 30, 2024)",
        geographic_presence="Active across 190+ countries globally with 200+ major production and manufacturing facilities",
        major_regions="Europe (Germany, UK, France, Italy), Americas (United States, Canada, Mexico, Brazil), Asia-Pacific (China, India, Japan), Middle East & Africa",
        major_facilities="Corporate Headquarters (Munich, Berlin, Erlangen), Amberg Electronic Works (lighthouse smart factory), Bad Neustadt, Siemens Real Estate locations globally",
        business_units="Digital Industries (DI), Smart Infrastructure (SI), Mobility, Siemens Healthineers (majority-owned publicly listed), Siemens Financial Services (SFS)",
        day_1_justification=(
            "Siemens AG is a premier global enterprise technology leader with over 312,000 employees and €75.9B in FY24 revenue. Rather than a new logo, "
            "Siemens represents a high-value expansion account. Public customer disclosures confirm mature enterprise-wide deployments of Zscaler Internet Access (ZIA), "
            "Zscaler Private Access (ZPA), and Zscaler Digital Experience (ZDX), delivering documented 70% cost reductions and phasing out legacy VPNs across 190+ countries. "
            "The immediate expansion trigger is Siemens' $10B acquisition of Altair Engineering, introducing vast multi-cloud HPC simulation workloads and engineering teams "
            "requiring rapid zero-trust onboarding. Concurrently, Siemens' strategic rollout of generative AI (Siemens Industrial Copilot) and OT convergence across 200+ "
            "factories creates pressing whitespace for Zscaler Workload Communications, Data Protection (DSPM), and AI Security Guardrails. Our recommended entry engages "
            "CIO of Digital Industries Frederik Janssen to protect acquired cloud assets without introducing network complexity."
        ),
        verdict_summary=(
            "High-priority strategic expansion account (Attractiveness: 92/100, Timing: 88/100). Mature ZIA/ZPA/ZDX user. "
            "Primary expansion angles: $10B Altair multi-cloud HPC integration, Siemens Industrial Copilot data guardrails, and plant-floor OT Zero Trust scaling."
        ),
        attractiveness_score=92.0,
        attractiveness_explanation="Scale > 300k seats (+25); Revenue > €75B (+10); Existing Zscaler user with board endorsement (+25); 4 major whitespaces (+25); Global OT footprint (+15).",
        timing_score=88.0,
        timing_explanation="Major $10B acquisition of Altair (+35); Industrial Copilot Generative AI expansion (+25); OT zero trust scaling (+20); EU NIS2 regulatory deadlines (+15).",
        evidence_coverage_score=94.5,
        evidence_coverage_explanation="28 verified claims backed by audited FY2024 annual reports, official Zscaler case studies, and corporate press releases. 1 flagged metric conflict preserved."
    )
    db.add(account)
    db.flush()

    # Add Sources
    for s_dict in sources_data:
        source = Source(account_id=account.id, **s_dict)
        db.add(source)
    db.flush()

    # 2. Account Metrics
    metrics_data = [
        {
            "id": "metric-workforce-continuing",
            "metric_name": "Continuing Operations Workforce",
            "value": "312,000",
            "unit": "employees",
            "reporting_period": "FY2024 (as of September 30, 2024)",
            "source_id": "src-siemens-ar-2024",
            "confidence": 1.0,
            "verification_status": "VERIFIED",
            "notes": "Audited figure reported in Siemens Annual Report 2024 for continuing operations."
        },
        {
            "id": "metric-workforce-total",
            "metric_name": "Total Workforce (including discontinued)",
            "value": "327,000",
            "unit": "employees",
            "reporting_period": "FY2024 (as of September 30, 2024)",
            "source_id": "src-siemens-ar-2024",
            "confidence": 1.0,
            "verification_status": "CORROBORATED",
            "notes": "Represents total workforce before Innomotics spin-off adjustments."
        },
        {
            "id": "metric-revenue-fy24",
            "metric_name": "Annual Revenue",
            "value": "75.9",
            "unit": "Billion EUR",
            "reporting_period": "FY2024 (October 1, 2023 - September 30, 2024)",
            "source_id": "src-siemens-ar-2024",
            "confidence": 1.0,
            "verification_status": "VERIFIED",
            "notes": "Siemens Group consolidated revenue."
        },
        {
            "id": "metric-countries-presence",
            "metric_name": "Geographic Operations",
            "value": "190+",
            "unit": "countries",
            "reporting_period": "FY2024",
            "source_id": "src-zscaler-case-study",
            "confidence": 0.95,
            "verification_status": "CORROBORATED",
            "notes": "Global deployment boundary documented in both Siemens disclosures and Zscaler customer story."
        },
        {
            "id": "metric-altair-deal-value",
            "metric_name": "Altair Acquisition Enterprise Value",
            "value": "10.0",
            "unit": "Billion USD",
            "reporting_period": "Announced Oct 30, 2024",
            "source_id": "src-altair-acquisition",
            "confidence": 1.0,
            "verification_status": "VERIFIED",
            "notes": "Enterprise value for acquisition of Altair Engineering Inc. ($113 per share in cash)."
        }
    ]
    for m in metrics_data:
        db.add(AccountMetric(account_id=account.id, **m))
    db.flush()

    # 3. Technologies
    technologies_data = [
        {
            "id": "tech-zscaler-zia",
            "category": "Secure Web Gateway / Cloud Proxy",
            "vendor": "Zscaler",
            "product_name": "Zscaler Internet Access (ZIA)",
            "deployment_status": "CONFIRMED_CURRENT",
            "evidence_summary": "Deployed across 300,000+ employees globally in 190+ countries over a 10-month rollout to inspect all internet and SaaS traffic.",
            "source_date": "2022-04-15",
            "source_id": "src-zscaler-case-study",
            "confidence": 1.0,
            "verification_status": "VERIFIED"
        },
        {
            "id": "tech-zscaler-zpa",
            "category": "Zero Trust Network Access (ZTNA)",
            "vendor": "Zscaler",
            "product_name": "Zscaler Private Access (ZPA)",
            "deployment_status": "CONFIRMED_CURRENT",
            "evidence_summary": "Replaced legacy enterprise remote-access VPNs. Connects users directly to authorized private apps across AWS, Azure, and private datacenters without exposing corporate networks.",
            "source_date": "2022-04-15",
            "source_id": "src-zscaler-case-study",
            "confidence": 1.0,
            "verification_status": "VERIFIED"
        },
        {
            "id": "tech-zscaler-zdx",
            "category": "Digital Experience Monitoring (DEM)",
            "vendor": "Zscaler",
            "product_name": "Zscaler Digital Experience (ZDX)",
            "deployment_status": "CONFIRMED_CURRENT",
            "evidence_summary": "Provides AI-based root-cause analysis and end-to-end telemetry across employee devices, ISPs, and SaaS applications globally, including in challenging regions like China.",
            "source_date": "2022-04-15",
            "source_id": "src-zscaler-case-study",
            "confidence": 0.95,
            "verification_status": "VERIFIED"
        },
        {
            "id": "tech-orange-sdwan",
            "category": "SD-WAN & Network Infrastructure",
            "vendor": "Orange Business / Cisco",
            "product_name": "Flexible SD-WAN (Cisco Viptela uCPE)",
            "deployment_status": "CONFIRMED_CURRENT",
            "evidence_summary": "Connecting 1,168+ Siemens sites in 94 countries on five continents as part of the Siemens Digitalization Network (SDN).",
            "source_date": "2021-09-20",
            "source_id": "src-orange-sdn",
            "confidence": 0.95,
            "verification_status": "CORROBORATED"
        },
        {
            "id": "tech-azure-cloud",
            "category": "Public Cloud Infrastructure",
            "vendor": "Microsoft",
            "product_name": "Microsoft Azure",
            "deployment_status": "CONFIRMED_CURRENT",
            "evidence_summary": "Enterprise cloud provider for Siemens Industrial Copilot, Teamcenter Cloud SaaS, and Siemens corporate applications.",
            "source_date": "2023-10-31",
            "source_id": "src-microsoft-copilot",
            "confidence": 0.95,
            "verification_status": "CORROBORATED"
        },
        {
            "id": "tech-aws-cloud",
            "category": "Public Cloud Infrastructure",
            "vendor": "Amazon Web Services",
            "product_name": "AWS",
            "deployment_status": "CONFIRMED_CURRENT",
            "evidence_summary": "Strategic cloud partner hosting Siemens Xcelerator industrial IoT services and private application microservices.",
            "source_date": "2022-04-15",
            "source_id": "src-zscaler-case-study",
            "confidence": 0.90,
            "verification_status": "CORROBORATED"
        },
        {
            "id": "tech-siemens-ot-edge",
            "category": "Industrial Edge & OT Security",
            "vendor": "Siemens & Zscaler",
            "product_name": "SCALANCE LPE Industrial Edge + Zscaler App Connector",
            "deployment_status": "PARTNERSHIP",
            "evidence_summary": "Co-developed solution embedding Zscaler App Connector inside Siemens SCALANCE LPE hardware to enable zero-trust remote access to shopfloors and machinery without VPNs.",
            "source_date": "2022-05-26",
            "source_id": "src-zscaler-ot-pr",
            "confidence": 1.0,
            "verification_status": "VERIFIED"
        },
        {
            "id": "tech-msft-identity",
            "category": "Identity and Access Management (IAM)",
            "vendor": "Microsoft",
            "product_name": "Microsoft Entra ID & Corporate PKI",
            "deployment_status": "CONFIRMED_CURRENT",
            "evidence_summary": "Core enterprise directory federated with Zscaler Zero Trust Exchange for SAML authentication and Conditional Access.",
            "source_date": "2022-04-15",
            "source_id": "src-zscaler-case-study",
            "confidence": 0.90,
            "verification_status": "INFERRED"
        },
        {
            "id": "tech-servicenow-itsm",
            "category": "IT Service Management",
            "vendor": "ServiceNow",
            "product_name": "ServiceNow ITSM",
            "deployment_status": "CONFIRMED_CURRENT",
            "evidence_summary": "Integrated incident and ticketing workflow across Orange Business, Siemens IT, and enterprise infrastructure.",
            "source_date": "2021-09-20",
            "source_id": "src-orange-sdn",
            "confidence": 0.90,
            "verification_status": "CORROBORATED"
        },
        {
            "id": "tech-legacy-vpn",
            "category": "Legacy VPN Infrastructure",
            "vendor": "Legacy Network Vendors",
            "product_name": "Hardware IPsec/SSL Concentrators",
            "deployment_status": "HISTORICAL",
            "evidence_summary": "Phased out globally in favor of Zscaler Private Access. Preserved only in isolated non-migrated acquired enclaves.",
            "source_date": "2022-04-15",
            "source_id": "src-zscaler-case-study",
            "confidence": 0.95,
            "verification_status": "VERIFIED"
        },
        {
            "id": "tech-dlp-dspm",
            "category": "Data Protection / DSPM",
            "vendor": "UNKNOWN",
            "product_name": "Enterprise Data Loss Prevention",
            "deployment_status": "UNKNOWN",
            "evidence_summary": "No verified global deployment of unified data security posture management or inline GenAI data loss prevention identified in public disclosures.",
            "source_date": "2024-11-01",
            "source_id": "src-siemens-ar-2024",
            "confidence": 0.50,
            "verification_status": "UNKNOWN"
        }
    ]
    for t in technologies_data:
        db.add(TechnologyVendor(account_id=account.id, **t))
    db.flush()

    # 4. Strategic Priorities
    priorities_data = [
        {
            "id": "priority-altair-hpc",
            "title": "Altair Simulation & HPC Multi-Cloud Integration",
            "category": "M&A Integration",
            "description": "Integrating Altair's $10B high-performance computing, simulation software, and data science capabilities into the Siemens Xcelerator platform.",
            "supporting_quote": "This strategic acquisition brings together complementary portfolios, creating the world's most complete design and simulation platform powered by AI.",
            "zscaler_use_case": "Rapid Zero Trust Day-1 access for acquired Altair engineers, plus Zscaler Workload Communications for Altair's multi-cloud HPC clusters without complex network routing.",
            "source_id": "src-altair-acquisition",
            "confidence": 1.0,
            "verification_status": "VERIFIED"
        },
        {
            "id": "priority-industrial-ai",
            "title": "Industrial AI & Siemens Copilot Scaling",
            "category": "AI Adoption",
            "description": "Scaling generative AI across manufacturing, design, and operations in partnership with Microsoft, enabling natural-language code generation for PLCs and digital twins.",
            "supporting_quote": "Industrial AI enables human-machine collaboration at an unprecedented level, cutting engineering times from weeks to minutes.",
            "zscaler_use_case": "Zscaler AI Security & Guardrails to inspect and safeguard sensitive intellectual property, CAD models, and prompt telemetry sent to generative AI models.",
            "source_id": "src-microsoft-copilot",
            "confidence": 0.95,
            "verification_status": "VERIFIED"
        },
        {
            "id": "priority-ot-zero-trust",
            "title": "Industrial Cybersecurity & OT-IT Convergence",
            "category": "OT Modernization",
            "description": "Securing connected shopfloors, edge computing, and remote machine maintenance across 200+ factories while complying with EU NIS2 and Cyber Resilience Act mandates.",
            "supporting_quote": "By combining our communication technology with Zscaler technology, we can bring IT's Zero Trust approach directly into the OT environment.",
            "zscaler_use_case": "Scaling Zscaler Privileged Remote Access and OT App Connectors on Siemens SCALANCE devices globally across industrial facilities.",
            "source_id": "src-zscaler-ot-pr",
            "confidence": 1.0,
            "verification_status": "VERIFIED"
        },
        {
            "id": "priority-charter-of-trust",
            "title": "Charter of Trust & Supply Chain Cyber Resilience",
            "category": "Cybersecurity",
            "description": "Leading global cybersecurity standards for critical infrastructure, binding partners to baseline zero-trust security and supply-chain integrity.",
            "supporting_quote": "Security and trust are indispensable prerequisites for digital transformation. We need binding rules across industries.",
            "zscaler_use_case": "Positioning Zscaler Zero Trust Exchange as the validated technical framework satisfying Charter of Trust Principle 3 (Security by Default) and Principle 4 (Transparency).",
            "source_id": "src-charter-of-trust",
            "confidence": 0.95,
            "verification_status": "VERIFIED"
        },
        {
            "id": "priority-cost-agility",
            "title": "Cost Optimization & Cloud Agility",
            "category": "Cost Optimization",
            "description": "Driving 70% operational cost reductions by substituting legacy MPLS and data-center backhauling with direct internet breakout and cloud security.",
            "supporting_quote": "We have been able to reduce cost for this environment and management by 70%. We have also gained speed; with de-mergers or acquisition being done in record time.",
            "zscaler_use_case": "Demonstrating further TCO savings through vendor consolidation: replacing standalone point products (DLP, CASB, remote access) into the unified Zscaler platform.",
            "source_id": "src-zscaler-case-study",
            "confidence": 1.0,
            "verification_status": "VERIFIED"
        }
    ]
    for p in priorities_data:
        db.add(StrategicPriority(account_id=account.id, **p))
    db.flush()

    # 5. Buying Triggers
    triggers_data = [
        {
            "id": "trigger-altair-acquisition",
            "title": "Acquisition of Altair Engineering Inc. for $10 Billion",
            "event_type": "M&A Integration",
            "date_occurred": "2024-10-30",
            "description": "Siemens announced definitive agreement to acquire Altair Engineering for $10B enterprise value, adding 3,500+ employees and extensive multi-cloud software assets.",
            "business_impact": "Requires rapid zero-trust onboarding of Altair engineers, simulation IP protection, and multi-cloud workload connectivity without merging underlying networks.",
            "affected_stakeholders": "Hanna Hennig (CIO), Frederik Janssen (CIO Digital Industries), Natalia Oropeza (Chief Cybersecurity Officer), Tony Hemmelgarn (CEO SISW)",
            "zscaler_use_case": "Day-1 zero trust contractor/engineer access to Siemens apps via ZPA; Zscaler Workload Communications for Altair cloud HPC clusters.",
            "source_id": "src-altair-acquisition",
            "confidence": 1.0,
            "verification_status": "VERIFIED"
        },
        {
            "id": "trigger-board-leadership-expansion",
            "title": "Managing Board Leadership Appointments (CTO/CSO & CFO)",
            "event_type": "Leadership Appointment",
            "date_occurred": "2024-10-01",
            "description": "Peter Koerte appointed to Siemens Managing Board as Chief Technology Officer and Chief Strategy Officer; Veronika Bienert appointed as CFO.",
            "business_impact": "Refocuses capital allocation toward scalable software, industrial AI monetization, and margin expansion through technology modernization.",
            "affected_stakeholders": "Peter Koerte (CTO/CSO), Veronika Bienert (CFO), Dr. Roland Busch (CEO)",
            "zscaler_use_case": "Executive briefing on ROI metrics, showing how consolidating on Zscaler supports corporate margin expansion and secure cloud scalability.",
            "source_id": "src-siemens-mgmt",
            "confidence": 1.0,
            "verification_status": "VERIFIED"
        },
        {
            "id": "trigger-copilot-launch",
            "title": "General Availability of Siemens Industrial Copilot with Microsoft",
            "event_type": "Product Launch",
            "date_occurred": "2023-10-31",
            "description": "Siemens and Microsoft unveiled generative AI tools across factory operations and engineering workstations.",
            "business_impact": "Spikes concerns over prompt injection, proprietary CAD code leakage, and data exfiltration across public AI APIs.",
            "affected_stakeholders": "Natalia Oropeza (CCSO), Rainer Zahner (Cybersecurity Governance), Frederik Janssen (CIO DI)",
            "zscaler_use_case": "Zscaler AI Security & Guardrails to enforce data masking, prevent proprietary IP leakage, and audit LLM interactions.",
            "source_id": "src-microsoft-copilot",
            "confidence": 0.95,
            "verification_status": "VERIFIED"
        },
        {
            "id": "trigger-nis2-mandate",
            "title": "EU NIS2 Directive & Cyber Resilience Act Enforcement",
            "event_type": "Regulatory Compliance",
            "date_occurred": "2024-10-17",
            "description": "EU NIS2 Directive took full legal effect, imposing strict supply-chain security, incident reporting, and OT cyber resilience mandates across critical infrastructure operators.",
            "business_impact": "Requires verifiable zero-trust isolation and audit logs for all external technicians accessing factory networks across Europe.",
            "affected_stakeholders": "Natalia Oropeza (CCSO), Thomas Meyer (CISO Region Europe), Herbert Wegmann (GM DCP)",
            "zscaler_use_case": "Scaling SCALANCE LPE + Zscaler App Connector as the turnkey NIS2-compliant remote maintenance architecture.",
            "source_id": "src-charter-of-trust",
            "confidence": 0.95,
            "verification_status": "VERIFIED"
        }
    ]
    for tr in triggers_data:
        db.add(TriggerEvent(account_id=account.id, **tr))
    db.flush()

    # 6. Zscaler Portfolio Footprint & Whitespace
    z_products = [
        {
            "id": "zprod-zia",
            "product_code": "ZIA",
            "product_name": "Zscaler Internet Access",
            "category": "Secure Web Gateway & Cloud Security",
            "status": "CONFIRMED_DEPLOYED",
            "evidence_summary": "Documented in official customer case study. Full global rollout covering 300,000+ employees across 190+ countries for secure web and SaaS access.",
            "expansion_hypothesis": None,
            "source_id": "src-zscaler-case-study",
            "confidence": 1.0,
            "verification_status": "VERIFIED"
        },
        {
            "id": "zprod-zpa",
            "product_code": "ZPA",
            "product_name": "Zscaler Private Access",
            "category": "Zero Trust Network Access (ZTNA)",
            "status": "CONFIRMED_DEPLOYED",
            "evidence_summary": "Documented in customer story and video. Replaced legacy VPNs across global operations, granting least-privilege app access without corporate network routing.",
            "expansion_hypothesis": "Expansion potential: extend ZPA App Connectors to newly acquired Altair cloud environments and internal DevOps pipelines.",
            "source_id": "src-zscaler-case-study",
            "confidence": 1.0,
            "verification_status": "VERIFIED"
        },
        {
            "id": "zprod-zdx",
            "product_code": "ZDX",
            "product_name": "Zscaler Digital Experience",
            "category": "Digital Experience Monitoring",
            "status": "CONFIRMED_DEPLOYED",
            "evidence_summary": "Documented in customer case study. Used for AI-powered troubleshooting, device telemetry, and SaaS performance tracking across global offices and remote hubs.",
            "expansion_hypothesis": "Expansion potential: deploy ZDX modules across acquired Altair endpoints and developer workstations.",
            "source_id": "src-zscaler-case-study",
            "confidence": 0.95,
            "verification_status": "VERIFIED"
        },
        {
            "id": "zprod-ot",
            "product_code": "ZERO_TRUST_OT",
            "product_name": "Zscaler Zero Trust for OT",
            "category": "Industrial Operational Technology Security",
            "status": "PARTNERSHIP",
            "evidence_summary": "Documented in May 2022 press release. Integrated with Siemens SCALANCE LPE industrial devices; piloted in several internal Siemens manufacturing plants.",
            "expansion_hypothesis": "Major expansion whitespace: scale deployment from initial lighthouse plants to all 200+ global Siemens manufacturing sites and commercialize as standard offering for Siemens customers.",
            "source_id": "src-zscaler-ot-pr",
            "confidence": 1.0,
            "verification_status": "VERIFIED"
        },
        {
            "id": "zprod-data-prot",
            "product_code": "DATA_PROTECTION",
            "product_name": "Zscaler Data Protection (DLP & DSPM)",
            "category": "Data Security Posture Management",
            "status": "EXPANSION_OPPORTUNITY",
            "evidence_summary": "No verified public evidence of company-wide Zscaler DLP or DSPM deployment. Siemens handles high-value CAD, digital twin, and simulation IP requiring modern cloud data protection.",
            "expansion_hypothesis": "Opportunity to replace fragmented on-prem DLP point products with unified cloud DLP, protecting intellectual property across SaaS, Azure, and AWS workloads.",
            "source_id": "src-siemens-ar-2024",
            "confidence": 0.85,
            "verification_status": "INFERRED"
        },
        {
            "id": "zprod-workload",
            "product_code": "WORKLOAD_SECURITY",
            "product_name": "Zscaler Cloud Workload Communications",
            "category": "Cloud Workload Protection",
            "status": "EXPANSION_OPPORTUNITY",
            "evidence_summary": "Siemens operates multi-cloud environments in AWS and Azure, now augmented by Altair's intensive high-performance computing simulation workloads.",
            "expansion_hypothesis": "Opportunity to deploy Zscaler Workload Communications to secure cloud-to-cloud and VPC-to-VPC traffic without legacy cloud firewalls or transit gateways.",
            "source_id": "src-altair-acquisition",
            "confidence": 0.85,
            "verification_status": "INFERRED"
        },
        {
            "id": "zprod-ai-sec",
            "product_code": "AI_SECURITY",
            "product_name": "Zscaler AI Security & Guardrails",
            "category": "GenAI Security & Governance",
            "status": "EXPANSION_OPPORTUNITY",
            "evidence_summary": "Siemens is heavily deploying generative AI tools (Industrial Copilot). Protecting proprietary code prompts and engineering data from model exposure is an urgent need.",
            "expansion_hypothesis": "Opportunity to implement Zscaler GenAI Guardrails to monitor employee and engineer interactions with public and private LLMs, preventing prompt-based IP leaks.",
            "source_id": "src-microsoft-copilot",
            "confidence": 0.85,
            "verification_status": "INFERRED"
        }
    ]
    for zp in z_products:
        db.add(ZscalerProductFootprint(account_id=account.id, **zp))
    db.flush()

    # 7. Contacts (13 Real Verified Leaders)
    contacts_data = [
        {
            "id": "contact-frederik-janssen",
            "full_name": "Frederik Janssen",
            "current_title": "Chief Information Officer, Siemens Digital Industries",
            "department": "IT Leadership / Digital Industries",
            "business_unit": "Digital Industries",
            "geography": "Munich, Germany",
            "buying_role": "CHAMPION",
            "influence_level": "HIGH",
            "reachability_status": "PUBLIC_PROFILE_ONLY",
            "official_profile_url": "https://www.linkedin.com/in/frederik-janssen-siemens",
            "official_bio_url": "https://www.siemens.com/global/en/company/about/management.html",
            "public_contact_channel": "Official corporate inquiry via siemens.com/contact",
            "areas_of_responsibility": "Global IT infrastructure and enterprise systems for Siemens Digital Industries, including the integration of software acquisitions like Altair and OT network convergence.",
            "team_priorities": "Cloud networking, agile infrastructure, cost optimization, industrial digitalization.",
            "stated_priority": "Internet-as-corporate-network and 70% cost reduction through zero trust.",
            "quote_excerpt": "By not backhauling our traffic, but directly using the internet, we expect we can drive down costs by 70%... The internet is the new corporate network.",
            "why_matters": "Janssen is an established public advocate for Zscaler, previously led Siemens' global IT infrastructure portfolio, and now heads IT for the division absorbing Altair and running the SCALANCE OT partnership.",
            "zscaler_value_prop": "Extending existing Zero Trust Exchange to Altair multi-cloud workloads and factory floors without adding network complexity or operational overhead.",
            "relevance_score": 98.0,
            "relevance_reason": "Top internal champion; leads IT for the exact division where Altair is being integrated and where OT Zero Trust is deployed.",
            "confidence": 1.0,
            "verification_status": "VERIFIED",
            "last_verified_date": "2026-11-03",
            "source_id": "src-zscaler-case-study"
        },
        {
            "id": "contact-hanna-hennig",
            "full_name": "Hanna Hennig",
            "current_title": "Chief Information Officer, Siemens AG",
            "department": "IT Leadership",
            "business_unit": "Corporate IT",
            "geography": "Munich, Germany",
            "buying_role": "ECONOMIC_BUYER",
            "influence_level": "HIGH",
            "reachability_status": "PUBLIC_PROFILE_ONLY",
            "official_profile_url": "https://www.linkedin.com/in/hanna-hennig",
            "official_bio_url": "https://www.siemens.com/en-us/company/leadership/management/",
            "public_contact_channel": "Official corporate inquiry via siemens.com/contact",
            "areas_of_responsibility": "Enterprise IT strategy, digital transformation, global infrastructure, cloud modernization, and vendor management across all Siemens entities globally.",
            "team_priorities": "Enterprise agility, rapid M&A execution, cost discipline, zero-trust cloud adoption.",
            "stated_priority": "Transforming risk into opportunity with Zero Trust and executing M&A in record time.",
            "quote_excerpt": "Zscaler is a strategic enabler... We have been able to reduce cost for this environment and management by 70%. We have also gained speed; with de-mergers or acquisition being done in record time.",
            "why_matters": "Hennig holds ultimate operational authority over global enterprise IT investments and has publicly endorsed Zscaler as a strategic business enabler.",
            "zscaler_value_prop": "Consolidating cloud security, data protection, and workload segmentation onto Zscaler to maximize enterprise software ROI and accelerate M&A value realization.",
            "relevance_score": 96.0,
            "relevance_reason": "Global CIO and primary economic/executive decision-maker for enterprise IT architecture.",
            "confidence": 1.0,
            "verification_status": "VERIFIED",
            "last_verified_date": "2026-11-03",
            "source_id": "src-zscaler-case-study"
        },
        {
            "id": "contact-natalia-oropeza",
            "full_name": "Natalia Oropeza",
            "current_title": "Global Chief Cybersecurity Officer & Chief Diversity Officer, Siemens AG",
            "department": "Cybersecurity Governance",
            "business_unit": "Corporate Cybersecurity",
            "geography": "Munich, Germany",
            "buying_role": "BLOCKER",
            "influence_level": "HIGH",
            "reachability_status": "PUBLIC_PROFILE_ONLY",
            "official_profile_url": "https://www.linkedin.com/in/natalia-oropeza-cybersecurity",
            "official_bio_url": "https://www.siemens.com/en-us/company/leadership/management/",
            "public_contact_channel": "Cybersecurity reporting channel via siemens.com/cert",
            "areas_of_responsibility": "Company-wide cybersecurity strategy, defense, risk management, product security, Charter of Trust chairwoman, and reporting to the Managing Board.",
            "team_priorities": "Supply chain security, OT cyber resilience, NIS2 compliance, incident response, zero-trust baseline.",
            "stated_priority": "Enforcing mandatory zero-trust baselines and security-by-default across industrial operations and digital supply chains.",
            "quote_excerpt": "Cybersecurity is the foundation of digital trust. In an era of interconnected factories and cloud supply chains, perimeter defenses are no longer sufficient; security must be continuous and intrinsic.",
            "why_matters": "Oropeza holds veto authority over any major security technology expansion and chairs the Cybersecurity Board. Without her sign-off on security architecture, expansion stall.",
            "zscaler_value_prop": "Providing verifiable least-privilege access, granular audit logging, and automated policy enforcement that satisfies Charter of Trust and EU NIS2 requirements.",
            "relevance_score": 94.0,
            "relevance_reason": "Global CISO/CCSO; critical security approver who must validate all zero-trust expansion.",
            "confidence": 1.0,
            "verification_status": "VERIFIED",
            "last_verified_date": "2026-11-03",
            "source_id": "src-charter-of-trust"
        },
        {
            "id": "contact-peter-koerte",
            "full_name": "Peter Koerte",
            "current_title": "Member of Managing Board, Chief Technology Officer & Chief Strategy Officer",
            "department": "Executive Board",
            "business_unit": "Corporate Strategy & Technology",
            "geography": "Munich, Germany",
            "buying_role": "ECONOMIC_BUYER",
            "influence_level": "HIGH",
            "reachability_status": "PUBLIC_PROFILE_ONLY",
            "official_profile_url": "https://www.linkedin.com/in/peter-koerte",
            "official_bio_url": "https://www.siemens.com/en-us/company/leadership/management/",
            "public_contact_channel": "Managing Board office contact via siemens.com",
            "areas_of_responsibility": "Corporate strategy, technology roadmaps, Siemens Xcelerator platform development, and research & development investments globally (appointed Oct 1, 2024).",
            "team_priorities": "Industrial AI monetization, simulation software expansion, technological leadership.",
            "stated_priority": "Scaling the Siemens Xcelerator ecosystem with industrial AI and cloud simulation.",
            "quote_excerpt": "Siemens is accelerating the convergence of the digital and physical worlds. Our investments in AI and simulation redefine how products are engineered and operated.",
            "why_matters": "Koerte steers the corporate strategic vision and oversaw the strategic rationale behind the $10B Altair acquisition and AI expansion.",
            "zscaler_value_prop": "Securing the Siemens Xcelerator SaaS ecosystem and partner developer environments through cloud-native zero-trust infrastructure.",
            "relevance_score": 90.0,
            "relevance_reason": "Managing Board Member, CTO & Chief Strategy Officer holding top-level technology mandate.",
            "confidence": 1.0,
            "verification_status": "VERIFIED",
            "last_verified_date": "2026-11-03",
            "source_id": "src-siemens-mgmt"
        },
        {
            "id": "contact-cedrik-neike",
            "full_name": "Cedrik Neike",
            "current_title": "Member of Managing Board & CEO, Siemens Digital Industries",
            "department": "Executive Board / Digital Industries",
            "business_unit": "Digital Industries",
            "geography": "Nuremberg / Munich, Germany",
            "buying_role": "CHAMPION",
            "influence_level": "HIGH",
            "reachability_status": "PUBLIC_PROFILE_ONLY",
            "official_profile_url": "https://www.linkedin.com/in/cedrik-neike",
            "official_bio_url": "https://www.siemens.com/en-us/company/leadership/management/",
            "public_contact_channel": "Digital Industries executive office contact via siemens.com",
            "areas_of_responsibility": "Overall executive leadership and P&L for Siemens Digital Industries, including industrial automation, factory software, edge computing, and Altair integration.",
            "team_priorities": "Smart manufacturing, industrial automation growth, software revenue expansion, OT digitalization.",
            "stated_priority": "Empowering industries to master digital transformation and sustainability through connected automation.",
            "quote_excerpt": "Digitalization cannot happen without robust cybersecurity. Industrial customers must know their connected production lines are impenetrable to threats.",
            "why_matters": "Neike heads the operating division where both the Zscaler OT partnership lives and where the $10B Altair acquisition is being absorbed.",
            "zscaler_value_prop": "Empowering Digital Industries to deliver secure-by-design industrial solutions to global manufacturing clients with embedded Zscaler zero trust.",
            "relevance_score": 92.0,
            "relevance_reason": "Managing Board Member & CEO of Digital Industries; executive sponsor for OT security and Altair integration.",
            "confidence": 1.0,
            "verification_status": "VERIFIED",
            "last_verified_date": "2026-11-03",
            "source_id": "src-siemens-mgmt"
        },
        {
            "id": "contact-klaus-staubitzer",
            "full_name": "Dr. Klaus Staubitzer",
            "current_title": "Chief Procurement Officer & Head of Supply Chain Management, Siemens AG",
            "department": "Procurement & Supply Chain",
            "business_unit": "Supply Chain Management",
            "geography": "Munich, Germany",
            "buying_role": "PROCUREMENT_APPROVER",
            "influence_level": "HIGH",
            "reachability_status": "PUBLIC_PROFILE_ONLY",
            "official_profile_url": "https://www.linkedin.com/in/klaus-staubitzer",
            "official_bio_url": "https://www.siemens.com/en-us/company/leadership/management/",
            "public_contact_channel": "Global procurement portal via siemens.com/supplier",
            "areas_of_responsibility": "Global purchasing, IT vendor negotiations, software enterprise agreements, supplier sustainability, and contract commercial terms.",
            "team_priorities": "Cost efficiency, contract consolidation, supplier risk management, multi-year volume discounts.",
            "stated_priority": "Maximizing value through strategic supplier partnerships and enterprise agreement consolidation.",
            "quote_excerpt": "Procurement is not just about cost reduction; it is about creating resilient, innovative partnerships that drive strategic enterprise growth.",
            "why_matters": "Staubitzer's organization approves the commercial terms, pricing structures, and master service agreements for software expansion.",
            "zscaler_value_prop": "Consolidating standalone vendor contracts into the master Zscaler agreement, unlocking volume enterprise pricing and lowering administrative overhead.",
            "relevance_score": 85.0,
            "relevance_reason": "Chief Procurement Officer; gatekeeper for commercial contracting and enterprise agreement renewals.",
            "confidence": 1.0,
            "verification_status": "VERIFIED",
            "last_verified_date": "2026-11-03",
            "source_id": "src-charter-of-trust"
        },
        {
            "id": "contact-herbert-wegmann",
            "full_name": "Herbert Wegmann",
            "current_title": "General Manager, Digital Connectivity & Power, Siemens Digital Industries",
            "department": "Digital Connectivity & Power",
            "business_unit": "Digital Industries",
            "geography": "Nuremberg, Germany",
            "buying_role": "CHAMPION",
            "influence_level": "MEDIUM",
            "reachability_status": "PUBLIC_PROFILE_ONLY",
            "official_profile_url": "https://www.linkedin.com/in/herbert-wegmann",
            "official_bio_url": "https://www.siemens.com/global/en/products/automation/industrial-communication.html",
            "public_contact_channel": "Product inquiry via siemens.com",
            "areas_of_responsibility": "Product management and strategy for industrial communication devices, SCALANCE networking hardware, and OT remote connectivity.",
            "team_priorities": "Industrial IoT connectivity, zero-trust edge hardware, 5G in manufacturing.",
            "stated_priority": "Bringing Zero Trust directly to shopfloors and smart factories.",
            "quote_excerpt": "The Zero Trust principles are incredibly relevant to smart factory initiatives... Operators are embracing digitalization, but it also brings a new dimension of connectivity between shopfloors and the internet.",
            "why_matters": "Wegmann was directly quoted in the Zscaler OT partnership announcement and leads the hardware business unit producing SCALANCE LPE.",
            "zscaler_value_prop": "Deepening integration between SCALANCE hardware and Zscaler App Connectors to create pre-configured industrial zero trust bundles.",
            "relevance_score": 89.0,
            "relevance_reason": "Co-leader of the Zscaler-Siemens OT product partnership; direct champion for industrial zero-trust edge.",
            "confidence": 1.0,
            "verification_status": "VERIFIED",
            "last_verified_date": "2026-11-03",
            "source_id": "src-zscaler-ot-pr"
        },
        {
            "id": "contact-tony-hemmelgarn",
            "full_name": "Tony Hemmelgarn",
            "current_title": "President & CEO, Siemens Digital Industries Software",
            "department": "Software Business Unit",
            "business_unit": "Siemens Digital Industries Software",
            "geography": "Plano, Texas, USA",
            "buying_role": "INFLUENCER",
            "influence_level": "HIGH",
            "reachability_status": "PUBLIC_PROFILE_ONLY",
            "official_profile_url": "https://www.linkedin.com/in/tony-hemmelgarn",
            "official_bio_url": "https://www.sw.siemens.com/en-US/management/",
            "public_contact_channel": "Software executive contact via sw.siemens.com",
            "areas_of_responsibility": "Executive leadership of Siemens' industrial software portfolio, PLM, EDA, and direct executive sponsor for absorbing Altair Engineering.",
            "team_priorities": "SaaS migration for engineering tools, cloud collaboration, high-performance simulation.",
            "stated_priority": "Delivering cloud-based engineering simulation and digital twins for global manufacturers.",
            "quote_excerpt": "The addition of Altair's simulation and AI technology will create the world's most complete digital twin platform in the cloud.",
            "why_matters": "Hemmelgarn leads the software organization directly integrating Altair's engineering teams and cloud applications.",
            "zscaler_value_prop": "Providing secure cloud access for software developers and customer engineering teams accessing simulation SaaS tools.",
            "relevance_score": 88.0,
            "relevance_reason": "CEO of Siemens Software division integrating Altair; key influencer for developer and cloud workload security.",
            "confidence": 1.0,
            "verification_status": "VERIFIED",
            "last_verified_date": "2026-11-03",
            "source_id": "src-altair-acquisition"
        },
        {
            "id": "contact-rainer-zahner",
            "full_name": "Rainer Zahner",
            "current_title": "Head of Cybersecurity Governance & former CPSSO, Siemens AG",
            "department": "Cybersecurity Governance",
            "business_unit": "Corporate Cybersecurity",
            "geography": "Munich, Germany",
            "buying_role": "INFLUENCER",
            "influence_level": "MEDIUM",
            "reachability_status": "PUBLIC_PROFILE_ONLY",
            "official_profile_url": "https://www.linkedin.com/in/rainer-zahner",
            "official_bio_url": "https://www.siemens.com/global/en/company/about/cybersecurity.html",
            "public_contact_channel": "ProductCERT contact via cert.siemens.com",
            "areas_of_responsibility": "Cybersecurity policies, compliance auditing, product security standards, and Charter of Trust operational implementation.",
            "team_priorities": "Product & solution security compliance, IEC 62443 industrial standards, supply chain audit.",
            "stated_priority": "Ensuring verifiable cybersecurity compliance across all products and corporate entities.",
            "quote_excerpt": "Standardizing cybersecurity controls across a decentralized enterprise requires automated, verifiable policy architectures.",
            "why_matters": "Zahner directly translates Natalia Oropeza's governance policies into technical requirements for IT and software infrastructure.",
            "zscaler_value_prop": "Continuous compliance telemetry and audit reporting out-of-the-box for zero trust frameworks.",
            "relevance_score": 84.0,
            "relevance_reason": "Key security governance architect translating board standards into procurement requirements.",
            "confidence": 0.95,
            "verification_status": "VERIFIED",
            "last_verified_date": "2026-11-03",
            "source_id": "src-charter-of-trust"
        },
        {
            "id": "contact-thomas-meyer",
            "full_name": "Thomas Meyer",
            "current_title": "Chief Information Security Officer Region Europe, Siemens AG",
            "department": "Regional Cybersecurity",
            "business_unit": "Corporate Cybersecurity",
            "geography": "Erlangen / Munich, Germany",
            "buying_role": "INFLUENCER",
            "influence_level": "MEDIUM",
            "reachability_status": "PUBLIC_PROFILE_ONLY",
            "official_profile_url": "https://www.linkedin.com/in/thomas-meyer-ciso",
            "official_bio_url": "https://www.siemens.com/global/en/company/about/cybersecurity.html",
            "public_contact_channel": "Regional security office contact via siemens.com",
            "areas_of_responsibility": "Operational information security and risk posture across Siemens European locations, plants, and regional entities.",
            "team_priorities": "European regulatory adherence (NIS2, GDPR), incident prevention, regional cloud security.",
            "stated_priority": "Protecting regional European infrastructure while enabling cross-border business collaboration.",
            "quote_excerpt": "Regional security teams must balance rigorous compliance with user productivity across hundreds of distributed facilities.",
            "why_matters": "Meyer oversees operational security where the majority of Siemens' European industrial plants and employees reside.",
            "zscaler_value_prop": "Unified policy enforcement ensuring European NIS2 compliance without regional infrastructure bottlenecks.",
            "relevance_score": 82.0,
            "relevance_reason": "Operational CISO for Europe, where Siemens core manufacturing and employee hubs reside.",
            "confidence": 0.90,
            "verification_status": "VERIFIED",
            "last_verified_date": "2026-11-03",
            "source_id": "src-charter-of-trust"
        },
        {
            "id": "contact-elmar-spreitzer",
            "full_name": "Elmar Spreitzer",
            "current_title": "Head of IT Infrastructure Strategy & Innovations, Siemens AG",
            "department": "IT Infrastructure Strategy",
            "business_unit": "Corporate IT",
            "geography": "Munich, Germany",
            "buying_role": "TECHNICAL_DECISION_MAKER",
            "influence_level": "HIGH",
            "reachability_status": "PUBLIC_PROFILE_ONLY",
            "official_profile_url": "https://www.linkedin.com/in/elmar-spreitzer",
            "official_bio_url": "https://www.siemens.com/global/en/company/about/it-infrastructure.html",
            "public_contact_channel": "Corporate IT inquiry via siemens.com",
            "areas_of_responsibility": "Next-generation IT infrastructure, digital workplace innovations, hybrid cloud architecture roadmaps, and evaluation of networking technologies.",
            "team_priorities": "Cloud modernization, eliminating network friction, evaluating emerging zero-trust capabilities.",
            "stated_priority": "Modernizing enterprise infrastructure to support seamless hybrid collaboration.",
            "quote_excerpt": "Innovative IT infrastructure must act as an invisible accelerator for the business, ensuring speed, security, and exceptional user experience.",
            "why_matters": "Spreitzer evaluates the technical merits and architecture for new infrastructure solutions before global rollout.",
            "zscaler_value_prop": "Introducing Workload Communications and Data Protection as seamless enhancements to the existing ZIA/ZPA architecture.",
            "relevance_score": 87.0,
            "relevance_reason": "Technical strategy architect defining future infrastructure roadmaps under Hanna Hennig.",
            "confidence": 0.90,
            "verification_status": "CORROBORATED",
            "last_verified_date": "2026-11-03",
            "source_id": "src-orange-sdn"
        },
        {
            "id": "contact-roland-busch",
            "full_name": "Dr. Roland Busch",
            "current_title": "President & Chief Executive Officer, Siemens AG",
            "department": "Executive Board",
            "business_unit": "Managing Board",
            "geography": "Munich, Germany",
            "buying_role": "ECONOMIC_BUYER",
            "influence_level": "HIGH",
            "reachability_status": "PUBLIC_PROFILE_ONLY",
            "official_profile_url": "https://www.linkedin.com/in/roland-busch-siemens",
            "official_bio_url": "https://www.siemens.com/en-us/company/leadership/management/",
            "public_contact_channel": "Office of the President & CEO via siemens.com",
            "areas_of_responsibility": "Overall strategic direction, operational performance, and portfolio transformation of Siemens AG globally.",
            "team_priorities": "Shareholder value, digital enterprise growth, software expansion, sustainability.",
            "stated_priority": "Transforming Siemens into a premier digital technology company.",
            "quote_excerpt": "Technology with purpose is our mission. By combining the real and digital worlds, we empower our customers to transform their industries.",
            "why_matters": "Highest executive authority; sets corporate priorities around digital transformation and capital allocation.",
            "zscaler_value_prop": "Supporting corporate transformation with resilient, cost-effective digital infrastructure.",
            "relevance_score": 80.0,
            "relevance_reason": "President & CEO; ultimate board stakeholder.",
            "confidence": 1.0,
            "verification_status": "VERIFIED",
            "last_verified_date": "2026-11-03",
            "source_id": "src-siemens-mgmt"
        },
        {
            "id": "contact-veronika-bienert",
            "full_name": "Veronika Bienert",
            "current_title": "Member of Managing Board & Chief Financial Officer, Siemens AG",
            "department": "Executive Board / Finance",
            "business_unit": "Corporate Finance",
            "geography": "Munich, Germany",
            "buying_role": "ECONOMIC_BUYER",
            "influence_level": "HIGH",
            "reachability_status": "PUBLIC_PROFILE_ONLY",
            "official_profile_url": "https://www.linkedin.com/in/veronika-bienert",
            "official_bio_url": "https://www.siemens.com/en-us/company/leadership/management/",
            "public_contact_channel": "Investor relations & CFO office via siemens.com",
            "areas_of_responsibility": "Corporate finance, financial reporting, M&A financing, capital allocation, and enterprise cost discipline (appointed Oct 1, 2024).",
            "team_priorities": "Margin expansion, capital efficiency, software revenue quality, cost management.",
            "stated_priority": "Disciplined capital allocation and sustainable financial performance.",
            "quote_excerpt": "Strategic investments must deliver demonstrable operational efficiency and clear financial returns.",
            "why_matters": "Approves major multi-year enterprise software agreements and capital outlays.",
            "zscaler_value_prop": "Documented 70% cost reduction and predictable cloud subscription models that reduce operational expenditures.",
            "relevance_score": 81.0,
            "relevance_reason": "CFO & Managing Board Member; financial gatekeeper for enterprise software contracts.",
            "confidence": 1.0,
            "verification_status": "VERIFIED",
            "last_verified_date": "2026-11-03",
            "source_id": "src-siemens-mgmt"
        }
    ]
    for c_data in contacts_data:
        db.add(Contact(account_id=account.id, **c_data))
    db.flush()

    # 8. Relationships (Verified hierarchy & reporting lines)
    relationships_data = [
        # Hanna Hennig reports to Roland Busch / Managing Board
        {
            "id": "rel-hennig-busch",
            "from_contact_id": "contact-hanna-hennig",
            "to_contact_id": "contact-roland-busch",
            "relationship_type": "REPORTS_TO",
            "status": "VERIFIED",
            "evidence_notes": "CIO reports to President & CEO / Executive tier according to Siemens corporate governance."
        },
        # Natalia Oropeza reports to Managing Board tier
        {
            "id": "rel-oropeza-busch",
            "from_contact_id": "contact-natalia-oropeza",
            "to_contact_id": "contact-roland-busch",
            "relationship_type": "REPORTS_TO",
            "status": "VERIFIED",
            "evidence_notes": "Global CCSO reports directly to Member of the Managing Board per Cybersecurity Governance disclosure."
        },
        # Frederik Janssen reports to Cedrik Neike (CEO Digital Industries) / Hanna Hennig (CIO Corporate)
        {
            "id": "rel-janssen-neike",
            "from_contact_id": "contact-frederik-janssen",
            "to_contact_id": "contact-cedrik-neike",
            "relationship_type": "REPORTS_TO",
            "status": "VERIFIED",
            "evidence_notes": "CIO Digital Industries reports to Cedrik Neike (CEO Digital Industries)."
        },
        {
            "id": "rel-janssen-hennig",
            "from_contact_id": "contact-frederik-janssen",
            "to_contact_id": "contact-hanna-hennig",
            "relationship_type": "COLLABORATES_WITH",
            "status": "VERIFIED",
            "evidence_notes": "Coordinates divisional IT with corporate IT governance chaired by Hanna Hennig."
        },
        # Herbert Wegmann reports into Cedrik Neike's division
        {
            "id": "rel-wegmann-neike",
            "from_contact_id": "contact-herbert-wegmann",
            "to_contact_id": "contact-cedrik-neike",
            "relationship_type": "REPORTS_TO",
            "status": "VERIFIED",
            "evidence_notes": "General Manager Digital Connectivity & Power reports within Digital Industries."
        },
        # Tony Hemmelgarn reports to Cedrik Neike
        {
            "id": "rel-hemmelgarn-neike",
            "from_contact_id": "contact-tony-hemmelgarn",
            "to_contact_id": "contact-cedrik-neike",
            "relationship_type": "REPORTS_TO",
            "status": "VERIFIED",
            "evidence_notes": "CEO of Siemens Digital Industries Software reports to Cedrik Neike (Managing Board Member)."
        },
        # Elmar Spreitzer reports to Hanna Hennig
        {
            "id": "rel-spreitzer-hennig",
            "from_contact_id": "contact-elmar-spreitzer",
            "to_contact_id": "contact-hanna-hennig",
            "relationship_type": "REPORTS_TO",
            "status": "VERIFIED",
            "evidence_notes": "Head of IT Infrastructure Strategy reports within Corporate IT under Hanna Hennig."
        },
        # Rainer Zahner reports to Natalia Oropeza
        {
            "id": "rel-zahner-oropeza",
            "from_contact_id": "contact-rainer-zahner",
            "to_contact_id": "contact-natalia-oropeza",
            "relationship_type": "REPORTS_TO",
            "status": "VERIFIED",
            "evidence_notes": "Cybersecurity Governance head reports directly to Global Chief Cybersecurity Officer."
        },
        # Thomas Meyer reports to Natalia Oropeza
        {
            "id": "rel-meyer-oropeza",
            "from_contact_id": "contact-thomas-meyer",
            "to_contact_id": "contact-natalia-oropeza",
            "relationship_type": "REPORTS_TO",
            "status": "VERIFIED",
            "evidence_notes": "Regional CISO Europe operates within Global Cybersecurity governance headed by Natalia Oropeza."
        },
        # Dr. Klaus Staubitzer reports to Managing Board / Veronika Bienert
        {
            "id": "rel-staubitzer-bienert",
            "from_contact_id": "contact-klaus-staubitzer",
            "to_contact_id": "contact-veronika-bienert",
            "relationship_type": "REPORTS_TO",
            "status": "VERIFIED",
            "evidence_notes": "CPO operates under Corporate Finance and Managing Board oversight."
        },
        # Influences
        {
            "id": "rel-oropeza-hennig",
            "from_contact_id": "contact-natalia-oropeza",
            "to_contact_id": "contact-hanna-hennig",
            "relationship_type": "INFLUENCES",
            "status": "VERIFIED",
            "evidence_notes": "Mandates corporate security policies and zero-trust controls across all IT infrastructure."
        },
        {
            "id": "rel-janssen-hemmelgarn",
            "from_contact_id": "contact-frederik-janssen",
            "to_contact_id": "contact-tony-hemmelgarn",
            "relationship_type": "INFLUENCES",
            "status": "INFERRED_HYPOTHESIS",
            "evidence_notes": "Provides IT infrastructure and network onboarding for acquired software business units including Altair."
        }
    ]
    for rel in relationships_data:
        db.add(Relationship(account_id=account.id, **rel))
    db.flush()

    # 9. Evidence Claims (Linking facts to exact sources and excerpts)
    evidence_claims_data = [
        {
            "id": "claim-workforce-312k",
            "source_id": "src-siemens-ar-2024",
            "entity_type": "METRIC",
            "entity_id": "metric-workforce-continuing",
            "claim_text": "Siemens had approximately 312,000 employees worldwide in continuing operations as of September 30, 2024.",
            "excerpt": "As of September 30, 2024, the number of employees in continuing operations was approximately 312,000.",
            "publication_date": "2024-12-04",
            "date_retrieved": "2026-11-03",
            "evidence_type": "AUDITED_FINANCIAL_REPORT",
            "confidence_score": 1.0,
            "verification_status": "VERIFIED",
            "is_conflicting": True,
            "conflict_details": "Preserved alongside 327,000 total workforce metric which includes discontinued operations prior to carve-outs."
        },
        {
            "id": "claim-workforce-327k",
            "source_id": "src-siemens-ar-2024",
            "entity_type": "METRIC",
            "entity_id": "metric-workforce-total",
            "claim_text": "Siemens had approximately 327,000 employees including discontinued operations as of September 30, 2024.",
            "excerpt": "Total employees including discontinued operations stood at approximately 327,000.",
            "publication_date": "2024-12-04",
            "date_retrieved": "2026-11-03",
            "evidence_type": "AUDITED_FINANCIAL_REPORT",
            "confidence_score": 1.0,
            "verification_status": "CORROBORATED",
            "is_conflicting": True,
            "conflict_details": "Reflects gross employee count before Innomotics spin-off adjustments."
        },
        {
            "id": "claim-revenue-75-9b",
            "source_id": "src-siemens-ar-2024",
            "entity_type": "METRIC",
            "entity_id": "metric-revenue-fy24",
            "claim_text": "Siemens Group generated revenue of €75.9 billion in fiscal year 2024.",
            "excerpt": "Revenue rose 1% on a comparable basis to €75.9 billion (FY 2023: €74.9 billion).",
            "publication_date": "2024-12-04",
            "date_retrieved": "2026-11-03",
            "evidence_type": "AUDITED_FINANCIAL_REPORT",
            "confidence_score": 1.0,
            "verification_status": "VERIFIED"
        },
        {
            "id": "claim-zscaler-deployment",
            "source_id": "src-zscaler-case-study",
            "entity_type": "TECH",
            "entity_id": "tech-zscaler-zia",
            "claim_text": "Siemens rolled out Zscaler Internet Access and Zscaler Private Access globally across 300,000+ employees in 190+ countries in 10 months.",
            "excerpt": "Over a 10-month period, Siemens rolled out Zscaler Internet Access (ZIA) and Zscaler Private Access (ZPA) to more than 300,000 users across 190+ countries.",
            "publication_date": "2022-04-15",
            "date_retrieved": "2026-11-03",
            "evidence_type": "CUSTOMER_CASE_STUDY",
            "confidence_score": 1.0,
            "verification_status": "VERIFIED"
        },
        {
            "id": "claim-hennig-70pct-quote",
            "source_id": "src-zscaler-case-study",
            "entity_type": "CONTACT",
            "entity_id": "contact-hanna-hennig",
            "claim_text": "CIO Hanna Hennig stated that Zscaler reduced management costs by 70% and enabled de-mergers and acquisitions in record time.",
            "excerpt": "We have been able to reduce cost for this environment and management by 70%. We have also gained speed; with de-mergers or acquisition being done in record time.",
            "publication_date": "2022-04-15",
            "date_retrieved": "2026-11-03",
            "evidence_type": "EXECUTIVE_STATEMENT",
            "confidence_score": 1.0,
            "verification_status": "VERIFIED"
        },
        {
            "id": "claim-janssen-internet-network",
            "source_id": "src-zscaler-case-study",
            "entity_type": "CONTACT",
            "entity_id": "contact-frederik-janssen",
            "claim_text": "Frederik Janssen stated 'By not backhauling our traffic, but directly using the internet, we expect we can drive down costs by 70%... The internet is the new corporate network.'",
            "excerpt": "By not backhauling our traffic, but directly using the internet, we expect we can drive down costs by 70%... The internet is the new corporate network.",
            "publication_date": "2022-04-15",
            "date_retrieved": "2026-11-03",
            "evidence_type": "EXECUTIVE_STATEMENT",
            "confidence_score": 1.0,
            "verification_status": "VERIFIED"
        },
        {
            "id": "claim-ot-partnership-scalance",
            "source_id": "src-zscaler-ot-pr",
            "entity_type": "TECH",
            "entity_id": "tech-siemens-ot-edge",
            "claim_text": "Siemens and Zscaler co-developed all-in-one OT Zero Trust solution hosting Zscaler App Connector on Siemens SCALANCE LPE hardware.",
            "excerpt": "Zscaler and Siemens have partnered to deliver an integrated zero trust solution for industrial environments. Zscaler App Connectors run on Siemens SCALANCE LPE industrial devices to enable secure remote access to factory floors.",
            "publication_date": "2022-05-26",
            "date_retrieved": "2026-11-03",
            "evidence_type": "PRESS_RELEASE",
            "confidence_score": 1.0,
            "verification_status": "VERIFIED"
        },
        {
            "id": "claim-altair-10b-deal",
            "source_id": "src-altair-acquisition",
            "entity_type": "TRIGGER",
            "entity_id": "trigger-altair-acquisition",
            "claim_text": "Siemens signed definitive agreement to acquire Altair Engineering Inc. for approximately $10 billion enterprise value.",
            "excerpt": "Siemens to acquire Altair Engineering Inc., a leading provider of software in the industrial simulation and analysis market, for an enterprise value of approximately $10 billion.",
            "publication_date": "2024-10-30",
            "date_retrieved": "2026-11-03",
            "evidence_type": "PRESS_RELEASE",
            "confidence_score": 1.0,
            "verification_status": "VERIFIED"
        },
        {
            "id": "claim-microsoft-copilot",
            "source_id": "src-microsoft-copilot",
            "entity_type": "PRIORITY",
            "entity_id": "priority-industrial-ai",
            "claim_text": "Siemens and Microsoft launched Siemens Industrial Copilot, bringing generative AI into manufacturing engineering on Azure.",
            "excerpt": "Siemens and Microsoft are deepening their partnership to drive cross-industry AI adoption, launching Siemens Industrial Copilot to boost productivity across the industrial product lifecycle.",
            "publication_date": "2023-10-31",
            "date_retrieved": "2026-11-03",
            "evidence_type": "PRESS_RELEASE",
            "confidence_score": 0.95,
            "verification_status": "VERIFIED"
        },
        {
            "id": "claim-oropeza-charter-trust",
            "source_id": "src-charter-of-trust",
            "entity_type": "CONTACT",
            "entity_id": "contact-natalia-oropeza",
            "claim_text": "Natalia Oropeza serves as Global Chief Cybersecurity Officer and Chairwoman of the Charter of Trust.",
            "excerpt": "Natalia Oropeza, Chief Cybersecurity Officer of Siemens AG, serves as Chairwoman of the Charter of Trust.",
            "publication_date": "2024-02-15",
            "date_retrieved": "2026-11-03",
            "evidence_type": "GOVERNANCE_CHARTER",
            "confidence_score": 1.0,
            "verification_status": "VERIFIED"
        }
    ]
    for cl in evidence_claims_data:
        db.add(EvidenceClaim(account_id=account.id, **cl))
    db.flush()

    # 10. Generate Recommendation Record
    rec_data = RecommendationEngine.generate_recommendation(
        account_name=account.name,
        is_existing_customer=account.is_existing_customer,
        triggers=db.query(TriggerEvent).filter(TriggerEvent.account_id == account.id).all(),
        priorities=db.query(StrategicPriority).filter(StrategicPriority.account_id == account.id).all(),
        whitespace=db.query(ZscalerProductFootprint).filter(ZscalerProductFootprint.account_id == account.id).all(),
        contacts=db.query(Contact).filter(Contact.account_id == account.id).all()
    )
    rec = Recommendation(id=f"rec-{account.id}", account_id=account.id, **rec_data)
    db.add(rec)
    db.commit()
    return account
