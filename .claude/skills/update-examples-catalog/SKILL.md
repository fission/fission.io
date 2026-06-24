---
name: update-examples-catalog
description: Use when adding or refreshing a function example on the fission.io /examples page (triggers "add an example", "new example to examples page"). Edits static/data/examples.json only; never touches the page markup.
---

# Update Examples Catalog

## Overview

`/examples/` is a client-rendered catalog page: the HTML in `content/en/examples/_index.html` inlines JSON from `static/data/examples.json` via `{{< readfile >}}` and renders cards with vanilla JS.
**Adding an example is a data + logo change — never edit the page markup to add an entry.**

## `examples.json` schema

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
      "tags": ["hello-world"],             // card pills + searchable
      "language": "JavaScript"             // optional: borrow another group's logo (used in Misc)
    }
  ]
}
```

Key points:

- Add the example under its language group; the page renders group headers with counts automatically and hides empty groups.
- `link` must point into the `fission/examples` repo — do not link elsewhere.
- Keep `description` to one sentence — the cards clamp long text.

## Logos

Use the `optimize-svg` skill for logo SVG optimization.
Place the optimized file at `static/images/lang-logo/<name>-logo.svg`.
If a suitable logo is unavailable, omit the `logo` field — the page falls back to `misc-logo.svg`.

## Verify

Run the `verify-hugo-docsy-build` skill to confirm the build is clean, then check `/examples/` manually:

- New entry appears, logo renders (not the fallback), the example link resolves in `fission/examples`.
- Search finds it by name, description, or tag; the language filter includes its group; the results counter moves.

## Common Mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Edited page HTML to add an entry | Diff in `_index.html`, data drift | Entries live in `static/data/examples.json` only |
| Description longer than one sentence | Cards clamp at two lines, text is cut off | One sentence only |
| Link points outside `fission/examples` | Broken or irrelevant link | Always link into `github.com/fission/examples` |
