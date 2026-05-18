"""
pdf_generator.py
─────────────────
Generates a polished PDF:
  • Article pages  – reportlab Platypus
  • Visual Chart Overview page (last) – raw canvas, merged with pypdf
Charts included:
  ① Stat cards  (words / sections / sentences / read time)
  ② Article flow timeline
  ③ Horizontal bar chart (words per section)
  ④ Donut chart  (section distribution)
  ⑤ Key insights callout list
  ⑥ Supported-language grid
"""

import re, io, math, os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas
from pypdf import PdfWriter, PdfReader

# ── Palette ───────────────────────────────────────────────────────────────────
CYAN       = colors.HexColor("#00BCD4")
DARK_CYAN  = colors.HexColor("#00838F")
LIGHT_CYAN = colors.HexColor("#E0F7FA")
DARK_BG    = colors.HexColor("#0D1B2A")
BODY_TEXT  = colors.HexColor("#1A1A2E")
SUBTLE     = colors.HexColor("#546E7A")
WHITE      = colors.white
ACCENT     = colors.HexColor("#FF6F3C")
ACCENT2    = colors.HexColor("#7C4DFF")
ACCENT3    = colors.HexColor("#00E676")
PALE_GRAY  = colors.HexColor("#F5F7FA")
MID_GRAY   = colors.HexColor("#CFD8DC")
NAVY       = colors.HexColor("#060f1c")
STEEL      = colors.HexColor("#0a1628")
STEEL2     = colors.HexColor("#0e1f30")
MUTED_BLUE = colors.HexColor("#b0c4d8")
DIM_BLUE   = colors.HexColor("#7a9ab0")
SEP        = colors.HexColor("#1a2d3f")

CHART_COLORS = [
    colors.HexColor("#00BCD4"), colors.HexColor("#7C4DFF"),
    colors.HexColor("#FF6F3C"), colors.HexColor("#00E676"),
    colors.HexColor("#FFD740"), colors.HexColor("#FF4081"),
    colors.HexColor("#40C4FF"), colors.HexColor("#CCFF90"),
]


# ── Font helpers ──────────────────────────────────────────────────────────────
def register_unicode_fonts():
    candidates = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",      False),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", True),
        ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", False),
        ("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",    True),
        ("/usr/share/fonts/truetype/freefont/FreeSans.ttf",      False),
        ("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",  True),
        ("C:/Windows/Fonts/arial.ttf",   False),
        ("C:/Windows/Fonts/arialbd.ttf", True),
    ]
    reg = bold = False
    for path, is_bold in candidates:
        if not os.path.exists(path):
            continue
        try:
            if is_bold and not bold:
                pdfmetrics.registerFont(TTFont("UnicodeBold", path))
                bold = True
            elif not is_bold and not reg:
                pdfmetrics.registerFont(TTFont("Unicode", path))
                reg = True
        except Exception:
            continue
    return reg and bold


def get_styles(unicode_ok):
    base = "Unicode"     if unicode_ok else "Helvetica"
    bold = "UnicodeBold" if unicode_ok else "Helvetica-Bold"
    return {
        "h1":   ParagraphStyle("H1",   fontName=bold, fontSize=22, leading=28,
                               textColor=DARK_BG,   spaceAfter=8),
        "h2":   ParagraphStyle("H2",   fontName=bold, fontSize=14, leading=20,
                               textColor=DARK_CYAN, spaceAfter=4,  spaceBefore=14),
        "h3":   ParagraphStyle("H3",   fontName=bold, fontSize=12, leading=16,
                               textColor=BODY_TEXT, spaceAfter=4,  spaceBefore=10),
        "body": ParagraphStyle("Body", fontName=base, fontSize=11, leading=17,
                               textColor=BODY_TEXT, spaceAfter=6,  alignment=TA_JUSTIFY),
        "meta": ParagraphStyle("Meta", fontName=base, fontSize=9,  leading=13,
                               textColor=SUBTLE),
        "_base": base, "_bold": bold,
    }


# ── Article parsing helpers ───────────────────────────────────────────────────
def parse_article(text):
    segs = []
    for line in text.split("\n"):
        s = line.strip()
        if   not s:          segs.append(("space", ""))
        elif s.startswith("### "): segs.append(("h3", s[4:]))
        elif s.startswith("## "):  segs.append(("h2", s[3:]))
        elif s.startswith("# "):   segs.append(("h1", s[2:]))
        else:
            c = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
            c = re.sub(r"\*(.+?)\*",     r"<i>\1</i>", c)
            segs.append(("body", c))
    return segs


