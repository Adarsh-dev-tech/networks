# Repository notes (Computer Architecture study guide)

## What this repo is
`Computer Architecture.pdf` (87 pages, handwritten lecture notes) + `ca1.png`..`ca41.png`
(scans of past exam papers). Deliverable: `Computer_Architecture_Study_Guide.pdf`.

## Build pipeline
- Sources live in `/tmp/ca/build`: `gen.py` (ReportLab setup + flowable helpers
  `S fig formula callout bullets table Banner h1..h4 p`), `content1.py`..`content7.py`
  (each exposes `build()` appending to a local `F` via `def A(x): F.extend(...)`),
  `assemble.py` (imports gen + modules, writes the PDF).
- `python3 assemble.py <out.pdf>` builds the guide and prints pages/size/images.
- Fonts: Liberation under `/usr/share/fonts/truetype/liberation` (DejaVu fallback).
- Note pages rendered to `/tmp/ca/pages/pageNNN.png` (also `page002.jpg`..`page087.jpg`
  used as figure sources in `/tmp/ca/figs`).

## Gotchas
- Heredocs (`<<'EOF'`) silently strip a literal `\n` inside a line when writing Python
  string literals -> use `chr(10)` or write patch scripts with the file editor instead.
- Every `A(fig("pageNNN.jpg", ...))` must have a matching `A(p("<b>Reading the figure.</b> ..."))`
  explanation paragraph.
- The notes are handwriting: tesseract OCR is unreliable; topic detection only.

## Status
Guide is 80 pages / 42 diagrams. `content7.py` ends with a "Notes-Page Coverage Map"
(§17) mapping all 87 note pages to guide sections.
