"""График: обороты в минуту от радиуса пола при целевой тяжести.

Запуск: uv run calc/plots/spin_vs_radius.py
Выход:  assets/ship/spin-vs-radius.ru.svg, assets/ship/spin-vs-radius.en.svg
Числа — из data/canon.json (сначала uv run calc/derive.py), подписи — из data/strings.yaml.
Детерминирован: при неизменном входе SVG не переписываются.
"""
from __future__ import annotations

import io
import json
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import canonlib  # noqa: E402

OUT = ROOT / "assets" / "ship"
NAME = "spin-vs-radius"
R_RANGE = (10, 60)  # ось X графика, м — параметр оформления, не канон

# Палитра: dataviz reference palette, светлая поверхность (SVG вставляется картинкой и
# должен читаться и в тёмной теме Obsidian, поэтому фон непрозрачный).
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e6e5e0"
SERIES = "#2a78d6"
BAND = "#2a78d6"

plt.rcParams.update({
    "svg.hashsalt": "maya-in-transit",
    "svg.fonttype": "path",
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.edgecolor": INK_2,
    "axes.labelcolor": INK_2,
    "xtick.color": INK_2,
    "ytick.color": INK_2,
})


def rpm(a: float, r):
    return np.sqrt(a / r) * 60 / (2 * math.pi)


def render(lang: str, vals: dict, strings: dict) -> str:
    s = {k: v[lang] for k, v in strings["spin_vs_radius"].items()}
    a = vals["habitat.floor_accel"]["value"]
    r_spec = vals["habitat.floor_radius"]["value"]
    r_conc = vals["habitat.floor_radius_concept"]["value"]
    band = vals["habitat.floor_radius_concept_range"]["value"]
    fv = lambda k: canonlib.format_value(vals[k], lang)  # noqa: E731
    dec = "," if lang == "ru" else "."

    fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=100)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    r = np.linspace(*R_RANGE, 501)
    ax.axvspan(band[0], band[1], color=BAND, alpha=0.08, lw=0, zorder=0)
    ax.text((band[0] + band[1]) / 2, 0.97, s["concept_band"].format(range=fv("habitat.floor_radius_concept_range")),
            transform=ax.get_xaxis_transform(), ha="center", va="top", color=INK_2, fontsize=8.5)
    ax.plot(r, rpm(a, r), color=SERIES, lw=2, solid_capstyle="round", zorder=2)

    points = [
        (r_spec, s["spec_point"].format(radius=fv("habitat.floor_radius"), rpm=fv("ship.spin_rpm")), (14, 22)),
        (r_conc, s["concept_point"].format(radius=fv("habitat.floor_radius_concept"),
                                           rpm=fv("ship.spin_rpm_concept")), (-12, -36)),
    ]
    for x, label, off in points:
        y = float(rpm(a, x))
        ax.plot([x], [y], "o", ms=8, color=SERIES, mec=SURFACE, mew=2, zorder=3)
        ax.annotate(label, (x, y), xytext=off, textcoords="offset points", color=INK, fontsize=9,
                    ha="left" if off[0] > 0 else "right", va="center", linespacing=1.3,
                    multialignment="left" if off[0] > 0 else "right",
                    arrowprops=dict(arrowstyle="-", color=INK_2, lw=0.8, shrinkA=0, shrinkB=5))

    ax.set_xlim(*R_RANGE)
    ymax = math.ceil(float(rpm(a, R_RANGE[0])) + 0.5)
    ax.set_ylim(0, ymax)
    ax.set_title(s["title"].format(gravity=fv("habitat.floor_gravity")), loc="left", color=INK, fontsize=12, pad=12)
    ax.set_xlabel(s["xlabel"])
    ax.set_ylabel(s["ylabel"])
    ax.text(0.99, 0.03, s["formula"].format(accel=fv("habitat.floor_accel")), transform=ax.transAxes,
            ha="right", va="bottom", color=INK_2, fontsize=8.5)
    fmt = FuncFormatter(lambda v, _: (f"{v:g}").replace(".", dec))
    ax.xaxis.set_major_formatter(fmt)
    ax.yaxis.set_major_formatter(fmt)
    ax.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()

    buf = io.StringIO()
    fig.savefig(buf, format="svg", facecolor=SURFACE,
                metadata={"Date": None, "Creator": "calc/plots/spin_vs_radius.py"})
    plt.close(fig)
    return buf.getvalue()


def main():
    canon_json = ROOT / "data" / "canon.json"
    if not canon_json.exists():
        raise SystemExit("нет data/canon.json — сначала uv run calc/derive.py")
    vals = json.loads(canon_json.read_text(encoding="utf-8"))["values"]
    strings = canonlib.load_yaml(ROOT / "data" / "strings.yaml")
    OUT.mkdir(parents=True, exist_ok=True)
    for lang in ("ru", "en"):
        path = OUT / f"{NAME}.{lang}.svg"
        svg = render(lang, vals, strings)
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old == svg:
            print(f"без изменений: {path.relative_to(ROOT)}", flush=True)
        else:
            path.write_text(svg, encoding="utf-8")
            print(f"записан: {path.relative_to(ROOT)}", flush=True)


if __name__ == "__main__":
    main()
