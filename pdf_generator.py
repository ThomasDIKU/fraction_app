from typing import List, Tuple

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.graphics.shapes import Drawing, Line, Circle, String


Fraction = Tuple[int, int]


# -------------------------------------------------
# Tegn tallinje for én brøk
# -------------------------------------------------
def number_line(num: int, den: int, width=5 * cm) -> Drawing:
    d = Drawing(width, 1.5 * cm)
    y = 0.8 * cm

    # Tallinje
    d.add(Line(0, y, width, y, strokeWidth=2))

    # Markering
    x = width * (num / den)
    d.add(Circle(x, y, 3, fillColor=colors.black))

    # Endepunkter
    d.add(Line(0, y - 4, 0, y + 4))
    d.add(Line(width, y - 4, width, y + 4))

    # Labels
    d.add(String(-4, y - 12, "0", fontSize=10))
    d.add(String(width - 6, y - 12, "1", fontSize=10))

    return d


# -------------------------------------------------
# Byg ét brøkkort
# -------------------------------------------------
def fraction_card(num: int, den: int, styles) -> Table:
    frac = Paragraph(
        f"<para align='center'><font size=22>{num}<br/>—<br/>{den}</font></para>",
        styles["Normal"]
    )

    nl = number_line(num, den)

    card = Table(
        [[frac], [nl]],
        colWidths=[5.5 * cm],
        rowHeights=[3.2 * cm, 2.5 * cm]
    )

    card.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    return card


# -------------------------------------------------
# Byg PDF
# -------------------------------------------------
def build_pdf(
    output_path: str,
    fractions: List[Fraction],
    cards_per_row: int = 3
):
    """
    Genererer en PDF med brøkkort.

    Parameters
    ----------
    output_path : hvor PDF'en gemmes
    fractions : liste af (n, d)
    cards_per_row : fast 3 i v1
    """

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
    )

    styles = getSampleStyleSheet()

    # Lav kort
    cards = [
        fraction_card(n, d, styles)
        for n, d in fractions
    ]

    # Pak i rækker
    table_data = []
    row = []

    for card in cards:
        row.append(card)
        if len(row) == cards_per_row:
            table_data.append(row)
            row = []

    if row:
        table_data.append(row)

    # Hovedtabel
    main_table = Table(
        table_data,
        colWidths=[6 * cm] * cards_per_row,
        repeatRows=0
    )

    main_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    doc.build([main_table])
