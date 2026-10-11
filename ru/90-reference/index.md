---
title: Справочное
aliases: [reference, 90-reference, справочный раздел, служебные страницы]
type: section
status: draft
sources:
  - sources/00_project_wiki_index.md
tags: [reference]
---

# Справочное

Кратко: служебные страницы вики: глоссарий, журнал решений, противоречия, вопросы, канонические значения, внешние источники, чек-лист заморозки, план графики и библиотека промптов. Здесь не описывается мир, здесь им управляют.

## Оглавление

| Страница | Что внутри |
|---|---|
| [Глоссарий RU↔EN](glossary.md) | 60 терминов в парах русский и английский; словарь для будущего перевода |
| [Журнал решений](decisions.md) | явные решения пользователя D-NNN; верхний приоритет канона |
| [Противоречия](contradictions.md) | расхождения исходников C-NNN со статусом и рекомендацией |
| [Открытые вопросы](open-questions.md) | сквозные вопросы Q-NNN к пользователю и к расчётам |
| [Канонические значения](canon-values.md) | сводка чисел из `data/canon.yaml`; создаётся автоматически скриптами `tools/`, вручную не правится |
| [Внешние источники](sources.md) | все URL из исходников с пояснением, что они подтверждают |
| [Чек-лист заморозки](freeze-checklist.md) | 22 пункта, которые закрывают перед моделированием |
| [План чертежей и диаграмм](figures-roadmap.md) | что рисуем, чем и где; ID рисунков F-NN |
| [Библиотека промптов](diagram-prompts.md) | 20 промптов, общий стиль, служебные промпты на английском |

## Иерархия канона

При расхождении побеждает (сверху вниз):
1. новейшее явное решение пользователя ([журнал решений](decisions.md));
2. спецификация корабля (`sources/maya_ari_ship_3d_build_spec.md`);
3. документация миссии и физики ([миссия](../20-mission/index.md), [наука](../50-science/index.md));
4. концепция сериала (`sources/space_vlog_series_concept_v2.md`);
5. заметки к отдельным эпизодам ([сезон 1](../70-series/season-1.md)).

Исходники в `sources/` не редактируются; расхождения между ними записываются в [противоречия](contradictions.md), а рабочее решение, принятое пользователем, — в журнал решений.

## Идентификаторы
- **D-NNN** — решение ([журнал](decisions.md)), **C-NNN** — противоречие ([список](contradictions.md)), **Q-NNN** — вопрос ([список](open-questions.md)), **F-NN** — рисунок ([план](figures-roadmap.md)).
- Номера не переиспользуются. Ссылка вида C-001 из любой страницы ведёт в соответствующий файл.

## Откуда что взято

Соответствие исходников страницам вики. Помогает проверить, что ничего не потеряно при переносе.

### INDEX (`sources/00_project_wiki_index.md`)

| Раздел исходника | Где в вики |
|---|---|
| Purpose, Design workflow, Production north star | [Конвейер производства](../70-series/production-pipeline.md) |
| Canon hierarchy | выше на этой странице |
| Documentation rules | [Реализм: метод](../60-realism/index.md) |
| Initial diagram roadmap | [План чертежей и диаграмм](figures-roadmap.md) |
| Before Blender — minimum freeze checklist | [Чек-лист заморозки](freeze-checklist.md) |
| Proposed future wiki files | таблица ниже |

### CONCEPT (`sources/space_vlog_series_concept_v2.md`)

| Раздел исходника | Где в вики |
|---|---|
| One-line pitch, Core principle, What we deliberately avoid, Production north star | [Концепция](../70-series/series-concept.md) |
| The format, Episode formula | [Формат](../70-series/format.md) |
| Main camera setups | [Камеры](../70-series/cameras.md) |
| The character, Scientific philosophy | [Майя](../40-characters/maya.md), [Концепция](../70-series/series-concept.md) |
| Subtle 2050s technology, NOT CONFIRMED | [Технологии эпохи](../10-world/technology-2050s.md) |
| The spacecraft, Persistent objects | [Личные вещи и реквизит](../30-ship/habitat/personal-items.md), [Жилой модуль](../30-ship/habitat/index.md) |
| Mission architecture | [Запуск и сборка](../20-mission/launch-and-assembly.md), [Космическая отрасль](../10-world/space-industry.md) |
| The Jupiter arrival | [Прибытие](../20-mission/jupiter-arrival.md), [Тур по системе Юпитера](../20-mission/jovian-tour.md) |
| Important realism rule, Reality policy | [Реализм: метод](../60-realism/index.md) |
| SEASON 1 — EUROPA и 12 эпизодов | [Сезон 1](../70-series/season-1.md) |
| Why this version is easier to produce, Blender physics policy, simulation layers, hierarchy, fidelity levels | [Конвейер производства](../70-series/production-pipeline.md) |
| Long-term structure | [Дальнейшие этапы](../20-mission/future-arcs.md) |
| VERIFIED | [Миссии-прототипы](../50-science/reference-missions.md), [Внешние источники](sources.md) |
| Canonical ship design, Visual consequence of 0.5 g | [Искусственная гравитация](../30-ship/artificial-gravity.md) |

