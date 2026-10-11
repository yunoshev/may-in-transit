"""Общая часть: загрузка data/canon.yaml и data/derived.yaml, форматирование чисел по языку.

Используют tools/canon_sync.py, calc/derive.py, calc/plots/*.
"""
from __future__ import annotations

import hashlib
import math
from pathlib import Path

import yaml

try:
    _Loader = yaml.CSafeLoader
except AttributeError:  # pragma: no cover
    _Loader = yaml.SafeLoader

REPO_ROOT = Path(__file__).resolve().parent.parent
STATUSES = ["draft", "proposed", "canon", "frozen"]
NO_SPACE_UNITS = {"%", "″", "′", "°"}
FORMAT_KEYS = {"decimals", "approx", "unit_space"}
ENTRY_KEYS = {"value", "unit", "unit_en", "status", "source", "note", "format"}
DERIVED_KEYS = ENTRY_KEYS | {"formula", "inputs"}
MINUS = "−"
DASH = "–"
APPROX = "≈"
SPACES = {" ": " ", " ": " ", " ": " ", " ": " "}


def load_yaml(path: Path):
    with open(path, encoding="utf-8") as f:
        return yaml.load(f, Loader=_Loader)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def flatten(tree, prefix: str = "", out=None, errors=None):
    """Дерево групп → {"группа.ключ": запись}. Лист — словарь с полем value.

    Ключи верхнего уровня, начинающиеся с «_», служебные и пропускаются.
    """
    out = {} if out is None else out
    errors = [] if errors is None else errors
    if not isinstance(tree, dict):
        errors.append(f"{prefix or '<корень>'}: ожидался словарь")
        return out, errors
    for k, v in tree.items():
        if not isinstance(k, str):
            errors.append(f"{prefix}{k}: ключ должен быть строкой")
            continue
        if not prefix and k.startswith("_"):
            continue
        key = f"{prefix}{k}"
        if isinstance(v, dict) and "value" in v:
            out[key] = v
        elif isinstance(v, dict):
            flatten(v, key + ".", out, errors)
        else:
            errors.append(f"{key}: не группа и не запись (нет поля value)")
    return out, errors


