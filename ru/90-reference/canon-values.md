---
title: Канонические значения
aliases: [canon values, канон-значения, канонические числа]
type: reference
status: draft
sources:
  - sources/maya_ari_ship_3d_build_spec.md
  - sources/space_vlog_series_concept_v2.md
  - sources/anatomy_prompts.md
tags: [reference, canon]
---

# Канонические значения

> Генерируется tools/canon_sync.py — не править руками.
> Входные числа правят в `data/canon.yaml`, производные считает `calc/derive.py` → `data/derived.yaml`;
> затем `uv run tools/canon_sync.py --render`.

Кратко: все числа мира в одном месте. В тексте число привязывается спаном `<span data-canon="habitat.floor_radius">28 м</span>`, а `uv run tools/canon_sync.py --check` сверяет его с этой таблицей.

Входных значений: 106, производных: 25.

## Входные значения

### Миссия

| Ключ | Значение | Единица | Статус | Источник | Примечание |
|---|---|---|---|---|---|
| `mission.crew` | 1 | чел. | draft | [maya_ari_ship_3d_build_spec.md §шапка](../../sources/maya_ari_ship_3d_build_spec.md), [space_vlog_series_concept_v2.md §One-line pitch](../../sources/space_vlog_series_concept_v2.md) | Одноместный корабль, на борту только Майя; ARI — бортовой ИИ без тела. |
| `mission.era` | 2050–2059 | гг. | draft | [maya_ari_ship_3d_build_spec.md §шапка](../../sources/maya_ari_ship_3d_build_spec.md), [space_vlog_series_concept_v2.md §Mission architecture](../../sources/space_vlog_series_concept_v2.md) | «2050-е» без точного года; год старта не задан. |
| `mission.stasis_cruise` | ≈3 | года | draft | [space_vlog_series_concept_v2.md §Core principle](../../sources/space_vlog_series_concept_v2.md) | Реплика Майи «a little over three years, depending on where you count it from» — нижняя граница. Точная длительность перелёта — только по расчёту траектории. |

### Жилой модуль

| Ключ | Значение | Единица | Статус | Источник | Примечание |
|---|---|---|---|---|---|
| `habitat.floor_gravity` | 0,5 | g | draft | [maya_ari_ship_3d_build_spec.md §1.1](../../sources/maya_ari_ship_3d_build_spec.md), [maya_ari_ship_3d_build_spec.md §40](../../sources/maya_ari_ship_3d_build_spec.md), [space_vlog_series_concept_v2.md §Artificial gravity](../../sources/space_vlog_series_concept_v2.md) | Целевая тяжесть на полу жилого модуля; в м/с² — производная habitat.floor_accel. |
| `habitat.floor_radius` | 28 | м | proposed | [maya_ari_ship_3d_build_spec.md §1.1](../../sources/maya_ari_ship_3d_build_spec.md), [maya_ari_ship_3d_build_spec.md §40](../../sources/maya_ari_ship_3d_build_spec.md), [anatomy_prompts.md §Prompt 01](../../sources/anatomy_prompts.md) | Расстояние от оси вращения до пола. Конфликт C-001: CONCEPT даёт пример 25 м (4,23 об/мин) и диапазон 20–30 м; по иерархии канона побеждает SPEC — 28 м. |
| `habitat.floor_radius_concept` | 25 | м | draft | [space_vlog_series_concept_v2.md §Artificial gravity](../../sources/space_vlog_series_concept_v2.md) | Вариант из CONCEPT (пример расчёта); проигрывает SPEC, хранится для сравнения (C-001). |
| `habitat.floor_radius_concept_range` | 20–30 | м | draft | [space_vlog_series_concept_v2.md §Artificial gravity](../../sources/space_vlog_series_concept_v2.md) | «Для наглядного масштаба» по CONCEPT; 28 м из SPEC внутри диапазона. |
| `habitat.inner_diameter` | 2,8 | м | draft | [maya_ari_ship_3d_build_spec.md §3](../../sources/maya_ari_ship_3d_build_spec.md), [anatomy_prompts.md §Prompt 03](../../sources/anatomy_prompts.md) | Внутренний диаметр гермооболочки, «approximate». |
| `habitat.inner_length` | 6,0 | м | draft | [maya_ari_ship_3d_build_spec.md §3](../../sources/maya_ari_ship_3d_build_spec.md), [anatomy_prompts.md §Prompt 03](../../sources/anatomy_prompts.md) | Внутренняя длина гермооболочки; ось модуля параллельна оси вращения (SPEC §4, §8). |
| `habitat.usable_volume` | 24–28 | м³ | draft | [maya_ari_ship_3d_build_spec.md §3](../../sources/maya_ari_ship_3d_build_spec.md), [maya_ari_ship_3d_build_spec.md §40](../../sources/maya_ari_ship_3d_build_spec.md) | Полезный объём для человека после стоек, баков, изоляции и оборудования. |
| `habitat.window_width` | 0,8–1,0 | м | draft | [maya_ari_ship_3d_build_spec.md §8](../../sources/maya_ari_ship_3d_build_spec.md) | Видимый проём осевого окна, ширина. |
| `habitat.window_height` | 0,45–0,65 | м | draft | [maya_ari_ship_3d_build_spec.md §8](../../sources/maya_ari_ship_3d_build_spec.md) | Видимый проём осевого окна, высота. |
| `habitat.display_primary` | 32–40 | ″ | draft | [maya_ari_ship_3d_build_spec.md §6](../../sources/maya_ari_ship_3d_build_spec.md), [anatomy_prompts.md §Prompt 13](../../sources/anatomy_prompts.md) | Основной дисплей, диагональ «inch equivalent». |
| `habitat.display_secondary` | 20–27 | ″ | draft | [maya_ari_ship_3d_build_spec.md §6](../../sources/maya_ari_ship_3d_build_spec.md), [anatomy_prompts.md §Prompt 13](../../sources/anatomy_prompts.md) | Вспомогательный дисплей, диагональ «inch equivalent». |

