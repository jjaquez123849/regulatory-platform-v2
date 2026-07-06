from abc import ABC, abstractmethod

from app.engines.ai.ai_result import (
    AIExtractionResult,
    AIDocumentUnderstandingResult,
)


class BaseAIEngine(ABC):
    @abstractmethod
    def extract_fields(
        self,
        text: str,
        extraction_fields: list,
        instructions: str | None = None,
    ) -> list[AIExtractionResult]:
        pass

    @abstractmethod
    def summarize(self, text: str) -> str:
        pass

    @abstractmethod
    def classify_document(self, text: str, document_types: list) -> dict:
        pass

    @abstractmethod
    def understand_regulatory_request(
        self,
        text: str,
    ) -> AIDocumentUnderstandingResult:
        pass

    @abstractmethod
    def compare_request_vs_response(
        self,
        request_text: str,
        response_text: str,
    ) -> dict:
        pass
