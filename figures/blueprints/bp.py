"""Чертёжная библиотека листов-синек: стиль, размерные линии, выноски, штамп, линейка, силуэт человека.

Единый стиль всех листов figures/blueprints: классическая синька (тёмно-синий фон, светлые линии) с собственным
фоном — лист одинаково читается в светлой и тёмной теме Obsidian. Координаты здесь — пиксели листа;
перевод метров в пиксели делает View.
"""
from __future__ import annotations

import math
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import canonlib  # noqa: E402

# ---------- палитра ----------
BG = "#0e2c4f"         # поле листа
GRID = "#2b5a8a"       # сетка
INK = "#eef5ff"        # основные линии и текст
INK2 = "#a9c8ec"       # тонкие линии, размеры, вторичный текст
DIM = "#c9defa"        # размерные линии
FILL = "#16395f"       # заливка тел (чуть светлее фона)
FILL2 = "#1d4673"      # заливка выделенных тел
WATER = "#6fc3ff"      # вода
AMBER = "#ffbe55"      # спорное: C-003, альтернативы
SAFE = "#ff7f6e"       # ARI ISOLATE, рубильник, жёсткая линия
CAM = "#8ee6ff"        # камеры и конусы обзора
FONT = "'Helvetica Neue', Helvetica, Arial, 'DejaVu Sans', sans-serif"


def fnum(x: float, lang: str, nd: int | None = None) -> str:
    """Число для подписи: ru — запятая, en — точка; лишние нули не пишем."""
    if nd is None:
        nd = 0
        for d in (0, 1, 2):
            if abs(round(x, d) - x) < 1e-9:
                nd = d
                break
        else:
            nd = 2
    return canonlib.format_number(round(x, nd), lang, nd)


class View:
    """Метры → пиксели. ux, uy — единичные векторы осей мира на листе (в пикселях на метр задаёт k)."""

    def __init__(self, ox: float, oy: float, k: float, ux=(1, 0), uy=(0, -1)):
        self.ox, self.oy, self.k, self.ux, self.uy = ox, oy, k, ux, uy

    def __call__(self, a: float, b: float) -> tuple[float, float]:
        return (self.ox + self.k * (a * self.ux[0] + b * self.uy[0]),
                self.oy + self.k * (a * self.ux[1] + b * self.uy[1]))

    def L(self, m: float) -> float:
        return m * self.k


def _f(v: float) -> str:
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def pts(points) -> str:
    return " ".join(f"{_f(x)},{_f(y)}" for x, y in points)


