# pipeline/contracts.py
from enum import Enum
from typing import List, Dict, Any
from pydantic import BaseModel, Field, model_validator

class RiskLevel(str, Enum):
    """Defines the explicit risk tiers for ScamShield AI evaluation handles."""
    SAFE = "SAFE"
    SUSPICIOUS = "SUSPICIOUS"
    SCAM = "SCAM"

class DocumentChunk(BaseModel):
    """
    Data contract representing a structurally parsed regulatory document chunk.
    """
    chunk_id: str = Field(
        ..., 
        description="Unique deterministic MD5 or SHA-256 hash of the chunk content"
    )
    document_id: str = Field(
        ..., 
        description="Unique identifier of the source regulatory PDF/Word asset"
    )
    content: str = Field(
        ..., 
        description="Clean markdown text or structural table block extracted from the document"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Metadata mapping including page numbers, issuing authority, and tenant boundaries"
    )

class EvidenceMatch(BaseModel):
    """
    Granular citation component tracking exactly where information 
    was extracted to combat hallucination.
    """
    source_document: str = Field(
        ..., 
        description="Name of the official regulatory policy or advisory document matched"
    )
    clause_reference: str = Field(
        ..., 
        description="Exact clause, circular reference index, section number, or markdown header"
    )
    matched_text_context: str = Field(
        ..., 
        description="The relevant raw text snippet or tabular matrix used to verify the claim"
    )
    relevance_rationale: str = Field(
        ..., 
        description="Defensible structural explanation linking this regulatory chunk to the verdict"
    )

class VerdictResponse(BaseModel):
    """
    The complete, validated payload returned to the presentation layer 
    following a ScamShield AI risk analysis execution.
    """
    input_text_summary: str = Field(
        ..., 
        description="Concise, objective summary of the user input text being evaluated"
    )
    verdict: RiskLevel = Field(
        ..., 
        description="The definitive risk classification outcome"
    )
    risk_score: float = Field(
        ..., 
        ge=0.0, 
        le=1.0, 
        description="Calculated risk metric normalized strictly between 0.0 (Safe) and 1.0 (Confirmed Scam)"
    )
    reasoning_breakdown: List[str] = Field(
        ..., 
        description="Step-by-step logical verification points justifying the final verdict"
    )
    regulatory_citations: List[EvidenceMatch] = Field(
        ..., 
        description="Verifiable evidence array mapping the reasoning directly back to official documents"
    )
    recommended_actions: List[str] = Field(
        ..., 
        description="Actionable, clear mitigation steps advised for the end consumer"
    )

    @model_validator(mode="after")
    def verify_citations_present_if_unsafe(self) -> "VerdictResponse":
        """
        Enforces cross-field security validation. If a document is flagged 
        as unsafe, matching regulatory citations must be physically present.
        """
        if self.verdict in [RiskLevel.SCAM, RiskLevel.SUSPICIOUS] and not self.regulatory_citations:
            raise ValueError(
                f"Data Contract Violation: Regulatory citations are strictly required "
                f"when providing a status verdict of '{self.verdict.value}'."
            )
        return self