def _is_num(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def validate_entry(key: str, e: dict, derived: bool = False) -> list[str]:
    errs = []
    allowed = DERIVED_KEYS if derived else ENTRY_KEYS
    extra = set(e) - allowed
    if extra:
        errs.append(f"{key}: лишние поля {sorted(extra)}")
    v = e.get("value")
    if isinstance(v, list):
        if len(v) != 2 or not all(_is_num(x) for x in v):
            errs.append(f"{key}: диапазон должен быть [min, max] из двух чисел")
        elif v[0] > v[1]:
            errs.append(f"{key}: в диапазоне min > max")
    elif not _is_num(v):
        errs.append(f"{key}: value должно быть числом или [min, max]")
    for f in ("unit", "unit_en"):
        if not isinstance(e.get(f), str):
            errs.append(f"{key}: нет поля {f} (строка, \"\" для безразмерной)")
    if e.get("status") not in STATUSES:
        errs.append(f"{key}: status «{e.get('status')}» не из {STATUSES}")
    src = e.get("source")
    if src is not None and not isinstance(src, str) and not (
        isinstance(src, list) and all(isinstance(s, str) for s in src)
    ):
        errs.append(f"{key}: source — строка, список строк или null")
    if "note" in e and not isinstance(e["note"], str):
        errs.append(f"{key}: note должно быть строкой")
    fmt = e.get("format")
    if fmt is not None:
        if not isinstance(fmt, dict):
            errs.append(f"{key}: format должен быть словарём")
        else:
            bad = set(fmt) - FORMAT_KEYS
            if bad:
                errs.append(f"{key}: неизвестные поля format {sorted(bad)}")
            d = fmt.get("decimals")
            if d is not None and (not isinstance(d, int) or isinstance(d, bool) or d < 0):
                errs.append(f"{key}: format.decimals — целое ≥ 0")
            for b in ("approx", "unit_space"):
                if b in fmt and not isinstance(fmt[b], bool):
                    errs.append(f"{key}: format.{b} — true/false")
    if derived:
        if not isinstance(e.get("formula"), str):
            errs.append(f"{key}: нет формулы")
        if not isinstance(e.get("inputs"), list):
            errs.append(f"{key}: нет списка inputs")
    return errs


def load_canon(data_dir: Path):
    """→ (canon, derived, errors). canon/derived — упорядоченные dict ключ → запись."""
    data_dir = Path(data_dir)
    errors: list[str] = []
    canon_path = data_dir / "canon.yaml"
    try:
        canon, errs = flatten(load_yaml(canon_path) or {})
        errors += [f"canon.yaml: {m}" for m in errs]
    except (OSError, yaml.YAMLError) as exc:
        return {}, {}, [f"{canon_path}: {exc}"]
    for k, e in canon.items():
        errors += [f"canon.yaml: {m}" for m in validate_entry(k, e)]
    derived: dict = {}
    derived_path = data_dir / "derived.yaml"
    if derived_path.exists():
        try:
            raw = load_yaml(derived_path) or {}
            derived = dict((raw.get("values") or {}).items())
        except (OSError, yaml.YAMLError) as exc:
            errors.append(f"{derived_path}: {exc}")
        for k, e in derived.items():
            errors += [f"derived.yaml: {m}" for m in validate_entry(k, e, derived=True)]
            if k in canon:
                errors.append(f"derived.yaml: {k}: ключ уже есть в canon.yaml")
    return canon, derived, errors


def derived_meta(data_dir: Path) -> dict:
    p = Path(data_dir) / "derived.yaml"
    if not p.exists():
        return {}
    return (load_yaml(p) or {}).get("meta") or {}


# ---------- форматирование ----------

def _group(int_part: str, sep: str) -> str:
    if len(int_part) < 5:  # 4-значные числа не разбиваем: 2050, 9999
        return int_part
    out = []
    while len(int_part) > 3:
        out.insert(0, int_part[-3:])
        int_part = int_part[:-3]
    out.insert(0, int_part)
    return sep.join(out)


def format_number(x, lang: str, decimals: int | None = None) -> str:
    if decimals is None:
        if isinstance(x, int):
            s = str(x)
        else:
            s = repr(float(x))
            if "e" in s or "E" in s:
                s = f"{x:.10f}".rstrip("0").rstrip(".")
    else:
        s = f"{x:.{decimals}f}"
    neg = s.startswith("-")
    if neg:
        s = s[1:]
        if float(s) == 0:
            neg = False
    int_part, _, frac = s.partition(".")
    int_part = _group(int_part, " " if lang == "ru" else ",")
    s = int_part + (("," if lang == "ru" else ".") + frac if frac else "")
    return (MINUS + s) if neg else s


def format_value(entry: dict, lang: str, with_unit: bool = True) -> str:
    """Текст числа для страницы: ru — запятая и русская единица, en — точка и unit_en."""
    fmt = entry.get("format") or {}
    dec = fmt.get("decimals")
    v = entry["value"]
    if isinstance(v, list):
        s = format_number(v[0], lang, dec) + DASH + format_number(v[1], lang, dec)
    else:
        s = format_number(v, lang, dec)
    if fmt.get("approx"):
        s = APPROX + s
    if with_unit:
        unit = entry.get("unit" if lang == "ru" else "unit_en") or ""
        if unit:
            space = fmt.get("unit_space", unit not in NO_SPACE_UNITS)
            s += (" " if space else "") + unit
    return s


def normalize_ws(s: str) -> str:
    for a, b in SPACES.items():
        s = s.replace(a, b)
    return s


def lookup(key: str, canon: dict, derived: dict):
    if key in canon:
        return canon[key]
    return derived.get(key)


def sources_of(entry: dict) -> list[str]:
    src = entry.get("source")
    if src is None:
        return []
    return [src] if isinstance(src, str) else list(src)
