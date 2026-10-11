"""Лист (e): оси и системы координат — корабельная рамка (вид сбоку), локальная рамка модуля (разрез), сцена Blender.

Показывает ровно то, что записано на странице ru/30-ship/orientation-and-axes.md: +X — нос, по тяге; одна ось X у
хребта, вращения и цилиндра модуля; +Z — к оси вращения («вверх»), −Z — пол; Y — поперёк кабины. Нерешённое
(направление вращения, знак Y, вращение неба в окне, величина тяги) — янтарным и с пометкой.
Лист узкий и с крупным кеглем: читается при ширине ~800 px (телефон).
"""
from __future__ import annotations

import math

from bp import AMBER, BG, CAM, DIM, FILL, FILL2, INK, INK2, SAFE, Sheet, View  # noqa: F401
import geom

NAME = "ship-axes"
W, H = 1000, 1500

# кегли листов, читаемых с телефона (BP-05, BP-06)
T1, T2, T3 = 17, 15.5, 14.5
Z = 1.3          # множитель кегля заголовка, штампа и линеек


# ---------- общие помощники BP-05/06 ----------
def into_page(sh: Sheet, p, r=8.0, color=INK2):
    """Ось, уходящая от зрителя: ⊗."""
    sh.circle(p, r, stroke=color, sw=1.3, fill=BG)
    d = r * 0.7
    sh.line((p[0] - d, p[1] - d), (p[0] + d, p[1] + d), stroke=color, sw=1.2)
    sh.line((p[0] - d, p[1] + d), (p[0] + d, p[1] - d), stroke=color, sw=1.2)


def out_of_page(sh: Sheet, p, r=8.0, color=INK2):
    """Ось к зрителю: ⊙."""
    sh.circle(p, r, stroke=color, sw=1.3, fill=BG)
    sh.circle(p, 2.2, stroke="none", fill=color)


def arc_arrow(sh: Sheet, c, r, a0, a1, color=AMBER, sw=2.0, marker="aa", dash=None, ry=None):
    """Дуга окружности (или эллипса ry) от угла a0 к a1 (градусы, математические: 0 — вправо, против часовой
    на листе — положительное направление) со стрелкой на конце a1."""
    ry = r if ry is None else ry
    p0 = (c[0] + r * math.cos(math.radians(a0)), c[1] - ry * math.sin(math.radians(a0)))
    p1 = (c[0] + r * math.cos(math.radians(a1)), c[1] - ry * math.sin(math.radians(a1)))
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 0 if a1 > a0 else 1           # против часовой на экране — sweep 0
    sh.path(f"M{p0[0]:.2f},{p0[1]:.2f} A{r:.2f},{ry:.2f} 0 {large} {sweep} {p1[0]:.2f},{p1[1]:.2f}", stroke=color,
            sw=sw, marker_end=marker, dash=dash)


def status_note(c, key: str) -> str:
    """Пометка статуса канона для чисел, которые ещё не согласованы (draft/proposed), иначе пусто."""
    st = c.vals[key]["status"]
    return "" if st in ("canon", "frozen") else c.s(f"st_{st}")


def panel(sh: Sheet, x, y, w, h, title, sub=None, color=INK2, tcolor=INK):
    sh.rect(x, y, w, h, stroke=color, sw=1.1, fill=BG)
    sh.text((x + 16, y + 28), title, size=T1, weight="bold", color=tcolor)
    if sub:
        sh.text((x + 16, y + 50), sub, size=T3, color=INK2)


ZB = 1.1        # штамп BP-05/06


def footer_big(sh: Sheet, c, sheet_id: str, notes):
    """Нижнее поле листов BP-05/06: пометки слева от штампа (текст с \n, цвет), штамп внизу справа."""
    bw, bh = 440 * ZB, 112 * ZB
    y0 = sh.h - 28 - bh
    y = y0 + 18
    for txt, col in notes:
        sh.text((40, y), txt, size=T3, color=col, lh=1.3)
        y += (txt.count("\n") + 1) * T3 * 1.3 + 8
    sh.title_block(sh.w - 30 - bw, y0, bw, bh, c.s("project"), c.s("sheet_name"), sheet_id,
                   c.s("rev"), c.s("date"), c.s("canon_rev"), z=ZB)


