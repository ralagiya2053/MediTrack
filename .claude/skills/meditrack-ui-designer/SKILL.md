---
name: meditrack-ui-designer
description: Designs and generates modern, calm, clinical UI for MediTrack, a personal health-journal web app built on Flask + Jinja2 + vanilla CSS (repo on GitHub). Produces clean, restrained pages and components — cards, forms, tables, dashboards, vitals panels, modal dialogs — with a clinical teal-and-coral palette, soft borders, generous whitespace, and medical Lucide icons. Use this skill whenever the user asks to design, build, create, redesign, improve, or style any MediTrack page, screen, section, or component — including phrasings like "design the X page", "create UI for X", "build a component for X", "make the X look better", "redesign X", or any request about MediTrack's frontend, layout, CSS, or visual polish — even when MediTrack isn't named explicitly if the conversation context is clearly about it.
disable-model-invocation: true
---

# MediTrack UI Designer

You are designing frontend UI for **MediTrack**, a personal health-journal web app. MediTrack is a Flask app with server-rendered Jinja2 templates, vanilla CSS, and a small amount of vanilla JS. The goal of this skill is to help you generate UI that feels like it belongs in a calm, credible health product — not a generic SaaS dashboard, not a fintech app with medical nouns pasted on, and not a React/Tailwind output that doesn't match the stack.

The tone of MediTrack is **clinical, restrained, and calm**. Users log symptoms and vitals; the app presents data without diagnosing, reassuring, or alarming. The UI must reflect that discipline. Nothing is flashy; nothing is playful; nothing shouts.

## What MediTrack's stack looks like

- **Backend:** Flask (`app.py`), SQLite via raw `sqlite3` (`database/db.py`)
- **Templates:** Jinja2 in `templates/` — `base.html`, `landing.html`, `login.html`, `register.html`, `terms.html`, `privacy.html`, `disclaimer.html`
- **Styles:** vanilla CSS in `static/css/style.css` — no Tailwind, no preprocessors, no CSS-in-JS
- **Scripts:** small vanilla JS in `static/js/main.js`
- **Icons:** Lucide, loaded via CDN in `base.html`, used as `<i data-lucide="icon-name">` and initialized with `lucide.createIcons()`
- **Port:** 5001

Generate output that fits this stack. Do not introduce React, Vue, Tailwind, Bootstrap, shadcn, or styled-components.

## Before you design: read what already exists

MediTrack already has a design system. Before generating anything new, read:

- `static/css/style.css` — the full token list and existing component classes
- `templates/base.html` — layout structure, nav, footer, block names
- `templates/landing.html` — reference for the visual tone (hero + vitals panel + features + CTA)
- `templates/terms.html` or any other `.legal-*` page — reference for long-form content pages
- `templates/login.html` — reference for auth-card patterns

The goal is *consistency*. MediTrack should feel like one coherent product. If you can't see the files, ask the user to paste `style.css` and one template before generating.

## Design tokens — always use these, never hardcode

These are the exact variables defined in `static/css/style.css`. Use them by name. Do not invent new values.

### Colors

| Variable | Purpose |
|---|---|
| `--ink` | Primary text and headings |
| `--ink-soft` | Body paragraphs |
| `--ink-muted` | Secondary metadata, labels |
| `--ink-faint` | Placeholder text, quiet meta |
| `--paper` | Page background |
| `--paper-warm` | Section band background (e.g. `.features`) |
| `--paper-card` | Card / surface background (white) |
| `--accent` | Primary clinical teal `#0f5c6b` — links, CTAs, active states |
| `--accent-light` | Soft teal wash for badges/callouts |
| `--accent-2` | Warm coral `#c96a4b` — secondary highlights only |
| `--accent-2-light` | Soft coral wash |
| `--ok` | Green for positive vitals / stable status |
| `--warn` | Amber for watch / moderate |
| `--danger` | Red for high / concerning |
| `--danger-light` | Soft red wash for errors |
| `--border` | Default border |
| `--border-soft` | Fainter divider (used between legal sections, list rows) |

### Typography

- **`--font-display`** — DM Serif Display. Use for: page titles (`h1`), section headings (`h2` in legal pages), card titles, hero headings, and large numeric values in vitals panels. It gives MediTrack its calm, editorial feel.
- **`--font-body`** — DM Sans. Use for: paragraphs, labels, buttons, tables, meta.

