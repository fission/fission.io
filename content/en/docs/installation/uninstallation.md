---
title: "Uninstalling Fission"
linkTitle: Uninstallation
weight: 71
description: >
  Uninstallation guide for Fission
---
If you want to completely uninstall Fission from your cluster, the following command will help you do that.
This might be required in situations where in you want to uninstall the current version and [install Fission](/docs/installation/index.html) as a fresh instance.

```bash
helm delete --purge <release name>
```

> Get the release name by running `helm list` and replace with the actual `<release name>`

The above command will *only delete the installed services*. Custom resources that were created by Fission will need to be **manually deleted**.

Get a list of fission CRDs

```bash
kubectl get crd
```

```bash
NAME                                       CREATED AT
canaryconfigs.fission.io                   2022-01-17T05:47:28Z
environments.fission.io                    2022-01-17T05:47:29Z
functions.fission.io                       2022-01-17T05:47:29Z
httptriggers.fission.io                    2022-01-17T05:47:29Z
instrumentations.opentelemetry.io          2022-01-03T04:38:39Z
issuers.cert-manager.io                    2022-01-03T04:36:14Z
jaegers.jaegertracing.io                   2022-01-03T04:51:35Z
kuberneteswatchtriggers.fission.io         2022-01-17T05:47:29Z
messagequeuetriggers.fission.io            2022-01-17T05:47:29Z
opentelemetrycollectors.opentelemetry.io   2022-01-03T04:38:39Z
orders.acme.cert-manager.io                2022-01-03T04:36:15Z
packages.fission.io                        2022-01-17T05:47:30Z
timetriggers.fission.io                    2022-01-17T05:47:30Z

```

Delete individual CRD, replace `<crd-name>` with the actual CRD name

```bash
kubectl get <crd-name> -o name | xargs -n1 kubectl delete
```
