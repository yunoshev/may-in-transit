// Поиск Quartz по-русски. Штатный кодировщик режет текст только по пробелам и ищет по префиксу,
// поэтому «окно» не находит «окна», «окне», а токены вроде «стазис,» и «(отсек)» не совпадают
// с запросом. Патч: убираем знаки препинания по краям слов, ё -> е и грубо отбрасываем
// русские окончания (стемминг по суффиксам). Кодировщик общий для индекса и запроса.
// Подсветка результатов использует ту же нормализацию.
export const target = "quartz/components/scripts/search.inline.ts"

const RU = String.raw`
// ---- русская морфология (патч site/patches/01-search-russian.mjs) ----
const ruEndings = [
  "иями", "ями", "ами", "ией", "иях", "иям", "ого", "его", "ому", "ему", "ыми", "ими",
  "ее", "ие", "ые", "ое", "ей", "ий", "ый", "ой", "ем", "им", "ым", "ом", "их", "ых", "ую", "юю",
  "ая", "яя", "ою", "ею", "ов", "ев", "ах", "ях", "ам", "ям", "ии", "ия", "ию", "ью", "ья", "ье",
  "ы", "и", "а", "я", "у", "ю", "е", "о",
].sort((a, b) => b.length - a.length)

const ruStem = (word: string): string => {
  if (!/[а-я]/.test(word) || word.length < 4) return word
  let w = word
  for (const e of ruEndings) {
    if (w.endsWith(e) && w.length - e.length >= 3) {
      w = w.slice(0, -e.length)
      break
    }
  }
  if (w.length > 3 && /[ьй]$/.test(w)) w = w.slice(0, -1)
  return w
}

const encoder = (str: string): string[] => {
  const out: string[] = []
  for (const raw of baseEncoder(str)) {
    const tok = raw.replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}]+$/gu, "").replace(/ё/g, "е")
    if (tok) out.push(ruStem(tok))
  }
  return out
}

// слово текста подходит под запрос, если основа слова начинается с основы одного из терминов
const stemMatch = (tok: string, terms: string[]): boolean => {
  const toks = encoder(tok)
  return terms.some((term) => encoder(term).some((q) => toks.some((t) => t.startsWith(q))))
}

// регулярное выражение подсветки: для русских терминов — основа + любое окончание
const highlightRegex = (term: string): RegExp => {
  const t = term.toLowerCase()
  const stem = /[а-яё]/.test(t) ? encoder(t)[0] : undefined
  if (!stem) return new RegExp(t, "gi")
  const body = stem.replace(/[.*+?^$()|[\]\\{}]/g, "\\$&").replace(/е/g, "[её]")
  return new RegExp("(?<![\\p{L}\\p{N}])" + body + "[\\p{L}\\p{N}]*", "giu")
}

`

export const edits = [
  {
    find: "const encoder = (str: string): string[] => {",
    replace: "const baseEncoder = (str: string): string[] => {",
  },
  {
    find: "let index = new FlexSearch.Document<Item>({",
    replace: RU + "let index = new FlexSearch.Document<Item>({",
  },
  // подбор окна-фрагмента вокруг совпадения
  {
    find: "tokenizedTerms.some((term) => tok.toLowerCase().startsWith(term.toLowerCase()))",
    replace:
      "tokenizedTerms.some((term) => tok.toLowerCase().startsWith(term.toLowerCase())) ||\n      stemMatch(tok, tokenizedTerms)",
  },
  // подсветка слов в заголовке и фрагменте
  {
    find: "      return tok\n    })\n    .join(\" \")",
    replace:
      "      if (stemMatch(tok, tokenizedTerms)) {\n        return tok.replace(/[\\p{L}\\p{N}]+/u, (m) => `<span class=\"highlight\">${m}</span>`)\n      }\n      return tok\n    })\n    .join(\" \")",
  },
  // подсветка в окне предпросмотра справа
  {
    find: "const regex = new RegExp(term.toLowerCase(), \"gi\")\n      const matches = nodeText.match(regex)",
    replace: "const regex = highlightRegex(term)\n      const matches = nodeText.match(regex)",
  },
]
