from app.engines.document_intelligence.document_pipeline import (
    DocumentPipeline,
)


class DocumentIntelligenceEngine:

    def __init__(self):

        self.pipeline = DocumentPipeline()

    def understand_document(
        self,
        text: str
    ):
        return self.pipeline.analyze(text)
