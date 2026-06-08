import json, os, sys, glob

# Regenerates static/data/examples.json (consumed by content/en/examples/_index.html)
# from the per-language examples.json files in the fission/examples repository.
#
# The examples repo keeps a flat examples.json next to each language's samples
# ({name, description, path, tag, language}); this site needs them grouped by
# language with a logo and group-level tags. This script bridges the two.
#
# Usage (run from this tools/ directory):
#   python3 examples.py [path-to-fission-examples-checkout]
# Defaults to a sibling checkout at ../../examples.

# Catalog groups in display order. Each top-level directory in the examples repo
# maps to one group; everything under miscellaneous/ (recursively) collapses into
# "Misc". `langs` lists the source `language` values that feed group-level cards;
# `dir`/`recursive` locate the source examples.json files.
GROUPS = [
    {"language": "JavaScript", "logo": "/images/lang-logo/nodejs-logo.svg",
     "tags": ["node.js", "javascript"], "dir": "nodejs"},
    {"language": "Python", "logo": "/images/lang-logo/python-logo.svg",
     "tags": ["python"], "dir": "python"},
    {"language": "Go", "logo": "/images/lang-logo/go-logo.svg",
     "tags": ["go"], "dir": "go"},
    {"language": "Java", "logo": "/images/lang-logo/java-logo.svg",
     "tags": ["java"], "dir": "java"},
    {"language": ".NET", "logo": "/images/lang-logo/dotnet-logo.svg",
     "tags": ["c#", ".net"], "dir": "dotnet"},
    {"language": "Perl", "logo": "/images/lang-logo/perl-logo.svg",
     "tags": ["perl"], "dir": "perl"},
    {"language": "PHP", "logo": "/images/lang-logo/php-logo.svg",
     "tags": ["php"], "dir": "php7"},
    {"language": "Ruby", "logo": "/images/lang-logo/ruby-logo.svg",
     "tags": ["ruby"], "dir": "ruby"},
    {"language": "Misc", "logo": "/images/lang-logo/misc-logo.svg",
     "tags": ["misc"], "dir": "miscellaneous", "recursive": True},
]

# Normalize the per-example `language` field to a catalog group name. The site
# uses it to pick a per-card logo (falling back to the group logo), so a Misc
# card written in Go still shows the Go logo. Empty/unknown values yield null.
LANGUAGE_ALIASES = {
    "javascript": "JavaScript",
    "python": "Python",
    "go": "Go",
    "java": "Java",
    "c#": ".NET",
    ".net": ".NET",
    "perl": "Perl",
    "php": "PHP",
    "ruby": "Ruby",
    "tensorflow": "TensorFlow",
}

# Redundant with the group itself; dropped from per-card tags.
DROP_TAGS = {"miscellaneous"}


def normalize_language(value):
    return LANGUAGE_ALIASES.get((value or "").strip().lower())


def normalize_tags(tags):
    out = []
    for tag in tags or []:
        tag = tag.strip().lower()
        if tag and tag not in DROP_TAGS and tag not in out:
            out.append(tag)
    return out


def source_files(repo, group):
    base = os.path.join(repo, group["dir"])
    if group.get("recursive"):
        return sorted(glob.glob(os.path.join(base, "**", "examples.json"), recursive=True))
    path = os.path.join(base, "examples.json")
    return [path] if os.path.isfile(path) else []


def build_example(src):
    example = {
        "name": src["name"].strip(),
        "description": src["description"].strip(),
        "link": src["path"].strip(),
        "tags": normalize_tags(src.get("tag")),
    }
    language = normalize_language(src.get("language"))
    if language:
        example["language"] = language
    return example


def build_catalog(repo):
    catalog = []
    for group in GROUPS:
        files = source_files(repo, group)
        if not files:
            print("warning: no examples.json found for group", group["language"],
                  "under", os.path.join(repo, group["dir"]))
        examples = []
        for path in files:
            with open(path) as f:
                for src in json.load(f):
                    examples.append(build_example(src))
        if not examples:
            continue
        catalog.append({
            "language": group["language"],
            "logo": group["logo"],
            "tags": group["tags"],
            "examples": examples,
        })
    return catalog


def main():
    repo = sys.argv[1] if len(sys.argv) > 1 else os.path.join("..", "..", "examples")
    if not os.path.isdir(repo):
        print("examples repo not found at", repo,
              "- pass the path to a fission/examples checkout as the first argument")
        sys.exit(1)

    catalog = build_catalog(repo)
    total = sum(len(g["examples"]) for g in catalog)
    with open("../static/data/examples.json", "w") as f:
        json.dump(catalog, f, indent=2)
        f.write("\n")
    print("wrote", total, "examples across", len(catalog), "groups to static/data/examples.json")


if __name__ == "__main__":
    main()