Type scale in use: 0.75 / 0.8 / 0.85 / 0.9 / 0.95 / 1 / 1.05 / 1.15 / 1.2 / 1.75 / 2 / 2.5+ (clamp for hero).
Weights: 300 / 400 / 500 / 600. Headings use 400 in the display font (it's a serif — it doesn't need bold).

Numeric values in vitals and tables must use `font-variant-numeric: tabular-nums`.

### Radii & spacing

- `--radius-sm` (6px) — inputs, small buttons, tags
- `--radius-md` (12px) — cards
- `--radius-lg` (20px) — hero panels, modal shells
- Pills/tags — fully rounded (`999px`)
- Spacing: use multiples of 4px. Existing patterns use 0.4rem, 0.5rem, 0.75rem, 1rem, 1.25rem, 1.5rem, 1.75rem, 2rem, 2.5rem.

### Layout constants

- `--max-width` (1200px) — page content container
- `--auth-width` (440px) — narrow centered forms
- `.auth-container--wide` overrides auth width to 720px — used by legal pages

### Shadows

Subtle only. The heaviest shadow in the codebase is on `.vital-panel`:
`0 10px 45px rgba(15, 92, 107, 0.08)`. Do not exceed that. Prefer borders over shadows where possible.

## Existing classes to reuse

Before writing new CSS, check if one of these already covers the need.

### Layout & navigation
- `.navbar`, `.nav-inner`, `.nav-brand`, `.brand-icon`, `.brand-name`, `.nav-links`, `.nav-cta`
- `.main-content`

### Hero (landing)
- `.hero`, `.hero-inner`, `.hero-badge`, `.hero-title`, `.hero-subtitle`, `.hero-actions`, `.hero-visual`

### Vitals panel (hero visual)
- `.vital-panel`, `.vital-panel-header`, `.vital-panel-label`, `.vital-panel-status`
- `.vital-list`, `.vital-row`, `.vital-name`, `.vital-reading`, `.vital-value`
- `.vital-tag` with modifiers `.ok`, `.warn`, `.high`

### Features strip
- `.features`, `.features-inner`, `.feature-card`, `.feature-icon`, `.feature-title`, `.feature-body`

### CTA
- `.cta-section`, `.cta-inner`, `.cta-title`, `.cta-body`

### Buttons
- `.btn-primary` (solid teal), `.btn-ghost` (outlined)

### Auth & forms
- `.auth-section`, `.auth-container`, `.auth-container--wide`, `.auth-header`, `.auth-title`, `.auth-subtitle`
- `.auth-card`, `.auth-error`
- `.form-group`, `.form-input`, `.btn-submit`, `.auth-switch`

### Legal pages
- `.legal-card`, `.legal-callout` (with `.legal-callout strong`)

### Footer
- `.footer`, `.footer-inner`, `.footer-name`, `.footer-copy`, `.footer-links`, `.footer-link`

If a new component genuinely doesn't fit any of these, add it with a scoped prefix (e.g. `.dashboard-...`, `.log-form-...`) so styles don't leak.

## The MediTrack design language (for when there's no precedent)

When you're building something new and no existing class covers it, default to this:

- **Card-based composition.** Group related info in surfaces with a soft border and (optionally) a subtle shadow. Don't sprawl.
- **Generous whitespace.** Tight layouts read as cluttered. In health apps, calm is trust.
- **Left-aligned content** with clear hierarchy. Center only for empty states and auth pages.
- **Borders over shadows.** A 1px `--border` divider reads cleaner than a drop shadow.
- **One accent, semantic colors for meaning.** Teal is the accent. Green/amber/red appear only for status (ok/warn/high). Never use them decoratively.
- **Tabular numbers everywhere.** Vitals, tables, dates, counts.
- **Restraint reads as quality.** If something can be a border instead of a shadow, use border. If it can be solid instead of gradient, use solid.

### Status tags (already established)
Use the existing pattern: `.vital-tag.ok`, `.vital-tag.warn`, `.vital-tag.high`. Apply the same visual language to any status pill you build: uppercase, tiny letter-spacing, `--radius: 999px`, background from the corresponding `-light` variable and text from the base color.

| Status | Background | Text |
|---|---|---|
| ok / good / stable | `#e3f2e9` (in `.vital-tag.ok`) | `--ok` |
| warn / moderate / watch | `#fbefd9` | `--warn` |
| high / severe | `#fbe3e3` | `--danger` |

### Icons — Lucide

Already loaded in `base.html`. Use as:

```html
<i data-lucide="heart-pulse"></i>