#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mobile about readability, black-screen reduce, notes same-window + home for all dirs."""
from pathlib import Path
import re

ROOT = Path('.')
idx_path = ROOT / 'index.html'
t = idx_path.read_text(encoding='utf-8')

about_mobile_css = """
        /* about mobile readability */
        .about-text h3 {
            margin-top: 1.6rem;
            margin-bottom: 0.85rem;
            letter-spacing: 0.04em;
            line-height: 1.35;
            color: var(--text-primary);
            font-size: 0.95rem;
        }
        .about-text h3:first-child { margin-top: 0.35rem; }
        .about-text h4 {
            margin-top: 1.25rem;
            margin-bottom: 0.55rem;
            color: var(--accent-cyan);
            font-size: 0.95rem;
        }
        .about-text p {
            text-align: left;
            text-indent: 0;
            margin: 0 0 0.85rem;
            line-height: 1.7;
            word-spacing: normal;
            hyphens: auto;
            -webkit-hyphens: auto;
        }
        .about-text ul {
            margin: 0.4rem 0 1rem 1.1rem;
            padding: 0;
        }
        .about-text li {
            margin: 0.4rem 0;
            line-height: 1.55;
            text-align: left;
        }
        @media (max-width: 720px) {
            .about-layout {
                grid-template-columns: 1fr;
                gap: 1.4rem;
                justify-items: stretch;
            }
            .about-text {
                padding: 1.35rem 1.15rem 1.5rem;
                font-size: 0.95rem;
                line-height: 1.7;
                border-radius: 14px;
                width: 100%;
                max-width: 100%;
            }
            .about-text p {
                text-align: left;
                text-indent: 0;
                text-align-last: left;
                word-break: normal;
                overflow-wrap: break-word;
            }
            .about-text h3 {
                margin-top: 1.45rem;
                margin-bottom: 0.75rem;
                font-size: 0.88rem;
                text-align: left;
                letter-spacing: 0.06em;
            }
            .about-text h3:first-child { margin-top: 0.15rem; }
            .about-text::before,
            .about-text::after {
                display: none;
            }
            .about-photo-wrap { margin-bottom: 0.25rem; }
        }
"""

if '/* about mobile readability */' not in t:
    marker = "        .pillars { display: grid;"
    if marker not in t:
        raise SystemExit('pillars marker missing')
    t = t.replace(marker, about_mobile_css + "\n" + marker, 1)

t = t.replace(
    '.about-text p { text-align: justify; text-indent: 2ch; }',
    '.about-text p { text-align: left; text-indent: 0; margin: 0 0 0.85rem; line-height: 1.75; }'
)

old_fade = """        .fade-in {
            opacity: 0;
            transform: translateY(24px);
            transition:
                opacity 0.75s var(--ease-out-expo),
                transform 0.75s var(--ease-out-expo),
                filter 0.75s var(--ease-out-expo);
            filter: blur(4px);
            will-change: opacity, transform;
        }"""
new_fade = """        .fade-in {
            opacity: 0.001;
            transform: translateY(16px);
            transition:
                opacity 0.55s var(--ease-out-expo),
                transform 0.55s var(--ease-out-expo);
            will-change: opacity, transform;
        }
        .hero .fade-in,
        #about .about-photo-wrap.fade-in,
        #about .about-text.fade-in {
            opacity: 1;
            transform: none;
        }"""
if old_fade in t:
    t = t.replace(old_fade, new_fade)
elif '/* first-screen no black flash */' not in t:
    t = re.sub(
        r'\.fade-in\s*\{\s*opacity:\s*0;',
        '.fade-in { opacity: 0.001;',
        t,
        count=1,
    )
    if '#about .about-text.fade-in' not in t:
        t = t.replace(
            '.fade-in.visible {',
            '''.hero .fade-in,
        #about .about-photo-wrap.fade-in,
        #about .about-text.fade-in {
            opacity: 1;
            transform: none;
            filter: none;
        }
        .fade-in.visible {''',
            1,
        )

needle = 'if (reduceMotion) drawFrame();\n        else startParticles();'
if needle in t and 'mobile-particles-guard' not in t:
    t = t.replace(
        needle,
        """/* mobile-particles-guard */
        const isCoarse = window.matchMedia('(pointer: coarse)').matches
            || window.matchMedia('(max-width: 720px)').matches;
        if (reduceMotion) drawFrame();
        else if (isCoarse) {
            drawFrame();
        } else startParticles();"""
    )

idx_path.write_text(t, encoding='utf-8')
print('index patched')

t = idx_path.read_text(encoding='utf-8')
before = t.count('target="_blank"')
t = re.sub(
    r'(href="(?!https?:)[^"]+\.html")\s+target="_blank"\s+rel="noopener"',
    r'\1',
    t,
)
idx_path.write_text(t, encoding='utf-8')
print('stripped target blanks', before - t.count('target="_blank"'))

skip = {'.git', '.github', 'assets', 'build', 'backups', 'archive', 'node_modules', 'scripts', 'kimi'}
n = 0
for folder in ROOT.iterdir():
    if not folder.is_dir() or folder.name in skip:
        continue
    for html in folder.rglob('*.html'):
        try:
            content = html.read_text(encoding='utf-8')
        except Exception:
            continue
        if 'notes-topnav' not in content and 'notes.css' not in content:
            continue
        orig = content
        if 'class="nav-home"' not in content and 'notes-topnav-links' in content:
            content = content.replace(
                '<div class="notes-topnav-links">',
                '<div class="notes-topnav-links">\n    <a class="nav-home" href="/">← На главную</a>',
                1,
            )
        content = re.sub(
            r'(<a class="brand" href=")[^"]*(")',
            r'\1/\2',
            content,
            count=1,
        )
        if content != orig:
            html.write_text(content, encoding='utf-8')
            n += 1
print('note pages with home nav', n)
