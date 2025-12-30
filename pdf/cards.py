"""
Logik for ét brøkkort.

Et kort repræsenterer:
- én brøk
- én eller flere visuelle repræsentationer (senere)

Denne fil indeholder KUN:
- sammensætning af kortets elementer
- ingen PDF-dokumentlogik
"""

from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.units import cm

from pdf.templates import (
    CARD_WIDTH,
    CARD_HEIGHT,
    CARD_BORDER_COLOR,
    CARD_BORDER_WIDTH,
)

# Midlertidig import (flyttes senere)
from pdf.generator import draw_number_line


# -------------------------------------------------
# Byg ét brøkkort
# -------------------------------------------------
def build_fraction_card(num: int, den: int, styles) -> Table:
    """
    Bygger ét brøkkort for brøken num/den.

    Returnerer et ReportLab Table-objekt.
    """

    fraction_text = Paragraph(
        f"<para align='center'><font size=22>{num}<br/>—<br/>{den}</font></para>",
        styles["Normal"]
    )

    number_line = draw_number_line(num, den)

    card = Table(
        [[fraction_text], [number_line]],
        colWidths=[CARD_WIDTH],
        rowHeights=[CARD_HEIGHT * 0.55, CARD_HEIGHT * 0.45]
    )

    card.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), CARD_BORDER_WIDTH, CARD_BORDER_COLOR),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    return card
