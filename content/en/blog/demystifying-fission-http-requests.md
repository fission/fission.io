+++
title = "Demystifying Fission - HTTP Requests in Fission"
date = "2022-03-17T09:30:34+05:30"
author = "Atulpriya Sharma"
description = "Understand how http requests work with Fission functions."
categories = ["Fission"]
type = "blog"
images = ["images/featured/demystifying-fission-http-requests.png"]
+++

The first ever message that was sent from one computer to another was "lo" on the ARPRANET in 1969.
That one message was a stepping stone to the modern day emails, instant messages and the Internet.
In today's blog post in our Demystifying Fission series, we are going to talk about how Fission handles HTTP requests and routes them to functions.

But before we dive into it, let us do some revision, shall we?

{{< figure src="/images/featured/demystifying-fission-http-requests.png" alt="HTTP requests in Fission" height="600" width="800">}} HTTP requests in Fission

## Hypertext Transfer Portocol - HTTP

The foundation of the modern day internet is Hypertext Transfer Protocol - HTTP.
An application layer protocol, HTTP allows two networked devices to communicate with each other.
A typical HTTP flow involves a client and a server.
The client makes a request to the server that returns a response back to the client with the response data.
So when you fired up google.com, you actually *requested* the server to *respond* with Google's home page.

{{< figure src="https://media.geeksforgeeks.org/wp-content/uploads/20210905091508/ImageOfHTTPRequestResponse-660x374.png" alt="Simple HTTP Request Response architecture. Courtesy: geeksforgeeks.org" height="400" width="600">}} Simple HTTP Request Response architecture. Courtesy: geeksforgeeks.org"

### HTTP Request

HTTP requests are a way clients like web browsers communicate with web servers to load a website.
Each request has a set of encoded data that carries different types of information that helps the web server understand the request and revert with a required response.

- **HTTP version type**: *HTTP protocol version - HTTP/1.0, HTTP/1.1, HTTP/2 etc.*
- **URL**: *actual URL requested*
- **HTTP Method**: *set of methods that indicate what action to be performed - GET, POST, DELETE etc.*
- **HTTP Request Headers**: *key-value based information part of every request that provide context of the request*

### HTTP Response

Every HTTP request sent to the server is served with a response.
The response you receive from the server contains the data you requested for.
The response also has some more information along with the data requested for.

- **HTTP Status Code**: *3-digit codes used to indicate the status of an HTTP request.*
- **HTTP Response Headers**: *Just like HTTP Request Headers, these are key-value based information providing additional context to the response.*

## Fission Functions

If there's one place where all the action takes place in Fission, it is a Fission function.
A Fission function is a piece of user defined code that is executed in response to an event.
These events are used by triggers that *trigger* a function based on the event.
Fission offers a variety of triggers including:

- HTTP Trigger
- Time Trigger
- Message Queue Trigger
- Kubernetes Watch Trigger

