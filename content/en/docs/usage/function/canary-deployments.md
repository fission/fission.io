---
title: "Canary Deployments for Functions"
draft: false
weight: 49
description: >
  Gradually shift HTTP traffic to a new function version with a CanaryConfig, using Prometheus health checks to auto-rollback on failure.
---

**A CanaryConfig gradually shifts HTTP traffic to a new function version, using Prometheus health checks to roll back automatically if the new version becomes unhealthy.**
Traffic starts at 0% and increases in steps up to 100%, unless the failure threshold is exceeded first.

### Setup & pre-requisites

Enable the canary feature by setting `canaryDeployment.enabled` to `true` in the Helm chart during Fission installation.

The feature relies on **Prometheus** metrics to judge the health of the new version of the function.
Point Fission at your Prometheus by setting the `prometheus.serviceEndpoint` Helm value to a Prometheus URL that is reachable from inside the cluster.
You can reuse an existing Prometheus deployment or install one alongside Fission.
If no reachable Prometheus endpoint is configured, the canary deployment feature cannot evaluate function health and rollouts will not progress.

#### Canary Config parameters

A Canary Config has the following parameters:

| Parameter | Description |
|---|---|
| `duration` | How frequently user traffic is incremented for the new version of the function |
| `failurethreshold` | The percentage threshold beyond which the new version of a function is declared unhealthy |
| `newfunction` | Name of the latest version of the function |
| `oldfunction` | Name of the current stable version of the function |
| `trigger` | Name of the HTTP trigger object |
| `weightincrement` | Percentage increase of user traffic toward the new version at each step |
| `failureType` | How the health of the new version is checked. The only supported type is `status-code` (the HTTP status code), so a function that returns a status code other than 200 is considered unhealthy. Set in the CanaryConfig spec — the CLI does not expose a flag for it. |

For example, suppose the current stable version of a function is `fn-a-v1` and the new version is `fn-a-v2`.
We want to increment traffic towards the new version in steps of 30% every 1m, with a failure threshold of 10%.
The sample canary config below captures this.

```yaml
apiVersion: fission.io/v1
kind: CanaryConfig
metadata:
  name: canary-1
  namespace: default
spec:
  duration: 1m
  failureType: status-code
  failurethreshold: 10
  newfunction: fn-a-v2
  oldfunction: fn-a-v1
  trigger: route-fn-a
  weightincrement: 30
```

Every 1m, the percentage of failed requests to `fn-a-v2` is calculated from Prometheus metrics.
If it is under the configured failure threshold of 10%, the traffic to `fn-a-v2` is incremented by 30%.
This cycle repeats until either the failure threshold is reached (the deployment is rolled back) or `fn-a-v2` is receiving 100% of user traffic.

#### Steps to setup a canary config

1. Create an environment:

  ```bash
  $ fission env create --name nodejs --image ghcr.io/fission/node-env
  ```

2. Create fission functions:

```bash
$ fission fn create --name fna-v1 --code hello.js --env nodejs
$ fission fn create --name fna-v2 --code hello2.js --env nodejs
```

3. Create an http trigger to these functions:

```bash
$ fission route create --name route-fn-a --function fna-v1 --weight 100 --function fna-v2 --weight 0 --url /hello2
```

4. Create a canary config:

```bash
$ fission canary create --name canary-1 --newfunction fna-v2 --oldfunction fna-v1 --httptrigger route-fn-a --increment-step 30 --increment-interval 1m --failure-threshold 10
```

{{% notice info %}}
`fission canary-config` is a valid alias for `fission canary`, so older commands such as `fission canary-config create` still work.
{{% /notice %}}

#### Steps to verify the status of a canary deployment

Check the status of the canary deployment of the new version of the function:

```bash
$ fission canary get --name canary-1
```

The status is one of:

| Status | Meaning |
|---|---|
| `Pending` | The canary deployment is in progress |
| `Succeeded` | The new version of the function is receiving 100% of the user traffic |
| `Failed` | The failure threshold was reached, so 100% of the traffic was routed back to the old version of the function (rollback) |
| `Aborted` | There were some failures during the canary deployment |

#### Running canaries faster than the default scrape interval

The `scrape_interval` for Prometheus server is 1m by default.
If the "duration" parameter needs to be less than 1m, the `scrape_interval` parameter needs to configured to a much lower value.
This can be done by updating the config map for prometheus server.
Updating the config map is enough; the prometheus server does not need to be restarted.
