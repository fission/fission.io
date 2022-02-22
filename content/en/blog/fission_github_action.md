+++
title = "New! Fission GitHub Action: Easily Automate Your CI/CD Workflows"
date = "2019-04-25T18:30:53+05:30"
author = "Vishal Biyani"
description = "Easily deploy Fission functions with GitHub Actions"
categories = ["Tutorials"]
type = "blog"
+++

# Introduction

GitHub recently launched [GitHub Actions](https://github.com/features/actions) which enable developers to develop workflows and execute them based on events in code repositories such as a push event or an issue creation. 

There are many Actions available on the [Github marketplace](https://github.com/marketplace?type=actions) which you can use for automating various tasks and workflows around development and deployment. In this tutorial we will use the recently launched [Fission Action](https://github.com/marketplace/actions/fission) and build a simple workflow that deploys a Fission function to a Kubernetes cluster.

# Prerequisites

You will need a Kubernetes cluster with Fission installed. Please follow the [instructions here](/docs/installation/) for installing Fission in your Kubernetes cluster. Then, verify that the fission cli is working by using the `fission --version` command.

# Local Development

Let’s create a simple NodeJS function which prints “Hello World!” when invoked.

```
$ fission spec init
$ cat hello.js
module.exports = async function(context) {
    return {
        status: 200,
        body: "Hello, Fission!\n"
    };
}
$ fission env create --name node --image fission/node-env --spec
$ fission fn create --name hellonode --env node --code hello.js --spec
```

At this point we can apply the function specs and test the function. We now have a working function which we can commit to a GitHub repository.

```
$ fission spec apply
$ fission fn test --name hellonode
Hello World!
```

# CD workflow with Fission Action

The next step is to automate the deployment of the function to a cluster on every push. For this we will use a workflow that is based on a Fission action.

## Understanding Fission GitHub Action

First, a quick overview of what goes on behind the scenes of the Fission GitHub Action. The Fission Action is a container which has a Kubectl CLI, Kubeconfig template & Fission CLI built into it. The default entrypoint populates the Kubeconfig template based on the environment variables and then runs the fission spec apply command.


## Building a workflow with the Fission GitHub Action

Now using this Action - let’s build a simple workflow which will be triggered once there’s a code push and deploy/apply the functions. The workflow is defined in .github/main.workflow file in the same repository as code. You can check out more details and [options of GitHub workflow here](https://docs.github.com/en/actions/learn-github-actions/workflow-syntax-for-github-actions)


```
workflow "Fission CD" {
  on = "push"
  resolves = [
    "FissionCD",
  ]
}

action "FissionCD" {
  uses = "docker://fission/github-action:1.0.0"
  secrets = ["CERTIFICATE_AUTHORITY", "SERVER_ADDRESS", "USER_TOKEN"]
}

```


Push the code to a repository with the workflow definition. Assuming you have Git Hub Actions enabled in your repo, you will see an Action tab. You will notice that the workflow is marked as invalid and has errors. This is because it does not yet have values for the secrets.



![Workflow Error](/images/githubaction/github_workflow_error.png)

Edit the workflow and enter the values of the secrets required to execute the workflow. 

You can copy the value of the certificate authority, token and Kubernetes server address from Kubeconfig for the purpose of testing but ideally you’d want to use  a dedicated service account with the appropriate access. GitHub makes these secrets available to the containers running the workflow as environment variables.


![Workflow Secrets](/images/githubaction/workflow_secret.png)

Once you have entered all the secret values - save and commit the change to master. This will kick off the workflow and you will see it running and can then also check the logs:


![Workflow Secrets](/images/githubaction/workflow_running.png)

In the logs below, we can see that Fission Action applied the specs and the environment and that the function was created. You can test out the function now!

```
### STARTED FissionCD 15:16:50Z

Pulling image: gcr.io/github-actions-images/action-runner:latest
latest: Pulling from github-actions-images/action-runner
169185f82c45: Pulling fs layer
0ccde4b6b241: Pulling fs layer

..
..
..


8522a1fc57c5: Pull complete
Digest: sha256:43a18edb4167aca86e24424a985417a490e99a8b432aa75404e18cba56052176
Status: Downloaded newer image for vishalbiyani/fission-action:7
1 environment created: nodejs
1 package created: hello-js-cpdz
1 function created: nhello

### SUCCEEDED FissionCD 15:17:32Z (41.909s)
```

You can find the code used for the demo in [this GitHub repository](https://github.com/fission/action-demo) and can checkout logs for past [executions here](https://github.com/fission/action-demo/actions).


# There is more!

This tutorial covers the simplest application of the Fission GitHub Action to deploy functions. You can use Fission and other GitHub Actions to build powerful workflows and do a lot more. Try out the Fission GitHub Action to automate your other CI/CD processes and accelerate your development. Reach out to us up on [Slack](/slack) if you have any queries or interesting ideas that we can explore together.


--- 


**_Author:_**

* [Vishal Biyani](https://twitter.com/vishal_biyani)  **|**  [Fission Contributor](https://github.com/vishal-biyani)  **|**  CTO - [InfraCloud Technologies](http://infracloud.io/)