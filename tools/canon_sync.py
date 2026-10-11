"""Синхронизация чисел в тексте с data/canon.yaml и data/derived.yaml.

Число в markdown привязано так:  <span data-canon="habitat.floor_radius">28 м</span>
Ключ ищется в canon.yaml, затем в derived.yaml. Формат — по языку файла:
  ru/ — десятичная запятая, unit;  en/ — точка, unit_en;  диапазон через «–»;  «≈» и точность — из format.
Спаны внутри кода (``` и `…`) и HTML-комментариев не трогаются.

Режимы:
  --check   (по умолчанию) печатает «файл:строка ключ ожидалось «…» найдено «…»», код 1 при расхождении
            или неизвестном ключе; также ловит устаревшие derived.yaml и canon-values.md
  --write   переписывает ТЕКСТ внутри спанов, остальное байт в байт
  --render  генерирует ru/90-reference/canon-values.md

Запуск: uv run tools/canon_sync.py [--check|--write|--render] [--root ПАПКА] [--data ПАПКА]
"""
from __future__ import annotations

import argparse
import os
import re
import signal
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import canonlib  # noqa: E402
import mdscan  # noqa: E402

SPAN_RE = re.compile(r"<span\b(?P<attrs>[^>]*)>(?P<text>[^<]*)</span>")
ATTR_RE = re.compile(r"\bdata-canon\s*=\s*(?P<q>[\"'])(?P<key>.*?)(?P=q)")
LANGS = ("ru", "en")
RENDER_PATH = Path("ru/90-reference/canon-values.md")


def scan_spans(text: str):
    """→ [(start, end, key, inner_start, inner_end, inner_text)] вне кода."""
    masked = mdscan.code_mask(text)
    out = []
    for m in SPAN_RE.finditer(text):
        if masked[m.start():m.end()] != text[m.start():m.end()]:
            continue  # спан целиком или частично в коде/комментарии
        a = ATTR_RE.search(m.group("attrs"))
        if not a:
            continue
        out.append((m.start(), m.end(), a.group("key").strip(), m.start("text"), m.end("text"), m.group("text")))
    return out


def md_files(root: Path):
    for lang in LANGS:
        base = root / lang
        if base.is_dir():
            for p in sorted(base.rglob("*.md")):
                if not any(part.startswith(".") for part in p.relative_to(root).parts):
                    yield lang, p


def check_or_write(root: Path, canon: dict, derived: dict, write: bool) -> tuple[int, int, int, int]:
    n_spans = n_files = bad = unknown = 0
    for lang, path in md_files(root):
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        spans = scan_spans(text)
        if not spans:
            continue
        n_files += 1
        rel = path.relative_to(root).as_posix()
        pieces, last, changed = [], 0, False
        for start, end, key, i0, i1, found in spans:
            n_spans += 1
            line = mdscan.line_of(text, start)
            entry = canonlib.lookup(key, canon, derived)
            if entry is None:
                unknown += 1
                print(f"{rel}:{line} {key} неизвестный ключ, найдено «{found}»", flush=True)
                continue
            expected = canonlib.format_value(entry, lang)
            if canonlib.normalize_ws(found).strip() == expected:
                continue
            bad += 1
            if write:
                pieces.append(text[last:i0])
                pieces.append(expected)
                last = i1
                changed = True
                print(f"{rel}:{line} {key} «{found}» → «{expected}»", flush=True)
            else:
                print(f"{rel}:{line} {key} ожидалось «{expected}» найдено «{found}»", flush=True)
        if write and changed:
            pieces.append(text[last:])
            path.write_bytes("".join(pieces).encode("utf-8"))
    return n_spans, n_files, bad, unknown


# ---------- render ----------

def _cell(s) -> str:
    return str(s).replace("\n", " ").replace("|", "\\|").strip()


def _source_md(src: str, page_dir: Path, root: Path) -> str:
    if src.startswith("http://") or src.startswith("https://"):
        return f"[{urlparse(src).netloc}]({src})"
    path, sep, section = src.partition(" §")
    target = root / path
    if path.startswith("sources/") or target.exists():
        rel = os.path.relpath(target, page_dir).replace(os.sep, "/")
        label = Path(path).name + (f" §{section}" if sep else "")
        return f"[{_cell(label)}]({rel})"
    return _cell(src)


def _raw_number(v) -> str:
    if isinstance(v, list):
        return canonlib.DASH.join(_raw_number(x) for x in v)
    s = f"{v:.6g}" if isinstance(v, float) else str(v)
    return s.replace("-", canonlib.MINUS).replace(".", ",")


def _groups(entries: dict) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for k in entries:
        groups.setdefault(k.split(".", 1)[0], []).append(k)
    return groups


