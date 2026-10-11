#!/usr/bin/env node
// Подготовка сборки сайта: одинаково для локальной машины и CI.
//
//   node site/prepare.mjs
//
// 1. Клонирует Quartz v4 на закреплённый коммит в site/.work/quartz и ставит зависимости.
// 2. Накладывает конфиг из site/ (quartz.config.ts, quartz.layout.ts, styles/, patches).
// 3. Собирает content/ из ru/ и assets/ с сохранением путей; ru/index.md становится
//    корневой страницей; ссылки на неопубликованные файлы (sources/, CLAUDE.md…)
//    превращаются в обычный текст; пишет robots.txt.
//
// Содержимое вики (ru/, assets/, …) не изменяется: все правки делаются в копии.

import { execFileSync } from "node:child_process"
import fs from "node:fs"
import path from "node:path"
import { fileURLToPath, pathToFileURL } from "node:url"

// ---- закреплённая версия Quartz ------------------------------------------------------
// ветка v4 (официальная линия Quartz 4), коммит после тега v4.5.2: исправления SPA-навигации,
// проводника и зависимостей. v5.0.0 существует, но не используется. Менять осознанно.
export const QUARTZ_REPO = "https://github.com/jackyzha0/quartz.git"
export const QUARTZ_COMMIT = "d25a6eabf96751ffca56f8a8139272def7a65041"

const SITE_DIR = path.dirname(fileURLToPath(import.meta.url))
const REPO_ROOT = path.resolve(SITE_DIR, "..")
const WORK_DIR = path.resolve(process.env.SITE_WORK_DIR ?? path.join(SITE_DIR, ".work"))
const QUARTZ_DIR = path.join(WORK_DIR, "quartz")
const CONTENT_DIR = path.join(QUARTZ_DIR, "content")

// что публикуется: репозиторный путь -> то же имя внутри content/
const PUBLISHED_ROOTS = ["ru", "assets"]
// ru/index.md становится главной страницей сайта
const MOVED = new Map([["ru/index.md", "index.md"]])
const SKIP_FILE = (name) => name.startsWith(".") || name.endsWith(".meta.yaml")

const log = (...a) => console.log("[prepare]", ...a)
const run = (cmd, args, cwd) => execFileSync(cmd, args, { cwd, stdio: "inherit" })
const out = (cmd, args, cwd) => execFileSync(cmd, args, { cwd, encoding: "utf8" }).trim()

// ---- 1. клон Quartz ------------------------------------------------------------------
function ensureQuartz() {
  fs.mkdirSync(WORK_DIR, { recursive: true })
  const hasGit = fs.existsSync(path.join(QUARTZ_DIR, ".git"))
  let head = ""
  if (hasGit) {
    try {
      head = out("git", ["rev-parse", "HEAD"], QUARTZ_DIR)
    } catch {}
  }
  if (head !== QUARTZ_COMMIT) {
    log(`Quartz: fetch ${QUARTZ_COMMIT.slice(0, 10)}`)
    if (!hasGit) {
      fs.mkdirSync(QUARTZ_DIR, { recursive: true })
      run("git", ["init", "--quiet"], QUARTZ_DIR)
      run("git", ["remote", "add", "origin", QUARTZ_REPO], QUARTZ_DIR)
    }
    run("git", ["fetch", "--quiet", "--depth", "1", "origin", QUARTZ_COMMIT], QUARTZ_DIR)
    run("git", ["checkout", "--quiet", "--force", QUARTZ_COMMIT], QUARTZ_DIR)
  } else {
    log(`Quartz: уже на ${QUARTZ_COMMIT.slice(0, 10)}`)
  }

  const lock = path.join(QUARTZ_DIR, "package-lock.json")
  const stamp = path.join(QUARTZ_DIR, "node_modules", ".installed-commit")
  const installed = fs.existsSync(stamp) ? fs.readFileSync(stamp, "utf8").trim() : ""
  if (installed !== QUARTZ_COMMIT || !fs.existsSync(lock)) {
    log("npm ci")
    run("npm", ["ci", "--no-audit", "--no-fund"], QUARTZ_DIR)
    fs.writeFileSync(stamp, QUARTZ_COMMIT + "\n")
  }
}

