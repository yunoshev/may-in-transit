// Текст страницы для поиска и описаний собирается через toString(tree) без пробелов между
// блоками: ячейки таблиц и пункты списков склеиваются («РазделЧто внутриМир 2050-х»), слова
// пропадают из поиска. Патч добавляет пробел после каждого блочного элемента.
export const target = "quartz/plugins/transformers/description.ts"

export const edits = [
  { find: 'import { toString } from "hast-util-to-string"\n', replace: "" },
  {
    find: "export const Description:",
    replace: `const BLOCK = new Set(["p", "li", "td", "th", "tr", "div", "br", "blockquote", "pre", "figcaption", "summary"])
const blockText = (node: any): string => {
  if (node.type === "text") return node.value
  if (!node.children) return ""
  const inner = node.children.map(blockText).join("")
  const isBlock = node.type === "element" && (BLOCK.has(node.tagName) || /^h[1-6]$/.test(node.tagName))
  return isBlock ? inner + " " : inner
}

export const Description:`,
  },
  {
    find: "let text = escapeHTML(toString(tree))",
    replace: "let text = escapeHTML(blockText(tree))",
  },
]
