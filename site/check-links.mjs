#!/usr/bin/env node
// Проверка собранного сайта: внутренние ссылки, картинки, якоря. Запуск:
//   node site/check-links.mjs [папка-сборки]      по умолчанию site/.work/quartz/public
// Код выхода 1, если есть битые ссылки.
import fs from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"

const SITE_DIR = path.dirname(fileURLToPath(import.meta.url))
const PUBLIC = path.resolve(process.argv[2] ?? path.join(SITE_DIR, ".work/quartz/public"))
const ORIGIN = "http://site.test"
// на GitHub Pages сайт живёт в подпапке; абсолютные ссылки (404.html) начинаются с неё
const BASE_PATH = "/may-in-transit"

const files = []
;(function walk(d) {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    const p = path.join(d, e.name)
    e.isDirectory() ? walk(p) : files.push(p)
  }
})(PUBLIC)
const fileSet = new Set(files.map((f) => "/" + path.relative(PUBLIC, f).split(path.sep).join("/")))

function resolveOnDisk(urlPath) {
  const p = decodeURIComponent(urlPath)
  if (fileSet.has(p)) return p
  if (fileSet.has(p + ".html")) return p + ".html"
  const dir = p.endsWith("/") ? p : p + "/"
  if (fileSet.has(dir + "index.html")) return dir + "index.html"
  return null
}

const idCache = new Map()
function ids(file) {
  if (!idCache.has(file)) {
    const html = fs.readFileSync(path.join(PUBLIC, file), "utf8")
    const set = new Set()
    for (const m of html.matchAll(/\sid=("([^"]*)"|'([^']*)')/g)) set.add(m[2] ?? m[3])
    idCache.set(file, set)
  }
  return idCache.get(file)
}

const ATTR = /<(a|img|link|script|source|video|audio)\b[^>]*?\s(href|src)=("([^"]*)"|'([^']*)')/g
const broken = []
const missingAnchors = []
let total = 0
let pages = 0
for (const f of files.filter((x) => x.endsWith(".html"))) {
  pages++
  const rel = "/" + path.relative(PUBLIC, f).split(path.sep).join("/")
  // URL страницы без .html (так её открывает браузер на GitHub Pages)
  const pageUrl = ORIGIN + rel.replace(/\.html$/, "")
  const html = fs.readFileSync(f, "utf8")
  for (const m of html.matchAll(ATTR)) {
    const raw = (m[4] ?? m[5] ?? "").trim().replaceAll("&amp;", "&")
    if (!raw || /^(data:|mailto:|javascript:|tel:)/i.test(raw)) continue
    let u
    try {
      u = new URL(raw, pageUrl)
    } catch {
      broken.push({ page: rel, url: raw, why: "bad url" })
      continue
    }
    if (u.origin !== ORIGIN) continue // внешние не проверяем
    total++
    let pathname = u.pathname
    if (pathname === BASE_PATH) pathname = "/"
    else if (pathname.startsWith(BASE_PATH + "/")) pathname = pathname.slice(BASE_PATH.length)
    const target = resolveOnDisk(pathname)
    if (!target) {
      broken.push({ page: rel, url: raw, why: "нет файла " + pathname })
      continue
    }
    if (u.hash.length > 1 && target.endsWith(".html")) {
      const id = decodeURIComponent(u.hash.slice(1))
      if (!ids(target).has(id)) missingAnchors.push({ page: rel, url: raw, why: "нет якоря #" + id })
    }
  }
}

console.log(`страниц: ${pages}, внутренних ссылок/ресурсов проверено: ${total}`)
console.log(`битых: ${broken.length}; якорей не найдено: ${missingAnchors.length}`)
const group = (arr) => {
  const byTarget = new Map()
  for (const b of arr) {
    const k = b.why + "  <-  " + b.url
    byTarget.set(k, [...(byTarget.get(k) ?? []), b.page])
  }
  for (const [k, pgs] of byTarget) console.log(`  ${k}\n      из: ${pgs.slice(0, 4).join(", ")}${pgs.length > 4 ? ` (+${pgs.length - 4})` : ""}`)
}
group(broken)
group(missingAnchors)
process.exit(broken.length ? 1 : 0)