# ---------- лист ----------
def render(c) -> Sheet:
    hb = geom.habitat(c)
    shp = geom.ship(c, hb)
    sh = Sheet(W, H, c.lang, c.s("title"), c.s("desc"))
    sh.heading(40, 60, c.s("title"), c.s("subtitle"), z=Z)
    _side(sh, c, hb, shp)
    _section(sh, c, hb)
    _blender(sh, c, 590, 846, 370, 222)
    _window(sh, c, 590, 1084, 370, 214)
    footer_big(sh, c, "BP-05", [(c.s("draft2"), AMBER), (c.s("amber_legend"), AMBER)])
    return sh


def _side(sh: Sheet, c, hb, shp):
    """Вид А: корабль сбоку (силуэт BP-01 без радиаторов и деталей), ось X, тяга, вращение, рамка модуля."""
    v = c.v
    k = 8.0
    x_nose, oy = 760.0, 430.0
    V = View(x_nose, oy, k, ux=(-1, 0), uy=(0, 1))       # (станция от носа, радиус: + к жилому модулю)
    sh.text((40, 142), c.s("a_title"), size=T1 + 1, weight="bold", color=CAM)
    sh.text((40, 164), c.s("a_sub"), size=T3, color=INK2)

    S = lambda key: v(f"exterior.{key}.station")  # noqa: E731
    Ls, d = shp.L, shp.d

    def box(s0, s1, r0, r1, **kw):
        p, q = V(s1, r0), V(s0, r1)
        sh.rect(p[0], p[1], q[0] - p[0], q[1] - p[1], **kw)

    # хребет
    sp = sh.hatch_id("ax-spine", INK2, step=9, sw=0.7, angle=45, op=0.6)
    box(0, Ls, -d / 2, d / 2, stroke=INK, sw=1.3, fill=sp)
    # носовая мачта
    c0, c1 = S("comms")
    box(c0, c1, -0.5, 0.5, stroke=INK, sw=1.2, fill=FILL2)
    for sgn in (1, -1):
        sh.line(V(c1 - 1.5, sgn * 0.5), V(c1 - 2.8, sgn * 1.8), stroke=INK, sw=1.1)
    # баки, реактор, двигатели
    t0, t1 = S("tanks")
    td = v("exterior.tanks.diameter")
    tl = (t1 - t0) / 3
    for i in range(3):
        a = t0 + i * tl + 0.15
        b = a + tl - 0.3
        p, q = V(b, -td / 2), V(a, td / 2)
        sh.rect(p[0], p[1], q[0] - p[0], q[1] - p[1], stroke=INK, sw=1.2, fill=FILL2, rx=V.L(td / 2) * 0.6)
    e0, e1 = S("reactor")
    rd = v("exterior.reactor.diameter")
    box(e0 + 0.6, e1, -rd / 2, rd / 2, stroke=INK, sw=1.2, fill=FILL2, rx=3)
    box(e0, e0 + 0.6, -rd * 0.75, rd * 0.75, stroke=INK, sw=1.4, fill=INK2)
    g0, g1 = S("propulsion")
    box(g0, g1 - 2.2, -1.4, 1.4, stroke=INK, sw=1.2, fill=FILL2)
    for rr in (-0.9, 0, 0.9):
        sh.poly([V(g1 - 2.2, rr - 0.25), V(g1, rr - 0.55), V(g1, rr + 0.55), V(g1 - 2.2, rr + 0.25)], stroke=INK,
                sw=1.0, fill=FILL)
    pe = V(g1, 0)
    sh.poly([(pe[0], pe[1] - 11), (pe[0] - 64, pe[1] - 26), (pe[0] - 64, pe[1] + 26), (pe[0], pe[1] + 11)],
            stroke=INK2, sw=1.0, dash="5 4", op=0.9)
    # ступица, фермы, противовес
    bw = shp.boom_w
    vd = v("exterior.ari_core.vault_diameter")
    core, cl = v("exterior.ari_core.station"), v("exterior.ari_core.vault_length")
    cw0, cw1 = shp.cw_r
    cwm = (cw0 + cw1) / 2
    hc_st = shp.hab_center
    for rr in (cw0, cw1):
        box(hc_st - shp.cw_len / 2, hc_st + shp.cw_len / 2, -(rr - shp.cw_d / 2), -(rr + shp.cw_d / 2),
            stroke=INK2, sw=0.8, dash="3 4")
    box(shp.hub - bw / 2, shp.hub + bw / 2, -vd / 2, -(cwm + 0.3), stroke=INK, sw=1.1, fill=FILL)
    box(hc_st + shp.cw_len / 2, shp.hub - bw / 2, -(cwm - 0.3), -(cwm + 0.3), stroke=INK, sw=1.1, fill=FILL)
    box(hc_st - shp.cw_len / 2, hc_st + shp.cw_len / 2, -(cwm - shp.cw_d / 2), -(cwm + shp.cw_d / 2),
        stroke=INK, sw=1.5, fill=FILL2, rx=5)
    Ro, Lo = hb.Ro, hb.Lo
    ra = shp.hab_axis_r
    hcz = shp.floor_r - v("layout.hatch.center_height")
    box(shp.hub - bw / 2, shp.hub + bw / 2, vd / 2, hcz + 0.6, stroke=INK, sw=1.1, fill=FILL)
    box(hc_st + Lo / 2, shp.hub - bw / 2, hcz - 0.4, hcz + 0.4, stroke=INK, sw=1.1, fill=FILL)
    box(core - cl / 2, core + cl / 2, -vd / 2, vd / 2, stroke=INK, sw=1.6, fill="#2a5d93", rx=2)
    # жилой модуль
    box(hc_st - Lo / 2, hc_st + Lo / 2, ra - Ro, ra + Ro, stroke=INK, sw=1.7, fill=FILL2, rx=5)
    sh.line(V(hc_st - Lo / 2 + 0.5, shp.floor_r), V(hc_st + Lo / 2 - 0.5, shp.floor_r), stroke=INK2, sw=1.0,
            dash="4 3")
    pm = V(hc_st - 1.2, shp.floor_r)
    sh.person_side(pm[0], pm[1], k, v("maya.height"), facing=1)

    # ось X — через весь корабль
    sh.line(V(Ls + 9.5, 0), V(-1.0, 0), stroke=INK2, sw=1.0, dash="22 5 4 5")
    pax = V((t1 + e0) / 2 + 6, 0)
    sh.text((pax[0], oy - 38), c.s("axis"), size=T2, weight="bold", anchor="middle")
    sh.text((pax[0], oy - 17), c.s("axis2"), size=T3, color=INK2, anchor="middle")

    # --- нос: +X и вращение ---
    pn = V(0, 0)
    xr0 = pn[0] + 12
    sh.arrow((pn[0] + 10, oy), (pn[0] + 100, oy), color=INK, sw=2.6)
    sh.text((pn[0] + 106, oy + 6), "+X", size=T1 + 1, weight="bold")
    # кольцо вокруг оси, вид чуть со стороны носа: ближняя половина слева (сплошная), дальняя — пунктир;
    # обход совпадает с мини-видом с носа (против часовой) — условно
    arc_arrow(sh, (pn[0] + 42, oy), 13, 280, 440, color=AMBER, sw=1.6, ry=34, marker=None, dash="3 3")
    arc_arrow(sh, (pn[0] + 42, oy), 13, 100, 262, color=AMBER, sw=2.2, ry=34)
    sh.text((xr0, 292), c.s("nose"), size=T1, weight="bold", spacing=1)
    sh.text((xr0, 313), c.s("nose2"), size=T3, color=INK2)
    sh.text((xr0, 352), c.s("spin"), size=T2, weight="bold")
    sh.text((xr0, 372), c.s("spin2", rpm=c.fv("ship.spin_rpm"), t=c.fv("ship.spin_period")), size=T3)
    # мини-вид с носа: направление вращения условно
    g = (pn[0] + 36, oy + 82)
    sh.circle(g, 22, stroke=INK2, sw=1.0, dash="3 3")
    out_of_page(sh, g, r=6)
    arc_arrow(sh, g, 22, 200, 470, color=AMBER, sw=1.8)
    sh.text((g[0] + 34, g[1] - 8), c.s("from_nose"), size=T3, color=INK2)
    sh.text((g[0] + 34, g[1] + 11), c.s("dir_cond"), size=T3, color=AMBER)
    sh.text((g[0] + 34, g[1] + 29), c.s("dir_cond2"), size=T3, color=AMBER)

    # --- корма, тяга, выхлоп ---
    pa = V(Ls, 0)
    sh.text((40, oy - 52), c.s("aft"), size=T1, weight="bold", spacing=1)
    sh.text((40, oy - 31), c.s("aft2"), size=T3, color=INK2)
    sh.text((40, oy + 50), c.s("exhaust"), size=T3, color=INK2)
    ty = oy + 44
    sh.arrow((pa[0] + 4, ty), (pa[0] + 92, ty), color=INK, sw=2.6)
    sh.text((pa[0] + 100, ty + 6), c.s("thrust"), size=T2, weight="bold")

    # --- противовес ---
    pcw = V(hc_st - shp.cw_len / 2 - 1.0, -cwm)
    sh.text((pcw[0], pcw[1] + 5), c.s("cw"), size=T3)

    # --- R пола — слева от фермы ---
    xr = V(shp.hub + 2.6, 0)[0]
    yf = V(0, shp.floor_r)[1]
    sh.line(V(hc_st + Lo / 2 - 0.3, shp.floor_r), (xr - 8, yf), stroke=DIM, sw=0.7, op=0.8)
    sh.line((xr, oy + 6), (xr, yf), stroke=DIM, sw=0.9, marker_start="ad", marker_end="ad")
    ym = (oy + yf) / 2
    sh.text((xr - 8, ym), c.s("radius", r=c.fv("habitat.floor_radius")), size=T2, weight="bold", anchor="middle",
            rot=-90)
    st = status_note(c, "habitat.floor_radius")
    if st:
        sh.text((xr - 28, ym), c.s("st_floor_r", st=st), size=T3, color=AMBER, anchor="middle", rot=-90)

    # --- рамка модуля у самого модуля ---
    phf = V(hc_st + Lo / 2, ra - Ro)            # корма модуля, верх
    phn = V(hc_st - Lo / 2, ra - Ro)            # нос модуля, верх
    zx = phn[0] + 22
    sh.arrow((zx, phn[1] - 4), (zx, phn[1] - 66), color=INK, sw=2.2)
    sh.text((zx + 10, phn[1] - 52), c.s("z_up"), size=T2, weight="bold")
    sh.text((zx + 10, phn[1] - 33), c.s("z_up2"), size=T3, color=INK2)
    pf = V(hc_st + 1.4, ra + Ro)
    sh.arrow((pf[0], pf[1] + 2), (pf[0], pf[1] + 42), color=INK, sw=2.6)
    sh.text((pf[0] - 10, pf[1] + 34), c.s("down_a", g=c.fv("habitat.floor_gravity")), size=T2, weight="bold",
            anchor="end")
    # окно → +X
    wc_r = shp.floor_r - v("layout.window.center_height")
    pw = V(hc_st - Lo / 2, wc_r)
    sh.line((pw[0], pw[1] - 4), (pw[0], pw[1] + 4), stroke=CAM, sw=3)
    sh.arrow((pw[0] + 3, pw[1]), (pw[0] + 46, pw[1]), color=CAM, sw=2.0, marker="ac")
    sh.text((pw[0] + 52, pw[1] + 5), c.s("window"), size=T3, color=CAM)
    py_ = (phn[0] + 16, V(0, ra + Ro)[1] + 24)
    into_page(sh, py_, r=7, color=INK)
    sh.text((py_[0] + 14, py_[1] + 5), c.s("y_away"), size=T3)
    sh.text((py_[0] - 7, py_[1] + 28), c.s("hab"), size=T3, color=INK2)

    # --- тяга и «низ»; три рамки; линейка ---
    _thrust(sh, c, 40, 520, 410, 206)
    _frames(sh, c, 40, 206)
    sh.scale_bar(470, 742, k, [0, 10, 20], c.s("unit_m"), c.s("scale_a"), z=Z * 0.9)


