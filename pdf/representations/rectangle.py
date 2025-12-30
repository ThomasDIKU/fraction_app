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

    drawing = Drawing(width, height)

    cell_width = width / den

    for i in range(den):
        x = i * cell_width

        rect = Rect(
            x,
            0,
            cell_width,
            height,
            fillColor=fill_color if i < num else None,
            strokeColor=stroke_color,
            strokeWidth=1
        )

        drawing.add(rect)

    return drawing
