---
title: Библиотека промптов для диаграмм
aliases: [diagram prompts, anatomy prompts, prompt library, промпты для диаграмм]
type: reference
status: draft
sources:
  - sources/anatomy_prompts.md
  - sources/00_project_wiki_index.md (Initial diagram roadmap)
tags: [reference/figures, reference/prompts]
---

# Библиотека промптов для диаграмм

Кратко: перенесённая без изменений библиотека промптов из `sources/anatomy_prompts.md`: общий стиль, 20 промптов, промпт ревью и промпт заморозки. Тексты промптов остаются английскими дословно, они рассчитаны на генераторы изображений. Заголовки и пояснения по-русски: рекомендуемый инструмент, причина выбора и страница, где появится картинка. План всех рисунков с ID — [план чертежей](figures-roadmap.md).

## Как пользоваться
- Диаграммы остаются проектными предложениями, пока не проверены. Предпочитаем инженерную ясность, а не киношный стиль; никаких декоративных элементов без функции.
- Промпты работают вместе с каноном вики и спецификацией корабля. Числа в промптах (около 28 м, около 4 об/мин, 0,5 g) приведены как в исходниках; расхождение радиуса с концепцией записано в [C-001](contradictions.md), каноническое значение берётся из `data/canon.yaml`.
- Навык anatomy собирает рисунки кодом (`figures/<name>/build.mjs`), а не по прозаическому промпту, и подписей на рисунке не даёт; поэтому промпт для anatomy служит техническим заданием: перечень узлов и видов, а подписи и номера уходят в легенду на странице.
- Для ИИ-генераторов из промпта убираем требования подписей, размерных выносок и надписей на изображении: ИИ плохо рисует текст, а решение [D-006](decisions.md) требует картинки без текста. Расхождение описано в [C-010](contradictions.md).
- Каждую картинку проверяют глазами на соответствие канону перед вставкой.

## Общий стиль

Добавляется к любому промпту ниже. Для anatomy и кода применяются только пункты про ясность, сдержанные цвета и отсутствие фантазийных элементов; про подписи и выноски см. выше.

```text
Clean aerospace engineering visualization, technically plausible 2050s spacecraft, isometric or orthographic presentation, restrained colors, neutral background, clear labels, dimensional callouts, visible mechanical interfaces, no fantasy ornament, no unexplained glowing components, no weapons, no cinematic lens effects.
```

## Промпты по рисункам

### Prompt 01 — Полный вид корабля (Full spacecraft overview)

- **Рисунок:** F-01 в [плане графики](figures-roadmap.md)
- **Инструмент:** anatomy + код. Anatomy строит изометрию корабля без подписей; векторы вращения и тяги, размеры и числа добавляет код из `canon.yaml`; легенда с номерами идёт в текст страницы.
- **Страница:** [Внешний облик](../30-ship/exterior/index.md)

```text
Create an isometric technical overview of a fictional one-person 2050s Jupiter spacecraft named the Maya / ARI vehicle.

Show:
- long central spacecraft spine;
- main propulsion mounted on spin axis;
- power / reactor section far from crew habitat;
- large deployable radiators;
- forward communications and navigation hardware;
- one radial habitat pod;
- one opposing service / counterweight pod;
- approximately 28 m radius from spin axis to habitat floor;
- approximately 4 rpm nominal rotation;
- approximately 0.5 g at habitat floor;
- axial thrust direction;
- rotation direction;
- forward and aft orientation.

Label all major systems and show artificial-gravity vectors.
```

### Prompt 02 — Разнесённый вид снаружи (Exterior exploded view)

- **Рисунок:** F-02 в [плане графики](figures-roadmap.md)
- **Инструмент:** anatomy. Разнесённый вид — основная специализация anatomy; узлы нумеруются в легенде, интерфейсы служат референсом для Blender.
- **Страница:** [Внешний облик](../30-ship/exterior/index.md)

