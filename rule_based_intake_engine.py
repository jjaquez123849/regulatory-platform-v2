import re

from app.engines.intake_ai.contracts.base_intake_engine import BaseIntakeAIEngine
from app.engines.intake_ai.contracts.intake_result import (
    IntakeFinding,
    IntakeResult,
)


class RuleBasedIntakeEngine(BaseIntakeAIEngine):
    def analyze_text(self, text: str) -> IntakeResult:
        normalized = self._normalize_text(text)

        result = IntakeResult(
            document_type=self._detect_document_type(normalized),
            document_confidence=0.65,
            raw_text_preview=normalized[:1500],
        )

        self._find_request_number(normalized, result)
        self._find_regulator(normalized, result)
        self._find_due_date(normalized, result)
        self._find_requests(normalized, result)
        self._validate_required(result)

        return result

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

        if "solicita" in lowered or "requerimos" in lowered:
            return "requerimiento_generico"

        return "unknown"

    def _find_request_number(self, text: str, result: IntakeResult) -> None:
        patterns = [
            r"(SIB[-\s]?\d{4}[-\s]?\d+)",
            r"(REQ[-\s]?\d{4}[-\s]?\d+)",
            r"(Oficio\s*(?:No\.?|Núm\.?)?\s*[:\-]?\s*[A-Za-z0-9\-\/]+)",
            r"(Comunicación\s*(?:No\.?|Núm\.?)?\s*[:\-]?\s*[A-Za-z0-9\-\/]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                result.findings.append(
                    IntakeFinding(
                        field_name="numero_requerimiento",
                        value=match.group(1).strip(),
                        confidence=0.75,
                        source="regex",
                    )
                )
                return

    def _find_regulator(self, text: str, result: IntakeResult) -> None:
        candidates = [
            ("Superintendencia de Bancos", ["superintendencia de bancos", "sib"]),
            ("Dirección General de Impuestos Internos", ["dirección general de impuestos internos", "dgii"]),
            ("Unidad de Análisis Financiero", ["unidad de análisis financiero", "uaf"]),
            ("Banco Central", ["banco central", "bcrd"]),
        ]

        lowered = text.lower()

        for regulator, aliases in candidates:
            if any(alias in lowered for alias in aliases):
                result.findings.append(
                    IntakeFinding(
                        field_name="regulador",
                        value=regulator,
                        confidence=0.85,
                        source="rule",
                    )
                )
                return

    def _find_due_date(self, text: str, result: IntakeResult) -> None:
        patterns = [
            r"(?:antes del|a más tardar el|fecha límite|plazo)\s+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})",
            r"(\d{1,2}\s+de\s+[a-záéíóúñ]+\s+de\s+\d{4})",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                result.findings.append(
                    IntakeFinding(
                        field_name="fecha_limite",
                        value=match.group(1).strip(),
                        confidence=0.70,
                        source="regex",
                        needs_review=True,
                    )
                )
                return

    def _find_requests(self, text: str, result: IntakeResult) -> None:
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

        found = []

        for keyword in keywords:
            if keyword in lowered:
                found.append(keyword)

        result.requested_documents = sorted(set(found))

        for item in found:
            result.requests.append(
                {
                    "description": item,
                    "confidence": 0.55,
                    "source": "keyword",
                    "needs_review": True,
                }
            )

    def _validate_required(self, result: IntakeResult) -> None:
        existing = {item.field_name for item in result.findings}

        required = [
            "numero_requerimiento",
            "regulador",
            "fecha_limite",
        ]

        for field in required:
            if field not in existing:
                result.missing_fields.append(field)

        if result.document_type == "unknown":
            result.warnings.append("No se pudo clasificar el tipo de documento.")

        if result.missing_fields:
            result.warnings.append("Hay campos obligatorios pendientes de validar.")
