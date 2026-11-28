#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Subtle modern motion polish for TopDevOps index.html — no visual overload."""
from pathlib import Path
import re

p = Path("index.html")
t = p.read_text(encoding="utf-8")
if len(t) < 5000:
    raise SystemExit("index too small")
if "/* motion-polish v1 */" in t:
    print("already polished")
    raise SystemExit(0)

MOTION_CSS = r"""
        /* motion-polish v1 — modern, restrained */
        :root {
            --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
            --ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);
            --ease-spring: cubic-bezier(0.34, 1.4, 0.64, 1);
        }

        /* Softer reveal */
        .fade-in {
            opacity: 0;
            transform: translateY(24px);
            transition:
                opacity 0.75s var(--ease-out-expo),
                transform 0.75s var(--ease-out-expo),
                filter 0.75s var(--ease-out-expo);
            filter: blur(4px);
            will-change: opacity, transform;
        }
        .fade-in.visible {
            opacity: 1;
            transform: translateY(0);
            filter: blur(0);
        }
        /* Stagger for stats row */
        .stats-grid .stat-card.fade-in:nth-child(1) { transition-delay: 0.02s; }
        .stats-grid .stat-card.fade-in:nth-child(2) { transition-delay: 0.1s; }
        .stats-grid .stat-card.fade-in:nth-child(3) { transition-delay: 0.18s; }
        .stats-grid .stat-card.fade-in:nth-child(4) { transition-delay: 0.26s; }

        /* Cards: modern lift */
        .stat-card {
            transition:
                transform 0.45s var(--ease-out-expo),
                border-color 0.35s ease,
                box-shadow 0.45s var(--ease-out-expo);
        }
        .stat-card:hover {
            transform: translateY(-6px) scale(1.01);
        }

        /* Skill chips — springy micro-interaction */
        .skill-item {
            transition:
                transform 0.4s var(--ease-out-expo),
                background 0.3s ease,
                border-color 0.3s ease,
                color 0.3s ease,
                box-shadow 0.4s var(--ease-out-expo);
        }
        .skill-item:hover {
            transform: translateY(-3px) scale(1.03);
        }

        /* Social icons */
        .social-icon {
            transition:
                transform 0.4s var(--ease-out-expo),
                color 0.3s ease,
                box-shadow 0.4s ease,
                border-color 0.3s ease;
        }
        .social-icon:hover {
            transform: translateY(-5px) scale(1.06);
        }

        /* CTA sheen — soft light sweep, not flashy */
        .contact-btn.resume {
            overflow: hidden;
        }
        .contact-btn.resume .resume-sheen {
            position: absolute;
            inset: 0;
            border-radius: inherit;
            pointer-events: none;
            background: linear-gradient(
                105deg,
                transparent 35%,
                rgba(255, 255, 255, 0.35) 50%,
                transparent 65%
            );
            background-size: 220% 100%;
            animation: resumeSheen 3.8s ease-in-out infinite;
            mix-blend-mode: soft-light;
            opacity: 0.85;
        }
        @keyframes resumeSheen {
            0% { background-position: 120% 0; }
            45%, 100% { background-position: -40% 0; }
        }

        /* Magnetic elements: GPU-friendly */
        .magnetic {
            transition: transform 0.15s var(--ease-out-quart);
            will-change: transform;
        }

        /* Section title: calm underline grow when visible */
        .section-title {
            position: relative;
        }
        .section-title::after {
            content: '';
            display: block;
            width: 48px;
            height: 2px;
            margin: 0.75rem auto 0;
            border-radius: 2px;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple));
            transform: scaleX(0);
            transform-origin: center;
            transition: transform 0.7s var(--ease-out-expo);
            opacity: 0.85;
        }
        .fade-in.visible .section-title::after,
        section:has(.fade-in.visible) .section-title::after,
        .section-title.is-inview::after {
            transform: scaleX(1);
        }

        /* Timeline items: slight lateral ease */
        .timeline-item.fade-in {
            transform: translateY(20px) translateX(-8px);
        }
        .timeline-item.fade-in.visible {
            transform: translateY(0) translateX(0);
        }

        /* Ops panel glass hover */
        .ops-panel {
            transition: box-shadow 0.5s var(--ease-out-expo), border-color 0.35s ease;
        }
        .ops-panel:hover {
            box-shadow:
                inset 0 1px 0 rgba(255, 255, 255, 0.09),
                0 0 48px rgba(0, 212, 255, 0.1);
        }

        /* Nav links — smoother underline */
        nav a::after {
            transition: width 0.35s var(--ease-out-expo);
        }

        /* Respect reduced motion */
        @media (prefers-reduced-motion: reduce) {
            .fade-in {
                opacity: 1 !important;
                transform: none !important;
                filter: none !important;
                transition: none !important;
            }
            .stat-card:hover,
            .skill-item:hover,
            .social-icon:hover {
                transform: none;
            }
            .contact-btn.resume .resume-sheen {
                animation: none;
                opacity: 0;
            }
            .magnetic {
                transition: none;
            }
            .section-title::after {
                transform: scaleX(1);
            }
        }
"""

