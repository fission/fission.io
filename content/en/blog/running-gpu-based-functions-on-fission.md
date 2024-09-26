+++
title = "Running GPU based Functions on Fission"
date = "2024-09-26T00:00:34+05:30"
author = "Md Soharab Ansari"
description = "Do you want to run GPU based serverless functions on Fission?"
categories = ["Tutorials"]
type = "blog"
+++

With new advancements in AI, more people want to use GPU-based functions in serverless environments. Fission is a serverless framework that you can easily deploy on your Kubernetes clusters.

Fission helps users run their models for different tasks, such as image processing, video processing, and natural language processing.
Sometimes, you need special accelerators like GPUs to run these functions effectively.
In this guide, we will show you how to set up a GPU-enabled Fission environment and use it to run your GPU-based functions.

## Why run GPU based functions on Fission?

GPUs are efficient for SIMD (Single Instruction, Multiple Data) computations, which are commonly used in deep learning and matrix operations.
Many serverless workloads need to perform these operations, and GPUs can help you run them more efficiently.

Fission users have been using Fission for ML model deployment and various use cases, some of the organizations are using Fission for production workloads and need to run GPU-based functions to meet their performance requirements.

## Pre Requisites

### Kubernetes Cluster with GPU Nodes

You need a Kubernetes cluster with GPU nodes to run this demo.
We will schedule our environment and function pods on GPU nodes.
Please refer to [Kubernetes GPU Support](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/) for more details.

### Nvidia GPU Operator

