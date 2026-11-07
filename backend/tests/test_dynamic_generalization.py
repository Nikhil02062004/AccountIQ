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

def test_financial_normalization_multi_currency():
    """Tests financial normalizer across multi-currency figures, European notations, and missing values."""
    from backend.app.discovery.fact_extractor import FinancialNormalizer

    # European millions: €22,465 million -> 22.465B EUR
    fmt, val, sym, iso, per = FinancialNormalizer.normalize("€22,465 million", default_period="FY2025")
    assert val == 22.465
    assert iso == "EUR"
    assert "€22.465B" in fmt

    # US Billions: US$ 716.9 billion (2025)
    fmt, val, sym, iso, per = FinancialNormalizer.normalize("US$ 716.9 billion (2025)")
    assert val == 716.9
    assert iso == "USD"
    assert "$716.9B" in fmt
    assert "2025" in per

    # British Pounds: £15.2 billion (2024)
    fmt, val, sym, iso, per = FinancialNormalizer.normalize("£15.2 billion (2024)")
    assert val == 15.2
    assert iso == "GBP"
    assert "£15.2B" in fmt

    # Swiss Francs: CHF 29.8 billion
    fmt, val, sym, iso, per = FinancialNormalizer.normalize("CHF 29.8 billion")
    assert val == 29.8
    assert iso == "CHF"

    # Missing value MUST remain UNKNOWN, never $0.0B
    fmt, val, sym, iso, per = FinancialNormalizer.normalize(None)
    assert fmt == "UNKNOWN"
    assert val == 0.0

def test_workforce_normalization_ranges_and_dates():
    """Tests workforce normalizer preserving ranges and extracting reporting periods."""
    from backend.app.discovery.fact_extractor import WorkforceNormalizer

    # Single figure with FY
    fmt, num, per = WorkforceNormalizer.normalize("42,000 (FY26)")
    assert num == 42000
    assert "42,000" in fmt

    # Preserving range
    fmt, num, per = WorkforceNormalizer.normalize("10,000–25,000")
    assert "10,000" in fmt and "25,000" in fmt
    assert num == 25000

    # Missing remains UNKNOWN
    fmt, num, per = WorkforceNormalizer.normalize(None)
    assert fmt == "UNKNOWN"
    assert num == 0

def test_central_data_quality_gate():
    """Tests DataQualityGate enforcement for valid, partial, and rejected entities."""
    from backend.app.engine.quality_gate import DataQualityGate
    from backend.app.discovery.fact_extractor import ExtractedFacts
    from backend.app.discovery.source_discovery import DiscoveredSource

    # 1. Unresolved entity must FAIL
    unresolved_entity = {"is_resolved": False, "query": "Unknown Nonexistent Firm"}
    res = DataQualityGate.evaluate("unknown", unresolved_entity, [], ExtractedFacts())
    assert res.is_valid is False
    assert res.pipeline_status == "FAILED"

    # 2. Resolved entity with partial fields becomes PARTIALLY_COMPLETED
    resolved_entity = {"is_resolved": True, "canonical_name": "Test Firm"}
    sources = [DiscoveredSource(id="s1", name="Src", url="https://test.com", source_type="OFFICIAL_WEBSITE")]
    partial_facts = ExtractedFacts()
    partial_facts.headquarters = "London, UK"
    partial_facts.annual_revenue = "UNKNOWN" # Missing revenue
    res_partial = DataQualityGate.evaluate("test", resolved_entity, sources, partial_facts)
    assert res_partial.is_valid is True
    assert res_partial.pipeline_status == "PARTIALLY_COMPLETED"
    assert "annual_revenue" in res_partial.unknown_fields

@pytest.mark.asyncio
async def test_it_services_resolution_capgemini():
    """Tests generic identity resolution for an IT Services firm (Capgemini)."""
    capgemini = await EntityResolver.resolve("Capgemini")
    assert capgemini["is_resolved"] is True
    assert "paris" in capgemini["headquarters"].lower() or "france" in capgemini["headquarters"].lower()
    assert "consulting" in capgemini["industry"].lower() or "information technology" in capgemini["industry"].lower() or "services" in capgemini["industry"].lower()

