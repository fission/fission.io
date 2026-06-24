---
name: cut-fission-release
description: Use when preparing fission.io docs for a new Fission release (e.g. "new release v1.X.0", "create release notes page", "prepare for release"). Orchestrates the config.toml bump, release-notes page, compatibility matrix, What's New card, reference-doc regen, and the single-branch PR.
---

# Cut Fission Release

## Overview

A Fission release touches a predictable set of files on this site.
The single non-obvious thing: **the GitHub release body is just the goreleaser template** (a flat "What's Changed" PR list), so you must *author* the Upgrade Notes / Highlights / Fixes yourself from the PR titles and the linked GHSA/PR descriptions — never paste the GitHub body and call it done.

The product code lives at `github.com/fission/fission`; this repo is docs only.
Version values are decoupled: `release_version` (app, e.g. `v1.24.0`) and `chart_version` (Helm chart, e.g. `1.24.0`) move independently.

## What changes for every release

| File | Change |
|---|---|
| `config.toml` | Bump `release_version` and `chart_version` (verify both against the chart at the tag) |
| `content/en/docs/releases/vX.Y.Z.md` | New release-notes page (see weight rule below) |
| `content/en/docs/installation/upgrade.md` | New "Upgrade to X.Y.x release" section **only if** the release has breaking/behavioral changes |
| `content/en/docs/installation/compatibility.md` | Add a literal row for the **previous** release; update the top shortcode row's columns for the new one (see step 5) |
| `content/en/_index.html` | Replace a What's New card with the release announcement (see step 6) |
| `content/en/docs/reference/fission-cli/*`, `crd-reference.md` | Regenerated from the new `fission` binary **only if** the CLI/CRDs changed (run `regen-fission-reference-docs` skill) |
| `static/data/environments.json` | Refresh via `tools/environments.py` **only if** environment images changed with the release |

## Procedure

### 1. Pull the release facts from GitHub

The release may still be a **draft/prerelease** — `gh release view` finds it anyway.

```bash
gh release view vX.Y.0 --repo fission/fission --json body -q .body   # the verbatim "What's Changed" list
```

