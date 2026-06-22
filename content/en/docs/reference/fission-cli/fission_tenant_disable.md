---
title: fission tenant disable
slug: fission_tenant_disable
url: /docs/reference/fission-cli/fission_tenant_disable/
---
## fission tenant disable

Offboard a namespace (delete its FissionTenant)

### Synopsis

Delete the FissionTenant for --namespace. Refuses if the namespace still has functions unless --force is given; user resources are left in place (they simply stop being served).

```
fission tenant disable [flags]
```

### Options

```
  -n, --namespace string   -n |:|: If present, the namespace scope for this CLI request
      --force              Disable the tenant even if it still has functions/triggers (they will stop being served)
  -h, --help               help for disable
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission tenant](/docs/reference/fission-cli/fission_tenant/)	 - Manage multi-namespace tenancy (onboard/offboard namespaces)

