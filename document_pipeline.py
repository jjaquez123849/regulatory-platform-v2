from app.engines.document_intelligence.document_model import DocumentUnderstanding

from app.engines.document_intelligence.analyzers.metadata_analyzer import MetadataAnalyzer
from app.engines.document_intelligence.analyzers.issuer_analyzer import IssuerAnalyzer
from app.engines.document_intelligence.analyzers.entity_analyzer import EntityAnalyzer
from app.engines.document_intelligence.analyzers.request_analyzer import RequestAnalyzer
from app.engines.document_intelligence.analyzers.deadline_analyzer import DeadlineAnalyzer


class DocumentPipeline:

    def __init__(self):
        self.analyzers = [
            MetadataAnalyzer(),
            IssuerAnalyzer(),
            EntityAnalyzer(),
            RequestAnalyzer(),
            DeadlineAnalyzer(),
        ]

    def analyze(self, text: str) -> DocumentUnderstanding:
        understanding = DocumentUnderstanding()

        for analyzer in self.analyzers:
            analyzer.analyze(
                text=text,
                understanding=understanding
            )

        return understanding
