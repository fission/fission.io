---
name: updating-environments-and-examples
description: Use when adding or refreshing entries on the fission.io catalog pages — a new language environment, new environment/builder images, or a new function example (e.g. "add the Rust environment", "update environment images", "add an example to the examples page").
---

# Updating Environments and Examples

## Overview

`/environments/` and `/examples/` are client-rendered catalog pages: HTML in `content/en/{environments,examples}/_index.html` inlines JSON from `static/data/` via `{{< readfile >}}` and renders cards with vanilla JS.
**Adding an entry is a data + logo change — never touch the page markup for it.**

## Environments (`static/data/environments.json`)

Array of environment objects:

```json
{
  "name": "Node.js",                      // language; also the filter-dropdown value
  "displayName": "Binary",                // optional display override (used by Misc)
  "logo": "/images/lang-logo/nodejs-logo.svg",
  "repo": "https://github.com/fission/environments/tree/master/nodejs",
  "images": [
    { "main": "node-env-22", "builder": "node-builder-22" },  // runtime ⇄ builder pair
    { "main": "node-env-debian" }                             // runtime-only
  ]
}
```

Image names link to `https://github.com/fission/environments/pkgs/container/<name>` — they must match GHCR package names exactly.

### Refresh flow (after a fission/environments change)

1. Copy the upstream manifest into the tools dir:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/fission/environments/master/environments.json -o tools/environments.json
   ```
2. `cd tools && python3 environments.py` — regenerates `static/data/environments.json` image arrays.
3. **New language?** Add its mapping to `env_dict` in `tools/environments.py` first (upstream name → site name) and add a card entry (name/logo/repo, `"images": []`) to `static/data/environments.json` — the script looks up every upstream env in `env_dict` and crashes with a `KeyError` on an unmapped one.
4. Delete the copied `tools/environments.json` (it's scratch input, not tracked).

## Examples (`static/data/examples.json`)

Array of language groups, each with nested examples:

```json
{
  "language": "Python",
  "logo": "/images/lang-logo/python-logo.svg",
  "tags": ["python"],                      // group-level tags, searchable
  "examples": [
    {
      "name": "Hello World",
      "description": "One-sentence description shown on the card.",
      "link": "https://github.com/fission/examples/blob/main/python/hello.py",
      "tags": ["hello-world"],            // card pills + searchable
      "language": "JavaScript"            // optional: borrow another group's logo (used in Misc)
    }
  ]
}
```

- Add the example under its language group; the page renders group headers with counts automatically and hides empty groups.
- `link` should point into the `fission/examples` repo.
- Keep descriptions to one sentence — the cards clamp long text.

## Logos

- SVG into `static/images/lang-logo/`, optimized: `npx svgo --multipass <file>` (revert if svgo makes it bigger).
Target well under 10 KB.
- Missing/unknown logo → omit the field; the page falls back to `misc-logo.svg`.
- Card styling comes from `.env-card*` / `.example-card*` in `assets/scss/_variables_project.scss` — see `.claude/resources/design-system.md`.

## Verify

```bash
hugo server   # then on /environments/ and /examples/:
```

- New entry appears, logo renders (not the fallback), GHCR/example links resolve.
- Search finds it by image name (environments) or by name/description/tag (examples); the language filter includes it; the results counter moves.
- `./build.sh` clean.

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Edited page HTML to add an entry | Diff in `_index.html`, data drift | Entries live in `static/data/*.json` only |
| New upstream env without `env_dict` mapping | `environments.py` crashes with `KeyError` | Map it in `tools/environments.py` first |
| Image name ≠ GHCR package name | Badge 404s on click | Verify at `github.com/fission/environments/pkgs/container/<name>` |
| Committed `tools/environments.json` | Scratch upstream copy in the repo | Delete it after running the script |