Verify the chart facts at the tag (don't assume they match the previous release):

```bash
gh api "repos/fission/fission/contents/charts/fission-all/Chart.yaml?ref=vX.Y.0" -q .content | base64 -d | grep -E '^(version|appVersion|kubeVersion)'
gh api "repos/fission/fission/contents/charts/fission-all/values.yaml?ref=vX.Y.0" -q .content | base64 -d | grep -A2 -iE '^internalAuth:'
```

For any PR that mentions a GHSA or a behavioral change, read its body — that's where the real upgrade detail and accurate wording live:

```bash
gh pr view <N> --repo fission/fission --json title,body -q '.title + "\n\n" + .body'
```

Watch the `?ref=...` URLs in zsh — the `?` globs. Quote them.

### 2. Bump `config.toml`

```toml
release_version = "vX.Y.Z"   # app version, with leading v
chart_version   = "A.B.C"    # chart version from Chart.yaml, no leading v
```

These can differ — set each from what you read at the tag.
Never hardcode versions in docs prose; use `{{< release-version >}}` / `{{< chart-version >}}` shortcodes there.

### 3. Create the release-notes page

`content/en/docs/releases/vX.Y.Z.md`. **Weight is reverse-chronological — lower = newer.** The newest existing page is the lowest weight; the new page is one less.
(v1.20.5=73, v1.21.0=72, v1.22.0=71, v1.23.0=70, v1.24.0=69 …)

```yaml
---
title: "vX.Y.Z"
linkTitle: vX.Y.Z
weight: <previous_newest - 1>
---
```

Section template (copy the most recent release page as the model):

- **Upgrade Notes** — only if there are breaking/behavioral changes.
A short `{{< notice warning >}}` lead-in, then a `### ` subsection per breaking change spelling out *what changed and the action the operator must take*.
**This page is the canonical home for the per-release upgrade detail** — don't push it into the upgrade guide (see step 4).
- **Deprecations/Removals** — Kubernetes-version support statement, removed fields/routes, dropped tokens, etc.
- **Highlights** — author 3–6 bullets from the PR titles + GHSA/PR bodies.
Group the security work; name the user-facing features.
- **Fixes** — notable bug fixes and the chart-version line.
- **Changelog → What's Changed** — paste the GitHub body's PR list **verbatim**.
- **New Contributors** — include **only if the GitHub body has it**.
No first-time contributors → omit entirely.
- **Full Changelog** — `https://github.com/fission/fission/compare/vPREV...vX.Y.Z`.
- **References** — upgrade guide, related docs, environments, CRD spec, releases.

### 4. Upgrade-guide pointer (breaking changes only)

Keep `content/en/docs/installation/upgrade.md` **compact** — the per-version detail lives in the release-notes Upgrade Notes (step 3), not here.
Add a short `## Upgrade to X.Y.x release` section **immediately before the previous version's section** (the file is newest-first under the "latest" block): two or three sentences on the nature of the release, then a link to the release notes for the specifics.

```markdown
## Upgrade to X.Y.x release

vX.Y.0 is a security-hardening release. ... Specs that rely on the rejected primitives will fail admission after upgrade, so review them first.

See the [vX.Y.0 release notes](/docs/releases/vX.Y.Z/#upgrade-notes) for the full list of breaking changes and the action each one requires.
```

The release page's Upgrade Notes should link back to the general guide (`/docs/installation/upgrade/`) for the routine CRD/CLI/chart steps.
Don't duplicate the breaking-change detail in both places.

### 5. Compatibility matrix

`content/en/docs/installation/compatibility.md` has a Kubernetes table and a KEDA table.
The **top row of each uses `{{< release-version >}}`**, so after the config.toml bump it labels itself with the new version automatically — but its *data columns* still describe the previous release until you update them.

- Insert a literal row for the previous release (copy the old top row's data, replace the shortcode with the literal `vX.Y.Z`).
- Update the top row's columns for the new release: built-against = the `k8s.io/api` minor in the release's `go.mod`; tested-with = the `kindest/node` versions in the release's CI workflows; minimum = the chart's `kubeVersion` floor; KEDA = the `keda` version in `go.mod`/values.
- Update any `kubeVersion` notice text if the floor changed.

```bash
gh api "repos/fission/fission/contents/go.mod?ref=vX.Y.0" -q .content | base64 -d | grep -E 'k8s.io/api |keda'
```

### 6. Homepage What's New card

The landing page announces releases in the "What's New" cards, which are **hardcoded in `content/en/_index.html`** (~line 333) — the `[[params.whatsnew]]` block in `config.toml` is not referenced by any layout, but keep it in sync anyway.

Replace the stalest card with a `RELEASE`-badged card: heading "Announcing Fission vX.Y.Z", a one-sentence summary of the headline changes, and a `hero-mid` button linking `/docs/releases/vX.Y.Z/`.

### 7. Reference docs (CLI/CRD), if changed

If the CLI/CRDs changed, run the `regen-fission-reference-docs` skill.

### 8. Verify the build

Verify with the `verify-hugo-docsy-build` skill (pinned Hugo), then confirm the upgrade anchor resolves:

```bash
grep -oE 'upgrade-to-12[0-9]x-release' public/docs/installation/upgrade/index.html | sort -u
```

### 9. Branch, commit, PR

Keep all release changes on **one branch** for the user to review and merge.
Do not push or merge unprompted.
If there is an already-open related PR (environments refresh, reference-doc update), it can be folded into the release branch when the user asks.

```bash
git switch -c docs-vX.Y.0
git add config.toml content/en/_index.html content/en/docs/releases/vX.Y.Z.md \
  content/en/docs/installation/upgrade.md content/en/docs/installation/compatibility.md \
  content/en/docs/reference/
git commit   # message: "Doc changes vX.Y.0"
gh pr create ...
```

`public/` and `resources/_gen/` are build artifacts — gitignored, never commit them.

## Linking rules

- **Use plain absolute URLs** for in-repo links: `/docs/installation/upgrade/`, `/docs/releases/vX.Y.Z/`.
The dominant repo convention.
- **Do NOT use the custom `{{< relref >}}` shortcode** for content pages — it only resolves section `_index.md` paths and throws `can't evaluate field URL in type page.Page` on regular pages, failing the build.
- Use `{{< release-version >}}` / `{{< chart-version >}}` for version strings in prose; the release-notes page title legitimately hardcodes its own version.
- **Only link repo files that actually exist at the linked ref** — verify each `github.com/fission/*/blob|tree/...` URL (e.g. `curl -sL -o /dev/null -w "%{http_code}"`).
- **Don't reference internal RFC numbers (RFC-NNNN) in prose** — those design docs are not in fission/fission, so the references point at nothing a reader can find.
Describe the change itself instead.
The only acceptable RFC mentions are inside the verbatim "What's Changed" PR-title list.

## Common Mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Pasted the GitHub release body as the whole page | Page has a PR list but no real Highlights/Upgrade Notes | Author Highlights/Fixes/Upgrade Notes from PR + GHSA bodies |
| Wrong weight direction | New release sorts below old ones in the sidebar | Lower weight = newer; new page = previous newest − 1 |
| Used `{{< relref >}}` | Build error: `can't evaluate field URL in type page.Page` | Use absolute `/docs/...` URLs |
| Verified with `hugo --gc --quiet` | "Clean locally" but Netlify fails | Run via `verify-hugo-docsy-build` skill (pinned Hugo) |
| Added a "New Contributors" section with no new contributors | Empty/fabricated section | Include it only if the GitHub body has one |
| Assumed `chart_version == release_version` | Wrong chart version published in docs | Read `Chart.yaml` `version` at the tag |
| Bumped only `release_version` | `{{< chart-version >}}` still shows the old chart | Bump both in `config.toml` |
| Forgot the compatibility matrix | Top (shortcode) row shows the new version with the *old* release's K8s/KEDA data | Add literal row for previous release; update top-row columns (step 5) |
| Edited only `[[params.whatsnew]]` in config.toml | Homepage still shows the old card | The cards are hardcoded in `content/en/_index.html`; edit there (step 6) |

## Red Flags — Stop

- About to commit a release page whose Highlights are just the raw PR list → write real highlights.
- The new release page's weight is ≥ the previous release's → you have the direction backwards.

(These are the silent failures — they ship without an error. The loud ones, `{{< relref >}}` build errors and using the wrong build command, are in Common Mistakes above.)
