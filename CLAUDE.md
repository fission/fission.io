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
- Netlify pins exact versions in `netlify.toml`: **Hugo 0.152.2** (extended) and **Go 1.25.5**.
Match these locally when reproducing CI builds — Hugo behavior differs across versions.
- The Docsy theme is pulled as a **Hugo Module** via `go.mod` (`github.com/google/docsy`), not a git submodule.
The `.gitmodules` file is empty and the `git submodule update` line in `CONTRIBUTING.md` is stale — ignore it.
- There are no unit tests. CI (`.github/workflows/main.yml`) runs reviewdog misspell + languagetool on changed `*.md` files only.

## Content architecture

All site content is under `content/en/` (single language, `defaultContentLanguage = "en"` in `config.toml`):

- `docs/` — versioned product documentation (architecture, concepts, installation, usage, reference, releases, trouble-shooting, contributing).
- `blog/` — blog posts; permalink scheme is `/blog/:slug/` (set in `config.toml` `[permalinks]`).
- `environments/`, `examples/`, `support/`, `author/` — top-level sections wired into the main menu in `config.toml`.
- `_index.html` is the landing page; many of its content blocks come from `[params]` in `config.toml` (`whatsnew` cards, hero links, etc.) rather than from Markdown.

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
