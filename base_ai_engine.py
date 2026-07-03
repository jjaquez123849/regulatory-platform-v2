from abc import ABC, abstractmethod

from app.engines.ai.ai_result import AIExtractionResult


class BaseAIEngine(ABC):
    @abstractmethod
    def extract_fields(
        self,
        text: str,
        extraction_fields: list
    ) -> list[AIExtractionResult]:
        pass

    @abstractmethod
    def summarize(
        self,
        text: str
    ) -> str:
        pass

    @abstractmethod
    def classify_document(
        self,
        text: str,
        document_types: list
    ) -> dict:
        pass