# Inject CSS before last </style> in head
style_close = t.rfind("</style>")
if style_close < 0:
    raise SystemExit("no </style>")
t = t[:style_close] + "\n" + MOTION_CSS + "\n        " + t[style_close:]

# Add sheen span inside resume buttons if missing
if "resume-sheen" not in t:
    t = re.sub(
        r'(<a href="resume\.pdf" id="resume-btn(?:-hero)?" class="contact-btn resume magnetic"[^>]*>)',
        r'\1\n                    <span class="resume-sheen" aria-hidden="true"></span>',
        t,
    )

# Upgrade magnetic JS to smoothed lerp + rAF; keep existing block if present
OLD_MAG = """            document.querySelectorAll('.magnetic').forEach((el) => {
                const strength = el.classList.contains('resume') ? 0.18 : 0.3;
                el.addEventListener('mousemove', (e) => {
                    const rect = el.getBoundingClientRect();
                    const dx = (e.clientX - rect.left - rect.width / 2) * strength;
                    const dy = (e.clientY - rect.top - rect.height / 2) * strength;
                    el.style.transform = `translate(${dx}px, ${dy}px)`;
                });
                el.addEventListener('mouseleave', () => {
                    el.style.transform = '';
                });
            });"""

NEW_MAG = """            document.querySelectorAll('.magnetic').forEach((el) => {
                const strength = el.classList.contains('resume') ? 0.14 : 0.28;
                let tx = 0, ty = 0, cx = 0, cy = 0, raf = 0, active = false;
                const tick = () => {
                    cx += (tx - cx) * 0.18;
                    cy += (ty - cy) * 0.18;
                    el.style.transform = `translate(${cx.toFixed(2)}px, ${cy.toFixed(2)}px)`;
                    if (Math.abs(tx - cx) > 0.05 || Math.abs(ty - cy) > 0.05 || active) {
                        raf = requestAnimationFrame(tick);
                    } else {
                        raf = 0;
                        if (!active) el.style.transform = '';
                    }
                };
                el.addEventListener('mousemove', (e) => {
                    const rect = el.getBoundingClientRect();
                    tx = (e.clientX - rect.left - rect.width / 2) * strength;
                    ty = (e.clientY - rect.top - rect.height / 2) * strength;
                    active = true;
                    if (!raf) raf = requestAnimationFrame(tick);
                });
                el.addEventListener('mouseleave', () => {
                    tx = 0; ty = 0; active = false;
                    if (!raf) raf = requestAnimationFrame(tick);
                });
            });"""

if OLD_MAG in t:
    t = t.replace(OLD_MAG, NEW_MAG)
else:
    print("WARN: magnetic block not exact — skip JS magnetic upgrade")

# Section title inview helper near IntersectionObserver
IO_MARKER = "entry.target.classList.add('visible');"
IO_EXTRA = """entry.target.classList.add('visible');
                    entry.target.querySelectorAll('.section-title').forEach(st => st.classList.add('is-inview'));"""
if IO_MARKER in t and "is-inview" not in t.split("IntersectionObserver")[1][:800]:
    t = t.replace(IO_MARKER, IO_EXTRA, 1)

p.write_text(t, encoding="utf-8")
assert "motion-polish v1" in t
assert "resumeSheen" in t
print("OK", len(t))