def extract_sections(article):
    sections, head, body = [], "Introduction", []
    for line in article.split("\n"):
        s = line.strip()
        if s.startswith("## ") or s.startswith("# "):
            if body: sections.append((head, " ".join(body)))
            head, body = re.sub(r"^#+\s*", "", s), []
        elif s and not s.startswith("#"):
            clean = re.sub(r"[*#]", "", s).strip()
            if clean: body.append(clean)
    if body: sections.append((head, " ".join(body)))
    return sections


def extract_key_sentences(article, n=5):
    result = []
    for s in re.split(r'(?<=[.!?])\s+', article):
        clean = re.sub(r'[#*]', '', s).strip()
        if 40 < len(clean) < 180:
            result.append(clean)
        if len(result) >= n: break
    return result


def _t(text, chars):
    return text[:chars] + ".." if len(text) > chars else text


# ── Header / footer for article pages ────────────────────────────────────────
def _art_hf(c, doc):
    c.saveState()
    w, h = A4
    c.setStrokeColor(CYAN);  c.setLineWidth(1.5)
    c.line(20*mm, h-18*mm, w-20*mm, h-18*mm)
    c.setFont("Helvetica", 8); c.setFillColor(SUBTLE)
    c.drawString(20*mm, h-14*mm, "YouTube -> Article & PDF")
    c.drawRightString(w-20*mm, h-14*mm, "Powered by Groq AI")
    c.setStrokeColor(MID_GRAY); c.setLineWidth(0.5)
    c.line(20*mm, 15*mm, w-20*mm, 15*mm)
    c.setFont("Helvetica", 8); c.setFillColor(SUBTLE)
    c.drawCentredString(w/2, 10*mm, f"Page {doc.page}")
    c.restoreState()


# ═══════════════════════════════════════════════════════════════════════════════
#  CHART PAGE – drawn directly on a raw reportlab canvas
# ═══════════════════════════════════════════════════════════════════════════════

def _draw_stat_cards(c, x, y, w, article, language, bf, bdf):
    secs     = extract_sections(article)
    words    = len(re.sub(r'[#*]', '', article).split())
    sents    = len(re.split(r'[.!?]+', article))
    read_min = max(1, round(words / 200))
    stats = [
        ("WORDS",     str(words),         CYAN),
        ("SECTIONS",  str(len(secs)),      ACCENT2),
        ("SENTENCES", str(sents),          ACCENT),
        ("READ TIME",f"{read_min} min",    ACCENT3),
    ]
    cw, ch = (w - 3*5) / 4, 36
    for i, (label, value, col) in enumerate(stats):
        cx = x + i*(cw+5)
        c.setFillColor(STEEL); c.setStrokeColor(col); c.setLineWidth(1.5)
        c.roundRect(cx, y, cw, ch, 4, fill=1, stroke=1)
        c.setFillColor(col);  c.setStrokeColor(colors.transparent)
        c.roundRect(cx, y+ch-5, cw, 5, 2, fill=1, stroke=0)
        c.setFillColor(WHITE); c.setFont(bdf, 13)
        c.drawCentredString(cx+cw/2, y+14, value)
        c.setFillColor(col);  c.setFont(bf, 6)
        c.drawCentredString(cx+cw/2, y+5,  label)


def _draw_timeline(c, x, y, w, sections, bf, bdf):
    h = 52
    c.setFillColor(STEEL); c.setStrokeColor(colors.transparent)
    c.roundRect(x, y, w, h, 5, fill=1, stroke=0)
    c.setFillColor(CYAN);  c.setFont(bdf, 8)
    c.drawString(x+10, y+h-13, "ARTICLE FLOW TIMELINE")

    tly, tx0, tx1 = y+20, x+18, x+w-18
    c.setStrokeColor(colors.HexColor("#1a3a4a")); c.setLineWidth(2)
    c.line(tx0, tly, tx1, tly)
    # arrow
    c.setFillColor(CYAN); c.setStrokeColor(CYAN)
    p = c.beginPath()
    p.moveTo(tx1, tly); p.lineTo(tx1-5, tly+4); p.lineTo(tx1-5, tly-4); p.close()
    c.drawPath(p, fill=1, stroke=0)

    n    = min(len(sections), 7)
    step = (tx1-tx0-10)/max(n-1,1) if n > 1 else 0
    for i in range(n):
        nx  = tx0 + i*step if n > 1 else (tx0+tx1)/2
        col = CHART_COLORS[i % len(CHART_COLORS)]
        c.setFillColor(col); c.setStrokeColor(WHITE); c.setLineWidth(1)
        c.circle(nx, tly, 5, fill=1, stroke=1)
        c.setFillColor(WHITE); c.setFont(bdf, 5.5)
        c.drawCentredString(nx, tly-2, str(i+1))
        c.setFillColor(MUTED_BLUE); c.setFont(bf, 5.5)
        c.drawCentredString(nx, tly-14, _t(sections[i][0], 11))


