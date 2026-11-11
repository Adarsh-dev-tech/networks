"""Shared ReportLab setup + flowable helpers for the Computer Architecture guide."""
import os, json
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, Image, KeepTogether,
                                PageBreak, Flowable, CondPageBreak)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FDIR = "/usr/share/fonts/truetype/liberation"
DDIR = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("Body", f"{FDIR}/LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Body-Bold", f"{FDIR}/LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Body-Italic", f"{FDIR}/LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Body-BoldItalic", f"{FDIR}/LiberationSerif-BoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("Head", f"{FDIR}/LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Head-Reg", f"{FDIR}/LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Mono", f"{FDIR}/LiberationMono-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Mono-Bold", f"{FDIR}/LiberationMono-Bold.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("Body", normal="Body", bold="Body-Bold", italic="Body-Italic",
                   boldItalic="Body-BoldItalic")

# ---- palette (same as the Computer Networks guide) ----
NAVY   = colors.HexColor("#1A3A5C")
BLUE   = colors.HexColor("#2E6DA4")
AMBER  = colors.HexColor("#FFF3D6")
AMBERB = colors.HexColor("#E0A800")
LIGHT  = colors.HexColor("#EEF3F8")
GREY   = colors.HexColor("#5A6672")
GREEN  = colors.HexColor("#1E7B4D")
GREENBG= colors.HexColor("#E8F5EE")
RED    = colors.HexColor("#B23A3A")
REDBG  = colors.HexColor("#FBEAEA")
RULE   = colors.HexColor("#C7D2DC")

PW, PH = A4
LM = RM = 1.4*cm
TM = 1.5*cm
BM = 1.4*cm
CW = PW - LM - RM   # content width

def S(name, **kw):
    base = dict(fontName="Body", fontSize=9.2, leading=12.4, textColor=colors.HexColor("#1B1B1B"),
                alignment=TA_LEFT, spaceBefore=0, spaceAfter=0)
    base.update(kw)
    return ParagraphStyle(name, **base)

ST = {
 'h1':   S('h1', fontName="Head", fontSize=17, leading=20, textColor=colors.white, spaceAfter=2),
 'h1sub':S('h1sub', fontName="Head-Reg", fontSize=9.5, leading=12, textColor=colors.HexColor("#D6E2EE")),
 'h2':   S('h2', fontName="Head", fontSize=12.6, leading=15.5, textColor=NAVY, spaceBefore=7, spaceAfter=3.5),
 'h3':   S('h3', fontName="Head", fontSize=10.6, leading=13, textColor=BLUE, spaceBefore=5, spaceAfter=2.5),
 'h4':   S('h4', fontName="Head", fontSize=9.6, leading=12, textColor=colors.HexColor("#37424D"), spaceBefore=4, spaceAfter=2),
 'body': S('body', spaceAfter=3.5, alignment=TA_JUSTIFY),
 'bul':  S('bul', leftIndent=11, bulletIndent=2.5, spaceAfter=1.7, alignment=TA_JUSTIFY),
 'bul2': S('bul2', leftIndent=22, bulletIndent=13, spaceAfter=1.4, fontSize=8.9, leading=11.8),
 'cap':  S('cap', fontName="Head-Reg", fontSize=7.7, leading=9.6, textColor=GREY, alignment=TA_CENTER, spaceBefore=1.5),
 'form': S('form', fontName="Mono", fontSize=9.0, leading=12.6, textColor=colors.HexColor("#5A3E00")),
 'tblh': S('tblh', fontName="Head", fontSize=8.2, leading=10, textColor=colors.white),
 'tbl':  S('tbl', fontSize=8.2, leading=10.3),
 'tblb': S('tblb', fontName="Body-Bold", fontSize=8.2, leading=10.3),
 'q':    S('q', fontName="Head", fontSize=10.2, leading=12.8, textColor=colors.HexColor("#7A1F1F"), spaceBefore=4, spaceAfter=2),
 'ans':  S('ans', fontName="Head", fontSize=9.4, leading=11.8, textColor=GREEN, spaceBefore=3, spaceAfter=2),
 'toc':  S('toc', fontSize=9.3, leading=12.4),
}

FIGDIR = "/tmp/ca/figs"
def fig(name, w=None, cap=None):
    """Return a flowable image scaled to width w (cm) or default half-width, with caption."""
    path = f"{FIGDIR}/{name}"
    from PIL import Image as PILImage
    iw, ih = PILImage.open(path).size
    ar = ih/iw
    if w is None: w = CW
    wpt = w if isinstance(w,(int,float)) and w>50 else w*cm
    hpt = wpt*ar
    maxh = 12.5*cm
    if hpt > maxh:
        hpt = maxh; wpt = hpt/ar
    im = Image(path, width=wpt, height=hpt)
    im.hAlign = 'CENTER'
    if cap:
        return KeepTogether([im, Paragraph(cap, ST['cap'])])
    return im

def formula(text, label=None):
    """Amber formula box."""
    p = Paragraph(text, ST['form'])
    if label:
        p = Paragraph(f"<b>{label}</b>  " + text, ST['form'])
    t = Table([[p]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),AMBER),
        ('BOX',(0,0),(-1,-1),0.8,AMBERB),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ]))
    return KeepTogether([Spacer(1,2.5), t, Spacer(1,3.5)])

