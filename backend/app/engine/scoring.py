from typing import Dict, Any, List

def calculate_account_attractiveness_score(
    is_existing_customer: bool,
    employee_count_numeric: int,
    revenue_billions: float,
    has_large_ot_footprint: bool,
    unlocked_expansion_categories: int
) -> tuple[float, str]:
    """
    Transparent weighted rules-based calculation of Account Attractiveness (0-100).
    Factors:
    - Scale & TAM footprint: 35% (Enterprise tier > 100k employees, multi-billion revenue)
    - Existing Customer Momentum: 25% (Zero trust already proven at board level, lower adoption barrier)
    - Expansion Whitespace Breadth: 25% (Multiple viable modules: Data Protection, Cloud Workloads, AI Security, OT)
    - Strategic Synergies: 15% (Co-innovation, OT partnership)
    """
    score = 0.0
    breakdown = []

    # 1. Scale
    if employee_count_numeric > 100000:
        score += 25.0
        breakdown.append(f"Workforce scale > 100k seats ({employee_count_numeric:,} reported) (+25)")
    elif employee_count_numeric > 20000:
        score += 15.0
        breakdown.append(f"Workforce scale > 20k seats ({employee_count_numeric:,} reported) (+15)")
    elif employee_count_numeric > 0:
        score += 5.0
        breakdown.append(f"Enterprise scale ({employee_count_numeric:,} reported seats) (+5)")
    else:
        score += 2.0
        breakdown.append("Workforce undisclosed in public records (Baseline +2)")

    if revenue_billions > 50.0:
        score += 10.0
        breakdown.append(f"Annual revenue > $50B (${revenue_billions:.1f}B reported) (+10)")
    elif revenue_billions > 10.0:
        score += 5.0
        breakdown.append(f"Annual revenue > $10B (${revenue_billions:.1f}B reported) (+5)")
    elif revenue_billions > 0.0:
        score += 2.0
        breakdown.append(f"Annual revenue reported (${revenue_billions:.1f}B) (+2)")
    else:
        score += 1.0
        breakdown.append("Audited revenue undisclosed or aggregated (Baseline +1)")

    # 2. Existing Customer Status
    if is_existing_customer:
        score += 25.0
        breakdown.append("Existing Zscaler customer with proven enterprise deployment (+25)")
    else:
        score += 10.0
        breakdown.append("New logo prospect (+10)")

    # 3. Whitespace Breadth
    expansion_pts = min(25.0, unlocked_expansion_categories * 6.25)
    score += expansion_pts
    breakdown.append(f"{unlocked_expansion_categories} distinct expansion whitespaces identified (+{expansion_pts:.1f})")

    # 4. Strategic Footprint
    if has_large_ot_footprint:
        score += 15.0
        breakdown.append("Industrial operational technology (OT) footprint & edge expansion potential (+15)")

    final_score = round(min(100.0, score), 1)
    explanation = "Attractiveness breakdown: " + "; ".join(breakdown) + f". Final score: {final_score}/100."
    return final_score, explanation


