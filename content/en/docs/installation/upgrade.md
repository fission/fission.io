---
title: "Upgrade Guide"
weight: 60
description: >
  Upgrade guidance 1.13 onwards
---

{{< notice warning >}}
Note: Fission upgrades cause a downtime as of now, however we try to minimize it. Please upvote the [issue#1856](https://github.com/fission/fission/issues/1856) so we can priortize fixing it.
{{< /notice >}}

## Upgrade to the latest Fission version

### Upgrade/Replace the CRDs

```sh
kubectl replace -k "github.com/fission/fission/crds/v1?ref={{% release-version %}}"
```

### Install the latest Fission CLI

Please make sure you have the latest CLI installed. Refer to [Fission CLI Installation]({{< ref "_index.en.md#install-fission-cli">}})

### Upgrade Fission chart

 Update the helm repo and upgrade by mentioning the namespace Fission is installed in :

```sh
export FISSION_NAMESPACE="fission"
helm repo update
helm upgrade --namespace $FISSION_NAMESPACE fission fission-charts/fission-all
```

_See [configuration](#configuration) below._

## Upgrade to 1.15.x release from 1.14.x release

With 1.15.x release, following changes are made:

- `fission-core` chart is removed
- `fission-all` chart is made similar `fission-core` chart
- In the `fission-all` chart, the following components are disabled which were enabled by default earlier. If you want to enable them, please use `--set` flag.

  - nats - Set `nats.enabled=true` to enable Fission Nats integration
  - influxdb - Set `influxdb.enabled=true` to enable Fission InfluxDB and logger component
  - prometheus - Set `prometheus.enabled=true` to install Prometheus with Fission
  - canaryDeployment - Set `canaryDeployment.enabled=true` to enable Canary Deployment

_See [configuration](#configuration) below._

### Migrating from `fission-core` chart to `fission-all` chart

`Fission-all` chart is now exactly similar to `fission-core` chart and can be used to migrate from `fission-core`.

If you are upgrading from the fission-core chart, you can use the following command to migrate with required changes.

```console
helm upgrade [RELEASE_NAME] fission-charts/fission-all --namespace fission
```

## Configuration

See [Customizing the Chart Before Installing](https://helm.sh/docs/intro/using_helm/#customizing-the-chart-before-installing). To see all configurable options with detailed comments:

```console
helm show values fission-charts/fission-all
```

You may also `helm show values` on chart's dependencies for additional options.