```text
Create an exploded technical diagram separating:
1. habitat pressure vessel;
2. protective shell;
3. rotating boom / radial structure;
4. service / counterweight pod;
5. central structural spine;
6. power-conditioning hardware;
7. reactor / primary power source;
8. radiator assemblies;
9. main propulsion section;
10. communications antenna;
11. external cameras;
12. propellant / consumable tanks.

Make interfaces useful as Blender modelling reference.
```

### Prompt 03 — Внешняя оболочка жилого модуля (Habitat exterior shell)

- **Рисунок:** F-03 в [плане графики](figures-roadmap.md)
- **Инструмент:** код + anatomy. Ортографические виды с размерами строит код из `canon.yaml`; изометрию даёт anatomy.
- **Страница:** [Жилой модуль снаружи](../30-ship/exterior/habitat-pod-exterior.md)

```text
Create isometric and orthographic reference views for the habitat pod.

Canonical targets:
- ~2.8 m internal diameter;
- ~6.0 m internal length;
- one-person occupancy;
- axial observation window;
- service hatch;
- radial-structure attachment;
- external cameras;
- thermal-control connections.

Include front, side, top, isometric views and major dimensions.
```

### Prompt 04 — Разрез жилого модуля (Habitat cutaway)

- **Рисунок:** F-04 в [плане графики](figures-roadmap.md)
- **Инструмент:** anatomy. Изометрический разрез интерьера без подписей; зоны нумеруются в легенде.
- **Страница:** [Планировка](../30-ship/habitat/interior-layout.md)

```text
Create an isometric cutaway showing:
- main work / command station;
- chair;
- primary and secondary displays;
- forward axial window;
- compact galley;
- hygiene / toilet compartment;
- stasis / sleep / medical / radiation-shelter compartment;
- ECLSS service wall;
- water and consumable storage;
- medical locker;
- fold-away exercise system;
- clothing / personal storage;
- technical tool drawers;
- camera A / B / C.
```

### Prompt 05 — Искусственная гравитация (Artificial gravity)

- **Рисунок:** F-05 в [плане графики](figures-roadmap.md)
- **Инструмент:** код. Диаграмма с векторами, радиусом и оборотами; числа должны браться из `canon.yaml` и расчёта, а не вписываться руками.
- **Страница:** [Искусственная гравитация](../30-ship/artificial-gravity.md)

```text
Create an engineering diagram showing:
- spacecraft spin axis;
- habitat at ~28 m radius;
- opposite counterweight pod;
- ~4 rpm rotation;
- 0.5 g at habitat floor;
- floor acceleration vector;
- main axial thrust direction;
- axial observation-window direction.

Add a local habitat inset with Maya standing and slightly lower effective gravity at head height.
```

### Prompt 06 — Раскладка камер (Camera layout)

- **Рисунок:** F-06 в [плане графики](figures-roadmap.md)
- **Инструмент:** код. Вид сверху и изометрия с конусами обзора и безопасными зонами 9:16; геометрия по координатам камер.
- **Страница:** [Камеры](../70-series/cameras.md)

```text
Create top-down and isometric camera-layout diagrams for vertical 9:16 production.

Camera A:
- main vlog camera;
- medium shot;
- Maya + workstation + window.

Camera B:
- upper-corner wide;
- workstation + galley + service area.

Camera C:
- closer workstation camera;
- intimate vlog / ARI dialogue.

Show viewing cones and safe areas for subtitles and ARI graphics.
```

### Prompt 07 — ECLSS / жизнеобеспечение (ECLSS / life support)

- **Рисунок:** F-07 в [плане графики](figures-roadmap.md)
- **Инструмент:** код. Функциональная схема потоков воздуха, кислорода, воды и отходов; удобно писать на Mermaid или SVG.
- **Страница:** [Жизнеобеспечение](../30-ship/systems/life-support.md)

