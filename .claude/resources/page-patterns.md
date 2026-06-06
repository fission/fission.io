# Page patterns and content architecture

Conventions for docs IA, section pages, blog, and the homepage.
Established in the v1.25 site overhaul (PR #288).

## Docs section order (nav weights)

Getting Started (1) → Concepts (2) → Architecture (3) → Installation (4) → Usage (5) → Troubleshooting (6) → Contributing (7) → Reference (9) → Releases (70).
New top-level sections must slot into this learning path, not append at the end.

## Page skeletons

- **Concept** (`docs/concepts/*`): definition → why it matters → diagram → how it works → related links.
- **Architecture** (`docs/architecture/*`): one-line role in bold → core/optional notice → diagram → responsibilities/flow → config knobs (helm values, cited) → related.
- **Task/usage** (`docs/usage/*`): what you'll accomplish → prerequisites → steps with expected output → verify → troubleshooting links.
- **Installation**: prereqs → tabbed steps → verify with `fission check` → next steps.

## Linking and version rules

- Internal links: plain absolute URLs (`/docs/installation/upgrade/`).
**Never `{{< relref >}}`** on regular content pages — the custom shortcode only resolves section `_index.md` paths and fails the build otherwise.
- Versions in prose: `{{< release-version >}}` / `{{< chart-version >}}` shortcodes, never literals (exceptions: historical rows in `installation/compatibility.md`, release-notes pages about themselves).
- One sentence per line in Markdown (renders identically; diffs become per-sentence).
- Auto-generated pages are off-limits to hand edits: `docs/reference/fission-cli/*`, `crd-reference.md`, `metrics-reference.md`.

## Catalog pages (environments, examples)

`content/en/environments/_index.html` and `content/en/examples/_index.html` are HTML pages that inline JSON from `static/data/*.json` via `{{< readfile >}}` and render cards client-side with vanilla JS.

- Keep on any change: search box, language filter, live results count (`aria-live="polite"`), empty-state messages.
- Card markup is built in JS template literals — style hooks are the `.env-card*` / `.example-card*` / `.catalog-*` SCSS namespaces, **no inline styles**.
- Examples page groups by language with `.example-group__header` (logo + name + count); groups with zero visible examples are hidden.
- Data schemas + update flow: see the `updating-environments-and-examples` skill.

## Blog

- Front matter: `title`, `date` (ISO-8601 with TZ), `author`, `categories` (usually `["Tutorials"]` or `["Fission"]`), `description`, `type: "blog"`, optional `images = ["images/featured/<slug>.png"]`.
- Featured image: PNG ≈1000×563 in `static/images/featured/`; referencing it in `images` makes it the list-card thumbnail and the OG image.
Posts without one get a branded navy fallback automatically.
- List page is a card grid: local override `layouts/blog/list.html`; thumbnail resolution order is front-matter `images` → page-bundle resource matching `*featured*` → fallback.
- **Single-post layout trap**: Docsy v0.15 renders `layouts/blog/_td-content.html` (via `.Render "_td-content"`).
A `layouts/blog/content.html` override is dead code — that file was deleted for exactly this reason.
- Byline (date · author link · reading time) and the lightbox are automatic; don't add reading time manually.
- Docs-only meta links ("Create child page", doc issues) are hidden on blog via `.td-blog .td-page-meta__*` CSS in `_variables_project.scss` (needs `!important`); "Edit this page" stays.
- Authoring walkthrough: see the `writing-blog-posts` skill.

## Homepage (`content/en/_index.html`)

- **What's New cards are hardcoded here** (~line 333).
The `[[params.whatsnew]]` block in `config.toml` is **not referenced by any layout** — update both to keep them in sync, but the HTML is what renders.
- Hero, feature, and community sections use legacy shared classes (`.card-shadow`, `.community-cards`, duplicated `.show-mobile`/`.show-desktop` blocks).
Known cleanup candidate; don't extend the duplication pattern to new pages — build single responsive markup like `content/en/support/_index.html`.

## Support page

`content/en/support/_index.html`: purple hero (sized to content, no fixed min-height) → sponsor cards (`.support-sponsor`, flex-centered logos with `object-fit: contain`) → "Looking for help?" strip (`.support-help`) → community cards (`.support-community`, single responsive block).
