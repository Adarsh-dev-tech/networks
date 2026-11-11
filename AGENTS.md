# Repository notes (Computer Architecture study guide)

## What this repo is
`Computer Architecture.pdf` (87 pages, handwritten lecture notes) + `ca1.png`..`ca41.png`
(scans of past exam papers). Deliverable: `Computer_Architecture_Study_Guide.pdf`.

## Build pipeline
Sources live in `/tmp/ca/build`:
- `gen.py` — ReportLab setup + flowable helpers (`fig formula callout bullets table Banner h1..h4 p`) and the `TocDocTemplate` / `build_toc` used for the contents page.
- `content1.py`..`content7.py` — the authored content, each exposing `build()` that appends to a local `F` via `def A(x): F.extend(...)`.
- `extra.py` — `EXTRA[<name>]` string blocks with the sections the previous guide lacked (cache levels, levels of parallelism, SIMD/MIMD, shared vs distributed memory, topologies, DVFS, superscalar, CPU-time metrics, a worked Tomasulo example) plus `PAGE_MAP` (notes page -> topic) used to build the coverage table.
- `pool.json` / `sections.json` — the content of `content*.py` extracted unit-by-unit (an `ast` walk of each `build()`); `sections.json` groups units into sections keyed by a stable slug (`<module>__<slug>`).
- `gen2.py` — rebuilds the guide **in the exact order of the handwritten notes**. Its `ORDER` list is the single source of truth for sequence; each entry is `('banner'|'sec'|'extra'|'pyqindex'|'coverage'|'audit', ...)`. It renumbers the `h3`/`h4` headings to `§n.sub` and de-duplicates figures.
- `assemble2.py` — imports `gen2`, adds the title page + TOC, writes the PDF, prints pages/size/images.

Build: `python3 assemble2.py <out.pdf>`.

## Gotchas
- Heredocs (`<<'EOF'`) silently strip a literal `\n` inside a line when writing Python string literals -> use `chr(10)` or write patch scripts with the file editor instead.
- Every `A(fig("pageNNN.jpg", ...))` must have a matching `A(p("<b>Reading the figure.</b> ..."))` explanation paragraph (currently 46 figures, all explained).
- `sections.json` keys are position-based internally; always address sections by their `stable` slug.
- Re-generating `sections.json` after editing `content*.py` requires the ast-walk snippet; the stable slugs must stay the same.
- Fonts: Liberation under `/usr/share/fonts/truetype/liberation` (DejaVu fallback).
- Note pages rendered to `/tmp/ca/pages/pageNNN.png` and `/tmp/ca/figs/pageNNN.jpg` (figure sources).

## Status
Guide is 81 pages / 46 diagrams, ordered to follow the notes page-by-page:
foundations (pp. 2-7) -> ISA/RISC-CISC/data (pp. 12-13, 15, 18) -> performance & Amdahl
(pp. 19-23) -> dependability (pp. 24-27) -> CPU time/CPI/MIPS (pp. 28-32) -> pipelining
(pp. 33-36) -> loop unrolling (pp. 49-52) -> branch prediction (pp. 37-41, 45-46) ->
scoreboarding/Tomasulo (pp. 42-44, 47-48, 53-60) -> speculation/ROB (pp. 55-66) ->
multiprocessors (pp. 5, 7-11, 68) -> cache (pp. 70-81) -> virtual memory (p. 82) ->
cache coherence (pp. 84-87) -> vector/SIMD/GPU (pp. 16-17, 61-62) -> appendices
(PYQ index, 87-row coverage table, audit report).
