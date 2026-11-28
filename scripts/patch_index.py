#!/usr/bin/env python3
"""Restore and patch index.html from known-good base commit."""
from pathlib import Path
import urllib.request

BASE = "https://raw.githubusercontent.com/forestplus/TopDevOps/b2c150efeb1f25f0db8d37d1a82f6b111a2208ba/index.html"

print("Downloading base index...")
urllib.request.urlretrieve(BASE, "index.html")
html = Path("index.html").read_text(encoding="utf-8")
print("base size", len(html))

html = html.replace("og-image.png?v=20261125", "og-image.png?v=20261128")
html = html.replace('dateModified": "2026-11-11"', 'dateModified": "2026-11-28"')

css_add = """
        /* profile photo */
        .about-layout { display: grid; grid-template-columns: 200px 1fr; gap: 2.5rem; align-items: start; }
        .about-photo-wrap { position: relative; width: 180px; margin: 0 auto; }
        .about-photo {
            width: 180px; height: 180px; border-radius: 50%;
            object-fit: cover; display: block;
            border: 2px solid rgba(0,212,255,0.35);
            box-shadow: 0 0 0 6px rgba(0,212,255,0.08), 0 12px 40px rgba(0,0,0,0.45);
        }
        .about-photo-ring {
            position: absolute; inset: -6px; border-radius: 50%;
            border: 1px dashed rgba(0,212,255,0.25); pointer-events: none;
            animation: spinSlow 28s linear infinite;
        }
        @keyframes spinSlow { to { transform: rotate(360deg); } }
        @media (prefers-reduced-motion: reduce) { .about-photo-ring { animation: none; } }
        .about-photo-caption {
            text-align: center; margin-top: 0.85rem;
            font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
            color: var(--text-muted); letter-spacing: 0.04em;
        }
        @media (max-width: 720px) {
            .about-layout { grid-template-columns: 1fr; justify-items: center; text-align: center; }
            .about-text { text-align: left; }
        }
        .notes-search-wrap { max-width: 520px; margin: 0 auto 1.6rem; position: relative; }
        .notes-search {
            width: 100%; padding: 0.85rem 1.1rem 0.85rem 2.7rem;
            border-radius: 12px; border: 1px solid var(--border);
            background: rgba(15,15,26,0.85); color: var(--text-primary);
            font-size: 0.95rem; font-family: inherit; outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        .notes-search::placeholder { color: var(--text-muted); }
        .notes-search:focus {
            border-color: var(--accent-cyan);
            box-shadow: 0 0 0 3px rgba(0,212,255,0.15);
        }
        .notes-search-icon {
            position: absolute; left: 0.95rem; top: 50%; transform: translateY(-50%);
            color: var(--accent-cyan); opacity: 0.7; pointer-events: none; font-size: 1rem;
        }
        .notes-search-clear {
            position: absolute; right: 0.7rem; top: 50%; transform: translateY(-50%);
            background: none; border: none; color: var(--text-muted); cursor: pointer;
            font-size: 1.1rem; padding: 0.2rem 0.4rem; display: none;
        }
        .notes-search-clear.visible { display: block; }
        .notes-search-clear:hover { color: var(--accent-cyan); }
        .notes-group.hidden-by-search { display: none !important; }
        .notes-list li.hidden-by-search { display: none !important; }
        .notes-empty {
            text-align: center; color: var(--text-muted); padding: 1.5rem;
            font-size: 0.9rem; display: none;
        }
        .notes-empty.visible { display: block; }
"""

marker = "        .section-subtitle { text-align: center; color: var(--text-secondary); margin-bottom: 3rem; font-size: 0.9rem; }"
if marker not in html:
    raise SystemExit("CSS marker missing")
html = html.replace(marker, marker + "\n" + css_add)