### Майя

| Ключ | Значение | Единица | Статус | Источник | Примечание |
|---|---|---|---|---|---|
| `maya.height` | 1,7 | м | draft | [anatomy_prompts.md §Prompt 18](../../sources/anatomy_prompts.md) | Эталонный рост для референс-листа Blender; в расчётах — высота головы над полом. |
| `maya.age` | 25–33 | лет | draft | [space_vlog_series_concept_v2.md §The character](../../sources/space_vlog_series_concept_v2.md) | Трактовка «mid-20s to early-30s»; точный возраст не задан. |

### Производство

| Ключ | Значение | Единица | Статус | Источник | Примечание |
|---|---|---|---|---|---|
| `production.blender_unit` | 1 | м | draft | [maya_ari_ship_3d_build_spec.md §35](../../sources/maya_ari_ship_3d_build_spec.md) | 1 единица Blender = 1 м. |
| `production.interior_cameras` | 3 | — | draft | [maya_ari_ship_3d_build_spec.md §26](../../sources/maya_ari_ship_3d_build_spec.md) | Камеры A (влог), B (общий план), C (крупный план у дисплея). |
| `production.exterior_camera_feeds` | 5 | — | draft | [maya_ari_ship_3d_build_spec.md §26](../../sources/maya_ari_ship_3d_build_spec.md) | Навигационная, кормовая, внешняя жилого модуля, инспекционная фермы, научная на Юпитер. |
| `production.blocking_positions` | 6 | — | draft | [maya_ari_ship_3d_build_spec.md §37](../../sources/maya_ari_ship_3d_build_spec.md), [anatomy_prompts.md §Prompt 19](../../sources/anatomy_prompts.md) | Повторяемые позиции героини в кадре. |

### Сериал

| Ключ | Значение | Единица | Статус | Источник | Примечание |
|---|---|---|---|---|---|
| `series.season1_episodes` | 12 | — | draft | [space_vlog_series_concept_v2.md §Season 1 — suggested 12 episodes](../../sources/space_vlog_series_concept_v2.md) | Предложенное число эпизодов сезона 1 (Европа). |
| `series.short_duration` | 30–60 | с | draft | [space_vlog_series_concept_v2.md §Episode formula](../../sources/space_vlog_series_concept_v2.md) | Длительность вертикального ролика 9:16. |
| `series.ep6_title_distance` | 600 | млн км | draft | [space_vlog_series_concept_v2.md §Episode 6](../../sources/space_vlog_series_concept_v2.md) | Из названия эпизода 6 («600 million kilometres from home»). CONCEPT требует пересчитать по траектории; попадает в диапазон Земля–Юпитер astro.earth_jupiter_distance. |

### Физические константы и параметры

| Ключ | Значение | Единица | Статус | Источник | Примечание |
|---|---|---|---|---|---|
| `physics.g_earth` | 9,81 | м/с² | draft | [maya_ari_ship_3d_build_spec.md §4](../../sources/maya_ari_ship_3d_build_spec.md), [space_vlog_series_concept_v2.md §Blender physics policy](../../sources/space_vlog_series_concept_v2.md) | Округлённое земное ускорение, принятое в исходниках (4,905 = 0,5 × 9,81) и в Blender по умолчанию. Стандартное g₀ = 9,80665 м/с²; расхождение 0,03 % — несущественно. |
| `physics.au` | 149 597 870,7 | км | draft | IAU 2012 Resolution B2 | Астрономическая единица, точное значение по определению. |
| `physics.speed_of_light` | 299 792,458 | км/с | draft | SI, определение метра | Скорость света в вакууме, точное значение. |
| `physics.walk_speed` | 1 | м/с | draft | — | Расчётный параметр для оценки Кориолиса — спокойный шаг по кабине; не из исходников. |

### Земля и Юпитер

