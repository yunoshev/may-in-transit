---
title: Внешние источники
aliases: [sources, references, external sources, URL из исходников, ссылки]
type: reference
status: draft
sources:
  - sources/space_vlog_series_concept_v2.md (VERIFIED)
  - sources/maya_ari_ship_3d_build_spec.md §38
tags: [reference/sources]
---

# Внешние источники

Кратко: все URL, которые встречаются в исходниках, сгруппированные по темам. У каждого указано, что он подтверждает, и на каких страницах вики используется. Ссылки перенесены как в исходниках; содержание страниц в волне 1 заново не проверялось. Проверка по существу — задача агента реализма в волне 2 ([метод](../60-realism/index.md)).

## Как пользоваться
- Факт из реального мира на странице вики, помеченный `[!verified]`, должен опираться либо на источник из этой таблицы, либо на новый источник, который сюда же добавляется.
- Источник добавляется один раз; страницы только ссылаются на запись здесь или на URL.
- WebSearch ограничен, предпочтительны WebFetch известных страниц (NASA, ESA, JPL, рецензируемые журналы).

## Туры по системе Юпитера и гравитационные манёвры у лун

| Источник | URL | Что подтверждает | Где используется |
|---|---|---|---|
| ESA — JUICE Trajectory Profile | https://www.cosmos.esa.int/web/juice/trajectory-profile | миссия JUICE проводит годы в туре по системе Юпитера; гравитационные манёвры у Каллисто и Ганимеда формируют траекторию | [Тур по системе Юпитера](../20-mission/jovian-tour.md), [Гравитационный манёвр](../50-science/gravity-assist.md), [Миссии-прототипы](../50-science/reference-missions.md) |
| NASA — Europa Study 2012 Report | https://europa.nasa.gov/system/downloadable_items/56_ES_2012_Report_-_Final_-_20120502.pdf | исследования миссии к Европе используют манёвры у Ганимеда после выхода на орбиту Юпитера, чтобы снизить орбитальную энергию и организовать сближения с Европой | [Тур по системе Юпитера](../20-mission/jovian-tour.md), [Прибытие](../20-mission/jupiter-arrival.md), [Встречи с Европой](../20-mission/europa-encounters.md) |

Вывод CONCEPT: фиктивная миссия с повторяющимися петлями с помощью лун — разумная художественная экстраполяция, но её траектория требует собственной симуляции.

## Длительность перелёта к Юпитеру

| Источник | URL | Что подтверждает | Где используется |
|---|---|---|---|
| NASA — Europa Clipper trajectory | https://science.nasa.gov/missions/europa-clipper/europa-clipper-resources/europa-clippers-trajectory-to-jupiter/ | траектория Europa Clipper около 5,5 лет с гравитационными манёврами у Марса и Земли | [Перелёт к Юпитеру](../20-mission/interplanetary-cruise.md), [Миссии-прототипы](../50-science/reference-missions.md) |
| ESA — JUICE journey and Jupiter system tour (видео) | https://www.esa.int/ESA_Multimedia/Videos/2022/03/Juice_s_journey_and_Jupiter_system_tour | перелёт JUICE около 8 лет с несколькими планетарными манёврами | [Перелёт к Юпитеру](../20-mission/interplanetary-cruise.md), [Миссии-прототипы](../50-science/reference-missions.md) |

Вывод CONCEPT: вымышленная пилотируемая миссия 2050-х может использовать более энергичную траекторию, поэтому длительность перелёта и стазиса не копирует ни одну из этих миссий ([Q-003](open-questions.md)).

## Компактный многофункциональный жилой модуль и функции экипажа

| Источник | URL | Что подтверждает | Где используется |
|---|---|---|---|
| NASA — Gateway: The Lunar Space Station | https://www.nasa.gov/podcasts/houston-we-have-a-podcast/gateway-the-lunar-space-station/ | Gateway HALO — компактная среда, где упражнения, гигиена и хранение делят ограниченное пространство | [Жилой модуль](../30-ship/habitat/index.md), [Планировка](../30-ship/habitat/interior-layout.md), [Хранение](../30-ship/habitat/storage.md) |
| ESA — Gateway: Lunar I-Hab | https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/Gateway_Lunar_I-Hab | I-Hab — модуль около 10 м³ для сна, еды, упражнений и медицинских функций | [Жилой модуль](../30-ship/habitat/index.md), [Гермокорпус](../30-ship/habitat/pressure-vessel.md), [Тренажёры](../30-ship/habitat/exercise.md) |
| NASA — Meet NASA's Orion Spacecraft | https://www.nasa.gov/missions/meet-nasas-orion-spacecraft/ | на Orion есть питьевая вода, подогрев еды, компактный туалет и тренажёр; экипаж использует зоны хранения и плотные материалы как укрытие при солнечном радиационном событии | [Камбуз](../30-ship/habitat/galley.md), [Санузел](../30-ship/habitat/hygiene.md), [Тренажёры](../30-ship/habitat/exercise.md), [Радиационная защита](../30-ship/systems/radiation-protection.md) |

## Системы жизнеобеспечения (ECLSS)

