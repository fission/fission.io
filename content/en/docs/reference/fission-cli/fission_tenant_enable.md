---
title: fission tenant enable
slug: fission_tenant_enable
url: /docs/reference/fission-cli/fission_tenant_enable/
---
## fission tenant enable

Onboard a namespace as a Fission tenant

### Synopsis

Create (or update) the FissionTenant for --namespace so Fission manages functions and builders there. Idempotent.

```
fission tenant enable [flags]
```

### Options

```
  -n, --namespace string            -n |:|: If present, the namespace scope for this CLI request
      --function-namespace string   Namespace where this tenant's function pods run (defaults to the tenant namespace)
      --builder-namespace string    Namespace where this tenant's builder pods run (defaults to the tenant namespace)
  -h, --help                        help for enable
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission tenant](/docs/reference/fission-cli/fission_tenant/)	 - Manage multi-namespace tenancy (onboard/offboard namespaces)

