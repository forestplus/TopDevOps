#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply resume CTA UI: view in browser + pulse animation."""
from pathlib import Path
import re

p = Path("index.html")
t = p.read_text(encoding="utf-8")
print("loaded", len(t))
if len(t) < 5000:
    raise SystemExit("index too small")

t = re.sub(
    r'(<a href="resume\.pdf" id="resume-btn(?:-hero)?" class="contact-btn resume magnetic") download>',
    r'\1 target="_blank" rel="noopener noreferrer">',
    t,
)
t = t.replace(
    'data-ru="Скачать резюме" data-en="Download resume">Скачать резюме',
    'data-ru="Посмотреть резюме (PDF)" data-en="View resume (PDF)">Посмотреть резюме (PDF)',
)
t = t.replace(
    '<span class="contact-icon">⬇</span>',
    (
        '<span class="contact-icon" aria-hidden="true">'
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
        '<polyline points="14 2 14 8 20 8"/>'
        '<line x1="12" y1="18" x2="12" y2="12"/>'
        '<line x1="9" y1="15" x2="15" y2="15"/>'
        "</svg></span>"
    ),
)

old_css = """        .contact-btn.resume {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple) 55%, var(--accent-pink));
            background-size: 200% 200%; color: #050508; border: none; border-radius: 50px;
            font-weight: 700; padding: 1.05rem 2.4rem; letter-spacing: 0.01em;
            box-shadow: 0 10px 34px -10px rgba(0,212,255,0.5);
            animation: resumeGlow 4s ease-in-out infinite, resumeGradient 6s ease infinite;
        }
        .contact-btn.resume:hover {
            transform: translateY(-4px) scale(1.035);
            box-shadow: 0 16px 44px -8px rgba(124,58,237,0.55);
            border-color: transparent;
        }
        .contact-btn.resume .contact-icon { display: inline-block; animation: resumeBounce 1.8s ease-in-out infinite; }
        @keyframes resumeGlow {
            0%, 100% { box-shadow: 0 10px 34px -10px rgba(0,212,255,0.5); }
            50% { box-shadow: 0 10px 40px -6px rgba(236,72,153,0.55); }
        }
        @keyframes resumeGradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
        @keyframes resumeBounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(3px); } }
        @media (prefers-reduced-motion: reduce) {
            .contact-btn.resume, .contact-btn.resume .contact-icon { animation: none; }
        }"""

new_css = """        .contact-btn.resume {
            background: linear-gradient(135deg, #00d4ff 0%, #7c3aed 45%, #ec4899 100%);
            background-size: 220% 220%; color: #050508; border: none; border-radius: 50px;
            font-weight: 700; padding: 1.1rem 2.5rem; letter-spacing: 0.02em;
            box-shadow: 0 0 0 0 rgba(0,212,255,0.45), 0 12px 36px -10px rgba(124,58,237,0.55);
            animation: resumePulse 2.2s ease-in-out infinite, resumeGradient 5s ease infinite;
            position: relative;
        }
        .contact-btn.resume::after {
            content: '';
            position: absolute; inset: -3px; border-radius: 52px;
            background: linear-gradient(135deg, rgba(0,212,255,0.55), rgba(236,72,153,0.45));
            z-index: -1; opacity: 0.65; filter: blur(10px);
            animation: resumeHalo 2.2s ease-in-out infinite;
        }
        .contact-btn.resume:hover {
            transform: translateY(-4px) scale(1.04);
            box-shadow: 0 0 0 4px rgba(0,212,255,0.25), 0 18px 48px -8px rgba(124,58,237,0.6);
            border-color: transparent;
            animation-play-state: paused;
        }
        .contact-btn.resume:hover::after { animation-play-state: paused; opacity: 0.9; }
        .contact-btn.resume .contact-icon {
            display: inline-flex; align-items: center; justify-content: center;
            animation: resumeIconPulse 2.2s ease-in-out infinite;
        }
        .contact-btn.resume .contact-icon svg { display: block; }
        @keyframes resumePulse {
            0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(0,212,255,0.4), 0 12px 36px -10px rgba(124,58,237,0.5); }
            50% { transform: scale(1.045); box-shadow: 0 0 0 10px rgba(0,212,255,0), 0 16px 42px -8px rgba(236,72,153,0.55); }
        }
        @keyframes resumeHalo {
            0%, 100% { opacity: 0.45; transform: scale(1); }
            50% { opacity: 0.85; transform: scale(1.04); }
        }
        @keyframes resumeGradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
        @keyframes resumeIconPulse { 0%, 100% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.12); opacity: 0.9; } }
        @media (prefers-reduced-motion: reduce) {
            .contact-btn.resume, .contact-btn.resume .contact-icon, .contact-btn.resume::after { animation: none; }
        }"""

if old_css not in t:
    raise SystemExit("css block not found")
t = t.replace(old_css, new_css)

p.write_text(t, encoding="utf-8")
assert "Посмотреть резюме" in t
assert "resumePulse" in t
assert 'resume magnetic" download' not in t
print("OK", len(t))
