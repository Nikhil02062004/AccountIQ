import datetime
import uuid
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, Text, DateTime, ForeignKey, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from backend.app.db import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    legal_name = Column(String, nullable=True)
    ticker = Column(String, nullable=True)
    website = Column(String, nullable=True)
    headquarters = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    
    # Customer classification
    is_existing_customer = Column(Boolean, default=True)
    customer_type = Column(String, default="Existing Customer / Expansion Opportunity")
    
    # Global Footprint
    global_workforce = Column(String, nullable=True)
    annual_revenue = Column(String, nullable=True)
    geographic_presence = Column(Text, nullable=True)
    major_regions = Column(Text, nullable=True) # JSON or comma-separated
    major_facilities = Column(Text, nullable=True)
    business_units = Column(Text, nullable=True)
    
    # Day 1 response & verdicts
    day_1_justification = Column(Text, nullable=True)
    verdict_summary = Column(Text, nullable=True)
    
    # Scores (0-100)
    attractiveness_score = Column(Float, default=0.0)
    attractiveness_explanation = Column(Text, nullable=True)
    timing_score = Column(Float, default=0.0)
    timing_explanation = Column(Text, nullable=True)
    evidence_coverage_score = Column(Float, default=0.0)
    evidence_coverage_explanation = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    metrics = relationship("AccountMetric", back_populates="account", cascade="all, delete-orphan")
    technologies = relationship("TechnologyVendor", back_populates="account", cascade="all, delete-orphan")
    priorities = relationship("StrategicPriority", back_populates="account", cascade="all, delete-orphan")
    triggers = relationship("TriggerEvent", back_populates="account", cascade="all, delete-orphan")
    zscaler_products = relationship("ZscalerProductFootprint", back_populates="account", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="account", cascade="all, delete-orphan")
    sources = relationship("Source", back_populates="account", cascade="all, delete-orphan")
    claims = relationship("EvidenceClaim", back_populates="account", cascade="all, delete-orphan")
    relationships = relationship("Relationship", back_populates="account", cascade="all, delete-orphan")
    recommendation = relationship("Recommendation", back_populates="account", uselist=False, cascade="all, delete-orphan")
    research_runs = relationship("ResearchRun", back_populates="account", cascade="all, delete-orphan")


