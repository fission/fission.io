+++
title = "Running GPU based Functions on Fission"
date = "2024-09-19T13:20:34+05:30"
author = "Md Soharab Ansari"
description = "Do you want to run GPU based serverless functions on Fission?"
categories = ["Tutorials"]
type = "blog"
images = ["/images/featured/serverless-developer.png"]
+++

Fission provides you with a serverless framework that you can deploy on your Kubernetes clusters.
There are various use cases where you can use Fission, and today we'll show you how to deploy a GPU based function in Fission.

## GPU based Functions on Fission
We will create Fission's environment and builder images with all the depedncies installed for running a GPU based function. Then we will verify the GPU availability inside environment container by running a simple function.

We will also create a package using [sentiment analysis](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english) model from huggingface and then create a function using this package. Finally, we will run some test for this function.

So let’s get started!

## Pre Requisites
### Nvidia GPU
### Fission
Before you start working on this demo, you need to ensure that you have Fission installed and running on a Kubernetes cluster. You can refer to our [Fission Installation](https://fission.io/docs/installation/) guide for more.

## Steps
- Create a Python based environment and builder image for use with Fission with all pre-requisites for Nvidia GPU and Pytorch installed.
- Test the environment and builder image.
- Create a package using [sentiment analysis](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english) model from huggingface.
- Create a function and test the above package.

### Create environment and builder images
We will use [Pytorch](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch) container image provided by Nvidia and build our Python environment on top of this image. This container image contains the complete source of the version of PyTorch in /opt/pytorch. It is prebuilt and installed in the default Python environment (/usr/local/lib/python3.10/dist-packages/torch) in the container image. The container also includes [Cuda 12.6](https://docs.nvidia.com/deeplearning/frameworks/pytorch-release-notes/rel-24-08.html#rel-24-08).

> Note: `nvcr.io/nvidia/pytorch:24.08-py3` image size is ~10GB so creating env and builder images will take some time.
#### Create environment image
We will build the environment using our current [python](https://github.com/fission/environments/blob/master/python) environment's source code and dependencies.

- Replace the [Dockerfile](https://github.com/fission/environments/blob/master/python/Dockerfile) in [Python environments repository](https://github.com/fission/environments/tree/master/python) with following contents:

```bash
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
$ docker build -t USER/python-pytorch-env .
```

- Verify that image is created.
```bash
$ docker images | grep python-pytorch-env
sohrab/python-pytorch-env                   latest            1032fa124b2b   2 days ago      20.5GB
```

#### Create builder image
- Replace the [Dockerfile](https://github.com/fission/environments/blob/master/python/Dockerfile) in [Python environments repository](https://github.com/fission/environments/tree/master/python) with following contents:

```bash
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
$ docker build -t USER/python-pytorch-builder .
```

- Verify that image is created.
```bash
$ docker images | grep python-pytorch-builder
USER/python-pytorch-builder               latest            3fa2801dcb1d   2 days ago      20.5GB
```

#### Push the images to a Container Registry
- You can push the images to a container registry like GHCR or use them locally.
```bash
$ docker push REGISTRY/USER/python-pytorch-env
$ docker push REGISTRY/USER/python-pytorch-builder
```

- Alternatively, you can also use the existing images which I have built and pushed to GHCR already.
```bash
$ docker pull ghcr.io/soharab-ic/python-pytorch-env:latest
$ docker pull ghcr.io/soharab-ic/python-pytorch-builder:latest
```

### Test the Environment and Builder image
In this step, we will do following things:
- Create an environmnt in Fission using newly created environment and builder image.
- Edit the environment deployment and add GPU resources and nodeSelector to make environment pod schedule on GPU nodes.
- Create a function and verify the GPU availability inside the environment container.

#### Create Environment
- Create Python environment using `python-pytorch-env` and `python-pytorch-builder` images.
```bash
$ fission env create --name python --image ghcr.io/soharab-ic/python-pytorch-env --builder ghcr.io/soharab-ic/python-pytorch-builder --poolsize 1
```

#### Edit the Environment Deployment
- The `fission env create` command will create two deployments. One deployment named `poolmgr-python-default-*` for environment and another for builder named `python-*`.
- Edit the environment deployment and add GPU resources to `python` environment container. Update the `nodeSelector` for scheduling pods on a node with GPU resources.
```bash
resources:
  limits:
    nvidia.com/gpu: "1"
  requests:
    nvidia.com/gpu: "1"
```
```bash
nodeSelector:
  kubernetes.io/hostname: gpu-node03
```
- After edit, make sure that pods are schduled on GPU nodes and respective environment container spec have gpu resources.

#### Create a function to verify if GPU is available inside environment container
- Create a `cuda.py` file and add following contents:
```bash
import torch

def main():
    if torch.cuda.is_available():
        return "Cuda is available: "+torch.cuda.get_device_name(0)+"\n"
    else:
        return "Cuda is not available\n"

```
- Create the function with `fission function create` command.
```bash
$ fission fn create --name cuda --env python --code cuda.py
```

- Test the function
```bash
$ fission fn test --name cuda
Cuda is available: NVIDIA GeForce RTX 4090
```
Now, our environment pods are scheduled on GPU nodes and GPU is available inside environment container for further use.

### Create a Package
Fission environment is created and GPU is available for use with Fission function. Let's create a package using [sentiment analysis](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english) model from huggingface. Provided a sentence, the sentiment analysis model will tell us the sentiment associated with sentence is either `POSITIVE` or `NEGATIVE`. The package will have dependency on `transformers` and `numpy` modules. The tree structure of directory and contents of the file would look like:

```bash
sentiment/
├── __init__.py
├── build.sh
├── requirements.txt
└── sentiment.py
```
And the file contents:
- sentiment.py
```bash
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
$ chmod +x build.sh
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
Since we are working with a source package, we provided the build command. Once you create the package, the build process will start, and you can see the build logs with the fission package info command. Wait for the package build to succeed:
```bash
$ fission pkg info --name sentiment-pkg
```

### Create a function and test the package
Using the package in previous step, you can create a function. Since this package is already associated with a source archive, an environment and a build command, you don’t need to provide these while creating a function from this package.

#### Create the function
The only additional thing you’ll need to provide is the Function’s entrypoint:
```bash
$ fission fn create --name sentiment-fn --pkg sentiment-pkg --entrypoint "sentiment.main"
function 'sentiment-fn' created
```

#### Test the function
The function will accept HTTP Post request with body. Provide the sentence, you want to analyze in the request body.

Test the function:
```bash
$ fission fn test --name sentiment-fn --method POST --body "I am happy"
Sentiment: POSITIVE
$ fission fn test --name sentiment-fn --method POST --body "I am not happy"
Sentiment: NEGATIVE
```

## Conclusion
Congratulations! You have successfully deployed and executed a GPU based function on Fission. This was a simple tutorial to show you how you can use GPU in Fission environment. You are now ready to extend this example with your use case.

*Let us know what you're building?*

For any issues or clarification, you can reach out to the author.

## Want more?

More examples can be found in our [examples directory on GitHub](https://github.com/fission/examples/). Follow **[Fission on Twitter](https://www.twitter.com/fissionio)** for more updates!

---

**_Author:_**

[Md Soharab Ansari](https://www.linkedin.com/in/md-soharab-ansari)  **|**  Product Enginner - [InfraCloud Technologies](http://infracloud.io/)