```text
Create a functional schematic with:

AIR:
cabin → particulate filtration → CO2 removal → trace contaminant control → humidity control → cabin.

OXYGEN:
water / O2 generation → cabin control → emergency O2 reserve.

WATER:
humidity condensate + greywater + urine processing → purification → potable storage → galley / hygiene / life support.

WASTE:
toilet / biological waste → processing / sealed storage.

MONITORING:
pressure, O2, CO2, humidity, temperature, smoke.

Show serviceable filters accessible from the habitat.
```

### Prompt 08 — Вода и радиационная защита (Water and radiation shielding)

- **Рисунок:** F-08 в [плане графики](figures-roadmap.md)
- **Инструмент:** anatomy. Сечение жилого модуля с окружением койки стазиса; слои нумеруются в легенде.
- **Страница:** [Радиационная защита](../30-ship/systems/radiation-protection.md)

```text
Create a habitat cross-section showing:
- stasis berth;
- surrounding water tanks;
- food / consumables;
- hygiene supplies;
- polyethylene-rich material;
- outer pressure shell;
- protective outer shell.

Show how existing mission mass contributes to shielding.
```

### Prompt 09 — Камбуз (Galley)

- **Рисунок:** F-09 в [плане графики](figures-roadmap.md)
- **Инструмент:** anatomy. Детальный вид компактного оборудования без подписей; легенда в тексте.
- **Страница:** [Камбуз](../30-ship/habitat/galley.md)

```text
Create a compact galley detail showing:
- potable-water dispenser;
- hot-water outlet;
- food warmer;
- refrigeration drawer;
- packaged-food storage;
- utensil drawer;
- mug retention slot;
- small work surface;
- waste drawer;
- cleaning supplies.

The habitat operates at 0.5 g.
```

### Prompt 10 — Санузел (Hygiene compartment)

- **Рисунок:** F-10 в [плане графики](figures-roadmap.md)
- **Инструмент:** anatomy. Компактный модуль в разрезе и изометрии; легенда в тексте.
- **Страница:** [Санузел](../30-ship/habitat/hygiene.md)

```text
Create a compact one-person hygiene module showing:
- toilet;
- airflow / vacuum-assisted waste interface;
- handwash basin;
- retractable hygiene spray;
- mirror;
- personal-care storage;
- ventilation;
- towel storage;
- waste-service access.
```

### Prompt 11 — Стазис, медицина, укрытие (Stasis / medical / shelter)

- **Рисунок:** F-11 в [плане графики](figures-roadmap.md)
- **Инструмент:** anatomy. Технический вид койки и окружения; промпт прямо запрещает фэнтезийную криоэстетику, anatomy даёт строгую геометрию.
- **Страница:** [Отсек стазиса, сна и укрытия](../30-ship/habitat/stasis-shelter.md)

```text
Create a technical diagram showing:
- fixed stasis berth;
- padded medical surface;
- partially transparent cover;
- physiological monitoring;
- fluid / IV interfaces;
- ventilation;
- emergency mechanical release;
- ARI camera / microphone;
- medical storage;
- surrounding water / consumable shielding.

Avoid fantasy cryogenic aesthetics.
```

### Prompt 12 — Архитектура ARI (ARI architecture)

- **Рисунок:** F-12 в [плане графики](figures-roadmap.md)
- **Инструмент:** код. Системная схема со связями и разделением уровней автономии; Mermaid или SVG.
- **Страница:** [ARI в корабле](../30-ship/systems/ari-interfaces.md)

```text
Create a system diagram showing ARI connected to:
- microphones;
- speakers;
- displays;
- internal cameras;
- exterior cameras;
- navigation;
- propulsion control;
- life-support monitoring;
- communications;
- science instruments;
- maintenance diagnostics;
- stasis / medical monitoring.

Separate advisory functions, routine autonomy, safety-critical control, and manual human override.
```

### Prompt 13 — Рабочее место и геройская стена (Workstation / hero wall)

- **Рисунок:** F-13 в [плане графики](figures-roadmap.md)
- **Инструмент:** код + anatomy. Раскладка и размеры дисплеев и статусной строки — код; вид стены — anatomy.
- **Страница:** [Геройская стена](../30-ship/habitat/hero-wall.md)

