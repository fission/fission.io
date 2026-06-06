# Contributing

There are many areas we can use contributions — ranging from documentation, blog posts, feature proposals, issue triage, samples, and content creation.

First, please read the [code of conduct](https://github.com/fission/.github/blob/main/CODE_OF_CONDUCT.md). By participating, you're expected to uphold this code.

## Prerequisites

- **Hugo (extended)** and **Go** — the exact versions Netlify builds with are pinned in [`netlify.toml`](netlify.toml) (`HUGO_VERSION`, `GO_VERSION`); use the same Hugo version locally, behavior differs across releases.
Go is needed because the [Docsy](https://www.docsy.dev) theme is loaded as a Hugo Module (declared in `go.mod` — there are **no git submodules** to initialize).
- **Node.js (LTS)** — for the PostCSS toolchain.

## Setup

1. Clone the repo and install NPM dependencies

    ```sh
    npm install
    ```

2. Run the Hugo server

    ```sh
    $ hugo server
    Web Server is available at http://localhost:1313/ (bind address 127.0.0.1)
    Press Ctrl+C to stop
    ```

    Visit [localhost:1313](http://localhost:1313/) to preview the site.
    Hugo downloads the Docsy module automatically on first run.

3. (Optional) Run the full production build — exactly what Netlify runs:

    ```sh
    ./build.sh
    ```

## Making changes

1. Create a new branch.
2. Make your changes.
3. Verify locally with the Hugo server; for template/partial changes restart the server (Docsy caches partials).
4. Run `./build.sh` to make sure the production build passes with no warnings.
5. Commit and push your changes to the branch.
6. Raise a PR to the default branch and verify your changes on the Netlify deploy-preview URL posted on the PR.
7. Once the PR is merged, your changes go live automatically.

## Authoring conventions

- **Every page needs a front-matter `description:`** — one factual sentence; it becomes the meta description and the page's entry in `/llms.txt`.
- **Never hardcode Fission versions** in prose — use the `{{< release-version >}}` and `{{< chart-version >}}` shortcodes (values come from `config.toml`).
- **Internal links** are plain absolute URLs (`/docs/installation/upgrade/`); don't use the `relref` shortcode on regular pages.
- **One sentence per line** in Markdown — rendering is identical, but diffs and reviews become per-sentence.
- **Diagrams** are written as Mermaid code fences and follow the site's color/width conventions.
- **Moving or renaming a page?** Add a redirect in `netlify.toml` so inbound links keep working.
- Auto-generated reference pages (`docs/reference/fission-cli/*`, `crd-reference.md`, `metrics-reference.md`) are regenerated from the Fission codebase — don't hand-edit them.

Detailed conventions (design system, Mermaid diagram rules, page skeletons, SEO rules) live in [`.claude/resources/`](.claude/resources/), and [`CLAUDE.md`](CLAUDE.md) gives AI coding assistants the same guidance.

## Common content tasks

- **Blog post** — front-matter template, featured-image workflow, and category conventions: see `.claude/skills/writing-blog-posts/`.
- **New language environment or example** — both catalog pages are data-driven from `static/data/*.json`: see `.claude/skills/updating-environments-and-examples/` and [`tools/README.md`](tools/README.md).
- **Docs for a new Fission release** — version bumps, release-notes page, compatibility matrix: see `.claude/skills/cutting-fission-release-docs/`.
