#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix notes navigation UX: TOC layout, same-window links, expand spacing, home CTA."""
from pathlib import Path
import re

ROOT = Path('.')

# --- index.html ---
idx = ROOT / 'index.html'
if idx.exists():
    t = idx.read_text(encoding='utf-8')
    # Fix expand-all stuck to search: remove negative margin
    t2 = t.replace(
        '.notes-controls { max-width: 900px; margin: -1.8rem auto 1.1rem; display: flex; justify-content: flex-end; }',
        '.notes-controls { max-width: 900px; margin: 0.35rem auto 1.25rem; display: flex; justify-content: flex-end; }'
    )
    if t2 == t:
        t2 = re.sub(
            r'\.notes-controls\s*\{[^}]*margin:\s*-1\.8rem[^;]*;',
            '.notes-controls { max-width: 900px; margin: 0.35rem auto 1.25rem;',
            t,
            count=1,
        )
    t = t2
    # notes links: open in same window
    t = re.sub(
        r'(href="(?:ai-ml|docker|k8s|linux|git|devops|microservices|windows|network|python|security|monitoring)/[^"]+\.html")\s+target="_blank"\s+rel="noopener"',
        r'\1',
        t,
    )
    idx.write_text(t, encoding='utf-8')
    print('index.html updated')
else:
    print('no index.html')

# --- note pages: ensure home nav is prominent ---
note_dirs = ['ai-ml', 'docker', 'k8s', 'linux', 'git', 'devops', 'microservices', 'windows', 'network', 'python', 'security', 'monitoring']
n_pages = 0
for d in note_dirs:
    folder = ROOT / d
    if not folder.is_dir():
        continue
    for html in folder.glob('*.html'):
        t = html.read_text(encoding='utf-8')
        orig = t
        if 'class="nav-home"' not in t and 'notes-topnav-links' in t:
            t = t.replace(
                '<div class="notes-topnav-links">',
                '<div class="notes-topnav-links">\n    <a class="nav-home" href="/">← На главную</a>',
                1,
            )
        t = re.sub(
            r'(<div class="topbar"><a href="\.\./">)← TopDevOps(</a>)',
            r'\1← На главную\2',
            t,
        )
        t = re.sub(
            r'(<a class="back" href="\.\./">)← На главную TopDevOps(</a>)',
            r'\1← На главную\2',
            t,
        )
        t = re.sub(
            r'(<a class="back" href="/">)← На главную TopDevOps(</a>)',
            r'\1← На главную\2',
            t,
        )
        if t != orig:
            html.write_text(t, encoding='utf-8')
            n_pages += 1
print('note pages patched', n_pages)
