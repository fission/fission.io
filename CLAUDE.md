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
- Netlify pins the exact `HUGO_VERSION` (extended) and `GO_VERSION` in `netlify.toml` — treat that file as the source of truth and match it locally; Hugo behavior differs across versions, so don't assume the latest works.
- **Local Homebrew Hugo breaks this build.** Hugo 0.158+ wraps the PostCSS pipeline in Node's permission model with a restricted filesystem scope, so `hugo --minify` hangs/fails. Use the `netlify.toml`-pinned Hugo (not the Homebrew one); see the `verify-hugo-docsy-build` skill.
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

Strict authoring rules (absolute URLs not `relref`, version shortcodes not literals, lazy-loaded images with dimensions, no inline styles) and the visual language are documented in `.claude/resources/`:

- [design-system.md](.claude/resources/design-system.md) — palette, card pattern, SCSS namespaces in `_variables_project.scss`, Bootstrap 5 gotchas, image/SVG rules.
- [page-patterns.md](.claude/resources/page-patterns.md) — docs nav order, page skeletons, catalog/blog/homepage/support structures and their traps.
- [seo.md](.claude/resources/seo.md) — required front-matter descriptions, JSON-LD partial, llms.txt + markdown-mirror outputs, title/heading conventions.
- [mermaid-diagrams.md](.claude/resources/mermaid-diagrams.md) — the fission diagram palette and styling hooks (generic mermaid mechanics live in the `author-mermaid-docsy-diagram` skill).

Consult the matching resource file before styling or restructuring a page.

## Skills

Recurring workflows are codified as skills — use them instead of rediscovering the process.

Project-local (`.claude/skills/`, fission-specific):

- **cut-fission-release** — orchestrates a Fission release doc cut (version bumps, release-notes page, compatibility matrix, What's New card); composes the reference-regen and build-verify skills.
- **regen-fission-reference-docs** — regenerate and check in the CLI/CRD reference from a new `fission` binary.
- **update-environments-catalog** / **update-examples-catalog** — add or refresh entries on the environments / examples catalog pages.

Generic Hugo/Docsy skills (shared via the harness repo, available here too): **bump-hugo-docsy-versions**, **verify-hugo-docsy-build**, **author-mermaid-docsy-diagram**, **write-hugo-blog-post**, **optimize-svg**.

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