// ---- 2. наложение конфига --------------------------------------------------------------
async function overlay() {
  const files = [
    ["quartz.config.ts", "quartz.config.ts"],
    ["quartz.layout.ts", "quartz.layout.ts"],
    ["styles/custom.scss", "quartz/styles/custom.scss"],
  ]
  for (const [from, to] of files) {
    fs.copyFileSync(path.join(SITE_DIR, from), path.join(QUARTZ_DIR, to))
  }
  // свои компоненты: site/components/*.tsx -> quartz/components/, стили рядом лежат в styles/
  const compDir = path.join(SITE_DIR, "components")
  if (fs.existsSync(compDir)) {
    for (const f of fs.readdirSync(compDir)) {
      fs.copyFileSync(path.join(compDir, f), path.join(QUARTZ_DIR, "quartz/components", f))
    }
  }
  // картинка превью ссылок (og:image) и прочая статика: site/static/* -> quartz/static/
  const staticDir = path.join(SITE_DIR, "static")
  if (fs.existsSync(staticDir)) {
    for (const f of fs.readdirSync(staticDir)) {
      fs.copyFileSync(path.join(staticDir, f), path.join(QUARTZ_DIR, "quartz/static", f))
    }
  }
  await applyPatches()
}

// точечные правки исходников Quartz: строка-якорь обязана найтись, иначе падаем громко
async function applyPatches() {
  const patchDir = path.join(SITE_DIR, "patches")
  if (!fs.existsSync(patchDir)) return
  for (const f of fs.readdirSync(patchDir).filter((n) => n.endsWith(".mjs")).sort()) {
    const { target, edits } = await import(pathToFileURL(path.join(patchDir, f)).href)
    const file = path.join(QUARTZ_DIR, target)
    // всегда от чистого файла: сбрасываем к закреплённому коммиту
    run("git", ["checkout", "--quiet", "--", target], QUARTZ_DIR)
    let src = fs.readFileSync(file, "utf8")
    for (const { find, replace } of edits) {
      if (!src.includes(find)) {
        throw new Error(`patch ${f}: якорь не найден в ${target}:\n${find.slice(0, 200)}`)
      }
      src = src.replace(find, () => replace)
    }
    fs.writeFileSync(file, src)
    log(`patch ${f} -> ${target}`)
  }
}

// ---- 3. content/ -----------------------------------------------------------------------
function listFiles(dir, base = dir) {
  const res = []
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (SKIP_FILE(e.name)) continue
    const p = path.join(dir, e.name)
    if (e.isDirectory()) res.push(...listFiles(p, base))
    else if (e.isFile()) res.push(path.relative(base, p).split(path.sep).join("/"))
  }
  return res
}

