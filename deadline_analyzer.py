import re

from app.engines.document_intelligence.analyzers.base_analyzer import BaseAnalyzer


class DeadlineAnalyzer(BaseAnalyzer):

    def analyze(self, text, understanding):
        lower = text.lower()

        patterns = [
            r"plazo de\s+(\d+)\s+d[ií]as",
            r"en\s+(\d+)\s+d[ií]as",
            r"(\d+)\s+d[ií]as h[aá]biles",
            r"(\d+)\s+horas",
            r"antes del\s+(\d{1,2}/\d{1,2}/\d{4})",
            r"a m[aá]s tardar el\s+(\d{1,2}/\d{1,2}/\d{4})",
        ]

        for pattern in patterns:
            match = re.search(pattern, lower, re.IGNORECASE)

            if match:
                understanding.due_date = match.group(0)
                understanding.metadata["deadline_detected"] = match.group(0)
                return
