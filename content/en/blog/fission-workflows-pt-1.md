+++
title = "Getting Started: Composing Serverless Functions with Fission Workflows (Part 1)"
date = "2018-03-27T04:25:55-07:00"
author = "Erwin Van Eyk"
description = "Composing Fission functions with Fission Workflows (Part 1)"
categories = ["Fission"]
type = "blog"
+++


_This is the first of a 2-part introduction to Fission Workflows._


Fission provides fast serverless functions on Kubernetes. While functions are great for specific pieces of business logic, any non-trivial application requires a composition of functions.

There are many ways to compose functions. You can directly call functions from each other — but there are some disadvantages to this. For one, the structure of the application becomes hard to understand; dependencies are not obvious; essentially, every function becomes an API. Second, there’s no persistent state; if there’s a failure or exception and you want to retry, the whole function must run again.  

Alternatively, you can wire up a set of functions using message queues to send the output of one function to a message topic that triggers another function. While this helps with persistence and retries (because you can retry individual functions rather than the whole composition), it doesn’t help at all with making the system easier to understand. It’s also hard to replicate any dynamic control flow (such as an if statement or a loop).


## Workflows
A third way to compose Fission functions is using _**workflows**_. Think of a flowchart: a sequence of tasks, decisions, loops and so on. A flowchart makes the structure of a complex task obvious. 

Workflows are like flowcharts for serverless functions, except they’re more powerful. You can compose together functions in sequence or in parallel, send the output of a function to the inputs of another, write if statements, loops, and even functions that operate on other functions.

### Use cases, Demos, Examples

Broadly we see a few areas where workflows are useful:

- **Devops automation use cases**
- **Data processing use cases**
- **Business process automation**


### Demos

- [Slack Weather Example](https://github.com/fission/fission-workflows/tree/master/examples/slackweather): Notifies users on Slack of the weather conditions of a given location. 

![flowchart-1](/images/slack-fchart.png)


![slack-image](/images/slack-msg-image.png)


**_[Find more cool demos/examples of apps built using Fission Workflows here](https://github.com/fission/fission-workflows/tree/master/examples)_**.


---


## Terminology/Concepts

Here are a few terms and concepts that you should know in order to better understand workflows.

A _**Task**_ is a unit of computation within a workflow. Most commonly, it is a function call. It takes in data input and outputs the resulting data or error. A task can specify its input using a Javascript expression; this allows inline transformations of data from the output of other tasks. A workflow is defined as a list of tasks.

_A task can have a **dependency** on one or more other tasks. With dependencies you can manipulate the control flow within a workflow._

A _**Dynamic Task**_ can manipulate control flow. For example, it could be an if-statement, a loop, etc. A dynamic task is just a regular task that returns another task instead of data. Users can extend workflows by writing their own dynamic tasks.

_Control flow constructs_ are available as dynamic tasks. For example, an “if” dynamic task checks the value of an expression and executes one of two tasks given to it.

Workflows themselves are Fission functions — this allows workflows to be triggered the same way as any other function.

Workflows are specified in _**YAML**_. 

_Below is an example of the specifications of a workflow, from the Slack Weather application, in YAML._


![yaml-image-1](/images/yaml-ex-1.png)



---

## Rationale: Code or Data?

Should a workflow be specified as code or data? Code provides more flexibility: why would anyone want to write an if-statement in YAML?

However, writing a workflow as a data structure does have two big advantages: 

- _**Analyzability**_: Arbitrary code is hard to analyze. But if a workflow is a data structure, the system can analyze it and reason about it as a whole. For example, it knows up-front what set of functions make up the workflow — which makes things like upgrades much easier.  

- _**Usability**_: You can make a workflow without doing any coding at all. Along with the fission function library, this opens up the usage of serverless functions to a large set of people who aren’t comfortable writing large amounts of complex code.

We went with something of a hybrid. Though the workflow definition is a static list of tasks, there are two dynamic properties in workflows:

1. **Inputs to tasks are specified as Javascript expressions**

2. **Dynamic tasks. Fission comes with loops, conditionals, and the map function built-in. Users can also define their own dynamic tasks.**

We think this approach is the best of both worlds: we get the advantages of workflows-as-data, but with a lot more flexibility than simple static workflows.


Stay tuned for **[Part 2](/blog/getting-started-composing-serverless-functions-with-fission-workflows-part-2/)** of this post, as we dive deeper into the potential of Fission Workflows, what implementation looks like, and how it makes serverless application development that much easier.

_In the meantime, feel free to [**join the Fission community**](/)!_

---


**_Authors:_**

* Soam Vasani **|** Senior Software Engineer, Platform9 Systems **|** [Tweet the Author](https://www.twitter.com/soamv)

* Timirah James **|** Fission Developer Advocate, Platform9 Systems  **|**  [Tweet the Author](https://www.twitter.com/timirahj)

* Erwin Van Eyk **|** Software Engineer Intern, Platform9 Systems **|** [Tweet the Author](https://www.twitter.com/erwinvaneyk)


