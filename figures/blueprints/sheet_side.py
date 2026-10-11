"""Лист (a): корабль сбоку — хребет и ось вращения, жилой модуль на радиусе пола, противовес, ядро ARI.

Вид поперёк плоскости ферм: хребет горизонтально, нос справа; жилой модуль под осью (его «вниз» —
радиально наружу — совпадает с низом листа), противовес над осью. Грубо и пропорционально.
"""
from __future__ import annotations

from bp import AMBER, BG, CAM, DIM, FILL, FILL2, INK, INK2, SAFE, WATER, Sheet, View  # noqa: F401
import geom
from sheet_cross import footer

NAME = "ship-side-schematic"
W, H = 1660, 1300


def render(c) -> Sheet:
    hb = geom.habitat(c)
    shp = geom.ship(c, hb)
    v = c.v
    sh = Sheet(W, H, c.lang, c.s("title"), c.s("desc"))
    k = 15.5
    x_nose, oy = 1300.0, 600.0
    # (станция s от носа, радиус r: + к жилому модулю) → лист
    V = View(x_nose, oy, k, ux=(-1, 0), uy=(0, 1))
    sh.heading(40, 58, c.s("title"), c.s("subtitle"))

    S = lambda key: v(f"exterior.{key}.station")  # noqa: E731
    Ls, d = shp.L, shp.d

    def box(s0, s1, r0, r1, **kw):
        p, q = V(s1, r0), V(s0, r1)
        sh.rect(p[0], p[1], q[0] - p[0], q[1] - p[1], **kw)

    # --- ось вращения ---
    sh.line(V(Ls + 6.5, 0), V(-4.5, 0), stroke=INK2, sw=1.0, dash="22 5 4 5")

    # --- радиаторы (в плоскости листа, обе стороны) ---
    r0, r1 = S("radiators")
    span = v("exterior.radiators.half_span")
    rad = sh.hatch_id("rad", INK2, step=8, sw=0.6, angle=90, op=0.35)
    for sgn in (1, -1):
        box(r0, r1, sgn * (d / 2 + 0.3), sgn * span, stroke=INK, sw=1.2, fill=rad)
        for ss in range(int(r0) + 3, int(r1), 3):
            sh.line(V(ss, sgn * (d / 2 + 0.3)), V(ss, sgn * span), stroke=INK2, sw=0.7, op=0.8)

    # --- хребет ---
    sp = sh.hatch_id("spine", INK2, step=10, sw=0.7, angle=45, op=0.6)
    box(0, Ls, -d / 2, d / 2, stroke=INK, sw=1.3, fill=sp)

    # --- носовая секция: мачта датчиков и антенна ---
    c0, c1 = S("comms")
    box(c0, c1, -0.5, 0.5, stroke=INK, sw=1.2, fill=FILL2)
    pd = V(c0 + 0.6, 0)
    sh.path(f"M{pd[0] + 6},{pd[1] - V.L(2.2)} Q{pd[0] - 10},{pd[1]} {pd[0] + 6},{pd[1] + V.L(2.2)}", stroke=INK,
            sw=1.8)
    sh.line(V(c0 + 0.6, 0), V(c0 - 0.6, 0), stroke=INK, sw=1.4)
    for sgn in (1, -1):
        sh.line(V(c1 - 1.5, sgn * 0.5), V(c1 - 2.8, sgn * 1.8), stroke=INK, sw=1.2)

    # --- баки ---
    t0, t1 = S("tanks")
    td = v("exterior.tanks.diameter")
    n = 3
    tl = (t1 - t0) / n
    for i in range(n):
        a = t0 + i * tl + 0.15
        b = a + tl - 0.3
        p, q = V(b, -td / 2), V(a, td / 2)
        sh.rect(p[0], p[1], q[0] - p[0], q[1] - p[1], stroke=INK, sw=1.3, fill=FILL2, rx=V.L(td / 2) * 0.6)

    # --- реактор и теневая защита ---
    e0, e1 = S("reactor")
    rd = v("exterior.reactor.diameter")
    box(e0 + 0.6, e1, -rd / 2, rd / 2, stroke=INK, sw=1.3, fill=FILL2, rx=4)
    box(e0, e0 + 0.6, -rd * 0.75, rd * 0.75, stroke=INK, sw=1.5, fill=INK2)
    # --- двигатели ---
    g0, g1 = S("propulsion")
    box(g0, g1 - 2.2, -1.4, 1.4, stroke=INK, sw=1.2, fill=FILL2)
    for rr in (-0.9, 0, 0.9):
        a, b = V(g1 - 2.2, rr - 0.25), V(g1, rr - 0.55)
        a2, b2 = V(g1 - 2.2, rr + 0.25), V(g1, rr + 0.55)
        sh.poly([a, b, b2, a2], stroke=INK, sw=1.1, fill=FILL)
    pe = V(g1, 0)
    sh.poly([(pe[0], pe[1] - 14), (pe[0] - 95, pe[1] - 34), (pe[0] - 95, pe[1] + 34), (pe[0], pe[1] + 14)],
            stroke=INK2, sw=1.0, dash="5 4", op=0.9)

    # --- противовес (над осью) ---
    cw0, cw1 = shp.cw_r
    cwm = (cw0 + cw1) / 2
    hc_st = shp.hab_center
    for rr, dash in ((cw0, "3 4"), (cw1, "3 4")):
        box(hc_st - shp.cw_len / 2, hc_st + shp.cw_len / 2, -(rr - shp.cw_d / 2), -(rr + shp.cw_d / 2),
            stroke=INK2, sw=0.9, dash=dash)
    box(hc_st - shp.cw_len / 2, hc_st + shp.cw_len / 2, -(cwm - shp.cw_d / 2), -(cwm + shp.cw_d / 2),
        stroke=INK, sw=1.6, fill=FILL2, rx=6)
    bwid = shp.boom_w
    vd = v("exterior.ari_core.vault_diameter")
    box(shp.hub - bwid / 2, shp.hub + bwid / 2, -vd / 2, -(cwm + 0.3), stroke=INK, sw=1.2, fill=FILL)
    box(hc_st + shp.cw_len / 2, shp.hub - bwid / 2, -(cwm - 0.3), -(cwm + 0.3), stroke=INK, sw=1.2, fill=FILL)
    # ход противовеса
    xa = V(hc_st - shp.cw_len / 2 - 1.2, 0)[0]
    sh.line((xa, V(0, -cw0)[1]), (xa, V(0, -cw1)[1]), stroke=DIM, sw=0.9, marker_start="ad", marker_end="ad")

    # --- жилой модуль (под осью) ---
    Ro, Lo = hb.Ro, hb.Lo
    ra = shp.hab_axis_r
    box(hc_st - Lo / 2, hc_st + Lo / 2, ra - Ro, ra + Ro, stroke=INK, sw=1.8, fill=FILL2, rx=6)
    sh.line(V(hc_st - Lo / 2 + 0.5, shp.floor_r), V(hc_st + Lo / 2 - 0.5, shp.floor_r), stroke=INK2, sw=1.0,
            dash="4 3")
    wc_r = shp.floor_r - v("layout.window.center_height")
    sh.line(V(hc_st - Lo / 2, wc_r - 0.4), V(hc_st - Lo / 2, wc_r + 0.4), stroke=CAM, sw=3)
    pm = V(hc_st - 1.5, shp.floor_r)
    sh.person_side(pm[0], pm[1], k, v("maya.height"), facing=1)
    # ферма жилого модуля с коленом к кормовому люку (вариант SPEC, C-003)
    hcz = shp.floor_r - v("layout.hatch.center_height")
    box(shp.hub - bwid / 2, shp.hub + bwid / 2, vd / 2, hcz + 0.6, stroke=INK, sw=1.2, fill=FILL)
    box(hc_st + Lo / 2, shp.hub - bwid / 2, hcz - 0.4, hcz + 0.4, stroke=INK, sw=1.2, fill=FILL)
    # жёсткая линия ARI ISOLATE по ферме
    sh.line(V(shp.hub, vd / 2 + 0.2), V(shp.hub, hcz), stroke=SAFE, sw=1.6, dash="6 4")
    sh.line(V(shp.hub, hcz), V(hc_st + Lo / 2, hcz), stroke=SAFE, sw=1.6, dash="6 4")

    # --- ступица: ядро ARI, батареи, рубильник ---
    core, cl = v("exterior.ari_core.station"), v("exterior.ari_core.vault_length")
    b0, b1 = v("exterior.ari_core.battery_station")
    box(b0, b1, -1.1, 1.1, stroke=INK, sw=1.2, fill=FILL2)
    box(core - cl / 2, core + cl / 2, -vd / 2, vd / 2, stroke=INK, sw=2.2, fill="#2a5d93", rx=3)
    pc = V(core, 0)
    sh.circle(pc, V.L(cl) * 1.05, stroke=CAM, sw=1.2, dash="3 3")
    br = V(v("exterior.ari_core.manual_breaker.station"), v("exterior.ari_core.manual_breaker.radius"))
    sh.circle(br, 3.2, stroke="none", fill=SAFE)
    sh.leader(br, (br[0] - 30, br[1] + 70), c.s("breaker_short"), side="left", color=SAFE, tcolor=SAFE, size=11.5)

    # --- надписи узлов ---
    sh.text(V(c1 - 3.0, 3.4), c.s("comms"), size=12, anchor="middle")
    sh.text(V((t0 + t1) / 2, td / 2 + 1.4), c.s("tanks"), size=12, anchor="middle")
    sh.text(V((r0 + r1) / 2, span + 1.6), c.s("radiators"), size=12, anchor="middle")
    pr = V((e0 + e1) / 2, -rd * 0.75 - 2.6)
    sh.text(pr, c.s("reactor"), size=12, anchor="middle")
    pg = V((g0 + g1) / 2, -2.6)
    sh.text(pg, c.s("propulsion"), size=12, anchor="middle")
    pt = V(g1 - 3, 3.6)
    sh.arrow((pt[0] - 50, pt[1]), (pt[0] + 40, pt[1]), color=INK, sw=2.6)
    sh.text((pt[0] - 50, pt[1] + 22), c.s("thrust"), size=12.5, weight="bold")
    sh.text((pe[0] - 100, pe[1] - 44), c.s("exhaust"), size=11.5, color=INK2)
    sh.text(V(Ls + 0.5, -4.5), c.s("aft"), size=13, weight="bold", anchor="end", spacing=1)
    pn = V(-0.4, -4.4)
    sh.text((pn[0], pn[1] - 10), c.s("nose"), size=13, weight="bold", spacing=1)
    sh.arrow(pn, (pn[0] + 52, pn[1]), color=INK, sw=2.2)
    sh.text((V(-3.6, 0)[0] + 24, oy + 30), c.s("axis"), size=11.5, color=INK2)
    sh.text(V(shp.hub + 1.8, -3.3), c.s("core_short"), size=15, weight="bold", color=CAM, anchor="end")

    # вращение
    pspin = V(-3.6, 0)
    rx, ry = 13, 52
    sh.path(f"M{pspin[0]},{pspin[1] - ry} A{rx},{ry} 0 1 1 {pspin[0] - 0.1},{pspin[1] + ry}", stroke=INK, sw=1.8,
            marker_end="aw")
    sh.text((pspin[0] + 24, pspin[1] - 22), c.s("spin", rpm=c.fv("ship.spin_rpm"), t=c.fv("ship.spin_period")),
            size=12.5, weight="bold")
    sh.text((pspin[0] + 24, pspin[1] - 4), c.s("spin2"), size=11.5, color=INK2)

    # противовес — подпись
    pcw = V(hc_st - shp.cw_len / 2 - 2.2, -cwm)
    sh.text((pcw[0], pcw[1] - 4), c.s("cw", r=c.fv("exterior.counterweight.radius")), size=12)
    sh.text((pcw[0], pcw[1] + 13), c.s("cw2"), size=11, color=INK2)

    # жилой модуль, окно, R пола, 0,5 g
    pw = V(hc_st - Lo / 2, wc_r)
    sh.arrow((pw[0] + 3, pw[1]), (pw[0] + 58, pw[1]), color=CAM, sw=1.8, marker="ac")
    sh.text((pw[0] + 96, pw[1] + 4), c.s("window"), size=12, color=CAM)
    xr = V(-1.4, 0)[0]
    sh.line(V(hc_st - Lo / 2 + 0.3, shp.floor_r), (xr + 8, V(0, shp.floor_r)[1]), stroke=DIM, sw=0.7, op=0.8)
    sh.dim((xr, oy), (xr, V(0, shp.floor_r)[1]), 0, c.s("radius", r=c.fv("habitat.floor_radius")), size=13,
           tick_ext=False)
    pf = V(hc_st + 1.8, shp.floor_r)
    sh.arrow(pf, (pf[0], pf[1] + 62), color=INK, sw=2.6)
    sh.text((pf[0] - 10, pf[1] + 56), c.s("floor_g", g=c.fv("habitat.floor_gravity"), a=c.fv("habitat.floor_accel")),
            size=12.5, weight="bold", anchor="end")
    ph = V(hc_st + 1.0, ra - Ro)
    sh.leader(ph, (V(shp.hub, 0)[0] - 18, ph[1] - 34), c.s("habitat", d=c.fv("exterior.habitat.outer_diameter"),
                                                            l=c.fv("exterior.habitat.outer_length")), side="left")
    pc3 = V(shp.hub + 0.3, hcz + 0.9)
    sh.text((pc3[0] - 6, pc3[1] + 4), c.s("c003"), size=11.5, color=AMBER, anchor="end")
    pbw = V(shp.hub + 1.2, 13)
    sh.text(pbw, c.s("boom"), size=11.5, color=INK, anchor="middle", rot=-90)
    pwl = V(shp.hub - 1.3, 13)
    sh.text(pwl, c.s("wire"), size=11.5, color=SAFE, anchor="middle", rot=-90)

    # длина хребта — снизу
    yb = 1128
    for ss in (0, Ls):
        p = V(ss, 0)
        sh.line((p[0], p[1] + 30 if ss == 0 else p[1] + 40), (p[0], yb + 6), stroke=DIM, sw=0.7, op=0.6)
    sh.dim((V(Ls, 0)[0], yb), (V(0, 0)[0], yb), 0, c.s("spine", l=c.fv("exterior.spine.length")), size=12.5,
           tick_ext=False)

    # --- деталь A: ступица ×K ---
    _detail(sh, c, shp, hb, V)
    # --- врезка: Майя и градиент тяжести ---
    _maya_inset(sh, c)

    footer(sh, c, "BP-01", scale_m=(0, 10, 20, 30), k=k)
    return sh


