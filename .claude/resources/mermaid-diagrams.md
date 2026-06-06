# Mermaid diagram conventions

How diagrams are authored across the docs.
Established in the v1.25 docs overhaul (PR #288); the global theme lives in `config.toml` under `[params.mermaid]` (Docsy-native support — authors just write ` ```mermaid ` fences, no per-page setup).

## Global theme

White nodes, grey-blue `#94a3b8` borders, slate `#64748b` arrows, navy `#1f2a43` text, Lato.
Defined once in `config.toml` `[params.mermaid.themeVariables]`; per-diagram colors come from the classDef kit below.

## The color kit

Apply semantic classes via classDefs in every flowchart:

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

- Write numbered edge labels as `-->|"<b>1.</b> create Package"|`.
The `<b>` renders crimson bold via `.mermaid .edgeLabel b` in `_variables_project.scss`.
- **Never use circled glyphs** (①②③) — explicitly rejected in review.
- sequenceDiagrams use `autonumber` instead.

## Width rule (the critical one)

The docs column is ~800 px; a diagram whose natural (viewBox) width exceeds **~900 px** shrinks until text is unreadable inline.

- Prefer `flowchart TB` over `LR`.
- ≤3 nodes per rank; ≤4-word edge labels.
- sequenceDiagrams: `autonumber`, ≤4 participants, short participant names.
- Avoid side-by-side subgraphs: subgraph `direction` is **ignored** when its nodes have external edges, so paired subgraphs force a wide layout.
- ≤12 nodes per diagram — split bigger ones.

Verify by measuring in a browser: `document.querySelector('.mermaid svg').viewBox.baseVal.width` — keep it under ~900–950.
`content/en/docs/architecture/buildermgr.md` is the exemplar compact diagram.

## Diagram type choice

- `flowchart TB` — component/data flows (the default).
- `sequenceDiagram` — request/interaction ordering between ≤4 participants.
- `stateDiagram-v2` — lifecycles (package/function states).
- No classDiagram.

## Tooling gotchas

- Click-to-zoom comes from the lightbox in `layouts/partials/hooks/body-end.html`; it keeps the SVG `id` on the clone (mermaid scopes its embedded CSS to that id) — don't strip ids.
- **Docsy caches partials**: after editing `body-end.html` (or any hook partial), restart `hugo server`; a live reload serves the stale partial.
- Diagrams must be readable inline without clicking — the lightbox is a bonus, not a crutch.