Read more about [Fission Triggers](/docs/concepts/#triggers).

You must now be wondering, **how does a trigger *trigger* a function?**
That's the job of the [Fission Router](/docs/architecture/router).

Fission Router acts as a bridge between triggers and functions.
It forwards HTTP requests to function pods.
If a function pod is already running, the router will route the request to the pod, else it will request for one from the [executor](/docs/architecture/executor).

{{< figure src="https://platform9.com/wp-content/uploads/2019/01/diagram_how-fission-works.png" alt="Fission architecture. Courtesy: platform9.com" height="600" width="800">}} Fission architecture. Courtesy: platform9.com

### How Fission maps HTTP requests to user function

Having understood the basics of HTTP and how requests are forwarded to Fission functions, let us now understand how Fission maps HTTP requests to user functions.
Here is a brief diagram describes how requests being sent to function inside Kubernetes cluster.

![router maps req to fn](/images/how-to-develop-a-serverless-application-with-fission/router-maps-request-to-fn.svg)

The requests will first come to the `router` and it checks whether the destination `URL` and `HTTP method` are registered by `http trigger`.
Once both are matched, router will then proxy request to the function pod (a pod specialized with function pointed by http trigger) to get response from it; reject, otherwise.

#### What's Content of Request Payload

Now, we know how a request being proxied to the user function, there are some questions you might want to ask:

1. Will `router` modify http request?
2. What's the payload that will be passed to the function?

To answer these questions, let's create a python function that returns HTTP `Header`, `Query String` and `Message Body` to see what's inside of a request sent to user function.

* requestdata.py
  
```python
from flask import request
from flask import current_app

def main():
    current_app.logger.info("Received request")
    msg = "\n---HEADERS---\n%s\n---QUERY STRING---\n%s\n\n--BODY--\n%s\n-----\n" % (request.headers, request.query_string, request.get_data())
    return msg
```

```bash
$ fission env create --name pythonv1 --image fission/python-env:0.9.2 --version 1 --period 5

# With flag --method and --url, we can create a function and an HTTP trigger at the same time. 
$ fission fn create --name reqpayload --env pythonv1 \
    --code requestdata.py --method POST --url "/test/{foobar}"

$ curl -X POST -d '{"test": "foo"}' \
    -H "Content-Type: application/json" \
    "http://${FISSION_ROUTER}/test/pathvar?foo=bar"
```

**NOTE**: For how to set up `$FISSION_ROUTER`, please visit [here](/docs/installation/env_vars/)

#### Request Payload

```html
---HEADERS---
Accept-Encoding: gzip
Host: 172.17.0.25:8888
Connection: close
Accept: */*
User-Agent: curl/7.54.0
Content-Length: 15
Content-Type: application/json
X-Forwarded-For: 172.17.0.1
X-Fission-Function-Uid: 82c95606-9afa-11e8-bbd1-08002720b796
X-Fission-Function-Resourceversion: 480652
X-Fission-Function-Name: reqpayload
X-Fission-Function-Namespace: default
X-Fission-Params-Foobar: pathvar

---QUERY STRING---
b'foo=bar'

--BODY--
b'{"test": "foo"}'
-----
```

As you can see, the router leaves `query string` and `body` parts intact, so you can access the value as usual.
On the other hand, some `header` fields were changed/added to the payload. Let's see from where these values came from.

**Fields Changed**

* `Host`: Originally, host is the address to the fission router. The value was replaced with the address of function pod or the kubernetes service address of the function.

* `X-Forwarded-For`: The address of docker network interface was added during proxy stage.

**Fields Added**

* `X-Fission-Function-*`: The metadata of function that processed the request.

* `X-Fission-Params-*`: The path parameters specified in http trigger url. One thing worth noticing is that the name of parameter will be replaced by the URL.

For example, `{foobar}` in `"/test/{foobar}"` will be converted and added to request header with header key `X-Fission-Params-Foobar`.

## Conclusion

Many of you would have created Fission functions, but we're sure you wouldn't have known about this.
HTTP triggers are one of the most popular ways to trigger a Fission function.
Understanding how Fission processes these requests and responses, will make it easier for you develop your application on Fission.
Moreover, with this understanding, debugging or troubleshooting your Fission functions would be a faster and easier.

**Demystifying Fission** is our series of blog posts on topics that'll help you understand Fission better.
Do check out our other posts in the Demystifying Fission series:

- [Understanding Pool Manager](/blog/demystifying-fission-pool-manager)
- [Understanding New Deploy](/blog/demystifying-fission-new-deploy)

Join [Fission Slack](https://fission.io/slack) channel or [Tweet to Us](https://twitter.com/fissionio) and we should be more than happy to help!

---

**_Author:_**

[Atulpriya Sharma](https://twitter.com/TheTechMaharaj)  **|**  Developer Advocate - [InfraCloud Technologies](http://infracloud.io/)