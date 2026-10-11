"""Геометрия жилого модуля и корабля из data/canon.json + инвариантные проверки раскладки.

Локальная рамка модуля: X — к носу (0 — середина внутренней длины), Y — влево при взгляде в нос, Z = 0 — пол,
+Z — к оси вращения. Станции хребта — метры от носового конца к корме. Всё в метрах.
Проверки падают с понятной ошибкой, если правка canon.yaml ломает раскладку (зоны перекрыты, окно не
вписывается в переборку и т. п.) — чертёж не должен молча рисовать невозможное.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

ZONE_ORDER = ["window_bay", "main_cabin", "galley_storage", "stasis", "eclss_wall", "vestibule"]
INCH = 0.0254


class LayoutError(SystemExit):
    pass


def _need(cond: bool, msg: str):
    if not cond:
        raise LayoutError(f"ошибка раскладки: {msg}")


def display_size(diag_inch: float, aspect=(16, 9)) -> tuple[float, float]:
    """Ширина и высота экрана 16:9 по диагонали в дюймах, м."""
    d = diag_inch * INCH
    a, b = aspect
    c = math.hypot(a, b)
    return d * a / c, d * b / c


@dataclass
class Hab:
    R: float          # внутренний радиус гермооболочки
    Ro: float         # наружный радиус защитной оболочки
    L: float          # внутренняя длина
    Lo: float         # наружная длина
    h: float          # пол ниже оси цилиндра (ось на Z = h)
    floor_w: float
    ceil: float
    tank_h: float
    locker_d: float
    locker_front_h: float
    aisle: float
    zones: dict

    @property
    def axis_z(self) -> float:
        return self.h

    @property
    def crown(self) -> float:
        return self.h + self.R

    @property
    def bottom(self) -> float:
        return self.h - self.R

    def half(self, z: float, r: float | None = None) -> float:
        """Полуширина окружности радиуса r (по умолчанию внутренней) на высоте z над полом."""
        r = self.R if r is None else r
        dz = z - self.h
        return math.sqrt(max(r * r - dz * dz, 0.0))

    @property
    def deck_half(self) -> float:
        return self.half(0.0)

    @property
    def ceil_half(self) -> float:
        return self.half(self.ceil)


def habitat(c) -> Hab:
    v = c.v
    zones = {z: v(f"layout.zones.{z}") for z in ZONE_ORDER + ["hygiene"]}
    hb = Hab(R=v("habitat.inner_diameter") / 2, Ro=v("exterior.habitat.outer_diameter") / 2,
             L=v("habitat.inner_length"), Lo=v("exterior.habitat.outer_length"),
             h=v("layout.hull.floor_below_axis"), floor_w=v("layout.hull.floor_width"),
             ceil=v("layout.hull.ceiling_height"), tank_h=v("layout.hull.underfloor_tank_height"),
             locker_d=v("layout.lockers.depth"), locker_front_h=v("layout.lockers.front_height"),
             aisle=v("layout.aisle_width"), zones=zones)
    check_habitat(hb, c)
    return hb


def check_habitat(hb: Hab, c):
    v = c.v
    # оболочка
    _need(0 < hb.h < hb.R, "пол должен быть ниже оси, но выше дна цилиндра")
    _need(hb.Ro > hb.R and hb.Lo > hb.L, "наружные размеры меньше внутренних")
    _need(hb.ceil < hb.crown - 0.05, f"потолок {hb.ceil} не помещается под свод {hb.crown:.2f}")
    _need(hb.ceil >= v("maya.height") + 0.3, "над головой меньше 0,3 м")
    _need(hb.tank_h < hb.R - hb.h - 0.05, "подпольные баки не помещаются в полость под палубой")
    # шкафы: фасады при |Y| = floor_w/2, глубина не выходит за корпус на высоте оси
    face = hb.floor_w / 2
    _need(face + hb.locker_d <= hb.R - 0.03, "шкафы глубже, чем позволяет корпус на высоте оси")
    _need(face < hb.deck_half, "ширина пола больше хорды палубы")
    _need(hb.locker_front_h <= hb.h + math.sqrt(hb.R ** 2 - face ** 2), "фасады шкафов выше обвода корпуса")
    # зоны: от носа к корме без зазоров и перекрытий, в пределах длины
    x = hb.L / 2
    for z in ZONE_ORDER:
        a, b = hb.zones[z]
        _need(abs(b - x) < 1e-6, f"зона {z} начинается при X={b}, ожидалось {x:.2f} (зоны идут подряд от носа)")
        _need(b > a, f"зона {z} пустая")
        x = a
    _need(abs(x + hb.L / 2) < 1e-6, f"зоны не доходят до кормы: конец {x}, ожидалось {-hb.L / 2}")
    hy, st = hb.zones["hygiene"], hb.zones["stasis"]
    _need(st[0] <= hy[0] and hy[1] <= st[1], "санузел должен лежать в полосе отсека стазиса (они бок о бок)")
    _need(hb.aisle < hb.floor_w, "проход шире пола")
    # окно: проём (наибольший из диапазона) вписывается в переборку
    ww, wh = v("habitat.window_width")[1], v("habitat.window_height")[1]
    wc = v("layout.window.center_height")
    top = wc + wh / 2
    _need(hb.half(top) >= ww / 2 + 0.03 and wc - wh / 2 > 0.3, "окно не вписывается в носовую переборку")
    _need(top <= hb.ceil, "верх окна выше потолка")
    # люк в кормовой переборке и в своде
    hd, hc = v("layout.hatch.diameter"), v("layout.hatch.center_height")
    _need(hb.half(hc + hd / 2) >= hd / 2 * 0.7 and hc - hd / 2 > 0, "люк не вписывается в кормовую переборку")
    ax = v("layout.hatch.alt_ceiling_x")
    vz = hb.zones["vestibule"]
    _need(vz[0] <= ax - hd / 2 + 1e-6 and ax <= vz[1] + 0.25,
          "люк в своде должен стоять над тамбуром (может заходить на проём стены СЖО)")
    _need(hb.ceil_half >= hd / 2 * 0.6, f"свод слишком узок для люка Ø{hd}")
    # рабочее место
    dx = v("layout.desk.x")
    mc = hb.zones["main_cabin"]
    _need(mc[0] <= dx[0] < dx[1] <= mc[1], "стол выходит за главную кабину")
    _need(v("layout.chair.seat_height") < v("layout.desk.height"), "сиденье выше стола")
    for key, rng in (("primary", "habitat.display_primary"), ("secondary", "habitat.display_secondary")):
        w, hh = display_size(v(rng)[1])
        cx, cz = v(f"layout.display_{key}.center_x"), v(f"layout.display_{key}.center_height")
        _need(cz - hh / 2 > v("layout.desk.height"), f"дисплей {key} ниже столешницы")
        _need(mc[0] - 0.2 <= cx - w / 2 and cx + w / 2 <= mc[1], f"дисплей {key} выходит за главную кабину")
    p1, p2 = display_size(v("habitat.display_primary")[1]), display_size(v("habitat.display_secondary")[1])
    c1, c2 = v("layout.display_primary.center_x"), v("layout.display_secondary.center_x")
    _need(abs(c1 - c2) >= (p1[0] + p2[0]) / 2, "дисплеи перекрываются")
    px, pz = v("layout.ari_isolate_panel.x"), v("layout.ari_isolate_panel.height")
    _need(v("layout.desk.height") < pz < v("layout.display_secondary.center_height") - p2[1] / 2,
          "панель ARI ISOLATE должна быть между столешницей и вспомогательным дисплеем")
    # камеры внутри корпуса
    for cam in "abc":
        x, y, z = (v(f"layout.camera_{cam}.{k}") for k in ("x", "y", "height"))
        _need(-hb.L / 2 < x < hb.L / 2, f"камера {cam} вне длины модуля")
        _need(abs(y) < hb.half(z) - 0.05 and 0 < z < hb.crown, f"камера {cam} вне сечения корпуса")


@dataclass
class Ship:
    L: float
    d: float
    hub: float
    floor_r: float
    hab_center: float     # станция центра жилого модуля
    hab_axis_r: float     # радиус оси цилиндра модуля
    boom_w: float
    cw_r: tuple
    cw_len: float
    cw_d: float


def ship(c, hb: Hab) -> Ship:
    v = c.v
    hub = v("exterior.hub.station")
    elbow = v("exterior.boom.elbow_x")       # X оси фермы в лок. рамке модуля (отрицательный — к корме)
    s = Ship(L=v("exterior.spine.length"), d=v("exterior.spine.diameter"), hub=hub,
             floor_r=v("habitat.floor_radius"), hab_center=hub + elbow, hab_axis_r=v("habitat.floor_radius") - hb.h,
             boom_w=v("exterior.boom.width"), cw_r=tuple(v("exterior.counterweight.radius")),
             cw_len=v("exterior.counterweight.length"), cw_d=v("exterior.counterweight.diameter"))
    check_ship(s, hb, c)
    return s


def check_ship(s: Ship, hb: Hab, c):
    v = c.v
    _need(-hb.Lo / 2 - v("exterior.boom.width") / 2 > v("exterior.boom.elbow_x") - 1.5,
          "колено фермы слишком далеко за кормой")
    _need(v("exterior.boom.elbow_x") < -hb.Lo / 2, "ось фермы (вариант SPEC) должна быть за кормовым торцем")
    seq = ["comms", "tanks", "radiators", "reactor", "propulsion"]
    prev = -1.0
    for k in seq:
        a, b = v(f"exterior.{k}.station")
        _need(a >= prev - 1e-6 and b > a, f"станции хребта не по порядку на {k}")
        prev = b
    _need(abs(v("exterior.propulsion.station")[1] - s.L) < 1e-6, "срез двигателей должен совпадать с концом хребта")
    _need(v("exterior.comms.station")[1] < s.hub < v("exterior.tanks.station")[0], "ступица вне промежутка "
          "между носовой секцией и баками")
    core, cl = v("exterior.ari_core.station"), v("exterior.ari_core.vault_length")
    bat = v("exterior.ari_core.battery_station")
    _need(abs(core - s.hub) < cl / 2, "ядро ARI должно быть в ступице")
    _need(bat[0] >= core + cl / 2 - 1e-6 and bat[1] <= v("exterior.tanks.station")[0], "батареи между сейфом и баками")
    _need(abs(v("exterior.ari_core.manual_breaker.station") - s.hub) < cl / 2, "рубильник не у сейфа")
    _need(v("exterior.ari_core.manual_breaker.radius") > v("exterior.ari_core.vault_diameter") / 2,
          "рубильник внутри сейфа")
    hab_top = s.hab_axis_r - hb.Ro
    _need(hab_top > v("exterior.tanks.diameter") / 2, "жилой модуль задевает баки")
    _need(s.cw_r[0] - s.cw_d / 2 > v("exterior.ari_core.vault_diameter") / 2 + 2, "противовес слишком близко к оси")
