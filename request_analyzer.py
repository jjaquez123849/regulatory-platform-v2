import re

from app.engines.document_intelligence.analyzers.base_analyzer import BaseAnalyzer
from app.engines.document_intelligence.document_model import DocumentRequest


class RequestAnalyzer(BaseAnalyzer):

    KEYWORDS = [
        "certificación",
        "certificacion",
        "inmovilización",
        "inmovilizacion",
        "descongelamiento",
        "bloqueo",
        "desbloqueo",
        "estado de cuenta",
        "movimientos",
        "información",
        "informacion",
        "productos",
        "remitir",
        "solicita",
        "requerimos",
    ]

    def analyze(self, text, understanding):
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        for line in lines:
            lower = line.lower()

            if any(keyword in lower for keyword in self.KEYWORDS):
                request_type = self._classify_request_type(lower)

                understanding.requests.append(
                    DocumentRequest(
                        request_number=None,
                        description=line,
                        priority=self._detect_priority(lower),
                        metadata={
                            "request_type": request_type,
                            "source": "request_analyzer"
                        }
                    )
                )

    def _classify_request_type(self, text):
        if "certific" in text:
            return "certificacion"

        if "inmoviliz" in text or "bloqueo" in text:
            return "inmovilizacion"

        if "descongel" in text or "desbloqueo" in text:
            return "descongelamiento"

        if "estado de cuenta" in text:
            return "estado_cuenta"

        if "movimiento" in text:
            return "movimientos"

        if "producto" in text:
            return "informacion_productos"

        return "otro"

    def _detect_priority(self, text):
        if re.search(r"\b(urgente|inmediato|24 horas|48 horas)\b", text):
            return "high"

        return "medium"
