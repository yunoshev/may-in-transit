"""Лист (d): продольный разрез жилого модуля по оси кабины (Y = 0), вид на +Y (геройскую стену), нос справа."""
from __future__ import annotations

from bp import AMBER, BG, CAM, DIM, FILL, FILL2, INK, INK2, SAFE, WATER, Sheet, View  # noqa: F401
import geom
from sheet_cross import footer

NAME = "habitat-long-section"
W, H = 1560, 1140


def render(c) -> Sheet:
    hb = geom.habitat(c)
    v = c.v
    sh = Sheet(W, H, c.lang, c.s("title"), c.s("desc"))
    k = 125.0
    ox, oy = 772.0, 725.0                      # X = 0 и пол
    V = View(ox, oy, k, ux=(1, 0), uy=(0, -1))  # (X, Z) → лист
    R, Ro, L, Lo, h = hb.R, hb.Ro, hb.L, hb.Lo, hb.h
    z = hb.zones
    top_in, bot_in, top_out, bot_out = h + R, h - R, h + Ro, h - Ro
    face = hb.floor_w / 2

    sh.heading(40, 58, c.s("title"), c.s("subtitle"))

    def box(x0, x1, z0, z1, **kw):
        p, q = V(x0, z1), V(x1, z0)
        sh.rect(p[0], p[1], q[0] - p[0], q[1] - p[1], **kw)

    # --- оболочка в разрезе ---
    hatch = sh.hatch_id("shell", INK2, step=7, sw=0.8, op=0.55)
    o1, o2 = V(-Lo / 2, top_out), V(Lo / 2, bot_out)
    i1, i2 = V(-L / 2, top_in), V(L / 2, bot_in)
    rr = V.L(0.3)
    outer = (f"M{o1[0] + rr},{o1[1]} H{o2[0] - rr} Q{o2[0]},{o1[1]} {o2[0]},{o1[1] + rr} V{o2[1] - rr} "
             f"Q{o2[0]},{o2[1]} {o2[0] - rr},{o2[1]} H{o1[0] + rr} Q{o1[0]},{o2[1]} {o1[0]},{o2[1] - rr} "
             f"V{o1[1] + rr} Q{o1[0]},{o1[1]} {o1[0] + rr},{o1[1]} Z")
    sh.path(outer + f" M{i1[0]},{i1[1]} V{i2[1]} H{i2[0]} V{i1[1]} Z", stroke="none", fill=hatch,
            extra=' fill-rule="evenodd"')

    # --- окно в носовой переборке ---
    wc = v("layout.window.center_height")
    hmin, hmax = v("habitat.window_height")
    p, q = V(L / 2 - 0.02, wc + hmax / 2), V(Lo / 2 + 0.02, wc - hmax / 2)
    sh.rect(p[0], p[1], q[0] - p[0], q[1] - p[1], stroke="none", fill=BG)
    for xx in (L / 2 + 0.12, L / 2 + 0.2):
        sh.line(V(xx, wc + hmax / 2), V(xx, wc - hmax / 2), stroke=CAM, sw=1.2)
    for s in (1, -1):
        sh.line(V(L / 2, wc + s * hmax / 2), V(Lo / 2, wc + s * hmax / 2), stroke=INK, sw=1.2)
        sh.line(V(L / 2 - 0.1, wc + s * hmin / 2), V(L / 2, wc + s * hmin / 2), stroke=INK2, sw=1.0, dash="3 2")
    # шторка — снаружи, поднята (положение «внешняя или внутренняя» не решено)
    box(Lo / 2 + 0.03, Lo / 2 + 0.11, wc + hmax / 2 + 0.05, wc + hmax / 2 + 0.75, stroke=INK2, sw=1.0, dash="4 3")

    # --- люк по SPEC: кормовая переборка, туннель, колено, ферма ---
    hd, hc = v("layout.hatch.diameter"), v("layout.hatch.center_height")
    ex, bw = v("exterior.boom.elbow_x"), v("exterior.boom.width")
    p, q = V(-Lo / 2 - 0.02, hc + hd / 2), V(-L / 2 + 0.02, hc - hd / 2)
    sh.rect(p[0], p[1], q[0] - p[0], q[1] - p[1], stroke="none", fill=BG)
    for s in (1, -1):
        sh.line(V(-Lo / 2, hc + s * hd / 2), V(-L / 2, hc + s * hd / 2), stroke=INK, sw=1.4)
    zb_top = 4.45
    boom = [V(-Lo / 2, hc + hd / 2), V(ex + bw / 2, hc + hd / 2), V(ex + bw / 2, zb_top), V(ex - bw / 2, zb_top),
            V(ex - bw / 2, hc - hd / 2 - 0.1), V(ex + bw / 2 - 0.25, hc - hd / 2), V(-Lo / 2, hc - hd / 2)]
    sh.poly(boom, stroke=INK, sw=1.4, fill=FILL)
    _break(sh, V(ex - bw / 2 - 0.1, zb_top), V(ex + bw / 2 + 0.1, zb_top), INK)
    # линия ARI ISOLATE: от панели по кабине к ферме (жёсткий провод)
    # вариант C-003: люк в своде над тамбуром, шахта к ферме
    axh = v("layout.hatch.alt_ceiling_x")
    p, q = V(axh - hd / 2, top_out + 0.02), V(axh + hd / 2, top_in - 0.02)
    sh.rect(p[0], p[1], q[0] - p[0], q[1] - p[1], stroke="none", fill=BG)
    for s in (-1, 1):
        sh.line(V(axh + s * hd / 2, top_in), V(axh + s * hd / 2, top_out), stroke=AMBER, sw=1.3, dash="5 3")
        sh.line(V(axh + s * bw / 2, top_out), V(axh + s * bw / 2, zb_top), stroke=AMBER, sw=1.3, dash="7 4")
    sh.line(V(axh - hd / 2, top_in), V(axh + hd / 2, top_in), stroke=AMBER, sw=1.6, dash="5 3")
    _break(sh, V(axh - bw / 2 - 0.1, zb_top), V(axh + bw / 2 + 0.1, zb_top), AMBER)

    # --- палуба и подпольные баки ---
    box(-L / 2, L / 2, -0.06, 0, stroke=INK, sw=1.2, fill=FILL2)
    wh = sh.hatch_id("water", WATER, step=5, sw=0.9, angle=-45, op=0.55)
    t_top, t_bot = -0.08, -0.08 - hb.tank_h
    tanks = [(z["stasis"][0], z["stasis"][1]), (z["galley_storage"][0], z["main_cabin"][0] + 0.5),
             (z["main_cabin"][0] + 0.5, z["window_bay"][0])]
    for a, b in tanks:
        box(a + 0.03, b - 0.03, t_bot, t_top, stroke=WATER, sw=1.1, fill=wh, rx=4)
        pc = V((a + b) / 2, (t_top + t_bot) / 2)
        sh.text((pc[0], pc[1] + 4), c.s("water"), size=11, color=WATER, anchor="middle")
    # под стеной СЖО и тамбуром — оборудование
    box(z["vestibule"][0] + 0.05, z["eclss_wall"][1] - 0.05, t_bot, t_top, stroke=INK2, sw=0.9, dash="4 3")

    # --- потолочная панель (над тамбуром — открытый свод под люк-вариант) ---
    box(z["eclss_wall"][0], L / 2, hb.ceil, hb.ceil + 0.035, stroke=INK, sw=1.1, fill=FILL2)

    # --- вид на стену +Y за плоскостью разреза ---
    lk = sh.hatch_id("lk", INK2, step=9, sw=0.6, angle=90, op=0.28)
    fh = hb.locker_front_h
    mc, gs = z["main_cabin"], z["galley_storage"]
    box(gs[0], mc[1], 0, fh, stroke=INK2, sw=0.9, fill=lk)            # фасады нижних шкафов
    box(gs[0], mc[1], fh, hb.ceil, stroke=INK2, sw=0.9, fill=FILL)    # верхние шкафы (наклонные)
    for xx in (0.4, 0.8, 1.3, 1.8, 2.2):
        sh.line(V(xx, fh), V(xx, hb.ceil), stroke=INK2, sw=0.7, op=0.7)
    # камбуз
    gh = v("layout.galley.counter_height")
    box(gs[0] + 0.02, gs[1] - 0.02, 0, gh, stroke=INK, sw=1.2, fill=FILL2)
    box(gs[0] + 0.02, gs[1] - 0.02, gh, gh + 0.04, stroke=INK, sw=1.2, fill=INK2)
    for zz in (0.3, 0.6):
        sh.line(V(gs[0] + 0.05, zz), V(gs[1] - 0.05, zz), stroke=INK2, sw=0.8)
    # стол, дисплеи, панель ARI ISOLATE, камера C
    d0, d1 = v("layout.desk.x")
    dh = v("layout.desk.height")
    box(d0, d1, dh - 0.04, dh, stroke=INK, sw=1.4, fill=FILL2)
    sh.line(V(d0 + 0.05, dh - 0.04), V(d0 + 0.05, 0), stroke=INK, sw=1.2)
    for key, rng in (("primary", "habitat.display_primary"), ("secondary", "habitat.display_secondary")):
        w_, h_ = geom.display_size(v(rng)[1])
        xc, zc = v(f"layout.display_{key}.center_x"), v(f"layout.display_{key}.center_height")
        box(xc - w_ / 2, xc + w_ / 2, zc - h_ / 2, zc + h_ / 2, stroke=INK, sw=1.4, fill="#22507f")
        w2, h2 = geom.display_size(v(rng)[0])
        box(xc - w2 / 2, xc + w2 / 2, zc - h2 / 2, zc + h2 / 2, stroke=INK2, sw=0.8, dash="3 3")
    px, pz = v("layout.ari_isolate_panel.x"), v("layout.ari_isolate_panel.height")
    box(px - 0.12, px + 0.12, pz - 0.05, pz + 0.05, stroke=SAFE, sw=1.4, fill=BG)
    for i in range(4):
        xx = px - 0.09 + i * 0.06
        box(xx - 0.015, xx + 0.015, pz - 0.03, pz + 0.03, stroke=SAFE, sw=0.9, fill=SAFE if i == 3 else "none")
    # кресло (спинкой к зрителю)
    chx = (d0 + d1) / 2
    sh_ = v("layout.chair.seat_height")
    box(chx - 0.24, chx + 0.24, sh_ - 0.07, sh_, stroke=INK, sw=1.2, fill="none")
    box(chx - 0.22, chx + 0.22, sh_ + 0.02, sh_ + 0.62, stroke=INK, sw=1.2, fill="none", rx=6)
    sh.line(V(chx, sh_ - 0.07), V(chx, 0.05), stroke=INK, sw=2.0)
    sh.line(V(chx - 0.25, 0.02), V(chx + 0.25, 0.02), stroke=INK, sw=2.0)
    # санузел: стенка у прохода с дверью
    hy0, hy1 = z["hygiene"]
    box(hy0, hy1, 0, hb.ceil, stroke=INK, sw=1.3, fill=FILL)
    box(hy0 + 0.25, hy1 - 0.2, 0.02, 1.9, stroke=INK2, sw=1.0, dash="5 3")
    pc = V((hy0 + hy1) / 2, 1.2)
    sh.text((pc[0], pc[1]), c.s("wc"), size=11.5, color=INK, anchor="middle")
    # ниша: медшкаф у борта
    st0 = z["stasis"][0]
    box(st0 + 0.05, hy0 - 0.05, 0.9, 1.6, stroke=INK2, sw=1.0, fill=lk)
    pc = V((st0 + hy0) / 2, 1.25)
    sh.text((pc[0], pc[1] + 4), c.s("med"), size=10.5, color=INK2, anchor="middle")
    # стена СЖО: модули за проёмом
    e0, e1 = z["eclss_wall"]
    box(e0, e1, 0, hb.ceil + 0.035, stroke=INK, sw=1.3, fill=FILL2)
    for zz in (0.55, 1.1, 1.6):
        sh.line(V(e0, zz), V(e1, zz), stroke=INK2, sw=0.9)
    pc = V((e0 + e1) / 2, 0.85)
    sh.text((pc[0] + 4, pc[1]), c.s("eclss"), size=10.5, color=INK, anchor="middle", rot=-90)

    # --- контур корпуса поверх ---
    sh.path(outer, stroke=INK, sw=1.6)
    sh.rect(i1[0], i1[1], i2[0] - i1[0], i2[1] - i1[1], stroke=INK, sw=2.2)
    sh.line(V(-Lo / 2 - 0.3, h), V(Lo / 2 + 0.3, h), stroke=INK2, sw=0.9, dash="16 4 3 4")

    # --- жёсткая линия ARI ISOLATE: панель → пленум → корма → туннель → ферма (вариант SPEC) ---
    wire = [V(px, pz + 0.05), V(px, hb.ceil + 0.07), V(-L / 2 + 0.1, hb.ceil + 0.07), V(-L / 2 + 0.1, hc + 0.3),
            V(ex, hc + 0.3), V(ex, zb_top - 0.1)]
    sh.poly(wire, stroke=SAFE, sw=1.6, dash="7 4", closed=False)
    pwl = V(ex - 0.2, 2.6)
    sh.text(pwl, c.s("wire"), size=11.5, color=SAFE, anchor="middle", rot=-90)

    # --- Майя у окна (позиция 3) ---
    pm = V(L / 2 - 0.25, 0)
    sh.person_side(pm[0], pm[1], k, v("maya.height"), facing=1)
    pt = V(L / 2 - 0.27, v("maya.height") + 0.12)
    sh.text(pt, c.s("maya", h=c.fv("maya.height")), size=11.5, color=INK, anchor="middle")

    # --- камеры: C на стене +Y, A и B — по −Y, за плоскостью (пунктир) ---
    for cam, letter, dashed in (("c", "C", False), ("a", "A", True), ("b", "B", True)):
        pp = V(v(f"layout.camera_{cam}.x"), v(f"layout.camera_{cam}.height"))
        if dashed:
            sh.circle(pp, 9, stroke=CAM, sw=1.1, fill=BG, dash="2 2")
            sh.text((pp[0], pp[1] + 4), letter, size=11, color=CAM, anchor="middle", weight="bold", halo=False)
        else:
            sh.tag(pp, letter)

    # --- направления ---
    pw = V(Lo / 2 + 0.06, wc)
    sh.arrow((pw[0], pw[1]), (pw[0] + 62, pw[1]), color=INK, sw=2.0)
    sh.text((pw[0] + 64, pw[1] + 4), "+X", size=12, color=INK)
    pdn = V(Lo / 2 + 0.45, -0.15)
    sh.arrow(pdn, (pdn[0], pdn[1] + 92), color=INK, sw=2.2)
    sh.text((pdn[0] + 12, pdn[1] + 46), c.s("down", g=c.fv("habitat.floor_gravity")), size=12.5, weight="bold")
    sh.text((pdn[0] + 12, pdn[1] + 64), c.s("down2"), size=11.5, color=INK2)
    pup = V(ex, zb_top + 0.2)
    sh.arrow((pup[0], pup[1]), (pup[0], pup[1] - 30), color=INK, sw=2.0)
    sh.text((pup[0] + 14, pup[1] - 14), c.s("to_axis", r=c.fv("habitat.floor_radius")), size=12.5, weight="bold")
    pa = V(axh + bw / 2 + 0.12, zb_top - 0.15)
    sh.text(pa, c.s("alt"), size=12, color=AMBER)
    sh.text((40, 712), c.s("spec"), size=12, color=INK)
    sh.text((40, 732), c.s("c003"), size=12.5, color=AMBER, weight="bold")
    sh.text((40, 770), c.s("cams_ab", a=c.fv("layout.camera_a.height"), b=c.fv("layout.camera_b.height")),
            size=11.5, color=CAM)

    # --- размеры: цепочка зон, длины ---
    yb = V(0, bot_out)[1]
    chain = [z["vestibule"], z["eclss_wall"], z["stasis"], z["galley_storage"], z["main_cabin"], z["window_bay"]]
    names = ["n_vest", "n_eclss", "n_aft", "n_galley", "n_main", "n_window"]
    for (a, b), nm in zip(chain, names):
        p, q = V(a, bot_in), V(b, bot_in)
        sh.dim(p, q, -(yb - p[1] + 30), c.m(b - a), size=11)
        pc = V((a + b) / 2, 0)
        sh.text((pc[0], yb + 52), c.s(nm), size=11, color=INK2, anchor="middle")
    p, q = V(-L / 2, bot_in), V(L / 2, bot_in)
    sh.dim(p, q, -(yb - p[1] + 88), c.fv("habitat.inner_length"))
    p, q = V(-Lo / 2, bot_out), V(Lo / 2, bot_out)
    sh.dim(p, q, -(yb - p[1] + 124), c.fv("exterior.habitat.outer_length"))
    # высота потолка — в нише
    sh.dim(V(-1.55, 0), V(-1.55, hb.ceil), 0, c.fv("layout.hull.ceiling_height"), tick_ext=False)
    # люк: центр и диаметр — в тамбуре
    xv = z["vestibule"][0] + 0.1
    sh.dim(V(xv, 0), V(xv, hc), 0, c.s("hatch_c", z=c.fv("layout.hatch.center_height")), size=11, tick_ext=False)
    sh.line(V(-L / 2, hc), V(xv + 0.32, hc), stroke=DIM, sw=0.7, op=0.8)
    xv2 = xv + 0.32
    sh.line(V(-L / 2, hc + hd / 2), V(xv2 + 0.06, hc + hd / 2), stroke=DIM, sw=0.7, op=0.8)
    sh.line(V(-L / 2, hc - hd / 2), V(xv2 + 0.06, hc - hd / 2), stroke=DIM, sw=0.7, op=0.8)
    sh.dim(V(xv2, hc - hd / 2), V(xv2, hc + hd / 2), 0, c.s("hatch_d", d=c.fv("layout.hatch.diameter")), size=11,
           tick_ext=False, text_side=-1)
    # окно: центр и высота — справа снаружи
    xw = V(Lo / 2, 0)[0] + 110
    sh.line(V(Lo / 2, 0), (xw + 8, oy), stroke=DIM, sw=0.7, op=0.8)
    sh.line(V(Lo / 2 + 0.55, wc), (xw + 8, V(0, wc)[1]), stroke=DIM, sw=0.7, op=0.8)
    sh.dim((xw, oy), (xw, V(0, wc)[1]), 0, c.s("win_c", z=c.fv("layout.window.center_height")), size=11,
           tick_ext=False, text_side=-1)
    xw2 = xw + 40
    for s in (1, -1):
        sh.line(V(Lo / 2, wc + s * hmax / 2), (xw2 + 8, V(0, wc + s * hmax / 2)[1]), stroke=DIM, sw=0.7, op=0.8)
    sh.dim((xw2, V(0, wc - hmax / 2)[1]), (xw2, V(0, wc + hmax / 2)[1]), 0, c.fv("habitat.window_height"),
           size=11, tick_ext=False, text_side=-1)

    # --- выноски сверху: лесенка, текст влево от выноски ---
    labels = [
        ((px, pz + 0.05), c.s("isolate", z=c.fv("layout.ari_isolate_panel.height")), SAFE),
        ((d0 + 0.3, dh), c.s("desk", h=c.fv("layout.desk.height"), s=c.fv("layout.chair.seat_height")), INK2),
        ((gs[0] + 0.55, gh + 0.04), c.s("galley", h=c.fv("layout.galley.counter_height")), INK2),
        ((v("layout.display_primary.center_x") + 0.2, 1.42),
         c.s("displays", p=c.fv("habitat.display_primary"), s=c.fv("habitat.display_secondary"),
             z=c.fv("layout.display_primary.center_height")), INK2),
        ((v("layout.camera_c.x"), v("layout.camera_c.height") + 0.07),
         c.s("cam_c", z=c.fv("layout.camera_c.height")), CAM),
        ((L / 2 + 0.2, wc + hmax / 2 + 0.4), c.s("window", w=c.fv("habitat.window_width"),
                                                  h=c.fv("habitat.window_height")), INK2),
    ]
    labels.sort(key=lambda t: t[0][0])
    ys = [V(0, top_out)[1] - 22 - 34 * i for i in range(len(labels))]
    for ((fx, fz), lab, col), ty in zip(labels, ys):
        fp = V(fx, fz)
        sh.circle(fp, 2.4, stroke="none", fill=col)
        sh.poly([fp, (fp[0], ty), (fp[0] - 8, ty)], stroke=col, sw=0.9, closed=False)
        sh.text((fp[0] - 12, ty + 4), lab, size=12, color=col if col in (SAFE, CAM) else INK, anchor="end")

    # --- оси ---
    axx, axy = 82, 900
    sh.arrow((axx, axy), (axx + 52, axy), color=INK2, sw=1.4, marker="ai")
    sh.arrow((axx, axy), (axx, axy - 52), color=INK2, sw=1.4, marker="ai")
    sh.circle((axx, axy), 7, stroke=INK2, sw=1.2)
    sh.line((axx - 5, axy - 5), (axx + 5, axy + 5), stroke=INK2, sw=1.1)
    sh.line((axx - 5, axy + 5), (axx + 5, axy - 5), stroke=INK2, sw=1.1)
    sh.text((axx + 58, axy + 4), c.s("ax_x"), size=12, color=INK2)
    sh.text((axx + 8, axy - 52), "+Z", size=12, color=INK2)
    sh.text((axx - 8, axy + 24), c.s("ax_y"), size=11, color=INK2)

    footer(sh, c, "BP-04", scale_m=(0, 0.5, 1, 1.5, 2), k=k)
    return sh


def _break(sh: Sheet, p, q, color):
    """Линия обрыва (зигзаг) поперёк длинной детали."""
    mx = (p[0] + q[0]) / 2
    y = p[1]
    sh.poly([(p[0], y), (mx - 8, y), (mx - 3, y - 8), (mx + 3, y + 8), (mx + 8, y), (q[0], y)], stroke=color,
            sw=1.3, closed=False, fill=BG)
