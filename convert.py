#!/usr/bin/env python3
from __future__ import annotations

import logging
import re
import sys
from pathlib import Path

from docling.document_converter import DocumentConverter
from rich.console import Console
from rich.status import Status


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "_", text)
    return text[:80]


def split_by_chapters(markdown: str) -> list[tuple[str, str]]:
    pattern = r"^(# .+)$"
    parts = re.split(pattern, markdown, flags=re.MULTILINE)

    if len(parts) <= 1:
        return []

    chapters = []
    for i in range(1, len(parts), 2):
        title = parts[i].lstrip("# ").strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        chapters.append((title, parts[i] + body))

    return chapters


def get_page_count(pdf_path: Path) -> int:
    import pypdfium2 as pdfium
    pdf = pdfium.PdfDocument(pdf_path)
    count = len(pdf)
    pdf.close()
    return count


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python convert.py <pdf_file>")
        sys.exit(1)

    pdf_path = Path(sys.argv[1]).resolve()
    if not pdf_path.exists():
        print(f"File not found: {pdf_path}")
        sys.exit(1)

    output_dir = pdf_path.parent / f"{slugify(pdf_path.stem)}_output"
    output_dir.mkdir(parents=True, exist_ok=True)

    console = Console()
    total_pages = get_page_count(pdf_path)
    console.print(f"[bold]PDF has {total_pages} pages")

    logging.getLogger("docling").setLevel(logging.WARNING)

    with Status("[bold blue]Initializing pipeline...", console=console) as status:
        converter = DocumentConverter()

        status.update("[bold blue]Converting PDF (this may take a while)...")
        result = converter.convert(str(pdf_path))

        status.update("[bold blue]Exporting to Markdown...")
        markdown = result.document.export_to_markdown()

    console.print("[bold blue]Splitting into chapters...")
    chapters = split_by_chapters(markdown)

    if chapters:
        for i, (title, content) in enumerate(chapters, 1):
            filename = f"{i:02d}_{slugify(title)}.md"
            (output_dir / filename).write_text(content, encoding="utf-8")
            console.print(f"  [dim]{filename}")
        console.print(f"[green]Saved {len(chapters)} chapters to {output_dir}/")
    else:
        out_file = output_dir / f"{slugify(pdf_path.stem)}.md"
        out_file.write_text(markdown, encoding="utf-8")
        console.print(f"[green]Saved to {out_file}")


if __name__ == "__main__":
    main()
