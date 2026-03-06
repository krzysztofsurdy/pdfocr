#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

from docling.document_converter import DocumentConverter
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn


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

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Converting PDF...", total=None)

        converter = DocumentConverter()
        result = converter.convert(str(pdf_path))

        progress.update(task, description="Exporting to Markdown...")
        markdown = result.document.export_to_markdown()

    chapters = split_by_chapters(markdown)

    if chapters:
        for i, (title, content) in enumerate(chapters, 1):
            filename = f"{i:02d}_{slugify(title)}.md"
            (output_dir / filename).write_text(content, encoding="utf-8")
        console.print(f"[green]Saved {len(chapters)} chapters to {output_dir}/")
    else:
        out_file = output_dir / f"{slugify(pdf_path.stem)}.md"
        out_file.write_text(markdown, encoding="utf-8")
        console.print(f"[green]Saved to {out_file}")


if __name__ == "__main__":
    main()
