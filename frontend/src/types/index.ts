export interface AccountSummary {
  id: string;
  name: string;
  legal_name?: string;
  industry?: string;
  headquarters?: string;
  is_existing_customer: boolean;
  customer_type: string;
  attractiveness_score: number;
  timing_score: number;
  evidence_coverage_score: number;
  verdict_summary?: string;
  created_at: string;
  updated_at: string;
}

export interface AccountMetric {
  id: string;
  metric_name: string;
  value: string;
  unit?: string;
  reporting_period?: string;
  confidence: number;
  verification_status: string;
  notes?: string;
}

export interface TechnologyVendor {
  id: string;
  category: string;
  vendor: string;
  product_name?: string;
  deployment_status: string;
  evidence_summary?: string;
  source_date?: string;
  confidence: number;
  verification_status: string;
}

export interface StrategicPriority {
  id: string;
  title: string;
  category: string;
  description: string;
  supporting_quote?: string;
  zscaler_use_case?: string;
  confidence: number;
  verification_status: string;
}

export interface TriggerEvent {
  id: string;
  title: string;
  event_type: string;
  date_occurred: string;
  description: string;
  business_impact: string;
  affected_stakeholders?: string;
  zscaler_use_case: string;
  confidence: number;
  verification_status: string;
}

export interface ZscalerProductFootprint {
  id: string;
  product_code: string;
  product_name: string;
  category: string;
  status: string;
  evidence_summary: string;
  expansion_hypothesis?: string;
  confidence: number;
  verification_status: string;
}

export interface Contact {
  id: string;
  full_name: string;
  current_title: string;
  department: string;
  business_unit?: string;
  geography?: string;
  buying_role: string;
  influence_level: string;
  reachability_status: string;
  official_profile_url?: string;
  official_bio_url?: string;
  public_contact_channel?: string;
  areas_of_responsibility?: string;
  team_priorities?: string;
  stated_priority?: string;
  quote_excerpt?: string;
  why_matters?: string;
  zscaler_value_prop?: string;
  relevance_score: number;
  relevance_reason?: string;
  confidence: number;
  verification_status: string;
  last_verified_date: string;
}

export interface Recommendation {
  id: string;
  account_id: string;
  recommended_first_contact_id?: string;
  recommended_second_contact_id?: string;
  first_contact?: Contact;
  second_contact?: Contact;
  outreach_angle: string;
  why_this_account: string;
  why_now: string;
  why_this_stakeholder: string;
  business_problem: string;
  relevant_zscaler_capability: string;
  suggested_opener_draft: string;
  why_second_stakeholder?: string;
  risks_and_unknowns: string;
  additional_info_needed: string;
  supporting_evidence_summary: string;
}

export interface AccountDetail extends AccountSummary {
  ticker?: string;
  website?: string;
  description?: string;
  global_workforce?: string;
  annual_revenue?: string;
  geographic_presence?: string;
  major_regions?: string;
  major_facilities?: string;
  business_units?: string;
  day_1_justification?: string;
  attractiveness_explanation?: string;
  timing_explanation?: string;
  evidence_coverage_explanation?: string;
  metrics: AccountMetric[];
  technologies: TechnologyVendor[];
  priorities: StrategicPriority[];
  triggers: TriggerEvent[];
  zscaler_products: ZscalerProductFootprint[];
  contacts: Contact[];
  recommendation?: Recommendation;
}

export interface Source {
  id: string;
  name: string;
  url: string;
  source_type: string;
  publication_date?: string;
  date_retrieved: string;
  author?: string;
  is_official: boolean;
  reliability_weight: number;
  notes?: string;
}

export interface EvidenceClaim {
  id: string;
  source_id: string;
  source_name: string;
  source_url: string;
  source_type: string;
  entity_type: string;
  entity_id?: string;
  claim_text: string;
  excerpt: string;
  publication_date?: string;
  date_retrieved: string;
  evidence_type: string;
  confidence_score: number;
  verification_status: string;
  is_conflicting: boolean;
  conflict_details?: string;
  is_stale: boolean;
}

export interface EvidenceExplorerData {
  sources: Source[];
  claims: EvidenceClaim[];
  total_sources: number;
  total_claims: number;
}

export interface QualityReport {
  total_claims: number;
  verified_claims: number;
  corroborated_claims: number;
  inferred_claims: number;
  unknown_claims: number;
  stale_claims: number;
  conflicting_claims: number;
  total_contacts: number;
  contacts_with_verified_titles: number;
  contacts_with_public_profiles: number;
  contacts_with_verified_reachability: number;
  verification_rate: number;
  methodology_notes: string;
}

export interface ResearchProgress {
  run_id: string;
  account_id: string;
  company_query: string;
  status: string;
  current_step: string;
  progress_pct: number;
  logs: string[];
  error_message?: string;
}
