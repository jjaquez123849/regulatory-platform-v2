from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pdfplumber


@dataclass
class DocumentIntelligenceResult:
    document_id: str
    package_dir: str
    extracted_text: str
    normalized_text: str
    dom: dict
    metadata: dict


class DocumentIntelligenceEngine:
    def __init__(self, base_training_dir: str):
        self.base_dir = Path(base_training_dir)
        self.package_dir = self.base_dir / "document_packages"
        self.extracted_text_dir = self.base_dir / "extracted_text"
        self.report_dir = self.base_dir / "reports"

        self.package_dir.mkdir(parents=True, exist_ok=True)
        self.extracted_text_dir.mkdir(parents=True, exist_ok=True)
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def build_package(self, source_file: str | Path) -> DocumentIntelligenceResult:
        source_path = Path(source_file)

        if not source_path.exists():
            raise ValueError(f"Archivo no encontrado: {source_path}")

        document_id = source_path.stem
        target_dir = self.package_dir / document_id
        target_dir.mkdir(parents=True, exist_ok=True)

        original_path = target_dir / source_path.name
        shutil.copy2(source_path, original_path)

        extension = source_path.suffix.lower()

        if extension == ".pdf":
            extracted_text, normalized_text, dom = self._process_pdf(source_path)
        else:
            extracted_text = source_path.read_text(encoding="utf-8", errors="ignore")
            normalized_text = self._normalize_text(extracted_text)
            dom = self._build_text_dom(document_id, source_path.name, extracted_text)

        metadata = {
            "document_id": document_id,
            "source_filename": source_path.name,
            "extension": extension,
            "sha256": self._sha256(source_path),
            "processed_at": datetime.utcnow().isoformat(),
            "engine": "DocumentIntelligenceEngine",
            "engine_version": "1.0",
            "extracted_length": len(extracted_text),
            "normalized_length": len(normalized_text),
            "pages": len(dom.get("pages", [])),
            "contains_tables": any(page.get("tables") for page in dom.get("pages", [])),
            "contains_images": any(page.get("images") for page in dom.get("pages", [])),
            "contains_qr": any(page.get("qr_codes") for page in dom.get("pages", [])),
            "contains_barcodes": any(page.get("barcodes") for page in dom.get("pages", [])),
            "ocr_available": False,
            "qr_detection_available": False,
            "barcode_detection_available": False,
        }

        (target_dir / "extracted.txt").write_text(extracted_text, encoding="utf-8")
        (target_dir / "normalized.txt").write_text(normalized_text, encoding="utf-8")
        (target_dir / "document.dom.json").write_text(
            json.dumps(dom, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        (target_dir / "metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        # Compatibilidad con RKF actual
        (self.extracted_text_dir / f"{document_id}.txt").write_text(
            normalized_text,
            encoding="utf-8",
        )

        return DocumentIntelligenceResult(
            document_id=document_id,
            package_dir=str(target_dir),
            extracted_text=extracted_text,
            normalized_text=normalized_text,
            dom=dom,
            metadata=metadata,
        )

    def _process_pdf(self, pdf_path: Path) -> tuple[str, str, dict]:
        pages = []
        extracted_chunks = []
        normalized_chunks = []

        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                words = page.extract_words(
                    x_tolerance=2,
                    y_tolerance=3,
                    keep_blank_chars=False,
                    use_text_flow=False,
                    extra_attrs=[],
                )

                lines = self._words_to_lines(words)
                paragraphs = self._lines_to_paragraphs(lines)

                tables = self._extract_tables(page)
                images = self._extract_images(page)

                page_text = "\n".join(line["text"] for line in lines).strip()
                normalized_page_text = self._normalize_text(page_text)

                extracted_chunks.append(f"\n--- PAGE {page_number} ---\n{page_text}")
                normalized_chunks.append(
                    f"\n--- PAGE {page_number} ---\n{normalized_page_text}"
                )

                page_payload = {
                    "page_number": page_number,
                    "width": page.width,
                    "height": page.height,
                    "orientation": "landscape" if page.width > page.height else "portrait",
                    "text": page_text,
                    "normalized_text": normalized_page_text,
                    "lines": lines,
                    "paragraphs": paragraphs,
                    "tables": tables,
                    "images": images,
                    "qr_codes": [],
                    "barcodes": [],
                    "headers": self._detect_headers(lines),
                    "footers": self._detect_footers(lines),
                    "reading_order": self._build_reading_order(paragraphs, tables),
                    "quality": {
                        "word_count": len(words),
                        "line_count": len(lines),
                        "paragraph_count": len(paragraphs),
                        "table_count": len(tables),
                        "image_count": len(images),
                        "needs_ocr": len(words) < 10 and len(images) > 0,
                    },
                }

                pages.append(page_payload)

        extracted_text = "\n\n".join(extracted_chunks).strip()
        normalized_text = "\n\n".join(normalized_chunks).strip()

        dom = {
            "dom_version": "1.0",
            "document_id": pdf_path.stem,
            "source_file": pdf_path.name,
            "document_type": "PDF",
            "pages": pages,
        }

        return extracted_text, normalized_text, dom

    def _words_to_lines(self, words: list[dict]) -> list[dict]:
        if not words:
            return []

        sorted_words = sorted(words, key=lambda item: (item["top"], item["x0"]))

        line_groups: list[list[dict]] = []

        for word in sorted_words:
            placed = False

            for group in line_groups:
                avg_top = sum(item["top"] for item in group) / len(group)

                if abs(word["top"] - avg_top) <= 3:
                    group.append(word)
                    placed = True
                    break

            if not placed:
                line_groups.append([word])

        lines = []

        for index, group in enumerate(line_groups, start=1):
            group = sorted(group, key=lambda item: item["x0"])
            text = self._join_words_by_coordinates(group)

            lines.append(
                {
                    "id": f"line_{index}",
                    "line_index": index,
                    "text": text,
                    "x0": min(item["x0"] for item in group),
                    "x1": max(item["x1"] for item in group),
                    "top": min(item["top"] for item in group),
                    "bottom": max(item["bottom"] for item in group),
                    "words": [
                        {
                            "text": item["text"],
                            "x0": item["x0"],
                            "x1": item["x1"],
                            "top": item["top"],
                            "bottom": item["bottom"],
                        }
                        for item in group
                    ],
                }
            )

        return lines

    def _join_words_by_coordinates(self, words: list[dict]) -> str:
        if not words:
            return ""

        output = []
        previous = None

        for word in words:
            current_text = word["text"]

            if previous is None:
                output.append(current_text)
                previous = word
                continue

            gap = word["x0"] - previous["x1"]
            avg_char_width = max(
                (previous["x1"] - previous["x0"]) / max(len(previous["text"]), 1),
                1,
            )

            if gap > avg_char_width * 0.45:
                output.append(" ")

            output.append(current_text)
            previous = word

        return "".join(output).strip()

    def _lines_to_paragraphs(self, lines: list[dict]) -> list[dict]:
        if not lines:
            return []

        paragraphs = []
        current = []
        paragraph_index = 1

        for line in lines:
            if not current:
                current.append(line)
                continue

            previous = current[-1]
            vertical_gap = line["top"] - previous["bottom"]
            left_shift = abs(line["x0"] - previous["x0"])

            starts_new = vertical_gap > 10 or left_shift > 80

            if starts_new:
                paragraphs.append(
                    self._build_paragraph(paragraph_index, current)
                )
                paragraph_index += 1
                current = [line]
            else:
                current.append(line)

        if current:
            paragraphs.append(self._build_paragraph(paragraph_index, current))

        return paragraphs

    def _build_paragraph(self, index: int, lines: list[dict]) -> dict:
        text = " ".join(line["text"] for line in lines).strip()

        return {
            "id": f"paragraph_{index}",
            "paragraph_index": index,
            "text": text,
            "line_ids": [line["id"] for line in lines],
            "x0": min(line["x0"] for line in lines),
            "x1": max(line["x1"] for line in lines),
            "top": min(line["top"] for line in lines),
            "bottom": max(line["bottom"] for line in lines),
        }

    def _extract_tables(self, page: Any) -> list[dict]:
        tables = []

        try:
            extracted_tables = page.extract_tables() or []

            for index, table in enumerate(extracted_tables, start=1):
                tables.append(
                    {
                        "id": f"table_{index}",
                        "table_index": index,
                        "rows": table,
                        "row_count": len(table),
                        "column_count": max((len(row) for row in table), default=0),
                    }
                )
        except Exception:
            return []

        return tables

    def _extract_images(self, page: Any) -> list[dict]:
        images = []

        for index, image in enumerate(page.images or [], start=1):
            images.append(
                {
                    "id": f"image_{index}",
                    "image_index": index,
                    "x0": image.get("x0"),
                    "x1": image.get("x1"),
                    "top": image.get("top"),
                    "bottom": image.get("bottom"),
                    "width": image.get("width"),
                    "height": image.get("height"),
                    "contains_text": None,
                    "contains_qr": None,
                    "contains_barcode": None,
                    "ocr_required": True,
                }
            )

        return images

    def _detect_headers(self, lines: list[dict]) -> list[str]:
        return [line["text"] for line in lines[:3]]

    def _detect_footers(self, lines: list[dict]) -> list[str]:
        return [line["text"] for line in lines[-3:]]

    def _build_reading_order(
        self,
        paragraphs: list[dict],
        tables: list[dict],
    ) -> list[str]:
        items = []

        for paragraph in paragraphs:
            items.append(
                {
                    "id": paragraph["id"],
                    "top": paragraph["top"],
                    "x0": paragraph["x0"],
                }
            )

        for table in tables:
            items.append(
                {
                    "id": table["id"],
                    "top": 999999,
                    "x0": 0,
                }
            )

        return [
            item["id"]
            for item in sorted(items, key=lambda value: (value["top"], value["x0"]))
        ]

    def _normalize_text(self, text: str) -> str:
        if not text:
            return ""

        text = text.replace("\r", "\n")

        # Separación dinámica de minúscula seguida de mayúscula
        text = self._safe_regex_replace(
            r"([a-záéíóúñ])([A-ZÁÉÍÓÚÑ])",
            r"\1 \2",
            text,
        )

        # Separación dinámica letra-número / número-letra
        text = self._safe_regex_replace(
            r"([A-Za-zÁÉÍÓÚáéíóúñÑ])(\d)",
            r"\1 \2",
            text,
        )
        text = self._safe_regex_replace(
            r"(\d)([A-Za-zÁÉÍÓÚáéíóúñÑ])",
            r"\1 \2",
            text,
        )

        # Normalización de espacios, sin diccionario duro
        import re

        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    def _safe_regex_replace(self, pattern: str, repl: str, text: str) -> str:
        import re

        return re.sub(pattern, repl, text)

    def _build_text_dom(
        self,
        document_id: str,
        source_file: str,
        text: str,
    ) -> dict:
        lines = [
            {
                "id": f"line_{index + 1}",
                "line_index": index + 1,
                "text": line,
            }
            for index, line in enumerate(text.splitlines())
            if line.strip()
        ]

        return {
            "dom_version": "1.0",
            "document_id": document_id,
            "source_file": source_file,
            "document_type": "TEXT",
            "pages": [
                {
                    "page_number": None,
                    "text": text,
                    "normalized_text": self._normalize_text(text),
                    "lines": lines,
                    "paragraphs": [],
                    "tables": [],
                    "images": [],
                    "qr_codes": [],
                    "barcodes": [],
                    "headers": [],
                    "footers": [],
                    "reading_order": [line["id"] for line in lines],
                    "quality": {
                        "word_count": len(text.split()),
                        "line_count": len(lines),
                        "paragraph_count": 0,
                        "table_count": 0,
                        "image_count": 0,
                        "needs_ocr": False,
                    },
                }
            ],
        }

    def _sha256(self, path: Path) -> str:
        hasher = hashlib.sha256()

        with path.open("rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                hasher.update(chunk)

        return hasher.hexdigest()
