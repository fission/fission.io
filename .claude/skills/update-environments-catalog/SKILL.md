---
name: update-environments-catalog
description: Use when adding or refreshing a language environment on the fission.io /environments page (triggers "add the Rust environment", "update environment images", "new env image"). Edits static/data/environments.json only and runs tools/environments.py.
---

# Update Environments Catalog

## Overview

`/environments/` is a client-rendered catalog page: the HTML in `content/en/environments/_index.html` inlines JSON from `static/data/environments.json` via `{{< readfile >}}` and renders cards with vanilla JS.
**Adding or refreshing an environment is a data + logo change — never touch the page markup.**

The cross-repo sync trigger: when `fission/environments` ships an image change upstream, that is what prompts a refresh here.

## `environments.json` object schema

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

## Refresh flow (after a fission/environments change)

1. Copy the upstream manifest into the tools dir:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/fission/environments/master/environments.json -o tools/environments.json
   ```
2. Run the generator:
   ```bash
   cd tools && python3 environments.py
   ```
   This regenerates the `images` arrays in `static/data/environments.json`.
3. Delete the scratch copy — it is not tracked:
   ```bash
   rm tools/environments.json
   ```

## Adding a new language (the `env_dict` KeyError trap)

The script looks up every upstream environment name in `env_dict` in `tools/environments.py` and crashes with a `KeyError` on any unmapped entry.
Before running the script for a new language:

1. Add a mapping to `env_dict` in `tools/environments.py`: upstream name → site display name.
2. Add a card entry to `static/data/environments.json` with `name`, `logo`, `repo`, and `"images": []` — the script fills in `images`, but the card entry must exist first.

Then run the refresh flow above.

## Logos

Use the `optimize-svg` skill for logo SVG optimization (don't restate svgo flags here).
Place the optimized file at `static/images/lang-logo/<name>-logo.svg`.
Target well under 10 KB.
If a suitable logo is unavailable, omit the `logo` field — the page falls back to `misc-logo.svg`.
Card styling (`.env-card*`) lives in `assets/scss/_variables_project.scss` — see `.claude/resources/design-system.md`.

## Verify

Run the `verify-hugo-docsy-build` skill to confirm the build is clean, then check `/environments/` manually:

- New entry appears, logo renders (not the fallback), GHCR links resolve.
- Search finds it by image name; the language filter includes it; the results counter moves.

## Common Mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Edited page HTML to add an entry | Diff in `_index.html`, data drift | Entries live in `static/data/environments.json` only |
| New upstream env without `env_dict` mapping | `environments.py` crashes with `KeyError` | Map it in `tools/environments.py` first; add a card entry with `"images": []` |
| Image name ≠ GHCR package name | Badge 404s on click | Verify at `github.com/fission/environments/pkgs/container/<name>` |
| Committed `tools/environments.json` | Scratch upstream copy in the repo | Delete it after running the script |
