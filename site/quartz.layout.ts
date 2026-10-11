import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

// Проводник: показывает разделы вики вместо технической папки ru/ и сортирует их по
// номеру в имени папки (10-world, 20-mission…). Функции сериализуются в браузер через toString(),
// поэтому они самодостаточны и не используют внешние переменные.
const explorer = Component.Explorer({
  folderDefaultState: "collapsed",
  folderClickBehavior: "link",
  useSavedState: true,
  filterFn: (node) => node.slugSegment !== "tags",
  mapFn: (node) => {
    // корень дерева: поднимаем содержимое ru/ на верхний уровень (главная — это заголовок сайта)
    if (node.slugSegment === undefined) {
      const ru = node.children.find((c) => c.slugSegment === "ru")
      if (ru) {
        node.children = [...ru.children, ...node.children.filter((c) => c !== ru)]
      }
    }
  },
  sortFn: (a, b) => {
    if (a.isFolder !== b.isFolder) return a.isFolder ? -1 : 1
    if (a.isFolder) {
      return a.slugSegment.localeCompare(b.slugSegment, undefined, { numeric: true })
    }
    return a.displayName.localeCompare(b.displayName, "ru", { numeric: true, sensitivity: "base" })
  },
})

// компоненты на всех страницах
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({ links: {} }),
}

// страницы вики
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ConditionalRender({
      component: Component.Breadcrumbs({ rootName: "Главная" }),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TagList(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        { Component: Component.Search(), grow: true },
        { Component: Component.Darkmode() },
        { Component: Component.ReaderMode() },
      ],
    }),
    explorer,
  ],
  right: [
    Component.Graph(),
    Component.DesktopOnly(Component.TableOfContents()),
    Component.Backlinks(),
  ],
}

// страницы-списки (папки, теги)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [
    Component.Breadcrumbs({ rootName: "Главная" }),
    Component.ArticleTitle(),
    Component.ContentMeta(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        { Component: Component.Search(), grow: true },
        { Component: Component.Darkmode() },
        { Component: Component.ReaderMode() },
      ],
    }),
    explorer,
  ],
  // у разделов (index.md) тоже есть граф, оглавление и обратные ссылки
  right: [
    Component.Graph(),
    Component.DesktopOnly(Component.TableOfContents()),
    Component.Backlinks(),
  ],
}
