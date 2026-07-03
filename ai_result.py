from dataclasses import dataclass
from typing import Any


@dataclass
class AIExtractionResult:
    target_entity: str
    target_field: str
    value: Any
    confidence_score: float
    explanation: str | None = None