def render_page(root: Path, data_dir: Path, canon: dict, derived: dict) -> str:
    page = root / RENDER_PATH
    page_dir = page.parent
    strings = {}
    sp = data_dir / "strings.yaml"
    if sp.exists():
        strings = (canonlib.load_yaml(sp) or {}).get("canon_groups") or {}
    gname = lambda g: (strings.get(g) or {}).get("ru", g)  # noqa: E731

    files = []
    for e in canon.values():
        for s in canonlib.sources_of(e):
            p = s.partition(" §")[0]
            if p.startswith("sources/") and p not in files:
                files.append(p)

    L = []
    L += ["---", "title: Канонические значения", "aliases: [canon values, канон-значения, канонические числа]",
          "type: reference", "status: draft", "sources:"]
    L += [f"  - {p}" for p in files]
    L += ["tags: [reference, canon]", "---", "", "# Канонические значения", "",
          "> Генерируется tools/canon_sync.py — не править руками.",
          "> Входные числа правят в `data/canon.yaml`, производные считает `calc/derive.py` → `data/derived.yaml`;",
          "> затем `uv run tools/canon_sync.py --render`.", "",
          "Кратко: все числа мира в одном месте. В тексте число привязывается спаном "
          "`<span data-canon=\"habitat.floor_radius\">28 м</span>`, а `uv run tools/canon_sync.py --check` "
          "сверяет его с этой таблицей.", "",
          f"Входных значений: {len(canon)}, производных: {len(derived)}.", "",
          "## Входные значения", ""]
    for g, keys in _groups(canon).items():
        L += [f"### {gname(g)}", "", "| Ключ | Значение | Единица | Статус | Источник | Примечание |",
              "|---|---|---|---|---|---|"]
        for k in keys:
            e = canon[k]
            src = ", ".join(_source_md(s, page_dir, root) for s in canonlib.sources_of(e)) or "—"
            L.append(f"| `{k}` | {_cell(canonlib.format_value(e, 'ru', with_unit=False))} | "
                     f"{_cell(e.get('unit') or '—')} | {e['status']} | {src} | {_cell(e.get('note', ''))} |")
        L.append("")
    L += ["## Производные величины", "",
          "Считает `calc/derive.py`; статус производной — самый слабый из статусов входов.", ""]
    for g, keys in _groups(derived).items():
        L += [f"### {gname(g)}", "",
              "| Ключ | Значение | Без округления | Единица | Формула | Входы | Статус | Примечание |",
              "|---|---|---|---|---|---|---|---|"]
        for k in keys:
            e = derived[k]
            inputs = ", ".join(f"`{i}`" for i in e.get("inputs", []))
            L.append(f"| `{k}` | {_cell(canonlib.format_value(e, 'ru', with_unit=False))} | "
                     f"{_raw_number(e['value'])} | {_cell(e.get('unit') or '—')} | `{_cell(e['formula'])}` | "
                     f"{inputs} | {e['status']} | {_cell(e.get('note', ''))} |")
        L.append("")
    L += ["## Связи",
          "- [Справочное](index.md) — оглавление раздела",
          "- [Решения](decisions.md) — изменения канонических чисел фиксируются здесь",
          "- [Противоречия](contradictions.md) — расхождения чисел между исходниками (C-001: радиус пола)",
          ""]
    return "\n".join(L)


def main():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="сверить спаны (по умолчанию)")
    mode.add_argument("--write", action="store_true", help="переписать текст спанов")
    mode.add_argument("--render", action="store_true", help="сгенерировать ru/90-reference/canon-values.md")
    ap.add_argument("--root", type=Path, default=canonlib.REPO_ROOT, help="корень вики (где ru/ и en/)")
    ap.add_argument("--data", type=Path, default=None, help="папка с canon.yaml (по умолчанию <root>/data)")
    args = ap.parse_args()
    root = args.root.resolve()
    data_dir = (args.data or root / "data").resolve()

    canon, derived, errors = canonlib.load_canon(data_dir)
    for e in errors:
        print(f"ошибка данных: {e}", flush=True)
    if errors:
        raise SystemExit(1)

    problems = 0
    meta = canonlib.derived_meta(data_dir)
    if not derived:
        print("предупреждение: нет data/derived.yaml — запустите uv run calc/derive.py", flush=True)
    elif meta.get("canon_sha256") != canonlib.sha256_file(data_dir / "canon.yaml"):
        print("ошибка: data/derived.yaml устарел относительно canon.yaml — запустите uv run calc/derive.py", flush=True)
        problems += 1

    if args.render:
        if problems:
            raise SystemExit(1)
        page = root / RENDER_PATH
        text = render_page(root, data_dir, canon, derived)
        if page.exists() and page.read_text(encoding="utf-8") == text:
            print(f"без изменений: {RENDER_PATH.as_posix()}", flush=True)
        else:
            page.parent.mkdir(parents=True, exist_ok=True)
            page.write_text(text, encoding="utf-8")
            print(f"записан: {RENDER_PATH.as_posix()}", flush=True)
        return

    n_spans, n_files, bad, unknown = check_or_write(root, canon, derived, write=args.write)
    if not args.write:
        page = root / RENDER_PATH
        if page.exists():
            if page.read_text(encoding="utf-8") != render_page(root, data_dir, canon, derived):
                print(f"ошибка: {RENDER_PATH.as_posix()} устарела — запустите uv run tools/canon_sync.py --render",
                      flush=True)
                problems += 1
        elif (root / "ru").is_dir():
            print(f"предупреждение: нет {RENDER_PATH.as_posix()} — запустите --render", flush=True)
    verb = "исправлено" if args.write else "расхождений"
    print(f"canon_sync: спанов {n_spans} в {n_files} файлах; {verb} {bad}; "
          f"неизвестных ключей {unknown}; прочих ошибок {problems}", flush=True)
    raise SystemExit(1 if ((bad and not args.write) or unknown or problems) else 0)


if __name__ == "__main__":
    main()
