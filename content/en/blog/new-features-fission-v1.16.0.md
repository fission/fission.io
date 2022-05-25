+++
title = "New Features in Fission: Health Check, Authentication & Much More"
date = "2022-05-24T01:05:00-07:00"
author = "Atulpriya Sharma"
description = "New Features in Fission: Custom Metrics, Authentication & Much More"
categories = ["Fission"]
type = "blog"
+++

The best part of being an open source project is that there so many opportunities to improve.
People from all over the world come together and contribute to make a project better.
And we’re thankful to our amazing community that has helped us make Fission better over time.
We are happy to announce a **new version of Fission - v1.16.0** that brings exciting new features, bug fixes and enhancements.

In this blog post, I’ll throw light on these features and how you can use them.

## 6 New Features in Fission v.1.16.0

This release comes with 6 new features.
Most of these features were requested by the community, and we’re glad that a few of them came forward and implemented those features.
Hence, without much ado, let’s go straight into the 6 new features in Fission.

{{< figure src="/images/featured/fission-new-features-v1.16.0.png" alt="New Fission Features Released v1.16.0" height="400" width="600">}}

### Autoscaling functions with Custom metrics

In our previous releases, whenever you create a function based on newdeploy or container executor type, it would scale up or down according to the load which was determined by the metric `targetCPU`.
There was no way you could scale on the basis of metrics like number of messages in a queue, number of requests etc.
In our latest release, you can now provide `hpaMetrics` in the function spec file which will allow scaling based on any metric the user has exposed.
If you are interested in knowing more about this feature, you can go through this [blog](https://fission.io/blog/autoscaling-serverless-functions-with-custom-metrics/).

### Authentication for Fission Function Calls

Prior to this release, users didn’t have any mechanism in place to authenticate function calls.
The only authentication that was available was via means of [ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/).
Hence, if a user didn’t use an ingress, Fission didn’t offer any authentication mechanism out of the box.

In this release, we've introduced an **authentication mechanism for all function calls**.
Though it’s an optional feature, we recommend you use it and have only authenticated requests reach your functions.

```bash
curl http://localhost:8888/hello -H "Authorization: Bearer ${FISSION_AUTH_TOKEN}"
hello, world!
```

You generate an `authentication token` and pass it with your API calls to your functions.
Only if there’s a valid token the request will be processed, else it will return a `HTTP 401` error.
We have detailed documentation on using [authentication for fission function](docs/installation/authentication/), you should check it out to understand this better.

### Fission Services Check

Sometimes when you’re deploying Fission on a new cluster or creating a new function, you might hit a roadblock.
Most of the time it’s because the **underlying environment is not ready** or some component is missing or misconfigured.

To overcome this issue, the latest version introduced **Fission Services Check**.
With a couple of basic commands, you can see the health of the environment and whether all the services are running as expected.
You can now check the status of the environment using fission `check` command which will list down the status of Fission services.

```bash
$ fission check

fission-services
--------------------
√ controller is running fine
√ executor is running fine
√ router is running fine
× storagesvc deployment is not running

fission-version
--------------------
√ fission is up-to-date
```

This is extremely helpful and handy while troubleshooting.
Check our detailed guide on this in our [Troubleshooting Fission](docs/trouble-shooting/setup/fission/) document.

### Commit Labels for Fission Spec

One of the easiest ways to deploy your application Fission is using [Fission Spec](/docs/usage/spec/).
It’s a collection of commands that instruct the Fission CLI to set up the environment, functions, packages etc. that is required to run an application.

However, in practical scenarios, the application is never deployed in a single go.
It’s usually iterated multiple times maybe due to feature additions or bug fixes.
While using fission `spec apply` command, it wasn’t possible to **keep a track of which version of the code is actually deployed**.

To overcome this, we’ve implemented a feature to append `--commitlabel` to `fission spec apply`.
Whenever a fission spec apply command is executed, a label called `commit` is appended to all spec resources present in specdir.
The value will be the `commitId` from the respective repository `HEAD`.

The value of the `commit` label for different status of the file is as follows:

| Git Gile Status                       | Label Value           |
|---------------------------------------|-----------------------|
| New untracked file                    | `untracked`           |
| New staged file                       | `staged`              |
| Tracked file with changes in worktree | `<commitID>-unstaged` |
| Tracked file with changes staged      | `<commitID>-staged`   |
| Tracked file with clean commit        | `<commitID>`          |

### Fission metrics

Debugging is quite a hard process and it might be time consumimg if you have no idea what caused the error.
To make things a bit easier, we have added new prometheus metrics in our latest version which will provide better insights into fission.
We have some metrics like `http_requests_total`, `http_requests_in_flight` etc. which are common to all fission components.
Other than that, we have added some specific metrics for each of the components. For example, we have added `fission_archive_memory_bytes` to keep track of total memory consumed currently by archives in the `storagesvc` component.
Lastly, there are some default metrics provided by the Go language like `go_goroutines` which tell you number of goroutines currently existing.
To access the metrics, you just need to install prometheus on the cluster.
You can install prometheus using [prometheus-community/prometheus](https://artifacthub.io/packages/helm/prometheus-community/prometheus) or [prometheus-community/kube-prometheus-stack](https://artifacthub.io/packages/helm/prometheus-community/kube-prometheus-stack).
We'll be releasing a blog soon listing all the metrics.

### Fission Spec CLI Support

A couple of minor feature additions were done to the Fission Spec CLI commands.

One of the concerns was that when any Fission CRD is deleted and if the resources are not found, the command exits with non-zero error code.
Considering the **need for graceful exit**, we’ve added a new `--ignorenotfound` flag that returns a zero exit status even if the resource is not found.

Another one is regarding Fission resources via specs.
When a resource is already deployed with fission spec, and we are trying to deploy it with some other deployment, then the command fails due to conflict.
To allow this behavior, the `--force` flag was added that would allow you to include the existing resources in the new deployment.

## Tried Fission Yet?

Fission is one amongst the few **open source serverless frameworks available for Kubernetes**.
You can use Fission to build serverless backends, implement webhooks or even create Kubernetes watch triggers.
All of this can be done on your private Kubernetes cluster or on any public cloud Kubernetes offering.

With the addition of these new features, you can take advantage of Fission and develop more secure and flexible applications.
To view the complete list of changes, read our [v1.16.0 release documentation](docs/releases/v1.16.0/).

To help you get started, we have quite a few sample codes in the [Fission Example Repository](https://github.com/fission/examples) that you must check and try.
If you have any issues or suggestions, share them with us.
Join our [Fission Slack](https://fission.io/slack) channel or DM us [@Fissionio](https://twitter.com/fissionio) on Twitter if you’ve any queries around this.

---

**_Author:_**

[Atulpriya Sharma](https://twitter.com/TheTechMaharaj)  **|**  Developer Advocate - [InfraCloud Technologies](http://infracloud.io/)
