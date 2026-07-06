from abc import ABC, abstractmethod

from app.engines.intake_ai.contracts.intake_result import IntakeResult


class BaseIntakeAIEngine(ABC):
    @abstractmethod
    def analyze_text(self, text: str) -> IntakeResult:
        raise NotImplementedError
