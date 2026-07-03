import re

from sqlalchemy.orm import Session

from app.engines.ai.ai_result import AIExtractionResult
from app.engines.ai.base_ai_engine import BaseAIEngine
from app.models.learning import ExtractionLearningExample


class RuleBasedAIEngine(BaseAIEngine):
    def __init__(self, db: Session | None = None):
        self.db = db

    def extract_fields(
    self,
    text: str,
    extraction_fields: list,
    instructions: str | None = None
) -> list[AIExtractionResult]:
    results = []

    enriched_text = text

    if instructions:
        enriched_text = f"{instructions}\n\n{text}"

    for field in extraction_fields:
        learned_value = self._extract_from_learning(
            text=enriched_text,
            target_entity=field.target_entity,
            target_field=field.target_field,
            document_type_id=field.document_type_id
        )

        if learned_value:
            results.append(
                AIExtractionResult(
                    target_entity=field.target_entity,
                    target_field=field.target_field,
                    value=learned_value,
                    confidence_score=0.75,
                    explanation="Valor sugerido usando ejemplos aprendidos."
                )
            )
            continue

        value = self._extract_by_field_name(
            text=enriched_text,
            source_name=field.source_name,
            instructions=field.instructions
        )

        if value:
            results.append(
                AIExtractionResult(
                    target_entity=field.target_entity,
                    target_field=field.target_field,
                    value=value,
                    confidence_score=0.60 if instructions else 0.55,
                    explanation=f"Valor detectado usando reglas e instrucciones para {field.source_name}"
                )
            )

    return results

    def summarize(self, text: str) -> str:
        clean_text = " ".join(text.split())

        if len(clean_text) <= 800:
            return clean_text

        return clean_text[:800] + "..."

    def classify_document(
        self,
        text: str,
        document_types: list
    ) -> dict:
        text_lower = text.lower()

        best_match = None
        best_score = 0

        for document_type in document_types:
            score = 0
            name = (document_type.name or "").lower()
            code = (document_type.code or "").lower()

            if name and name in text_lower:
                score += 0.5

            if code and code in text_lower:
                score += 0.5

            if score > best_score:
                best_score = score
                best_match = document_type

        return {
            "document_type_id": best_match.id if best_match else None,
            "confidence_score": best_score,
            "reason": "Clasificación inicial basada en coincidencia de nombre/código"
        }

    def _extract_from_learning(
        self,
        text: str,
        target_entity: str,
        target_field: str,
        document_type_id: int | None = None
    ) -> str | None:
        if not self.db:
            return None

        query = (
            self.db.query(ExtractionLearningExample)
            .filter(
                ExtractionLearningExample.target_entity == target_entity,
                ExtractionLearningExample.target_field == target_field
            )
        )

        if document_type_id:
            query = query.filter(
                ExtractionLearningExample.document_type_id == document_type_id
            )

        examples = query.order_by(
            ExtractionLearningExample.created_at.desc()
        ).limit(25).all()

        text_lower = text.lower()

        for example in examples:
            original = (example.original_value or "").strip()
            corrected = (example.corrected_value or "").strip()

            if not original or not corrected:
                continue

            if original.lower() in text_lower:
                return corrected

        return None

    def _extract_by_field_name(
        self,
        text: str,
        source_name: str,
        instructions: str | None = None
    ) -> str | None:
        source = source_name.lower()
        lines = text.splitlines()

        for line in lines:
            clean = line.strip()
            lower = clean.lower()

            if source in lower:
                if ":" in clean:
                    return clean.split(":", 1)[1].strip()

                return clean

        if "fecha" in source:
            return self._extract_date(text)

        if (
            "identificacion" in source
            or "identificación" in source
            or "cedula" in source
            or "cédula" in source
        ):
            return self._extract_identification(text)

        if "numero" in source or "número" in source or "requerimiento" in source:
            return self._extract_request_number(text)

        return None

    def _extract_date(self, text: str) -> str | None:
        patterns = [
            r"\b\d{2}/\d{2}/\d{4}\b",
            r"\b\d{4}-\d{2}-\d{2}\b",
            r"\b\d{2}-\d{2}-\d{4}\b",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)

        return None

    def _extract_identification(self, text: str) -> str | None:
        patterns = [
            r"\b\d{3}-\d{7}-\d\b",
            r"\b\d{11}\b",
            r"\b\d{9}\b",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)

        return None

    def _extract_request_number(self, text: str) -> str | None:
        patterns = [
            r"(oficio|requerimiento|comunicación|comunicacion)\s*(no\.?|número|numero)?\s*[:#-]?\s*([A-Za-z0-9\-\/]+)",
            r"\b[A-Z]{2,5}-\d{4}-\d+\b",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(len(match.groups()))

        return None
