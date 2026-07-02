from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from app.models.document import Document, DocumentExtractionResult
from app.models.document_config import ExcelColumnMapping


def read_excel_with_config(
    db: Session,
    document: Document
) -> dict:
    if not document.document_type_id:
        raise ValueError("El documento no tiene tipo de documento configurado.")

    file_path = Path(document.file_path)

    if not file_path.exists():
        raise ValueError("El archivo físico no existe.")

    mappings = (
        db.query(ExcelColumnMapping)
        .filter(ExcelColumnMapping.document_type_id == document.document_type_id)
        .all()
    )

    if not mappings:
        raise ValueError("No hay mapeos Excel configurados para este tipo de documento.")

    results = []
    errors = []

    mappings_by_sheet = {}

    for mapping in mappings:
        sheet_key = mapping.sheet_name or "__default__"
        mappings_by_sheet.setdefault(sheet_key, []).append(mapping)

    for sheet_key, sheet_mappings in mappings_by_sheet.items():
        header_row = sheet_mappings[0].header_row or 1

        try:
            if sheet_key == "__default__":
                df = pd.read_excel(
                    file_path,
                    header=header_row - 1
                )
                sheet_name_used = None
            else:
                df = pd.read_excel(
                    file_path,
                    sheet_name=sheet_key,
                    header=header_row - 1
                )
                sheet_name_used = sheet_key

        except Exception as error:
            errors.append(f"No se pudo leer hoja '{sheet_key}': {error}")
            continue

        df.columns = [str(col).strip() for col in df.columns]

        for mapping in sheet_mappings:
            column_name = mapping.column_name.strip()

            if column_name not in df.columns:
                if mapping.is_required:
                    errors.append(f"Columna requerida no encontrada: {column_name}")
                continue

            for row_index, row in df.iterrows():
                value = row.get(column_name)

                if pd.isna(value):
                    continue

                extraction = DocumentExtractionResult(
                    document_id=document.id,
                    record_id=document.record_id,
                    target_entity=mapping.target_entity,
                    target_field=mapping.target_field,
                    extracted_value=str(value),
                    normalized_value=str(value).strip(),
                    confidence_score="1.0",
                    status="proposed"
                )

                db.add(extraction)

                results.append(
                    {
                        "sheet_name": sheet_name_used,
                        "row_index": int(row_index) + 1,
                        "column_name": column_name,
                        "target_entity": mapping.target_entity,
                        "target_field": mapping.target_field,
                        "value": str(value)
                    }
                )

    document.processing_status = "excel_extracted" if not errors else "excel_extracted_with_errors"

    db.commit()

    return {
        "document_id": document.id,
        "status": document.processing_status,
        "results_count": len(results),
        "results": results,
        "errors": errors
    }
