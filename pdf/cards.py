"""
Logik for ét brøkkort som en stak af repræsentationer.

Et kort = én brøk + 1..n repræsentationer
Alle repræsentationer behandles ens (symbol er også en repræsentation).
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
# Repræsentations-dispatch
# -------------------------------------------------
def _build_representation(rep: str, num: int, den: int, styles):
    if rep == "symbol":
        return Paragraph(
            f"<para align='center'><font size={FRACTION_FONT_SIZE}>{num}<br/>—<br/>{den}</font></para>",
            styles["Normal"]
        )

    if rep == "rectangle":
        return draw_rectangle_fraction(num, den)

    # default = numberline
    return draw_number_line(num, den)


# -------------------------------------------------
# Byg ét brøkkort
# -------------------------------------------------
def build_fraction_card(
    num: int,
    den: int,
    styles,
    representations: list[str] | None = None
) -> Table:
    """
    Bygger ét brøkkort for brøken num/den.

    representations:
        None  -> ["symbol", "numberline"]
        ["symbol"]
        ["numberline", "rectangle"]
        ["symbol", "numberline", "rectangle"]
    """

    if not representations:
        representations = ["symbol", "numberline"]

    visuals = [
        _build_representation(rep, num, den, styles)
        for rep in representations
    ]

    # -------------------------------------------------
    # Dynamisk layout
    # -------------------------------------------------
    row_count = len(visuals)

    # Symbol fylder lidt mindre end grafik
    weights = []
    for rep in representations:
        if rep == "symbol":
            weights.append(1)
        else:
            weights.append(2)

    total_weight = sum(weights)
    row_heights = [
        CARD_HEIGHT * (w / total_weight)
        for w in weights
    ]

    rows = [[v] for v in visuals]

    card = Table(
        rows,
        colWidths=[CARD_WIDTH],
        rowHeights=row_heights
    )

    card.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), CARD_BORDER_WIDTH, CARD_BORDER_COLOR),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 0.25 * cm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.25 * cm),
    ]))

    return card
