from reportlab.graphics.shapes import Drawing, Line, Circle, String
from reportlab.lib import colors
from reportlab.lib.units import cm


def draw_number_line(num: int, den: int, width=5 * cm) -> Drawing:
    drawing = Drawing(width, 1.5 * cm)
    y = 0.8 * cm

    # Tallinje
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