def _frames(sh: Sheet, c, x, y):
    """Три рамки — короткая таблица (страница, раздел «Три рамки»)."""
    sh.text((x, y), c.s("frames"), size=T2, weight="bold", color=INK2)
    rows = [("f_ship", "f_ship2"), ("f_local", "f_local2"), ("f_sky", "f_sky2")]
    yy = y + 27
    for a, b in rows:
        sh.text((x, yy), c.s(a), size=T3, weight="bold")
        sh.text((x, yy + 19), c.s(b), size=T3, color=INK2)
        yy += 46


def _thrust(sh: Sheet, c, x, y, w, h):
    """Тяга и «низ»: эффективный «вниз» наклоняется к корме; величина тяги не задана (C-004)."""
    panel(sh, x, y, w, h, c.s("thr_title"))
    o = (x + 92, y + 70)
    L = 96.0
    tilt = 0.32                                   # условный наклон, величина не задана
    sh.arrow(o, (o[0], o[1] + L), color=INK, sw=2.4)
    sh.arrow(o, (o[0] - L * tilt, o[1]), color=AMBER, sw=2.0, marker="aa", dash="5 3")
    sh.line((o[0] - L * tilt, o[1]), (o[0] - L * tilt, o[1] + L), stroke=INK2, sw=0.8, dash="2 3")
    sh.line((o[0], o[1] + L), (o[0] - L * tilt, o[1] + L), stroke=INK2, sw=0.8, dash="2 3")
    sh.arrow(o, (o[0] - L * tilt, o[1] + L), color=INK2, sw=2.0, marker="ai", dash="6 3")
    sh.text((o[0] + 10, o[1] + L - 4), "−Z", size=T3, weight="bold")
    sh.text((o[0] - L * tilt - 6, o[1] - 8), "−X", size=T3, color=AMBER, anchor="middle")
    tx = x + 150
    sh.text((tx, y + 78), c.s("thr_1", a=c.fv("habitat.floor_accel")), size=T3)
    sh.text((tx, y + 102), c.s("thr_2"), size=T3, color=AMBER)
    sh.text((tx, y + 126), c.s("thr_3"), size=T3, color=INK2)
    sh.text((tx, y + 145), c.s("thr_4", a=c.fv("habitat.floor_accel")), size=T3, color=INK2)
    sh.text((x + 16, y + h - 16), c.s("thr_5"), size=T3, color=AMBER)