### SPEC (`sources/maya_ari_ship_3d_build_spec.md`)

| Разделы | Где в вики |
|---|---|
| §1, §2, §31, §40 | [Общая архитектура](../30-ship/ship-architecture.md) и страницы [внешнего облика](../30-ship/exterior/index.md) |
| §3 | [Гермокорпус](../30-ship/habitat/pressure-vessel.md) |
| §4, §35 | [Ориентация и оси](../30-ship/orientation-and-axes.md), [Соглашения Blender](../70-series/blender-conventions.md) |
| §5 | [Планировка](../30-ship/habitat/interior-layout.md) |
| §6, §36 | [Рабочее место](../30-ship/habitat/command-station.md), [Дисплеи и органы управления](../30-ship/habitat/displays-and-controls.md), [Экранные шаблоны](../70-series/screen-templates.md) |
| §7 | [ARI в корабле](../30-ship/systems/ari-interfaces.md), [ARI](../40-characters/ari.md) |
| §8 | [Обзорное окно и шторка](../30-ship/habitat/observation-window.md) |
| §9–§25, §27–§28 | страницы [жилого модуля](../30-ship/habitat/index.md) |
| §26 | [Внутренние камеры](../30-ship/habitat/interior-cameras.md), [Камеры](../70-series/cameras.md) |
| §29 | [Геройская стена](../30-ship/habitat/hero-wall.md) |
| §30 | [Согласованность снаружи и внутри](../30-ship/exterior-interior-continuity.md) |
| §32 | [Служебный модуль-противовес](../30-ship/exterior/service-pod.md) |
| §33, §34 | [Минимальный набор ассетов](../70-series/asset-list.md) |
| §37 | [Шесть позиций](../70-series/blocking.md) |
| §38, §39 | [Внешние источники](sources.md), [Реализм: метод](../60-realism/index.md) |
| §41 | [Конвейер производства](../70-series/production-pipeline.md) |

### PROMPTS (`sources/anatomy_prompts.md`)
Целиком — [Библиотека промптов](diagram-prompts.md); распределение по рисункам — [План чертежей и диаграмм](figures-roadmap.md).

### Планировавшиеся файлы INDEX и их место в вики

| Файл из INDEX | Где в вики |
|---|---|
| 01_mission_architecture | [Миссия](../20-mission/index.md) |
| 02_spacecraft_exterior | [Внешний облик](../30-ship/exterior/index.md) |
| 03_habitat_interior | [Жилой модуль](../30-ship/habitat/index.md) |
| 04_artificial_gravity | [Искусственная гравитация](../30-ship/artificial-gravity.md) |
| 05_life_support | [Жизнеобеспечение](../30-ship/systems/life-support.md) |
| 06_ari_system | [ARI в корабле](../30-ship/systems/ari-interfaces.md) |
| 07_visual_language | [Материалы и маркировка](../30-ship/habitat/materials-and-markings.md), [Сериал](../70-series/index.md) |
| 08_asset_register | [Минимальный набор ассетов](../70-series/asset-list.md) |
| 09_science_reference | [Наука](../50-science/index.md) |

## Связи
- [Главная](../index.md) — вход в вики
- [Реализм](../60-realism/index.md) — метод оценки и сводная таблица
- [Корабль](../30-ship/index.md) — основной предмет канона
- [Сериал](../70-series/index.md) — производственные материалы

## Основания
> [!production] Решение для производства
> Раздел служебный: на его страницах решения, противоречия и вопросы получают номера, чтобы на них можно было ссылаться из любой страницы и из перевода.

## Открытые вопросы
- Страница [канонических значений](canon-values.md) создаётся автоматически скриптами `tools/`; до её появления ссылка висит и lint её не проверяет как существующую.
