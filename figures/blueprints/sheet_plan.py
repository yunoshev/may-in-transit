"""Лист (b): план жилого модуля — вид сверху (от оси вращения на пол), нос вверху, +Y слева."""
from __future__ import annotations

import math

from bp import AMBER, BG, CAM, DIM, FILL, FILL2, INK, INK2, SAFE, WATER, Sheet, View  # noqa: F401
import geom
from sheet_cross import footer

NAME = "habitat-plan"
W, H = 1340, 1440


def render(c) -> Sheet:
    hb = geom.habitat(c)
    v = c.v
    sh = Sheet(W, H, c.lang, c.s("title"), c.s("desc"))
    k = 118.0
    cx, cy = 600.0, 590.0
    # мир (X, Y) → лист: +X вверх, +Y влево
    V = View(cx, cy, k, ux=(0, -1), uy=(-1, 0))
    R, Ro, L, Lo = hb.R, hb.Ro, hb.L, hb.Lo
    face = hb.floor_w / 2
    back = face + hb.locker_d
    z = hb.zones
    a2 = hb.aisle / 2

    sh.heading(40, 58, c.s("title"), c.s("subtitle"))

    def box(x0, x1, y0, y1, **kw):
        p, q = V(x1, y0), V(x0, y1)
        sh.rect(p[0], p[1], q[0] - p[0], q[1] - p[1], **kw)

    # --- оболочка в разрезе на высоте оси цилиндра ---
    hatch = sh.hatch_id("shell", INK2, step=7, sw=0.8, op=0.55)
    o1, o2 = V(Lo / 2, Ro), V(-Lo / 2, -Ro)
    i1, i2 = V(L / 2, R), V(-L / 2, -R)
    rr = V.L(0.3)
    sh.path(f"M{o1[0] + rr},{o1[1]} H{o2[0] - rr} Q{o2[0]},{o1[1]} {o2[0]},{o1[1] + rr} V{o2[1] - rr} "
            f"Q{o2[0]},{o2[1]} {o2[0] - rr},{o2[1]} H{o1[0] + rr} Q{o1[0]},{o2[1]} {o1[0]},{o2[1] - rr} "
            f"V{o1[1] + rr} Q{o1[0]},{o1[1]} {o1[0] + rr},{o1[1]} Z "
            f"M{i1[0]},{i1[1]} V{i2[1]} H{i2[0]} V{i1[1]} Z", stroke="none", fill=hatch,
            extra=' fill-rule="evenodd"')
    sh.path(f"M{o1[0] + rr},{o1[1]} H{o2[0] - rr} Q{o2[0]},{o1[1]} {o2[0]},{o1[1] + rr} V{o2[1] - rr} "
            f"Q{o2[0]},{o2[1]} {o2[0] - rr},{o2[1]} H{o1[0] + rr} Q{o1[0]},{o2[1]} {o1[0]},{o2[1] - rr} "
            f"V{o1[1] + rr} Q{o1[0]},{o1[1]} {o1[0] + rr},{o1[1]} Z", stroke=INK, sw=1.6)
    sh.rect(i1[0], i1[1], i2[0] - i1[0], i2[1] - i1[1], stroke=INK, sw=2.2)
    # кромка палубы (ниже секущей плоскости)
    for s in (1, -1):
        sh.line(V(L / 2, s * hb.deck_half), V(-L / 2, s * hb.deck_half), stroke=INK2, sw=0.8, dash="2 4", op=0.8)

    # --- окно в носовой переборке ---
    wmax, wmin = v("habitat.window_width")
    p, q = V(Lo / 2 + 0.02, wmax / 2), V(L / 2 - 0.02, -wmax / 2)
    sh.rect(p[0], p[1], q[0] - p[0], q[1] - p[1], stroke="none", fill=BG)
    for xx in (L / 2 + 0.12, L / 2 + 0.2):
        sh.line(V(xx, wmax / 2), V(xx, -wmax / 2), stroke=CAM, sw=1.2)
    sh.line(V(L / 2 - 0.08, wmin / 2), V(L / 2 - 0.08, -wmin / 2), stroke=INK2, sw=1.0, dash="3 3")
    for s in (1, -1):
        sh.line(V(Lo / 2, s * wmax / 2), V(L / 2, s * wmax / 2), stroke=INK, sw=1.2)
    top = V(Lo / 2, 0)
    sh.arrow((top[0], top[1] - 4), (top[0], top[1] - 46), color=INK, sw=2.0)
    sh.text((top[0] + 12, top[1] - 30), c.s("view"), size=12.5, color=INK2)

    # --- границы зон ---
    for xb in (z["window_bay"][0], z["galley_storage"][1]):
        sh.line(V(xb, face), V(xb, -face), stroke=INK2, sw=0.9, dash="8 5")
    sh.line(V(z["galley_storage"][0], R), V(z["galley_storage"][0], -R), stroke=INK, sw=1.4)

    # --- шкафы вдоль бортов в открытой комнате ---
    lk = sh.hatch_id("lk", INK2, step=9, sw=0.6, angle=0, op=0.35)
    x0, x1 = z["galley_storage"][0], z["main_cabin"][1]
    for s in (1, -1):
        box(x0, x1, s * face, s * back, stroke=INK, sw=1.1, fill=lk)
        sh.line(V(x1, s * face), V(x1, s * R), stroke=INK, sw=1.1)
        for xx in (0.4, 0.8, 1.3, 1.8, 2.2):
            sh.line(V(xx, s * face), V(xx, s * back), stroke=INK2, sw=0.7, op=0.7)

    # --- рабочее место A (+Y) ---
    d0, d1 = v("layout.desk.x")
    dd = v("layout.desk.depth")
    box(d0, d1, face - dd, face, stroke=INK, sw=1.4, fill=FILL2)
    for key, rng in (("primary", "habitat.display_primary"), ("secondary", "habitat.display_secondary")):
        w_, _ = geom.display_size(v(rng)[1])
        xc = v(f"layout.display_{key}.center_x")
        box(xc - w_ / 2, xc + w_ / 2, face - 0.06, face, stroke=INK, sw=1.0, fill=INK2)
    chx = (d0 + d1) / 2
    chy = face - dd - 0.32
    pc = V(chx, chy)
    sh.circle(pc, V.L(0.25), stroke=INK, sw=1.3, fill=FILL2)
    b0, b1 = V(chx + 0.2, chy - 0.24), V(chx - 0.2, chy - 0.30)
    sh.rect(b1[0], b0[1], b0[0] - b1[0], b1[1] - b0[1], stroke=INK, sw=1.2, fill=FILL2, rx=3)
    # панель ARI ISOLATE
    px = v("layout.ari_isolate_panel.x")
    box(px - 0.12, px + 0.12, face - 0.1, face - 0.02, stroke=SAFE, sw=1.6, fill=SAFE)

    # --- камбуз (+Y) и хранение (−Y) ---
    g0, g1 = z["galley_storage"]
    gd = v("layout.galley.counter_depth")
    box(g0 + 0.02, g1 - 0.02, face - gd, face, stroke=INK, sw=1.3, fill=FILL2)
    sh.circle(V(g0 + 0.25, face - 0.28), V.L(0.06), stroke=INK2, sw=1.0)
    box(g0 + 0.45, g1 - 0.1, face - 0.45, face - 0.12, stroke=INK2, sw=0.9)

    # --- кормовая полоса: санузел (+Y), ниша, отсек стазиса (−Y), проход ---
    wall = dict(stroke=INK, sw=1.6)
    hy0, hy1 = z["hygiene"]
    st0, st1 = z["stasis"]
    sh.line(V(hy1, a2), V(hy0, a2), **wall)
    sh.line(V(hy0, a2), V(hy0, R), **wall)
    sh.line(V(st1, -a2), V(st0, -a2), **wall)
    # двери: проёмы в стенках у прохода
    for (xa, xb_), s in (((hy0 + 0.25, hy1 - 0.2), 1), ((st0 + 0.55, st1 - 0.55), -1)):
        p, q = V(xb_, s * a2), V(xa, s * a2)
        sh.line(p, q, stroke=BG, sw=3.2, cap="butt")
        sh.line(p, q, stroke=INK2, sw=1.0, dash="3 3")
    # санузел: унитаз и умывальник
    wc = V((hy0 + hy1) / 2 - 0.15, 0.95)
    sh.add(f'<ellipse cx="{wc[0]}" cy="{wc[1]}" rx="{V.L(0.19)}" ry="{V.L(0.24)}" fill="none" stroke="{INK}" '
           f'stroke-width="1.1"/>')
    box(hy1 - 0.4, hy1 - 0.08, 0.8, 1.25, stroke=INK, sw=1.0)
    # ниша и медшкаф
    box(st0, hy0, face, back, stroke=INK, sw=1.1, fill=lk)
    # отсек стазиса: койка и вода у борта
    box(st0 + 0.05, st1 - 0.05, -a2 - 0.12, -a2 - 0.87, stroke=INK, sw=1.4, fill=FILL2, rx=10)
    wh = sh.hatch_id("water", WATER, step=5, sw=0.9, angle=-45, op=0.6)
    box(st0, st1, -1.25, -R, stroke=WATER, sw=1.0, fill=wh)

    # --- стена СЖО: модули (+Y), вода (−Y), проём ---
    e0, e1 = z["eclss_wall"]
    for ya, yb in ((a2, 0.75), (0.75, 1.15)):
        box(e0 + 0.02, e1 - 0.02, ya + 0.02, yb - 0.02, stroke=INK, sw=1.1, fill=FILL2)
    box(e0, e1, 1.15, R, stroke=INK, sw=1.0, fill=FILL2)
    box(e0, e1, -a2, -R, stroke=WATER, sw=1.0, fill=wh)
    sh.line(V(e1, a2), V(e0, a2), **wall)
    sh.line(V(e1, -a2), V(e0, -a2), **wall)

    # --- люки: по SPEC в корме, вариант C-003 в своде ---
    hd = v("layout.hatch.diameter")
    p, q = V(-L / 2 + 0.02, hd / 2), V(-Lo / 2 - 0.02, -hd / 2)
    sh.rect(p[0], p[1], q[0] - p[0], q[1] - p[1], stroke="none", fill=BG)
    for s in (1, -1):
        sh.line(V(-L / 2, s * hd / 2), V(-Lo / 2, s * hd / 2), stroke=INK, sw=1.4)
    ex = v("exterior.boom.elbow_x")
    bw = v("exterior.boom.width")
    for s in (1, -1):
        sh.line(V(-Lo / 2, s * hd / 2), V(ex, s * hd / 2), stroke=INK2, sw=1.1)
    sh.circle(V(ex, 0), V.L(bw / 2), stroke=INK2, sw=1.4, fill=FILL)
    sh.circle(V(ex, 0), 5, stroke=INK2, sw=1.2)
    sh.circle(V(ex, 0), 1.5, stroke="none", fill=INK2)
    ax_ = v("layout.hatch.alt_ceiling_x")
    sh.circle(V(ax_, 0), V.L(hd / 2), stroke=AMBER, sw=1.6, dash="6 4")
    sh.circle(V(ax_, 0), V.L(bw / 2), stroke=AMBER, sw=1.0, dash="2 4")

    # --- камеры ---
    cone = V.L(1.6)
    for cam, letter in (("a", "A"), ("b", "B"), ("c", "C")):
        pp = V(v(f"layout.camera_{cam}.x"), v(f"layout.camera_{cam}.y"))
        sh.camera(pp, 90 + v(f"layout.camera_{cam}.yaw"), v(f"layout.camera_{cam}.hfov"), cone, letter)

    # --- надписи зон внутри ---
    def zlabel(x, y, key, size=12.5, color=INK, **kw):
        p = V(x, y)
        sh.text((p[0], p[1] + size * 0.35), c.s(key, **kw), size=size, color=color, anchor="middle")

    zlabel(sum(z["window_bay"]) / 2 - 0.05, 0, "z_window", size=11.5)
    zlabel(1.22, -0.3, "z_main", size=13)
    sh.text(V(2.2, 0.2), "A", size=26, weight="bold", color=INK2, anchor="middle")
    sh.text(V(2.2, -0.62), "B", size=26, weight="bold", color=INK2, anchor="middle")
    zlabel(sum(z["galley_storage"]) / 2, -0.2, "z_galley", size=11.5)
    zlabel(-1.0, 0, "z_aisle", size=11, color=INK2)
    zlabel(sum(z["vestibule"]) / 2 + 0.02, -1.0, "z_vest", size=11.5)
    zlabel(sum(z["eclss_wall"]) / 2, -0.75, "z_eclss", size=10.5)
    zlabel(-0.75, -0.8, "z_stasis", size=10, color=INK)
    zlabel(-0.55, 0.75, "z_wc", size=11.5)
    zlabel(-1.6, 0.68, "z_nook", size=10.5, color=INK2)

    # --- размеры справа: цепочка зон, длина, наружная длина ---
    xr = V(0, -Ro)[0]
    chain = [z["window_bay"], z["main_cabin"], z["galley_storage"], z["stasis"], z["eclss_wall"], z["vestibule"]]
    for a, b in chain:
        p, q = V(b, -R), V(a, -R)
        sh.dim((p[0], p[1]), (q[0], q[1]), xr - p[0] + 26, c.m(b - a), size=11)
    p, q = V(L / 2, -R), V(-L / 2, -R)
    sh.dim(p, q, xr - p[0] + 62, c.fv("habitat.inner_length"))
    p, q = V(Lo / 2, -Ro), V(-Lo / 2, -Ro)
    sh.dim(p, q, xr - p[0] + 98, c.fv("exterior.habitat.outer_length"))
    # ширина пола и проход — внутри
    sh.dim(V(0.9, face), V(0.9, -face), 0, c.fv("layout.hull.floor_width"), tick_ext=False)
    sh.dim(V(-0.4, a2), V(-0.4, -a2), 0, c.fv("layout.aisle_width"), size=11, tick_ext=False, text_side=-1)
    # диаметры — снизу
    yb = V(ex - bw / 2, 0)[1]
    p, q = V(-L / 2, R), V(-L / 2, -R)
    sh.dim(p, q, -(yb - p[1] + 40), c.s("d_in", d=c.fv("habitat.inner_diameter")))
    p, q = V(-Lo / 2 + 0.3, Ro), V(-Lo / 2 + 0.3, -Ro)
    sh.dim(p, q, -(yb - p[1] + 76), c.s("d_out", d=c.fv("exterior.habitat.outer_diameter")))

    # --- выноски слева (+Y) ---
    xl = V(0, Ro)[0] - 34
    left = [
        (V(v("layout.display_primary.center_x"), face - 0.03), 195,
         c.s("displays", p=c.fv("habitat.display_primary"), s=c.fv("habitat.display_secondary"),
             z=c.fv("layout.display_primary.center_height"))),
        (V(d0 + 0.15, face - dd / 2), 315, c.s("desk", x=c.rng("layout.desk.x"), h=c.fv("layout.desk.height"))),
        (V(px, face - 0.06), 385, c.s("isolate", z=c.fv("layout.ari_isolate_panel.height")), SAFE),
        (V(g0 + 0.5, face - gd / 2), 560, c.s("galley", h=c.fv("layout.galley.counter_height"))),
        (V((hy0 + hy1) / 2, 1.05), 665, c.s("wc", x=c.rng("layout.zones.hygiene"))),
        (V(st0 + 0.3, face + 0.15), 760, c.s("nook")),
        (V(e0 + 0.2, 0.55), 845, c.s("eclss", x=c.rng("layout.zones.eclss_wall"))),
    ]
    for item in left:
        feat, ty, lab = item[:3]
        col = item[3] if len(item) > 3 else INK2
        sh.leader(feat, (xl, ty), lab, side="left", color=col, tcolor=col if col != INK2 else INK)
    # камера C — слева
    pc_ = V(v("layout.camera_c.x"), v("layout.camera_c.y"))
    sh.leader((pc_[0] - 9, pc_[1]), (xl, 255), c.s("cam_c", z=c.fv("layout.camera_c.height")), side="left",
              color=CAM, tcolor=CAM, dot=False)

    # --- выноски справа (−Y) ---
    xrr = V(0, -Ro)[0] + 140
    right = [
        (V(L / 2 + 0.16, -0.3), 175, c.s("window", w=c.fv("habitat.window_width"), h=c.fv("habitat.window_height"),
                                          z=c.fv("layout.window.center_height")), INK2),
        (V(v("layout.camera_a.x"), v("layout.camera_a.y")), 330,
         c.s("cam_a", z=c.fv("layout.camera_a.height")), CAM),
        (V(1.6, -face - 0.15), 425, c.s("zone_b"), INK2),
        (V(v("layout.camera_b.x"), v("layout.camera_b.y")), 540,
         c.s("cam_b", z=c.fv("layout.camera_b.height")), CAM),
        (V(0.4, -face - 0.15), 600, c.s("storage"), INK2),
        (V(-1.3, -a2 - 0.5), 700, c.s("stasis", x=c.rng("layout.zones.stasis")), INK2),
        (V(-0.6, -1.3), 790, c.s("water"), WATER),
        (V(ax_ + hd / 2 * 0.7, -hd / 2 * 0.7), 880, c.s("hatch_alt", d=c.fv("layout.hatch.diameter")), AMBER),
        (V(-L / 2 - 0.25, -hd / 2), 985, c.s("hatch_spec", d=c.fv("layout.hatch.diameter")), INK2),
        (V(ex - bw / 2 * 0.7, -bw / 2 * 0.7), 1075, c.s("elbow"), INK2),
    ]
    for feat, ty, lab, col in right:
        tcol = col if col in (CAM, AMBER, WATER) else INK
        sh.leader(feat, (xrr, ty), lab, side="right", color=col, tcolor=tcol)
    sh.text((xrr + 14, 1135), c.s("c003"), size=12.5, color=AMBER, weight="bold")
    sh.text((xrr + 14, 1155), c.s("cones"), size=11.5, color=CAM)

    # --- оси ---
    ox, oy = 92, 1080
    sh.arrow((ox, oy), (ox, oy - 52), color=INK2, sw=1.4, marker="ai")
    sh.arrow((ox, oy), (ox - 52, oy), color=INK2, sw=1.4, marker="ai")
    sh.circle((ox, oy), 7, stroke=INK2, sw=1.2)
    sh.circle((ox, oy), 2, stroke="none", fill=INK2)
    sh.text((ox + 8, oy - 50), c.s("ax_x"), size=12, color=INK2)
    sh.text((ox - 74, oy + 4), "+Y", size=12, color=INK2)
    sh.text((ox + 14, oy + 22), c.s("ax_z"), size=11, color=INK2)

    footer(sh, c, "BP-02", scale_m=(0, 0.5, 1, 1.5, 2), k=k)
    return sh
