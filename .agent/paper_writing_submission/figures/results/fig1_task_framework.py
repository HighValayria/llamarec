"""
Figure 1: Supervision interfaces for recommendation-tuned LLMs.

This script renders a conceptual framework figure from the paper's frozen
problem formulation and method framework. It writes both PNG and SVG outputs.
No numeric data or experiment outputs are generated.
"""

from __future__ import annotations

import math
from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont


OUT_DIR = Path(__file__).resolve().parent
PNG_PATH = OUT_DIR / "fig1_task_framework.png"
SVG_PATH = OUT_DIR / "fig1_task_framework.svg"

WIDTH = 2400
HEIGHT = 1450
DPI = (450, 450)

COLORS = {
    "text": "#20242A",
    "muted": "#68717C",
    "grid": "#D7DEE7",
    "history": "#E8F4FA",
    "history_stroke": "#2E86AB",
    "base": "#F3F4F6",
    "base_stroke": "#6B7280",
    "y_fill": "#FFF1D7",
    "y_stroke": "#D98B00",
    "n_fill": "#EAF7E8",
    "n_stroke": "#3D8B40",
    "m_fill": "#F5ECFA",
    "m_stroke": "#8A4FB3",
    "arrow": "#2A2F35",
    "output": "#FFFFFF",
    "soft": "#FAFBFC",
}


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


FONT_TITLE = load_font(44, bold=True)
FONT_SUBTITLE = load_font(30)
FONT_HEAD = load_font(34, bold=True)
FONT_BODY = load_font(27)
FONT_SMALL = load_font(24)
FONT_TINY = load_font(21)


class Svg:
    def __init__(self) -> None:
        self.parts: list[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
            '<rect width="100%" height="100%" fill="white"/>',
            '<style>text{font-family:Arial,Calibri,sans-serif;fill:#20242A}.title{font-size:44px;font-weight:700}.subtitle{font-size:30px;fill:#68717C}.head{font-size:34px;font-weight:700}.body{font-size:27px}.small{font-size:24px}.tiny{font-size:21px;fill:#68717C}</style>',
        ]

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        fill: str,
        stroke: str,
        width: float = 2,
        rx: float = 18,
    ) -> None:
        self.parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{width:.1f}"/>'
        )

    def line(self, x1: float, y1: float, x2: float, y2: float, stroke: str, width: float = 3) -> None:
        self.parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{width:.1f}" stroke-linecap="round"/>'
        )

    def polygon(self, points: list[tuple[float, float]], fill: str) -> None:
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        self.parts.append(f'<polygon points="{pts}" fill="{fill}"/>')

    def text(self, x: float, y: float, text: str, cls: str = "body", anchor: str = "middle") -> None:
        self.parts.append(f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{escape(text)}</text>')

    def finish(self) -> str:
        return "\n".join(self.parts + ["</svg>\n"])


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_centered(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    text: str,
    font: ImageFont.ImageFont,
    fill: str,
) -> None:
    w, h = text_size(draw, text, font)
    draw.text((xy[0] - w / 2, xy[1] - h / 2), text, font=font, fill=fill)


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    svg: Svg,
    x: float,
    y: float,
    text: str,
    font: ImageFont.ImageFont,
    cls: str,
    fill: str,
    chars: int,
    line_h: int,
    anchor: str = "middle",
) -> None:
    lines = wrap(text, width=chars)
    for i, line in enumerate(lines):
        yy = y + i * line_h
        if anchor == "start":
            draw.text((x, yy), line, font=font, fill=fill)
            svg.text(x, yy + line_h - 5, line, cls, "start")
        else:
            draw_centered(draw, (x, yy + line_h / 2), line, font, fill)
            svg.text(x, yy + line_h - 6, line, cls)


def draw_box(
    draw: ImageDraw.ImageDraw,
    svg: Svg,
    xywh: tuple[int, int, int, int],
    fill: str,
    stroke: str,
    title: str,
    body: list[str],
    label: str | None = None,
) -> None:
    x, y, w, h = xywh
    draw.rounded_rectangle((x, y, x + w, y + h), radius=20, fill=fill, outline=stroke, width=3)
    svg.rect(x, y, w, h, fill, stroke, 3, 20)
    if label:
        draw.rounded_rectangle((x + 24, y + 20, x + 120, y + 58), radius=18, fill=stroke)
        draw_centered(draw, (x + 72, y + 39), label, FONT_SMALL, "white")
        svg.rect(x + 24, y + 20, 96, 38, stroke, stroke, 1, 18)
        svg.text(x + 72, y + 48, label, "small")
        title_x = x + 150
    else:
        title_x = x + 34
    draw.text((title_x, y + 22), title, font=FONT_HEAD, fill=COLORS["text"])
    svg.text(title_x, y + 58, title, "head", "start")
    body_y = y + 86
    for i, line in enumerate(body):
        draw_wrapped(draw, svg, x + w / 2, body_y + i * 74, line, FONT_BODY, "body", COLORS["text"], 42, 32)


