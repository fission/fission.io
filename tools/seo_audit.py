#!/usr/bin/env python3
"""SEO/GEO audit harness for the built fission.io site (public/).

Crawls the rendered HTML and scores eight dimensions:
crawlability, indexation, page intent, titles, internal links,
structured data, source citations, answer-first content.

Also runs a priority-query benchmark: each target query must map to a
clear, answer-ready page. Re-run after every fix to measure progress.

Stdlib only. Usage: python3 tools/seo_audit.py [public_dir]
"""
import sys, os, re, json, glob
from html.parser import HTMLParser

PUB = sys.argv[1] if len(sys.argv) > 1 else "public"
BASE = "https://fission.io"

# ---- Priority queries → the page that should answer them (path under public/) ----
# Each entry: (query, expected target path, intent kind)
PRIORITY_QUERIES = [
    ("what is fission serverless", "index.html", "informational"),
    ("install fission on kubernetes", "docs/installation/index.html", "howto"),
    ("create a fission function", "docs/usage/function/functions/index.html", "howto"),
    ("fission getting started tutorial", "docs/getting-started/index.html", "howto"),
    ("fission multi-namespace tenancy", "docs/usage/multi-namespace-tenancy/index.html", "howto"),
    ("run fission function locally", "docs/usage/function/run-local/index.html", "howto"),
    ("debug fission function", "docs/usage/function/debugging/index.html", "howto"),
    ("fission gateway api http route", "docs/usage/gateway-api/index.html", "howto"),
    ("fission message queue trigger keda", "docs/usage/triggers/message-queue-trigger-kind-keda/index.html", "howto"),
    ("fission autoscaling executor poolmgr", "docs/usage/function/executor/index.html", "howto"),
    ("fission prometheus monitoring metrics", "docs/usage/observability/prometheus/index.html", "howto"),
    ("fission opentelemetry tracing", "docs/usage/observability/opentelemetry/index.html", "howto"),
    ("fission upgrade guide", "docs/installation/upgrade/index.html", "howto"),
    ("fission architecture components", "docs/architecture/index.html", "informational"),
    ("fission vs knative comparison", "docs/concepts/comparison/index.html", "comparison"),
    ("fission environments languages python nodejs go", "docs/usage/languages/index.html", "informational"),
]

class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title=None; self._intitle=False
        self.desc=None; self.canonical=None; self.robots=None
        self.h1=0; self.ld=[]; self._inld=False; self._ld=""
        self.links=[]; self.text=[]; self._inbody=False
        self._skip=0  # inside script/style/nav/header/footer
        self._first_p=None; self._inp=False; self._pbuf=""
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if t=="title": self._intitle=True
        elif t=="meta":
            n=(a.get("name") or a.get("property") or "").lower()
            if n=="description" and self.desc is None: self.desc=a.get("content","")
            if n=="robots": self.robots=(a.get("content") or "").lower()
        elif t=="link" and (a.get("rel")=="canonical" or "canonical" in (a.get("rel") or "")):
            self.canonical=a.get("href")
        elif t=="h1": self.h1+=1
        elif t=="script" and a.get("type")=="application/ld+json":
            self._inld=True; self._ld=""
        elif t in ("script","style","nav","header","footer"): self._skip+=1
        elif t=="a" and a.get("href"): self.links.append(a["href"])
        elif t=="main": self._inbody=True
        elif t=="p" and self._first_p is None and self._skip==0: self._inp=True; self._pbuf=""
    def handle_endtag(self,t):
        if t=="title": self._intitle=False
        elif t=="script" and self._inld:
            self._inld=False; self.ld.append(self._ld)
        elif t in ("script","style","nav","header","footer") and self._skip>0: self._skip-=1
        elif t=="p" and self._inp:
            self._inp=False
            if self._pbuf.strip() and self._first_p is None: self._first_p=self._pbuf.strip()
    def handle_data(self,d):
        if self._intitle: self.title=(self.title or "")+d
        if self._inld: self._ld+=d
        if self._skip==0: self.text.append(d)
        if self._inp: self._pbuf+=d