def _draw_bar_chart(c, x, y, w, h, sections, bf, bdf):
    c.setFillColor(PALE_GRAY); c.setStrokeColor(MID_GRAY); c.setLineWidth(0.5)
    c.roundRect(x, y, w, h, 4, fill=1, stroke=1)
    c.setFillColor(DARK_BG); c.setFont(bdf, 8)
    c.drawString(x+8, y+h-13, "WORD COUNT PER SECTION")
    c.setStrokeColor(CYAN); c.setLineWidth(1.5)
    c.line(x+8, y+h-16, x+105, y+h-16)

    n      = min(len(sections), 6)
    counts = [max(len(b.split()), 1) for _, b in sections[:n]]
    maxc   = max(counts)
    label_w = 52
    lw, bmax = label_w, w-label_w-26
    row_h  = (h-26) / max(n, 1)

    for i in range(n):
        ratio  = counts[i] / maxc
        by     = y + 10 + (n-1-i)*row_h + row_h*0.18
        bh     = row_h*0.58
        bx     = x+10+lw
        col    = CHART_COLORS[i % len(CHART_COLORS)]
        c.setFillColor(MID_GRAY); c.rect(bx, by, bmax, bh, fill=1, stroke=0)
        c.setFillColor(col)
        c.roundRect(bx, by, max(bmax*ratio, 4), bh, 2, fill=1, stroke=0)
        c.setFillColor(BODY_TEXT); c.setFont(bf, 7)
        c.drawRightString(bx-4, by+bh*0.28, _t(sections[i][0], 13))
        c.setFillColor(SUBTLE);  c.setFont(bf, 6)
        c.drawString(bx+max(bmax*ratio,4)+3, by+bh*0.28, f"{counts[i]}w")


def _draw_donut(c, cx, cy, r, sections, bf, bdf):
    n      = min(len(sections), 6)
    counts = [max(len(b.split()),1) for _,b in sections[:n]]
    total  = sum(counts)
    labels = [sections[i][0] for i in range(n)]

    angle = 90
    for i, cnt in enumerate(counts):
        sweep = 360*cnt/total
        c.setFillColor(CHART_COLORS[i%len(CHART_COLORS)])
        c.setStrokeColor(WHITE); c.setLineWidth(1.5)
        c.wedge(cx-r, cy-r, cx+r, cy+r, angle, sweep, fill=1, stroke=1)
        angle += sweep

    c.setFillColor(STEEL); c.setStrokeColor(colors.transparent)
    c.circle(cx, cy, r*0.48, fill=1, stroke=0)

    c.setFillColor(WHITE); c.setFont(bdf, 9)
    c.drawCentredString(cx, cy+4,  f"{total}")
    c.setFillColor(SUBTLE); c.setFont(bf, 6)
    c.drawCentredString(cx, cy-5, "words")

    c.setFillColor(WHITE); c.setFont(bdf, 8)
    c.drawCentredString(cx, cy+r+10, "SECTION DISTRIBUTION")

    lx, ly = cx-r, cy-r-14
    for i in range(n):
        c.setFillColor(CHART_COLORS[i%len(CHART_COLORS)])
        c.rect(lx, ly-i*11, 7, 7, fill=1, stroke=0)
        c.setFillColor(MUTED_BLUE); c.setFont(bf, 6)
        c.drawString(lx+10, ly-i*11+1, _t(labels[i], 18))