| Ключ | Значение | Единица | Статус | Источник | Примечание |
|---|---|---|---|---|---|
| `astro.earth_a` | 1 | а. е. | draft | [nssdc.gsfc.nasa.gov](https://nssdc.gsfc.nasa.gov/planetary/factsheet/jupiterfact.html) | Модель: орбита Земли круговая, радиус 1 а. е. Реальный эксцентриситет Земли 0,0167 (перигелий 147,095, афелий 152,100 млн км) в модели не учитывается. |
| `astro.jupiter_a` | 5,2038 | а. е. | draft | [nssdc.gsfc.nasa.gov](https://nssdc.gsfc.nasa.gov/planetary/factsheet/jupiterfact.html) | Большая полуось Юпитера, 778,479 млн км / 149,598 млн км (NSSDC, обновлено 2 окт. 2024). |
| `astro.jupiter_e` | 0,0487 | — | draft | [nssdc.gsfc.nasa.gov](https://nssdc.gsfc.nasa.gov/planetary/factsheet/jupiterfact.html) | Эксцентриситет орбиты Юпитера по таблице NSSDC (0,0487; перигелий 740,595, афелий 816,363 млн км — согласуются). В постановке было 0,0489 (старая версия таблицы); средние элементы J2000 дают 0,0484. |
| `astro.earth_jupiter_min_nssdc` | 588,5 | млн км | draft | [nssdc.gsfc.nasa.gov](https://nssdc.gsfc.nasa.gov/planetary/factsheet/jupiterfact.html) | Теоретический минимум NSSDC: перигелий Юпитера минус афелий Земли. Для сверки с моделью; недостижим — направления перигелия Юпитера и афелия Земли не совпадают. |
| `astro.earth_jupiter_max_nssdc` | 968,5 | млн км | draft | [nssdc.gsfc.nasa.gov](https://nssdc.gsfc.nasa.gov/planetary/factsheet/jupiterfact.html) | Теоретический максимум NSSDC — афелий Юпитера плюс афелий Земли. Для сверки с моделью. |

### Реальные ориентиры

| Ключ | Значение | Единица | Статус | Источник | Примечание |
|---|---|---|---|---|---|
| `reference.ihab_volume` | ≈10 | м³ | draft | [maya_ari_ship_3d_build_spec.md §38](../../sources/maya_ari_ship_3d_build_spec.md) | ESA Lunar I-Hab — «roughly 10 m³» жилого модуля для экипажа Gateway; реальный ориентир для сравнения. |
| `reference.clipper_cruise` | ≈5,5 | года | draft | [space_vlog_series_concept_v2.md §Long cruise times to Jupiter](../../sources/space_vlog_series_concept_v2.md) | Перелёт Europa Clipper с гравманёврами у Марса и Земли; реальный ориентир. |
| `reference.juice_cruise` | ≈8 | лет | draft | [space_vlog_series_concept_v2.md §Long cruise times to Jupiter](../../sources/space_vlog_series_concept_v2.md) | Перелёт JUICE с несколькими гравманёврами; реальный ориентир. |

### Раскладка жилого модуля (черновик)

| Ключ | Значение | Единица | Статус | Источник | Примечание |
|---|---|---|---|---|---|
| `layout.hull.floor_below_axis` | 0,75 | м | draft | [maya_ari_ship_3d_build_spec.md §3](../../sources/maya_ari_ship_3d_build_spec.md), [maya_ari_ship_3d_build_spec.md §13](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Плоская палуба ниже оси цилиндра модуля на эту величину: ось на высоте 0,75 м над полом (Z = 0,75), свод 2,15 м, хорда палубы ≈2,36 м, подпольная полость 0,65 м по оси (геометрию считает генератор чертежей). Компромисс между высотой кабины и объёмом подпольных баков. |
| `layout.hull.floor_width` | 2,0 | м | draft | — | Предложение, не согласовано. Чистая ширина пола главной кабины между вертикальными фасадами нижних шкафов (фасады при \|Y\| = 1,0 м). По ней ходит Майя; хорда палубы шире, ≈2,36 м. |
| `layout.hull.ceiling_height` | 2,05 | м | draft | [anatomy_prompts.md §Prompt 18](../../sources/anatomy_prompts.md) | Предложение, не согласовано. Чистая высота от пола до потолочной панели по оси кабины; над панелью до свода ≈0,10 м под свет, микрофоны ARI и воздуховоды. Запас над головой при росте 1,7 м — 0,35 м. |
| `layout.hull.underfloor_tank_height` | 0,5 | м | draft | [maya_ari_ship_3d_build_spec.md §13](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Высота подпольных водяных баков по оси модуля (вода «в полу и структурных полостях», SPEC §13); бока баков повторяют обвод корпуса. Баки под главной кабиной и камбузом. |
| `layout.lockers.depth` | 0,35 | м | draft | [maya_ari_ship_3d_build_spec.md §14](../../sources/maya_ari_ship_3d_build_spec.md), [anatomy_prompts.md §Prompt 18](../../sources/anatomy_prompts.md) | Предложение, не согласовано. Глубина стеновых шкафов по горизонтали на высоте оси модуля; выше и ниже задняя стенка повторяет корпус. За шкафом до корпуса ≈5 см под кабели и изоляцию. |
| `layout.lockers.front_height` | 1,6 | м | draft | — | Предложение, не согласовано. Высота вертикальных фасадов нижних шкафов; выше — наклонные верхние шкафы, как багажные полки самолёта, до края потолочной панели. |
| `layout.zones.window_bay` | 2,6–3,0 | м | draft | [maya_ari_ship_3d_build_spec.md §5](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Диапазон X (лок. рамка: 0 — середина модуля, + к носу): носовая переборка с осевым окном и внутренней частью шторки, место «у окна» (позиция 3). |
| `layout.zones.main_cabin` | 0,8–2,6 | м | draft | [maya_ari_ship_3d_build_spec.md §5](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Диапазон X главной рабочей и влоговой кабины: зона A — рабочее место у стены +Y (геройская стена), зона B — у стены −Y (назначение не определено). |
| `layout.zones.galley_storage` | 0,0–0,8 | м | draft | [maya_ari_ship_3d_build_spec.md §5](../../sources/maya_ari_ship_3d_build_spec.md), [maya_ari_ship_3d_build_spec.md §9](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Диапазон X: камбуз у стены +Y рядом с рабочим местом (SPEC §9), хранение у стены −Y. Часть одной открытой комнаты с главной кабиной. |
| `layout.zones.hygiene` | −1,1–0,0 | м | draft | [maya_ari_ship_3d_build_spec.md §5](../../sources/maya_ari_ship_3d_build_spec.md), [maya_ari_ship_3d_build_spec.md §10](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Диапазон X закрываемой кабинки санузла у борта +Y (от прохода до корпуса). За ней, X −2,0…−1,1, — сервисная ниша перед стеной СЖО и медшкаф на борту. |
| `layout.zones.stasis` | −2,0–0,0 | м | draft | [maya_ari_ship_3d_build_spec.md §5](../../sources/maya_ari_ship_3d_build_spec.md), [maya_ari_ship_3d_build_spec.md §11](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Диапазон X отсека SLEEP / MED / SAFE у борта −Y, койка вдоль X; сзади водяная часть стены СЖО, снизу подпольные баки — «самая защищённая часть» (SPEC §11, §13). |
| `layout.zones.eclss_wall` | −2,4–−2,0 | м | draft | [maya_ari_ship_3d_build_spec.md §5](../../sources/maya_ari_ship_3d_build_spec.md), [maya_ari_ship_3d_build_spec.md §12](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Диапазон X поперечной стены СЖО: обслуживаемые модули на половине +Y (лицом в сервисную нишу), вода на половине −Y (за отсеком стазиса), посередине дверной проём в тамбур. |
| `layout.zones.vestibule` | −3,0–−2,4 | м | draft | [maya_ari_ship_3d_build_spec.md §5](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Диапазон X тамбура перед люком на ферму. По SPEC §5 люк в кормовой переборке (X = −3,0); вариант C-003 — люк в «потолке» над тамбуром. |
| `layout.aisle_width` | 0,7 | м | draft | — | Предложение, не согласовано. Ширина центрального прохода между санузлом и отсеком стазиса и дверного проёма в стене СЖО; без прохода корма с люком недостижима (план SPEC §5 его не рисует). |
| `layout.desk.x` | 1,0–2,5 | м | draft | [maya_ari_ship_3d_build_spec.md §6](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Диапазон X стола рабочего места у геройской стены (+Y); кресло по центру стола. |
| `layout.desk.depth` | 0,55 | м | draft | — | Предложение, не согласовано. Глубина стола от фасада шкафов (\|Y\| = 1,0 м) к середине кабины. |
| `layout.desk.height` | 0,74 | м | draft | [anatomy_prompts.md §Prompt 18](../../sources/anatomy_prompts.md) | Предложение, не согласовано. Высота столешницы, обычная земная: при 0,5 g поза сидя та же, что на Земле (нейтральная поза невесомости не нужна). |
| `layout.chair.seat_height` | 0,45 | м | draft | [anatomy_prompts.md §Prompt 18](../../sources/anatomy_prompts.md) | Предложение, не согласовано. Высота сиденья кресла рабочего места над полом, для роста 1,7 м. |
| `layout.galley.counter_height` | 0,9 | м | draft | [maya_ari_ship_3d_build_spec.md §9](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Высота столешницы камбуза — работа стоя. |
| `layout.galley.counter_depth` | 0,6 | м | draft | — | Предложение, не согласовано. Глубина камбузной стены от фасада шкафов к середине кабины. |
| `layout.window.center_height` | 1,4 | м | draft | [maya_ari_ship_3d_build_spec.md §8](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Высота центра осевого окна над полом, по оси Y = 0. Проём habitat.window_width × habitat.window_height при любом размере из диапазона захватывает глаза стоящей (≈1,58 м) и сидящей (≈1,2 м) Майи и вписывается в носовую переборку. |
| `layout.display_primary.center_x` | 1,95 | м | draft | [maya_ari_ship_3d_build_spec.md §6](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. X центра основного дисплея (habitat.display_primary) на фасаде геройской стены (+Y) над столом. |
| `layout.display_primary.center_height` | 1,2 | м | draft | [anatomy_prompts.md §Prompt 13](../../sources/anatomy_prompts.md) | Предложение, не согласовано. Высота центра основного дисплея — у глаз сидящей Майи (≈1,2 м). |
| `layout.display_secondary.center_x` | 1,15 | м | draft | [maya_ari_ship_3d_build_spec.md §6](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. X центра вспомогательного дисплея, к корме от основного, на той же стене. |
| `layout.display_secondary.center_height` | 1,2 | м | draft | [anatomy_prompts.md §Prompt 13](../../sources/anatomy_prompts.md) | Предложение, не согласовано. Высота центра вспомогательного дисплея. |
| `layout.ari_isolate_panel.x` | 1,15 | м | draft | [maya_ari_ship_3d_build_spec.md §6](../../sources/maya_ari_ship_3d_build_spec.md), [decisions.md §D-010](decisions.md) | Предложение, не согласовано. X панели защищённых органов (SPEC §6) с переключателем ARI ISOLATE под крышкой: на геройской стене (+Y), под вспомогательным дисплеем, в досягаемости из кресла. Жёсткий провод от панели идёт по ферме к контакторам ядра ARI (exterior.ari_core). |
| `layout.ari_isolate_panel.height` | 0,9 | м | draft | [decisions.md §D-010](decisions.md) | Предложение, не согласовано. Высота центра панели над полом — над столешницей, ниже дисплеев. |
| `layout.camera_a.x` | 1,45 | м | draft | [maya_ari_ship_3d_build_spec.md §26](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Камера A (влог) — у стены −Y напротив рабочего места; X лок. рамки. |
| `layout.camera_a.y` | −0,9 | м | draft | [maya_ari_ship_3d_build_spec.md §26](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Y камеры A (−Y — правый борт, если смотреть в нос). |
| `layout.camera_a.height` | 1,3 | м | draft | [maya_ari_ship_3d_build_spec.md §26](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Высота камеры A — «near eye level» сидящей Майи с небольшим запасом. |
| `layout.camera_a.yaw` | 57 | ° | draft | [anatomy_prompts.md §Prompt 06](../../sources/anatomy_prompts.md) | Предложение, не согласовано. Курс камеры A в плане (от +X к +Y): в кадре Майя за столом, геройская стена и край осевого окна. |
| `layout.camera_a.hfov` | 50 | ° | draft | [anatomy_prompts.md §Prompt 06](../../sources/anatomy_prompts.md) | Предложение, не согласовано. Горизонтальное поле зрения вертикального кадра 9:16 (вертикальное ≈80°). |
| `layout.camera_b.x` | 0,05 | м | draft | [maya_ari_ship_3d_build_spec.md §26](../../sources/maya_ari_ship_3d_build_spec.md), [contradictions.md §C-009](contradictions.md) | Предложение, не согласовано. Камера B (общий план) — верхний кормовой угол открытой комнаты, на передней стенке отсека стазиса (C-009: по SPEC). Сервисная стена из этой точки не видна. |
| `layout.camera_b.y` | −0,8 | м | draft | [maya_ari_ship_3d_build_spec.md §26](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Y камеры B — под краем верхних шкафов борта −Y. |
| `layout.camera_b.height` | 1,75 | м | draft | [maya_ari_ship_3d_build_spec.md §26](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Высота камеры B — выше головы, под верхними шкафами (у свода корпус уже 0,7 м). |
| `layout.camera_b.yaw` | 48 | ° | draft | [anatomy_prompts.md §Prompt 06](../../sources/anatomy_prompts.md) | Предложение, не согласовано. Курс камеры B: рабочее место, камбуз, окно. |
| `layout.camera_b.hfov` | 68 | ° | draft | [anatomy_prompts.md §Prompt 06](../../sources/anatomy_prompts.md) | Предложение, не согласовано. Горизонтальное поле зрения камеры B, кадр 9:16 (вертикальное ≈100°). |
| `layout.camera_c.x` | 2,45 | м | draft | [maya_ari_ship_3d_build_spec.md §26](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Камера C (крупный план) — на геройской стене у носового края основного дисплея. |
| `layout.camera_c.y` | 0,95 | м | draft | [maya_ari_ship_3d_build_spec.md §26](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Y камеры C (+Y — геройская стена). |
| `layout.camera_c.height` | 1,3 | м | draft | [maya_ari_ship_3d_build_spec.md §26](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Высота камеры C — уровень глаз сидящей Майи. |
| `layout.camera_c.yaw` | −131 | ° | draft | [anatomy_prompts.md §Prompt 06](../../sources/anatomy_prompts.md) | Предложение, не согласовано. Курс камеры C: на кресло, «slightly off-axis» от основного дисплея. |
| `layout.camera_c.hfov` | 43 | ° | draft | [anatomy_prompts.md §Prompt 06](../../sources/anatomy_prompts.md) | Предложение, не согласовано. Горизонтальное поле зрения камеры C, кадр 9:16 (вертикальное ≈70°). |
| `layout.hatch.diameter` | 0,8 | м | draft | [anatomy_prompts.md §Prompt 18](../../sources/anatomy_prompts.md), International Docking System Standard (IDSS) IDD — проход Ø800 мм | Предложение, не согласовано. Чистый диаметр люка на ферму; ориентир — проход стыковочного стандарта IDSS. Тот же диаметр у варианта люка в «потолке» (C-003). |
| `layout.hatch.center_height` | 0,9 | м | draft | [maya_ari_ship_3d_build_spec.md §5](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Высота центра люка в кормовой переборке (по SPEC §5, C-003): порог 0,5 м, верх 1,3 м — проход пригнувшись. |
| `layout.hatch.alt_ceiling_x` | −2,6 | м | draft | [contradictions.md §C-003](contradictions.md) | Предложение, не согласовано. X центра альтернативного люка в своде над тамбуром (вариант (а) C-003); на чертежах пунктиром. Ферма при этом стоит над тамбуром без колена. |

### Внешний облик корабля (черновик)

| Ключ | Значение | Единица | Статус | Источник | Примечание |
|---|---|---|---|---|---|
| `exterior.habitat.outer_diameter` | 3,4 | м | draft | [anatomy_prompts.md §Prompt 02](../../sources/anatomy_prompts.md), [anatomy_prompts.md §Prompt 03](../../sources/anatomy_prompts.md) | Предложение, не согласовано. Наружный диаметр жилого модуля по защитной оболочке: внутренний 2,8 м плюс 0,3 м на сторону — гермооболочка, изоляция, противометеоритный экран (PROMPTS 02 №2). |
| `exterior.habitat.outer_length` | 7,0 | м | draft | [anatomy_prompts.md §Prompt 03](../../sources/anatomy_prompts.md) | Предложение, не согласовано. Наружная длина модуля: внутренние 6,0 м плюс 0,5 м на торец — рама окна и короб шторки спереди, днище сзади. |
| `exterior.spine.length` | 72 | м | draft | [maya_ari_ship_3d_build_spec.md §1](../../sources/maya_ari_ship_3d_build_spec.md), [anatomy_prompts.md §Prompt 01](../../sources/anatomy_prompts.md) | Предложение, не согласовано. Длина хребта от носа до среза двигателей — грубо, по пропорции к радиусу 28 м: реактор далеко от жилья (PROMPTS 01), между ними баки и радиаторы. |
| `exterior.spine.diameter` | 1,6 | м | draft | — | Предложение, не согласовано. Поперечник фермы хребта — для силуэта. |
| `exterior.comms.station` | 0–6 | м | draft | [maya_ari_ship_3d_build_spec.md §1](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Станции носовой секции «sensor / comms» (м от носа). |
| `exterior.hub.station` | 12 | м | draft | [maya_ari_ship_3d_build_spec.md §1](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Станция ступицы — узла, где корни обеих ферм встречаются с хребтом; здесь же ядро ARI. Оси обеих ферм — на этой станции. |
| `exterior.boom.width` | 1,2 | м | draft | [maya_ari_ship_3d_build_spec.md §5](../../sources/maya_ari_ship_3d_build_spec.md), [maya_ari_ship_3d_build_spec.md §34](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Поперечник проходной фермы: внутри гермотрубка под люк Ø0,8 м, трассы и жёсткая линия ARI ISOLATE. |
| `exterior.boom.elbow_x` | −4,3 | м | draft | [contradictions.md §C-003](contradictions.md) | Предложение, не согласовано. X оси фермы в лок. рамке модуля для варианта SPEC (люк в корме): колено за кормовым торцем. Модуль висит на ферме носом вперёд; его центр на 4,3 м к носу от станции ступицы. |
| `exterior.counterweight.radius` | 22–26 | м | draft | [maya_ari_ship_3d_build_spec.md §1](../../sources/maya_ari_ship_3d_build_spec.md), [maya_ari_ship_3d_build_spec.md §32](../../sources/maya_ari_ship_3d_build_spec.md) | Предложение, не согласовано. Радиус центра противовеса — диапазон хода («~variable» SPEC §1.1): баланс m·r при расходе запасов. Центр противовеса — на одной станции с центром жилого модуля (динамический баланс). |
| `exterior.counterweight.length` | 4,0 | м | draft | [anatomy_prompts.md §Prompt 15](../../sources/anatomy_prompts.md) | Предложение, не согласовано. Длина противовеса вдоль X. |
| `exterior.counterweight.diameter` | 3,0 | м | draft | [anatomy_prompts.md §Prompt 15](../../sources/anatomy_prompts.md) | Предложение, не согласовано. Диаметр противовеса — короче и толще жилого модуля, не его близнец. |
| `exterior.tanks.station` | 16–28 | м | draft | [maya_ari_ship_3d_build_spec.md §1](../../sources/maya_ari_ship_3d_build_spec.md), [contradictions.md §C-007](contradictions.md) | Предложение, не согласовано. Станции баков рабочего тела на хребте сразу за ступицей (C-007, вариант а): их масса прикрывает ядро ARI с кормы. |
| `exterior.tanks.diameter` | 5,0 | м | draft | — | Предложение, не согласовано. Поперечник пакета баков вокруг хребта. |
| `exterior.radiators.station` | 31–55 | м | draft | [maya_ari_ship_3d_build_spec.md §1](../../sources/maya_ari_ship_3d_build_spec.md), [anatomy_prompts.md §Prompt 14](../../sources/anatomy_prompts.md) | Предложение, не согласовано. Станции раскладных радиаторов между баками и реактором (SPEC §1.1). |
| `exterior.radiators.half_span` | 9 | м | draft | — | Предложение, не согласовано. Вылет панели радиатора от оси хребта; на чертеже панели в плоскости ферм, их ориентация не решена. |
| `exterior.reactor.station` | 58–63 | м | draft | [maya_ari_ship_3d_build_spec.md §1](../../sources/maya_ari_ship_3d_build_spec.md), [anatomy_prompts.md §Prompt 14](../../sources/anatomy_prompts.md) | Предложение, не согласовано. Станции реактора с теневой защитой на носовой стороне; до жилого модуля ≈50 м по оси. |
| `exterior.reactor.diameter` | 3,0 | м | draft | — | Предложение, не согласовано. Поперечник блока реактора и защиты. |
| `exterior.propulsion.station` | 64–72 | м | draft | [maya_ari_ship_3d_build_spec.md §1](../../sources/maya_ari_ship_3d_build_spec.md), [anatomy_prompts.md §Prompt 14](../../sources/anatomy_prompts.md) | Предложение, не согласовано. Станции осевой двигательной установки; срез сопел — корма хребта. |
| `exterior.ari_core.station` | 12 | м | draft | [decisions.md §D-010](decisions.md) | Предложение, не согласовано. Станция центра ядра ARI — на оси вращения в ступице. На оси ядро не нарушает статический баланс; его прикрывают баки за ним и сам хребет. |
| `exterior.ari_core.vault_length` | 3,0 | м | draft | [www.jpl.nasa.gov](https://www.jpl.nasa.gov/news/juno-armored-up-to-go-to-jupiter) | Предложение, не согласовано. Длина бронированного сейфа ядра вдоль хребта. Прецедент — титановый сейф электроники Juno: стенки ≈1 см, ≈200 кг, «размером с багажник внедорожника» (NASA JPL, 2010). |
| `exterior.ari_core.vault_diameter` | 2,6 | м | draft | [www.jpl.nasa.gov](https://www.jpl.nasa.gov/news/juno-armored-up-to-go-to-jupiter) | Предложение, не согласовано. Диаметр сейфа ядра ARI, соосного хребту. |
| `exterior.ari_core.power` | 20–50 | кВт | draft | [decisions.md §D-010](decisions.md) | Предложение, не согласовано. Электрическая мощность ядра: «десятки кВт» от реактора; тепло — по хребту на радиаторы. |
| `exterior.ari_core.battery_energy` | 100 | кВт·ч | draft | — | Предложение, не согласовано. Батарейный буфер ядра: ≈2 ч при 50 кВт или ≈5 ч при 20 кВт — переждать останов и перезапуск реактора. |
| `exterior.ari_core.battery_station` | 13,5–15,0 | м | draft | — | Предложение, не согласовано. Станции кольцевого блока батарей сразу за сейфом, перед баками. |
| `exterior.ari_core.manual_breaker.station` | 12 | м | draft | [decisions.md §D-010](decisions.md) | Предложение, не согласовано. Станция ручного механического рубильника питания ARI — у сейфа, в торце проходной фермы жилого модуля. Рядом силовые контакторы: их держит только жёсткий провод от ARI ISOLATE в кабине, без ПО в цепи. |
| `exterior.ari_core.manual_breaker.radius` | 1,6 | м | draft | [decisions.md §D-010](decisions.md) | Предложение, не согласовано. Расстояние рубильника от оси вращения; тяжесть там ≈0,03 g — Майя добирается по ферме, где вес падает от 0,5 g почти до нуля. |

## Производные величины

Считает `calc/derive.py`; статус производной — самый слабый из статусов входов.

### Жилой модуль

| Ключ | Значение | Без округления | Единица | Формула | Входы | Статус | Примечание |
|---|---|---|---|---|---|---|---|
| `habitat.floor_accel` | 4,905 | 4,905 | м/с² | `a = g_пол · g` | `habitat.floor_gravity`, `physics.g_earth` | draft | Целевое ускорение на полу; совпадает с 4,905 м/с² из SPEC §4 и CONCEPT. |
| `habitat.gross_volume` | ≈37 | 36,9451 | м³ | `V = π · (D / 2)² · L` | `habitat.inner_diameter`, `habitat.inner_length` | draft | Брутто-объём внутреннего цилиндра без торцевых днищ; SPEC §3: «roughly 37 m³». |
| `habitat.usable_fraction` | ≈65–76 | 64,9612–75,7881 | % | `V_полезн / V × 100 %` | `habitat.usable_volume`, `habitat.gross_volume` | draft | Доля полезного объёма от брутто-объёма цилиндра. |
| `habitat.window_image_period` | ≈15,0 | 15,012 | с | `T_окно = T = 2π / ω` | `ship.spin_period` | draft | Окно смотрит вдоль оси вращения (SPEC §8): картинка не уходит из окна, а поворачивается вокруг центра окна с периодом вращения корабля; объект точно на оси вращается на месте. |

### Производство

| Ключ | Значение | Без округления | Единица | Формула | Входы | Статус | Примечание |
|---|---|---|---|---|---|---|---|
| `production.blender_gravity_z` | −4,905 | −4,905 | м/с² | `Z = −a` | `habitat.floor_accel` | draft | Scene Gravity Z в Blender (SPEC §4): интерьер не вращается, тяжесть — постоянная вниз. |

### Вращение корабля

| Ключ | Значение | Без округления | Единица | Формула | Входы | Статус | Примечание |
|---|---|---|---|---|---|---|---|
| `ship.spin_omega` | 0,419 | 0,418543 | рад/с | `ω = √(a / r)` | `habitat.floor_accel`, `habitat.floor_radius` | draft | Угловая скорость вращения корабля вокруг продольной оси (из a = ω²r). |
| `ship.spin_rpm` | ≈4,0 | 3,99679 | об/мин | `n = 60 · ω / 2π` | `ship.spin_omega` | draft | SPEC §1.1 и §40 округляют до «~4 rpm». |
| `ship.spin_period` | ≈15,0 | 15,012 | с | `T = 2π / ω` | `ship.spin_omega` | draft | Период одного оборота корабля. |
| `ship.spin_rpm_concept` | ≈4,23 | 4,22981 | об/мин | `n = 60 · √(a / r_concept) / 2π` | `habitat.floor_accel`, `habitat.floor_radius_concept` | draft | Обороты для варианта CONCEPT 25 м; совпадает с «4.23 rpm» из CONCEPT (C-001). |
| `ship.spin_period_concept` | ≈14,2 | 14,185 | с | `T = 2π / √(a / r_concept)` | `habitat.floor_accel`, `habitat.floor_radius_concept` | draft | Период вращения для варианта CONCEPT 25 м. |
| `ship.spin_rpm_concept_range` | ≈3,9–4,7 | 3,86127–4,72907 | об/мин | `n = 60 · √(a / r) / 2π, r = 30…20 м` | `habitat.floor_accel`, `habitat.floor_radius_concept_range` | draft | Обороты на краях диапазона радиусов CONCEPT 20–30 м. |

### Искусственная тяжесть

| Ключ | Значение | Без округления | Единица | Формула | Входы | Статус | Примечание |
|---|---|---|---|---|---|---|---|
| `gravity.head_accel` | 4,61 | 4,6072 | м/с² | `a_гол = ω² · (r − h)` | `ship.spin_omega`, `habitat.floor_radius`, `maya.height` | draft | Тяжесть на высоте головы стоящей Майи (h — рост, голова на h над полом, ближе к оси). |
| `gravity.head_g` | 0,47 | 0,469643 | g | `a_гол / g` | `gravity.head_accel`, `physics.g_earth` | draft | То же в долях земной тяжести. |
| `gravity.gradient_head` | 6,1 | 6,07143 | % | `(a − a_гол) / a × 100 % = h / r × 100 %` | `habitat.floor_accel`, `gravity.head_accel` | draft | Перепад тяжести от ног к голове: голова легче ступней на эту долю. |
| `gravity.coriolis_across` | 0,84 | 0,837087 | м/с² | `a_К = 2 · ω · v` | `ship.spin_omega`, `physics.walk_speed` | draft | Шаг поперёк кабины (по Y, касательно вращению; v ⊥ ω). Кориолисово ускорение радиальное: по ходу вращения Майя тяжелее, против — легче на эту величину; центробежная поправка v²/r ≈ 0,04 м/с² — на порядок меньше. |
| `gravity.coriolis_across_frac` | ≈17 | 17,066 | % | `2 · ω · v / a × 100 %` | `gravity.coriolis_across`, `habitat.floor_accel` | draft | Кориолис при шаге поперёк кабины в долях местной тяжести на полу. |
| `gravity.coriolis_along` | 0 | 0 | м/с² | `a_К = 2 · ω × v = 0 при v ∥ ω` | `ship.spin_omega`, `physics.walk_speed` | draft | Шаг вдоль кабины: ось модуля параллельна оси вращения (SPEC §4: +X — вперёд по оси), v ∥ ω, векторное произведение равно нулю. Подъём и приседание (по Z) дают боковой снос. |

### Земля и Юпитер

| Ключ | Значение | Без округления | Единица | Формула | Входы | Статус | Примечание |
|---|---|---|---|---|---|---|---|
| `astro.earth_jupiter_min_au` | ≈3,95 | 3,95037 | а. е. | `d_min = a_J · (1 − e_J) − a_З` | `astro.jupiter_a`, `astro.jupiter_e`, `astro.earth_a` | draft | Модель: Земля на круговой орбите 1 а. е.; Юпитер — кеплеров эллипс (a, e по NSSDC); орбиты компланарны (наклон Юпитера 1,3° не учтён); минимум — противостояние при Юпитере в перигелии, максимум — соединение при Юпитере в афелии. Корабль в системе Юпитера считается в его центре (орбиты спутников — до ~1,9 млн км, < 0,5 %). Теоретические крайние значения NSSDC с учётом эксцентриситета Земли — 588,5–968,5 млн км (astro.earth_jupiter_*_nssdc). |
| `astro.earth_jupiter_max_au` | ≈6,46 | 6,45723 | а. е. | `d_max = a_J · (1 + e_J) + a_З` | `astro.jupiter_a`, `astro.jupiter_e`, `astro.earth_a` | draft | Модель: Земля на круговой орбите 1 а. е.; Юпитер — кеплеров эллипс (a, e по NSSDC); орбиты компланарны (наклон Юпитера 1,3° не учтён); минимум — противостояние при Юпитере в перигелии, максимум — соединение при Юпитере в афелии. Корабль в системе Юпитера считается в его центре (орбиты спутников — до ~1,9 млн км, < 0,5 %). Теоретические крайние значения NSSDC с учётом эксцентриситета Земли — 588,5–968,5 млн км (astro.earth_jupiter_*_nssdc). |
| `astro.earth_jupiter_min` | ≈591 | 590,968 | млн км | `d_min · а. е.` | `astro.earth_jupiter_min_au`, `physics.au` | draft | Модель: Земля на круговой орбите 1 а. е.; Юпитер — кеплеров эллипс (a, e по NSSDC); орбиты компланарны (наклон Юпитера 1,3° не учтён); минимум — противостояние при Юпитере в перигелии, максимум — соединение при Юпитере в афелии. Корабль в системе Юпитера считается в его центре (орбиты спутников — до ~1,9 млн км, < 0,5 %). Теоретические крайние значения NSSDC с учётом эксцентриситета Земли — 588,5–968,5 млн км (astro.earth_jupiter_*_nssdc). |
| `astro.earth_jupiter_max` | ≈966 | 965,987 | млн км | `d_max · а. е.` | `astro.earth_jupiter_max_au`, `physics.au` | draft | Модель: Земля на круговой орбите 1 а. е.; Юпитер — кеплеров эллипс (a, e по NSSDC); орбиты компланарны (наклон Юпитера 1,3° не учтён); минимум — противостояние при Юпитере в перигелии, максимум — соединение при Юпитере в афелии. Корабль в системе Юпитера считается в его центре (орбиты спутников — до ~1,9 млн км, < 0,5 %). Теоретические крайние значения NSSDC с учётом эксцентриситета Земли — 588,5–968,5 млн км (astro.earth_jupiter_*_nssdc). |
| `astro.earth_jupiter_distance` | ≈591–966 | 590,968–965,987 | млн км | `[d_min, d_max]` | `astro.earth_jupiter_min`, `astro.earth_jupiter_max` | draft | Модель: Земля на круговой орбите 1 а. е.; Юпитер — кеплеров эллипс (a, e по NSSDC); орбиты компланарны (наклон Юпитера 1,3° не учтён); минимум — противостояние при Юпитере в перигелии, максимум — соединение при Юпитере в афелии. Корабль в системе Юпитера считается в его центре (орбиты спутников — до ~1,9 млн км, < 0,5 %). Теоретические крайние значения NSSDC с учётом эксцентриситета Земли — 588,5–968,5 млн км (astro.earth_jupiter_*_nssdc). |
| `astro.light_delay_min` | ≈33 | 32,8543 | мин | `τ_min = d_min / c` | `astro.earth_jupiter_min`, `physics.speed_of_light` | draft | Задержка сигнала в одну сторону: расстояние / c, по прямой, без задержек в аппаратуре и релятивистских поправок. Допущения расстояния — см. astro.earth_jupiter_distance. |
| `astro.light_delay_max` | ≈54 | 53,7031 | мин | `τ_max = d_max / c` | `astro.earth_jupiter_max`, `physics.speed_of_light` | draft | Задержка сигнала в одну сторону: расстояние / c, по прямой, без задержек в аппаратуре и релятивистских поправок. Допущения расстояния — см. astro.earth_jupiter_distance. |
| `astro.light_delay` | ≈33–54 | 32,8543–53,7031 | мин | `[τ_min, τ_max]` | `astro.light_delay_min`, `astro.light_delay_max` | draft | Задержка сигнала в одну сторону: расстояние / c, по прямой, без задержек в аппаратуре и релятивистских поправок. Допущения расстояния — см. astro.earth_jupiter_distance. |

## Связи
- [Справочное](index.md) — оглавление раздела
- [Решения](decisions.md) — изменения канонических чисел фиксируются здесь
- [Противоречия](contradictions.md) — расхождения чисел между исходниками (C-001: радиус пола)
