from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class EvidenceClaimSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    account_id: str
    source_id: str
    entity_type: str
    entity_id: Optional[str] = None
    claim_text: str
    excerpt: str
    publication_date: Optional[str] = None
    date_retrieved: str
    evidence_type: str
    confidence_score: float
    verification_status: str
    is_conflicting: bool = False
    conflict_details: Optional[str] = None
    is_stale: bool = False
    source_name: Optional[str] = None
    source_url: Optional[str] = None

class SourceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    account_id: str
    name: str
    url: str
    source_type: str
    publication_date: Optional[str] = None
    date_retrieved: str
    author: Optional[str] = None
    is_official: bool = True
    reliability_weight: float = 1.0
    notes: Optional[str] = None

class AccountMetricSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    account_id: str
    source_id: Optional[str] = None
    metric_name: str
    value: str
    unit: Optional[str] = None
    reporting_period: Optional[str] = None
    confidence: float
    verification_status: str
    notes: Optional[str] = None

class TechnologyVendorSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    account_id: str
    source_id: Optional[str] = None
    category: str
    vendor: str
    product_name: Optional[str] = None
    deployment_status: str
    evidence_summary: Optional[str] = None
    source_date: Optional[str] = None
    confidence: float
    verification_status: str

class StrategicPrioritySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    account_id: str
    source_id: Optional[str] = None
    title: str
    category: str
    description: str
    supporting_quote: Optional[str] = None
    zscaler_use_case: Optional[str] = None
    confidence: float
    verification_status: str

class TriggerEventSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    account_id: str
    source_id: Optional[str] = None
    title: str
    event_type: str
    date_occurred: str
    description: str
    business_impact: str
    affected_stakeholders: Optional[str] = None
    zscaler_use_case: str
    confidence: float
    verification_status: str

class ZscalerProductFootprintSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    account_id: str
    source_id: Optional[str] = None
    product_code: str
    product_name: str
    category: str
    status: str
    evidence_summary: str
    expansion_hypothesis: Optional[str] = None
    confidence: float
    verification_status: str

class ContactSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    account_id: str
    source_id: Optional[str] = None
    full_name: str
    current_title: str
    department: str
    business_unit: Optional[str] = None
    geography: Optional[str] = None
    buying_role: str
    influence_level: str
    reachability_status: str
    official_profile_url: Optional[str] = None
    official_bio_url: Optional[str] = None
    public_contact_channel: Optional[str] = None
    areas_of_responsibility: Optional[str] = None
    team_priorities: Optional[str] = None
    stated_priority: Optional[str] = None
    quote_excerpt: Optional[str] = None
    why_matters: Optional[str] = None
    zscaler_value_prop: Optional[str] = None
    relevance_score: float
    relevance_reason: Optional[str] = None
    confidence: float
    verification_status: str
    last_verified_date: str

class RelationshipSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    account_id: str
    from_contact_id: str
    to_contact_id: str
    relationship_type: str
    status: str
    evidence_notes: Optional[str] = None
    from_contact_name: Optional[str] = None
    to_contact_name: Optional[str] = None

class RecommendationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    account_id: str
    recommended_first_contact_id: Optional[str] = None
    recommended_second_contact_id: Optional[str] = None
    first_contact: Optional[ContactSchema] = None
    second_contact: Optional[ContactSchema] = None
    outreach_angle: str
    why_this_account: str
    why_now: str
    why_this_stakeholder: str
    business_problem: str
    relevant_zscaler_capability: str
    suggested_opener_draft: str
    why_second_stakeholder: Optional[str] = None
    risks_and_unknowns: str
    additional_info_needed: str
    supporting_evidence_summary: str

class AccountSummarySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    legal_name: Optional[str] = None
    industry: Optional[str] = None
    headquarters: Optional[str] = None
    is_existing_customer: bool
    customer_type: str
    attractiveness_score: float
    timing_score: float
    evidence_coverage_score: float
    verdict_summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class AccountDetailSchema(AccountSummarySchema):
    ticker: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    global_workforce: Optional[str] = None
    annual_revenue: Optional[str] = None
    geographic_presence: Optional[str] = None
    major_regions: Optional[str] = None
    major_facilities: Optional[str] = None
    business_units: Optional[str] = None
    day_1_justification: Optional[str] = None
    attractiveness_explanation: Optional[str] = None
    timing_explanation: Optional[str] = None
    evidence_coverage_explanation: Optional[str] = None
    
    metrics: List[AccountMetricSchema] = []
    technologies: List[TechnologyVendorSchema] = []
    priorities: List[StrategicPrioritySchema] = []
    triggers: List[TriggerEventSchema] = []
    zscaler_products: List[ZscalerProductFootprintSchema] = []
    contacts: List[ContactSchema] = []
    relationships: List[RelationshipSchema] = []
    recommendation: Optional[RecommendationSchema] = None

class NewResearchRequest(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=100)
    industry: Optional[str] = None
    is_existing_customer: bool = False
    customer_type: Optional[str] = "Prospect"

class ResearchProgressResponse(BaseModel):
    run_id: str
    account_id: str
    company_query: str
    status: str
    current_step: str
    progress_pct: int
    logs: List[str]
    error_message: Optional[str] = None

class DataQualityReportSchema(BaseModel):
    total_claims: int
    verified_claims: int
    corroborated_claims: int
    inferred_claims: int
    unknown_claims: int
    stale_claims: int
    conflicting_claims: int
    total_contacts: int
    contacts_with_verified_titles: int
    contacts_with_public_profiles: int
    contacts_with_verified_reachability: int
    verification_rate: float
    methodology_notes: str
