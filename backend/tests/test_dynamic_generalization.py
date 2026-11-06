import pytest
import asyncio
from backend.app.discovery.entity_resolver import EntityResolver
from backend.app.discovery.source_discovery import SourceDiscoveryManager
from backend.app.discovery.fact_extractor import FactExtractor
from backend.app.engine.recommendation_engine import RecommendationEngine
from backend.app.engine.scoring import (
    calculate_account_attractiveness_score,
    calculate_timing_score,
    calculate_evidence_coverage_score
)
from backend.app.db import SessionLocal
from backend.app.models.entities import Account, Contact, TriggerEvent, Recommendation

@pytest.mark.asyncio
async def test_entity_resolution_us_public():
    """Tests resolution of large US public corporations (Amazon, Alphabet, Microsoft)."""
    amazon = await EntityResolver.resolve("Amazon")
    assert amazon["is_resolved"] is True
    assert "seattle" in amazon["headquarters"].lower()
    assert amazon["company_type"] == "Public"
    assert amazon["ticker"] in ["AMZN", "NASDAQ: AMZN"] or amazon.get("ticker") is not None

    alphabet = await EntityResolver.resolve("Alphabet Inc.")
    assert alphabet["is_resolved"] is True
    assert "mountain view" in alphabet["headquarters"].lower()
    assert alphabet["company_type"] == "Public"

@pytest.mark.asyncio
async def test_entity_resolution_parent_subsidiary():
    """Tests parent vs subsidiary distinction for Google LLC -> Alphabet Inc."""
    google = await EntityResolver.resolve("Google LLC")
    assert google["is_resolved"] is True
    assert google["is_subsidiary"] is True
    assert google["parent_company"] == "Alphabet Inc."
    assert "mountain view" in google["headquarters"].lower()
    assert "Alphabet Inc." in google["identity_notes"]

@pytest.mark.asyncio
async def test_entity_resolution_global_enterprises():
    """Tests resolution across European and Indian industrial enterprises."""
    reliance = await EntityResolver.resolve("Reliance Industries")
    assert reliance["is_resolved"] is True
    assert "mumbai" in reliance["headquarters"].lower()
    assert "india" in reliance["headquarters"].lower()

    bmw = await EntityResolver.resolve("BMW")
    assert bmw["is_resolved"] is True
    assert "munich" in bmw["headquarters"].lower()

@pytest.mark.asyncio
async def test_entity_resolution_fictional_unknown():
    """Tests that a fictional or unresolvable company remains UNKNOWN and does not hallucinate."""
    unknown = await EntityResolver.resolve("Fictional Quantum Obscure 9999 Ltd")
    assert unknown["is_resolved"] is False
    assert unknown["headquarters"] == "UNKNOWN"
    assert unknown["country"] == "UNKNOWN"

@pytest.mark.asyncio
async def test_fact_extraction_no_siemens_leakage():
    """Verifies that extracting facts for Amazon does not leak Siemens data or Munich headquarters."""
    entity = await EntityResolver.resolve("Amazon")
    sources = await SourceDiscoveryManager().discover_sources("test-amzn", entity)
    facts = FactExtractor.extract("test-amzn", entity, sources)

    # Must be Seattle, NOT Munich
    assert "seattle" in facts.headquarters.lower()
    assert "munich" not in facts.headquarters.lower()
    # Employee count must reflect Amazon scale (>1M), not 311,000
    assert facts.workforce_numeric > 1000000
    # Revenue must reflect Amazon (>500B), not Siemens 75.9B
    assert facts.revenue_numeric_billions > 400.0
    # Check triggers do not mention Altair or Siemens Copilot
    trigger_text = " ".join([t[0] + " " + t[3] for t in facts.triggers]).lower()
    assert "altair" not in trigger_text
    assert "siemens industrial copilot" not in trigger_text

def test_recommendation_account_agnostic():
    """Verifies recommendations for dynamic accounts do not default to Frederik Janssen or Altair."""
    # Test with contacts
    contacts = [
        type("ContactStub", (), {
            "id": "c1",
            "full_name": "Andy Jassy",
            "current_title": "President & CEO",
            "buying_role": "ECONOMIC_BUYER",
            "stated_priority": "Enterprise AI expansion and customer obsession"
        })(),
        type("ContactStub", (), {
            "id": "c2",
            "full_name": "Adam Selipsky",
            "current_title": "Cloud Strategy Lead",
            "buying_role": "CHAMPION",
            "stated_priority": "Cloud scalability and zero trust"
        })()
    ]
    triggers = [
        type("TriggerStub", (), {
            "title": "AWS Bedrock Enterprise Expansion",
            "event_type": "Product Launch",
            "description": "Expanded generative AI cloud services.",
            "business_impact": "Accelerates enterprise cloud adoption."
        })()
    ]

    rec = RecommendationEngine.generate_recommendation(
        account_name="Amazon",
        is_existing_customer=False,
        triggers=triggers,
        priorities=[],
        whitespace=[],
        contacts=contacts
    )

    assert "frederik janssen" not in rec["suggested_opener_draft"].lower()
    assert "altair" not in rec["why_now"].lower()
    assert "siemens" not in rec["why_this_account"].lower()
    assert "Amazon" in rec["why_this_account"]
    assert "AWS Bedrock Enterprise Expansion" in rec["why_now"]

def test_recommendation_empty_contacts_honest_message():
    """Verifies that an account with no contacts receives an honest insufficient data message."""
    rec = RecommendationEngine.generate_recommendation(
        account_name="Obscure Corp",
        is_existing_customer=False,
        triggers=[],
        priorities=[],
        whitespace=[],
        contacts=[]
    )
    assert rec["recommended_first_contact_id"] is None
    assert "Insufficient verified" in rec["why_this_stakeholder"]
    assert "Draft unavailable" in rec["suggested_opener_draft"] or "Outreach draft unavailable" in rec["suggested_opener_draft"]

def test_scoring_account_agnostic_timing():
    """Verifies timing score explanation only references actual triggers, not hardcoded Altair."""
    triggers = [
        {"title": "AWS Bedrock Enterprise AI", "event_type": "Product Launch"},
        {"title": "Global Cloud Regional Modernization", "event_type": "Cloud Transformation"}
    ]
    score, exp = calculate_timing_score(triggers=triggers)
    assert "altair" not in exp.lower()
    assert "siemens industrial copilot" not in exp.lower()
    assert "AWS Bedrock Enterprise AI" in exp

def test_siemens_flagship_remains_intact():
    """Verifies that Siemens AG account data and recommendations remain 100% intact."""
    db = SessionLocal()
    siemens = db.query(Account).filter(Account.id == "siemens-ag").first()
    assert siemens is not None
    assert "Munich, Germany" in siemens.headquarters
    assert siemens.attractiveness_score == 92.0
    assert siemens.timing_score == 88.0

    contacts = db.query(Contact).filter(Contact.account_id == "siemens-ag").all()
    assert len(contacts) == 13
    assert any("Frederik Janssen" in c.full_name for c in contacts)

    rec = db.query(Recommendation).filter(Recommendation.account_id == "siemens-ag").first()
    assert rec is not None
    assert "Altair" in rec.outreach_angle or "Altair" in rec.why_now
    db.close()