```text
Create a detailed reference for:
- primary 32–40 inch display;
- secondary 20–27 inch display;
- persistent status strip;
- guarded emergency controls;
- ARI mic / speaker;
- personal shelf;
- structural ribs;
- storage panels;
- nearby window.

Status strip should include ship time, spin / gravity, cabin pressure, O2, CO2, water, next manoeuvre, communications delay.
```

### Prompt 14 — Двигательная установка и энергетика (Propulsion / power section)

- **Рисунок:** F-14 в [плане графики](figures-roadmap.md)
- **Инструмент:** anatomy + код. Кормовая секция в изометрии — anatomy; трассы тока и тепла, подписи — код.
- **Страница:** [Двигательная установка и баки (и Реактор и энергетика)](../30-ship/exterior/propulsion.md)

```text
Create an aft-section diagram showing:
- central spine;
- reactor / primary power source;
- shielding direction away from habitat;
- power-conditioning hardware;
- large radiators;
- electric-propulsion thrusters;
- propellant tanks;
- high-current power routing;
- thermal routing.

Keep propulsion aligned with spin axis.
```

### Prompt 15 — Противовес / служебный модуль (Counterweight / service pod)

- **Рисунок:** F-15 в [плане графики](figures-roadmap.md)
- **Инструмент:** anatomy. Разрез с возможным содержимым; пометка «вымышленная инженерная реализация» уходит в блок «Вымысел» на странице.
- **Страница:** [Служебный модуль-противовес](../30-ship/exterior/service-pod.md)

```text
Create a cutaway showing possible contents:
- water reserve;
- dry stores;
- replacement parts;
- science payloads;
- power electronics;
- batteries;
- waste storage;
- movable ballast.

Explain balancing role and mark it as fictional engineering implementation.
```

### Prompt 16 — Прибытие к Юпитеру (Jupiter arrival overview)

- **Рисунок:** F-16 в [плане графики](figures-roadmap.md)
- **Инструмент:** код. Орбитальная схема по рассчитанным данным; подпись из промпта остаётся, пока траектория не рассчитана.
- **Страница:** [Тур по системе Юпитера](../20-mission/jovian-tour.md)

```text
Create a simplified orbital diagram showing:
- Jupiter;
- incoming trajectory;
- Jupiter capture;
- large looping Jovian orbits;
- Europa;
- Ganymede;
- Callisto;
- example moon gravity assists.

Label:
CONCEPTUAL JOVIAN TOUR — FINAL TRAJECTORY TBD
```

### Prompt 17 — Объяснение гравитационного манёвра (Gravity assist explainer)

- **Рисунок:** F-17 в [плане графики](figures-roadmap.md)
- **Инструмент:** код. Двухпанельная схема с векторами до и после пролёта.
- **Страница:** [Гравитационный манёвр](../50-science/gravity-assist.md)

```text
Create a two-panel explanation:
- approach to a moving Jovian moon;
- departure with changed Jupiter-relative velocity vector.

Show moon motion, incoming vector, outgoing vector, Jupiter reference frame, and resulting orbit change.
```

### Prompt 18 — Лист референса для Blender (Blender modelling reference sheet)

- **Рисунок:** F-18 в [плане графики](figures-roadmap.md)
- **Инструмент:** код + anatomy. Лист с размерами и ортографическими видами из `canon.yaml` — код; изометрический разрез — anatomy.
- **Страница:** [Соглашения Blender](../70-series/blender-conventions.md)

```text
Create:
- orthographic front;
- orthographic side;
- orthographic top;
- isometric cutaway;
- all major dimensions;
- camera A / B / C;
- Maya at 1.7 m scale;
- hatch clearances;
- chair dimensions;
- desk height;
- window dimensions;
- storage depths;
- equipment-panel depths.

Suitable for direct Blender reference.
```

### Prompt 19 — Вертикальные композиции кадра (Vertical shot composition)

