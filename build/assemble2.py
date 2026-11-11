"""Assemble the notes-order Computer Architecture study guide."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen
from gen import (h1,h2,h3,h4,p,bullets,formula,callout,table,fig,Spacer,PageBreak,
                 Paragraph,ST,NAVY,AMBER,AMBERB,LIGHT,GREY,RULE,CW,PW,PH,LM,RM,TM,BM)
from reportlab.platypus import Table, TableStyle, Flowable, KeepTogether
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus.tableofcontents import TableOfContents
import gen2


def title_page():
    F = []
    F.append(Spacer(1, 3.0*cm))
    F.append(Paragraph("Computer Architecture",
        gen.S('tp', fontName="Head", fontSize=34, leading=38, textColor=NAVY, alignment=1)))
    F.append(Spacer(1, 0.25*cm))
    F.append(Paragraph("Exam Study Guide — in the order of the lecture notes",
        gen.S('tp2', fontName="Head-Reg", fontSize=17, leading=22, textColor=colors.HexColor("#2E6DA4"), alignment=1)))
    F.append(Spacer(1, 0.7*cm))
    F.append(Paragraph("A complete, expanded and fully solved version of the lecturer’s handwritten notes. "
        "The sections follow the notes page by page — foundations, performance and Amdahl, ISA and "
        "RISC/CISC, dependability, pipelining, loop unrolling, branch prediction, scoreboarding and "
        "Tomasulo, speculation and the reorder buffer, multiprocessors, cache memory, virtual memory, "
        "cache coherence, and vector/SIMD/GPU architectures — with every previous-year question solved "
        "step by step.",
        gen.S('tp3', fontSize=10.5, leading=14.5, textColor=colors.HexColor("#37424D"), alignment=1)))
    F.append(Spacer(1, 1.1*cm))
    F.append(table(["Source materials analysed", "Coverage"],
      [["<b>Computer Architecture.pdf</b> — 87 handwritten pages", "Every topic, formula, diagram and worked example, in notes order"],
       ["<b>ca1.png … ca41.png</b> — 41 scanned past-paper questions", "100% of questions solved, with full reasoning"]],
      widths=[1.6, 1.6]))
    F.append(Spacer(1, 0.8*cm))
    F.append(callout("<b>How to use this guide.</b> It is organised to match the handwritten notes exactly, "
        "so you can read it alongside them. Each section teaches the concept from scratch, gives the "
        "formulas with every variable explained, explains the diagrams, and then solves the past-paper "
        "questions on that topic. The grey caption under each section banner tells you which note pages it "
        "corresponds to, and the coverage table at the end proves that every page is accounted for.", 'tip'))
    F.append(PageBreak())
    return F


def toc_page():
    F = []
    F.append(Paragraph("Contents", gen.S('toch', fontName="Head", fontSize=18, leading=22, textColor=NAVY, spaceAfter=8)))
    toc = TableOfContents()
    toc.levelStyles = [
        gen.S('t0', fontName="Head", fontSize=10.4, leading=15.4, textColor=NAVY, leftIndent=0, firstLineIndent=0),
    ]
    toc.dotsMinLevel = 0
    F.append(toc)
    F.append(PageBreak())
    return F


def main(out):
    story = []
    story += title_page()
    story += toc_page()
    story += gen2.build()
    gen.build_toc(out, story)
    import pymupdf
    d = pymupdf.open(out)
    print("BUILD OK", out)
    print("PAGES:", d.page_count)
    print("SIZE MB:", round(os.path.getsize(out)/1e6, 2))
    print("IMAGES:", sum(len(d[i].get_images()) for i in range(d.page_count)))


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/ca/build/out.pdf"
    main(out)