class Sheet:
    def __init__(self, w: int, h: int, lang: str, title: str, desc: str = ""):
        self.w, self.h, self.lang, self.title, self.desc = w, h, lang, title, desc
        self.els: list[str] = []
        self.defs: list[str] = []

    # ---------- примитивы ----------
    def add(self, s: str):
        self.els.append(s)

    @staticmethod
    def _st(stroke=INK, sw=1.2, fill="none", dash=None, op=None, cap=None, extra=""):
        s = f'stroke="{stroke}" stroke-width="{_f(sw)}" fill="{fill}"'
        if dash:
            s += f' stroke-dasharray="{dash}"'
        if op is not None:
            s += f' opacity="{_f(op)}"'
        if cap:
            s += f' stroke-linecap="{cap}"'
        return s + extra

    def line(self, p, q, stroke=INK, sw=1.2, dash=None, op=None, marker_end=None, marker_start=None, cap="round"):
        m = ""
        if marker_end:
            m += f' marker-end="url(#{marker_end})"'
        if marker_start:
            m += f' marker-start="url(#{marker_start})"'
        self.add(f'<line x1="{_f(p[0])}" y1="{_f(p[1])}" x2="{_f(q[0])}" y2="{_f(q[1])}" '
                 f'{self._st(stroke, sw, dash=dash, op=op, cap=cap)}{m}/>')

    def poly(self, points, stroke=INK, sw=1.2, fill="none", dash=None, closed=True, op=None, marker_end=None,
             join="round"):
        tag = "polygon" if closed else "polyline"
        m = f' marker-end="url(#{marker_end})"' if marker_end else ""
        self.add(f'<{tag} points="{pts(points)}" {self._st(stroke, sw, fill, dash, op)} '
                 f'stroke-linejoin="{join}"{m}/>')

    def rect(self, x, y, w, h, stroke=INK, sw=1.2, fill="none", dash=None, rx=0, op=None):
        if w < 0:
            x, w = x + w, -w
        if h < 0:
            y, h = y + h, -h
        r = f' rx="{_f(rx)}"' if rx else ""
        self.add(f'<rect x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}"{r} '
                 f'{self._st(stroke, sw, fill, dash, op)}/>')

    def circle(self, c, r, stroke=INK, sw=1.2, fill="none", dash=None, op=None):
        self.add(f'<circle cx="{_f(c[0])}" cy="{_f(c[1])}" r="{_f(r)}" {self._st(stroke, sw, fill, dash, op)}/>')

    def path(self, d, stroke=INK, sw=1.2, fill="none", dash=None, op=None, marker_end=None, extra=""):
        m = f' marker-end="url(#{marker_end})"' if marker_end else ""
        self.add(f'<path d="{d}" {self._st(stroke, sw, fill, dash, op)} stroke-linejoin="round"{m}{extra}/>')

    def text(self, p, s, size=13, color=INK, anchor="start", weight="normal", rot=0, halo=True, italic=False,
             spacing=None, lh=1.25):
        """Текст с ореолом цвета фона — читается поверх линий. Многострочный через \n."""
        lines = str(s).split("\n")
        tr = f' transform="rotate({_f(rot)} {_f(p[0])} {_f(p[1])})"' if rot else ""
        st = ' font-style="italic"' if italic else ""
        sp = f' letter-spacing="{_f(spacing)}"' if spacing is not None else ""
        cls = ' class="h"' if halo else ""
        out = (f'<text x="{_f(p[0])}" y="{_f(p[1])}" font-size="{_f(size)}" fill="{color}" '
               f'text-anchor="{anchor}" font-weight="{weight}"{st}{sp}{cls}{tr}>')
        if len(lines) == 1:
            out += escape(lines[0])
        else:
            for i, ln in enumerate(lines):
                dy = "0" if i == 0 else _f(size * lh)
                out += f'<tspan x="{_f(p[0])}" dy="{dy}">{escape(ln)}</tspan>'
        self.add(out + "</text>")

    # ---------- чертёжные элементы ----------
    def dim(self, p, q, off: float, label: str, size=12, ext=6, gap=3, color=DIM, text_shift=0.0, text_side=1,
            tick_ext=True):
        """Размер между точками p и q, вынесенный на off пикселей по нормали (нормаль — поворот p→q на −90°
        в экранных координатах: для p→q вправо нормаль смотрит вверх)."""
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(dx, dy)
        tx, ty = dx / L, dy / L
        nx, ny = ty, -tx
        a = (p[0] + nx * off, p[1] + ny * off)
        b = (q[0] + nx * off, q[1] + ny * off)
        sgn = 1 if off >= 0 else -1
        if tick_ext and abs(off) > gap:
            for s0 in (p, q):
                self.line((s0[0] + nx * gap * sgn, s0[1] + ny * gap * sgn),
                          (s0[0] + nx * (off + ext * sgn), s0[1] + ny * (off + ext * sgn)), stroke=color, sw=0.7,
                          op=0.8)
        self.line(a, b, stroke=color, sw=0.9, marker_start="ad", marker_end="ad")
        ang = math.degrees(math.atan2(dy, dx))
        if ang > 89.9:
            ang -= 180
        elif ang <= -90.1:
            ang += 180
        mx, my = (a[0] + b[0]) / 2 + tx * text_shift, (a[1] + b[1]) / 2 + ty * text_shift
        # «верх» повёрнутого текста; text_side=1 — подпись над линией, −1 — под ней
        upx, upy = math.sin(math.radians(ang)), -math.cos(math.radians(ang))
        d = 4 if text_side > 0 else -(size * 0.8 + 4)
        self.text((mx + upx * d, my + upy * d), label, size=size, color=INK, anchor="middle", rot=ang)

    def leader(self, feat, elbow, label, side="right", color=INK2, size=12.5, dot=True, tcolor=INK, shoulder=10,
               weight="normal"):
        """Выноска: точка на детали → излом → полка → текст."""
        if dot:
            self.circle(feat, 2.4, stroke="none", fill=color)
        end = (elbow[0] + (shoulder if side == "right" else -shoulder), elbow[1])
        self.poly([feat, elbow, end], stroke=color, sw=0.9, closed=False)
        anchor = "start" if side == "right" else "end"
        n = len(str(label).split("\n"))
        y0 = elbow[1] + size * 0.35 - (n - 1) * size * 1.25 / 2
        self.text((end[0] + (4 if side == "right" else -4), y0), label, size=size, color=tcolor, anchor=anchor,
                  weight=weight)

    def arrow(self, p, q, color=INK, sw=2.0, marker="aw", dash=None):
        self.line(p, q, stroke=color, sw=sw, marker_end=marker, dash=dash, cap="butt")

    def tag(self, c, s, color=CAM, r=9, size=11):
        """Кружок с буквой (камеры A/B/C)."""
        self.circle(c, r, stroke=color, sw=1.3, fill=BG)
        self.text((c[0], c[1] + size * 0.36), s, size=size, color=color, anchor="middle", weight="bold", halo=False)

    def hatch_id(self, name: str, color: str, step=6, sw=0.8, angle=45, op=0.7) -> str:
        pid = f"h-{name}"
        self.defs.append(
            f'<pattern id="{pid}" patternUnits="userSpaceOnUse" width="{step}" height="{step}" '
            f'patternTransform="rotate({angle})"><line x1="0" y1="0" x2="0" y2="{step}" stroke="{color}" '
            f'stroke-width="{sw}" opacity="{op}"/></pattern>')
        return f"url(#{pid})"

    def scale_bar(self, x, y, k, meters: list[float], unit: str, label: str, z: float = 1.0):
        """Линейка: чередующиеся ячейки, подписи делений, подпись «масштаб». z — множитель кегля."""
        x0 = x
        for i in range(len(meters) - 1):
            a, b = meters[i], meters[i + 1]
            self.rect(x0 + a * k, y, (b - a) * k, 6, stroke=INK, sw=0.9, fill=INK if i % 2 == 0 else BG)
        for m in meters:
            self.text((x0 + m * k, y + 20 * z), fnum(m, self.lang), size=11 * z, color=INK2, anchor="middle")
        self.text((x0 + meters[-1] * k + 12, y + 7), unit, size=11 * z, color=INK2)
        self.text((x0, y - 8), label, size=11 * z, color=INK2)

    def title_block(self, x, y, w, h, project, sheet_name, sheet_id, rev, date, small, z: float = 1.0):
        """Штамп: проект, имя листа, ревизия, дата. z — множитель кегля и отступов (w, h задаёт вызов)."""
        self.rect(x, y, w, h, stroke=INK, sw=1.4, fill=BG)
        r1 = y + h * 0.38
        self.line((x, r1), (x + w, r1), stroke=INK, sw=0.9)
        cx = x + w * 0.72
        self.line((cx, r1), (cx, y + h), stroke=INK, sw=0.9)
        self.text((x + 12, y + h * 0.38 - 12 * z), project, size=17 * z, weight="bold", spacing=1.2, halo=False)
        self.text((x + 12, r1 + 22 * z), sheet_name, size=13 * z, halo=False)
        self.text((x + 12, r1 + 42 * z), small, size=10.5 * z, color=INK2, halo=False)
        self.text((cx + 10, r1 + 20 * z), rev, size=12 * z, weight="bold", color=AMBER, halo=False)
        self.text((cx + 10, r1 + 38 * z), date, size=11.5 * z, color=INK2, halo=False)
        self.text((cx + 10, r1 + 55 * z), sheet_id, size=11.5 * z, color=INK2, halo=False)

    def heading(self, x, y, title, sub, z: float = 1.0):
        """Заголовок листа и подзаголовок; z — множитель кегля (крупнее для листов, читаемых с телефона)."""
        self.text((x, y), title, size=22 * z, weight="bold", spacing=0.4)
        if sub:
            self.text((x, y + 22 * z), sub, size=13 * z, color=INK2)

    # ---------- силуэты ----------
    def person_front(self, cx, floor_y, k, H, color=INK, fill=FILL2):
        """Человек анфас (или со спины) ростом H, cx — середина, floor_y — уровень пола (пиксели), k — px/м."""
        R = [(0.05, 1.47), (0.20, 1.41), (0.235, 1.10), (0.225, 0.80), (0.185, 0.80), (0.17, 1.10),
             (0.15, 1.00), (0.17, 0.88), (0.15, 0.48), (0.105, 0.06), (0.125, 0.0), (0.03, 0.0), (0.035, 0.46),
             (0.0, 0.80)]
        s = H / 1.7
        right = [(cx + x * k * s, floor_y - z * k * s) for x, z in R]
        left = [(cx - x * k * s, floor_y - z * k * s) for x, z in reversed(R)]
        self.poly(right + left, stroke=color, sw=1.1, fill=fill)
        self.circle((cx, floor_y - 1.585 * k * s), 0.105 * k * s, stroke=color, sw=1.1, fill=fill)

    def person_side(self, cx, floor_y, k, H, facing=1, color=INK, fill=FILL2):
        """Человек в профиль; facing=+1 — смотрит вправо."""
        P = [(-0.04, 1.47), (-0.105, 1.36), (-0.075, 1.05), (-0.115, 0.88), (-0.075, 0.60), (-0.075, 0.33),
             (-0.06, 0.0), (0.19, 0.0), (0.05, 0.08), (0.06, 0.45), (0.075, 0.52), (0.085, 0.80), (0.085, 1.00),
             (0.125, 1.25), (0.045, 1.47)]
        s = H / 1.7
        pp = [(cx + facing * x * k * s, floor_y - z * k * s) for x, z in P]
        self.poly(pp, stroke=color, sw=1.1, fill=fill)
        arm = [(-0.03, 1.40), (0.035, 1.40), (0.06, 0.83), (0.005, 0.83)]
        self.poly([(cx + facing * x * k * s, floor_y - z * k * s) for x, z in arm], stroke=color, sw=1.0, fill=fill)
        self.circle((cx + facing * 0.02 * k * s, floor_y - 1.585 * k * s), 0.105 * k * s, stroke=color, sw=1.1,
                    fill=fill)

    def camera(self, p, yaw_deg, hfov_deg, length_px, letter, flip_y=False, dashed=False):
        """Камера в плане: конус обзора и кружок с буквой. yaw — угол экрана (градусы, 0 — вправо, против часовой)."""
        a0 = math.radians(yaw_deg - hfov_deg / 2)
        a1 = math.radians(yaw_deg + hfov_deg / 2)
        sgn = 1 if flip_y else -1
        e0 = (p[0] + length_px * math.cos(a0), p[1] + sgn * length_px * math.sin(a0))
        e1 = (p[0] + length_px * math.cos(a1), p[1] + sgn * length_px * math.sin(a1))
        self.poly([p, e0, e1], stroke=CAM, sw=0.9, fill="none", dash="4 3")
        self.add(f'<polygon points="{pts([p, e0, e1])}" fill="{CAM}" opacity="0.10" stroke="none"/>')
        am = math.radians(yaw_deg)
        tip = (p[0] + 0.45 * length_px * math.cos(am), p[1] + sgn * 0.45 * length_px * math.sin(am))
        self.line(p, tip, stroke=CAM, sw=1.0, dash="2 3")
        self.tag(p, letter)

    # ---------- сборка ----------
    def svg(self) -> str:
        grid = (f'<pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">'
                f'<path d="M20 0H0V20" fill="none" stroke="{GRID}" stroke-width="0.5" opacity="0.45"/></pattern>'
                f'<pattern id="grid5" width="100" height="100" patternUnits="userSpaceOnUse">'
                f'<path d="M100 0H0V100" fill="none" stroke="{GRID}" stroke-width="0.8" opacity="0.55"/></pattern>')
        markers = "".join(
            f'<marker id="{mid}" viewBox="0 0 10 10" refX="{rx}" refY="5" markerWidth="{mw}" markerHeight="{mw}" '
            f'markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0,1.2 L10,5 L0,8.8 z" '
            f'fill="{col}"/></marker>'
            for mid, col, mw, rx in (("ad", DIM, 8, 10), ("aw", INK, 13, 8), ("aa", AMBER, 12, 8),
                                     ("ar", SAFE, 12, 8), ("ac", CAM, 11, 8), ("ai", INK2, 10, 8),
                                     ("awt", WATER, 12, 8)))
        style = (f"<style>text{{font-family:{FONT};}} .h{{paint-order:stroke;stroke:{BG};stroke-width:4px;"
                 f"stroke-linejoin:round;}}</style>")
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}" lang="{self.lang}" role="img">\n'
                f"<title>{escape(self.title)}</title>\n<desc>{escape(self.desc)}</desc>\n"
                f"<defs>{style}{grid}{markers}{''.join(self.defs)}</defs>\n"
                f'<rect width="{self.w}" height="{self.h}" fill="{BG}"/>\n'
                f'<rect width="{self.w}" height="{self.h}" fill="url(#grid)"/>\n'
                f'<rect width="{self.w}" height="{self.h}" fill="url(#grid5)"/>\n'
                f'<rect x="12" y="12" width="{self.w - 24}" height="{self.h - 24}" fill="none" stroke="{INK}" '
                f'stroke-width="1.6"/>\n'
                f'<rect x="17" y="17" width="{self.w - 34}" height="{self.h - 34}" fill="none" stroke="{INK}" '
                f'stroke-width="0.6" opacity="0.7"/>\n')
        return head + "\n".join(self.els) + "\n</svg>\n"


class Ctx:
    """Значения канона и строки листа для одного языка."""

    def __init__(self, vals: dict, strings: dict, sheet_key: str, lang: str):
        self.vals, self.lang = vals, lang
        self._s = strings["blueprints"][sheet_key]
        self._c = strings["blueprints"]["common"]

    def v(self, key):
        return self.vals[key]["value"]

    def fv(self, key, with_unit=True):
        return canonlib.format_value(self.vals[key], self.lang, with_unit=with_unit)

    def s(self, key, **kw):
        src = self._s if key in self._s else self._c
        txt = src[key][self.lang]
        return txt.format(**kw) if kw else txt

    def m(self, x: float) -> str:
        """Длина в метрах с единицей по языку (не меньше одного знака после запятой)."""
        nd = 1 if abs(round(x, 1) - x) < 1e-9 else 2
        return f"{fnum(x, self.lang, nd)} {self._c['unit_m'][self.lang]}"

    def rng(self, key) -> str:
        """Диапазон координат «a…b м» — читается лучше, чем «−2,4–−2,0 м» при отрицательных концах."""
        a, b = self.v(key)
        return f"{fnum(a, self.lang, 1)}…{fnum(b, self.lang, 1)} {self._c['unit_m'][self.lang]}"
