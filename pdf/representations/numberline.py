from reportlab.graphics.shapes import Drawing, Line, Circle, String
from reportlab.lib import colors
from reportlab.lib.units import cm


def draw_numberline(
    numerator: int,
    denominator: int,
    *,
    width: float = 5 * cm,
    height: float = 1.6 * cm,
    show_divisions: bool = True,
    show_marker: bool = True
) -> Drawing:
    """
    Tegner en tallinje fra 0 til 1 med valgfri inddeling og markering.
    """

    d = Drawing(width, height)

    # Baseline
    y = height / 2
    margin = 0.4 * cm
    x_start = margin
    x_end = width - margin

    line_color = colors.darkgray

    # Hovedlinje
    d.add(Line(
        x_start, y,
        x_end, y,
        strokeWidth=1.5,
        strokeColor=line_color
    ))

    # Endemarkeringer
    end_height = 6
    d.add(Line(x_start, y - end_height, x_start, y + end_height, strokeColor=line_color))
    d.add(Line(x_end, y - end_height, x_end, y + end_height, strokeColor=line_color))

    # Inddelingsstreger (nævner)
    if show_divisions and denominator > 1:
        step = (x_end - x_start) / denominator
        tick_height = 4

        for i in range(1, denominator):
            x = x_start + i * step
            d.add(Line(
                x, y - tick_height,
                x, y + tick_height,
                strokeWidth=1,
                strokeColor=line_color
            ))

    # Markering (prik)
    if show_marker:
        pos = numerator / denominator
        x_marker = x_start + pos * (x_end - x_start)

        d.add(Circle(
            x_marker,
            y,
            1.2,
            fillColor=colors.black,
            strokeColor=colors.black
        ))

    # Tal 0 og 1 (indenfor linjen)
    label_offset = 16

    d.add(String(
        x_start,
        y - label_offset,
        "0",
        fontSize=10,
        textAnchor="middle"
    ))

    d.add(String(
        x_end,
        y - label_offset,
        "1",
        fontSize=10,
        textAnchor="middle"
    ))

    return d


# -------------------------------------------------
# BAGUDKOMPATIBILITET
# -------------------------------------------------
# cards.py importerer stadig draw_number_line
draw_number_line = draw_numberline
