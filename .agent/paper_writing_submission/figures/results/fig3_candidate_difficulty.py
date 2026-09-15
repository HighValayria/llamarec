"""
Figure 3: Candidate difficulty changes ranking interpretation.

This script reads the paper-facing candidate robustness CSV and renders a
two-panel HR@1 figure without requiring matplotlib. It writes both PNG and SVG
outputs next to this script. The PNG uses Pillow; the SVG is generated from the
same geometry.
"""

from __future__ import annotations

import csv
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "tables" / "table2_candidate_robustness.csv"
OUT_DIR = Path(__file__).resolve().parent
PNG_PATH = OUT_DIR / "fig3_candidate_difficulty.png"
SVG_PATH = OUT_DIR / "fig3_candidate_difficulty.svg"

WIDTH = 2400
HEIGHT = 1500
DPI = (450, 450)

COLORS = {
    "N-K0": "#0077BB",
    "M1": "#EE7733",
    "grid": "#D8DEE6",
    "axis": "#2A2F35",
    "text": "#20242A",
    "muted": "#6E7781",
    "panel": "#F7F9FB",
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


FONT = load_font(38)
FONT_SMALL = load_font(31)
FONT_TINY = load_font(26)
FONT_BOLD = load_font(44, bold=True)
FONT_PANEL = load_font(36, bold=True)


def fmt(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.3f}"


def read_rows() -> list[dict[str, str]]:
    with DATA_PATH.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def ordered_values(rows: list[dict[str, str]], dataset: str, protocols: list[str]) -> dict[str, list[float]]:
    out = {"N-K0": [], "M1": []}
    for protocol in protocols:
        for model in ["N-K0", "M1"]:
            match = [
                r
                for r in rows
                if r["dataset"] == dataset and r["protocol"] == protocol and r["model"] == model
            ]
            if not match:
                raise ValueError(f"Missing row for {dataset} {protocol} {model}")
            out[model].append(float(match[0]["hr1"]))
    return out


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


class Svg:
    def __init__(self) -> None:
        self.parts: list[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
            '<rect width="100%" height="100%" fill="white"/>',
            '<style>text{font-family:Arial,Calibri,sans-serif;fill:#20242A}.small{font-size:31px}.tiny{font-size:26px}.title{font-size:44px;font-weight:700}.panel{font-size:36px;font-weight:700}</style>',
        ]

    def rect(self, x: float, y: float, w: float, h: float, fill: str, stroke: str | None = None) -> None:
        stroke_attr = f' stroke="{stroke}" stroke-width="2"' if stroke else ""
        self.parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"{stroke_attr}/>')

    def line(self, x1: float, y1: float, x2: float, y2: float, stroke: str, width: float = 2) -> None:
        self.parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{width:.1f}"/>')

    def text(self, x: float, y: float, text: str, cls: str = "small", anchor: str = "middle") -> None:
        self.parts.append(f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{escape(text)}</text>')

    def finish(self) -> str:
        return "\n".join(self.parts + ["</svg>\n"])


def draw_panel(
    img_draw: ImageDraw.ImageDraw,
    svg: Svg,
    x0: int,
    y0: int,
    w: int,
    h: int,
    title: str,
    protocols: list[str],
    values: dict[str, list[float]],
) -> None:
    plot_left = x0 + 110
    plot_top = y0 + 120
    plot_right = x0 + w - 45
    plot_bottom = y0 + h - 160
    plot_w = plot_right - plot_left
    plot_h = plot_bottom - plot_top
    max_y = 0.8

    img_draw.rectangle((x0, y0, x0 + w, y0 + h), fill=COLORS["panel"])
    svg.rect(x0, y0, w, h, COLORS["panel"])
    img_draw.text((x0 + 30, y0 + 35), title, font=FONT_PANEL, fill=COLORS["text"])
    svg.text(x0 + 30, y0 + 70, title, "panel", "start")

    for tick in [0.0, 0.2, 0.4, 0.6, 0.8]:
        y = plot_bottom - (tick / max_y) * plot_h
        img_draw.line((plot_left, y, plot_right, y), fill=COLORS["grid"], width=2)
        svg.line(plot_left, y, plot_right, y, COLORS["grid"], 2)
        img_draw.text((plot_left - 80, y - 17), f"{tick:.1f}", font=FONT_TINY, fill=COLORS["muted"])
        svg.text(plot_left - 35, y + 9, f"{tick:.1f}", "tiny", "end")

    img_draw.line((plot_left, plot_top, plot_left, plot_bottom), fill=COLORS["axis"], width=3)
    img_draw.line((plot_left, plot_bottom, plot_right, plot_bottom), fill=COLORS["axis"], width=3)
    svg.line(plot_left, plot_top, plot_left, plot_bottom, COLORS["axis"], 3)
    svg.line(plot_left, plot_bottom, plot_right, plot_bottom, COLORS["axis"], 3)

    group_w = plot_w / len(protocols)
    bar_w = min(95, group_w * 0.26)
    for i, protocol in enumerate(protocols):
        cx = plot_left + group_w * (i + 0.5)
        for j, model in enumerate(["N-K0", "M1"]):
            value = values[model][i]
            bar_h = (value / max_y) * plot_h
            x = cx + (j - 0.5) * (bar_w + 12) - bar_w / 2
            y = plot_bottom - bar_h
            img_draw.rectangle((x, y, x + bar_w, plot_bottom), fill=COLORS[model])
            svg.rect(x, y, bar_w, bar_h, COLORS[model])
            draw_centered(img_draw, (x + bar_w / 2, y - 22), fmt(value), FONT_TINY, COLORS["text"])
            svg.text(x + bar_w / 2, y - 14, fmt(value), "tiny")
        label = protocol.replace("Canonical ", "").replace("Amazon ", "")
        draw_centered(img_draw, (cx, plot_bottom + 45), label, FONT_TINY, COLORS["text"])
        svg.text(cx, plot_bottom + 55, label, "tiny")

    # Axis label
    draw_centered(img_draw, (plot_left - 70, plot_top + plot_h / 2), "HR@1", FONT_SMALL, COLORS["text"])
    svg.text(plot_left - 70, plot_top + plot_h / 2, "HR@1", "small")


def main() -> None:
    rows = read_rows()
    ml_protocols = ["Canonical Random-k5", "PopMatch-k5", "Random-k20", "Random-k50"]
    amz_protocols = ["Random-k5", "PopMatch-k5"]
    ml_values = ordered_values(rows, "MovieLens-1M", ml_protocols)
    amz_values = ordered_values(rows, "Amazon Musical Instruments", amz_protocols)

    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    svg = Svg()

    draw.text((110, 70), "Candidate difficulty changes HR@1 and model separation", font=FONT_BOLD, fill=COLORS["text"])
    draw.text((110, 125), "Random-k5 is a reference setting; PopMatch-k5 and larger candidate sets provide harder checks.", font=FONT_SMALL, fill=COLORS["muted"])
    svg.text(110, 105, "Candidate difficulty changes HR@1 and model separation", "title", "start")
    svg.text(110, 160, "Random-k5 is a reference setting; PopMatch-k5 and larger candidate sets provide harder checks.", "small", "start")

    draw_panel(draw, svg, 100, 220, 1320, 900, "MovieLens-1M", ml_protocols, ml_values)
    draw_panel(draw, svg, 1510, 220, 790, 900, "Amazon Musical Instruments seed42", amz_protocols, amz_values)

    # Legend
    legend_y = 1190
    for i, model in enumerate(["N-K0", "M1"]):
        x = 905 + i * 260
        draw.rectangle((x, legend_y, x + 52, legend_y + 34), fill=COLORS[model])
        draw.text((x + 68, legend_y - 2), model, font=FONT_SMALL, fill=COLORS["text"])
        svg.rect(x, legend_y, 52, 34, COLORS[model])
        svg.text(x + 68, legend_y + 28, model, "small", "start")

    note = "Source: table2_candidate_robustness.csv. Bars show HR@1; missing NDCG/MRR for k20/k50 are not imputed."
    draw.text((110, 1290), note, font=FONT_TINY, fill=COLORS["muted"])
    svg.text(110, 1320, note, "tiny", "start")

    image.save(PNG_PATH, dpi=DPI)
    SVG_PATH.write_text(svg.finish(), encoding="utf-8")
    print(f"wrote {PNG_PATH}")
    print(f"wrote {SVG_PATH}")


if __name__ == "__main__":
    main()
