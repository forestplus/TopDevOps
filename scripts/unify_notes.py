#!/usr/bin/env python3
"""Rewrite all knowledge-base HTML pages to use shared dark theme + sticky nav."""
from pathlib import Path
import re

ROOT = Path(".")
SKIP_PREFIXES = ("new/", "archive/", "backups/", "kimi/", "v4/", "build/", "scripts/")
SKIP_NAMES = {"index.html", "404.html", "CV_ParamonovD.html", "hh5.html",
              "resume_slides_en.html"}

NAV = '''<nav class="notes-topnav" aria-label="Site">
  <a class="brand" href="/">dmitriy@devops<span>~</span></a>
  <div class="notes-topnav-links">
    <a href="/#about">Обо мне</a>
    <a href="/#experience">Опыт</a>
    <a href="/#notes">Заметки</a>
    <a href="/#contacts">Контакты</a>
    <a href="/resume.pdf">Резюме</a>
  </div>
</nav>
'''

FOOTER = '''<div class="notes-footer">
  <a href="/#notes">← Все заметки</a> ·
  <a href="/">topdevops.pro</a> ·
  Дмитрий Парамонов
</div>
'''

STYLE_RE = re.compile(r"<style\b[^>]*>.*?</style>", re.I | re.S)
BODY_OPEN_RE = re.compile(r"<body\b[^>]*>", re.I)


def should_process(path: Path) -> bool:
    rel = path.as_posix()
    if not rel.endswith(".html"):
        return False
    if path.name in SKIP_NAMES:
        return False
    if "/" not in rel:
        return False
    if any(rel.startswith(p) for p in SKIP_PREFIXES):
        return False
    return True


def transform(html: str, rel: str) -> str:
    html2, n = STYLE_RE.subn("", html, count=1)

    if "assets/notes.css" not in html2:
        depth = rel.count("/")
        rel_css = "../" * depth + "assets/notes.css"
        link = f'<link rel="stylesheet" href="{rel_css}">\n'
        if "</head>" in html2:
            html2 = html2.replace("</head>", link + "</head>", 1)
        else:
            html2 = link + html2

    if "notes-topnav" not in html2:
        m = BODY_OPEN_RE.search(html2)
        if m:
            html2 = html2[: m.end()] + "\n" + NAV + html2[m.end() :]

    if "notes-footer" not in html2:
        if "</div>\n\n</body>" in html2:
            html2 = html2.replace("</div>\n\n</body>", FOOTER + "</div>\n\n</body>", 1)
        elif "</body>" in html2:
            html2 = html2.replace("</body>", FOOTER + "\n</body>", 1)

    html2 = re.sub(
        r"(<body[^>]*)\s+style=\"[^\"]*\"",
        r"\1",
        html2,
        count=1,
        flags=re.I,
    )

    if 'name="theme-color"' not in html2:
        html2 = html2.replace(
            "</head>",
            '<meta name="theme-color" content="#050508">\n</head>',
            1,
        )

    return html2


def main() -> None:
    files = sorted(p for p in ROOT.rglob("*.html") if should_process(p))
    print(f"candidates: {len(files)}")
    changed = 0
    for p in files:
        rel = p.as_posix()
        original = p.read_text(encoding="utf-8", errors="replace")
        updated = transform(original, rel)
        if updated != original:
            p.write_text(updated, encoding="utf-8")
            changed += 1
            print("updated", rel)
        else:
            print("skip", rel)
    print(f"done: {changed}/{len(files)} updated")


if __name__ == "__main__":
    main()
