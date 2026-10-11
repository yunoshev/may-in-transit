"""Карточка-превью для ссылок на сайт (og:image): Майя в рост рядом с кораблём на фоне Юпитера, стиль синьки.

Запуск: uv run figures/og-card/build.py
Выход:  figures/og-card/og-card.svg (исходник) и site/static/og-image.png (1200×630, рендер headless Chrome)
Пропорции корабля — из data/canon.json (хребет, радиус пола, противовес, положение ступицы), как на BP-01.
Лицо и внешность Майи не утверждены — на карточке только силуэт.
"""
from __future__ import annotations

import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
W, H = 1200, 630

BG = "#0e2c4f"
GRID = "#2b5a8a"
INK = "#eef5ff"
INK2 = "#a9c8ec"
FILL = "#16395f"
FILL2 = "#1d4673"
SAFE = "#ff7f6e"
CAM = "#8ee6ff"
FONT = "'Helvetica Neue', Helvetica, Arial, 'DejaVu Sans', sans-serif"

CHROME = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
]


def val(vals, key, default):
    v = vals.get(key, {}).get("value", default)
    return sum(v) / len(v) if isinstance(v, list) else v


def fnum(x):
    return f"{x:g}".replace(".", ",")


def smooth(points, closed=True):
    """Сглаженный контур через точки (Catmull-Rom → кубические Безье)."""
    n = len(points)
    d = [f"M{points[0][0]:.1f},{points[0][1]:.1f}"]
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = points[(i - 1) % n] if closed or i > 0 else points[i]
        p1, p2 = points[i], points[(i + 1) % n]
        p3 = points[(i + 2) % n] if closed or i + 2 < n else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}")
    return " ".join(d) + (" Z" if closed else "")


def maya(cx, floor_y, height):
    """Силуэт анфас: комбинезон, волосы собраны в пучок, руки вдоль тела. Координаты — метры при росте 1,7."""
    k = height / 1.7
    half = [  # правая половина сверху вниз: (x, z)
        (0.045, 1.47), (0.06, 1.43), (0.15, 1.405), (0.195, 1.37), (0.205, 1.25), (0.215, 1.08),
        (0.205, 0.86), (0.2, 0.76), (0.175, 0.73), (0.165, 0.78), (0.17, 0.9), (0.165, 1.08), (0.15, 1.2),
        (0.13, 1.06), (0.125, 1.0), (0.155, 0.9), (0.16, 0.8), (0.14, 0.6), (0.115, 0.46), (0.1, 0.25),
        (0.085, 0.07), (0.115, 0.02), (0.11, 0.0), (0.035, 0.0), (0.04, 0.07), (0.05, 0.25), (0.05, 0.46),
        (0.035, 0.65), (0.0, 0.76),
    ]
    right = [(cx + x * k, floor_y - z * k) for x, z in half]
    left = [(cx - x * k, floor_y - z * k) for x, z in reversed(half[:-1])]
    body = smooth(right + left)
    hy = floor_y - 1.585 * k
    hair = smooth([(cx + dx * k, hy - dz * k) for dx, dz in (
        (0.0, 0.125), (0.07, 0.11), (0.095, 0.05), (0.09, -0.04), (0.075, -0.075), (0.07, -0.01),
        (0.055, 0.05), (0.0, 0.07), (-0.055, 0.05), (-0.07, -0.01), (-0.075, -0.075), (-0.09, -0.04),
        (-0.095, 0.05), (-0.07, 0.11))])
    out = [
        f'<path d="{body}" fill="{FILL2}" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>',
        f'<ellipse cx="{cx:.1f}" cy="{hy:.1f}" rx="{0.072 * k:.1f}" ry="{0.098 * k:.1f}" fill="{FILL2}" '
        f'stroke="{INK}" stroke-width="2.2"/>',
        f'<path d="{hair}" fill="{FILL}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>',
        f'<circle cx="{cx + 0.035 * k:.1f}" cy="{hy - 0.15 * k:.1f}" r="{0.045 * k:.1f}" fill="{FILL}" '
        f'stroke="{INK}" stroke-width="2"/>',
        # швы комбинезона: молния и пояс
        f'<line x1="{cx:.1f}" y1="{floor_y - 1.42 * k:.1f}" x2="{cx:.1f}" y2="{floor_y - 0.86 * k:.1f}" '
        f'stroke="{INK2}" stroke-width="1.2"/>',
        f'<path d="M{cx - 0.128 * k:.1f},{floor_y - 1.0 * k:.1f} Q{cx:.1f},{floor_y - 0.985 * k:.1f} '
        f'{cx + 0.128 * k:.1f},{floor_y - 1.0 * k:.1f}" fill="none" stroke="{INK2}" stroke-width="1.2"/>',
        # нашивка миссии на плече
        f'<circle cx="{cx - 0.12 * k:.1f}" cy="{floor_y - 1.3 * k:.1f}" r="{0.025 * k:.1f}" fill="none" '
        f'stroke="{CAM}" stroke-width="1.4"/>',
    ]
    return out


