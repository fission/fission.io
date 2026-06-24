---
name: regen-fission-reference-docs
description: Use when the Fission CLI commands/flags or CRD schemas changed and the reference docs need regenerating and committing (triggers "regen reference docs", "check in fission-cli reference", "CRD reference changed"). Covers which files are generated and that they must be committed with the release.
---

# Regen Fission Reference Docs

## Overview

When a Fission release changes CLI commands/flags or CRD schemas, the reference docs in this site must be regenerated from the new `fission` binary and committed as part of the release.
**The most-missed step:** the regenerated files almost always appear as already-modified or untracked files in the working tree by the time you start the release — they belong to the release commit, not a separate PR.

## Generated files

| Path | Source |
|---|---|
| `content/en/docs/reference/fission-cli/*.md` | Regenerated from the `fission` binary's built-in help |
| `content/en/docs/reference/crd-reference.md` | Regenerated from the CRD schemas at the release tag |
| `content/en/docs/reference/metrics-reference.md` | Also auto-generated — do not hand-edit |

## When they appear

After you pull the new `fission` binary for the release, the regeneration tool writes these files directly.
Check working-tree state before assuming nothing changed:

```bash
git status content/en/docs/reference/
```

- **Modified files** (`M`) → updated CLI flags or CRD fields; stage them.
- **Untracked files** (`??`) matching `fission_*_*.md` → new subcommands; stage them too.
- No changes → CLI and CRDs are unchanged for this release; skip this step.

## Commit with the release

Stage the reference files alongside the rest of the release changes — they must land in the same PR, not a separate commit or follow-up:

```bash
git add content/en/docs/reference/
```

Do not skip staging untracked `??` files; a new subcommand page left unstaged means the docs ship incomplete.

## Red Flags — Stop

- About to open a separate PR for just reference-doc regeneration → fold it into the release branch instead.
- `metrics-reference.md` appears in your diff with hand-authored edits → revert and regenerate from the binary.
- Untracked `?? fission_*_*.md` files are not staged → a new subcommand is missing from the published docs.
