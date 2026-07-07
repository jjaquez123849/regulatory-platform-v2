from pathlib import Path
import json


BASE_DIR = Path(r"C:\AML_APPS\RegulatoryPlatform\ai_training")

EXTRACTED_TEXT_DIR = BASE_DIR / "extracted_text"
REVIEWED_RIR_DIR = BASE_DIR / "reviewed_json"
DATASETS_DIR = BASE_DIR / "datasets"
REPORTS_DIR = BASE_DIR / "reports"


SYSTEM_PROMPT = """
Actúa como un analista experto en requerimientos regulatorios bancarios.

Tu tarea es convertir el texto del documento en RIR 1.0.

Reglas:
1. Devuelve solo JSON válido.
2. Usa rir_version = "1.0".
3. No inventes información.
4. Si un dato no aparece, usa null.
5. Toda autoridad, persona, solicitud, fecha o instrumento legal debe tener evidencia.
6. El issuer no siempre es la autoridad que origina la solicitud.
7. Si el documento indica que una entidad actúa por orden de otra, representa la cadena de autoridad.
8. Si hay personas en tablas, listas, comas, “y/o” o “/”, representa Party, PartyGroup o PartyRelationship.
""".strip()


def ensure_dirs():
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def main():
    ensure_dirs()

    output_path = DATASETS_DIR / "rir_sft_dataset.jsonl"
    report_path = REPORTS_DIR / "rir_dataset_report.json"

    processed = []
    skipped = []

    reviewed_files = sorted(REVIEWED_RIR_DIR.glob("*.json"))

    with output_path.open("w", encoding="utf-8") as output:
        for rir_path in reviewed_files:
            document_id = rir_path.stem.replace(".reviewed", "")
            text_path = EXTRACTED_TEXT_DIR / f"{document_id}.txt"

            if not text_path.exists():
                skipped.append({
                    "document_id": document_id,
                    "reason": "No existe texto extraído",
                })
                continue

            text = text_path.read_text(encoding="utf-8", errors="ignore").strip()
            rir = json.loads(rir_path.read_text(encoding="utf-8"))

            if not text:
                skipped.append({
                    "document_id": document_id,
                    "reason": "Texto vacío",
                })
                continue

            item = {
                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": text,
                    },
                    {
                        "role": "assistant",
                        "content": json.dumps(rir, ensure_ascii=False),
                    },
                ],
                "metadata": {
                    "document_id": document_id,
                    "task": "document_to_rir",
                    "rir_version": "1.0",
                },
            }

            output.write(json.dumps(item, ensure_ascii=False) + "\n")

            processed.append({
                "document_id": document_id,
                "text_length": len(text),
                "rir_file": str(rir_path),
            })

    report = {
        "dataset_file": str(output_path),
        "processed_count": len(processed),
        "skipped_count": len(skipped),
        "processed": processed,
        "skipped": skipped,
    }

    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Dataset RIR generado.")
    print(f"Procesados: {len(processed)}")
    print(f"Omitidos: {len(skipped)}")
    print(f"Dataset: {output_path}")


if __name__ == "__main__":
    main()
