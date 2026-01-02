"""
Logik for ét brøkkort som en stak af repræsentationer.

Et kort = én brøk + 1..n repræsentationer
Alle repræsentationer (symbol, tallinje, rektangel) behandles ens
og får eksplicit tildelt højde.
"""

from reportlab.platypus import Table, TableStyle, Paragraph, KeepInFrame
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
# Symbol-repræsentation (robust)
# -------------------------------------------------
def _build_symbol_representation(num: int, den: int, styles, height):
    """
    Bygger symbol-repræsentationen med kendt maks-højde.
    Kan aldrig overskride kortets ramme.
    """

    paragraph = Paragraph(
        f"<para align='center'><font size={FRACTION_FONT_SIZE}>{num}<br/>—<br/>{den}</font></para>",
        styles["Normal"]
    )

    frame = KeepInFrame(
        maxWidth=CARD_WIDTH,
        maxHeight=height,
        content=[paragraph],
        mode="shrink"   # skalerer tekst hvis nødvendigt
    )

    table = Table(
        [[frame]],
        colWidths=[CARD_WIDTH],
        rowHeights=[height]
    )

    table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 0.25 * cm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.25 * cm),
    ]))

    return table


# -------------------------------------------------
# Repræsentations-dispatch
# -------------------------------------------------
def _build_representation(rep: str, num: int, den: int, styles, height):
    if rep == "symbol":
        return _build_symbol_representation(num, den, styles, height)

    if rep == "rectangle":
        return draw_rectangle_fraction(num, den, height=height)

    # default = numberline
    return draw_number_line(num, den, height=height)


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
        None -> ["symbol", "numberline"]
        ["symbol"]
        ["numberline", "rectangle"]
        ["symbol", "numberline", "rectangle"]
        (rækkefølgen er fri)
    """

    if not representations:
        representations = ["symbol", "numberline"]

    # -------------------------------------------------
    # Beregn højde pr. repræsentation (vægte)
    # -------------------------------------------------
    weights = [
        1 if rep == "symbol" else 2
        for rep in representations
    ]

    total_weight = sum(weights)

    row_heights = [
        CARD_HEIGHT * (w / total_weight)
        for w in weights
    ]

    # -------------------------------------------------
    # Byg repræsentationer MED kendt højde
    # -------------------------------------------------
    visuals = [
        _build_representation(rep, num, den, styles, height)
        for rep, height in zip(representations, row_heights)
    ]

    rows = [[v] for v in visuals]

    # -------------------------------------------------
    # Kort-table
    # -------------------------------------------------
    card = Table(
        rows,
        colWidths=[CARD_WIDTH],
        rowHeights=row_heights
    )

    card.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), CARD_BORDER_WIDTH, CARD_BORDER_COLOR),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 0.15 * cm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.15 * cm),
    ]))

    return card
