"""Лист (f): вращение и искусственная гравитация — вид вдоль оси с носа, градиент пол–голова, Кориолис при ходьбе.

Показывает то, что записано на страницах ru/30-ship/artificial-gravity.md и ru/50-science/rotating-reference-frames.md:
весь корабль вращается вокруг O; жилой модуль на радиусе пола, противовес — напротив; a = ω²r; голова легче ног;
Кориолис вдоль модуля 0, поперёк — 2ωv. Все числа — из data/canon.json (canon.yaml + derived.yaml).
Направление вращения не задано — янтарным и «условно». Узкий лист с крупным кеглем: читается при ширине ~800 px.
"""
from __future__ import annotations

from bp import AMBER, BG, CAM, DIM, FILL, FILL2, INK, INK2, Sheet, View  # noqa: F401
import geom
from sheet_axes import T1, T2, T3, Z, arc_arrow, footer_big, out_of_page, panel, status_note

NAME = "rotation-gravity"
W, H = 1000, 1800


def render(c) -> Sheet:
    hb = geom.habitat(c)
    shp = geom.ship(c, hb)
    sh = Sheet(W, H, c.lang, c.s("title"), c.s("desc"))
    sh.heading(40, 60, c.s("title"), c.s("subtitle"), z=Z)
    _main(sh, c, hb, shp)
    _gradient(sh, c, hb, 40, 812, 920, 424)
    _coriolis(sh, c, hb, 40, 1254, 920, 380)
    footer_big(sh, c, "BP-06", [(c.s("draft2"), AMBER), (c.s("amber_legend"), AMBER)])
    return sh


