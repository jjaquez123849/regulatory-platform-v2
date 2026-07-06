import re

from sqlalchemy.orm import Session

from app.engines.ai.ai_result import (
    AIExtractionResult,
    AIDocumentUnderstandingResult,
)
from app.engines.ai.base_ai_engine import BaseAIEngine
from app.models.learning import ExtractionLearningExample


class RuleBasedAIEngine(BaseAIEngine):
    def __init__(self, db: Session | None = None):
        self.db = db

    def extract_fields(
        self,
        text: str,
        extraction_fields: list,
        instructions: str | None = None,
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
                document_type_id=field.document_type_id,
            )

            if learned_value:
                results.append(
                    AIExtractionResult(
                        target_entity=field.target_entity,
                        target_field=field.target_field,
                        value=learned_value,
                        confidence_score=0.75,
                        explanation="Valor sugerido usando ejemplos aprendidos.",
                    )
                )
                continue

            value = self._extract_by_field_name(
                text=enriched_text,
                source_name=field.source_name,
                instructions=field.instructions,
            )

            if value:
                results.append(
                    AIExtractionResult(
                        target_entity=field.target_entity,
                        target_field=field.target_field,
                        value=value,
                        confidence_score=0.60 if instructions else 0.55,
                        explanation=f"Valor detectado usando reglas para {field.source_name}",
                    )
                )

        return results

    def summarize(self, text: str) -> str:
        clean_text = " ".join((text or "").split())

        if len(clean_text) <= 800:
            return clean_text

        return clean_text[:800] + "..."

    def classify_document(self, text: str, document_types: list) -> dict:
        text_lower = (text or "").lower()

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
            "reason": "Clasificación basada en coincidencia de nombre/código.",
        }

    def understand_regulatory_request(
        self,
        text: str,
    ) -> AIDocumentUnderstandingResult:
        clean_text = self._normalize_text(text)

        result = AIDocumentUnderstandingResult(
            document_type=self._detect_document_type(clean_text),
            confidence_score=0.60,
            summary=self.summarize(clean_text),
            raw_text_preview=clean_text[:1500],
        )

        extracted = {}

        request_number = self._extract_request_number(clean_text)
        if request_number:
            extracted["numero_requerimiento"] = request_number

        regulator = self._extract_regulator(clean_text)
        if regulator:
            extracted["regulador"] = regulator

        due_date = self._extract_due_date(clean_text)
        if due_date:
            extracted["fecha_limite"] = due_date

        requests = self._extract_requests(clean_text)
        result.requests = requests
        result.requested_documents = [item["description"] for item in requests]
        extracted["solicitudes"] = result.requested_documents

        result.extracted_log_fields = extracted

        required_fields = [
            "numero_requerimiento",
            "regulador",
            "fecha_limite",
        ]

        for field in required_fields:
            if field not in extracted or not extracted[field]:
                result.missing_fields.append(field)

        if result.document_type == "unknown":
            result.warnings.append("No se pudo clasificar el documento con reglas.")

        if result.missing_fields:
            result.warnings.append("Hay campos obligatorios pendientes.")

        return result

    def compare_request_vs_response(
        self,
        request_text: str,
        response_text: str,
    ) -> dict:
        request_analysis = self.understand_regulatory_request(request_text)

        response_lower = self._normalize_text(response_text).lower()

        matched = []
        missing = []

        for item in request_analysis.requested_documents:
            if item.lower() in response_lower:
                matched.append(item)
            else:
                missing.append(item)

        return {
            "matched_requirements": matched,
            "missing_requirements": missing,
            "is_complete": len(missing) == 0,
            "summary": (
                "Respuesta completa según reglas básicas."
                if len(missing) == 0
                else "La respuesta parece incompleta según reglas básicas."
            ),
        }

    def _normalize_text(self, text: str) -> str:
        return re.sub(r"\s+", " ", text or "").strip()

    def _detect_document_type(self, text: str) -> str:
        lowered = text.lower()

        if "superintendencia de bancos" in lowered or "sib" in lowered:
            return "requerimiento_sib"

        if "dirección general de impuestos internos" in lowered or "dgii" in lowered:
            return "requerimiento_dgii"

        if "unidad de análisis financiero" in lowered or "uaf" in lowered:
            return "requerimiento_uaf"

        if "banco central" in lowered or "bcrd" in lowered:
            return "requerimiento_bcrd"

        if "solicita" in lowered or "requerimos" in lowered:
            return "requerimiento_generico"

        return "unknown"

    def _extract_from_learning(
        self,
        text: str,
        target_entity: str,
        target_field: str,
        document_type_id: int | None = None,
    ) -> str | None:
        if not self.db:
            return None

        query = self.db.query(ExtractionLearningExample).filter(
            ExtractionLearningExample.target_entity == target_entity,
            ExtractionLearningExample.target_field == target_field,
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
        instructions: str | None = None,
    ) -> str | None:
        source = (source_name or "").lower()
        lines = text.splitlines()

        for line in lines:
            clean = line.strip()
            lower = clean.lower()

            if source and source in lower:
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

    def _extract_due_date(self, text: str) -> str | None:
        patterns = [
            r"(?:antes del|a más tardar el|fecha límite|plazo)\s+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",
            r"(\d{1,2}\s+de\s+[a-záéíóúñ]+\s+de\s+\d{4})",
            r"\b\d{4}-\d{2}-\d{2}\b",
            r"\b\d{2}/\d{2}/\d{4}\b",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1) if match.groups() else match.group(0)

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
            r"\b[A-Z]{2,5}-\d{4}-\d+\b",
            r"(?:oficio|requerimiento|comunicación|comunicacion)\s*(?:no\.?|número|numero)?\s*[:#-]?\s*([A-Za-z0-9\-\/]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1) if match.groups() else match.group(0)

        return None

    def _extract_regulator(self, text: str) -> str | None:
        lowered = text.lower()

        candidates = [
            ("Superintendencia de Bancos", ["superintendencia de bancos", "sib"]),
            (
                "Dirección General de Impuestos Internos",
                ["dirección general de impuestos internos", "dgii"],
            ),
            ("Unidad de Análisis Financiero", ["unidad de análisis financiero", "uaf"]),
            ("Banco Central", ["banco central", "bcrd"]),
        ]

        for name, aliases in candidates:
            if any(alias in lowered for alias in aliases):
                return name

        return None

    def _extract_requests(self, text: str) -> list[dict]:
        lowered = text.lower()

        keywords = [
            "estado de cuenta",
            "contrato",
            "beneficiario",
            "formulario",
            "certificación",
            "documentación",
            "movimientos",
            "productos activos",
            "expediente",
        ]

        results = []

        for keyword in keywords:
            if keyword in lowered:
                results.append(
                    {
                        "description": keyword,
                        "confidence": 0.55,
                        "source": "keyword",
                        "needs_review": True,
                    }
                )

        return results
