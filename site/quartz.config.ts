import { h } from "preact"
import { QuartzConfig } from "./quartz/cfg"
import { QuartzTransformerPlugin } from "./quartz/plugins/types"
import * as Plugin from "./quartz/plugins"

/**
 * Конфиг сайта «Maya in Transit» (Quartz v4). Накладывается скриптом site/prepare.mjs.
 * Справка: https://quartz.jzhao.xyz/configuration
 */

// Закрытый от индексации сайт: <meta name="robots"> в <head> каждой страницы (включая 404).
const NoIndex: QuartzTransformerPlugin = () => ({
  name: "NoIndex",
  externalResources: () => ({
    additionalHead: [h("meta", { name: "robots", content: "noindex, nofollow" })],
  }),
})

const config: QuartzConfig = {
  configuration: {
    pageTitle: "Maya in Transit",
    pageTitleSuffix: "",
    enableSPA: true,
    enablePopovers: true,
    analytics: null,
    locale: "ru-RU",
    baseUrl: "yunoshev.github.io/may-in-transit",
    ignorePatterns: ["private", "templates", ".obsidian"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      // шрифты с кириллицей
      typography: {
        header: "Inter",
        body: "Inter",
        code: "JetBrains Mono",
      },
      // палитра Obsidian: нейтральный фон, фиолетовый акцент
      colors: {
        lightMode: {
          light: "#ffffff",
          lightgray: "#e3e3e3",
          gray: "#b4b4b4",
          darkgray: "#4f4f55",
          dark: "#222222",
          secondary: "#705dcf",
          tertiary: "#8875ff",
          highlight: "rgba(136, 117, 255, 0.12)",
          textHighlight: "#fff23688",
        },
        darkMode: {
          light: "#1e1e1e",
          lightgray: "#363636",
          gray: "#6a6a6a",
          darkgray: "#c4c4c8",
          dark: "#dadada",
          secondary: "#a78bfa",
          tertiary: "#8875ff",
          highlight: "rgba(136, 117, 255, 0.15)",
          textHighlight: "#b3aa0288",
        },
      },
    },
  },
  plugins: {
    transformers: [
      NoIndex(),
      Plugin.FrontMatter(),
      // даты не показываем: в рабочей копии content/ они бессмысленны (время сборки)
      Plugin.SyntaxHighlighting({
        theme: { light: "github-light", dark: "github-dark" },
        keepBackground: false,
      }),
      // callout'ы Obsidian, Mermaid; сырой HTML (<span data-canon>) проходит штатно
      Plugin.ObsidianFlavoredMarkdown({
        callouts: true,
        mermaid: true,
        enableInHtmlEmbed: false,
        parseTags: false,
        parseArrows: false,
      }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      // ссылки в вики относительные: `../30-ship/x.md`, `../../assets/ship/x.svg`
      Plugin.CrawlLinks({ markdownLinkResolution: "relative" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      // AliasRedirects сознательно выключен: aliases в шапках — поисковые синонимы для Obsidian
      // («SLEEP / MED / SAFE», «укрытие»…), а не адреса; редиректы с ними дали бы мусорные файлы.
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      // contentIndex нужен поиску, графу и проводнику; sitemap/RSS закрытому сайту не нужны
      Plugin.ContentIndex({ enableSiteMap: false, enableRSS: false }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
    ],
  },
}

export default config