def arrowhead(end: tuple[float, float], angle: float, size: float = 18) -> list[tuple[float, float]]:
    x, y = end
    return [
        (x, y),
        (x - size * math.cos(angle - 0.45), y - size * math.sin(angle - 0.45)),
        (x - size * math.cos(angle + 0.45), y - size * math.sin(angle + 0.45)),
    ]


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    svg: Svg,
    start: tuple[float, float],
    end: tuple[float, float],
    color: str = COLORS["arrow"],
    width: int = 4,
) -> None:
    draw.line((start, end), fill=color, width=width)
    svg.line(start[0], start[1], end[0], end[1], color, width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    head = arrowhead(end, angle)
    draw.polygon(head, fill=color)
    svg.polygon(head, color)


def main() -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    svg = Svg()

    draw.text((110, 70), "Supervision interfaces induce different recommendation capabilities", font=FONT_TITLE, fill=COLORS["text"])
    draw.text((110, 125), "The same user history can be scored through preference, next-item, or unified multi-task interfaces.", font=FONT_SUBTITLE, fill=COLORS["muted"])
    svg.text(110, 105, "Supervision interfaces induce different recommendation capabilities", "title", "start")
    svg.text(110, 160, "The same user history can be scored through preference, next-item, or unified multi-task interfaces.", "subtitle", "start")

    # Shared input and base model.
    draw_box(
        draw,
        svg,
        (120, 270, 410, 250),
        COLORS["history"],
        COLORS["history_stroke"],
        "Shared input",
        ["User history", "Target item or candidate set"],
    )
    draw_box(
        draw,
        svg,
        (710, 270, 410, 250),
        COLORS["base"],
        COLORS["base_stroke"],
        "Base LLM",
        ["Zero-shot reference", "Same model family"],
    )
    draw_arrow(draw, svg, (530, 395), (710, 395))

    # Interface branches.
    y_box = (150, 690, 560, 315)
    n_box = (920, 690, 560, 315)
    m_box = (1690, 690, 560, 315)

    draw_arrow(draw, svg, (915, 520), (430, 690))
    draw_arrow(draw, svg, (915, 520), (1200, 690))
    draw_arrow(draw, svg, (915, 520), (1970, 690))

    draw_box(
        draw,
        svg,
        y_box,
        COLORS["y_fill"],
        COLORS["y_stroke"],
        "Preference interface",
        ["History + item", "Yes/no preference score"],
        "Y-K0",
    )
    draw_box(
        draw,
        svg,
        n_box,
        COLORS["n_fill"],
        COLORS["n_stroke"],
        "Next-item interface",
        ["History + candidates", "Select next observed item"],
        "N-K0",
    )
    draw_box(
        draw,
        svg,
        m_box,
        COLORS["m_fill"],
        COLORS["m_stroke"],
        "Unified multi-task",
        ["One adapted model", "Y and N outputs available"],
        "M1",
    )

    # Output boxes.
    outputs = [
        ((185, 1105, 490, 130), COLORS["y_stroke"], "Ranking route: sort candidates by P(Yes)"),
        ((955, 1105, 490, 130), COLORS["n_stroke"], "Ranking route: score candidate labels"),
        ((1725, 1105, 490, 130), COLORS["m_stroke"], "Retention test: one model, two interfaces"),
    ]
    for xywh, stroke, text in outputs:
        x, y, w, h = xywh
        draw.rounded_rectangle((x, y, x + w, y + h), radius=18, fill=COLORS["output"], outline=stroke, width=3)
        svg.rect(x, y, w, h, COLORS["output"], stroke, 3, 18)
        draw_wrapped(draw, svg, x + w / 2, y + 31, text, FONT_BODY, "body", COLORS["text"], 34, 34)

    draw_arrow(draw, svg, (430, 1005), (430, 1105), COLORS["y_stroke"])
    draw_arrow(draw, svg, (1200, 1005), (1200, 1105), COLORS["n_stroke"])
    draw_arrow(draw, svg, (1970, 1005), (1970, 1105), COLORS["m_stroke"])

    # Boundary note.
    note = "Conceptual figure only: M1 is a unified interface setting, not a new architecture or a dominance claim."
    draw.rounded_rectangle((360, 1280, 2040, 1380), radius=16, fill=COLORS["soft"], outline=COLORS["grid"], width=2)
    draw_wrapped(draw, svg, 1200, 1305, note, FONT_SMALL, "small", COLORS["muted"], 72, 30)
    svg.rect(360, 1280, 1680, 100, COLORS["soft"], COLORS["grid"], 2, 16)

    image.save(PNG_PATH, dpi=DPI)
    SVG_PATH.write_text(svg.finish(), encoding="utf-8")
    print(f"wrote {PNG_PATH}")
    print(f"wrote {SVG_PATH}")


if __name__ == "__main__":
    main()