def _draw_key_insights(c, x, y, w, h, sentences, bf, bdf):
    c.setFillColor(ACCENT2); c.setFont(bdf, 8)
    c.drawString(x, y+h-12, "KEY INSIGHTS")
    c.setStrokeColor(ACCENT2); c.setLineWidth(2)
    c.line(x, y+h-15, x+68, y+h-15)

    n     = min(len(sentences), 5)
    row_h = (h-20) / max(n, 1)
    for i, sent in enumerate(sentences[:n]):
        ry  = y+h-22-i*row_h
        col = CHART_COLORS[i%len(CHART_COLORS)]
        c.setFillColor(col); c.rect(x, ry-row_h+8, 3, row_h-6, fill=1, stroke=0)
        c.setFillColor(col); c.setStrokeColor(colors.transparent)
        c.circle(x+12, ry-row_h/2+5, 7, fill=1, stroke=0)
        c.setFillColor(WHITE); c.setFont(bdf, 6.5)
        c.drawCentredString(x+12, ry-row_h/2+3, str(i+1))

        max_ch = int(w/4.0)
        wds    = sent.split()
        l1, l2, l1l = [], [], 0
        for wd in wds:
            if l1l+len(wd)+1 <= max_ch: l1.append(wd); l1l+=len(wd)+1
            else:                        l2.append(wd)
        line1 = " ".join(l1)
        line2 = " ".join(l2)
        if len(line2) > max_ch: line2 = line2[:max_ch-2]+"..."

        c.setFillColor(colors.HexColor("#d0e8f0")); c.setFont(bf, 7.5)
        c.drawString(x+23, ry-row_h/2+9, line1)
        if line2:
            c.setFillColor(SUBTLE); c.setFont(bf, 7)
            c.drawString(x+23, ry-row_h/2-1, line2)


def _draw_lang_grid(c, x, y, w, h, current_lang, bf, bdf):
    c.setFillColor(ACCENT); c.setFont(bdf, 8)
    c.drawString(x, y+h-12, "SUPPORTED LANGUAGES")
    c.setStrokeColor(ACCENT); c.setLineWidth(2)
    c.line(x, y+h-15, x+100, y+h-15)

    langs = ["English","Hindi","Spanish","French","German",
             "Portuguese","Arabic","Chinese","Japanese","Korean",
             "Italian","Russian","Turkish","Bengali","Marathi",
             "Tamil","Telugu","Gujarati","Punjabi","Dutch"]
    cols_n = 5
    rows   = math.ceil(len(langs)/cols_n)
    cw, ch = w/cols_n, (h-22)/rows
    sy     = y+h-22

    for i, lang in enumerate(langs):
        ci, ri = i%cols_n, i//cols_n
        lx, ly = x+ci*cw, sy-ri*ch-ch
        is_cur = (current_lang.lower().startswith(lang.lower())
                  or lang.lower() in current_lang.lower())
        if is_cur:
            c.setFillColor(CYAN); c.setStrokeColor(DARK_CYAN); c.setLineWidth(1)
            c.roundRect(lx+1, ly+1, cw-2, ch-2, 3, fill=1, stroke=1)
            c.setFillColor(DARK_BG); c.setFont(bdf, 6.5)
        else:
            c.setFillColor(STEEL2); c.setStrokeColor(colors.HexColor("#1a3a4a")); c.setLineWidth(0.5)
            c.roundRect(lx+1, ly+1, cw-2, ch-2, 3, fill=1, stroke=1)
            c.setFillColor(DIM_BLUE); c.setFont(bf, 6.5)
        c.drawCentredString(lx+cw/2, ly+ch/2-3, lang)


def _build_chart_page(article, video_title, language, bf, bdf):
    """Return bytes of a single-page PDF with the visual chart overview."""
    W, H = A4
    buf  = io.BytesIO()
    c    = rl_canvas.Canvas(buf, pagesize=A4)
    M    = 18*mm
    CW   = W - 2*M
    GAP  = 4*mm

    secs      = extract_sections(article)
    sentences = extract_key_sentences(article, 5)

    # ── Full background ───────────────────────────────────────────────────────
    c.setFillColor(DARK_BG); c.rect(0, 0, W, H, fill=1, stroke=0)

    # ── Header band ───────────────────────────────────────────────────────────
    HDR = 26*mm
    c.setFillColor(NAVY); c.rect(0, H-HDR, W, HDR, fill=1, stroke=0)
    c.setStrokeColor(CYAN); c.setLineWidth(3)
    c.line(0, H-HDR, W, H-HDR)

    c.setFillColor(WHITE); c.setFont(bdf, 15)
    c.drawString(M, H-13*mm, "Visual Overview & Cheatsheet")
    c.setFillColor(CYAN); c.setFont(bf, 8)
    c.drawString(M, H-20*mm, _t(video_title, 72))

    lang_short = language.split("(")[0].strip()
    bw = len(lang_short)*5.2+14
    c.setFillColor(CYAN); c.roundRect(W-M-bw, H-18*mm, bw, 11, 3, fill=1, stroke=0)
    c.setFillColor(DARK_BG); c.setFont(bdf, 7)
    c.drawCentredString(W-M-bw/2, H-13*mm, lang_short)

    top = H-HDR-4*mm

    # ROW 1 – stat cards
    STAT_H = 36
    _draw_stat_cards(c, M, top-STAT_H, CW, article, language, bf, bdf)
    top -= STAT_H+GAP

    # ROW 2 – timeline
    TL_H = 52
    _draw_timeline(c, M, top-TL_H, CW, secs, bf, bdf)
    top -= TL_H+GAP

    # ROW 3 – bar chart (left 58%) + donut (right 38%)
    R3H = 75*mm
    BW, DW, DGAP = CW*0.57, CW*0.38, CW*0.05
    _draw_bar_chart(c, M, top-R3H, BW, R3H, secs, bf, bdf)
    pie_cx = M+BW+DGAP+DW*0.38
    pie_cy = top-R3H/2
    pie_r  = min(DW, R3H)*0.26
    _draw_donut(c, pie_cx, pie_cy, pie_r, secs, bf, bdf)
    top -= R3H+GAP

    # ROW 4 – key insights (left 54%) + language grid (right 41%)
    R4H  = 65*mm
    KW   = CW*0.54
    LGW  = CW*0.41
    LGAP = CW*0.05
    _draw_key_insights(c, M, top-R4H, KW, R4H, sentences, bf, bdf)
    _draw_lang_grid(c, M+KW+LGAP, top-R4H, LGW, R4H, language, bf, bdf)

    # Footer
    c.setStrokeColor(SEP); c.setLineWidth(1)
    c.line(M, 12*mm, W-M, 12*mm)
    c.setFillColor(SUBTLE); c.setFont(bf, 7)
    c.drawCentredString(W/2, 8*mm,
        "Generated by YouTube -> Article & PDF   |   Powered by Groq AI (LLaMA-3.3-70B)")

    c.showPage()
    c.save()
    return buf.getvalue()


