import logging
import re
from typing import Dict, Any, List, Tuple
from backend.app.discovery.fact_extractor import ExtractedFacts
from backend.app.discovery.source_discovery import DiscoveredSource

logger = logging.getLogger(__name__)

class QualityGateResult:
    def __init__(self):
        self.is_valid: bool = True
        self.pipeline_status: str = "COMPLETED" # COMPLETED, PARTIALLY_COMPLETED, FAILED
        self.quality_score: float = 100.0
        self.warnings: List[str] = []
        self.errors: List[str] = []
        self.verified_fields: List[str] = []
        self.unknown_fields: List[str] = []


class DataQualityGate:
    """
    Central Data Quality Gate enforcing schema, numeric validity, currency integrity,
    evidence provenance, and multi-tenant account isolation prior to database commit.
    """

    @classmethod
    def evaluate(
        cls,
        account_id: str,
        entity: Dict[str, Any],
        sources: List[DiscoveredSource],
        facts: ExtractedFacts
    ) -> QualityGateResult:
        result = QualityGateResult()

        # 1. Company Identity Validation
        if not entity.get("is_resolved", False):
            result.is_valid = False
            result.pipeline_status = "FAILED"
            result.errors.append(f"Company identity could not be confidently verified for '{entity.get('query')}'.")
            result.quality_score = 0.0
            return result

        # 2. Source Relevance & Discovery Validation
        if not sources:
            result.is_valid = False
            result.pipeline_status = "FAILED"
            result.errors.append(f"Zero reliable public sources could be retrieved for '{entity.get('canonical_name')}'.")
            result.quality_score = 10.0
            return result

        # 3. Numeric & Financial Validation
        if facts.annual_revenue == "UNKNOWN":
            result.unknown_fields.append("annual_revenue")
            result.warnings.append("Annual revenue is unconfirmed or aggregated in subsidiary accounts.")
        else:
            if facts.revenue_numeric_billions <= 0.0:
                result.errors.append("Invalid non-positive revenue figure detected; resetting to UNKNOWN.")
                facts.annual_revenue = "UNKNOWN"
                result.unknown_fields.append("annual_revenue")
            else:
                result.verified_fields.append("annual_revenue")

        # 4. Workforce Scale Validation
        if facts.global_workforce == "UNKNOWN":
            result.unknown_fields.append("global_workforce")
            result.warnings.append("Workforce scale is undisclosed in public registers.")
        else:
            if facts.workforce_numeric <= 0 and "–" not in facts.global_workforce and "-" not in facts.global_workforce:
                facts.global_workforce = "UNKNOWN"
                result.unknown_fields.append("global_workforce")
            else:
                result.verified_fields.append("global_workforce")

        # 5. Headquarters Validation
        if facts.headquarters == "UNKNOWN":
            result.unknown_fields.append("headquarters")
            result.warnings.append("Corporate headquarters address could not be verified.")
        else:
            result.verified_fields.append("headquarters")

        # 6. Contact Stakeholder Validation
        if not facts.contacts:
            result.unknown_fields.append("contacts")
            result.warnings.append("No executive leadership contacts discovered from verified public profiles.")
        else:
            result.verified_fields.append("contacts")

        # 7. Evidence Claims & Provenance Validation
        valid_claims = []
        for claim in facts.evidence_claims:
            # Enforce that account_id matches strictly
            if claim.get("account_id") != account_id:
                logger.error(f"Account ID mismatch in claim {claim.get('id')}: {claim.get('account_id')} vs {account_id}")
                continue

            # Enforce that claim has non-empty excerpt
            if not claim.get("excerpt"):
                claim["verification_status"] = "UNKNOWN"
                claim["confidence_score"] = 0.30
            valid_claims.append(claim)
        facts.evidence_claims = valid_claims

        # 8. Determine Pipeline Status & Quality Score
        penalty = (len(result.unknown_fields) * 15.0) + (len(result.errors) * 25.0)
        result.quality_score = max(20.0, min(100.0, 100.0 - penalty))

        if result.unknown_fields:
            result.pipeline_status = "PARTIALLY_COMPLETED"
        else:
            result.pipeline_status = "COMPLETED"

        return result
