# Repository notes (Computer Architecture annotated study guide)

## What this repo is
`Computer Architecture.pdf` — 87 pages of handwritten lecture notes.
`ca1.png` .. `ca41.png` — 41 scans of previous-year exam papers (a scan may hold several questions).
Deliverable: `Computer_Architecture_Study_Guide.pdf` — an **annotated, page-by-page** guide.

## What the deliverable is
The guide follows the handwritten notes from page 1 to page 87 **in the exact original order**.
For every content-bearing page it shows: (1) a legible screenshot of the original handwritten page,
(2) a transcription, (3) a full explanation of every concept, formula, diagram, table, example and
annotation, expanded from first principles with variables defined. All 41 past-paper scans are
transcribed and solved, and each is placed at the notes page whose topic it examines. Appendices:
PYQ index, 87-row source-coverage table, verification report. No page limit is imposed.

## Build pipeline (sources live in `build/`, working copies in `/tmp/ca/build`)
- `gen.py` — ReportLab setup, fonts, colour palette, paragraph styles, flowable helpers
  (`p bullets formula callout table fig h1..h4`), and `build_toc` (two-pass build for TOC page numbers).
- `gen3.py` — the page-by-page primitives: `PageBand` (the per-page banner, TOC-registered),
  `screenshot`, `ca_screenshot`, `Transcript` (the transcription box) and `eval_units`
  (compiles a snippet of `A(...)` source into flowables).
- `pagecontent_1.py` .. `pagecontent_5.py` — `PAGES[n]` dicts for the handwritten pages
  (`title`, `transcript`, `explain` (a string of `A(...)` calls), `pyqs=[...]`).
- `pagecontent_pyq.py` + `pagecontent_pyq2/3/4.py` — `PYQS[ca]` dicts (later files override earlier
  ones with the most faithful transcriptions). Every scan ca1..ca41 has one.
- `assemble3.py` — the entry point: builds the title page, TOC, then loops `num = 1..87`
  emitting band → screenshot → transcription → explanation → attached PYQ solutions, then the appendices.
- `prepare_assets.py` — renders `Computer Architecture.pdf` to `/tmp/ca/pages/pageNNN.png` (200 dpi)
  and writes the compressed JPEGs `/tmp/ca/embed/pageNNN.jpg` and `/tmp/ca/embed/caN.jpg`.

## Build steps
```
python3 build/prepare_assets.py          # needs Computer Architecture.pdf + ca*.png
cd /tmp/ca/build && python3 assemble3.py /tmp/ca/build/annotated.pdf
cp /tmp/ca/build/annotated.pdf /workspace/project/networks/Computer_Architecture_Study_Guide.pdf
```

## Gotchas
- `prepare_assets.py` writes to `/tmp/ca/...`, which is wiped between sessions — regenerate first.
- `gen3.PageBand` truncates over-long titles to the band width; keep titles short.
- Never shorten a transcription to fit a page — the guide has no page limit.
- PYQ assignment must stay a partition: run the checker that every ca1..ca41 is assigned exactly once.
- The notes are handwriting; a few marginal annotations are only partly legible. Say so rather than guess.

## Status
232 pages, 128 embedded images (87 note screenshots + 41 PYQ scans), 0 layout overflows,
all 87 pages annotated, all 41 PYQs solved, TOC resolved.