def _section(sh: Sheet, c, hb):
    """Вид Б: поперечный разрез модуля в локальной рамке (упрощённый BP-03), вид в нос."""
    v = c.v
    y0 = 800
    sh.text((40, y0), c.s("b_title"), size=T1 + 1, weight="bold", color=CAM)
    sh.text((40, y0 + 22), c.s("b_sub"), size=T3, color=INK2)
    k = 84.0
    R, Ro, h = hb.R, hb.Ro, hb.h
    cx = 250.0
    crown_y = 912.0
    floor_y = crown_y + (Ro + h) * k
    V = View(cx, floor_y, k, ux=(-1, 0), uy=(0, -1))      # (Y, Z): +Y влево, +Z вверх
    ax = V(0, h)
    # окно за плоскостью разреза
    wc = v("layout.window.center_height")
    ww, wh = v("habitat.window_width")[1], v("habitat.window_height")[1]
    a, b = V(ww / 2, wc + wh / 2), V(-ww / 2, wc - wh / 2)
    sh.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], stroke=CAM, sw=1.1, dash="6 4", op=0.9)
    # оболочка
    hatch = sh.hatch_id("ax-shell", INK2, step=7, sw=0.8, op=0.5)
    sh.path(f"M {ax[0] - V.L(Ro)} {ax[1]} a {V.L(Ro)} {V.L(Ro)} 0 1 0 {2 * V.L(Ro)} 0 "
            f"a {V.L(Ro)} {V.L(Ro)} 0 1 0 {-2 * V.L(Ro)} 0 Z "
            f"M {ax[0] - V.L(R)} {ax[1]} a {V.L(R)} {V.L(R)} 0 1 1 {2 * V.L(R)} 0 "
            f"a {V.L(R)} {V.L(R)} 0 1 1 {-2 * V.L(R)} 0 Z", stroke="none", fill=hatch, extra=' fill-rule="evenodd"')
    sh.circle(ax, V.L(Ro), stroke=INK, sw=1.5)
    sh.circle(ax, V.L(R), stroke=INK, sw=2.0)
    # палуба
    dh = hb.deck_half
    a, b = V(dh, 0), V(-dh, -0.06)
    sh.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], stroke=INK, sw=1.2, fill=FILL2)
    # Майя
    p = V(-0.55, 0)
    sh.person_front(p[0], p[1], k, v("maya.height"))
    # ось цилиндра
    sh.line(V(Ro + 0.2, h), V(-Ro - 0.2, h), stroke=INK2, sw=0.9, dash="16 4 3 4")

    # --- оси локальной рамки: начало на полу по оси кабины ---
    o = V(0, 0)
    top = V(0, h + Ro)
    sh.line(o, (o[0], top[1]), stroke=INK, sw=1.3, dash="7 4")
    sh.arrow((o[0], top[1]), (o[0], top[1] - 50), color=INK, sw=2.6)
    sh.text((o[0] - 14, top[1] - 34), "+Z", size=T1 + 2, weight="bold", anchor="end")
    sh.text((o[0] + 14, top[1] - 38), c.s("to_axis", r=c.fv("habitat.floor_radius")), size=T2, weight="bold")
    sh.text((o[0] + 14, top[1] - 18), c.s("to_axis2"), size=T3, color=INK2)
    bot = V(0, h - Ro)
    sh.arrow((o[0], o[1] + 4), (o[0], bot[1] + 46), color=INK, sw=2.6)
    sh.text((o[0] - 14, bot[1] + 40), "−Z", size=T1 + 2, weight="bold", anchor="end")
    sh.text((o[0] + 14, bot[1] + 24), c.s("down", g=c.fv("habitat.floor_gravity"), a=c.fv("habitat.floor_accel")),
            size=T2, weight="bold")
    sh.text((o[0] + 14, bot[1] + 44), c.s("down2"), size=T3, color=INK2)
    # +Y влево (вид в нос), −Y вправо
    xl, xrr = 56.0, V(-Ro - 0.15, 0)[0]
    sh.arrow(o, (xl, o[1]), color=INK, sw=2.2)
    sh.line(o, (xrr, o[1]), stroke=INK, sw=1.2, dash="7 4")
    sh.text((xl + 2, o[1] - 12), "+Y", size=T1 + 2, weight="bold")
    sh.text((xrr + 6, o[1] + 6), "−Y", size=T1, weight="bold", color=INK2)
    into_page(sh, o, r=9, color=INK)
    sh.text((xl + 2, o[1] + 26), c.s("y_across"), size=T3, color=INK2)
    # подписи справа от разреза
    xr = V(-Ro, 0)[0] + 16
    sh.text((xr, V(0, h + 0.62)[1]), c.s("x_into"), size=T3, color=INK)
    pw = V(-ww / 2, wc + wh / 2)
    sh.leader((pw[0] - 2, pw[1] + 4), (xr - 6, V(0, h + 1.15)[1]), c.s("win_b"), side="right", color=CAM,
              tcolor=CAM, size=T3)
    sh.text((40, 1300), c.s("y_note"), size=T3, color=AMBER, lh=1.3)
    sh.scale_bar(xr + 30, floor_y + 62, k, [0, 0.5, 1], c.s("unit_m"), c.s("scale_b"), z=Z * 0.9)


