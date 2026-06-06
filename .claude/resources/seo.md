# SEO and LLM-friendliness conventions

Established in the SEO/LLM audit round (June 2026).

## Hard rules for every content page

- **Front matter `description:` is required** — one factual sentence (~70–155 chars), task-oriented.
It becomes the meta description, og:description, and the page's entry in `/llms.txt` and the markdown mirror.
Pages without it fall back to `.Summary` (first ~70 words) — sloppy in SERPs and AI indexes.
Only exception: auto-generated reference pages (`fission-cli/*`, `crd-reference.md`, `metrics-reference.md`).
- **One `<h1>` per page.** Markdown pages get their h1 from the front-matter title — body headings start at `##`.
HTML section pages (`_index.html` files) keep exactly one `<h1>` (the hero); later section headings are `<h2 class="section-title">` etc. — styling is class-based, so the tag level is free.
- Release pages: `title: "vX.Y.Z Release Notes"` + `linkTitle: vX.Y.Z` (sidebar stays compact, `<title>`/h1 get keywords).

## Structured data (JSON-LD)

`layouts/partials/schema.html` — Docsy's head.html invokes `partial "schema.html"`, this site-level partial supplies it:

| Page | Entities |
|---|---|
| Home | `Organization` + `WebSite` + `SoftwareApplication` (version from `params.release_version`) |
| Blog post | `BlogPosting` (author Person, image from front-matter `images`, dates from `.Date`/`.Lastmod`) |
| Docs page | `TechArticle` + `BreadcrumbList` (from `.Ancestors`) |

Values go through `jsonify` — never hand-build JSON strings in the template.
Validate after changes: extract `application/ld+json` blocks from built pages and `json.loads` them.

## LLM outputs (config.toml)

- `[outputs] home` includes `LLMS` → Docsy renders `/llms.txt` (markdown site index) from its `layouts/index.llms.txt`.
- A `markdown` output format (text/markdown, baseName index, notAlternative) on home/section/page → Docsy's `layouts/all.md` renders every page as `<url>/index.md`, and llms.txt links those `.md` URLs automatically.
- The `.md` mirrors stay out of `sitemap.xml` (verify with `grep -c '\.md' public/sitemap.xml` → 0).
- AI crawlers (GPTBot, ClaudeBot, PerplexityBot, …) are deliberately NOT blocked in robots.txt.

## Titles

- Site title stays the short "Fission" (it suffixes every page title).
- Home `<title>`/og:title come from the landing page's front-matter title ("Fission — Open Source Kubernetes-native Serverless Framework") via the **forked** `layouts/partials/head.html` (one-block change from Docsy v0.15 — re-diff on Docsy bumps).

## Analytics

- Analytics runs through **GTM container `GTM-NX83GPK`** (inline snippet in `layouts/partials/hooks/head-end.html`), which loads **GA4 `G-BKDL6KWXQX`** (verified by inspecting the served gtm.js; it also carries a dead legacy UA tag).
- `services.googleAnalytics.id` in config.toml is **intentionally empty** — setting it would make Docsy inject gtag.js alongside GTM and double-count every hit.

## Taxonomy pages

- `/tags/`, `/categories/*`, `/author/*` are thin listings: **noindexed** (`noindex, follow` in the forked `partials/head.html`) and **excluded from sitemap.xml** (`layouts/sitemap.xml` override of Hugo's embedded template).
They remain crawlable and linked for navigation.

## Search (Algolia DocSearch)

- Config: `[params.search.algolia]` in config.toml (search-only API key — safe to be public).
- The DocSearch crawler runs on Algolia's infrastructure on its own weekly schedule; the repo cannot trigger a crawl.
Manual re-crawl: https://crawler.algolia.com/ with the DocSearch account that owns app `MSV5TDX060`.

## Plumbing

- `layouts/robots.txt` → `/robots.txt` with the `Sitemap:` line (`enableRobotsTXT = true`).
- Canonicals: `layouts/partials/hooks/head-end.html` (per-page `canonicalUrl` front-matter override supported).
- OG image: `static/images/og-image-fission.png` (1200×628) via `params.images`; blog posts override with front-matter `images`.
- http→https and www→apex 301s are handled by Netlify; legacy URL redirects live in `netlify.toml` — add one whenever a page moves.
