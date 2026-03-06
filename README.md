# pdfocr

PDF to Markdown converter powered by [Docling](https://github.com/DS4SD/docling). Handles text-based PDFs, scanned/image PDFs, and mixed documents with OCR. Automatically detects chapters and splits output into separate Markdown files.

## Installation

```bash
git clone https://github.com/krzysztofsurdy/pdfocr.git
cd pdfocr
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```bash
# Basic usage - outputs to ./output/
python convert.py document.pdf

# Specify output directory
python convert.py document.pdf ./my-output
```

If the PDF contains chapters (detected via top-level headings), each chapter is saved as a separate file:

```
output/
  01_introduction.md
  02_getting_started.md
  03_advanced_topics.md
```

If no chapters are detected, a single Markdown file is created.

## License

MIT
