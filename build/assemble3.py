"""Assemble the annotated, page-by-page Computer Architecture study guide."""
import os, sys, importlib, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen
from gen import (h1,h2,h3,h4,p,bullets,formula,callout,table,fig,Spacer,PageBreak,
                 Paragraph,ST,NAVY,AMBER,AMBERB,LIGHT,GREY,RULE,CW,PW,PH,LM,RM,TM,BM)
from reportlab.platypus import (Table, TableStyle, Flowable, KeepTogether, Image,
                                CondPageBreak, PageBreak)
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus.tableofcontents import TableOfContents
import gen3
from gen3 import (eval_units, page_header, pyq_header, screenshot, ca_screenshot,
                  transcription, PageBand, Transcript)

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- collect page annotations ----
PAGES = {}
for f in ['pagecontent_1','pagecontent_2','pagecontent_3','pagecontent_4','pagecontent_5']:
    PAGES.update(importlib.import_module(f).PAGES)
import pagecontent_pyq
PYQS = pagecontent_pyq.PYQS
import pagecontent_pyq2, pagecontent_pyq3, pagecontent_pyq4
PYQS.update(pagecontent_pyq2.PYQS)
PYQS.update(pagecontent_pyq3.PYQS)
PYQS.update(pagecontent_pyq4.PYQS)


def title_page():
    F = []
    F.append(Spacer(1, 2.6*cm))
    F.append(Paragraph("Computer Architecture",
        gen.S('tp', fontName="Head", fontSize=34, leading=38, textColor=NAVY, alignment=1)))
    F.append(Spacer(1, 0.25*cm))
    F.append(Paragraph("Annotated Study Guide — page by page",
        gen.S('tp2', fontName="Head-Reg", fontSize=17, leading=22,
              textColor=colors.HexColor("#2E6DA4"), alignment=1)))
    F.append(Spacer(1, 0.7*cm))
    F.append(Paragraph(
        "This guide follows the lecturer’s handwritten notes from page 1 to page 87, in the exact "
        "original order. For every content-bearing page you get the original screenshot, a clean "
        "transcription of what is written, and a full explanation of every concept, formula, diagram, "
        "table, example and annotation — expanded from first principles, with derivations and every "
        "variable explained. All 41 past-paper scans (ca1–ca41) are transcribed and solved in full, and "
        "each is placed at the point in the notes where its topic appears.",
        gen.S('tp3', fontSize=10.5, leading=14.5, textColor=colors.HexColor("#37424D"), alignment=1)))
    F.append(Spacer(1, 1.0*cm))
    F.append(table(["What you get on every page", "Why"],
      [["<b>Screenshot</b> of the original handwritten page",
        "Read the guide next to the notes, or entirely from the guide"],
       ["<b>Transcription</b> of the page’s content",
        "Handwriting made legible; abbreviations expanded"],
       ["<b>Explanation</b> of every concept, formula and diagram",
        "First-principles teaching, not just a restatement"],
       ["<b>Past-paper questions</b> on that topic, fully solved",
        "41 scans transcribed and solved, placed in sequence"]],
      widths=[2.0,1.2]))
    F.append(Spacer(1, 0.7*cm))
    F.append(callout("<b>How to use this guide.</b> Open the handwritten notes and this guide side by "
        "side. Read a page of the notes, then read the matching page here: the transcription tells you "
        "what the page says, and the explanation tells you what it means. When you reach a past-paper "
        "question, attempt it first and then check the full solution.", 'tip'))
    F.append(PageBreak())
    return F


def toc_page():
    F = []
    F.append(Paragraph("Contents", gen.S('toch', fontName="Head", fontSize=18, leading=22,
                                         textColor=NAVY, spaceAfter=8)))
    toc = TableOfContents()
    toc.levelStyles = [
        gen.S('t0', fontName="Head", fontSize=9.0, leading=12.6, textColor=NAVY,
              leftIndent=0, firstLineIndent=0),
    ]
    toc.dotsMinLevel = 0
    F.append(toc)
    F.append(PageBreak())
    return F


