from pathlib import Path
import json

from app.rir.rir_validator import validate_rir


BASE_DIR = Path(r"C:\AML_APPS\RegulatoryPlatform\ai_training")

EXTRACTED_TEXT_DIR = BASE_DIR / "extracted_text"
REVIEWED_RIR_DIR = BASE_DIR / "reviewed_json"


def ensure_rkf_dirs():
    EXTRACTED_TEXT_DIR.mkdir(parents=True, exist_ok=True)
    REVIEWED_RIR_DIR.mkdir(parents=True, exist_ok=True)


def list_rkf_documents() -> list[dict]:
    ensure_rkf_dirs()

    documents = []

    for text_file in sorted(EXTRACTED_TEXT_DIR.glob("*.txt")):
        document_id = text_file.stem
        reviewed_file = REVIEWED_RIR_DIR / f"{document_id}.reviewed.rir.json"

        documents.append(
            {
                "document_id": document_id,
                "text_file": text_file.name,
                "has_reviewed_rir": reviewed_file.exists(),
                "reviewed_rir_file": reviewed_file.name if reviewed_file.exists() else None,
            }
        )

    return documents


def get_rkf_document(document_id: str) -> dict:
    ensure_rkf_dirs()

    text_path = EXTRACTED_TEXT_DIR / f"{document_id}.txt"

    if not text_path.exists():
        raise ValueError("Documento de texto no encontrado.")

    return {
        "document_id": document_id,
        "text": text_path.read_text(encoding="utf-8", errors="ignore"),
    }


def build_empty_rir(document_id: str) -> dict:
    return {
        "rir_version": "1.0",
        "document": {
            "id": document_id,
            "title": None,
            "document_type": "REGULATORY_REQUEST",
            "source": "TEXT",
            "language": "es",
            "pages": None,
            "received_datetime": None,
            "document_datetime": None,
            "hash": None,
            "ocr_quality": None,
            "classification": {
                "label": "requerimiento_informacion",
                "confidence": 0.0,
            },
        },
        "authorities": [],
        "authority_relationships": [],
        "authority_chain": {},
        "legal_instruments": [],
        "request": {
            "reference": None,
            "purpose": None,
            "priority": "UNKNOWN",
            "confidentiality": None,
            "response_required": True,
            "response_type": "INFORMATION_RESPONSE",
            "deadline": {
                "date": None,
                "business_days": None,
                "calendar_days": None,
                "time": None,
                "timezone": "America/Santo_Domingo",
                "raw_text": None,
                "evidence_ids": [],
            },
            "legal_basis": [],
            "summary": None,
            "evidence_ids": [],
        },
        "parties": [],
        "party_groups": [],
        "party_relationships": [],
        "requested_items": [],
        "attachments": [],
        "evidence": [],
        "ai_analysis": {
            "model": "human_review",
            "version": "rir_manual_review_v1",
            "prompt_version": None,
            "temperature": None,
            "execution_time_ms": None,
            "tokens_input": None,
            "tokens_output": None,
            "overall_confidence": None,
            "warnings": [],
            "human_review_required": False,
        },
        "validation": {
            "is_valid": False,
            "missing_required_objects": [],
            "warnings": [],
            "errors": [],
        },
    }


def get_rkf_rir(document_id: str) -> dict:
    ensure_rkf_dirs()

    reviewed_path = REVIEWED_RIR_DIR / f"{document_id}.reviewed.rir.json"

    if reviewed_path.exists():
        return json.loads(reviewed_path.read_text(encoding="utf-8"))

    return build_empty_rir(document_id)


def save_rkf_rir(document_id: str, rir: dict) -> dict:
    ensure_rkf_dirs()

    rir["rir_version"] = "1.0"

    validation = validate_rir(rir)
    rir["validation"] = {
        "is_valid": validation["is_valid"],
        "missing_required_objects": [],
        "warnings": [],
        "errors": validation["errors"],
    }

    output_path = REVIEWED_RIR_DIR / f"{document_id}.reviewed.rir.json"

    output_path.write_text(
        json.dumps(rir, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "document_id": document_id,
        "saved": True,
        "file": str(output_path),
        "validation": validation,
    }


def validate_rkf_rir(document_id: str) -> dict:
    rir = get_rkf_rir(document_id)
    return validate_rir(rir)