class Source(Base):
    __tablename__ = "sources"

    id = Column(String, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    source_type = Column(String, nullable=False) # OFFICIAL_WEBSITE, ANNUAL_REPORT, PRESS_RELEASE, CUSTOMER_STORY, etc.
    publication_date = Column(String, nullable=True)
    date_retrieved = Column(String, nullable=False)
    author = Column(String, nullable=True)
    is_official = Column(Boolean, default=True)
    reliability_weight = Column(Float, default=1.0)
    notes = Column(Text, nullable=True)

    account = relationship("Account", back_populates="sources")
    claims = relationship("EvidenceClaim", back_populates="source", cascade="all, delete-orphan")


class EvidenceClaim(Base):
    __tablename__ = "evidence_claims"

    id = Column(String, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    source_id = Column(String, ForeignKey("sources.id", ondelete="CASCADE"), nullable=False)
    
    entity_type = Column(String, nullable=False) # METRIC, TECH, PRIORITY, TRIGGER, PRODUCT, CONTACT, RELATIONSHIP
    entity_id = Column(String, nullable=True)
    
    claim_text = Column(Text, nullable=False)
    excerpt = Column(Text, nullable=False)
    publication_date = Column(String, nullable=True)
    date_retrieved = Column(String, nullable=False)
    evidence_type = Column(String, default="PRIMARY_DISCLOSURE")
    
    confidence_score = Column(Float, default=0.9) # 0.0 - 1.0
    verification_status = Column(String, default="VERIFIED") # VERIFIED, CORROBORATED, INFERRED, UNKNOWN, STALE
    
    is_conflicting = Column(Boolean, default=False)
    conflict_details = Column(Text, nullable=True)
    is_stale = Column(Boolean, default=False)

    account = relationship("Account", back_populates="claims")
    source = relationship("Source", back_populates="claims")


class AccountMetric(Base):
    __tablename__ = "account_metrics"

    id = Column(String, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    source_id = Column(String, ForeignKey("sources.id"), nullable=True)
    
    metric_name = Column(String, nullable=False) # e.g. "Total Workforce", "FY24 Revenue"
    value = Column(String, nullable=False)
    unit = Column(String, nullable=True)
    reporting_period = Column(String, nullable=True) # "FY2024 (Ending Sept 30, 2024)"
    
    confidence = Column(Float, default=1.0)
    verification_status = Column(String, default="VERIFIED")
    notes = Column(Text, nullable=True)

    account = relationship("Account", back_populates="metrics")


class TechnologyVendor(Base):
    __tablename__ = "technology_vendors"

    id = Column(String, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    source_id = Column(String, ForeignKey("sources.id"), nullable=True)

    category = Column(String, nullable=False) # SD-WAN, Secure Web Gateway, Private Access, Cloud, Identity, Endpoint, OT
    vendor = Column(String, nullable=False)
    product_name = Column(String, nullable=True)
    
    deployment_status = Column(String, default="CONFIRMED_CURRENT")
    # CONFIRMED_CURRENT, HISTORICAL, HIRING_SIGNAL, PARTNERSHIP, INFERENCE, UNKNOWN
    
    evidence_summary = Column(Text, nullable=True)
    source_date = Column(String, nullable=True)
    confidence = Column(Float, default=0.9)
    verification_status = Column(String, default="VERIFIED")

    account = relationship("Account", back_populates="technologies")


class StrategicPriority(Base):
    __tablename__ = "strategic_priorities"

    id = Column(String, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    source_id = Column(String, ForeignKey("sources.id"), nullable=True)

    title = Column(String, nullable=False)
    category = Column(String, nullable=False) # Cloud, AI, OT, M&A, Cost Optimization, Cyber Resilience
    description = Column(Text, nullable=False)
    supporting_quote = Column(Text, nullable=True)
    
    zscaler_use_case = Column(Text, nullable=True)
    confidence = Column(Float, default=0.95)
    verification_status = Column(String, default="VERIFIED")

    account = relationship("Account", back_populates="priorities")


class TriggerEvent(Base):
    __tablename__ = "trigger_events"

    id = Column(String, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    source_id = Column(String, ForeignKey("sources.id"), nullable=True)

    title = Column(String, nullable=False)
    event_type = Column(String, nullable=False) # M&A, Leadership, Product Launch, Regulatory, Partnership
    date_occurred = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    business_impact = Column(Text, nullable=False)
    affected_stakeholders = Column(Text, nullable=True)
    
    zscaler_use_case = Column(Text, nullable=False)
    confidence = Column(Float, default=0.95)
    verification_status = Column(String, default="VERIFIED")

    account = relationship("Account", back_populates="triggers")


class ZscalerProductFootprint(Base):
    __tablename__ = "zscaler_product_footprints"

    id = Column(String, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    source_id = Column(String, ForeignKey("sources.id"), nullable=True)

    product_code = Column(String, nullable=False) # ZIA, ZPA, ZDX, DATA_PROTECTION, WORKLOAD_SECURITY, AI_SECURITY, ZERO_TRUST_OT
    product_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    
    status = Column(String, default="CONFIRMED_DEPLOYED")
    # CONFIRMED_DEPLOYED, HISTORICAL, PARTNERSHIP, EXPANSION_OPPORTUNITY, UNKNOWN
    
    evidence_summary = Column(Text, nullable=False)
    expansion_hypothesis = Column(Text, nullable=True)
    confidence = Column(Float, default=0.9)
    verification_status = Column(String, default="VERIFIED")

    account = relationship("Account", back_populates="zscaler_products")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(String, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    source_id = Column(String, ForeignKey("sources.id"), nullable=True)

    full_name = Column(String, nullable=False, index=True)
    current_title = Column(String, nullable=False)
    department = Column(String, nullable=False) # IT Leadership, Cybersecurity, Procurement, Executive Board, Business Unit
    business_unit = Column(String, nullable=True)
    geography = Column(String, nullable=True)
    
    # Buying role hypothesis
    buying_role = Column(String, default="INFLUENCER")
    # ECONOMIC_BUYER, TECHNICAL_DECISION_MAKER, CHAMPION, INFLUENCER, BLOCKER, PROCUREMENT_APPROVER, UNKNOWN
    influence_level = Column(String, default="HIGH") # HIGH, MEDIUM, LOW
    
    # Reachability & Privacy
    reachability_status = Column(String, default="PUBLIC_PROFILE_ONLY")
    # VERIFIED_PUBLIC_CHANNEL, PUBLIC_PROFILE_ONLY, UNVERIFIED, UNKNOWN
    official_profile_url = Column(String, nullable=True)
    official_bio_url = Column(String, nullable=True)
    public_contact_channel = Column(String, nullable=True)
    
    # What this person cares about
    areas_of_responsibility = Column(Text, nullable=True)
    team_priorities = Column(Text, nullable=True)
    stated_priority = Column(Text, nullable=True)
    quote_excerpt = Column(Text, nullable=True)
    why_matters = Column(Text, nullable=True)
    zscaler_value_prop = Column(Text, nullable=True)
    
    # Scoring & Validation
    relevance_score = Column(Float, default=80.0)
    relevance_reason = Column(Text, nullable=True)
    confidence = Column(Float, default=0.95)
    verification_status = Column(String, default="VERIFIED")
    last_verified_date = Column(String, nullable=False)

    account = relationship("Account", back_populates="contacts")
    outgoing_relationships = relationship("Relationship", foreign_keys="Relationship.from_contact_id", back_populates="from_contact", cascade="all, delete-orphan")
    incoming_relationships = relationship("Relationship", foreign_keys="Relationship.to_contact_id", back_populates="to_contact", cascade="all, delete-orphan")


class Relationship(Base):
    __tablename__ = "relationships"

    id = Column(String, primary_key=True, index=True, default=lambda: str(datetime.datetime.utcnow().timestamp()))
    account_id = Column(String, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    from_contact_id = Column(String, ForeignKey("contacts.id", ondelete="CASCADE"), nullable=False)
    to_contact_id = Column(String, ForeignKey("contacts.id", ondelete="CASCADE"), nullable=False)
    
    relationship_type = Column(String, default="REPORTS_TO")
    # REPORTS_TO, INFLUENCES, COLLABORATES_WITH, COUNCILS_WITH
    
    status = Column(String, default="VERIFIED") # VERIFIED, INFERRED_HYPOTHESIS, UNKNOWN
    evidence_notes = Column(Text, nullable=True)
    source_id = Column(String, ForeignKey("sources.id"), nullable=True)

    account = relationship("Account", back_populates="relationships")
    from_contact = relationship("Contact", foreign_keys=[from_contact_id], back_populates="outgoing_relationships")
    to_contact = relationship("Contact", foreign_keys=[to_contact_id], back_populates="incoming_relationships")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    account_id = Column(String, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    recommended_first_contact_id = Column(String, ForeignKey("contacts.id"), nullable=True)
    recommended_second_contact_id = Column(String, ForeignKey("contacts.id"), nullable=True)
    
    outreach_angle = Column(String, nullable=False)
    why_this_account = Column(Text, nullable=False)
    why_now = Column(Text, nullable=False)
    why_this_stakeholder = Column(Text, nullable=False)
    business_problem = Column(Text, nullable=False)
    relevant_zscaler_capability = Column(Text, nullable=False)
    
    suggested_opener_draft = Column(Text, nullable=False)
    why_second_stakeholder = Column(Text, nullable=True)
    
    risks_and_unknowns = Column(Text, nullable=False)
    additional_info_needed = Column(Text, nullable=False)
    supporting_evidence_summary = Column(Text, nullable=False)
    
    account = relationship("Account", back_populates="recommendation")
    first_contact = relationship("Contact", foreign_keys=[recommended_first_contact_id])
    second_contact = relationship("Contact", foreign_keys=[recommended_second_contact_id])


class ResearchRun(Base):
    __tablename__ = "research_runs"

    id = Column(String, primary_key=True, index=True)
    account_id = Column(String, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    company_query = Column(String, nullable=False)
    
    status = Column(String, default="PENDING") # PENDING, RUNNING, COMPLETED, FAILED
    current_step = Column(String, default="INITIALIZING")
    progress_pct = Column(Integer, default=0)
    
    logs_json = Column(Text, default="[]")
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    account = relationship("Account", back_populates="research_runs")