def _detail(sh: Sheet, c, shp, hb, V0):
    v = c.v
    bx, by, bw_, bh = 556, 104, 534, 340
    sh.rect(bx, by, bw_, bh, stroke=CAM, sw=1.2, fill=BG)
    kk = 36.0
    core = v("exterior.ari_core.station")
    cx, cy = bx + bw_ * 0.56, by + 150
    V = View(cx + core * kk, cy, kk, ux=(-1, 0), uy=(0, 1))
    clip = "clip-detail"
    sh.defs.append(f'<clipPath id="{clip}"><rect x="{bx + 1}" y="{by + 56}" width="{bw_ - 2}" height="{bh - 120}"/>'
                   f'</clipPath>')
    sh.add(f'<g clip-path="url(#{clip})">')
    d = shp.d
    sp = sh.hatch_id("spine2", INK2, step=10, sw=0.7, angle=45, op=0.6)

    def box(s0, s1, r0, r1, **kw):
        p, q = V(s1, r0), V(s0, r1)
        sh.rect(p[0], p[1], q[0] - p[0], q[1] - p[1], **kw)

    sh.line(V(core + 9, 0), V(core - 9, 0), stroke=INK2, sw=1.0, dash="22 5 4 5")
    box(core - 9, core + 9, -d / 2, d / 2, stroke=INK, sw=1.2, fill=sp)
    t0 = v("exterior.tanks.station")[0]
    td = v("exterior.tanks.diameter")
    p, q = V(t0 + 6, -td / 2), V(t0 + 0.15, td / 2)
    sh.rect(p[0], p[1], q[0] - p[0], q[1] - p[1], stroke=INK, sw=1.3, fill=FILL2, rx=V.L(td / 2) * 0.6)
    bw = shp.boom_w
    vd = v("exterior.ari_core.vault_diameter")
    cl = v("exterior.ari_core.vault_length")
    box(shp.hub - bw / 2, shp.hub + bw / 2, -vd / 2, -6, stroke=INK, sw=1.3, fill=FILL)
    box(shp.hub - bw / 2, shp.hub + bw / 2, vd / 2, 6, stroke=INK, sw=1.3, fill=FILL)
    box(shp.hub - 0.4, shp.hub + 0.4, vd / 2, 6, stroke=INK2, sw=0.9, dash="4 3")
    for rr in [vd / 2 + 0.3 + 0.35 * i for i in range(10)]:
        sh.line(V(shp.hub - 0.3, rr), V(shp.hub + 0.3, rr), stroke=INK2, sw=0.7, op=0.7)
    b0, b1 = v("exterior.ari_core.battery_station")
    box(b0, b1, -1.1, 1.1, stroke=INK, sw=1.3, fill=FILL2)
    for ss in (b0 + 0.5, b0 + 1.0):
        sh.line(V(ss, -1.1), V(ss, 1.1), stroke=INK2, sw=0.8)
    vh = sh.hatch_id("vault", CAM, step=6, sw=0.7, angle=45, op=0.35)
    box(core - cl / 2, core + cl / 2, -vd / 2, vd / 2, stroke=CAM, sw=2.6, fill="#2a5d93", rx=4)
    box(core - cl / 2 + 0.08, core + cl / 2 - 0.08, -vd / 2 + 0.08, vd / 2 - 0.08, stroke="none", fill=vh)
    p = V(core, 0)
    sh.text((p[0], p[1] + 9), "ARI", size=26, weight="bold", color=INK, anchor="middle")
    kc = V(core - 0.85, vd / 2 - 0.05)
    sh.rect(kc[0] - 11, kc[1] - 9, 22, 11, stroke=SAFE, sw=1.4, fill=BG)
    mb = V(v("exterior.ari_core.manual_breaker.station") + 0.15, v("exterior.ari_core.manual_breaker.radius"))
    sh.circle(mb, 4, stroke=SAFE, sw=1.6, fill=BG)
    sh.line(mb, (mb[0] + 14, mb[1] + 12), stroke=SAFE, sw=2.4)
    sh.poly([(kc[0], kc[1] + 2), (kc[0], V(0, vd / 2 + 0.25)[1]), V(shp.hub - 0.25, vd / 2 + 0.25),
             V(shp.hub - 0.25, 6)], stroke=SAFE, sw=1.8, dash="6 4", closed=False)
    sh.add("</g>")
    # заголовок
    sh.text((bx + 14, by + 24), c.s("detail_title"), size=14, weight="bold", color=CAM)
    sh.text((bx + 14, by + 43), c.s("detail_sub"), size=11.5, color=INK2)
    # выноски: сейф и батареи — вверх вправо, контакторы и рубильник — вниз
    vt = V(core - cl / 2 + 0.3, -vd / 2)
    sh.leader(vt, (vt[0] + 18, by + 66), c.s("vault", d=c.fv("exterior.ari_core.vault_diameter"),
                                              l=c.fv("exterior.ari_core.vault_length")), side="right", color=CAM,
              size=11.5)
    bt = V((b0 + b1) / 2, -1.1)
    sh.leader(bt, (bt[0] - 18, by + 76), c.s("battery", e=c.fv("exterior.ari_core.battery_energy")), side="left",
              size=11.5)
    sh.leader((kc[0] + 11, kc[1] - 3), (kc[0] + 44, by + bh - 96), c.s("contactors"), side="right", color=SAFE,
              tcolor=SAFE, size=11.5)
    sh.leader((mb[0] - 4, mb[1]), (bx + 262, by + bh - 76), c.s("breaker"), side="left", color=SAFE,
              tcolor=SAFE, size=11.5)
    sh.text((bx + 14, by + bh - 46), c.s("power", p=c.fv("exterior.ari_core.power")), size=11.5, color=INK)
    sh.text((bx + 14, by + bh - 28), c.s("juno"), size=11, color=INK2)
    sh.text((bx + 14, by + bh - 11), c.s("tanks_shield"), size=11, color=INK2)
    # связь детали с главным видом
    hub = V0(shp.hub, 0)
    sh.line((hub[0] - V0.L(1.4), hub[1] - V0.L(3.0)), (bx + bw_ - 2, by + bh), stroke=CAM, sw=0.9, dash="3 3")
    sh.text((bx + bw_ - 22, by + bh - 6), "A", size=14, weight="bold", color=CAM)


