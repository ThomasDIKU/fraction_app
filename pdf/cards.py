"""
Logik for ét brøkkort.
"""

from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.units import cm

from pdf.templates import (
    CARD_WIDTH,
    CARD_HEIGHT,
    CARD_BORDER_COLOR,
    CARD_BORDER_WIDTH,
    FRACTION_FONT_SIZE,
)

from pdf.representations.numberline import draw_number_line
from pdf.representations.rectangle import draw_rectangle_fraction


# -------------------------------------------------
# Byg ét brøkkort
# -------------------------------------------------
def build_fraction_card(
    num: int,
    den: int,
    styles,
    representation: str = "numberline"
) -> Table:
    """
    Bygger ét brøkkort for brøken num/den.

    representation:
        - "numberline" (default)
        - "rectangle"
    """

    fraction_text = Paragraph(
        f"<para align='center'><font size={FRACTION_FONT_SIZE}>{num}<br/>—<br/>{den}</font></para>",
        styles["Normal"]
    )

    # Vælg repræsentation
    if representation == "rectangle":
        visual = draw_rectangle_fraction(num, den)
    else:
        visual = draw_number_line(num, den)

    # Proportioner
    fraction_height = CARD_HEIGHT * 0.6
    visual_height = CARD_HEIGHT * 0.4

    card = Table(
        [[fraction_text], [visual]],
        colWidths=[CARD_WIDTH],
        rowHeights=[fraction_height, visual_height]
    )

    card.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), CARD_BORDER_WIDTH, CARD_BORDER_COLOR),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 0.3 * cm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.3 * cm),
    ]))

    return card
