from reportlab.graphics.shapes import Drawing, Rect
from reportlab.lib import colors
from reportlab.lib.units import cm


def draw_rectangle_fraction(
    num: int,
    den: int,
    width: float = 5 * cm,
    height: float | None = None,
    fill_color=colors.HexColor("#1f77b4"),
    stroke_color=colors.black
) -> Drawing:
    """
    Tegner en adaptiv rektangel-arealmodel for brøken num/den.

    Rektanglet opdeles i 'den' lige store lodrette felter.
    'num' felter farves, alle felter har kontur.
    """

    if height is None:
        height = 1.5 * cm

    MAX_RECT_HEIGHT = 2.2 * cm
    rect_height = min(height, MAX_RECT_HEIGHT)

    drawing = Drawing(width, rect_height)

    cell_width = width / den

    for i in range(den):
        rect = Rect(
            i * cell_width,
            0,
            cell_width,
            rect_height,
            fillColor=fill_color if i < num else None,
            strokeColor=stroke_color,
            strokeWidth=1
        )
        drawing.add(rect)

    return drawing
