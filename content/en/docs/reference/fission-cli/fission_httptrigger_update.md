---
title: fission httptrigger update
slug: fission_httptrigger_update
url: /docs/reference/fission-cli/fission_httptrigger_update/
---
## fission httptrigger update

Update an HTTP trigger

```
fission httptrigger update [flags]
```

### Options

```
      --name string                     HTTP trigger name
      --url string                      URL pattern (See gorilla/mux supported patterns) [DEPRECATED for 'fn create', use 'route create' instead]
      --function stringArray            Name(s) of the function for this trigger. (If 2 functions are supplied with this flag, traffic gets routed to them based on weights supplied with --weight flag.)
      --method stringArray              HTTP Methods: GET,POST,PUT,DELETE,HEAD. To mention single method: --method GET and for multiple methods --method GET --method POST. [DEPRECATED for 'fn create', use 'route create' instead] (default [GET])
      --createingress                   Creates ingress with same URL
      --ingressrule string              Host for Ingress rule: --ingressrule host=path (the format of host/path depends on what ingress controller you used)
      --ingressannotation stringArray   Annotation for Ingress: --ingressannotation key=value (the format of annotation depends on what ingress controller you used)
      --ingresstls string               Name of the Secret contains TLS key and crt for Ingress (the usability of TLS features depends on what ingress controller you used)
      --weight ints                     Weight for each function supplied with --function flag, in the same order. Used for canary deployment
      --prefix string                   Prefix with which functions are exposed. NOTE: Prefix takes precedence over URL/RelativeURL [DEPRECATED for 'fn create', use 'route create' instead]
      --keepprefix                      Keep the prefix in the URL while forwarding request to the function
  -h, --help                            help for update
```

### Options inherited from parent commands

```
      --kube-context string   Kubernetes context to be used for the execution of Fission commands
  -n, --namespace string      -n |:|: If present, the namespace scope for this CLI request
      --server string         Server URL
  -v, --verbosity int         -v |:|: CLI verbosity (0 is quiet, 1 is the default, 2 is verbose) (default 1)
```

### SEE ALSO

* [fission httptrigger](/docs/reference/fission-cli/fission_httptrigger/)	 - Create, update and manage HTTP triggers

