import re

from app.engines.document_intelligence.analyzers.base_analyzer import BaseAnalyzer
from app.engines.document_intelligence.document_model import DocumentEntity


class EntityAnalyzer(BaseAnalyzer):

    def analyze(self, text, understanding):
        self._extract_identifications(text, understanding)
        self._extract_emails(text, understanding)
        self._extract_accounts(text, understanding)

    def _add_entity(self, understanding, entity_type, value, confidence=0.65):
        if not value:
            return

        exists = any(
            item.entity_type == entity_type and item.value == value
            for item in understanding.entities
        )

        if exists:
            return

        understanding.entities.append(
            DocumentEntity(
                entity_type=entity_type,
                value=value,
                confidence=confidence
            )
        )

    def _extract_identifications(self, text, understanding):
        patterns = [
            r"\b\d{3}-\d{7}-\d\b",
            r"\b\d{11}\b",
            r"\b\d{9}\b",
        ]

        for pattern in patterns:
            for match in re.findall(pattern, text):
                self._add_entity(
                    understanding,
                    "identification",
                    match,
                    confidence=0.80
                )

    def _extract_emails(self, text, understanding):
        pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

        for match in re.findall(pattern, text):
            self._add_entity(
                understanding,
                "email",
                match,
                confidence=0.90
            )

    def _extract_accounts(self, text, understanding):
        patterns = [
            r"(cuenta|cta\.?)\s*[:#-]?\s*(\d{6,20})",
            r"\b\d{10,20}\b",
        ]

        for pattern in patterns:
            for match in re.findall(pattern, text, re.IGNORECASE):
                value = match[-1] if isinstance(match, tuple) else match

                self._add_entity(
                    understanding,
                    "account",
                    value,
                    confidence=0.60
                )