[Nvidia GPU operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html) helps in managing GPU resources in Kubernetes cluster. It provides a way to configure and manage GPUs in Kubernetes.
You can refer to [Guide to NVIDIA GPU Operator in Kubernetes](https://www.infracloud.io/blogs/guide-to-nvidia-gpu-operator-in-kubernetes/).
You should have seen nodes with gpu label in your cluster.

```bash
$ kubectl get node -l nvidia.com/gpu.present=true
NAME           STATUS   ROLES    AGE   VERSION
infracloud01   Ready    <none>   48d   v1.30.2
infracloud02   Ready    <none>   81d   v1.30.2
infracloud03   Ready    <none>   81d   v1.30.2
```

### Fission

Before you start working on this demo, you need to ensure that you have Fission installed and running on a Kubernetes cluster. You can refer to our [Fission Installation](/docs/installation/) guide for more.

## Steps - GPU based Functions on Fission

Fission function need an environment to run the function code. For running GPU based functions, we need to create an environment which can leverage the GPU resources.

Following are the steps to create an environment with GPU support and run a GPU based function.

- We would create a Python based environment runtime and builder images with all the dependencies installed for running a GPU based function. E.g. Pytorch, Cuda, etc.
- Verify the environment and builder images are functional and can utilize the GPU resources.
- Create a function package using [sentiment analysis model from huggingface](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english) and then create a function using this package.
- Run the function and verify sentiment analysis for a given sentence.

So let’s get started!

### Setup Environment images for GPU based Functions

We will use [Pytorch image provided by Nvidia](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch) and build our Python environment on top of this image.
The container includes Pytorch and Cuda pre-installed with Python 3.10.

Please verify Pytorch and Cuda version compatibility with your use case according to your GPU models and driver versions.

> Note: `nvcr.io/nvidia/pytorch:24.08-py3` image size is ~10GB so creating env and builder images will take some time. You can pre-download the image on your gpu node to save time.

#### Environment runtime image

We will build the environment using our current [python](https://github.com/fission/environments/blob/master/python) environment's source code and dependencies.

- Replace the [Dockerfile](https://github.com/fission/environments/blob/master/python/Dockerfile) in [Python environments repository](https://github.com/fission/environments/tree/master/python) with following contents:

  ```dockerfile
  ARG PLATFORM=linux/amd64

  FROM --platform=${PLATFORM} nvcr.io/nvidia/pytorch:24.08-py3

  WORKDIR /app

  RUN apt-get update && apt-get install -y libev-dev libevdev2

  COPY requirements.txt /app
  RUN pip3 install -r requirements.txt

  COPY *.py /app/

  ENTRYPOINT ["python3"]
  CMD ["server.py"]
  ```

- Create `python-pytorch-env` image using this updated Dockerfile.

  ```bash
  docker build -t USER/python-pytorch-env .
  ```

- Verify that image is created.

  ```bash
  $ docker images | grep python-pytorch-env
  sohrab/python-pytorch-env                   latest            1032fa124b2b   2 days ago      20.5GB
  ```

#### Environment builder image

- Replace the [Dockerfile](https://github.com/fission/environments/blob/master/python/Dockerfile) in [Python environments repository](https://github.com/fission/environments/tree/master/python) with following contents:

  ```dockerfile
  ARG BUILDER_IMAGE=fission/builder
  ARG PLATFORM=linux/amd64

  FROM ${BUILDER_IMAGE}
  FROM --platform=${PLATFORM} nvcr.io/nvidia/pytorch:24.08-py3

  COPY --from=0 /builder /builder
  RUN apt-get update && apt-get install -y libev-dev libevdev2

  ADD defaultBuildCmd /usr/local/bin/build

  EXPOSE 8001
  ```

- Create `python-pytorch-builder` image using this updated Dockerfile.

  ```bash
  docker build -t USER/python-pytorch-builder .
  ```

- Verify that image is created.
  
  ```bash
  $ docker images | grep python-pytorch-builder
  USER/python-pytorch-builder               latest            3fa2801dcb1d   2 days ago      20.5GB
  ```

#### Push the images to a Container Registry

- You can push the images to a container registry like GHCR or use them locally.

  ```bash
  docker push REGISTRY/USER/python-pytorch-env
  docker push REGISTRY/USER/python-pytorch-builder
  ```

- Alternatively, you can also use the existing images which I have built and pushed to GHCR already.

  ```bash
  docker pull ghcr.io/soharab-ic/python-pytorch-env:latest
  docker pull ghcr.io/soharab-ic/python-pytorch-builder:latest
  ```

### Verify the Environment with GPU

In this step, we will do following things:

- Create an environmnt in Fission using newly created environment and builder image.
- Patch the environment spec and add GPU resources to the environment.
- Create a function and verify the GPU availability inside the environment container.

#### Fission Environment creation

- Create Python environment using `python-pytorch-env` and `python-pytorch-builder` images.
  
  ```bash
  fission env create --name python --image ghcr.io/soharab-ic/python-pytorch-env --builder ghcr.io/soharab-ic/python-pytorch-builder --poolsize 1
  ```

- Patch the environment spec and add GPU resources to `python` environment using `kubectl patch` command.

  ```bash
  kubectl patch environment python --type='json' -p='[{"op": "replace", "path": "/spec/resources", "value": {"limits": {"nvidia.com/gpu": "1"}, "requests": {"nvidia.com/gpu": "1"}}}]'
  ```

- After patch, make sure that respective environment pods have gpu resources.

#### Check Cuda device with a Fission Function

- Create a `cuda.py` file and add following contents:

  ```python
  import torch

  def main():
      if torch.cuda.is_available():
          return "Cuda is available: "+torch.cuda.get_device_name(0)+"\n"
      else:
          return "Cuda is not available\n"

  ```

- Create the function with `fission function create` command.

  ```bash
  fission fn create --name cuda --env python --code cuda.py
  ```

- Test the function
  
  ```bash
  $ fission fn test --name cuda
  Cuda is available: NVIDIA GeForce RTX 4090
  ```

Now, our environment pods have GPU available inside environment container for further use.

### Deploy Sentiment Analysis Model

Fission environment is created and GPU is available for use with Fission function. Let's create a package using [sentiment analysis](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english) model from huggingface.
Provided a sentence, the sentiment analysis model will tell us the sentiment associated with sentence is either `POSITIVE` or `NEGATIVE`.
The package will have dependency on `transformers` and `numpy` modules. The tree structure of directory and contents of the file would look like:

  ```bash
  sentiment/
  ├── __init__.py
  ├── build.sh
  ├── requirements.txt
  └── sentiment.py
  ```

And the file contents:

- sentiment.py

  ```python
  import torch
  from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
  from flask import request

  def main():
      if request.method != "POST":
          return "Method Not Allowed\n", 405

      sentence = request.get_data(as_text=True)
      if sentence == "":
          return "Please provide a sentence for the analysis.\n", 400

      tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
      model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
      inputs = tokenizer(sentence, return_tensors="pt")
      with torch.no_grad():
          logits = model(**inputs).logits

      predicted_class_id = logits.argmax().item()
      return "Sentiment: " + model.config.id2label[predicted_class_id] + "\n"

  ```

- requirements.txt

  ```bash
  numpy==1.26.2
  transformers==4.44.2
  ```

- build.sh

  ```bash
  #!/bin/sh
  pip3 install -r ${SRC_PKG}/requirements.txt -t ${SRC_PKG} && cp -r ${SRC_PKG} ${DEPLOY_PKG}
  ```

- `__init__.py` will be empty.

Make sure the `build.sh` file is executable:

  ```bash
  chmod +x build.sh
  ```

- Archive these files:

  ```bash
  $ zip -jr sentiment-src-pkg.zip sentiment/
    adding: sentiment.py (deflated 51%)
    adding: requirements.txt (stored 0%)
    adding: build.sh (deflated 24%)
    adding: __init__.py (stored 0%)
  ```

Using the source archive created in previous step, let's create a package in Fission:

```bash
$ fission package create --name sentiment-pkg --sourcearchive sentiment-src-pkg.zip --env python --buildcmd "./build.sh"
Package 'sentiment-pkg' created
```

Since we are working with a source package, we provided the build command.
Once you create the package, the build process will start, and you can see the build logs with the fission package info command.
Wait for the package build to succeed:

```bash
fission pkg info --name sentiment-pkg
```

Create a function using the package, notice are passing `sentiment.main` as entrypoint.

```bash
$ fission fn create --name sentiment-fn --pkg sentiment-pkg --entrypoint "sentiment.main"
function 'sentiment-fn' created
```

#### Invoke deployed model through function

The function will accept HTTP Post request with body. Provide the sentence, you want to analyze in the request body.

Test the function:

```bash
$ fission fn test --name sentiment-fn --method POST --body "I am happy"
Sentiment: POSITIVE
$ fission fn test --name sentiment-fn --method POST --body "I am not happy"
Sentiment: NEGATIVE
```

## Conclusion

This tutorial shows how to set up a GPU based environment and run a GPU based function on Fission.
Similar steps can be followed to deploy other models and use cases with GPU acceleration.
We will soon be adding more examples with different models and use cases.

*Let us know what you're building?*

For any issues or clarification, you can reach out to the author.

## Want more?

More examples can be found in our [examples directory on GitHub](https://github.com/fission/examples/). Follow **[Fission on Twitter](https://www.twitter.com/fissionio)** for more updates!

---

***Author:***

[Md Soharab Ansari](https://www.linkedin.com/in/md-soharab-ansari)  **|**  Product Enginner - [InfraCloud Technologies](http://infracloud.io/)
