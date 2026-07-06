from dataclasses import dataclass, field
from typing import Any


@dataclass
class IntakeFinding:
    field_name: str
    value: Any
    confidence: float = 0.0
    source: str | None = None
    needs_review: bool = False


@dataclass
class IntakeResult:
    document_type: str = "unknown"
    document_confidence: float = 0.0

    findings: list[IntakeFinding] = field(default_factory=list)

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
            "document_confidence": self.document_confidence,
            "findings": [
                {
                    "field_name": item.field_name,
                    "value": item.value,
                    "confidence": item.confidence,
                    "source": item.source,
                    "needs_review": item.needs_review,
                }
                for item in self.findings
            ],
            "people": self.people,
            "companies": self.companies,
            "products": self.products,
            "requests": self.requests,
            "requested_documents": self.requested_documents,
            "missing_fields": self.missing_fields,
            "warnings": self.warnings,
            "raw_text_preview": self.raw_text_preview,
        }
