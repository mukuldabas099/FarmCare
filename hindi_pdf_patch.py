"""
hindi_pdf_patch.py  (v2 — restructured paths)
==============================================
Registers NotoMerged fonts from the  fonts/  subfolder so that
ReportLab can render both English AND Hindi (Devanagari) in PDFs.

Font search order:
  1. <project_root>/fonts/NotoMerged-Regular.ttf   ← new location
  2. <project_root>/NotoMerged-Regular.ttf          ← old location (fallback)

If neither exists the caller falls back to plain Helvetica (no Hindi).
"""

import os
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib        import colors
from reportlab.pdfbase    import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Locate project root (this file lives there) ───────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))

# ── Font search paths (new folder first, then old root fallback) ──
def _find_font(filename: str) -> str | None:
    candidates = [
        os.path.join(_HERE, "fonts", filename),   # ← new location
        os.path.join(_HERE, filename),             # ← legacy root
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


_REGISTERED = False   # register only once per process


def register_hindi_fonts():
    """
    Call once at startup.  Safe to call multiple times — skips if already done.
    Raises RuntimeError if the merged font files are not found anywhere.
    """
    global _REGISTERED
    if _REGISTERED:
        return

    reg_path = _find_font("NotoMerged-Regular.ttf")
    bold_path = _find_font("NotoMerged-Bold.ttf")

    if not reg_path or not bold_path:
        missing = []
        if not reg_path:  missing.append("NotoMerged-Regular.ttf")
        if not bold_path: missing.append("NotoMerged-Bold.ttf")
        raise FileNotFoundError(
            f"[HindiFont] Missing merged font files: {missing}\n"
            f"  Run  python3 download_hindi_fonts.py  inside your project folder first.\n"
            f"  Expected location: {os.path.join(_HERE, 'fonts', 'NotoMerged-Regular.ttf')}"
        )

    pdfmetrics.registerFont(TTFont("NotoMerged",     reg_path))
    pdfmetrics.registerFont(TTFont("NotoMerged-Bold", bold_path))
    pdfmetrics.registerFontFamily(
        "NotoMerged",
        normal="NotoMerged",
        bold="NotoMerged-Bold",
        italic="NotoMerged",
        boldItalic="NotoMerged-Bold",
    )
    _REGISTERED = True
    print(f"[HindiFont] Registered NotoMerged from: {os.path.dirname(reg_path)}")


def get_pdf_fonts(lang: str = "en") -> dict:
    """
    Returns a dict of ReportLab ParagraphStyle objects.
    Uses NotoMerged (Hindi-capable) when lang=='hi', Helvetica otherwise.
    """
    CTX = colors.HexColor("#1a2e1a")
    CMT = colors.HexColor("#6b9a6b")
    CD  = colors.HexColor("#0d1f0d")
    CSC = colors.HexColor("#d4efd4")

    if lang == "hi":
        try:
            register_hindi_fonts()
            normal_font = "NotoMerged"
            bold_font   = "NotoMerged-Bold"
            italic_font = "NotoMerged"
        except (FileNotFoundError, Exception) as e:
            print(f"[HindiFont] WARNING — falling back to Helvetica: {e}")
            normal_font = "Helvetica"
            bold_font   = "Helvetica-Bold"
            italic_font = "Helvetica-Oblique"
    else:
        normal_font = "Helvetica"
        bold_font   = "Helvetica-Bold"
        italic_font = "Helvetica-Oblique"

    def ps(name, **kw):
        return ParagraphStyle(name, **kw)

    return {
        "body": ps("body",
                   fontName=normal_font, fontSize=9,
                   textColor=CTX, spaceAfter=3, leading=14),
        "bold": ps("bold",
                   fontName=bold_font, fontSize=9,
                   textColor=CTX),
        "sm":   ps("sm",
                   fontName=normal_font, fontSize=8,
                   textColor=CMT),
        "smi":  ps("smi",
                   fontName=italic_font, fontSize=7.5,
                   textColor=CMT, leading=11),
        "sec":  ps("sec",
                   fontName=bold_font, fontSize=11,
                   textColor=CD, backColor=CSC,
                   spaceAfter=4, spaceBefore=10,
                   leftIndent=6, borderPad=4),
    }