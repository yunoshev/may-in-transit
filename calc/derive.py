"""Производные величины из data/canon.yaml → data/derived.yaml и data/canon.json.

Запуск: uv run calc/derive.py [--root ПАПКА] [--check]
  --check  ничего не пишет; код 1, если derived.yaml или canon.json устарели.
Идемпотентен: при неизменном входе файлы не переписываются.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import canonlib  # noqa: E402

STATUS_RANK = {s: i for i, s in enumerate(canonlib.STATUSES)}

ASTRO_MODEL_NOTE = (
    "Модель: Земля на круговой орбите 1 а. е.; Юпитер — кеплеров эллипс (a, e по NSSDC); "
    "орбиты компланарны (наклон Юпитера 1,3° не учтён); минимум — противостояние при Юпитере в перигелии, "
    "максимум — соединение при Юпитере в афелии. Корабль в системе Юпитера считается в его центре "
    "(орбиты спутников — до ~1,9 млн км, < 0,5 %). Теоретические крайние значения NSSDC с учётом "
    "эксцентриситета Земли — 588,5–968,5 млн км (astro.earth_jupiter_*_nssdc)."
)
LIGHT_NOTE = (
    "Задержка сигнала в одну сторону: расстояние / c, по прямой, без задержек в аппаратуре и релятивистских "
    "поправок. Допущения расстояния — см. astro.earth_jupiter_distance."
)


def build(v: dict) -> list[dict]:
    """v — входные значения (ключ → число или [min, max]). Возвращает список производных.

    Каждая производная: key, value (полная точность), unit, unit_en, format, formula, inputs, note.
    Цепочки считаются по полной точности; округление — только при записи.
    """
    out: list[dict] = []
    full: dict = {}

    def d(key, value, unit, unit_en, formula, inputs, note, fmt=None):
        full[key] = value
        out.append(dict(key=key, value=value, unit=unit, unit_en=unit_en, format=fmt or {},
                        formula=formula, inputs=inputs, note=note))
        return value

    def val(k):
        return full[k] if k in full else v[k]

    # --- тяжесть и вращение ---
    a = d("habitat.floor_accel", v["habitat.floor_gravity"] * v["physics.g_earth"], "м/с²", "m/s²",
          "a = g_пол · g", ["habitat.floor_gravity", "physics.g_earth"],
          "Целевое ускорение на полу; совпадает с 4,905 м/с² из SPEC §4 и CONCEPT.", {"decimals": 3})
    d("production.blender_gravity_z", -a, "м/с²", "m/s²", "Z = −a", ["habitat.floor_accel"],
      "Scene Gravity Z в Blender (SPEC §4): интерьер не вращается, тяжесть — постоянная вниз.",
      {"decimals": 3})
    r = v["habitat.floor_radius"]
    w = d("ship.spin_omega", math.sqrt(a / r), "рад/с", "rad/s", "ω = √(a / r)",
          ["habitat.floor_accel", "habitat.floor_radius"],
          "Угловая скорость вращения корабля вокруг продольной оси (из a = ω²r).", {"decimals": 3})
    d("ship.spin_rpm", w * 60 / (2 * math.pi), "об/мин", "rpm", "n = 60 · ω / 2π", ["ship.spin_omega"],
      "SPEC §1.1 и §40 округляют до «~4 rpm».", {"decimals": 1, "approx": True})
    t = d("ship.spin_period", 2 * math.pi / w, "с", "s", "T = 2π / ω", ["ship.spin_omega"],
          "Период одного оборота корабля.", {"decimals": 1, "approx": True})

    rc = v["habitat.floor_radius_concept"]
    wc = math.sqrt(a / rc)
    d("ship.spin_rpm_concept", wc * 60 / (2 * math.pi), "об/мин", "rpm", "n = 60 · √(a / r_concept) / 2π",
      ["habitat.floor_accel", "habitat.floor_radius_concept"],
      "Обороты для варианта CONCEPT 25 м; совпадает с «4.23 rpm» из CONCEPT (C-001).",
      {"decimals": 2, "approx": True})
    d("ship.spin_period_concept", 2 * math.pi / wc, "с", "s", "T = 2π / √(a / r_concept)",
      ["habitat.floor_accel", "habitat.floor_radius_concept"], "Период вращения для варианта CONCEPT 25 м.",
      {"decimals": 1, "approx": True})
    lo, hi = v["habitat.floor_radius_concept_range"]
    d("ship.spin_rpm_concept_range",
      [math.sqrt(a / hi) * 60 / (2 * math.pi), math.sqrt(a / lo) * 60 / (2 * math.pi)],
      "об/мин", "rpm", "n = 60 · √(a / r) / 2π, r = 30…20 м",
      ["habitat.floor_accel", "habitat.floor_radius_concept_range"],
      "Обороты на краях диапазона радиусов CONCEPT 20–30 м.", {"decimals": 1, "approx": True})

    # --- геометрия модуля ---
    dia, length = v["habitat.inner_diameter"], v["habitat.inner_length"]
    gross = d("habitat.gross_volume", math.pi * (dia / 2) ** 2 * length, "м³", "m³", "V = π · (D / 2)² · L",
              ["habitat.inner_diameter", "habitat.inner_length"],
              "Брутто-объём внутреннего цилиндра без торцевых днищ; SPEC §3: «roughly 37 m³».",
              {"decimals": 0, "approx": True})
    u_lo, u_hi = v["habitat.usable_volume"]
    d("habitat.usable_fraction", [100 * u_lo / gross, 100 * u_hi / gross], "%", "%", "V_полезн / V × 100 %",
      ["habitat.usable_volume", "habitat.gross_volume"],
      "Доля полезного объёма от брутто-объёма цилиндра.", {"decimals": 0, "approx": True})

    # --- градиент тяжести ---
    h = v["maya.height"]
    g = v["physics.g_earth"]
    a_head = d("gravity.head_accel", w ** 2 * (r - h), "м/с²", "m/s²", "a_гол = ω² · (r − h)",
               ["ship.spin_omega", "habitat.floor_radius", "maya.height"],
               "Тяжесть на высоте головы стоящей Майи (h — рост, голова на h над полом, ближе к оси).",
               {"decimals": 2})
    d("gravity.head_g", a_head / g, "g", "g", "a_гол / g", ["gravity.head_accel", "physics.g_earth"],
      "То же в долях земной тяжести.", {"decimals": 2})
    d("gravity.gradient_head", 100 * (a - a_head) / a, "%", "%", "(a − a_гол) / a × 100 % = h / r × 100 %",
      ["habitat.floor_accel", "gravity.head_accel"],
      "Перепад тяжести от ног к голове: голова легче ступней на эту долю.", {"decimals": 1})

    # --- Кориолис ---
    vw = v["physics.walk_speed"]
    cor = d("gravity.coriolis_across", 2 * w * vw, "м/с²", "m/s²", "a_К = 2 · ω · v",
            ["ship.spin_omega", "physics.walk_speed"],
            "Шаг поперёк кабины (по Y, касательно вращению; v ⊥ ω). Кориолисово ускорение радиальное: "
            "по ходу вращения Майя тяжелее, против — легче на эту величину; центробежная поправка v²/r "
            "≈ 0,04 м/с² — на порядок меньше.", {"decimals": 2})
    d("gravity.coriolis_across_frac", 100 * cor / a, "%", "%", "2 · ω · v / a × 100 %",
      ["gravity.coriolis_across", "habitat.floor_accel"],
      "Кориолис при шаге поперёк кабины в долях местной тяжести на полу.", {"decimals": 0, "approx": True})
    d("gravity.coriolis_along", 0.0, "м/с²", "m/s²", "a_К = 2 · ω × v = 0 при v ∥ ω",
      ["ship.spin_omega", "physics.walk_speed"],
      "Шаг вдоль кабины: ось модуля параллельна оси вращения (SPEC §4: +X — вперёд по оси), v ∥ ω, "
      "векторное произведение равно нулю. Подъём и приседание (по Z) дают боковой снос.", {"decimals": 0})

    d("habitat.window_image_period", t, "с", "s", "T_окно = T = 2π / ω", ["ship.spin_period"],
      "Окно смотрит вдоль оси вращения (SPEC §8): картинка не уходит из окна, а поворачивается вокруг "
      "центра окна с периодом вращения корабля; объект точно на оси вращается на месте.",
      {"decimals": 1, "approx": True})

    # --- Земля – Юпитер ---
    aj, ej, ae = v["astro.jupiter_a"], v["astro.jupiter_e"], v["astro.earth_a"]
    au_mkm = v["physics.au"] / 1e6
    c = v["physics.speed_of_light"]
    dmin_au = d("astro.earth_jupiter_min_au", aj * (1 - ej) - ae, "а. е.", "AU", "d_min = a_J · (1 − e_J) − a_З",
                ["astro.jupiter_a", "astro.jupiter_e", "astro.earth_a"], ASTRO_MODEL_NOTE,
                {"decimals": 2, "approx": True})
    dmax_au = d("astro.earth_jupiter_max_au", aj * (1 + ej) + ae, "а. е.", "AU", "d_max = a_J · (1 + e_J) + a_З",
                ["astro.jupiter_a", "astro.jupiter_e", "astro.earth_a"], ASTRO_MODEL_NOTE,
                {"decimals": 2, "approx": True})
    dmin = d("astro.earth_jupiter_min", dmin_au * au_mkm, "млн км", "million km", "d_min · а. е.",
             ["astro.earth_jupiter_min_au", "physics.au"], ASTRO_MODEL_NOTE, {"decimals": 0, "approx": True})
    dmax = d("astro.earth_jupiter_max", dmax_au * au_mkm, "млн км", "million km", "d_max · а. е.",
             ["astro.earth_jupiter_max_au", "physics.au"], ASTRO_MODEL_NOTE, {"decimals": 0, "approx": True})
    d("astro.earth_jupiter_distance", [dmin, dmax], "млн км", "million km", "[d_min, d_max]",
      ["astro.earth_jupiter_min", "astro.earth_jupiter_max"], ASTRO_MODEL_NOTE, {"decimals": 0, "approx": True})
    lmin = d("astro.light_delay_min", dmin * 1e6 / c / 60, "мин", "min", "τ_min = d_min / c",
             ["astro.earth_jupiter_min", "physics.speed_of_light"], LIGHT_NOTE, {"decimals": 0, "approx": True})
    lmax = d("astro.light_delay_max", dmax * 1e6 / c / 60, "мин", "min", "τ_max = d_max / c",
             ["astro.earth_jupiter_max", "physics.speed_of_light"], LIGHT_NOTE, {"decimals": 0, "approx": True})
    d("astro.light_delay", [lmin, lmax], "мин", "min", "[τ_min, τ_max]",
      ["astro.light_delay_min", "astro.light_delay_max"], LIGHT_NOTE, {"decimals": 0, "approx": True})
    return out


def _round(x):
    if isinstance(x, list):
        return [_round(i) for i in x]
    y = float(f"{x:.6g}")
    return 0.0 if y == 0 else y


def weakest_status(keys, statuses: dict) -> str:
    return min((statuses[k] for k in keys), key=lambda s: STATUS_RANK[s])


def render_files(root: Path):
    data = root / "data"
    canon, _, errors = canonlib.load_canon(data)
    errors = [e for e in errors if e.startswith("canon.yaml")]
    if errors:
        for e in errors:
            print(f"ошибка: {e}", flush=True)
        raise SystemExit(1)
    values = {k: e["value"] for k, e in canon.items()}
    derived = build(values)

    statuses = {k: e["status"] for k, e in canon.items()}
    entries = {}
    for item in derived:
        k = item["key"]
        if k in canon:
            raise SystemExit(f"ошибка: производная {k} совпадает с ключом canon.yaml")
        missing = [i for i in item["inputs"] if i not in statuses]
        if missing:
            raise SystemExit(f"ошибка: {k}: неизвестные входы {missing}")
        status = weakest_status(item["inputs"], statuses)
        statuses[k] = status
        e = {"value": _round(item["value"]), "unit": item["unit"], "unit_en": item["unit_en"], "status": status}
        if item["format"]:
            e["format"] = item["format"]
        e["formula"] = item["formula"]
        e["inputs"] = item["inputs"]
        e["note"] = item["note"]
        entries[k] = e

    meta = {"generated_by": "calc/derive.py", "canon_sha256": canonlib.sha256_file(data / "canon.yaml")}
    header = "# Генерируется calc/derive.py из data/canon.yaml — не править руками.\n"
    derived_text = header + yaml.safe_dump({"meta": meta, "values": entries}, allow_unicode=True,
                                           sort_keys=False, width=100, default_flow_style=None)

    merged = {}
    for k, e in canon.items():
        merged[k] = {"kind": "canon", **e}
    for k, e in entries.items():
        merged[k] = {"kind": "derived", **e}
    json_text = json.dumps({"meta": {**meta, "note": "Слияние canon.yaml и derived.yaml; генерирует calc/derive.py"},
                            "values": merged}, ensure_ascii=False, indent=2) + "\n"
    return {data / "derived.yaml": derived_text, data / "canon.json": json_text}, entries


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=canonlib.REPO_ROOT)
    ap.add_argument("--check", action="store_true", help="только проверить, что файлы актуальны")
    args = ap.parse_args()
    files, entries = render_files(args.root.resolve())
    stale = 0
    for path, text in files.items():
        old = path.read_text(encoding="utf-8") if path.exists() else None
        rel = path.relative_to(args.root.resolve())
        if old == text:
            print(f"без изменений: {rel}", flush=True)
            continue
        stale += 1
        if args.check:
            print(f"устарел: {rel} — запустите uv run calc/derive.py", flush=True)
        else:
            path.write_text(text, encoding="utf-8")
            print(f"записан: {rel}", flush=True)
    if not args.check:
        for k, e in entries.items():
            print(f"  {k} = {canonlib.format_value(e, 'ru')}", flush=True)
    raise SystemExit(1 if (args.check and stale) else 0)


if __name__ == "__main__":
    main()
