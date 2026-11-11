"""Annotated, page-by-page study guide generator.

Layout per handwritten page:
    [ header: "Original notes - page N: <title>" ]
    [ screenshot of the handwritten page ]
    [ transcription of the page ]
    [ detailed explanation / derivation / reconstructed diagram ]
    [ any previous-year questions that belong to this page + full solutions ]
"""
import os, re, textwrap
import gen
from gen import (h1,h2,h3,h4,p,bullets,formula,callout,table,fig,Spacer,PageBreak,
                 Paragraph,ST,NAVY,AMBER,AMBERB,LIGHT,GREY,RULE,CW,PW,PH,LM,RM,TM,BM)
from reportlab.platypus import (Table, TableStyle, Flowable, KeepTogether, Image,
                                CondPageBreak)
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES_IMG = "/tmp/ca/embed"     # pageNNN.jpg  (screenshots of the notes)
CA_IMG = "/tmp/ca/embed"        # caN.jpg

_NS = {'gen': gen, 'h1':h1,'h2':h2,'h3':h3,'h4':h4,'p':p,'bullets':bullets,
       'formula':formula,'callout':callout,'table':table,'fig':fig,'Spacer':Spacer,
       'PageBreak':PageBreak,'Paragraph':Paragraph,'ST':ST}

def eval_units(src):
    """Compile a snippet of A(...) source and return the flowables it builds."""
    code = "def _e(A):\n" + textwrap.indent(src, '    ')
    ns = dict(_NS)
    exec(code, ns)
    out = []
    ns['_e'](lambda x: out.extend(x if isinstance(x,list) else [x]))
    return out


# ---------------------------------------------------------------- page header
class PageBand(Flowable):
    """Band heading for one handwritten page."""
    def __init__(self, num, title, kind="notes"):
        Flowable.__init__(self)
        self.num = num; self.title = title; self.kind = kind
        self._toc = (0, (f"Page {num} — {title}" if kind == "notes" else title))
    def wrap(self, aw, ah):
        self.width = aw; self.height = 1.05*cm
        return aw, self.height
    def draw(self):
        c = self.canv
        col = NAVY if self.kind == "notes" else colors.HexColor("#5B3A8E")
        c.setFillColor(col)
        c.roundRect(0, 0, self.width, self.height, 3, stroke=0, fill=1)
        c.setFillColor(AMBERB)
        c.rect(0, 0, 0.22*cm, self.height, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Head", 11.6)
        label = (f"Original notes — page {self.num}:  {self.title}" if self.kind=="notes"
                 else f"{self.title}")
        avail = self.width - 0.9*cm
        while label and pdfmetrics.stringWidth(label, "Head", 11.6) > avail:
            label = label[:-1]
        if label and not label.endswith(self.title) and len(label) < len(f"Original notes — page {self.num}:  {self.title}"):
            label = label[:-1] + "…"
        c.drawString(0.5*cm, self.height-0.70*cm, label)

def page_header(num, title):
    return KeepTogether([PageBand(num, title, "notes"), Spacer(1, 4)])

def pyq_header(title):
    return KeepTogether([PageBand(0, title, "pyq"), Spacer(1, 4)])


# ---------------------------------------------------------------- screenshot
def screenshot(png, width=13.2, caption=None):
    path = os.path.join(NOTES_IMG, png)
    from PIL import Image as PILImage
    iw, ih = PILImage.open(path).size
    w = width*cm; h = w*ih/iw
    img = Image(path, width=w, height=h)
    if caption:
        cap = Paragraph(caption, ST['cap'])
        return KeepTogether([img, Spacer(1, 2), cap])
    return img

def ca_screenshot(png, width=15.0, caption=None):
    path = os.path.join(CA_IMG, png)
    from PIL import Image as PILImage
    iw, ih = PILImage.open(path).size
    w = width*cm; h = w*ih/iw
    img = Image(path, width=w, height=h)
    if caption:
        return KeepTogether([img, Spacer(1, 2), Paragraph(caption, ST['cap'])])
    return img


# ---------------------------------------------------------------- transcription
class Transcript(Flowable):
    """A light box holding the cleaned-up transcription of a page."""
    def __init__(self, lines, width=None, font="Mono", size=7.4, leading=9.2):
        Flowable.__init__(self)
        self.lines = lines; self.font = font; self.size = size; self.leading = leading
        self._w = width
    def wrap(self, aw, ah):
        self.width = self._w or aw
        self.height = len(self.lines)*self.leading + 0.5*cm
        return self.width, self.height
    def draw(self):
        c = self.canv
        c.setFillColor(colors.HexColor("#F4F6F8"))
        c.setStrokeColor(colors.HexColor("#D7DEE5"))
        c.roundRect(0, 0, self.width, self.height, 3, stroke=1, fill=1)
        c.setFillColor(colors.HexColor("#33414D"))
        c.setFont(self.font, self.size)
        y = self.height - 0.34*cm
        for ln in self.lines:
            c.drawString(0.28*cm, y, ln)
            y -= self.leading

def transcription(text):
    lines = text.split("\n")
    return [Spacer(1, 3), Transcript(lines), Spacer(1, 3)]
