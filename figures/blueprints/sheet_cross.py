"""Лист (c): поперечный разрез жилого модуля через главную кабину, вид в нос."""
from __future__ import annotations

from bp import AMBER, BG, CAM, DIM, FILL, FILL2, INK, INK2, WATER, Sheet, View, fnum  # noqa: F401
import geom

NAME = "habitat-cross-section"
W, H = 1460, 1080


def render(c) -> Sheet:
    hb = geom.habitat(c)
    v = c.v
    desk = v("layout.desk.x")
    x_cut = (desk[0] + desk[1]) / 2           # разрез по креслу
    sh = Sheet(W, H, c.lang, c.s("title"), c.s("desc"))
    k = 190.0
    cx, floor_y = 640.0, 700.0
    # вид в нос: +Y — влево на листе, +Z — вверх
    V = View(cx, floor_y, k, ux=(-1, 0), uy=(0, -1))
    R, Ro, h = hb.R, hb.Ro, hb.h
    ax = V(0, h)
    face = hb.floor_w / 2

    sh.heading(40, 58, c.s("title"), c.s("subtitle", x=c.m(x_cut)))

    # --- окно за плоскостью разреза (на носовой переборке) ---
    wc = v("layout.window.center_height")
    for (w_, h_), dash, op in (((v("habitat.window_width")[1], v("habitat.window_height")[1]), "7 4", 0.9),
                               ((v("habitat.window_width")[0], v("habitat.window_height")[0]), "2 4", 0.7)):
        a, b = V(w_ / 2, wc + h_ / 2), V(-w_ / 2, wc - h_ / 2)
        sh.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], stroke=INK2, sw=1.0, dash=dash, op=op)

    # --- оболочка: кольцо с штриховкой ---
    hatch = sh.hatch_id("shell", INK2, step=7, sw=0.8, op=0.55)
    sh.path(f"M {ax[0] - V.L(Ro)} {ax[1]} a {V.L(Ro)} {V.L(Ro)} 0 1 0 {2 * V.L(Ro)} 0 "
            f"a {V.L(Ro)} {V.L(Ro)} 0 1 0 {-2 * V.L(Ro)} 0 Z "
            f"M {ax[0] - V.L(R)} {ax[1]} a {V.L(R)} {V.L(R)} 0 1 1 {2 * V.L(R)} 0 "
            f"a {V.L(R)} {V.L(R)} 0 1 1 {-2 * V.L(R)} 0 Z", stroke="none", fill=hatch, extra=' fill-rule="evenodd"')
    sh.circle(ax, V.L(Ro), stroke=INK, sw=1.6)
    sh.circle(ax, V.L(R), stroke=INK, sw=2.2)
    sh.circle(ax, V.L(R + 0.035), stroke=INK, sw=0.8, op=0.8)

    clip = "clip-hull"
    sh.defs.append(f'<clipPath id="{clip}"><circle cx="{ax[0]}" cy="{ax[1]}" r="{V.L(R) - 1.2}"/></clipPath>')
    sh.add(f'<g clip-path="url(#{clip})">')
    # подпольные баки
    t_top, t_bot = -0.08, -0.08 - hb.tank_h
    tclip = "clip-tank"
    sh.defs.append(f'<clipPath id="{tclip}"><circle cx="{ax[0]}" cy="{ax[1]}" r="{V.L(R - 0.05)}"/></clipPath>')
    wh = sh.hatch_id("water", WATER, step=5, sw=0.9, angle=-45, op=0.55)
    sh.add(f'<g clip-path="url(#{tclip})">')
    for y0, y1 in ((1.3, 0.47), (0.43, -0.43), (-0.47, -1.3)):
        a, b = V(y0, t_top), V(y1, t_bot)
        sh.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], stroke=WATER, sw=1.1, fill=wh, rx=4)
    sh.add("</g>")
    # палуба
    a, b = V(R, 0), V(-R, -0.06)
    sh.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], stroke=INK, sw=1.2, fill=FILL2)
    # шкафы: фасады до front_h, наклонные верхние шкафы до края потолочной панели
    fh = hb.locker_front_h
    cp = hb.ceil_half - 0.07
    lk = sh.hatch_id("locker", INK2, step=10, sw=0.6, angle=90, op=0.25)
    for sgn in (1, -1):
        outline = [V(sgn * face, 0), V(sgn * face, fh), V(sgn * cp, hb.ceil), V(sgn * 1.6, hb.ceil),
                   V(sgn * 1.6, 0)]
        sh.poly(outline, stroke="none", fill=FILL)
        sh.poly(outline, stroke="none", fill=lk)
        sh.poly([V(sgn * face, 0), V(sgn * face, fh), V(sgn * cp, hb.ceil)], stroke=INK, sw=1.6, closed=False)
        for z in (0.45, 0.9, 1.3):
            sh.line(V(sgn * face, z), V(sgn * 1.6, z), stroke=INK2, sw=0.8, op=0.8)
        sh.line(V(sgn * (face + hb.locker_d), 0), V(sgn * (face + hb.locker_d), hb.ceil), stroke=INK2, sw=0.9,
                dash="5 4")
    # потолочная панель
    a, b = V(cp + 0.2, hb.ceil + 0.035), V(-cp - 0.2, hb.ceil)
    sh.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], stroke=INK, sw=1.2, fill=FILL2)
    for y in (-0.25, 0.25):
        p = V(y, hb.ceil)
        sh.rect(p[0] - 11, p[1], 22, 4, stroke="none", fill=INK, op=0.9)
    sh.circle(V(0, hb.ceil - 0.03), 4, stroke=INK, sw=1.0, fill=BG)
    sh.add("</g>")

    # --- рабочее место у стены +Y ---
    dh, dd = v("layout.desk.height"), v("layout.desk.depth")
    a, b = V(face, dh), V(face - dd, dh - 0.04)
    sh.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], stroke=INK, sw=1.4, fill=FILL2)
    w1, h1 = geom.display_size(v("habitat.display_primary")[1])
    zc = v("layout.display_primary.center_height")
    a, b = V(face, zc + h1 / 2), V(face - 0.05, zc - h1 / 2)
    sh.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], stroke=INK, sw=1.4, fill=INK2)
    # кресло: смотрит в +Y, спинка со стороны −Y
    sh_ = v("layout.chair.seat_height")
    sc = face - dd - 0.32
    a, b = V(sc + 0.23, sh_), V(sc - 0.23, sh_ - 0.07)
    sh.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], stroke=INK, sw=1.3, fill=FILL2, rx=3)
    back = [V(sc - 0.23, sh_ - 0.02), V(sc - 0.29, sh_ + 0.62), V(sc - 0.23, sh_ + 0.64), V(sc - 0.17, sh_ - 0.02)]
    sh.poly(back, stroke=INK, sw=1.3, fill=FILL2)
    sh.line(V(sc, sh_ - 0.07), V(sc, 0.06), stroke=INK, sw=2.2)
    sh.line(V(sc + 0.24, 0.02), V(sc - 0.24, 0.02), stroke=INK, sw=2.2)

    # --- Майя 1,7 м ---
    ym = -0.62
    hm = v("maya.height")
    p = V(ym, 0)
    sh.person_front(p[0], p[1], k, hm)

    # --- ось цилиндра ---
    sh.line(V(Ro + 0.25, h), V(-Ro - 0.25, h), stroke=INK2, sw=0.9, dash="16 4 3 4")
    sh.line(V(0, h - 0.15), V(0, h + 0.15), stroke=INK2, sw=0.9)

    # --- направления: к оси вращения и «вниз» ---
    top = V(0, h + Ro)
    sh.arrow((top[0], top[1] - 8), (top[0], 150), color=INK, sw=2.2)
    sh.text((top[0] + 14, 162), c.s("to_axis", r=c.fv("habitat.floor_radius")), size=13.5, weight="bold")
    sh.text((top[0] + 14, 180), c.s("to_axis2"), size=12, color=INK2)
    dx0 = V(-Ro, 0)[0] + 120
    sh.arrow((dx0, floor_y - 120), (dx0, floor_y - 10), color=INK, sw=2.4)
    sh.text((dx0 + 14, floor_y - 74), c.s("down", g=c.fv("habitat.floor_gravity"),
                                          a=c.fv("habitat.floor_accel")), size=13, weight="bold")
    sh.text((dx0 + 14, floor_y - 56), c.s("down2"), size=12, color=INK2)
    sh.text((dx0 + 14, floor_y - 38), c.s("head_g", g=c.fv("gravity.head_g"), f=c.fv("habitat.floor_gravity")),
            size=12, color=INK2)

    # --- размеры ---
    yd = -0.23
    sh.dim(V(yd, 0), V(yd, hb.ceil), 0, c.fv("layout.hull.ceiling_height"), tick_ext=False)
    # рост Майи
    yh = ym - 0.30
    sh.dim(V(yh, 0), V(yh, hm), 0, c.s("maya", h=c.fv("maya.height")), tick_ext=False, text_side=-1)
    # пол ниже оси и высота баков — справа снаружи
    xr = V(-Ro, 0)[0] + 36
    sh.line(V(-hb.deck_half, 0), (xr + 8, floor_y), stroke=DIM, sw=0.7, op=0.8)
    sh.line(V(-Ro - 0.25, h), (xr + 8, ax[1]), stroke=DIM, sw=0.7, op=0.8)
    sh.dim((xr, floor_y), (xr, ax[1]), 0, c.fv("layout.hull.floor_below_axis"), tick_ext=False, text_side=-1)
    tb = V(-0.43, t_bot)
    tt = V(-1.0, t_top)
    sh.line(tt, (xr + 8, tt[1]), stroke=DIM, sw=0.7, op=0.8)
    sh.line(tb, (xr + 8, tb[1]), stroke=DIM, sw=0.7, op=0.8)
    sh.dim((xr, tb[1]), (xr, tt[1]), 0, c.fv("layout.hull.underfloor_tank_height"), tick_ext=False, text_side=-1)
    # ширина пола — под модулем
    zb = h - Ro - 0.2
    sh.dim(V(face, 0), V(-face, 0), -(V.L(-zb)), c.fv("layout.hull.floor_width"), ext=8)
    # глубина шкафа (борт −Y, на высоте оси)
    sh.dim(V(-face, h + 0.35), V(-face - hb.locker_d, h + 0.35), 0, c.fv("layout.lockers.depth"), size=11,
           tick_ext=False)

    # --- выноски слева ---
    xl = V(Ro, 0)[0] - 30
    left = [
        (V(face - 0.025, zc + 0.12), 355, c.s("display", d=c.fv("habitat.display_primary"),
                                              z=c.fv("layout.display_primary.center_height"))),
        (V(face, 1.45), 300, c.s("hero_wall")),
        (V(face - dd / 2, dh), 455, c.s("desk", h=c.fv("layout.desk.height"))),
        (V(sc, sh_), 530, c.s("chair", h=c.fv("layout.chair.seat_height"))),
        (V(0.3, wc + v("habitat.window_height")[1] / 2), 245, c.s("window", z=c.fv("layout.window.center_height"))),
    ]
    for feat, ty, lab in left:
        sh.leader(feat, (xl, ty), lab, side="left")
    # --- выноски справа ---
    xrr = V(-Ro, 0)[0] + 120
    right = [
        (V(-0.1, hb.ceil + 0.02), 245, c.s("ceiling")),
        (V(-(face + cp) / 2 - 0.05, (fh + hb.ceil) / 2 + 0.03), 300, c.s("bins")),
        (V(-face - 0.12, 1.45), 395, c.s("lockers")),
        (V(-0.75, (t_top + t_bot) / 2), 790, c.s("tanks")),
        (V(-R * 0.6, h - R * 0.8), 835, c.s("pshell", d=c.fv("habitat.inner_diameter"))),
        (V(-Ro * 0.45, h - Ro * 0.89), 880, c.s("oshell", d=c.fv("exterior.habitat.outer_diameter"))),
    ]
    for feat, ty, lab in right:
        sh.leader(feat, (xrr, ty), lab, side="right")
    sh.text(V(-Ro - 0.3, h + 0.12), c.s("axis"), size=11.5, color=INK2)

    # --- оси ---
    ox, oy = 92, 790
    sh.arrow((ox, oy), (ox - 0, oy - 52), color=INK2, sw=1.4, marker="ai")
    sh.arrow((ox, oy), (ox - 52, oy), color=INK2, sw=1.4, marker="ai")
    sh.circle((ox, oy), 7, stroke=INK2, sw=1.2)
    sh.line((ox - 5, oy - 5), (ox + 5, oy + 5), stroke=INK2, sw=1.1)
    sh.line((ox - 5, oy + 5), (ox + 5, oy - 5), stroke=INK2, sw=1.1)
    sh.text((ox + 6, oy - 58), "+Z", size=12, color=INK2)
    sh.text((ox - 74, oy + 4), "+Y", size=12, color=INK2)
    sh.text((ox + 12, oy + 22), c.s("x_axis"), size=11, color=INK2)

    footer(sh, c, "BP-03")
    return sh


def footer(sh: Sheet, c, sheet_id: str, scale_m=(0, 0.5, 1, 1.5, 2), k=190.0):
    sh.scale_bar(40, sh.h - 110, k, list(scale_m), c.s("unit_m"), c.s("scale"))
    sh.text((40, sh.h - 40), c.s("draft"), size=11.5, color=AMBER)
    sh.title_block(sh.w - 470, sh.h - 140, 440, 112, c.s("project"), c.s("sheet_name"), sheet_id,
                   c.s("rev"), c.s("date"), c.s("canon_rev"))
