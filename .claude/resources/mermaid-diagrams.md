# Mermaid palette (fission.io)

The fission-specific colors and styling hooks for mermaid diagrams in the docs.
The generic authoring mechanics — the ~900 px width rule, layout direction, the browser viewBox check, diagram-type choice, and the partial-cache/lightbox gotchas — live in the **`author-mermaid-docsy-diagram`** skill.
This file is the palette that skill tells you to apply.

Established in the v1.25 docs overhaul (PR #288); the global theme lives in `config.toml` under `[params.mermaid]` (Docsy-native — authors just write ` ```mermaid ` fences).

## Global theme

White nodes, grey-blue `#94a3b8` borders, slate `#64748b` arrows, navy `#1f2a43` text, Lato.
Defined once in `config.toml` `[params.mermaid.themeVariables]`; per-diagram colors come from the classDef kit below.

## The color kit

Apply these semantic classes via classDefs in every flowchart:

```text
classDef user fill:#ffffff,stroke:#94a3b8,color:#1f2a43
classDef fission fill:#e8f0fe,stroke:#2d70de,color:#1f2a43
classDef pod fill:#e6f7f1,stroke:#11a37f,color:#1f2a43,stroke-dasharray:5 3
classDef store fill:#fff7e0,stroke:#dba514,color:#1f2a43,stroke-dasharray:5 3
```

| Class | Meaning |
|---|---|
| `user` (white) | External actors: user, CLI, kubectl, external systems |
| `fission` (light blue) | Fission components: router, executor, buildermgr, webhook, … |
| `pod` (teal, dashed) | Pods/workloads Fission manages: function pods, builder pods |
| `store` (amber, dashed) | Storage/data: StorageSvc, archives, S3, queues |

Crimson is reserved for step numbers and error/deprecated annotations.

## Step numbers on arrows

Write numbered edge labels as `-->|"<b>1.</b> create Package"|`.
The `<b>` renders crimson bold via `.mermaid .edgeLabel b` in `_variables_project.scss`.
`content/en/docs/architecture/buildermgr.md` is the exemplar compact diagram.

## Fission lightbox hook

Click-to-zoom comes from the lightbox in `layouts/partials/hooks/body-end.html`; it keeps the SVG `id` on the clone (mermaid scopes its embedded CSS to that id) — don't strip ids.
After editing `body-end.html` (or any hook partial), restart `hugo server` — Docsy's `partialCached` serves the stale partial on live-reload.