| Источник | URL | Что подтверждает | Где используется |
|---|---|---|---|
| NASA — Environmental Control and Life Support Systems (ECLSS) | https://www.nasa.gov/reference/environmental-control-and-life-support-systems-eclss/ | регенерация воздуха, генерация кислорода, возврат воды, обращение с отходами и мониторинг среды — базовые функции жизнеобеспечения | [Жизнеобеспечение](../30-ship/systems/life-support.md), [Вода](../30-ship/systems/water.md), [Сервисная стена СЖО](../30-ship/habitat/service-wall.md) |
| ESA — Air Revitalization System | https://www.esa.int/content/view/full/194826 | системы регенерации воздуха удаляют CO2 и следовые загрязнители | [Жизнеобеспечение](../30-ship/systems/life-support.md) |
| ESA — Water Recovery System Racks | https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/Node-3_Cupola/Water_Recovery_System_Racks | системы возврата воды перерабатывают мочу, пот и гигиеническую воду | [Вода](../30-ship/systems/water.md), [Жизнеобеспечение](../30-ship/systems/life-support.md) |

## Радиационная защита запасами и водой

| Источник | URL | Что подтверждает | Где используется |
|---|---|---|---|
| NASA — Meet NASA's Orion Spacecraft | https://www.nasa.gov/missions/meet-nasas-orion-spacecraft/ | см. выше: экипаж Orion использует зоны хранения и плотные бортовые материалы как укрытие | [Радиационная защита](../30-ship/systems/radiation-protection.md), [Отсек стазиса, сна и укрытия](../30-ship/habitat/stasis-shelter.md) |
| ESA — For astronaut radiation protection, just add water | https://www.esa.int/Enabling_Support/Space_Engineering_Technology/For_astronaut_radiation_protection_just_add_water | ESA изучала воду как радиационную защиту | [Радиационная защита](../30-ship/systems/radiation-protection.md), [Вода](../30-ship/systems/water.md) |
| ESA — ESA engineers assess Moon Village habitat | https://www.esa.int/Enabling_Support/Space_Engineering_Technology/CDF/ESA_engineers_assess_Moon_Village_habitat | изучено размещение систем с водой вокруг защищаемых зон экипажа | [Радиационная защита](../30-ship/systems/radiation-protection.md), [Отсек стазиса, сна и укрытия](../30-ship/habitat/stasis-shelter.md) |

Ограничение SPEC §11 и §39: точная эффективность нашей компоновки не определена ([Q-015](open-questions.md)).

## Искусственная гравитация вращением

| Источник | URL | Что подтверждает | Где используется |
|---|---|---|---|
| NASA NTRS — Development and Comparison of an Artificial Gravity Concept for Human Spaceflight | https://ntrs.nasa.gov/citations/20205004959 | соотношение a = ω²r для вращательной искусственной гравитации; радиус около 28 м при около 4 об/мин даёт около 0,5 g на полу | [Искусственная гравитация](../30-ship/artificial-gravity.md), [Физика вращающейся системы](../50-science/rotating-reference-frames.md) |
| Frontiers in Systems Neuroscience — Artificial gravity as a countermeasure for mitigating physiological deconditioning during long-duration space missions | https://www.frontiersin.org/journals/systems-neuroscience/articles/10.3389/fnsys.2015.00092/full | рецензируемая литература использует то же соотношение; искусственная гравитация как средство против физиологической дезадаптации (deconditioning) в длительных полётах | [Искусственная гравитация](../30-ship/artificial-gravity.md), [Человек в долгом полёте](../50-science/human-factors.md) |

## Нужные, но пока не найденные источники
Исходники не дают ссылок на следующие темы. Источники добавит агент соответствующей страницы в волне 2.

| Тема | Страница |
|---|---|
| расстояния Земля–Юпитер, диапазон и сближения | [Расстояния и задержка сигнала](../50-science/distances-and-light-time.md) |
| радиационные пояса Юпитера, дозы у Европы | [Радиационная среда Юпитера](../50-science/jovian-radiation.md) |
| физические параметры Юпитера, Европы, Ганимеда, Каллисто, Ио | [Юпитер](../50-science/jupiter.md), [Европа](../50-science/europa.md) |
| траектории захвата у Юпитера (Juno и др.) | [Прибытие](../20-mission/jupiter-arrival.md) |
| переносимость вращения человеком, частичная гравитация | [Человек в долгом полёте](../50-science/human-factors.md) |

## Связи
- [Реализм: метод](../60-realism/index.md) — как источники превращаются в оценки
- [Миссии-прототипы](../50-science/reference-missions.md) — реальные миссии, на которые опираются источники
- [Жизнеобеспечение](../30-ship/systems/life-support.md) — основная страница по ECLSS-источникам
- [Справочное: оглавление](index.md) — другие служебные страницы

## Основания
> [!verified] Проверено
> Список URL взят дословно из sources/maya_ari_ship_3d_build_spec.md §38 и sources/space_vlog_series_concept_v2.md (VERIFIED). Содержание страниц по ссылкам в волне 1 не перепроверялось.

> [!production] Решение для производства
> Источник описан одним предложением «что подтверждает» и привязан к страницам, чтобы агент реализма мог проверять утверждения по записи, а не искать заново.

## Открытые вопросы
- Проверить, что все 14 URL открываются и подтверждают то, что приписано исходниками (волна 2).
- Добавить источники для тем из последней таблицы.
