from sqlalchemy.orm import Session

from app.models.document import Document
from app.engines.documents.excel_reader import read_excel_with_config
from app.engines.documents.pdf_reader import read_pdf_with_config


EXCEL_EXTENSIONS = ["xlsx", "xls", "csv"]
PDF_EXTENSIONS = ["pdf"]


def process_document(db: Session, document_id: int) -> dict:
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.is_deleted == False
        )
        .first()
    )

    if not document:
        raise ValueError("Documento no encontrado.")

    extension = (document.file_extension or "").lower()

    if extension in EXCEL_EXTENSIONS:
        return read_excel_with_config(
            db=db,
            document=document
        )

    if extension in PDF_EXTENSIONS:
        return read_pdf_with_config(
            db=db,
            document=document
        )

    document.processing_status = "unsupported_for_now"
    db.commit()

    return {
        "document_id": document.id,
        "status": document.processing_status,
        "message": f"Tipo de archivo aún no soportado para procesamiento automático: {extension}"
    }
