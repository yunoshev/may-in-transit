"""Сводка открытых вопросов: собирает таблицы в ru/00-open-questions/index.md из шапок страниц q-NNN-*.md.

Таблицы стоят между <!-- questions:begin --> и <!-- questions:end -->; руками их не правят.
Группы: главное сейчас (priority 1), ответ вписан (поле «Ответ» заполнено, вопрос ещё open),
ждут вашего ответа, ждут расчёта, противоречия (открытые C-NNN из contradictions.md), отвечено и снято.

Запуск:
  uv run tools/questions.py           пересобрать сводку
  uv run tools/questions.py --check   ничего не писать; код 1, если сводка устарела или шапка вопроса неверна
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mdscan  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
QDIR = ROOT / "ru" / "00-open-questions"
INDEX = QDIR / "index.md"
CONTRA = ROOT / "ru" / "90-reference" / "contradictions.md"
BEGIN, END = "<!-- questions:begin -->", "<!-- questions:end -->"

STATES = {"open", "answered", "superseded"}
ANSWERERS = {"user", "calc"}
SECTIONS = {
    "10-world": ("Мир", "../10-world/index.md"),
    "20-mission": ("Миссия", "../20-mission/index.md"),
    "30-ship": ("Корабль", "../30-ship/index.md"),
    "40-characters": ("Персонажи", "../40-characters/index.md"),
    "50-science": ("Наука", "../50-science/index.md"),
    "60-realism": ("Реализм", "../60-realism/index.md"),
    "70-series": ("Сериал", "../70-series/index.md"),
    "90-reference": ("Справочник", "../90-reference/index.md"),
}
# заглушки поля «Ответ»: если текст начинается иначе, ответ вписан руками
PLACEHOLDERS = ("Ждёт вашего ответа", "Нужен расчёт")


def section_text(body: str, heading: str) -> str:
    m = re.search(rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", body, re.S | re.M)
    return m.group(1).strip() if m else ""


def first_para(text: str) -> str:
    return " ".join(text.split("\n\n", 1)[0].split())


def load():
    qs, errors = [], []
    for p in sorted(QDIR.glob("q-*.md")):
        meta, body, _, err = mdscan.split_front_matter(p.read_text(encoding="utf-8"))
        rel = p.relative_to(ROOT).as_posix()
        if err or not meta:
            errors.append(f"{rel}: {err or 'нет шапки'}")
            continue
        m = re.match(r"q-(\d{3})-", p.name)
        title = str(meta.get("title", ""))
        q = {
            "n": int(m.group(1)) if m else 0,
            "file": p.name,
            "title": re.sub(r"^Q-\d{3}\s*—\s*", "", title),
            "state": meta.get("question"),
            "answerer": meta.get("answerer"),
            "priority": meta.get("priority"),
            "section": meta.get("section"),
            "decision": meta.get("decision") or [],
            "rec": first_para(section_text(body, "Рекомендация")),
            "answer": section_text(body, "Ответ"),
        }
        if isinstance(q["decision"], str):
            q["decision"] = [q["decision"]]
        if not m:
            errors.append(f"{rel}: имя не по шаблону q-NNN-….md")
        if not title.startswith(f"Q-{q['n']:03d}"):
            errors.append(f"{rel}: title должен начинаться с «Q-{q['n']:03d} —»")
        if q["state"] not in STATES:
            errors.append(f"{rel}: question «{q['state']}» — нужно {' | '.join(sorted(STATES))}")
        if q["answerer"] not in ANSWERERS:
            errors.append(f"{rel}: answerer «{q['answerer']}» — нужно {' | '.join(sorted(ANSWERERS))}")
        if q["priority"] not in (1, 2, 3):
            errors.append(f"{rel}: priority «{q['priority']}» — нужно 1, 2 или 3")
        if q["section"] not in SECTIONS:
            errors.append(f"{rel}: section «{q['section']}» — нужно одно из {', '.join(SECTIONS)}")
        if q["state"] == "answered" and not q["decision"]:
            errors.append(f"{rel}: отвеченный вопрос без decision: [D-NNN]")
        qs.append(q)
    seen = {}
    for q in qs:
        if q["n"] in seen:
            errors.append(f"номер Q-{q['n']:03d} занят дважды: {seen[q['n']]} и {q['file']}")
        seen[q["n"]] = q["file"]
    return qs, errors


def open_contradictions():
    text = CONTRA.read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r"^### (C-\d{3}) — (.+)\n\*\*Статус:\*\*\s*(.+)$", text, re.M):
        if m.group(3).strip().startswith("открыто"):
            out.append((m.group(1), m.group(2).strip()))
    return out


def cell(s: str) -> str:
    return s.replace("|", "\\|")


def qlink(q) -> str:
    return f"[Q-{q['n']:03d}]({q['file']})"


def sec(q) -> str:
    name, link = SECTIONS.get(q["section"], (str(q["section"]), None))
    return f"[{name}]({link})" if link else name


def written(q) -> bool:
    return q["state"] == "open" and bool(q["answer"]) and not q["answer"].startswith(PLACEHOLDERS)


def table_rec(rows):
    out = ["| | Вопрос | Раздел | Рекомендация |", "|---|---|---|---|"]
    out += [f"| {qlink(q)} | {cell(q['title'])} | {sec(q)} | {cell(q['rec'])} |" for q in rows]
    return out


def render(qs):
    key = lambda q: (q["priority"] or 9, q["n"])  # noqa: E731
    opened = [q for q in qs if q["state"] == "open"]
    wr = sorted([q for q in opened if written(q)], key=lambda q: q["n"])
    rest = [q for q in opened if not written(q)]
    top = sorted([q for q in rest if q["answerer"] == "user" and q["priority"] == 1], key=key)
    user = sorted([q for q in rest if q["answerer"] == "user" and q["priority"] != 1], key=key)
    calc = sorted([q for q in rest if q["answerer"] == "calc"], key=key)
    done = sorted([q for q in qs if q["state"] != "open"], key=lambda q: q["n"])
    contra = open_contradictions()

    out = [f"Открыто вопросов: **{len(opened)}** — ждут вашего ответа {len(top) + len(user)}, "
           f"ждут расчёта {len(calc)}" + (f", ответ вписан {len(wr)}" if wr else "")
           + f". Противоречий в исходниках: {len(contra)}. Отвечено и снято: {len(done)}.", ""]
    if wr:
        out += ["### Ответ вписан — ждёт оформления", "",
                "Ответ стоит на странице вопроса; главред оформит его решением и закроет вопрос.", ""]
        out += ["| | Вопрос | Раздел | Вписанный ответ |", "|---|---|---|---|"]
        out += [f"| {qlink(q)} | {cell(q['title'])} | {sec(q)} | {cell(first_para(q['answer']))} |" for q in wr]
        out.append("")
    out += ["### Главное сейчас", "", "От этих ответов зависят другие вопросы и пересборка сезона.", ""]
    out += table_rec(top) if top else ["Нет."]
    out += ["", "### Ждут вашего ответа", "", "Сначала приоритет 2 (нужен до заморозки раздела), потом 3 (можно позже).", ""]
    out += table_rec(user) if user else ["Нет."]
    out += ["", "### Ждут расчёта", "", "Ответ даст расчёт в `calc/` или проверка по источникам; ваше слово нужно, "
            "только если расчёт упрётся в выбор.", ""]
    out += table_rec(calc) if calc else ["Нет."]
    out += ["", "### Противоречия в исходниках", "",
            "Исходники расходятся между собой; разбор и рекомендации — в [противоречиях](../90-reference/contradictions.md).", ""]
    if contra:
        out += ["| | Тема |", "|---|---|"]
        out += [f"| [{c}](../90-reference/contradictions.md) | {cell(t)} |" for c, t in contra]
    else:
        out.append("Нет.")
    out += ["", "### Отвечено и снято", ""]
    if done:
        out += ["| | Вопрос | Итог |", "|---|---|---|"]
        for q in done:
            if q["state"] == "answered":
                res = "решение " + ", ".join(f"[{d}](../90-reference/decisions.md)" for d in q["decision"])
            else:
                res = "снят"
            out.append(f"| {qlink(q)} | {cell(q['title'])} | {res} |")
    else:
        out.append("Нет.")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="ничего не писать; код 1, если сводка устарела")
    args = ap.parse_args()
    qs, errors = load()
    for e in errors:
        print(f"ошибка: {e}", flush=True)
    text = INDEX.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        print(f"ошибка: в {INDEX.relative_to(ROOT)} нет маркеров {BEGIN} … {END}", flush=True)
        raise SystemExit(1)
    head, rest = text.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    new = f"{head}{BEGIN}\n{render(qs)}\n{END}{tail}"
    if args.check:
        if new != text:
            print("сводка вопросов устарела: uv run tools/questions.py", flush=True)
            raise SystemExit(1)
        print(f"сводка вопросов актуальна ({len(qs)} вопросов)", flush=True)
    elif new != text:
        INDEX.write_text(new, encoding="utf-8")
        print(f"сводка вопросов обновлена ({len(qs)} вопросов)", flush=True)
    else:
        print(f"сводка вопросов не изменилась ({len(qs)} вопросов)", flush=True)
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
