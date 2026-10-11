# Сайт вики (Quartz v4 на GitHub Pages)

Адрес: https://yunoshev.github.io/may-in-transit/ (закрыт от индексации: meta robots + robots.txt).
- `prepare.mjs` — клонирует Quartz на закреплённый коммит, накладывает конфиг, собирает `content/` из `ru/` и `assets/`.
  Ссылки на `sources/` и `CLAUDE.md` превращаются в подписи, `ru/index.md` становится главной, ведущий `# H1` убирается.
- `quartz.config.ts`, `quartz.layout.ts`, `styles/custom.scss` — конфиг, макет, стили (callout'ы и `data-canon` как в `wiki.css`).
- `patches/` — три точечные правки исходников Quartz (русский поиск, текст таблиц, прыжок страницы); якорь не найден = сборка падает.
- `check-links.mjs` — проверка внутренних ссылок и якорей в собранном сайте.
- Локально: `node site/prepare.mjs && cd site/.work/quartz && npx quartz build --serve` (Node >= 22). Всё в `site/.work/` не коммитится.
- Обновить Quartz: сменить `QUARTZ_COMMIT` в `prepare.mjs`, пересобрать, проверить `patches/`.
- CI: `.github/workflows/pages.yml`; один раз включить Settings -> Pages -> Source: GitHub Actions.
