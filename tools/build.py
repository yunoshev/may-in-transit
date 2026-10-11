"""Пересборка всего, что выводится из канона: производные числа, числа в тексте, свод значений, чертежи, графики,
сводка открытых вопросов.

Запуск:
  uv run tools/build.py            пересобрать и проверить (canon_sync --check, lint)
  uv run tools/build.py --check    ничего не писать; код 1, если что-то устарело
  uv run tools/build.py --watch    пересобирать при каждом сохранении входных файлов (Ctrl+C — выход)
  uv run tools/build.py --no-verify  пересобрать без проверок (так собирает сайт в CI)

Порядок: calc/derive.py → canon_sync --write (спаны data-canon в тексте) → canon_sync --render (canon-values.md)
→ figures/blueprints/build.py (чертежи BP-NN) → calc/plots/*.py (графики) → tools/questions.py (сводка вопросов)
→ canon_sync --check → lint.
Страницы вставляют SVG по ссылке, поэтому после пересборки Obsidian и сайт показывают новую версию сами.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable

# входы, при изменении которых --watch пересобирает; выходы (derived.yaml, canon.json, assets/) сюда не входят
WATCH = [ROOT / "data" / "canon.yaml", ROOT / "data" / "strings.yaml"]
WATCH_DIRS = [ROOT / "calc", ROOT / "figures" / "blueprints"]
QUESTIONS = ROOT / "ru" / "00-open-questions"  # страницы q-*.md: ответ, вписанный в Obsidian, сразу попадает в сводку


def plots():
    return sorted((ROOT / "calc" / "plots").glob("*.py"))


def steps(check, verify):
    if check:
        yield ["calc/derive.py", "--check"]
        yield ["tools/canon_sync.py", "--check"]
        yield ["figures/blueprints/build.py", "--check"]
        yield ["tools/questions.py", "--check"]
        yield ["tools/lint.py", "--quiet"]
        return
    yield ["calc/derive.py"]
    yield ["tools/canon_sync.py", "--write"]
    yield ["tools/canon_sync.py", "--render"]
    yield ["figures/blueprints/build.py"]
    for p in plots():
        yield [str(p.relative_to(ROOT))]
    yield ["tools/questions.py"]
    if verify:
        yield ["tools/canon_sync.py", "--check"]
        yield ["tools/lint.py", "--quiet"]


def run(check, verify):
    failed = []
    for args in steps(check, verify):
        print(f"\n▶ {' '.join(args)}", flush=True)
        if subprocess.run([PY, *args], cwd=ROOT).returncode != 0:
            failed.append(args[0])
    status = "ошибки в: " + ", ".join(failed) if failed else "всё собрано"
    print(f"\n{status}", flush=True)
    return 1 if failed else 0


def snapshot():
    files = [p for p in WATCH if p.exists()]
    for d in WATCH_DIRS:
        files += [p for p in d.rglob("*.py") if "__pycache__" not in p.parts]
    files += list(QUESTIONS.glob("q-*.md"))
    return {p: p.stat().st_mtime_ns for p in files}


def watch(verify):
    seen = snapshot()
    run(False, verify)
    print("\nслежу за data/canon.yaml, data/strings.yaml, calc/, figures/blueprints/, ru/00-open-questions/ — Ctrl+C для выхода",
          flush=True)
    try:
        while True:
            time.sleep(1)
            now = snapshot()
            changed = [p for p in now if seen.get(p) != now[p]] + [p for p in seen if p not in now]
            if changed:
                names = ", ".join(str(p.relative_to(ROOT)) for p in changed[:3])
                print(f"\n=== изменилось: {names}", flush=True)
                run(False, verify)
                seen = snapshot()
    except KeyboardInterrupt:
        print("\nостановлено", flush=True)
        return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="ничего не писать; код 1, если что-то устарело")
    mode.add_argument("--watch", action="store_true", help="пересобирать при сохранении входных файлов")
    ap.add_argument("--no-verify", action="store_true", help="не запускать canon_sync --check и lint")
    args = ap.parse_args()
    if args.watch:
        raise SystemExit(watch(not args.no_verify))
    raise SystemExit(run(args.check, not args.no_verify))


if __name__ == "__main__":
    main()
