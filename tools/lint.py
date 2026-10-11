"""Линтер вики: ссылки, шапки, имена файлов, оглавления, сироты. Только читает файлы.

Ошибки (код выхода 1):
  битые относительные ссылки и картинки; [[wikilinks]]; нет/невалидная шапка, нет title/type/status,
  type/status/realism вне списков CLAUDE.md; имя файла или папки не kebab-case;
  страница не упомянута в index.md своей папки; index.md подпапки не упомянут в index.md родителя.
Предупреждения:
  меньше 3 исходящих внутренних ссылок; сирота (нет входящих, кроме как из index.md);
  sources: в шапке указывает на несуществующий файл; якорь #… не найден среди заголовков цели.

Запуск: uv run tools/lint.py [--root ПАПКА] [--quiet]
"""
from __future__ import annotations

import argparse
import os
import re
import signal
import sys
import time
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdscan  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
LANGS = ("ru", "en")
TYPES = {"section", "concept", "system", "zone", "component", "entity", "person", "org", "place", "event",
         "episode", "reference"}
STATUSES = {"draft", "proposed", "canon", "frozen"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MIN_OUT_LINKS = 3


class Page:
    __slots__ = ("path", "rel", "text", "masked", "body_offset", "meta", "fm_error", "links", "anchors")

    def __init__(self, path: Path, root: Path):
        self.path = path
        self.rel = path.relative_to(root).as_posix()
        self.text = path.read_text(encoding="utf-8", errors="replace")
        self.meta, body, self.body_offset, self.fm_error = mdscan.split_front_matter(self.text)
        # маскируем код только в теле; смещения считаем от начала тела
        self.masked = mdscan.code_mask(body)
        self.links = []  # (line, target, is_image)
        for off, target, img in mdscan.iter_links(self.masked):
            self.links.append((self.body_offset + mdscan.line_of(self.masked, off), target, img))
        self.anchors = set()
        for h in mdscan.headings(self.masked):
            self.anchors |= mdscan.anchor_forms(h)


class Report:
    def __init__(self):
        self.items = defaultdict(list)  # rel → [(level, line, msg)]

    def err(self, rel, line, msg):
        self.items[rel].append(("ошибка", line, msg))

    def warn(self, rel, line, msg):
        self.items[rel].append(("предупр.", line, msg))

    def count(self, level):
        return sum(1 for v in self.items.values() for x in v if x[0] == level)

    def files_with(self, level):
        return sum(1 for v in self.items.values() if any(x[0] == level for x in v))


def collect(root: Path) -> list[Path]:
    out = []
    for lang in LANGS:
        base = root / lang
        if base.is_dir():
            for p in base.rglob("*.md"):
                if not any(part.startswith(".") for part in p.relative_to(root).parts):
                    out.append(p)
    return sorted(out)


def resolve(page_path: Path, target: str):
    """→ (Path|None, anchor|None, kind). kind: external | anchor | abs | file."""
    if mdscan.is_external(target):
        return None, None, "external"
    path_part, _, anchor = target.partition("#")
    anchor = anchor or None
    if not path_part:
        return page_path, anchor, "anchor"
    path_part = unquote(path_part)
    if path_part.startswith("/"):
        return None, anchor, "abs"
    return Path(os.path.normpath(page_path.parent / path_part)), anchor, "file"


def lint(root: Path) -> tuple[Report, int]:
    rep = Report()
    paths = collect(root)
    pages = {p: Page(p, root) for p in paths}
    incoming = defaultdict(set)   # цель → множество страниц-источников (не index.md)
    index_links = defaultdict(set)  # index.md → множество целей
    out_links = defaultdict(set)
    heading_cache: dict[Path, set] = {}
    bad_dirs = set()

    def anchors_of(p: Path):
        if p in pages:
            return pages[p].anchors
        if p not in heading_cache:
            try:
                heading_cache[p] = set().union(*[mdscan.anchor_forms(h) for h in
                                                 mdscan.headings(mdscan.code_mask(p.read_text(encoding="utf-8")))])
            except OSError:
                heading_cache[p] = set()
        return heading_cache[p]

    for path, pg in pages.items():
        rel = pg.rel
        rel_parts = path.relative_to(root).parts  # ("ru", "30-ship", "x.md")

        # --- имена ---
        if path.name != "index.md" and not NAME_RE.match(path.stem):
            rep.err(rel, None, f"имя файла «{path.name}» не по шаблону ^[a-z0-9]+(-[a-z0-9]+)*\\.md$")
        for i in range(1, len(rel_parts) - 1):
            d = "/".join(rel_parts[: i + 1])
            if not NAME_RE.match(rel_parts[i]) and d not in bad_dirs:
                bad_dirs.add(d)
                rep.err(rel, None, f"имя папки «{d}» не по шаблону ^[a-z0-9]+(-[a-z0-9]+)*$")

        # --- шапка ---
        if pg.fm_error:
            rep.err(rel, 1, pg.fm_error)
        elif pg.meta is None:
            rep.err(rel, 1, "нет шапки YAML (--- … ---)")
        else:
            m = pg.meta
            for f in ("title", "type", "status"):
                if m.get(f) in (None, ""):
                    rep.err(rel, 1, f"в шапке нет {f}")
            if m.get("type") not in (None, "") and m.get("type") not in TYPES:
                rep.err(rel, 1, f"type «{m.get('type')}» не из списка CLAUDE.md")
            if m.get("status") not in (None, "") and m.get("status") not in STATUSES:
                rep.err(rel, 1, f"status «{m.get('status')}» не из списка CLAUDE.md")
            if "realism" in m and (not isinstance(m["realism"], int) or isinstance(m["realism"], bool)
                                   or not 1 <= m["realism"] <= 5):
                rep.err(rel, 1, f"realism «{m['realism']}» — целое 1–5")
            srcs = m.get("sources") or []
            if isinstance(srcs, str):
                srcs = [srcs]
            if not isinstance(srcs, list):
                rep.warn(rel, 1, "sources в шапке — не список")
                srcs = []
            for s in srcs:
                if not isinstance(s, str):
                    rep.warn(rel, 1, f"sources: элемент «{s}» не строка")
                    continue
                if mdscan.is_external(s):
                    continue
                sp = s.split(" §", 1)[0].strip()
                if not (root / sp).exists():
                    head = re.match(r"\S+\.md\b", sp)
                    if head and (root / head.group(0)).exists():
                        rep.warn(rel, 1, f"sources: «{s}» — раздел указывайте через « §» (формат CLAUDE.md)")
                    else:
                        rep.warn(rel, 1, f"sources: нет файла «{sp}»")

        # --- wikilinks ---
        for mm in mdscan.WIKILINK_RE.finditer(pg.masked):
            rep.err(rel, pg.body_offset + mdscan.line_of(pg.masked, mm.start()),
                    f"wikilink {mm.group(0)} — нужна относительная markdown-ссылка")

        # --- ссылки ---
        is_index = path.name == "index.md"
        for line, target, img in pg.links:
            tpath, anchor, kind = resolve(path, target)
            what = "картинка" if img else "ссылка"
            if kind == "external":
                continue
            if kind == "abs":
                rep.err(rel, line, f"{what} с абсолютным путём «{target}» — нужен относительный")
                continue
            if kind == "file" and not tpath.exists():
                rep.err(rel, line, f"битая {what} «{target}»")
                continue
            if kind == "file" and tpath.is_dir():
                rep.err(rel, line, f"{what} на папку «{target}» — ссылайтесь на index.md")
                continue
            if anchor and tpath.suffix == ".md" and not anchor.startswith("^"):
                if not (mdscan.anchor_forms(anchor) & anchors_of(tpath)):
                    rep.warn(rel, line, f"якорь «#{unquote(anchor)}» не найден в {tpath.name}")
            if img or kind == "anchor":
                continue
            if tpath != path:
                out_links[path].add(tpath)
                if is_index:
                    index_links[path].add(tpath)
                else:
                    incoming[tpath].add(path)

    # --- оглавления, сироты, число ссылок ---
    for path, pg in pages.items():
        rel = pg.rel
        is_index = path.name == "index.md"
        lang_root = root / path.relative_to(root).parts[0]
        if is_index:
            if path.parent != lang_root:
                parent_index = path.parent.parent / "index.md"
                if not parent_index.exists():
                    rep.err(rel, None, f"нет {parent_index.relative_to(root).as_posix()} родительской папки")
                elif path not in index_links[parent_index]:
                    rep.err(rel, None, f"не упомянут в {parent_index.relative_to(root).as_posix()}")
        else:
            idx = path.parent / "index.md"
            if not idx.exists():
                rep.err(rel, None, f"в папке нет index.md ({idx.relative_to(root).as_posix()})")
            elif path not in index_links[idx]:
                rep.err(rel, None, f"не упомянута в оглавлении {idx.relative_to(root).as_posix()}")
            if not incoming[path]:
                rep.warn(rel, None, "сирота: нет входящих ссылок, кроме как из index.md")
        n_out = len(out_links[path])
        if n_out < MIN_OUT_LINKS:
            rep.warn(rel, None, f"исходящих внутренних ссылок {n_out} (< {MIN_OUT_LINKS})")
    return rep, len(pages)


def main():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=REPO_ROOT, help="корень вики (где ru/ и en/)")
    ap.add_argument("--quiet", action="store_true", help="только итоговые счётчики")
    args = ap.parse_args()
    t0 = time.perf_counter()
    rep, n = lint(args.root.resolve())
    if not args.quiet:
        for rel in sorted(rep.items):
            print(rel, flush=True)
            items = sorted(rep.items[rel], key=lambda x: (x[0] != "ошибка", x[1] or 0))
            for level, line, msg in items:
                where = f"{line}" if line else "—"
                print(f"  {level:<9}{where:>5}: {msg}", flush=True)
        if rep.items:
            print(flush=True)
    e, w = rep.count("ошибка"), rep.count("предупр.")
    dt = time.perf_counter() - t0
    print(f"lint: страниц {n}; ошибок {e} в {rep.files_with('ошибка')} файлах; "
          f"предупреждений {w} в {rep.files_with('предупр.')} файлах; {dt:.2f} с", flush=True)
    raise SystemExit(1 if e else 0)


if __name__ == "__main__":
    main()
