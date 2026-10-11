"""Разбор markdown для инструментов вики: шапка, маскирование кода, ссылки, заголовки.

Только чтение. Используют tools/lint.py и tools/canon_sync.py.
"""
from __future__ import annotations

import re
from urllib.parse import unquote

import yaml

try:
    _Loader = yaml.CSafeLoader
except AttributeError:  # pragma: no cover
    _Loader = yaml.SafeLoader

FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"(`+)(?:(?!\1).)+?\1", re.S)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)

# [текст](цель "заголовок") и ![alt](цель); цель — <...> или без пробелов, допускает одну пару скобок.
INLINE_LINK_RE = re.compile(
    r"(?P<img>!?)\[(?P<text>(?:[^\[\]\n]|\[[^\[\]\n]*\])*)\]"
    r"\(\s*(?P<target><[^>\n]*>|(?:[^()\s]|\([^()\s]*\))+)"
    r"(?:\s+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^()\n]*\)))?\s*\)"
)
REF_DEF_RE = re.compile(r"^ {0,3}\[(?P<label>[^\]\n]+)\]:\s*(?P<target><[^>\n]*>|\S+)", re.M)
HTML_ATTR_RE = re.compile(r"<(?P<tag>img|a)\b[^>]*?\b(?:src|href)\s*=\s*(?P<q>[\"'])(?P<target>.*?)(?P=q)", re.I)
WIKILINK_RE = re.compile(r"!?\[\[[^\[\]\n]+\]\]")
HEADING_RE = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.*?)(?:[ \t]+#+)?[ \t]*$")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def split_front_matter(text: str):
    """→ (meta|None, body, body_line_offset, error|None).

    meta None и error None — шапки нет. body_line_offset — номер строки (с 0), с которой начинается тело.
    """
    if not (text.startswith("---\n") or text.startswith("---\r\n")):
        return None, text, 0, None
    lines = text.splitlines(keepends=True)
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r\n") in ("---", "..."):
            raw = "".join(lines[1:i])
            body = "".join(lines[i + 1:])
            try:
                meta = yaml.load(raw, Loader=_Loader)
            except yaml.YAMLError as exc:
                mark = getattr(exc, "problem_mark", None)
                where = f" (строка {mark.line + 2})" if mark else ""
                return None, body, i + 1, f"невалидный YAML в шапке{where}: {getattr(exc, 'problem', exc)}"
            if meta is None:
                meta = {}
            if not isinstance(meta, dict):
                return None, body, i + 1, "шапка не является словарём YAML"
            return meta, body, i + 1, None
    return None, text, 0, "шапка не закрыта строкой ---"


def code_mask(text: str) -> str:
    """Копия text, где содержимое кода (ограждённые блоки, `инлайн`, <!-- комментарии -->)
    заменено пробелами; длина и переводы строк сохранены — смещения совпадают с оригиналом."""
    chars = list(text)

    def blank(a, b):
        for i in range(a, b):
            if chars[i] not in "\r\n":
                chars[i] = " "

    pos = 0
    fence = None
    fence_start = 0
    prose_start = 0
    prose_spans = []
    for line in text.splitlines(keepends=True):
        stripped = line.rstrip("\r\n")
        m = FENCE_RE.match(stripped)
        if fence is None:
            if m:
                prose_spans.append((prose_start, pos))
                fence = m.group(1)
                fence_start = pos
        else:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not stripped.strip()[len(m.group(1)):].strip():
                blank(fence_start, pos + len(line))
                fence = None
                prose_start = pos + len(line)
        pos += len(line)
    if fence is not None:  # незакрытый блок — до конца файла
        blank(fence_start, len(text))
    else:
        prose_spans.append((prose_start, len(text)))
    for a, b in prose_spans:
        seg = text[a:b]
        for rx in (HTML_COMMENT_RE, INLINE_CODE_RE):
            for m in rx.finditer(seg):
                blank(a + m.start(), a + m.end())
    return "".join(chars)


def line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def iter_links(masked: str):
    """→ (offset, target, is_image). Цель без <> и без заголовка; не декодирована."""
    for m in INLINE_LINK_RE.finditer(masked):
        t = m.group("target")
        if t.startswith("<") and t.endswith(">"):
            t = t[1:-1]
        yield m.start(), t, bool(m.group("img"))
    for m in REF_DEF_RE.finditer(masked):
        t = m.group("target")
        if t.startswith("<") and t.endswith(">"):
            t = t[1:-1]
        yield m.start(), t, False
    for m in HTML_ATTR_RE.finditer(masked):
        yield m.start(), m.group("target"), m.group("tag").lower() == "img"


def is_external(target: str) -> bool:
    return bool(SCHEME_RE.match(target)) or target.startswith("//")


def headings(masked: str) -> list[str]:
    out = []
    for line in masked.splitlines():
        m = HEADING_RE.match(line)
        if m:
            out.append(m.group(2).strip())
    return out


_STRIP_RE = re.compile(r"[#|^:\[\]]")


def anchor_forms(s: str) -> set[str]:
    """Нормальные формы якоря/заголовка: как в Obsidian (текст, пробелы как есть) и slug с дефисами."""
    s = unquote(s).strip()
    plain = re.sub(r"\s+", " ", _STRIP_RE.sub("", s)).strip().lower()
    slug = re.sub(r"[^\w\- ]", "", s.lower(), flags=re.U).strip().replace(" ", "-")
    return {plain, slug}