const FENCE = /^\s*(```|~~~)/
const LINK = /(!?)\[((?:[^\[\]]|\[[^\]]*\])*)\]\(([^()\s]+)((?:\s+"[^"]*")?)\)/g

// Quartz сам выводит заголовок страницы из `title` шапки; ведущий `# Заголовок` в теле дублирует его.
// Для главной title берётся из H1 («Maya in Transit», а не «… — главная»).
function stripLeadingH1(text, titleFromH1) {
  const m = text.match(/^(---\r?\n[\s\S]*?\r?\n---\r?\n)(\s*)#[ \t]+([^\r\n]+)\r?\n(\s*)/)
  if (!m) return text
  let [whole, fm, , h1] = m
  if (titleFromH1) fm = fm.replace(/^title:.*$/m, () => `title: ${h1.trim()}`)
  return fm + "\n" + text.slice(whole.length)
}

function rewriteMarkdown(text, srcRepoPath, published, dirs, stats) {
  const contentPath = MOVED.get(srcRepoPath) ?? srcRepoPath
  const srcDir = path.posix.dirname(srcRepoPath)
  const newDir = path.posix.dirname(contentPath)
  const lines = stripLeadingH1(text, srcRepoPath === "ru/index.md").split("\n")
  let inFrontmatter = lines[0]?.trim() === "---"
  let fence = null

  const rewriteTarget = (isImage, label, rawTarget, title) => {
    if (/^([a-z][a-z0-9+.-]*:|#|\/|\?)/i.test(rawTarget)) return null
    const [pathPart, ...rest] = rawTarget.split("#")
    const anchor = rest.length ? "#" + rest.join("#") : ""
    let decoded = pathPart
    try {
      decoded = decodeURI(pathPart)
    } catch {}
    const repoTarget = path.posix.normalize(path.posix.join(srcDir, decoded))
    const insidePublished = PUBLISHED_ROOTS.some((r) => repoTarget === r || repoTarget.startsWith(r + "/"))

    if (!insidePublished) {
      // файл вне вики (sources/, CLAUDE.md, data/…): не публикуем, оставляем подпись
      stats.unlinked.set(repoTarget, (stats.unlinked.get(repoTarget) ?? 0) + 1)
      if (isImage) return null
      const tip = `Вне вики, не публикуется: ${repoTarget}`.replace(/"/g, "&quot;")
      return `<span class="source-ref" title="${tip}">${label}</span>`
    }

    const exists = published.has(repoTarget) || dirs.has(repoTarget.replace(/\/$/, ""))
    if (!exists) {
      stats.broken.push({ file: srcRepoPath, target: rawTarget })
      return null
    }
    const mapped = MOVED.get(repoTarget) ?? repoTarget
    let rel = path.posix.relative(newDir, mapped)
    if (rawTarget.endsWith("/") && !rel.endsWith("/")) rel += "/"
    if (rel === "") rel = "."
    // сохраняем исходное написание, если оно уже верное
    const original = path.posix.normalize(decoded)
    if (original === rel || decoded === rel) return null
    stats.rewritten++
    return `${isImage ? "!" : ""}[${label}](${rel}${anchor}${title})`
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    if (inFrontmatter) {
      if (i > 0 && line.trim() === "---") inFrontmatter = false
      continue
    }
    const fm = line.match(FENCE)
    if (fm) {
      if (!fence) fence = fm[1]
      else if (fm[1] === fence) fence = null
      continue
    }
    if (fence) continue
    // не трогаем инлайн-код: нечётные куски после split по `...`
    const parts = line.split(/(`[^`]*`)/)
    for (let k = 0; k < parts.length; k += 2) {
      parts[k] = parts[k].replace(LINK, (whole, bang, label, target, title) => {
        const r = rewriteTarget(bang === "!", label, target, title)
        return r ?? whole
      })
    }
    lines[i] = parts.join("")
  }
  return lines.join("\n")
}

function buildContent() {
  if (!CONTENT_DIR.startsWith(WORK_DIR + path.sep)) throw new Error("content вне рабочей папки")
  fs.rmSync(CONTENT_DIR, { recursive: true, force: true })
  fs.mkdirSync(CONTENT_DIR, { recursive: true })

  const published = new Set()
  const dirs = new Set()
  for (const root of PUBLISHED_ROOTS) {
    const abs = path.join(REPO_ROOT, root)
    if (!fs.existsSync(abs)) continue
    dirs.add(root)
    for (const f of listFiles(abs)) {
      const rp = `${root}/${f}`
      published.add(rp)
      for (let d = path.posix.dirname(rp); d !== "." && d !== ""; d = path.posix.dirname(d)) dirs.add(d)
    }
  }

  const stats = { unlinked: new Map(), broken: [], rewritten: 0, pages: 0, files: 0 }
  for (const rp of [...published].sort()) {
    const dest = path.join(CONTENT_DIR, MOVED.get(rp) ?? rp)
    fs.mkdirSync(path.dirname(dest), { recursive: true })
    const src = path.join(REPO_ROOT, rp)
    if (rp.endsWith(".md")) {
      const text = fs.readFileSync(src, "utf8")
      fs.writeFileSync(dest, rewriteMarkdown(text, rp, published, dirs, stats))
      stats.pages++
    } else {
      fs.copyFileSync(src, dest)
      stats.files++
    }
  }

  fs.writeFileSync(path.join(CONTENT_DIR, "robots.txt"), "User-agent: *\nDisallow: /\n")

  log(`content: ${stats.pages} страниц, ${stats.files} файлов; ссылок пересчитано ${stats.rewritten}`)
  const unl = [...stats.unlinked.entries()]
  log(`ссылок на неопубликованное (стали текстом): ${unl.reduce((s, [, n]) => s + n, 0)} в ${unl.length} файлов`)
  for (const [t, n] of unl) log(`   ${t} x${n}`)
  log(`ссылок на ещё не созданные страницы (оставлены): ${stats.broken.length}`)
  for (const b of stats.broken) log(`   ${b.file} -> ${b.target}`)
  fs.writeFileSync(
    path.join(WORK_DIR, "prepare-report.json"),
    JSON.stringify({ unlinked: Object.fromEntries(unl), broken: stats.broken }, null, 2),
  )
}

if (!fs.existsSync(path.join(REPO_ROOT, "ru"))) throw new Error("не найден ru/ — запускайте из репозитория вики")
ensureQuartz()
await overlay()
buildContent()
log(`готово. Дальше: cd ${path.relative(process.cwd(), QUARTZ_DIR) || "."} && npx quartz build`)
