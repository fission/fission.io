---
title: fission alias create
slug: fission_alias_create
url: /docs/reference/fission-cli/fission_alias_create/
---
## fission alias create

Create a function alias

```
fission alias create [flags]
```

### Options

```
      --name string                Name for the function alias
      --function string            Function this alias points at
      --version string             FunctionVersion name the alias resolves to (exactly one of --version/--package-digest)
      --package-digest string      Package digest (sha256:<hex>) the alias resolves to declaratively (exactly one of --version/--package-digest)
      --weight int                 Percentage (0-100) of traffic served by the primary target; the remainder goes to --secondary-version. Requires --secondary-version; omit --weight entirely for 100% to the primary
      --secondary-version string   Secondary FunctionVersion name receiving the 100-minus-weight remainder of traffic
      --wait                       Wait for the alias to resolve to its updated target (see --timeout)
      --timeout duration           Maximum time to wait for the condition before giving up (default 1m0s)
  -h, --help                       help for create
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission alias](/docs/reference/fission-cli/fission_alias/)	 - Create, update and manage function aliases

