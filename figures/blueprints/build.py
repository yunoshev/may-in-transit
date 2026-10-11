"""Чертежи-синьки корабля Maya in Transit: SVG из data/canon.json и data/strings.yaml.

Запуск:  uv run figures/blueprints/build.py [--only ИМЯ] [--check]
Выход:   assets/ship/<имя>.ru.svg и assets/ship/<имя>.en.svg
  ship-side-schematic   — корабль сбоку: хребет, ось и вращение, модуль на радиусе пола, противовес, ядро ARI
  habitat-plan          — план жилого модуля: зоны, окно, люки (C-003), камеры A/B/C, панель ARI ISOLATE
  habitat-cross-section — поперечный разрез через главную кабину
  habitat-long-section  — продольный разрез: окно, зоны, высоты, тамбур и люк (C-003)
Числа — только из data/canon.json (сначала uv run calc/derive.py); геометрия проверяется (geom.py) и при
невозможной раскладке сборка падает. Детерминирован: при неизменном входе файлы не переписываются.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import bp  # noqa: E402
import sheet_cross  # noqa: E402
import sheet_long  # noqa: E402
import sheet_plan  # noqa: E402
import sheet_side  # noqa: E402

ROOT = bp.ROOT
OUT = ROOT / "assets" / "ship"
SHEETS = {
    "ship-side-schematic": ("ship_side", sheet_side.render),
    "habitat-plan": ("habitat_plan", sheet_plan.render),
    "habitat-cross-section": ("habitat_cross", sheet_cross.render),
    "habitat-long-section": ("habitat_long", sheet_long.render),
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", choices=sorted(SHEETS), help="собрать один лист")
    ap.add_argument("--check", action="store_true", help="ничего не писать; код 1, если SVG устарели")
    args = ap.parse_args()
    canon_json = ROOT / "data" / "canon.json"
    if not canon_json.exists():
        raise SystemExit("нет data/canon.json — сначала uv run calc/derive.py")
    vals = json.loads(canon_json.read_text(encoding="utf-8"))["values"]
    strings = bp.canonlib.load_yaml(ROOT / "data" / "strings.yaml")
    OUT.mkdir(parents=True, exist_ok=True)
    stale = 0
    for name, (skey, render) in SHEETS.items():
        if args.only and name != args.only:
            continue
        for lang in ("ru", "en"):
            ctx = bp.Ctx(vals, strings, skey, lang)
            svg = render(ctx).svg()
            path = OUT / f"{name}.{lang}.svg"
            old = path.read_text(encoding="utf-8") if path.exists() else None
            rel = path.relative_to(ROOT)
            if old == svg:
                print(f"без изменений: {rel}", flush=True)
            elif args.check:
                stale += 1
                print(f"устарел: {rel}", flush=True)
            else:
                path.write_text(svg, encoding="utf-8")
                print(f"записан: {rel}", flush=True)
    raise SystemExit(1 if stale else 0)


if __name__ == "__main__":
    main()