def _blender(sh: Sheet, c, x, y, w, h):
    panel(sh, x, y, w, h, c.s("bl_title"), c.s("bl_sub"))
    o = (x + 64, y + 164)
    sh.arrow(o, (o[0] + 58, o[1]), color=INK, sw=1.8)
    sh.arrow(o, (o[0] - 32, o[1] + 24), color=INK, sw=1.8)
    sh.arrow(o, (o[0], o[1] - 58), color=INK, sw=1.8)
    sh.text((o[0] + 62, o[1] + 6), "X", size=T2, weight="bold")
    sh.text((o[0] - 42, o[1] + 34), "Y", size=T2, weight="bold")
    sh.text((o[0] + 8, o[1] - 56), "Z", size=T2, weight="bold")
    sh.arrow((o[0] + 24, o[1] - 34), (o[0] + 24, o[1] - 2), color=INK2, sw=1.6, marker="ai")
    sh.text((o[0] + 32, o[1] - 16), "g", size=T3, color=INK2, italic=True)
    tx = x + 150
    sh.text((tx, y + 90), "Scene Gravity", size=T3, color=INK2)
    sh.text((tx, y + 111), c.s("bl_grav", gz=c.fv("production.blender_gravity_z")), size=T2, weight="bold")
    sh.text((tx, y + 140), c.s("bl_unit", u=c.fv("production.blender_unit")), size=T2)
    sh.text((tx, y + 170), c.s("bl_static"), size=T3, color=INK2)
    sh.text((tx, y + 189), c.s("bl_static2", g=c.fv("habitat.floor_gravity")), size=T3, color=INK2)