def callout(text, kind='info'):
    bg, bd = (LIGHT, BLUE) if kind=='info' else ((GREENBG, GREEN) if kind=='tip' else (REDBG, RED))
    p = Paragraph(text, S('co', fontSize=8.8, leading=11.6))
    t = Table([[p]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),
        ('LINEBEFORE',(0,0),(0,-1),2.4,bd),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ]))
    return KeepTogether([Spacer(1,2), t, Spacer(1,3)])

def bullets(items, style='bul'):
    return [Paragraph(x, ST[style], bulletText='•') if not x.startswith('~')
            else Paragraph(x[1:], ST[style], bulletText='–') for x in items]

def table(header, rows, widths=None, hdr_bg=NAVY):
    data=[]
    if header:
        data.append([Paragraph(h, ST['tblh']) for h in header])
    for r in rows:
        data.append([c if isinstance(c,Flowable) else Paragraph(str(c), ST['tbl']) for c in r])
    if widths is None:
        n=len(header) if header else len(rows[0])
        widths=[CW/n]*n
    else:
        tot=sum(widths)
        widths=[w/tot*CW for w in widths]
    t=Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st=[('GRID',(0,0),(-1,-1),0.4,RULE),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),
        ('TOPPADDING',(0,0),(-1,-1),2.6),('BOTTOMPADDING',(0,0),(-1,-1),2.6)]
    if header:
        st += [('BACKGROUND',(0,0),(-1,0),hdr_bg),
               ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, LIGHT])]
    else:
        st += [('ROWBACKGROUNDS',(0,0),(-1,-1),[colors.white, LIGHT])]
    t.setStyle(TableStyle(st))
    return t

class Banner(Flowable):
    """Full-width section banner."""
    def __init__(self, num, title, subtitle=None, h=1.55*cm):
        Flowable.__init__(self)
        self.num=num; self.title=title; self.subtitle=subtitle; self.h=h
        self._toc=(0, f"{num}.  {title}")
        self._toc=(0, f"{num}.  {title}")
        self._toc=(0, f"{num}.  {title}")
    def wrap(self, aw, ah):
        self.width=aw; return aw, self.h
    def draw(self):
        c=self.canv
        c.setFillColor(NAVY)
        c.roundRect(0,0,self.width,self.h,4,stroke=0,fill=1)
        c.setFillColor(AMBERB)
        c.rect(0,0,0.28*cm,self.h,stroke=0,fill=1)
        c.setFillColor(colors.white)
        c.setFont("Head",15.5)
        c.drawString(0.62*cm, self.h-0.72*cm, f"{self.num}.  {self.title}")
        if self.subtitle:
            c.setFont("Head-Reg",8.2); c.setFillColor(colors.HexColor("#CFDCEA"))
            c.drawString(0.62*cm, 0.28*cm, self.subtitle)

def h1(num,title,subtitle=None):
    return KeepTogether([Banner(num,title,subtitle), Spacer(1,6)])
def h2(t): return Paragraph(t, ST['h2'])
def h3(t): return Paragraph(t, ST['h3'])
def h4(t): return Paragraph(t, ST['h4'])
def p(t):  return Paragraph(t, ST['body'])

def make_doc(path, toc_pages=2):
    def deco(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(RULE); canvas.setLineWidth(0.5)
        canvas.line(LM, BM-0.35*cm, PW-RM, BM-0.35*cm)
        canvas.setFont("Head-Reg",7.4); canvas.setFillColor(GREY)
        canvas.drawString(LM, BM-0.72*cm, "Computer Architecture — Exam Study Guide")
        canvas.drawRightString(PW-RM, BM-0.72*cm, f"Page {doc.page}")
        canvas.restoreState()
    doc = BaseDocTemplate(path, pagesize=A4, leftMargin=LM, rightMargin=RM,
                          topMargin=TM, bottomMargin=BM,
                          title="Computer Architecture — Exam Study Guide",
                          author="Study Guide")
    frame = Frame(LM, BM, CW, PH-TM-BM, id='main', leftPadding=0, rightPadding=0,
                  topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id='main', frames=[frame], onPage=deco)])
    return doc

