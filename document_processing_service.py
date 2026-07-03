from sqlalchemy.orm import Session

from app.core.automation_events import AutomationEvent
from app.models.document import Document
from app.engines.documents.excel_reader import read_excel_with_config
from app.engines.documents.pdf_reader import read_pdf_with_config
from app.engines.documents.text_document_reader import read_text_document_with_config
from app.services.automation_engine_service import run_automation_event


EXCEL_EXTENSIONS = ["xlsx", "xls", "csv"]
PDF_EXTENSIONS = ["pdf"]
TEXT_EXTENSIONS = ["eml", "msg", "docx"]


def trigger_document_processed_event(db: Session, document: Document):
    if not document.record_id:
        return

    from app.services.record_service import get_record

    record = get_record(db, document.record_id)

    if not record:
        return

    run_automation_event(
        db=db,
        process_id=record.process_id,
        trigger_event=AutomationEvent.DOCUMENT_PROCESSED,
        context={
            "record": {
                "id": record.id,
                "process_id": record.process_id,
                "current_state_id": record.current_state_id,
            },
            "document": {
                "id": document.id,
                "document_type_id": document.document_type_id,
                "file_extension": document.file_extension,
                "direction": document.direction,
                "processing_status": document.processing_status,
            },
            "event": {
                "name": AutomationEvent.DOCUMENT_PROCESSED,
            },
        }
    )


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
        result = read_excel_with_config(db=db, document=document)
        trigger_document_processed_event(db, document)
        return result

    if extension in PDF_EXTENSIONS:
        result = read_pdf_with_config(db=db, document=document)
        trigger_document_processed_event(db, document)
        return result

    if extension in TEXT_EXTENSIONS:
        result = read_text_document_with_config(db=db, document=document)
        trigger_document_processed_event(db, document)
        return result

    document.processing_status = "unsupported_for_now"
    db.commit()

    return {
        "document_id": document.id,
        "status": document.processing_status,
        "message": f"Tipo de archivo aún no soportado para procesamiento automático: {extension}"
    }