def calculate_timing_score(
    triggers: List[Dict[str, Any]],
    has_recent_major_acquisition: bool = False,
    has_strategic_ai_initiative: bool = False,
    regulatory_pressures: bool = False
) -> tuple[float, str]:
    """
    Transparent weighted rules-based calculation of Account Timing (0-100).
    Uses account-specific triggers and dates. Never hardcodes unrelated company events.
    """
    score = 0.0
    breakdown = []

    # Check for actual acquisition trigger in triggers list
    acq_trigger = next((t for t in triggers if any(k in str(t.get("event_type", "")).lower() or k in str(t.get("title", "")).lower() for k in ["m&a", "acquisition", "merger"])), None)
    if acq_trigger or has_recent_major_acquisition:
        score += 35.0
        acq_name = acq_trigger.get("title", "Active Corporate Acquisition") if acq_trigger else "Active Corporate Acquisition"
        breakdown.append(f"Major corporate acquisition ({acq_name}) requiring cloud & identity integration (+35)")

    # Check for actual AI initiative trigger
    ai_trigger = next((t for t in triggers if any(k in str(t.get("event_type", "")).lower() or k in str(t.get("title", "")).lower() for k in ["ai", "generative ai", "copilot", "llm", "bedrock", "gemini"])), None)
    if ai_trigger or has_strategic_ai_initiative:
        score += 25.0
        ai_name = ai_trigger.get("title", "Enterprise AI Initiative") if ai_trigger else "Enterprise AI Program"
        breakdown.append(f"Strategic generative AI rollouts ({ai_name}) creating data security urgency (+25)")

    # Check for actual OT trigger
    ot_trigger = next((t for t in triggers if any(k in str(t.get("event_type", "")).lower() or k in str(t.get("title", "")).lower() for k in ["ot", "industrial", "factory", "automation", "plant"])), None)
    if ot_trigger:
        score += 20.0
        ot_name = ot_trigger.get("title", "OT Modernization")
        breakdown.append(f"Operational technology zero trust requirements ({ot_name}) (+20)")

    # Check for regulatory trigger
    reg_trigger = next((t for t in triggers if any(k in str(t.get("event_type", "")).lower() or k in str(t.get("title", "")).lower() for k in ["regulatory", "compliance", "nis2", "gdpr", "sovereign"])), None)
    if reg_trigger or regulatory_pressures:
        score += 20.0
        reg_name = reg_trigger.get("title", "Cybersecurity Regulatory Deadlines") if reg_trigger else "Cybersecurity & Data Privacy Mandates"
        breakdown.append(f"Compliance & regulatory windows ({reg_name}) (+20)")

    # Base timing for active enterprise updates
    if len(triggers) >= 2:
        score += 10.0
        breakdown.append(f"{len(triggers)} verified high-impact triggers recorded (+10)")
    elif len(triggers) == 1:
        score += 5.0
        breakdown.append("1 verified strategic trigger recorded (+5)")
    else:
        score += 5.0
        breakdown.append("Baseline enterprise digital transformation window (+5)")

    final_score = round(min(100.0, score), 1)
    explanation = "Timing breakdown: " + "; ".join(breakdown) + f". Final score: {final_score}/100."
    return final_score, explanation


def calculate_evidence_coverage_score(
    total_claims: int,
    verified_claims: int,
    corroborated_claims: int,
    official_sources_count: int,
    conflicting_claims: int
) -> tuple[float, str]:
    """
    Transparent calculation of Evidence Coverage & Groundedness (0-100).
    Formula:
    Coverage = (Verified + Corroborated * 1.2) / Total * 70% + Source Quality (30%) - Conflicts Penalty (5%)
    """
    if total_claims == 0:
        return 0.0, "No claims extracted yet."

    base_ratio = (verified_claims + (corroborated_claims * 1.1)) / max(1, total_claims)
    claim_score = min(70.0, base_ratio * 70.0)

    source_score = min(30.0, official_sources_count * 3.5)
    conflict_penalty = min(15.0, conflicting_claims * 3.0)

    final_score = round(max(0.0, min(100.0, claim_score + source_score - conflict_penalty)), 1)
    explanation = (
        f"Evidence coverage: {verified_claims} verified & {corroborated_claims} corroborated out of {total_claims} claims "
        f"({claim_score:.1f} pts), backed by {official_sources_count} primary/official disclosures ({source_score:.1f} pts)"
        + (f", with {conflicting_claims} flagged conflicts (-{conflict_penalty:.1f} pts)." if conflicting_claims > 0 else ".")
    )
    return final_score, explanation


def calculate_stakeholder_relevance_score(
    contact: Dict[str, Any],
    top_trigger_category: str
) -> tuple[float, str]:
    """
    Calculates stakeholder relevance based on buying role, department, public quotes, and trigger alignment.
    """
    role = contact.get("buying_role", "UNKNOWN")
    dept = contact.get("department", "")
    influence = contact.get("influence_level", "MEDIUM")
    
    score = 50.0 # base
    reasons = []

    if role == "TECHNICAL_DECISION_MAKER":
        score += 25.0
        reasons.append("Direct technical decision authority (+25)")
    elif role == "CHAMPION":
        score += 25.0
        reasons.append("Evidenced internal champion and transformation leader (+25)")
    elif role == "ECONOMIC_BUYER":
        score += 20.0
        reasons.append("Budgetary and board authority (+20)")
    elif role == "PROCUREMENT_APPROVER":
        score += 15.0
        reasons.append("Commercial procurement gatekeeper (+15)")
    elif role == "BLOCKER":
        score += 15.0
        reasons.append("Mandatory security and compliance approver (+15)")

    if influence == "HIGH":
        score += 15.0
        reasons.append("High executive influence level (+15)")

    if contact.get("stated_priority"):
        score += 10.0
        reasons.append("Directly documented public priority and quote (+10)")

    final_score = round(min(100.0, score), 1)
    explanation = "; ".join(reasons)
    return final_score, explanation
