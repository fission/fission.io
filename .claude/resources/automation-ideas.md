# Automation ideas (not yet implemented)

Captured during the v1.25 site overhaul.
Each of these removes a manual step from a recurring process; none exist yet.

## 1. Release-docs scaffolder

A `workflow_dispatch` GitHub Action (or `tools/release_docs.py`) that takes a tag (`v1.26.0`) and:

- pulls the release body via `gh release view` and `Chart.yaml`/`values.yaml` at the tag,
- bumps `release_version`/`chart_version` in `config.toml`,
- scaffolds `content/en/docs/releases/vX.Y.Z.md` with correct front matter/weight, the verbatim What's Changed list, and TODO markers for Highlights/Upgrade Notes,
- opens a draft PR.

A human still authors Highlights/Upgrade Notes (the GitHub body is just the goreleaser PR list).
Could even be a `repository_dispatch` triggered from the fission/fission release workflow.

## 2. environments.json drift check

Scheduled Action that fetches `fission/environments/environments.json`, runs the `tools/environments.py` mapping, and opens an issue/PR when `static/data/environments.json` is stale.
Today this is manual and only happens when someone remembers.

## 3. Link checker

Scheduled lychee (or htmltest) Action over the built site.
45 blog posts dating to 2018 plus docs accumulate dead external links; nothing checks them today.

## 4. PR lint gate

Extend `.github/workflows/main.yml` (currently misspell + languagetool only) with cheap grep checks that fail the PR:

- `{{< relref` in regular content pages (breaks the build in non-obvious ways),
- Bootstrap 4 utilities (`class="...ml-N..."`/`mr-N`) which are silent no-ops under BS5,
- `<img` without `loading=` in section-page HTML,
- accidentally committed `public/` or `resources/_gen/` artifacts,
- hardcoded `v1.\d+.\d+` in docs prose outside `releases/` and `compatibility.md`.

## 5. Hugo build check on PRs

GitHub Action running `./build.sh` with the `netlify.toml`-pinned Hugo version.
Netlify's deploy preview already gates merges, but an Actions job fails faster, annotates the PR, and catches forks where Netlify previews don't run.

## 6. SVG budget check

CI check that flags any committed SVG > ~10 KB (suggests `npx svgo --multipass`), so icon bloat like the old 52 KB `github.svg` can't recur.