def _maya_inset(sh: Sheet, c):
    v = c.v
    bx, by, bw_, bh = 40, 104, 500, 340
    sh.rect(bx, by, bw_, bh, stroke=INK2, sw=1.0, fill=BG)
    sh.text((bx + 14, by + 24), c.s("inset_title"), size=14, weight="bold")
    k = 90.0
    fx, fy = bx + 120, by + bh - 86
    sh.line((fx - 90, fy), (fx + 110, fy), stroke=INK, sw=2.2)
    hm = v("maya.height")
    sh.person_side(fx, fy, k, hm, facing=1)
    head_y = fy - hm * k
    # стрелки тяжести: длина пропорциональна ускорению
    ga = v("habitat.floor_accel")
    gh = v("gravity.head_accel")
    L0 = 70.0
    ax_ = fx + 150
    sh.arrow((ax_, fy - 2), (ax_, fy - 2 + L0), color=INK, sw=2.6)
    sh.arrow((ax_ + 70, head_y), (ax_ + 70, head_y + L0 * gh / ga), color=INK2, sw=2.2, marker="ai")
    sh.line((fx + 30, head_y), (ax_ + 82, head_y), stroke=INK2, sw=0.8, dash="3 3")
    sh.text((ax_ + 12, fy + 24), c.s("inset_floor", g=c.fv("habitat.floor_gravity"), a=c.fv("habitat.floor_accel")),
            size=12, weight="bold")
    sh.text((ax_ + 82, head_y + 24), c.s("inset_head", g=c.fv("gravity.head_g"), p=c.fv("gravity.gradient_head")),
            size=12, color=INK2)
    sh.arrow((fx - 60, fy - 40), (fx - 60, fy - 130), color=INK2, sw=1.6, marker="ai")
    sh.text((fx - 44, fy - 112), c.s("inset_axis"), size=11, color=INK2, anchor="start", rot=-90)
    sh.text((bx + 14, by + 46), c.s("inset_sub"), size=11.5, color=INK2)
