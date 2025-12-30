from typing import List, Tuple

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet

from pdf.cards import build_fraction_card


Fraction = Tuple[int, int]


# -------------------------------------------------
# Byg PDF
# -------------------------------------------------
def build_pdf(
    output_path: str,
    fractions: List[Fraction],
    cards_per_row: int = 3,
    representations: list[str] | None = None
):
    """
    Genererer en PDF med brøkkort.

    representations:
        None -> ["symbol", "numberline"]
        ["symbol"]
        ["numberline", "rectangle"]
        ["symbol", "numberline", "rectangle"]
    """

    if not representations:
        representations = ["symbol", "numberline"]

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
    )

    styles = getSampleStyleSheet()

    # Byg kort
    cards = [
        build_fraction_card(
            n,
            d,
            styles,
            representations=representations
        )
        for n, d in fractions
    ]

    # Pak kort i rækker
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
