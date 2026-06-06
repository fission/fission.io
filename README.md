# Fission Website Source

Source for [fission.io](https://fission.io) — the website and documentation for the [Fission](https://github.com/fission/fission) serverless framework.

## How the site is built

- [Hugo](https://gohugo.io) static site using the [Docsy](https://www.docsy.dev) theme.
Docsy is pulled in as a **Hugo Module** via `go.mod` (no git submodules).
- Hosted on [Netlify](https://netlify.com), which builds every push and every PR (deploy previews) by running `./build.sh`.
- Exact build tool versions are pinned in `netlify.toml` (Hugo extended + Go) — match them locally when reproducing CI builds.
- `npm install` provides the PostCSS toolchain Docsy needs.

## Repo organization

```text
content/en
├── _index.html   # Landing page
├── docs          # Documentation (getting-started, concepts, architecture,
│                 #   installation, usage, trouble-shooting, reference, releases)
├── blog          # Blog posts
├── environments  # Language runtimes catalog (data-driven)
├── examples      # Function examples catalog (data-driven)
├── support       # Commercial support and community page
└── author        # Blog author taxonomy pages

assets/scss       # Project styles (_variables_project.scss)
layouts           # Site-level template overrides (blog list, head, schema, shortcodes)
static/data       # environments.json / examples.json behind the catalog pages
static/images     # Images, logos, blog featured images
tools             # Helper scripts (environments.json refresh, release notes formatting)
```

- Versioned values (Fission release, Helm chart) live in `config.toml` (`release_version`, `chart_version`) and are referenced in content through the `{{< release-version >}}` / `{{< chart-version >}}` shortcodes.
- The site also serves machine-readable outputs for AI tools: [`/llms.txt`](https://fission.io/llms.txt) and a markdown mirror of every page at `<url>/index.md`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for local setup, the preview workflow, and authoring conventions.
