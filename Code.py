from pathlib import Path
import json

from app.engines.document_intelligence.document_intelligence_engine import (
    DocumentIntelligenceEngine,
)


BASE_DIR = Path(r"C:\AML_APPS\RegulatoryPlatform\ai_training")
RAW_INCOMING_DIR = BASE_DIR / "raw_documents" / "incoming"
REPORTS_DIR = BASE_DIR / "reports"

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".xls", ".txt"}


def main():
    RAW_INCOMING_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    engine = DocumentIntelligenceEngine(base_training_dir=str(BASE_DIR))

    processed = []
    skipped = []

    for file_path in sorted(RAW_INCOMING_DIR.iterdir()):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            skipped.append(
                {
                    "filename": file_path.name,
                    "reason": "Extensión no soportada",
                }
            )
            continue

        try:
            result = engine.build_package(file_path)

            processed.append(
                {
                    "document_id": result.document_id,
                    "filename": file_path.name,
                    "package_dir": result.package_dir,
                    "extracted_length": len(result.extracted_text),
                    "normalized_length": len(result.normalized_text),
                    "pages": result.metadata.get("pages"),
                    "contains_tables": result.metadata.get("contains_tables"),
                    "contains_images": result.metadata.get("contains_images"),
                }
            )

        except Exception as error:
            skipped.append(
                {
                    "filename": file_path.name,
                    "reason": str(error),
                }
            )

    report = {
        "processed_count": len(processed),
        "skipped_count": len(skipped),
        "processed": processed,
        "skipped": skipped,
    }

    report_path = REPORTS_DIR / "document_packages_report.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Document Intelligence Packages generados.")
    print(f"Procesados: {len(processed)}")
    print(f"Omitidos: {len(skipped)}")
    print(f"Reporte: {report_path}")


if __name__ == "__main__":
    main()
