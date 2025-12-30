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
def draw_number_line(num: int, den: int, width=5 * cm) -> Drawing:
    drawing = Drawing(width, 1.5 * cm)
    y = 0.8 * cm

    # Selve tallinjen
    drawing.add(Line(0, y, width, y, strokeWidth=2))

    # Markér brøken
    x = width * (num / den)
    drawing.add(Circle(x, y, 3, fillColor=colors.black))

    # Endepunkter
    drawing.add(Line(0, y - 4, 0, y + 4))
    drawing.add(Line(width, y - 4, width, y + 4))

    # Labels
    drawing.add(String(-4, y - 12, "0", fontSize=10))
    drawing.add(String(width - 6, y - 12, "1", fontSize=10))

    return drawing


# -------------------------------------------------
# Byg ét brøkkort
# -------------------------------------------------
def build_fraction_card(num: int, den: int, styles) -> Table:
    fraction_text = Paragraph(
        f"<para align='center'><font size=22>{num}<br/>—<br/>{den}</font></para>",
        styles["Normal"]
    )

    number_line = draw_number_line(num, den)

    card = Table(
        [[fraction_text], [number_line]],
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
    output_path : str
        Hvor PDF'en gemmes
    fractions : List[(n, d)]
        Liste af brøker
    cards_per_row : int
        Antal kort pr. række (v1: 3)
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
        build_fraction_card(n, d, styles)
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

    main_table = Table(
        table_data,
        colWidths=[6 * cm] * cards_per_row
    )

    main_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    doc.build([main_table])
