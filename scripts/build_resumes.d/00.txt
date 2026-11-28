#!/usr/bin/env python3
"""Build RU/EN resume PDFs with photo from HH.ru content."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage,
    KeepTogether, HRFlowable,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_JUSTIFY

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

CYAN = HexColor("#0a8fad")
DARK = HexColor("#1a1a22")
MUTED = HexColor("#5a5a6a")
TEXT = HexColor("#22222a")
LINE = HexColor("#d8dde6")

def find_photo():
    for p in ["photo-resume.jpg", "photo-avatar-240.png", "IMG_1447.jpeg", "IMG_1447.jpg"]:
        if Path(p).exists():
            return p
    cands = list(Path(".").glob("IMG_*.jpeg")) + list(Path(".").glob("IMG_*.jpg")) + list(Path(".").glob("IMG_*.png"))
    return str(cands[0]) if cands else None

def styles():
    return {
        "name": ParagraphStyle("name", fontName="DejaVuBold", fontSize=15, textColor=DARK, leading=18, spaceAfter=1),
        "role": ParagraphStyle("role", fontName="DejaVuBold", fontSize=10.5, textColor=CYAN, leading=13, spaceAfter=3),
        "meta": ParagraphStyle("meta", fontName="DejaVu", fontSize=8, textColor=MUTED, leading=10.5, spaceAfter=0.5),
        "h2": ParagraphStyle("h2", fontName="DejaVuBold", fontSize=10, textColor=CYAN, spaceBefore=8, spaceAfter=2, leading=12),
        "jt": ParagraphStyle("jt", fontName="DejaVuBold", fontSize=9, textColor=TEXT, leading=11, spaceAfter=0.5),
        "jm": ParagraphStyle("jm", fontName="DejaVu", fontSize=7.6, textColor=MUTED, leading=9.5, spaceAfter=1.5),
        "body": ParagraphStyle("body", fontName="DejaVu", fontSize=8, textColor=TEXT, leading=10.5, spaceAfter=1.5, alignment=TA_JUSTIFY),
        "b": ParagraphStyle("b", fontName="DejaVu", fontSize=7.8, textColor=TEXT, leading=10.2, leftIndent=4, spaceAfter=0.8),
        "sm": ParagraphStyle("sm", fontName="DejaVu", fontSize=7.6, textColor=TEXT, leading=9.8, spaceAfter=1),
    }

def header(s, photo, name, role, contacts, loc):
    img = RLImage(photo, width=26*mm, height=26*mm) if photo else Spacer(26*mm, 26*mm)
    right = [Paragraph(name, s["name"]), Paragraph(role, s["role"]), Paragraph(contacts, s["meta"]), Paragraph(loc, s["meta"])]
    t = Table([[img, right]], colWidths=[30*mm, 148*mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, 0), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t

def section(title, s):
    return [Paragraph(title, s["h2"]), HRFlowable(width="100%", thickness=0.8, color=LINE, spaceBefore=0, spaceAfter=3)]

def job(title, meta, intro, bullets, s):
    parts = [Paragraph(title, s["jt"]), Paragraph(meta, s["jm"])]
    if intro:
        parts.append(Paragraph(intro, s["body"]))
    for b in bullets:
        parts.append(Paragraph("• " + b, s["b"]))
    return KeepTogether(parts)

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DejaVu", 7)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(A4[0] / 2, 8 * mm, f"topdevops.pro  ·  page {doc.page}")
    canvas.restoreState()
