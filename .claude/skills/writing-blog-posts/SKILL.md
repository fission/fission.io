---
name: writing-blog-posts
description: Use when authoring or editing a post on the fission.io blog (e.g. "write a blog post about X", "publish a tutorial", "add a release announcement post"). Covers file layout, front matter, the featured-image workflow, category conventions, and verification.
---

# Writing Blog Posts

## Overview

Posts live in `content/en/blog/` and publish at `/blog/<slug>/` (permalink from the file/dir name, not the title).
The list page renders each post as a card: thumbnail, title, date · author · reading time, category pill, excerpt.
Byline and reading time on the post page are automatic — never add them by hand.

## File layout

- Text-only post: `content/en/blog/my-post-slug.md`.
- Post with its own screenshots/images: a bundle — `content/en/blog/my-post-slug/index.md` plus the images next to it, referenced relatively (`![…](diagram.png)`).
- Sitewide images (featured, shared logos) go under `static/images/`.

## Front matter

```toml
+++
title = "Event Driven Scaling Fission Functions with KEDA"
date = "2026-06-06T10:00:00+05:30"
author = "Jane Doe"
categories = ["Tutorials"]
description = "One-sentence summary used in cards, RSS, and OG tags"
type = "blog"
images = ["images/featured/my-post-featured.png"]
+++
```

- `type = "blog"` is required.
- `description` is required — it is the meta description, OG description, and llms.txt entry (see `.claude/resources/seo.md`).
- `categories`: `["Tutorials"]` for how-tos, `["Fission"]` for project/release news — reuse existing categories, don't invent new ones.
- `author` full name; it links to the author taxonomy page automatically.
- Use a real current `date` with timezone — the list groups by year and sorts by it.

## Featured image

1. Create a PNG around **1000×563** (16:9-ish) named `<slug>-featured.png`.
2. Put it in `static/images/featured/`.
3. Reference it in the `images` front-matter param (path relative to `static/`, leading slash optional).

That one param drives the blog-list card thumbnail **and** the OG/social preview image.
No featured image is fine — cards fall back to a branded navy placeholder.
Don't also embed the featured image at the top of the body; the card already shows it.

## Body conventions

- One sentence per line (project-wide Markdown rule).
- Code fences with language hints; real, runnable commands with expected output.
- Version strings via `{{< release-version >}}` / `{{< chart-version >}}` shortcodes — a post hardcoding "v1.25.0" goes stale silently.
- Internal links as absolute paths (`/docs/usage/…`), **never `{{< relref >}}`**.
- Images get descriptive alt text; the lightbox (click-to-zoom) wires up automatically.
- See `.claude/resources/page-patterns.md` for the full blog conventions and `.claude/resources/design-system.md` for visual rules.

## Verify

```bash
hugo server
```

- `/blog/` — card shows the thumbnail (not the fallback, if you added one), correct date/author/reading time/category pill, sane excerpt.
- `/blog/<slug>/` — byline renders, images load, code blocks highlight.
- `./build.sh` clean (catches bad front matter and broken refs).

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| `images` path typo / file not in `static/images/featured/` | Card shows the navy fallback unexpectedly | Path is relative to `static/`; check the filename |
| Edited `layouts/blog/content.html` for layout tweaks | Nothing changes | Dead file pattern — Docsy v0.15 renders `layouts/blog/_td-content.html` |
| Added "5 min read" or a byline manually | Duplicated meta on the post | Both are automatic from the layout |
| New category invented | Lonely taxonomy page | Stick to `Tutorials` / `Fission` |
| Date without timezone or in the future | Post sorts oddly or doesn't publish | ISO-8601 with TZ offset, current time |