def jupiter(cx, cy, r):
    out = [f'<clipPath id="jup"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>',
           f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{FILL}" stroke="{INK2}" stroke-width="1.6" opacity="0.9"/>']
    bands = [-0.72, -0.55, -0.38, -0.2, -0.05, 0.12, 0.3, 0.47, 0.63, 0.8]
    g = [f'<g clip-path="url(#jup)" stroke="{INK2}" fill="none" opacity="0.55">']
    for i, b in enumerate(bands):
        y = cy + b * r
        wob = 6 if i % 2 else -5
        g.append(f'<path d="M{cx - r},{y:.1f} Q{cx - r / 2},{y + wob:.1f} {cx},{y:.1f} T{cx + r},{y:.1f}" '
                 f'stroke-width="{1.4 if i % 3 else 2.4}"/>')
    g.append(f'<ellipse cx="{cx + 0.3 * r:.1f}" cy="{cy - 0.52 * r:.1f}" rx="{0.15 * r:.1f}" ry="{0.075 * r:.1f}" '
             f'stroke-width="1.8"/>')
    g.append("</g>")
    return out[:1], out[1:] + g


def ship(vals, x_aft, x_nose, y):
    """Корабль сбоку, нос справа; станции узлов — метры от носа (как в canon.yaml и на BP-01)."""
    L = val(vals, "exterior.spine.length", 72)
    k = (x_nose - x_aft) / L
    X = lambda st: x_nose - st * k  # noqa: E731
    span = lambda key, d: vals.get(key, {}).get("value", d)  # noqa: E731
    R = val(vals, "habitat.floor_radius", 28)
    Rc = val(vals, "exterior.counterweight.radius", 24)
    hub = X(val(vals, "exterior.hub.station", 12))
    s = []

    def rect(x, yy, w, h, fill=FILL2, sw=1.6, rx=0):
        s.append(f'<rect x="{x:.1f}" y="{yy:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" '
                 f'stroke="{INK}" stroke-width="{sw}"/>')

    # радиаторы над и под хребтом
    r0, r1 = span("exterior.radiators.station", [31, 55])
    hs = val(vals, "exterior.radiators.half_span", 9) * k
    for yy in (y - 6 - hs, y + 6):
        rect(X(r1), yy, (r1 - r0) * k, hs, fill=FILL, sw=1.2)
        for i in range(1, 6):
            xx = X(r1) + i * (r1 - r0) * k / 6
            s.append(f'<line x1="{xx:.1f}" y1="{yy:.1f}" x2="{xx:.1f}" y2="{yy + hs:.1f}" stroke="{INK2}" '
                     f'stroke-width="0.8" opacity="0.7"/>')
    # хребет
    d = val(vals, "exterior.spine.diameter", 1.6) * k
    rect(x_aft, y - d / 2, L * k, d, fill=FILL2, sw=1.4)
    # двигатели и выхлоп
    p0, p1 = span("exterior.propulsion.station", [64, 72])
    rect(X(p1), y - 1.8 * k, (p1 - p0) * k * 0.7, 3.6 * k)
    s.append(f'<path d="M{X(p1):.1f},{y - 1.2 * k:.1f} L{X(p1) - 22:.1f},{y - 2.6 * k:.1f} '
             f'L{X(p1) - 22:.1f},{y + 2.6 * k:.1f} L{X(p1):.1f},{y + 1.2 * k:.1f} Z" fill="{FILL}" stroke="{INK}" '
             f'stroke-width="1.4"/>')
    s.append(f'<path d="M{X(p1) - 24:.1f},{y - 2.4 * k:.1f} L{X(p1) - 105:.1f},{y - 5.5 * k:.1f} '
             f'M{X(p1) - 24:.1f},{y + 2.4 * k:.1f} L{X(p1) - 105:.1f},{y + 5.5 * k:.1f}" stroke="{INK2}" '
             f'stroke-width="1.2" stroke-dasharray="6 5"/>')
    # реактор и теневая защита (щит со стороны жилья, то есть к носу)
    q0, q1 = span("exterior.reactor.station", [58, 63])
    rd = val(vals, "exterior.reactor.diameter", 3.0) * k
    rect(X(q1), y - rd / 2, (q1 - q0) * k, rd)
    rect(X(q0) - 0.4 * k, y - rd * 0.95, 1.0 * k, rd * 1.9, fill=INK2, sw=1)
    # баки
    t0, t1 = span("exterior.tanks.station", [16, 28])
    td = val(vals, "exterior.tanks.diameter", 5.0) * k
    n = 3
    for i in range(n):
        a = t0 + i * (t1 - t0) / n
        s.append(f'<rect x="{X(a + (t1 - t0) / n) + 1.5:.1f}" y="{y - td / 2:.1f}" width="{(t1 - t0) / n * k - 3:.1f}" '
                 f'height="{td:.1f}" rx="{td / 2.6:.1f}" fill="{FILL2}" stroke="{INK}" stroke-width="1.5"/>')
    # ферма вниз к жилому модулю и вверх к противовесу
    bw = val(vals, "exterior.boom.width", 1.2) * k
    hd = val(vals, "exterior.habitat.outer_diameter", 3.4) * k
    hl = val(vals, "exterior.habitat.outer_length", 7.0) * k
    cd = val(vals, "exterior.counterweight.diameter", 3.0) * k
    cl = val(vals, "exterior.counterweight.length", 4.0) * k
    yf, yc = y + R * k, y - Rc * k
    rect(hub - bw / 2, yc + cd / 2, bw, yf - yc - cd / 2 - hd, fill=FILL, sw=1.2)
    s.append(f'<line x1="{hub:.1f}" y1="{y + 10}" x2="{hub:.1f}" y2="{yf - hd - 2:.1f}" stroke="{SAFE}" '
             f'stroke-width="1.6" stroke-dasharray="5 4"/>')
    rect(hub - hl / 2, yf - hd, hl, hd, fill=FILL2, sw=1.8, rx=8)
    rect(hub - cl / 2, yc - cd / 2, cl, cd, fill=FILL2, sw=1.6, rx=6)
    # ступица с ядром ARI
    vd = val(vals, "exterior.ari_core.vault_diameter", 2.6) * k
    vl = val(vals, "exterior.ari_core.vault_length", 3.0) * k
    rect(hub - vl / 2, y - vd / 2, vl, vd, fill="#2a5d94", sw=1.8)
    s.append(f'<circle cx="{hub:.1f}" cy="{y}" r="{vd * 1.15:.1f}" fill="none" stroke="{INK2}" stroke-width="1" '
             f'stroke-dasharray="4 4"/>')
    # носовая мачта
    c0, c1 = span("exterior.comms.station", [0, 6])
    rect(X(c1), y - 3, (c1 - c0) * k, 6, fill=FILL, sw=1.2)
    # ось вращения и стрелка вращения
    s.append(f'<line x1="{X(p1) - 130:.1f}" y1="{y}" x2="{x_nose + 46:.1f}" y2="{y}" stroke="{INK2}" '
             f'stroke-width="1" stroke-dasharray="14 5 3 5"/>')
    s.append(f'<path d="M{x_nose + 26:.1f},{y - 34} A12,36 0 0 1 {x_nose + 26:.1f},{y + 34}" fill="none" '
             f'stroke="{INK}" stroke-width="1.8" marker-end="url(#arr)"/>')
    yd = yf + 34
    s.append(f'<line x1="{x_aft:.1f}" y1="{yd:.1f}" x2="{x_nose:.1f}" y2="{yd:.1f}" stroke="{INK2}" '
             f'stroke-width="1.1" marker-start="url(#arr2)" marker-end="url(#arr2)"/>')
    for xx in (x_aft, x_nose):
        s.append(f'<line x1="{xx:.1f}" y1="{y + 12:.1f}" x2="{xx:.1f}" y2="{yd + 6:.1f}" stroke="{INK2}" '
                 f'stroke-width="0.7" stroke-dasharray="3 4" opacity="0.7"/>')
    xr = hub + hl / 2 + 22
    s.append(f'<line x1="{xr:.1f}" y1="{y:.1f}" x2="{xr:.1f}" y2="{yf:.1f}" stroke="{INK2}" stroke-width="1.1" '
             f'marker-start="url(#arr2)" marker-end="url(#arr2)"/>')
    s.append(f'<text x="{(x_aft + x_nose) / 2:.1f}" y="{yd - 9:.1f}" text-anchor="middle" font-size="17" '
             f'fill="{INK2}" class="h">хребет {fnum(L)} м</text>')
    s.append(f'<text x="{xr + 9:.1f}" y="{(y + yf) / 2 + 6:.1f}" font-size="17" fill="{INK2}" class="h">'
             f'R {fnum(R)} м</text>')
    labels = [
        (hub - hl / 2 - 12, yf - hd / 2 + 6, "end", "жилой модуль · 0,5 g"),
        (hub + 14, y - vd / 2 - 16, "start", "ядро ARI"),
    ]
    return s, labels, k


def build():
    vals = json.loads((ROOT / "data" / "canon.json").read_text(encoding="utf-8"))["values"]
    defs, jup = jupiter(1095, 230, 250)
    ship_els, labels, k = ship(vals, 560, 1110, 300)
    figure = maya(275, 585, 330)
    lab = []
    for x, y, anchor, text in labels:
        lab.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="17" fill="{INK}" '
                   f'class="h">{text}</text>')
    # размер Майи
    top, bot = 585 - 330, 585
    lab += [
        f'<line x1="378" y1="{top}" x2="378" y2="{bot}" stroke="{INK2}" stroke-width="1.2" '
        f'marker-start="url(#tick)" marker-end="url(#tick)"/>',
        f'<text x="392" y="{(top + bot) / 2 + 6:.0f}" font-size="18" fill="{INK2}">1,7 м</text>',
        f'<line x1="150" y1="{bot}" x2="410" y2="{bot}" stroke="{INK2}" stroke-width="1.2"/>',
        f'<text x="275" y="{bot + 26}" text-anchor="middle" font-size="18" fill="{INK}" letter-spacing="1.5">'
        f'МАЙЯ</text>',
    ]
    title = [
        f'<text x="64" y="112" font-size="66" font-weight="700" fill="{INK}" letter-spacing="0.5">Maya in Transit'
        f'</text>',
        f'<text x="66" y="160" font-size="25" fill="{INK2}">2050-е. Майя одна летит к Юпитеру</text>',
        f'<text x="66" y="192" font-size="25" fill="{INK2}">и ведёт с борта влог.</text>',
        f'<text x="1172" y="606" text-anchor="end" font-size="15" fill="{INK2}" letter-spacing="1">'
        f'ВИКИ МИРА · ЧЕРТЕЖИ · РАСЧЁТЫ</text>',
    ]
    grid = (f'<pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" '
            f'fill="none" stroke="{GRID}" stroke-width="0.5" opacity="0.5"/></pattern>'
            f'<pattern id="g5" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M100 0H0V100" '
            f'fill="none" stroke="{GRID}" stroke-width="1" opacity="0.7"/></pattern>'
            f'<marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="9" markerHeight="9" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" fill="{INK}"/></marker>'
            f'<marker id="arr2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
            f'orient="auto-start-reverse"><path d="M0,1 L10,5 L0,9" fill="none" stroke="{INK2}" stroke-width="1.4"/>'
            f'</marker>'
            f'<marker id="tick" viewBox="0 0 10 2" refX="5" refY="1" markerWidth="14" markerHeight="3" '
            f'orient="auto"><rect width="10" height="2" fill="{INK2}" transform="rotate(90 5 1)"/></marker>')
    style = (f"<style>text{{font-family:{FONT};}} .h{{paint-order:stroke;stroke:{BG};stroke-width:5px;"
             f"stroke-linejoin:round;}}</style>")
    svg = "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" lang="ru">',
        "<title>Maya in Transit</title>",
        f"<defs>{style}{grid}{''.join(defs)}</defs>",
        f'<rect width="{W}" height="{H}" fill="{BG}"/>',
        f'<rect width="{W}" height="{H}" fill="url(#g)"/><rect width="{W}" height="{H}" fill="url(#g5)"/>',
        *jup, *ship_els, *figure, *lab, *title,
        f'<rect x="12" y="12" width="{W - 24}" height="{H - 24}" fill="none" stroke="{INK}" stroke-width="1.6"/>',
        "</svg>",
    ])
    out_svg = HERE / "og-card.svg"
    out_svg.write_text(svg + "\n", encoding="utf-8")
    print(f"записан: {out_svg.relative_to(ROOT)}", flush=True)
    render(out_svg, ROOT / "site" / "static" / "og-image.png")


def render(svg_path, png_path):
    chrome = next((c for c in CHROME if Path(c).exists() or shutil.which(c)), None)
    if not chrome:
        print("нет Chrome — PNG не обновлён", flush=True)
        return
    png_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        html = Path(tmp) / "card.html"
        html.write_text(f'<!doctype html><html><body style="margin:0;background:{BG}">'
                        f'{svg_path.read_text(encoding="utf-8")}</body></html>', encoding="utf-8")
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={W},{H}",
                        f"--screenshot={png_path}", html.as_uri()], check=True, capture_output=True)
    print(f"записан: {png_path.relative_to(ROOT)}", flush=True)


if __name__ == "__main__":
    sys.exit(build())
