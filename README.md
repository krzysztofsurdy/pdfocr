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
source .venv/bin/activate
python convert.py path/to/document.pdf
```

The output directory is created next to the PDF, named after the file. For example:

```
python convert.py "My Report (2024).pdf"
```

Produces:

```
my_report_2024_output/
  01_introduction.md
  02_getting_started.md
  03_advanced_topics.md
```

If no chapters are detected, a single Markdown file is created instead.

## License

MIT
