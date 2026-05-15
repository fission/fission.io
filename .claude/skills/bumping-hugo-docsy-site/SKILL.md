---
name: bumping-hugo-docsy-site
description: Use when bumping Hugo, Go, or Docsy theme versions in this Hugo+Docsy site (theme loaded as a Hugo Module via go.mod, pinned in netlify.toml). Triggers include "update go version", "bump docsy", "upgrade hugo", or stale GO_VERSION/HUGO_VERSION in netlify.toml.
---

# Bumping a Hugo + Docsy + Netlify Site

## Overview

Versions are pinned in **three** places that must stay in sync: `go.mod` (Go directive + module require), `netlify.toml` (GO_VERSION + HUGO_VERSION across every `[context.*]`), and the Docsy module version itself.
The non-obvious trap: **`go mod tidy` strips the Docsy `require` lines** because no Go source imports them — Hugo's module system uses go.mod but Go's tooling can't see that. Use `hugo mod get` for module updates, not `go get` + `go mod tidy`.

## When to Use

- Routine version refresh on this site.
- User asks to "update Go", "bump Docsy", or "upgrade Hugo".
- Indicators: `[module]` block with `path = "github.com/google/docsy"` in `config.toml`, and `GO_VERSION`/`HUGO_VERSION` in `netlify.toml`.

## Quick Reference

| Version | Where pinned | How to update |
|---|---|---|
| Docsy theme | `go.mod` `require` | `hugo mod get github.com/google/docsy@vX.Y.Z` |
| Docsy dependencies | `go.mod` `require` | `hugo mod get github.com/google/docsy/dependencies@vX.Y.Z` |
| Go toolchain (directive) | `go.mod` `go ...` line | `go mod edit -go=X.Y.Z` |
| Go toolchain (Netlify) | `netlify.toml` `GO_VERSION` in every context | manual edit |
| Hugo (Netlify) | `netlify.toml` `HUGO_VERSION` in every context | manual edit |

## Procedure

### 1. Check the current state

```bash
cat go.mod
grep -E '(HUGO|GO)_VERSION' netlify.toml
go version    # local Go
hugo version  # local Hugo (extended build expected)
```

### 2. Look up the right versions

```bash
# Docsy + dependencies — go module proxy is authoritative
curl -s https://proxy.golang.org/github.com/google/docsy/@latest
curl -s https://proxy.golang.org/github.com/google/docsy/dependencies/@latest
```

**Hugo: pin to whatever Docsy itself targets, NOT the absolute latest Hugo release.**
Docsy's `package.json` carries a `hugo_version` field that records the Hugo version that release was tested against:

```bash
gh api "repos/google/docsy/contents/package.json?ref=v<docsy-version>" --jq .content | base64 -d | grep -A1 hugo_version
```

Bumping Hugo past that pin risks breakage. Specifically: Hugo 0.158+ wraps the PostCSS pipeline in Node's experimental Permission Model with a restricted filesystem scope, which breaks browserslist's parent-directory search and hangs/fails `hugo --minify`. Docsy v0.15.0 pins `hugo_version: "0.157.0"` (the last pre-permission-model release) for exactly this reason.

Note: `docsy/dependencies` moves rarely — pinned at `v0.7.2` since 2023.
Don't assume it has an update just because the main Docsy module does.

### 3. Update Docsy via `hugo mod get` (NOT `go get` + `go mod tidy`)

```bash
hugo mod get github.com/google/docsy@vX.Y.Z
hugo mod get github.com/google/docsy/dependencies@vA.B.C   # only if changed
```

**Why not `go mod tidy`:** It scans Go source files for imports. There are none for the theme — Hugo resolves modules at build time. `tidy` will silently strip both `require` lines, leaving an empty `go.mod` that Hugo then refuses to build against.
`hugo mod get` writes both `go.mod` and `go.sum` correctly.

If you already ran `go mod tidy` and lost the requires, recover with the same `hugo mod get` calls — they re-add them.

### 4. Bump the Go directive in go.mod

```bash
go mod edit -go=X.Y.Z   # match local `go version` or Netlify's GO_VERSION
```

### 5. Sync netlify.toml

Update **every** `[context.*]` block (currently `production`, `split1`, `deploy-preview`, `branch-deploy`):

```toml
HUGO_VERSION = "<new-hugo-version>"
GO_VERSION   = "<matches go.mod go directive>"
```

Easy to miss: the same pair is repeated 4× — use a single multi-line `Edit` covering all contexts, not four separate edits.

### 6. Verify the build locally

```bash
./build.sh   # the full production command — matches what Netlify runs
```

**Don't shortcut with `hugo --gc --quiet`.** It bypasses `--minify`, which is what triggers the PostCSS pipeline (and any Hugo/Docsy/Node-permission-model interactions). Always run the same flags Netlify will run: `hugo --minify --printPathWarnings --gc`.

If templates broke on a Docsy major bump, read the Docsy release notes — partials/shortcodes occasionally rename.

### 7. Review and commit

```bash
git diff --stat
git diff go.mod go.sum netlify.toml
```

Expect changes only in `go.mod`, `go.sum`, `netlify.toml`.
If `public/` or `resources/_gen/` show up they're build artifacts — `.gitignore` already excludes them, don't add them.

## Common Mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Ran `go mod tidy` after `go get` | `go.mod` requires section is empty | Re-run `hugo mod get` for each module |
| Pinned Hugo to the absolute latest release | `hugo --minify` hangs or errors with `ERR_ACCESS_DENIED` / "Access to this API has been restricted" from Node | Pin to whatever Docsy's `package.json` `hugo_version` field says |
| Verified with `hugo --gc --quiet` only | "Looked clean locally" but Netlify fails | Run `./build.sh` — it uses `--minify` which is what exercises the PostCSS pipeline |
| Bumped `GO_VERSION` in only one context | Production deploys on old Go, previews on new (or vice versa) | Update all 4 contexts |
| Bumped `HUGO_VERSION` in netlify but not the `go.mod` `go` directive | Local build uses different toolchain than CI | Keep them aligned |
| Used `go get` instead of `hugo mod get` | Works, but doesn't refresh Hugo's module cache the same way | Prefer `hugo mod get` |
| Pinned Hugo to non-extended version | SCSS/asset pipeline breaks | Docsy needs Hugo **extended** — Netlify's image is extended by default |

## Red Flags — Stop

- About to run `go mod tidy` after touching a module require → don't.
- About to commit only `go.mod` without `go.sum` or vice versa → both update together.
- `hugo --gc` prints warnings about missing partials after a Docsy major bump → check Docsy CHANGELOG before pushing.
- `netlify.toml` diff touches only one context → check the others.