old_sub = (
    '        <p class="section-subtitle" data-ru="закрытые кейсы / case notes" '
    'data-en="closed cases / case notes">закрытые кейсы / case notes</p>\n'
    '        <div class="notes-controls">'
)
new_sub = (
    '        <div class="notes-search-wrap">\n'
    '            <span class="notes-search-icon" aria-hidden="true">&#8981;</span>\n'
    '            <input type="search" id="notes-search" class="notes-search"\n'
    '                   data-placeholder-ru="Поиск по заметкам…" data-placeholder-en="Search notes…"\n'
    '                   placeholder="Поиск по заметкам…" autocomplete="off" enterkeyhint="search">\n'
    '            <button type="button" class="notes-search-clear" id="notes-search-clear" aria-label="Очистить">×</button>\n'
    '        </div>\n'
    '        <p class="notes-empty" id="notes-empty" data-ru="Ничего не найдено" data-en="Nothing found">Ничего не найдено</p>\n'
    '        <div class="notes-controls">'
)
if old_sub not in html:
    raise SystemExit("subtitle marker missing")
html = html.replace(old_sub, new_sub)

old_about = '        <div class="about">\n            <div class="about-text fade-in">'
new_about = (
    '        <div class="about about-layout">\n'
    '            <div class="about-photo-wrap fade-in">\n'
    '                <div class="about-photo-ring" aria-hidden="true"></div>\n'
    '                <img class="about-photo" src="photo-avatar-240.png" width="180" height="180"\n'
    '                     alt="Дмитрий Парамонов" loading="lazy" decoding="async">\n'
    '                <p class="about-photo-caption">DevOps / SRE Team Lead</p>\n'
    '            </div>\n'
    '            <div class="about-text fade-in">'
)
if old_about not in html:
    raise SystemExit("about marker missing")
html = html.replace(old_about, new_about)

search_js = r"""
        // ========== NOTES SEARCH ==========
        (function initNotesSearch() {
            var input = document.getElementById('notes-search');
            var clearBtn = document.getElementById('notes-search-clear');
            var emptyEl = document.getElementById('notes-empty');
            var section = document.getElementById('notes');
            if (!input || !section) return;
            function applyLangPlaceholder() {
                var lang = (document.documentElement.lang || 'ru').slice(0,2);
                if (lang !== 'en') lang = 'ru';
                var ph = input.getAttribute('data-placeholder-' + lang) || 'Search…';
                input.setAttribute('placeholder', ph);
            }
            applyLangPlaceholder();
            document.addEventListener('langchange', applyLangPlaceholder);
            function filter() {
                var q = (input.value || '').trim().toLowerCase();
                clearBtn.classList.toggle('visible', q.length > 0);
                var groups = section.querySelectorAll('.notes-group');
                var anyVisible = false;
                groups.forEach(function(group) {
                    var links = group.querySelectorAll('.notes-list a');
                    var groupVisible = false;
                    links.forEach(function(a) {
                        var li = a.closest('li');
                        var text = ((a.textContent || '') + ' ' + (a.getAttribute('data-ru')||'') + ' ' + (a.getAttribute('data-en')||'')).toLowerCase();
                        var titleEl = group.querySelector('.notes-toggle-label') || group.querySelector('.notes-group-title');
                        var title = (titleEl && titleEl.textContent) || '';
                        text += ' ' + title.toLowerCase();
                        var match = !q || text.indexOf(q) !== -1;
                        if (li) li.classList.toggle('hidden-by-search', !match);
                        if (match) groupVisible = true;
                    });
                    group.classList.toggle('hidden-by-search', !groupVisible);
                    if (groupVisible) {
                        anyVisible = true;
                        if (q && !group.classList.contains('open')) {
                            var btn = group.querySelector('.notes-toggle');
                            if (btn && btn.getAttribute('aria-expanded') === 'false') btn.click();
                        }
                    }
                });
                if (emptyEl) emptyEl.classList.toggle('visible', q && !anyVisible);
            }
            input.addEventListener('input', filter);
            input.addEventListener('search', filter);
            if (clearBtn) clearBtn.addEventListener('click', function() {
                input.value = '';
                filter();
                input.focus();
            });
        })();
"""
marker_js = '        // ========== SCROLL PROGRESS =========='
if marker_js not in html:
    raise SystemExit("JS marker missing")
html = html.replace(marker_js, search_js + "\n" + marker_js)

Path("index.html").write_text(html, encoding="utf-8")
assert "notes-search" in html
assert "photo-avatar-240.png" in html
print("patched OK", len(html))