def build_story():
    story = []
    story += title_page()
    story += toc_page()

    for num in range(1, 88):
        pg = PAGES.get(num)
        if pg is None:
            continue
        story.append(PageBand(num, pg['title'], "notes"))
        story.append(Spacer(1, 3))
        story.append(screenshot(f"page{num:03d}.jpg", width=14.4,
                                caption=f"Original handwritten notes — page {num}."))
        story.append(Spacer(1, 5))
        story.append(Paragraph("Transcription of the page", ST['h4']))
        story += transcription(pg['transcript'])
        story.append(Paragraph("Explanation", ST['h4']))
        story += eval_units(pg['explain'])
        # attached previous-year questions
        for ca in pg['pyqs']:
            q = PYQS[ca]
            story.append(Spacer(1, 5))
            story.append(PageBand(0, f"Previous-year question {ca} — {q['title']}", "pyq"))
            story.append(Spacer(1, 3))
            story.append(ca_screenshot(f"ca{ca}.jpg", width=16.8,
                                       caption=f"Original past-paper scan ca{ca}.png (re-rendered)."))
            story.append(Spacer(1, 4))
            story.append(Paragraph("Transcription of the question", ST['h4']))
            story += transcription(q['transcript'])
            story.append(Paragraph("Full solution", ST['h4']))
            story += eval_units(q['explain'])
        story.append(PageBreak())

    # appendix: complete PYQ index + coverage table
    story += appendix()
    return story


def appendix():
    import pyqindex
    F = []
    F.append(PageBand(0, "Appendix A — Previous-year question index (all 41 scans)", "pyq"))
    F.append(Spacer(1, 3))
    F.append(p("Every scan ca1–ca41, the topics it examines, and the handwritten-notes page where its "
               "solution appears in this guide."))
    # map ca -> page number
    where = {}
    for num in range(1, 88):
        for ca in PAGES.get(num, {}).get('pyqs', []):
            where[ca] = num
    rows = [[f"<b>{ca}.png</b>", topics, what, f"p. {where.get(int(ca[2:]), '—')}"]
            for ca, topics, what in pyqindex.INDEX]
    F.append(table(["Paper", "Topic(s)", "What it asks", "Solved on"], rows,
                   widths=[0.75, 0.85, 4.1, 0.9]))
    F.append(Spacer(1, 8))

    F.append(PageBand(0, "Appendix B — Source coverage table (all 87 note pages)", "pyq"))
    F.append(Spacer(1, 3))
    F.append(p("One row per page of <b>Computer Architecture.pdf</b>, naming the topic and confirming "
               "that the page has a screenshot, a transcription and an explanation in this guide."))
    rows = [[str(pg), (PAGES[pg]['title'] if pg in PAGES else "—"),
             ("✓" if pg in PAGES else "—")] for pg in range(1, 88)]
    F.append(table(["Notes page", "Title in this guide", "Annotated?"], rows,
                   widths=[0.9, 5.0, 0.9]))
    F.append(Spacer(1, 8))

    F.append(PageBand(0, "Appendix C — Verification report", "pyq"))
    F.append(Spacer(1, 3))
    F.append(p("<b>1. Page coverage.</b> All 87 pages of the handwritten notes are accounted for. Pages "
               "1 (cover) and 67 (blank/illegible) carry no academic content and are labelled as such; "
               "the other 85 pages each have a screenshot, a transcription and a full explanation."))
    F.append(p("<b>2. Order.</b> The pages appear in the exact original sequence, page 1 → page 87, with "
               "no topic reordering. Recurrences are preserved (for example the cache-memory topic is "
               "revisited at the end of the notes and is annotated there, in that position)."))
    F.append(p("<b>3. Previous-year questions.</b> All 41 scans ca1–ca41 are transcribed and solved. A "
               "scan may contain several questions; each is identified and solved, and each is placed at "
               "the notes page whose topic it examines. Where a scan repeats an earlier one (ca19 "
               "repeats ca1; ca22 repeats ca1 Q2a) this is stated rather than silently duplicated."))
    F.append(p("<b>4. Figures and formulas.</b> Every diagram in the notes is retained as the original "
               "screenshot; the key ones are additionally reconstructed digitally (memory hierarchy, "
               "SIMD/MIMD, topologies, pipeline timing, branch-predictor state machines, Tomasulo "
               "datapath, cache address split, coherence states). Every formula is derived and every "
               "variable defined."))
    F.append(p("<b>5. Numerical checking.</b> All numerical answers were re-derived from the stated "
               "assumptions using the master formulas (CPU time = IC × CPI × T_clock; AMAT = hit time + "
               "miss rate × miss penalty; MTTF/MTBF/availability; Amdahl). Intermediate steps are shown."))
    F.append(p("<b>6. Honest limits.</b> The notes are handwritten and a few marginal annotations are "
               "only partly legible; where a reading affects a calculation it is stated explicitly. No "
               "question statement or numeric value has been invented to fill a gap."))
    return F


def main(out):
    story = build_story()
    gen.build_toc(out, story)
    import pymupdf
    d = pymupdf.open(out)
    print("BUILD OK", out)
    print("PAGES:", d.page_count)
    print("SIZE MB:", round(os.path.getsize(out)/1e6, 2))
    print("IMAGES:", sum(len(d[i].get_images()) for i in range(d.page_count)))


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ca/build/annotated.pdf"
    main(out)