def _main(sh: Sheet, c, hb, shp):
    """Вид А: вдоль оси вращения с носа (+X к зрителю). Жилой модуль под O — его «вниз» совпадает с низом листа."""
    v = c.v
    k = 9.0
    O = (500.0, 476.0)
    V = View(O[0], O[1], k, ux=(1, 0), uy=(0, -1))      # (поперёк, к противовесу) → лист
    sh.text((40, 142), c.s("a_title"), size=T1 + 1, weight="bold", color=CAM)
    sh.text((40, 164), c.s("a_sub"), size=T3, color=INK2)
    rf = shp.floor_r
    Ro, R = hb.Ro, hb.R
    ra = shp.hab_axis_r
    cw0, cw1 = shp.cw_r
    cwm = (cw0 + cw1) / 2

    # траектория пола — окружность радиуса пола
    sh.circle(O, V.L(rf), stroke=INK2, sw=1.0, dash="3 5", op=0.9)
    pt = V(-rf * 0.80, -rf * 0.60)
    sh.text((pt[0] - 10, pt[1] + 26), c.s("path"), size=T3, color=INK2, anchor="end")

    # фермы
    bw = shp.boom_w
    a, b = V(-bw / 2, cwm), V(bw / 2, 0)
    sh.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], stroke=INK, sw=1.1, fill=FILL)
    a, b = V(-bw / 2, 0), V(bw / 2, -ra)
    sh.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], stroke=INK, sw=1.1, fill=FILL)
    # хребет и баки за ним
    sh.circle(O, V.L(v("exterior.tanks.diameter") / 2), stroke=INK2, sw=1.0, dash="4 3", fill=BG)
    sh.circle(O, V.L(shp.d / 2) + 1, stroke=INK, sw=1.4, fill=FILL2)
    out_of_page(sh, O, r=6, color=INK)
    # противовес: ход балласта пунктиром
    for rr in (cw0, cw1):
        sh.circle(V(0, rr), V.L(shp.cw_d / 2), stroke=INK2, sw=0.9, dash="3 4")
    sh.circle(V(0, cwm), V.L(shp.cw_d / 2), stroke=INK, sw=1.6, fill=FILL2)
    # жилой модуль
    pc = V(0, -ra)
    sh.circle(pc, V.L(Ro), stroke=INK, sw=1.6, fill=FILL2)
    sh.circle(pc, V.L(R), stroke=INK2, sw=0.9)
    fy = V(0, -rf)[1]
    sh.line((pc[0] - V.L(hb.deck_half), fy), (pc[0] + V.L(hb.deck_half), fy), stroke=INK, sw=1.2)
    sh.person_front(pc[0] - 2, fy, k, v("maya.height"))
    # выноска к детали Б
    sh.circle(pc, V.L(Ro) + 16, stroke=CAM, sw=1.1, dash="4 3")
    tb = (pc[0] + V.L(Ro) + 26, pc[1] - V.L(Ro) - 14)
    sh.tag(tb, "Б" if c.lang == "ru" else "B", r=11, size=13)

    # вращение — дуги условного направления (против часовой при виде с носа)
    rr = V.L(rf + 3.6)
    arc_arrow(sh, O, rr, -34, 34, color=AMBER, sw=2.6)
    arc_arrow(sh, O, rr, 146, 214, color=AMBER, sw=2.6)
    sh.text((40, 214), c.s("spin", rpm=c.fv("ship.spin_rpm")), size=T1 + 1, weight="bold")
    sh.text((40, 238), c.s("spin2", t=c.fv("ship.spin_period"), w=c.fv("ship.spin_omega")), size=T2)
    sh.text((40, 260), c.s("spin3"), size=T3, color=INK2)
    sh.text((40, 284), c.s("dir"), size=T3, color=AMBER)

    # O
    sh.text((O[0] + 20, O[1] - 6), c.s("o"), size=T2, weight="bold")
    sh.text((O[0] + 20, O[1] + 14), c.s("o2"), size=T3, color=INK2)

    # радиусы: цепочка слева от ферм
    xd = O[0] - 30
    ycw, yfl = V(0, cwm)[1], V(0, -rf)[1]
    sh.line((O[0] - 8, ycw), (xd - 6, ycw), stroke=DIM, sw=0.7, op=0.8)
    sh.line((pc[0] - V.L(hb.deck_half), yfl), (xd - 6, yfl), stroke=DIM, sw=0.7, op=0.8)
    sh.line((O[0] - 10, O[1]), (xd - 6, O[1]), stroke=DIM, sw=0.7, op=0.8)
    sh.line((xd, O[1] - 2), (xd, ycw), stroke=DIM, sw=0.9, marker_start="ad", marker_end="ad")
    sh.line((xd, O[1] + 2), (xd, yfl), stroke=DIM, sw=0.9, marker_start="ad", marker_end="ad")
    ym = (O[1] + yfl) / 2
    sh.text((xd - 8, ym), c.s("r_floor", r=c.fv("habitat.floor_radius")), size=T2, weight="bold", anchor="middle",
            rot=-90)
    st = status_note(c, "habitat.floor_radius")
    if st:
        sh.text((xd - 28, ym), c.s("st_floor_r", st=st), size=T3, color=AMBER, anchor="middle", rot=-90)
    ym2 = (O[1] + ycw) / 2
    sh.text((xd - 8, ym2), c.s("r_cw", r=c.fv("exterior.counterweight.radius")), size=T2, weight="bold",
            anchor="middle", rot=-90)
    st2 = status_note(c, "exterior.counterweight.radius")
    if st2:
        sh.text((xd - 28, ym2), st2, size=T3, color=AMBER, anchor="middle", rot=-90)

    # подписи масс
    pcw = V(0, cwm)
    sh.text((pcw[0] + 26, pcw[1] - 6), c.s("cw"), size=T2, weight="bold")
    sh.text((pcw[0] + 26, pcw[1] + 14), c.s("cw2"), size=T3, color=INK2)
    sh.text((pc[0] + 54, pc[1] + 10), c.s("hab"), size=T2, weight="bold")
    sh.text((pc[0] + 54, pc[1] + 30), c.s("hab2"), size=T3, color=INK2)

    # a = ω²r на полу — справа внизу
    sh.text((40, 690), c.s("a_floor", g=c.fv("habitat.floor_gravity"), a=c.fv("habitat.floor_accel")),
            size=T2, weight="bold")
    sh.text((40, 710), c.s("a_floor2"), size=T3, color=INK2)
    sh.scale_bar(40, 760, k, [0, 10, 20], c.s("unit_m"), c.s("scale_a"), z=Z * 0.9)