def build(path, story):
    doc = make_doc(path)
    doc.build(story)
    return path


from reportlab.platypus.tableofcontents import TableOfContents

class TocDocTemplate(BaseDocTemplate):
    def __init__(self, path, **kw):
        BaseDocTemplate.__init__(self, path, **kw)
        self._toc_entries = []
    def afterFlowable(self, flowable):
        toc = getattr(flowable, '_toc', None)
        if toc is not None:
            level, text = toc
            self.notify('TOCEntry', (level, text, self.page))

def make_doc2(path):
    def deco(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(RULE); canvas.setLineWidth(0.5)
        canvas.line(LM, BM-0.35*cm, PW-RM, BM-0.35*cm)
        canvas.setFont("Head-Reg",7.4); canvas.setFillColor(GREY)
        canvas.drawString(LM, BM-0.72*cm, "Computer Architecture — Exam Study Guide")
        canvas.drawRightString(PW-RM, BM-0.72*cm, f"Page {doc.page}")
        canvas.restoreState()
    doc = TocDocTemplate(path, pagesize=A4, leftMargin=LM, rightMargin=RM,
                         topMargin=TM, bottomMargin=BM,
                         title="Computer Architecture — Exam Study Guide",
                         author="Study Guide")
    frame = Frame(LM, BM, CW, PH-TM-BM, id='main', leftPadding=0, rightPadding=0,
                  topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id='main', frames=[frame], onPage=deco)])
    return doc

def build_toc(path, story):
    doc = make_doc2(path)
    doc.multiBuild(story)
    return path



from reportlab.platypus.tableofcontents import TableOfContents

class TocDocTemplate(BaseDocTemplate):
    def __init__(self, path, **kw):
        BaseDocTemplate.__init__(self, path, **kw)
        self._toc_entries = []
    def afterFlowable(self, flowable):
        toc = getattr(flowable, '_toc', None)
        if toc is not None:
            level, text = toc
            self.notify('TOCEntry', (level, text, self.page))

def make_doc2(path):
    def deco(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(RULE); canvas.setLineWidth(0.5)
        canvas.line(LM, BM-0.35*cm, PW-RM, BM-0.35*cm)
        canvas.setFont("Head-Reg",7.4); canvas.setFillColor(GREY)
        canvas.drawString(LM, BM-0.72*cm, "Computer Architecture — Exam Study Guide")
        canvas.drawRightString(PW-RM, BM-0.72*cm, f"Page {doc.page}")
        canvas.restoreState()
    doc = TocDocTemplate(path, pagesize=A4, leftMargin=LM, rightMargin=RM,
                         topMargin=TM, bottomMargin=BM,
                         title="Computer Architecture — Exam Study Guide",
                         author="Study Guide")
    frame = Frame(LM, BM, CW, PH-TM-BM, id='main', leftPadding=0, rightPadding=0,
                  topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id='main', frames=[frame], onPage=deco)])
    return doc

def build_toc(path, story):
    doc = make_doc2(path)
    doc.multiBuild(story)
    return path



from reportlab.platypus.tableofcontents import TableOfContents

class TocDocTemplate(BaseDocTemplate):
    def __init__(self, path, **kw):
        BaseDocTemplate.__init__(self, path, **kw)
        self._toc_entries = []
    def afterFlowable(self, flowable):
        toc = getattr(flowable, '_toc', None)
        if toc is not None:
            level, text = toc
            self.notify('TOCEntry', (level, text, self.page))

def make_doc2(path):
    def deco(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(RULE); canvas.setLineWidth(0.5)
        canvas.line(LM, BM-0.35*cm, PW-RM, BM-0.35*cm)
        canvas.setFont("Head-Reg",7.4); canvas.setFillColor(GREY)
        canvas.drawString(LM, BM-0.72*cm, "Computer Architecture — Exam Study Guide")
        canvas.drawRightString(PW-RM, BM-0.72*cm, f"Page {doc.page}")
        canvas.restoreState()
    doc = TocDocTemplate(path, pagesize=A4, leftMargin=LM, rightMargin=RM,
                         topMargin=TM, bottomMargin=BM,
                         title="Computer Architecture — Exam Study Guide",
                         author="Study Guide")
    frame = Frame(LM, BM, CW, PH-TM-BM, id='main', leftPadding=0, rightPadding=0,
                  topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id='main', frames=[frame], onPage=deco)])
    return doc

def build_toc(path, story):
    doc = make_doc2(path)
    doc.multiBuild(story)
    return path