# ═══════════════════════════════════════════════════════════════════════════════
#  PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════════

def generate_pdf(article: str, video_title: str, language: str = "English") -> tuple[bytes, str | None]:
    try:
        unicode_ok = register_unicode_fonts()
        styles     = get_styles(unicode_ok)
        bf, bdf    = styles["_base"], styles["_bold"]

        # ── 1. Article pages ──────────────────────────────────────────────────
        art_buf = io.BytesIO()
        doc = SimpleDocTemplate(
            art_buf, pagesize=A4,
            leftMargin=20*mm, rightMargin=20*mm,
            topMargin=25*mm,  bottomMargin=22*mm,
        )
        story = []

        # Title block
        tt = Table([[Paragraph(video_title[:120], styles["h1"])]], colWidths=[170*mm])
        tt.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), LIGHT_CYAN),
            ("TOPPADDING",    (0,0),(-1,-1), 12),
            ("BOTTOMPADDING", (0,0),(-1,-1), 12),
            ("LEFTPADDING",   (0,0),(-1,-1), 14),
            ("RIGHTPADDING",  (0,0),(-1,-1), 14),
            ("LINEBELOW",     (0,0),(-1,-1), 3, CYAN),
        ]))
        story += [tt, Spacer(1, 6*mm)]

        mt = Table([[
            Paragraph(f"Language: {language}", styles["meta"]),
            Paragraph("AI-generated article",  styles["meta"]),
        ]], colWidths=[85*mm, 85*mm])
        mt.setStyle(TableStyle([("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
        story += [mt, HRFlowable(width="100%", thickness=0.5, color=MID_GRAY, spaceAfter=8)]

        for seg, content in parse_article(article):
            if   seg == "space": story.append(Spacer(1, 2*mm))
            elif seg == "h1":
                story += [Paragraph(content, styles["h1"]),
                          HRFlowable(width="40%", thickness=2,   color=CYAN,   spaceAfter=4)]
            elif seg == "h2":
                story += [Paragraph(content, styles["h2"]),
                          HRFlowable(width="25%", thickness=1.5, color=ACCENT, spaceAfter=4)]
            elif seg == "h3": story.append(Paragraph(content, styles["h3"]))
            else:             story.append(Paragraph(content, styles["body"]))

        doc.build(story, onFirstPage=_art_hf, onLaterPages=_art_hf)

        # ── 2. Chart overview page ─────────────────────────────────────────────
        chart_bytes = _build_chart_page(article, video_title, language, bf, bdf)

        # ── 3. Merge with pypdf ────────────────────────────────────────────────
        writer = PdfWriter()
        for reader in [PdfReader(art_buf), PdfReader(io.BytesIO(chart_bytes))]:
            for page in reader.pages:
                writer.add_page(page)

        out_buf = io.BytesIO()
        writer.write(out_buf)
        return out_buf.getvalue(), None

    except Exception as e:
        return b"", f"PDF generation error: {e}"