def _gradient(sh: Sheet, c, hb, x, y, w, h):
    """Деталь Б: центростремительное ускорение на уровне пола и головы стоящей Майи."""
    v = c.v
    panel(sh, x, y, w, h, c.s("g_title"), c.s("g_sub"), color=CAM, tcolor=CAM)
    k = 92.0
    Ro, R, hh = hb.Ro, hb.R, hb.h
    cx = x + 200
    crown = y + 84
    fy = crown + (Ro + hh) * k
    V = View(cx, fy, k, ux=(1, 0), uy=(0, -1))
    ax = V(0, hh)
    hatch = sh.hatch_id("rg-shell", INK2, step=7, sw=0.8, op=0.5)
    sh.path(f"M {ax[0] - V.L(Ro)} {ax[1]} a {V.L(Ro)} {V.L(Ro)} 0 1 0 {2 * V.L(Ro)} 0 "
            f"a {V.L(Ro)} {V.L(Ro)} 0 1 0 {-2 * V.L(Ro)} 0 Z "
            f"M {ax[0] - V.L(R)} {ax[1]} a {V.L(R)} {V.L(R)} 0 1 1 {2 * V.L(R)} 0 "
            f"a {V.L(R)} {V.L(R)} 0 1 1 {-2 * V.L(R)} 0 Z", stroke="none", fill=hatch, extra=' fill-rule="evenodd"')
    sh.circle(ax, V.L(Ro), stroke=INK, sw=1.5)
    sh.circle(ax, V.L(R), stroke=INK, sw=2.0)
    a, b = V(-hb.deck_half, 0), V(hb.deck_half, -0.06)
    sh.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], stroke=INK, sw=1.2, fill=FILL2)
    hm = v("maya.height")
    pm = V(0.1, 0)
    sh.person_front(pm[0], pm[1], k, hm)
    head_y = V(0, hm)[1]
    # рост Майи
    xd = V(-0.55, 0)[0]
    sh.line((xd - 8, head_y), (pm[0] - 6, head_y), stroke=DIM, sw=0.7, op=0.8)
    sh.dim((xd, fy), (xd, head_y), 0, c.fv("maya.height"), size=T3, tick_ext=False)

    # стрелки к оси: длина ∝ ускорению
    ga, gh = v("habitat.floor_accel"), v("gravity.head_accel")
    L0 = 112.0
    x1, x2 = x + 450, x + 560
    for xx, yy in ((x1, fy), (x2, head_y)):
        sh.line((pm[0] + 22, yy), (xx + 10, yy), stroke=INK2, sw=0.8, dash="3 3")
    sh.arrow((x1, fy), (x1, fy - L0), color=INK, sw=3.0)
    sh.arrow((x2, head_y), (x2, head_y - L0 * gh / ga), color=INK, sw=3.0)
    sh.text((x1 + 14, fy - 30), c.s("g_floor", g=c.fv("habitat.floor_gravity")), size=T1 + 1, weight="bold")
    sh.text((x1 + 14, fy - 9), c.fv("habitat.floor_accel"), size=T3, color=INK2)
    sh.text((x2 + 14, head_y - 30), c.s("g_head", g=c.fv("gravity.head_g")), size=T1 + 1, weight="bold")
    sh.text((x2 + 14, head_y - 9), c.s("g_head2", a=c.fv("gravity.head_accel"), p=c.fv("gravity.gradient_head")),
            size=T3, color=INK2)
    # пояснение справа
    tx = x + 600
    ty = y + h - 150
    sh.text((tx, ty), c.s("g_1"), size=T2, weight="bold")
    sh.text((tx, ty + 22), c.s("g_2", h=c.fv("maya.height")), size=T3, color=INK2)
    sh.text((tx, ty + 42), c.s("g_3"), size=T3, color=INK2)
    sh.text((tx, ty + 70), c.s("g_4"), size=T3)
    sh.text((tx, ty + 90), c.s("g_5"), size=T3, color=INK2)
    sh.scale_bar(tx, y + h - 26, k, [0, 0.5, 1], c.s("unit_m"), "", z=Z * 0.9)


