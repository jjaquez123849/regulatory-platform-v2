from abc import ABC, abstractmethod

from app.engines.document_intelligence.document_model import (
    DocumentUnderstanding,
)


class BaseAnalyzer(ABC):

    @abstractmethod
    def analyze(
        self,
        text: str,
        understanding: DocumentUnderstanding
    ) -> None:
        """
        Analiza el documento y modifica el modelo DocumentUnderstanding.
        """
        pass