def crawl():
    pages={}
    for fp in glob.glob(f"{PUB}/**/index.html", recursive=True)+glob.glob(f"{PUB}/*.html"):
        rel=os.path.relpath(fp,PUB)
        html=open(fp,encoding="utf-8",errors="ignore").read()
        p=P();
        try: p.feed(html)
        except Exception: pass
        words=len(re.findall(r"\w+"," ".join(p.text)))
        lds=[]
        for b in p.ld:
            try: lds.append(json.loads(b))
            except Exception: lds.append({"_INVALID":True})
        # internal outlinks (same-site, strip anchors/queries) + external links
        out=set(); ext=set()
        for h in p.links:
            if h.startswith(BASE): h=h[len(BASE):]
            if h.startswith("/") and not h.startswith("//"):
                out.add(h.split("#")[0].split("?")[0])
            elif h.startswith("http"): ext.add(h)
        pages[rel]=dict(title=(p.title or "").strip(), desc=p.desc, canonical=p.canonical,
                        robots=p.robots, h1=p.h1, ld=lds, words=words, ext=ext,
                        first_p=p._first_p, out=out)
    return pages

def url_of(rel): return "/"+rel[:-len("index.html")] if rel.endswith("index.html") else "/"+rel

def main():
    pages=crawl()
    print(f"crawled {len(pages)} html pages from {PUB}\n")
    # inlink graph for orphan detection (content pages only: under /docs/, /blog/, etc.)
    inlinks={rel:0 for rel in pages}
    relurl={url_of(rel).rstrip("/")+"/":rel for rel in pages}
    if "index.html" in pages: relurl["/"]="index.html"
    for rel,p in pages.items():
        for o in p["out"]:
            key=o.rstrip("/")+"/"
            if key in relurl and relurl[key]!=rel: inlinks[relurl[key]]+=1

    issues=[]
    def add(sev,dim,msg): issues.append((sev,dim,msg))

    docs=[r for r in pages if r.startswith("docs/") and r.endswith("index.html")]
    # --- titles & descriptions & h1 & noindex (content pages) ---
    for rel in sorted(pages):
        p=pages[rel]
        is_taxonomy=any(rel.startswith(x) for x in ("tags/","categories/","author/"))
        is_ref="reference/fission-cli/" in rel or rel.endswith("reference/crd-reference/index.html") or "metrics-reference" in rel
        noindex = p["robots"] and "noindex" in p["robots"]
        if rel.startswith("docs/") and not is_ref:
            if not p["desc"]: add("med","titles",f"no meta description: {url_of(rel)}")
            elif not (60<=len(p["desc"])<=160): add("low","titles",f"description {len(p['desc'])} chars (want 60-160): {url_of(rel)}")
            if p["h1"]!=1: add("med","intent",f"h1 count={p['h1']} (want 1): {url_of(rel)}")
            if noindex: add("high","indexation",f"NOINDEX on content page: {url_of(rel)}")
            # canonical present and self-referential
            want=BASE+url_of(rel)
            if not p["canonical"]: add("med","crawlability",f"no canonical tag: {url_of(rel)}")
            elif p["canonical"].rstrip("/")!=want.rstrip("/"): add("low","crawlability",f"canonical mismatch ({p['canonical']} != {want}): {url_of(rel)}")
        if is_taxonomy and not noindex: add("low","indexation",f"taxonomy not noindexed: {url_of(rel)}")
        # skip search-engine verification token files (intentionally bare static html)
        is_verify = re.match(r"(google[0-9a-f]+|BingSiteAuth|yandex_)", os.path.basename(rel))
        if not p["title"] and not is_verify: add("med","titles",f"empty <title>: {url_of(rel)}")
    # --- structured data coverage ---
    for rel in docs:
        if "reference/fission-cli/" in rel: continue
        p=pages[rel]
        types=set()
        for b in p["ld"]:
            if b.get("_INVALID"): add("high","structured-data",f"INVALID JSON-LD: {url_of(rel)}"); continue
            t=b.get("@type");
            if isinstance(t,list): types.update(t)
            elif t: types.add(t)
            for g in b.get("@graph",[]) if isinstance(b.get("@graph"),list) else []:
                gt=g.get("@type"); types.add(gt) if gt else None
        if not p["ld"]: add("high","structured-data",f"no JSON-LD: {url_of(rel)}")
        elif "TechArticle" not in types and "BreadcrumbList" not in types:
            add("low","structured-data",f"JSON-LD present but no TechArticle/Breadcrumb: {url_of(rel)} ({types})")
    # --- orphan internal links (content pages with 0 inlinks) ---
    for rel in sorted(pages):
        if not rel.startswith("docs/") or not rel.endswith("index.html"): continue
        if "reference/fission-cli/" in rel: continue
        # section roots legitimately reached via nav; flag only leaf pages
        depth=rel.count("/")
        if inlinks[rel]==0 and depth>=2:
            add("med","internal-links",f"orphan (0 inlinks): {url_of(rel)}")
    # --- PRIORITY QUERY BENCHMARK (answer-first + citations checked inline below) ---
    print("=== PRIORITY QUERY BENCHMARK ===")
    bench_gaps=0
    for q,target,kind in PRIORITY_QUERIES:
        if target is None:
            print(f"  [GAP ] {q!r}\n         no target page exists ({kind})"); bench_gaps+=1
            add("high","page-intent",f"priority query has no answer page: {q!r} ({kind})"); continue
        p=pages.get(target)
        if not p:
            print(f"  [MISS] {q!r}\n         expected {target} not built"); bench_gaps+=1
            add("high","page-intent",f"priority target missing: {target} for {q!r}"); continue
        # answer-ready checks
        probs=[]
        if not p["desc"]: probs.append("no-description")
        if p["h1"]!=1: probs.append(f"h1={p['h1']}")
        fp=p["first_p"] or ""
        if len(fp)<40: probs.append("weak-first-paragraph")
        if p["words"]<120: probs.append(f"thin({p['words']}w)")
        if not p["ld"] and target.startswith("docs/"): probs.append("no-json-ld")
        # source-citation check (GEO): does the answer page cite an authoritative external source?
        AUTH=("github.com/fission","github.com/kubernetes","kubernetes.io","knative.dev",
              "openfaas.com","keda.sh","cncf.io","gateway-api.sigs.k8s.io","helm.sh",
              "opentelemetry.io","github.com/fission/fission","vmware-archive")
        cited=any(any(a in e for a in AUTH) for e in p["ext"])
        if not cited and kind in ("comparison","informational"): probs.append("no-source-citation")
        status="OK  " if not probs else "WARN"
        if probs: bench_gaps+=1
        print(f"  [{status}] {q!r} -> {url_of(target)}")
        if probs: print(f"         {', '.join(probs)}")
    print(f"\n  benchmark: {len(PRIORITY_QUERIES)-bench_gaps}/{len(PRIORITY_QUERIES)} queries answer-ready\n")

    # --- REPORT ---
    order={"high":0,"med":1,"low":2}
    issues.sort(key=lambda x:(order[x[0]],x[1]))
    from collections import Counter
    bydim=Counter((s,d) for s,d,_ in issues)
    print("=== ISSUES BY SEVERITY/DIMENSION ===")
    for (s,d),n in sorted(bydim.items(),key=lambda kv:(order[kv[0][0]],kv[0][1])):
        print(f"  {s.upper():4} {d:16} x{n}")
    print(f"\n  totals: high={sum(1 for i in issues if i[0]=='high')} "
          f"med={sum(1 for i in issues if i[0]=='med')} low={sum(1 for i in issues if i[0]=='low')}\n")
    print("=== TOP ISSUES (high+med) ===")
    hm=[i for i in issues if i[0] in ("high","med")]
    for s,d,m in hm: print(f"  [{s.upper()}][{d}] {m}")
    if not hm: print("  (none)")
    print("\n=== LOW ISSUES (sample, for polish) ===")
    for s,d,m in [i for i in issues if i[0]=="low"][:60]: print(f"  [{d}] {m}")

if __name__=="__main__":
    main()
