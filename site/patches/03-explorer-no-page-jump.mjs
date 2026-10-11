// При загрузке страницы проводник вызывал activeElement.scrollIntoView(), и вместе со списком
// прокручивалась вся страница (на длинных страницах она открывалась на 300–500 px ниже верха).
// Патч прокручивает только сам список проводника.
export const target = "quartz/components/scripts/explorer.inline.ts"

export const edits = [
  {
    find: 'activeElement.scrollIntoView({ behavior: "smooth" })',
    replace:
      "explorerUl.scrollTop += activeElement.getBoundingClientRect().top - explorerUl.getBoundingClientRect().top - explorerUl.clientHeight / 3",
  },
]