def _coriolis(sh: Sheet, c, hb, x, y, w, h):
    """Врезка В: Кориолис при ходьбе вдоль модуля (0) и поперёк (2ωv), знак — относительно вращения."""
    v = c.v
    panel(sh, x, y, w, h, c.s("c_title"), c.s("c_sub", v=c.fv("physics.walk_speed")), color=CAM, tcolor=CAM)
    # --- слева: вид сверху на пол ---
    sh.text((x + 16, y + 92), c.s("c_plan"), size=T3, color=INK2)
    k = 44.0
    L, fw = hb.L, v("layout.hull.floor_width")
    x0, yc = x + 40, y + 170
    sh.rect(x0, yc - fw / 2 * k, L * k, fw * k, stroke=INK, sw=1.6, fill=FILL)
    sh.line((x0 - 14, yc), (x0 + L * k + 22, yc), stroke=INK2, sw=1.0, dash="16 4 3 4")
    sh.text((x0 + L * k + 26, yc + 5), c.s("c_omega"), size=T3, color=INK2)
    sh.text((x0 + L * k - 4, yc - fw / 2 * k - 8), c.s("c_nose"), size=T3, color=INK2, anchor="end")
    # вдоль: стрелка по X
    sh.arrow((x0 + 40, yc + 22), (x0 + 150, yc + 22), color=INK, sw=2.6)
    sh.text((x0 + 40, yc + 12), "v", size=T3, weight="bold", italic=True)
    # поперёк: стрелка по Y
    xa = x0 + 205
    sh.arrow((xa, yc + fw / 2 * k - 6), (xa, yc - fw / 2 * k + 6), color=AMBER, sw=2.6, marker="aa")
    sh.text((xa + 8, yc - 18), "v", size=T3, weight="bold", italic=True, color=AMBER)
    ly = yc + fw / 2 * k + 34
    sh.text((x0 - 20, ly), c.s("c_along", a=c.fv("gravity.coriolis_along")), size=T2, weight="bold")
    sh.text((x0 - 20, ly + 20), c.s("c_along2"), size=T3, color=INK2)
    sh.text((x0 - 20, ly + 48), c.s("c_across", a=c.fv("gravity.coriolis_across"),
                                    p=c.fv("gravity.coriolis_across_frac")), size=T2, weight="bold", color=AMBER)
    sh.text((x0 - 20, ly + 68), c.s("c_across2"), size=T3, color=INK2)

    # --- справа: вид с носа ---
    kx = 44.0
    Ro, R, hh = hb.Ro, hb.R, hb.h
    cx = x + 690
    crown = y + 120
    fy = crown + (Ro + hh) * kx
    V = View(cx, fy, kx, ux=(1, 0), uy=(0, -1))
    ax = V(0, hh)
    sh.text((x + 500, y + 92), c.s("c_nose_view"), size=T3, color=INK2)
    sh.circle(ax, V.L(Ro), stroke=INK, sw=1.4, fill=FILL)
    sh.circle(ax, V.L(R), stroke=INK2, sw=1.0)
    sh.line(V(-hb.deck_half, 0), V(hb.deck_half, 0), stroke=INK, sw=1.4)
    sh.person_front(cx, fy, kx, v("maya.height"))
    # движение модуля при вращении — условно
    ty = crown - 14
    sh.arrow((cx - 70, ty), (cx + 70, ty), color=AMBER, sw=2.2, marker="aa")
    sh.text((cx + 80, ty + 5), c.s("c_move"), size=T3, color=AMBER)
    # шаг по ходу и против
    ya = fy - 10
    sh.arrow((cx + 12, ya), (cx + 46, ya), color=INK, sw=2.4)
    sh.arrow((cx - 12, ya), (cx - 46, ya), color=INK2, sw=2.4, marker="ai")
    by = V(0, hh - Ro)[1] + 30
    sh.text((x + 500, by), c.s("c_pro", p=c.fv("gravity.coriolis_across_frac")), size=T2, weight="bold")
    sh.text((x + 500, by + 22), c.s("c_retro", p=c.fv("gravity.coriolis_across_frac")), size=T2, weight="bold",
            color=INK2)
    sh.text((x + 500, by + 48), c.s("c_drop"), size=T3, color=INK2)
