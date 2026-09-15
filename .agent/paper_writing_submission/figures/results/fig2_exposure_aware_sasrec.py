"""
Figure 2: Exposure-aware comparison between N-K0 and SASRec.

This script renders a paper-facing data figure from existing stage-local
sample-efficiency and exposure-aware baseline artifacts. It does not generate
new experiment data. The main panel shows the MovieLens-1M PopMatch-k5
sample-exposure curve; the side panel shows the Amazon seed42 closest-exposure
boundary from Table 3 and explicitly marks high-exposure SASRec as not
evaluated.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
CURVE_PATH = ROOT.parent / "sample_efficiency_training_efficiency" / "final_curve" / "sample_efficiency_curve.csv"
TABLE3_PATH = ROOT / "tables" / "table3_exposure_aware_baseline.csv"
OUT_DIR = Path(__file__).resolve().parent
PNG_PATH = OUT_DIR / "fig2_exposure_aware_sasrec.png"
SVG_PATH = OUT_DIR / "fig2_exposure_aware_sasrec.svg"

WIDTH = 2400
HEIGHT = 1500
DPI = (450, 450)

COLORS = {
    "N-K0": "#0077BB",
    "SASRec": "#EE7733",
    "M1": "#009988",
    "text": "#20242A",
    "muted": "#6E7781",
    "grid": "#D8DEE6",
    "axis": "#2A2F35",
    "panel": "#F7F9FB",
    "closest": "#E9F5FB",
    "high": "#FFF4E2",
    "missing": "#FFFFFF",
    "missing_stroke": "#A6B0BB",
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
FONT_HEAD = load_font(35, bold=True)
FONT_BODY = load_font(28)
FONT_SMALL = load_font(24)
FONT_TINY = load_font(21)


class Svg:
    def __init__(self) -> None:
        self.parts: list[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
            '<rect width="100%" height="100%" fill="white"/>',
            '<style>text{font-family:Arial,Calibri,sans-serif;fill:#20242A}.title{font-size:44px;font-weight:700}.subtitle{font-size:30px;fill:#6E7781}.head{font-size:35px;font-weight:700}.body{font-size:28px}.small{font-size:24px}.tiny{font-size:21px;fill:#6E7781}</style>',
        ]

    def rect(self, x: float, y: float, w: float, h: float, fill: str, stroke: str | None = None, width: float = 2, rx: float = 0) -> None:
        stroke_attr = f' stroke="{stroke}" stroke-width="{width:.1f}"' if stroke else ""
        rx_attr = f' rx="{rx:.1f}"' if rx else ""
        self.parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"{stroke_attr}{rx_attr}/>')

    def line(self, x1: float, y1: float, x2: float, y2: float, stroke: str, width: float = 2, dash: str | None = None) -> None:
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{width:.1f}" stroke-linecap="round"{dash_attr}/>')

    def circle(self, x: float, y: float, r: float, fill: str, stroke: str = "white", width: float = 3) -> None:
        self.parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{width:.1f}"/>')

    def polyline(self, points: list[tuple[float, float]], stroke: str, width: float = 4) -> None:
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        self.parts.append(f'<polyline points="{pts}" fill="none" stroke="{stroke}" stroke-width="{width:.1f}" stroke-linejoin="round" stroke-linecap="round"/>')

    def text(self, x: float, y: float, text: str, cls: str = "body", anchor: str = "middle") -> None:
        self.parts.append(f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{escape(text)}</text>')

    def finish(self) -> str:
        return "\n".join(self.parts + ["</svg>\n"])


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_centered(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str, font: ImageFont.ImageFont, fill: str) -> None:
    w, h = text_size(draw, text, font)
    draw.text((xy[0] - w / 2, xy[1] - h / 2), text, font=font, fill=fill)


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    svg: Svg,
    x: float,
    y: float,
    text: str,
    chars: int,
    font: ImageFont.ImageFont = FONT_SMALL,
    cls: str = "small",
    fill: str = COLORS["text"],
    line_h: int = 31,
    anchor: str = "middle",
) -> None:
    for i, line in enumerate(wrap(text, width=chars)):
        yy = y + i * line_h
        if anchor == "start":
            draw.text((x, yy), line, font=font, fill=fill)
            svg.text(x, yy + line_h - 5, line, cls, "start")
        else:
            draw_centered(draw, (x, yy + line_h / 2), line, font, fill)
            svg.text(x, yy + line_h - 5, line, cls)


def read_curve() -> list[dict[str, str]]:
    with CURVE_PATH.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def read_table3() -> list[dict[str, str]]:
    with TABLE3_PATH.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def fmt_exposure(value: float) -> str:
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if value >= 1000:
        return f"{value / 1000:.0f}k"
    return str(int(value))


def curve_xy(
    exposure: float,
    hr: float,
    left: int,
    top: int,
    right: int,
    bottom: int,
    min_log: float,
    max_log: float,
    max_y: float,
) -> tuple[float, float]:
    x = left + ((math.log10(exposure) - min_log) / (max_log - min_log)) * (right - left)
    y = bottom - (hr / max_y) * (bottom - top)
    return x, y


def draw_main_curve(draw: ImageDraw.ImageDraw, svg: Svg, rows: list[dict[str, str]]) -> None:
    x0, y0, w, h = 100, 230, 1480, 900
    plot_left, plot_top = x0 + 120, y0 + 115
    plot_right, plot_bottom = x0 + w - 70, y0 + h - 150
    max_y = 0.70
    exposures = [float(r["N-task exposure"]) for r in rows]
    min_log, max_log = math.log10(min(exposures) * 0.82), math.log10(max(exposures) * 1.10)

    draw.rounded_rectangle((x0, y0, x0 + w, y0 + h), radius=8, fill=COLORS["panel"])
    svg.rect(x0, y0, w, h, COLORS["panel"], rx=8)
    draw.text((x0 + 32, y0 + 34), "MovieLens-1M PopMatch-k5 sample-exposure curve", font=FONT_HEAD, fill=COLORS["text"])
    svg.text(x0 + 32, y0 + 70, "MovieLens-1M PopMatch-k5 sample-exposure curve", "head", "start")

    # Regime shading.
    closest_l = curve_xy(2800, 0, plot_left, plot_top, plot_right, plot_bottom, min_log, max_log, max_y)[0]
    closest_r = curve_xy(26000, 0, plot_left, plot_top, plot_right, plot_bottom, min_log, max_log, max_y)[0]
    high_l = curve_xy(300000, 0, plot_left, plot_top, plot_right, plot_bottom, min_log, max_log, max_y)[0]
    draw.rectangle((closest_l, plot_top, closest_r, plot_bottom), fill=COLORS["closest"])
    svg.rect(closest_l, plot_top, closest_r - closest_l, plot_bottom - plot_top, COLORS["closest"])
    draw.rectangle((high_l, plot_top, plot_right, plot_bottom), fill=COLORS["high"])
    svg.rect(high_l, plot_top, plot_right - high_l, plot_bottom - plot_top, COLORS["high"])
    draw_centered(draw, ((closest_l + closest_r) / 2, plot_top + 28), "closest-exposure regime", FONT_TINY, COLORS["muted"])
    svg.text((closest_l + closest_r) / 2, plot_top + 36, "closest-exposure regime", "tiny")
    draw_centered(draw, ((high_l + plot_right) / 2, plot_top + 28), "high sequential exposure", FONT_TINY, COLORS["muted"])
    svg.text((high_l + plot_right) / 2, plot_top + 36, "high sequential exposure", "tiny")

    # Grid and axes.
    for tick in [0.0, 0.2, 0.4, 0.6]:
        y = plot_bottom - (tick / max_y) * (plot_bottom - plot_top)
        draw.line((plot_left, y, plot_right, y), fill=COLORS["grid"], width=2)
        svg.line(plot_left, y, plot_right, y, COLORS["grid"], 2)
        draw.text((plot_left - 78, y - 15), f"{tick:.1f}", font=FONT_TINY, fill=COLORS["muted"])
        svg.text(plot_left - 28, y + 8, f"{tick:.1f}", "tiny", "end")

    x_ticks = [3000, 6000, 12000, 24000, 768000, 1534656]
    for tick in x_ticks:
        x = curve_xy(tick, 0, plot_left, plot_top, plot_right, plot_bottom, min_log, max_log, max_y)[0]
        draw.line((x, plot_bottom, x, plot_bottom + 10), fill=COLORS["axis"], width=2)
        svg.line(x, plot_bottom, x, plot_bottom + 10, COLORS["axis"], 2)
        draw_centered(draw, (x, plot_bottom + 45), fmt_exposure(tick), FONT_TINY, COLORS["text"])
        svg.text(x, plot_bottom + 55, fmt_exposure(tick), "tiny")

    draw.line((plot_left, plot_top, plot_left, plot_bottom), fill=COLORS["axis"], width=3)
    draw.line((plot_left, plot_bottom, plot_right, plot_bottom), fill=COLORS["axis"], width=3)
    svg.line(plot_left, plot_top, plot_left, plot_bottom, COLORS["axis"], 3)
    svg.line(plot_left, plot_bottom, plot_right, plot_bottom, COLORS["axis"], 3)
    draw_centered(draw, (plot_left - 78, plot_top + (plot_bottom - plot_top) / 2), "HR@1", FONT_SMALL, COLORS["text"])
    svg.text(plot_left - 78, plot_top + (plot_bottom - plot_top) / 2, "HR@1", "small")
    draw_centered(draw, ((plot_left + plot_right) / 2, plot_bottom + 95), "N-task sample exposure (log scale)", FONT_SMALL, COLORS["text"])
    svg.text((plot_left + plot_right) / 2, plot_bottom + 108, "N-task sample exposure (log scale)", "small")

    by_model = {
        "N-K0": [r for r in rows if r["model"] == "N-K0"],
        "SASRec": [r for r in rows if r["model"] == "SASRec"],
    }
    for model, model_rows in by_model.items():
        points = [
            curve_xy(float(r["N-task exposure"]), float(r["HR@1"]), plot_left, plot_top, plot_right, plot_bottom, min_log, max_log, max_y)
            for r in model_rows
        ]
        draw.line(points, fill=COLORS[model], width=5, joint="curve")
        svg.polyline(points, COLORS[model], 5)
        for r, (x, y) in zip(model_rows, points):
            draw.ellipse((x - 11, y - 11, x + 11, y + 11), fill=COLORS[model], outline="white", width=3)
            svg.circle(x, y, 11, COLORS[model])
            label = f"{float(r['HR@1']):.3f}"
            y_offset = -34 if model == "N-K0" else 30
            draw_centered(draw, (x, y + y_offset), label, FONT_TINY, COLORS["text"])
            svg.text(x, y + y_offset + 8, label, "tiny")

    # Legend.
    legend_x, legend_y = x0 + 880, y0 + 65
    for i, model in enumerate(["N-K0", "SASRec"]):
        x = legend_x + i * 190
        draw.line((x, legend_y, x + 55, legend_y), fill=COLORS[model], width=6)
        draw.ellipse((x + 20, legend_y - 9, x + 38, legend_y + 9), fill=COLORS[model], outline="white", width=2)
        draw.text((x + 70, legend_y - 16), model, font=FONT_SMALL, fill=COLORS["text"])
        svg.line(x, legend_y, x + 55, legend_y, COLORS[model], 6)
        svg.circle(x + 29, legend_y, 9, COLORS[model])
        svg.text(x + 70, legend_y + 8, model, "small", "start")


def draw_amazon_panel(draw: ImageDraw.ImageDraw, svg: Svg, table3: list[dict[str, str]]) -> None:
    x0, y0, w, h = 1660, 230, 640, 900
    plot_left, plot_top = x0 + 100, y0 + 135
    plot_right, plot_bottom = x0 + w - 60, y0 + h - 210
    max_y = 0.70

    draw.rounded_rectangle((x0, y0, x0 + w, y0 + h), radius=8, fill=COLORS["panel"])
    svg.rect(x0, y0, w, h, COLORS["panel"], rx=8)
    draw.text((x0 + 32, y0 + 34), "Amazon seed42 boundary", font=FONT_HEAD, fill=COLORS["text"])
    svg.text(x0 + 32, y0 + 70, "Amazon seed42 boundary", "head", "start")
    draw_wrapped(draw, svg, x0 + 32, y0 + 88, "Closest-exposure row only; high-exposure SASRec was not evaluated.", 50, FONT_SMALL, "small", COLORS["muted"], 30, "start")

    rows = {
        r["model"]: r
        for r in table3
        if r["dataset"] == "Amazon Musical Instruments" and r["budget_regime"] in {"LLM N-task anchor", "closest N-task exposure"}
    }
    values = [("N-K0", float(rows["N-K0"]["hr1"])), ("SASRec", float(rows["SASRec"]["hr1"]))]

    for tick in [0.0, 0.2, 0.4, 0.6]:
        y = plot_bottom - (tick / max_y) * (plot_bottom - plot_top)
        draw.line((plot_left, y, plot_right, y), fill=COLORS["grid"], width=2)
        svg.line(plot_left, y, plot_right, y, COLORS["grid"], 2)
        draw.text((plot_left - 70, y - 14), f"{tick:.1f}", font=FONT_TINY, fill=COLORS["muted"])
        svg.text(plot_left - 24, y + 8, f"{tick:.1f}", "tiny", "end")
    draw.line((plot_left, plot_top, plot_left, plot_bottom), fill=COLORS["axis"], width=3)
    draw.line((plot_left, plot_bottom, plot_right, plot_bottom), fill=COLORS["axis"], width=3)
    svg.line(plot_left, plot_top, plot_left, plot_bottom, COLORS["axis"], 3)
    svg.line(plot_left, plot_bottom, plot_right, plot_bottom, COLORS["axis"], 3)
    draw_centered(draw, (plot_left - 70, plot_top + (plot_bottom - plot_top) / 2), "HR@1", FONT_SMALL, COLORS["text"])
    svg.text(plot_left - 70, plot_top + (plot_bottom - plot_top) / 2, "HR@1", "small")

    centers = [plot_left + 145, plot_left + 335]
    bar_w = 96
    for (model, value), cx in zip(values, centers):
        y = plot_bottom - (value / max_y) * (plot_bottom - plot_top)
        draw.rectangle((cx - bar_w / 2, y, cx + bar_w / 2, plot_bottom), fill=COLORS[model])
        svg.rect(cx - bar_w / 2, y, bar_w, plot_bottom - y, COLORS[model])
        draw_centered(draw, (cx, y - 25), f"{value:.3f}", FONT_TINY, COLORS["text"])
        svg.text(cx, y - 15, f"{value:.3f}", "tiny")
        draw_centered(draw, (cx, plot_bottom + 42), model, FONT_SMALL, COLORS["text"])
        svg.text(cx, plot_bottom + 55, model, "small")

    miss_x, miss_y, miss_w, miss_h = x0 + 90, y0 + h - 145, w - 180, 74
    draw.rounded_rectangle((miss_x, miss_y, miss_x + miss_w, miss_y + miss_h), radius=14, fill=COLORS["missing"], outline=COLORS["missing_stroke"], width=2)
    svg.rect(miss_x, miss_y, miss_w, miss_h, COLORS["missing"], COLORS["missing_stroke"], 2, 14)
    draw_wrapped(draw, svg, miss_x + miss_w / 2, miss_y + 14, "Amazon high-exposure SASRec: not evaluated", 42, FONT_SMALL, "small", COLORS["muted"], 30)


def main() -> None:
    curve = read_curve()
    table3 = read_table3()

    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    svg = Svg()

    draw.text((110, 70), "SASRec comparison depends on supervision exposure", font=FONT_TITLE, fill=COLORS["text"])
    draw.text((110, 125), "Closest-exposure and high-exposure regimes support different interpretations.", font=FONT_SUBTITLE, fill=COLORS["muted"])
    svg.text(110, 105, "SASRec comparison depends on supervision exposure", "title", "start")
    svg.text(110, 160, "Closest-exposure and high-exposure regimes support different interpretations.", "subtitle", "start")

    draw_main_curve(draw, svg, curve)
    draw_amazon_panel(draw, svg, table3)

    note = "Sources: final_curve/sample_efficiency_curve.csv and table3_exposure_aware_baseline.csv. Exposure is sample exposure, not strict FLOPs or wall-clock matching."
    draw.text((110, 1275), note, font=FONT_TINY, fill=COLORS["muted"])
    svg.text(110, 1305, note, "tiny", "start")

    image.save(PNG_PATH, dpi=DPI)
    SVG_PATH.write_text(svg.finish(), encoding="utf-8")
    print(f"wrote {PNG_PATH}")
    print(f"wrote {SVG_PATH}")


if __name__ == "__main__":
    main()
