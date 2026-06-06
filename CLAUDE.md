# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Source for [fission.io](https://fission.io), the marketing/docs site for the Fission serverless platform.
It is a [Hugo](https://gohugo.io) static site using the [Docsy](https://github.com/google/docsy) theme, deployed to Netlify.
This repo contains **no Fission product code** — that lives at https://github.com/fission/fission.
Work here is almost always content edits (Markdown under `content/en/`), template/asset tweaks (`layouts/`, `assets/scss/`, `static/`), or release-version bumps in `config.toml`.

## Build, serve, and deploy

- `npm install` — install PostCSS toolchain (autoprefixer for the Docsy theme).
- `hugo server` — local preview on http://localhost:1313/.
- `./build.sh` — what Netlify runs (`hugo --minify --printPathWarnings --gc`).
- Netlify pins exact versions in `netlify.toml` (currently **Hugo 0.157.0** extended and **Go 1.26.3**) — treat that file as the source of truth and match it locally when reproducing CI builds; Hugo behavior differs across versions.
- The Docsy theme is pulled as a **Hugo Module** via `go.mod` (`github.com/google/docsy`), not a git submodule.
The `.gitmodules` file is empty and the `git submodule update` line in `CONTRIBUTING.md` is stale — ignore it.
- There are no unit tests. CI (`.github/workflows/main.yml`) runs reviewdog misspell + languagetool on changed `*.md` files only.

## Content architecture

All site content is under `content/en/` (single language, `defaultContentLanguage = "en"` in `config.toml`):

- `docs/` — versioned product documentation (architecture, concepts, installation, usage, reference, releases, trouble-shooting, contributing).
- `blog/` — blog posts; permalink scheme is `/blog/:slug/` (set in `config.toml` `[permalinks]`).
- `environments/`, `examples/`, `support/`, `author/` — top-level sections wired into the main menu in `config.toml`.
- `_index.html` is the landing page; its content blocks (What's New cards, hero, community) are **hardcoded in that file** — the `[[params.whatsnew]]` block in `config.toml` is not referenced by any layout, so update both to keep them in sync but edit the HTML to change what renders.

Authoring conventions worth knowing:

- **Front matter** sets ordering via `weight:` and can opt a page out of features (`hide_feedback: true`, `hide_readingtime: true`).
- **Use the version shortcodes**, never hardcode versions in docs:
  - `{{< release-version >}}` → emits `params.release_version` (e.g. `v1.22.0`)
  - `{{< chart-version >}}` → emits `params.chart_version` (e.g. `1.22.1`)
  Both are defined in `config.toml` and rendered by `layouts/shortcodes/release-version.html` and `chart-version.html`.
- Other custom shortcodes live in `layouts/shortcodes/` (`tabs`, `tab`, `notice`, `img`, `readfile`, `relref`).
- `[markup.goldmark.renderer] unsafe = true` is set, so raw HTML in Markdown renders — this is intentional for the Docsy templates.

## Release bumps

When cutting a Fission release, two values in `config.toml` change independently (see commit `ef1ea56` "Separate app and chart version"):

- `release_version` — Fission app version (drives `{{< release-version >}}`, install docs, etc.).
- `chart_version` — Helm chart version (drives `{{< chart-version >}}`).

These are decoupled because the chart can revision without an app release.
Don't assume they move together.

## Design system & site conventions

The site follows a documented design language (navy/blue palette, white cards with hover lift, light-blue pills) and strict authoring rules (absolute URLs not `relref`, version shortcodes, lazy-loaded images with dimensions, no inline styles).
The details live in `.claude/resources/`:

- [.claude/resources/design-system.md](.claude/resources/design-system.md) — palette, card pattern, SCSS namespaces in `_variables_project.scss`, Bootstrap 5 gotchas, image/SVG rules.
- [.claude/resources/mermaid-diagrams.md](.claude/resources/mermaid-diagrams.md) — diagram color kit, the <900px width rule, step-number style, lightbox/partial-cache gotchas.
- [.claude/resources/page-patterns.md](.claude/resources/page-patterns.md) — docs nav order, page skeletons, catalog/blog/homepage/support page structures and their traps.
- [.claude/resources/automation-ideas.md](.claude/resources/automation-ideas.md) — backlog of process automation worth building.

Consult the matching resource file before styling or restructuring a page.

## Skills

Recurring workflows are codified as skills in `.claude/skills/` — use them instead of rediscovering the process:

- **cutting-fission-release-docs** — preparing the site for a new Fission release (version bumps, release-notes page, compatibility matrix, What's New card, upgrade guide).
- **bumping-hugo-docsy-site** — bumping the pinned Hugo/Go/Docsy versions safely.
- **updating-environments-and-examples** — adding or refreshing entries on the environments/examples catalog pages.
- **writing-blog-posts** — authoring a blog post with correct front matter and featured image.

## Redirects and URL stability

`netlify.toml` carries a long list of historical redirects (`/latest/*`, `/0.2.1/*`, `/0.4.0/*`, …) preserving old documentation URLs.
When renaming or moving a docs page, add a redirect rather than breaking inbound links.

## Helper scripts (`tools/`)

Python scripts run manually, not in CI:

- `tools/environments.py` — regenerates `static/data/environments.json` from an upstream `environments.json` copied in from the `fission/environments` repo.
Required when adding a new language environment to the site.
See `tools/README.md` for the env-dict mapping step.
- `tools/notes.py` — formats draft-release changelog text (paste into `notes.txt` first) for inclusion in `content/en/docs/releases/`.

## Markdown style

Treat each sentence as its own line within paragraphs (CommonMark renders single newlines as spaces, so HTML output is unchanged but diffs become per-sentence).
Don't rewrap whole paragraphs when changing one sentence.
