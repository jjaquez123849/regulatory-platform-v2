from dataclasses import dataclass, field
from typing import Any


@dataclass
class DocumentEntity:
    entity_type: str
    value: str
    confidence: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentRequest:
    request_number: str | None = None
    description: str = ""
    priority: str | None = None
    due_date: str | None = None
    related_entities: list[DocumentEntity] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentUnderstanding:

    document_type: str | None = None

    issuer: str | None = None

    regulator: str | None = None

    subject: str | None = None

    summary: str | None = None

    request_number: str | None = None

    request_date: str | None = None

    due_date: str | None = None

    entities: list[DocumentEntity] = field(default_factory=list)

    requests: list[DocumentRequest] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)
