from reportlab.graphics.shapes import Drawing, Rect
from reportlab.lib import colors
from reportlab.lib.units import cm


def draw_rectangle_fraction(
    num: int,
    den: int,
    width: float = 5 * cm,
    height: float = 1.5 * cm,
    fill_color=colors.HexColor("#1f77b4"),
    stroke_color=colors.black
) -> Drawing:
    """
    Tegner en rektangel-arealmodel for brøken num/den.
    Rektanglet opdeles i 'den' lige store lodrette felter.
    'num' felter farves, alle felter har kontur.
    """

    drawing = Drawing(width, height)

    cell_width = width / den

    for i in range(den):
        x = i * cell_width

        # Farv tællerens dele
        if i < num:
            rect = Rect(
                x, 0,
                cell_width, height,
                fillColor=fill_color,
                strokeColor=stroke_color,
                strokeWidth=1
            )
        else:
            rect = Rect(
                x, 0,
                cell_width, height,
                fillColor=None,
                strokeColor=stroke_color,
                strokeWidth=1
            )

        drawing.add(rect)

    return drawing
