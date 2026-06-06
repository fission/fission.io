# Design system

The visual language used across docs, section pages (environments/examples/support), and blog.
Established in the v1.25 site overhaul (PR #288).

## Palette

| Role | Value | Used for |
|---|---|---|
| Text (navy) | `#1f2a43` | Headings, card titles, body emphasis; also `$primary` in SCSS |
| Accent (blue) | `#2d70de` | Links, hover-state titles, icons; also `$secondary` |
| Tint (light blue) | `#e8f0fe` | Pill/badge backgrounds, tinted card headers, mermaid "fission" nodes |
| Pill text | `#1c4fa8` | Text on light-blue pills |
| Body grey | `#5a5b75` | Card descriptions, section text |
| Muted slate | `#64748b` / `#94a3b8` | Meta text, counters, secondary icons, mermaid arrows/borders |
| Borders | `#e4e9f2` (cards), `#cbd5e1` (form controls) | Hairlines |
| Hero purple | `linear-gradient(130deg, #473782 50%, #2c2c62 70%)` | Homepage + support hero |
| Navbar purple | `#2a1866` | Solid navbar / scrolled state |
| Hot accent | `#E361FD` | Navbar active underline |

Diagram-specific colors live in [mermaid-diagrams.md](mermaid-diagrams.md).

## Card pattern

The standard card (see `.env-card`, `.example-card`, `.support-community__card`, `.blog-card` in `assets/scss/_variables_project.scss`):

- White background, `border: 1px solid #e4e9f2`, `border-radius: 8px`.
- Shadow `0 5px 10px 0 rgba(41, 26, 204, 0.08)`.
- Hover: lift `transform: translateY(-2px)` + deeper shadow `0 10px 18px 0 rgba(41, 26, 204, 0.14)`; title shifts to accent blue.
- If the whole card is a link, set `text-decoration: none !important` on the card class — otherwise every word renders underlined blue.
- Tags/badges: rounded-full pills, `#e8f0fe` background, `#1c4fa8` text, small + semibold.

## SCSS organization

- All project styles live in `assets/scss/_variables_project.scss`, appended in commented, namespaced blocks: `.catalog-*` (search/filter toolbars), `.env-card*`, `.example-card*`, `.support-*`, `.blog-card*`, `.blog-list*`, `.fission-lightbox*`.
- **No inline styles** in content HTML — add a namespaced class instead.
- Docsy v0.15 = Bootstrap 5: use `ms-*`/`me-*`/`text-start`/`text-end` (the BS4 `ml-*`/`mr-*` classes silently do nothing) and `.form-select` for selects.
- Overriding a Docsy default sometimes needs `!important` (e.g. `.td-page-meta__*` links) — comment why when you do.
- Homepage legacy classes (`.card-shadow`, `.community-cards`, `.show-mobile`/`.show-desktop`, `.hero-mid*`) are shared by `content/en/_index.html`; don't restyle them for a section page — create a new namespace instead.

## Images

- Every `<img>` gets `loading="lazy" decoding="async"`, explicit `width`/`height`, and an `alt` (empty `alt=""` for decorative logos).
Exception: above-the-fold hero/sponsor images skip `loading="lazy"`.
- Run new SVGs through `npx svgo --multipass` before committing; revert any file svgo makes bigger.
- `static/images/github.svg` is the 0.7 KB official GitHub mark (it replaced a 52 KB illustration; used on homepage + support) — don't reintroduce heavy icon files.
- Language logos: SVG in `static/images/lang-logo/`; `misc-logo.svg` is the fallback.
- Blog featured images: PNG ≈1000×563 in `static/images/featured/` (see [page-patterns.md](page-patterns.md)).
- Diagrams and content images are click-to-zoom via the lightbox in `layouts/partials/hooks/body-end.html` — nothing to do per-page; it auto-wires `.td-content` images and mermaid SVGs.
