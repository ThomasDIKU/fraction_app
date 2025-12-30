"""
Layout- og designkonstanter for PDF-brøkkort.

Denne fil indeholder udelukkende:
- størrelser
- farver
- marginer
- visuelle standarder

Ingen logik og ingen PDF-generering her.
"""

from reportlab.lib import colors
from reportlab.lib.units import cm


# -------------------------------------------------
# Side-layout
# -------------------------------------------------
PAGE_MARGIN = 1.5 * cm


# -------------------------------------------------
# Kort-layout
# -------------------------------------------------
CARD_WIDTH = 5.5 * cm
CARD_HEIGHT = 5.7 * cm

CARD_PADDING = 0.3 * cm
CARDS_PER_ROW = 3


# -------------------------------------------------
# Typografi
# -------------------------------------------------
FRACTION_FONT_SIZE = 22
LABEL_FONT_SIZE = 10


# -------------------------------------------------
# Farver
# -------------------------------------------------
PRIMARY_COLOR = colors.black
SECONDARY_COLOR = colors.grey
ACCENT_COLOR = colors.HexColor("#1f77b4")  # diskret blå

CARD_BORDER_COLOR = colors.black
CARD_BORDER_WIDTH = 1


# -------------------------------------------------
# Tallinje
# -------------------------------------------------
NUMBERLINE_STROKE_WIDTH = 2
NUMBERLINE_MARK_RADIUS = 3
