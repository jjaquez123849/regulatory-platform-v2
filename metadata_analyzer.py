import re

from app.engines.document_intelligence.analyzers.base_analyzer import BaseAnalyzer


class MetadataAnalyzer(BaseAnalyzer):

    def analyze(
        self,
        text,
        understanding
    ):

        understanding.metadata["characters"] = len(text)

        understanding.metadata["lines"] = len(text.splitlines())

        understanding.metadata["words"] = len(text.split())

        understanding.metadata["paragraphs"] = len(
            [l for l in text.split("\n\n") if l.strip()]
        )

        understanding.metadata["contains_tables"] = bool(
            re.search(r"\|\s*\w+", text)
        )

        understanding.metadata["contains_signature"] = (
            "firma" in text.lower()
        )

        understanding.metadata["contains_annexes"] = (
            "anexo" in text.lower()
        )