- **Рисунок:** F-19 в [плане графики](figures-roadmap.md)
- **Инструмент:** код. Раскладки 9:16 с безопасными зонами; ИИ плохо держит точную композицию и зоны.
- **Страница:** [Камеры](../70-series/cameras.md)

```text
Create six 9:16 reusable compositions:
1. Maya seated at workstation;
2. Maya leaning against desk;
3. Maya at axial window;
4. Maya making coffee;
5. Maya servicing ECLSS;
6. Maya exercising.

Show subject placement, visible systems, subtitle safe area, ARI graphics safe area, screen visibility, and window visibility.
```

### Prompt 20 — Постер всей системы (Full system wiki poster)

- **Рисунок:** F-20 в [плане графики](figures-roadmap.md)
- **Инструмент:** код. Сборка из готовых рисунков F-01…F-17 с легендой слоёв реальности.
- **Страница:** [Корабль](../30-ship/index.md)

```text
Create one comprehensive technical poster combining:
- exterior isometric;
- habitat cutaway;
- artificial gravity;
- propulsion / power;
- life support;
- ARI;
- mission trajectory.

Include legend:
VERIFIED BASIS
FICTIONAL 2050s ASSUMPTION
PRODUCTION SIMPLIFICATION
```

## Служебные промпты

### Review prompt — ревью чертежа

- **Когда:** фаза D (ревью) процесса проектирования: после каждого нового чертежа; список вопросов совпадает с пунктами ревью INDEX, см. [метод реализма](../60-realism/index.md).
- **Инструмент:** текстовая модель (аудит), не генератор изображений. Результат — краткий список замечаний, без автоматической переделки.
- **Страница:** [Реализм: метод](../60-realism/index.md)

```text
Review this spacecraft diagram as an aerospace systems engineer and a Blender production designer.

Identify:
1. components with no clear function;
2. physically awkward geometry;
3. inaccessible maintenance areas;
4. exterior/interior inconsistencies;
5. unnecessary moving mechanisms;
6. unclear mass distribution;
7. camera / production problems;
8. opportunities to simplify while preserving realism.

Do not redesign automatically. Return a concise issue list first.
```

### Canon-freeze prompt — эталонная версия для заморозки

- **Когда:** фаза E (заморозка канона): после согласования дизайна и записи значений в [чек-лист заморозки](freeze-checklist.md).
- **Инструмент:** код (чертёж-эталон из `canon.yaml`) с подписями; генератор не вводит новых компонентов. Идентификатор ревизии берётся из канона.
- **Страница:** [Чек-лист заморозки](freeze-checklist.md)

```text
Produce a canonical technical reference version of this design.

Do not introduce new components.

Preserve approved geometry and terminology.

Add:
- dimensions;
- component labels;
- orientation;
- interface points;
- camera positions if relevant;
- revision identifier.

Title:
MAYA / ARI — CANONICAL REFERENCE — REV [X]
```

## Связи
- [План чертежей и диаграмм](figures-roadmap.md) — ID рисунков, инструменты, статусы
- [Чек-лист заморозки](freeze-checklist.md) — когда используется промпт Canon-freeze
- [Журнал решений](decisions.md) — D-006 и D-007 об источниках и цели графики
- [Реализм: метод](../60-realism/index.md) — ревью чертежей по слоям реальности
- [Корабль](../30-ship/index.md) — страницы, на которых появятся рисунки

## Основания
> [!production] Решение для производства
> Промпты хранятся в исходном виде, потому что они обращены к внешним генераторам; перевод на русский нарушил бы их работу. Русскими остаются только заголовки и пояснения, чтобы с библиотекой можно было работать в русской вики ([D-001](decisions.md)).

> [!conflict] Противоречие
> Промпты требуют подписей и размерных выносок на рисунке, а решение D-006 запрещает текст на ИИ-картинках и подписи в anatomy: [C-010](contradictions.md).

## Открытые вопросы
- Нужна ли русскоязычная версия промптов для будущих генераторов с русским вводом (сейчас нет).
- Какой генератор используется для ИИ-картинок вручную и через API (пока выбор за пользователем).