def _window(sh: Sheet, c, x, y, w, h):
    panel(sh, x, y, w, h, c.s("w_title"), c.s("w_sub"), color=CAM, tcolor=CAM)
    gc = (x + 72, y + 134)
    ww, wh = 104.0, 62.0
    sh.rect(gc[0] - ww / 2, gc[1] - wh / 2, ww, wh, stroke=CAM, sw=1.6, fill=FILL, rx=6)
    for r_, a0 in ((16, 30), (26, 210)):
        arc_arrow(sh, gc, r_, a0, a0 + 120, color=AMBER, sw=1.4, dash="4 3")
    sh.circle(gc, 3.5, stroke="none", fill=INK)
    for dx, dy in ((-36, -17), (32, 20), (38, -19), (-28, 19)):
        sh.circle((gc[0] + dx, gc[1] + dy), 1.6, stroke="none", fill=INK2)
    tx = x + 140
    sh.text((tx, y + 90), c.s("w_1"), size=T3)
    sh.text((tx, y + 109), c.s("w_2"), size=T3)
    sh.text((tx, y + 137), c.s("w_3"), size=T3, color=AMBER)
    sh.text((tx, y + 156), c.s("w_4", t=c.fv("habitat.window_image_period")), size=T3, color=AMBER)
    sh.text((tx, y + 184), c.s("w_5"), size=T3, color=AMBER)
