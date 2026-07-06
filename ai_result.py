from dataclasses import dataclass, field
from typing import Any


@dataclass
class AIExtractionResult:
    target_entity: str
    target_field: str
    value: Any
    confidence_score: float
    explanation: str | None = None


@dataclass
class AIDocumentUnderstandingResult:
    document_type: str = "unknown"
    confidence_score: float = 0.0
    summary: str = ""
    extracted_log_fields: dict[str, Any] = field(default_factory=dict)
    people: list[dict] = field(default_factory=list)
    companies: list[dict] = field(default_factory=list)
    products: list[dict] = field(default_factory=list)
    requests: list[dict] = field(default_factory=list)
    requested_documents: list[str] = field(default_factory=list)
    missing_fields: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    raw_text_preview: str = ""

    def to_dict(self) -> dict:
        return {
            "document_type": self.document_type,
            "confidence_score": self.confidence_score,
            "summary": self.summary,
            "extracted_log_fields": self.extracted_log_fields,
            "people": self.people,
            "companies": self.companies,
            "products": self.products,
            "requests": self.requests,
            "requested_documents": self.requested_documents,
            "missing_fields": self.missing_fields,
            "warnings": self.warnings,
            "raw_text_preview": self.raw_text_preview,
        }
