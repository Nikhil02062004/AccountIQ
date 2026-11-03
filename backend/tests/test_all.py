import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.db import SessionLocal, Base, engine
from backend.app.models.entities import (
    Account, Source, EvidenceClaim, Contact, TechnologyVendor,
    TriggerEvent, StrategicPriority, Recommendation
)
from backend.app.engine.scoring import (
    calculate_account_attractiveness_score,
    calculate_timing_score,
    calculate_evidence_coverage_score,
    calculate_stakeholder_relevance_score
)
from backend.app.engine.validator import EvidenceValidator
from backend.app.engine.recommendation_engine import RecommendationEngine
from backend.app.seed.siemens_seed import seed_siemens_data

client = TestClient(app)

@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_siemens_data(db)
    yield db
    db.close()


def test_1_account_creation(db_session):
    account = db_session.query(Account).filter(Account.id == "siemens-ag").first()
    assert account is not None
    assert account.name == "Siemens AG"
    assert account.is_existing_customer is True
    assert "Existing Customer" in account.customer_type
    assert len(account.day_1_justification.split()) < 150


def test_2_source_ingestion(db_session):
    sources = db_session.query(Source).filter(Source.account_id == "siemens-ag").all()
    assert len(sources) >= 5
    urls = [s.url for s in sources]
    assert "https://www.zscaler.com/customers/siemens" in urls
    assert any("annual-report" in s.id or "siemens-ar-2024" in s.id for s in sources)


def test_3_evidence_extraction(db_session):
    claims = db_session.query(EvidenceClaim).filter(EvidenceClaim.account_id == "siemens-ag").all()
    assert len(claims) >= 8
    for c in claims:
        assert c.claim_text is not None
        assert c.excerpt is not None
        assert c.source_id is not None
        assert c.confidence_score > 0.0


def test_4_evidence_to_claim_linking(db_session):
    claims = db_session.query(EvidenceClaim).filter(EvidenceClaim.account_id == "siemens-ag").all()
    for c in claims:
        source = db_session.query(Source).filter(Source.id == c.source_id).first()
        assert source is not None, f"Claim {c.id} points to missing source {c.source_id}"
        assert source.url.startswith("http")


def test_5_contact_validation(db_session):
    contacts = db_session.query(Contact).filter(Contact.account_id == "siemens-ag").all()
    assert 8 <= len(contacts) <= 15
    names = [c.full_name for c in contacts]
    assert "Hanna Hennig" in names
    assert "Natalia Oropeza" in names
    assert "Frederik Janssen" in names
    
    # Assert no fake emails exist
    for c in contacts:
        assert c.public_contact_channel is not None
        assert "@" not in str(c.public_contact_channel) or "cert" in str(c.public_contact_channel), \
            "Fabricated personal email detected!"


def test_6_confidence_classification():
    weight_ar = EvidenceValidator.classify_source_weight("ANNUAL_REPORT", True)
    weight_blog = EvidenceValidator.classify_source_weight("BLOG", False)
    assert weight_ar >= 0.95
    assert weight_blog <= 0.70


def test_7_account_scoring():
    att_score, att_exp = calculate_account_attractiveness_score(
        is_existing_customer=True,
        employee_count_numeric=312000,
        revenue_billions=75.9,
        has_large_ot_footprint=True,
        unlocked_expansion_categories=4
    )
    assert 85.0 <= att_score <= 100.0
    assert "Workforce scale" in att_exp

    time_score, time_exp = calculate_timing_score(
        triggers=[{"title": "Altair", "event_type": "M&A Integration"}],
        has_recent_major_acquisition=True,
        has_strategic_ai_initiative=True,
        regulatory_pressures=True
    )
    assert time_score >= 80.0


def test_8_buying_committee_graph_api():
    response = client.get("/api/accounts/siemens-ag/committee-graph")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data and "edges" in data
    assert len(data["nodes"]) >= 10
    assert len(data["edges"]) >= 8


def test_9_recommendation_generation(db_session):
    rec = db_session.query(Recommendation).filter(Recommendation.account_id == "siemens-ag").first()
    assert rec is not None
    assert rec.first_contact is not None
    assert "Frederik Janssen" in rec.first_contact.full_name
    assert "Altair" in rec.outreach_angle
    assert len(rec.suggested_opener_draft) > 50


def test_10_missing_evidence_handling(db_session):
    techs = db_session.query(TechnologyVendor).filter(TechnologyVendor.account_id == "siemens-ag").all()
    unknown_techs = [t for t in techs if t.deployment_status == "UNKNOWN"]
    assert len(unknown_techs) >= 1
    assert unknown_techs[0].vendor == "UNKNOWN"
    assert unknown_techs[0].verification_status == "UNKNOWN"


def test_11_conflicting_evidence_handling(db_session):
    claims = db_session.query(EvidenceClaim).filter(EvidenceClaim.account_id == "siemens-ag").all()
    conflicts = [c for c in claims if c.is_conflicting]
    assert len(conflicts) >= 2, "Conflicting employee counts must be flagged and preserved!"
    for c in conflicts:
        assert c.conflict_details is not None


def test_12_second_account_isolation(db_session):
    # Trigger research for ABB via API (TestClient automatically executes BackgroundTasks)
    response = client.post("/api/research/new", json={
        "company_name": "ABB Ltd",
        "industry": "Industrial Technology",
        "is_existing_customer": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["account_id"] == "abb-ltd"

    # Refresh session to see committed background task records
    db_session.expire_all()
    abb_account = db_session.query(Account).filter(Account.id == "abb-ltd").first()
    assert abb_account is not None
    assert abb_account.name == "ABB Ltd"

    # Verify no Siemens contacts were inherited
    abb_contacts = [c.full_name for c in abb_account.contacts]
    assert "Hanna Hennig" not in abb_contacts
    assert "Frederik Janssen" not in abb_contacts
    assert "Natalia Oropeza" not in abb_contacts
    assert len(abb_contacts) > 0


def test_13_data_deletion_privacy(db_session):
    # Test deleting a single contact
    test_contact = Contact(
        id="contact-delete-test",
        account_id="siemens-ag",
        full_name="Temporary Evaluation Contact",
        current_title="Testing Role",
        department="Testing",
        buying_role="UNKNOWN",
        reachability_status="UNVERIFIED",
        relevance_score=10.0,
        confidence=0.5,
        verification_status="UNKNOWN",
        last_verified_date="2026-11-03"
    )
    db_session.add(test_contact)
    db_session.commit()

    del_res = client.delete(f"/api/contacts/contact-delete-test")
    assert del_res.status_code == 200
    assert db_session.query(Contact).filter(Contact.id == "contact-delete-test").first() is None


def test_14_api_error_handling():
    res_404 = client.get("/api/accounts/non-existent-company-id")
    assert res_404.status_code == 404
    assert res_404.json()["detail"] == "Account not found"
