+++
title = "How to Develop a Serverless Application with Fission (Part 2)"
date = "2018-09-07T16:48:12+08:00"
author = "Ta-Ching Chen"
description = "Write serverless Java functions with JVM"
categories = ["Fission", "application"]
type = "post"
+++

# Introduction

[Part 1](/posts/how-to-develop-a-serverless-application-with-fission-pt-1) we talked about the advantage of adopting fission as serverless framework on 
kubernetes, basic concept of around fission core and how to create a simple HelloWorld example with fission.

In this post we'll dive deeper to see what's the payload of a HTTP request being passed to user function 
and learn how to create a guestbook application consists with REST functions in Golang.

# How Fission maps HTTP requests to user function

Before we diving into code, we first need to understand what exactly happened inside Fission. Here is a brief diagram describes how requests being sent to function inside Kubernetes cluster.

![router maps req to fn](/images/how-to-develop-a-serverless-application-with-fission/router-maps-request-to-fn.svg)

The requests will first come to the `router` and it checks whether the destination `URL` and `HTTP method` are registered by `http trigger`. 
Once both are matched, router will then proxy request to the function pod (a pod specialized with function pointed by http trigger) to get response from it; reject, otherwise.

# What's Content of Request Payload 

Now, we know how a request being proxied the user function, there are some questions you might want to ask:

1. Will `router` modify http request?
2. What's the payload will be passed to function?

To answer these questions, let's create a python function that returns HTTP `Header`, `Query String` and `Message Body`
to see what's inside of a request sent to user function.

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

# With flag --method and --url, we can create a function and a HTTP trigger at the same time. 
$ fission fn create --name reqpayload --env pythonv1 \
    --code requestdata.py --method POST --url "/test/{foobar}"

$ curl -X POST -d '{"test": "foo"}' \
    -H "Content-Type: application/json" \
    "http://${FISSION_ROUTER}/test/pathvar?foo=bar"
```

**NOTE**: For how to set up `$FISSION_ROUTER`, please visit https://docs.fission.io/latest/installation/env_vars/

## Request Payload

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

On the other hand, some `header` fields was changed/add to the payload, following we will explain where the value/fields came from.

**Fields Changed**

* `Host`: Originally, the host is address to the fission router. The value was replaced with the address of function pod or the kubernetes service address of function.

* `X-Forwarded-For`: The address of docker network interface was added during proxy stage.

**Fields Added**

* `X-Fission-Function-*`: The metadata of function that processing the request.

* `X-Fission-Params-*`: The path parameters specified in http trigger url. One thing worth to notice is that the name of parameter will be convert to a form with upper case of first character and lower case for the rest. For example, `{foobar}` in `"/test/{foobar}"` will be converted and added to request header with header key `X-Fission-Params-Foobar`.

# A Serverless Guestbook Application in Golang (Sample)

In this section, we use a simple guestbook to explain how to create a serverless application.

![router maps req to fn](/images/how-to-develop-a-serverless-application-with-fission/guestbook-diagram.svg)

The guestbook is composed with four REST APIs and each API consist of a function and a HTTP trigger.  

## Installation

You can clone repo below and follow the guide to install/try guestbook sample.

* [Fission REST API Repo](https://github.com/fission/fission-restapi-sample)

## Create Fission Objects for REST API

A REST API uses HTTP method to determine what's the action server needs to perform on resource(s) represents in the URL. 

```bash
POST   http://api.example.com/user-management/users/{id}
PUT    http://api.example.com/user-management/users/{id}
GET    http://api.example.com/user-management/users/{id}
DELETE http://api.example.com/user-management/users/{id}
```

To create a REST API with fission, we need to create following things to make it work:

* `HTTP Trigger` with specific HTTP method and URL contains the resource type we want manipulate with.
* `Function` to handle the HTTP request.

### HTTP Trigger

At part1, you can create a HTTP trigger with command

```bash
$ fission httptrigger create --method GET --url "/my-first-function" --function hello
```

There are 3 important elements in the command:

* `method`: The HTTP method of REST API
* `url`: The API URL contains the resource placeholder
* `function`: The function reference to a fission function

As a real world REST API, the URL would be more complex and contains the resource placeholder. To support such use cases, you can change URL to something like following:

```bash
$ fission httptrigger create --method GET \
    --url "/guestbook/messages/{id}" --function restapi-get
```

Since fission uses `gorilla/mux` as underlying URL router, you can write regular expression in URL to filter out illegal API requests.

* [route-29c87b8b-ffc1-4a13-bb1c-87f66367474a.yaml](https://github.com/fission/fission-restapi-sample/blob/4398eb195aeb59523101aa68a62782d91f86d85a/specs/route-29c87b8b-ffc1-4a13-bb1c-87f66367474a.yaml#L14)

```bash
$ fission httptrigger create --method GET \
    --url "/guestbook/messages/{id:[0-9]+}" --function restapi-get
```

### Function

To handle a REST API request, normally a function need to extract resource from the request URL. 
In fission you can get the resource value from request header directly as we described in [Request Payload](#request-payload).

That means you can get value from header with key `X-Fission-Params-Id` if URL is `/guestbook/messages/{id}`.

In Golang you can use `CanonicalMIMEHeaderKey` to transform letter case. 

* [rest-api/api.go](https://github.com/fission/fission-restapi-sample/blob/4398eb195aeb59523101aa68a62782d91f86d85a/rest-api/api.go#L39-L57) 

```go
import (
    "net/textproto"
)

const (
    URL_PARAMS_PREFIX = "X-Fission-Params"
)

func GetPathValue(r *http.Request, param string) string {
    // transform text case
    // For example: 'id' -> 'Id', 'fooBAR' -> 'Foobar', 'foo-BAR' -> 'Foo-Bar'.
    param = textproto.CanonicalMIMEHeaderKey(param)

    // generate header key for accessing request header value
    key := fmt.Sprintf("%s-%s", URL_PARAMS_PREFIX, param)

    // get header value
    return r.Header.Get(key)
}
```

When Golang server receive HTTP requests, it dispatches `entrypoint function` and passes whole `response writer` and `request` object to the function.

```go
func MessageGetHandler(w http.ResponseWriter, r *http.Request) {
    ...
}
```

In this way, you can access `query string` and `message body` as usual. 

* [rest-api/api.go](https://github.com/fission/fission-restapi-sample/blob/4398eb195aeb59523101aa68a62782d91f86d85a/rest-api/api.go#L65-L67)

```go
func GetQueryString(r *http.Request, query string) string {
    return r.URL.Query().Get(query)
}
```

* [rest-api/api.go](https://github.com/fission/fission-restapi-sample/blob/4398eb195aeb59523101aa68a62782d91f86d85a/rest-api/api.go#L103-L110)

```go
body, err := ioutil.ReadAll(r.Body)
if err != nil {
    err = errors.Wrap(err, "Error reading request body")
    log.Println(err.Error())
    w.WriteHeader(http.StatusBadRequest)
    w.Write([]byte(err.Error()))
    return
}
```

## Access Third-Party Service in Function 

In guestbook application we need to store messages in database. Since fission is build on top of kubernetes, 
it's very easy to achieve this by creating Kubernetes `Service(svc)` and `Deployment` let function to access with.

![Access 3rd service](/images/how-to-develop-a-serverless-application-with-fission/access-3rd-service.svg)

* [cockroachdb.yaml](https://github.com/fission/fission-restapi-sample/blob/4398eb195aeb59523101aa68a62782d91f86d85a/cockroachdb.yaml)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: cockroachdb
  namespace: guestbook
spec:
  selector:
    name:  cockroachdb
    service: database
  type:  ClusterIP
  ports:
  - name: db
    port: 26257
    targetPort:  26257
  - name: dashboard
    port: 8080
    targetPort: 8080
```

In [cockroachdb.yaml](https://github.com/fission/fission-restapi-sample/blob/4398eb195aeb59523101aa68a62782d91f86d85a/cockroachdb.yaml), 
we create a deployment and service for CockroachDB. After the creation, the function can access the service with DNS name `<service>.<namespace>:<port>`. 
In this case, the DNS name will be `cockroachdb.guestbook:26257`.

* [rest-api/api.go](https://github.com/fission/fission-restapi-sample/blob/4398eb195aeb59523101aa68a62782d91f86d85a/rest-api/api.go#L29)

```go
dbUrl := "postgresql://root@cockroachdb.guestbook:26257/guestbook?sslmode=disable"
```

# Conclusion

This part we know what's the actual request payload a function get and understand how to developer a guestbook application that
store message in 3rd-party database service.

[Part 3](/posts/how-to-develop-a-serverless-application-with-fission-pt-3) will introduce how to use AJAX to interact with backend
function also how to deploy a application to different fission clusters. 

And feel free to [join the Fission community](https://fission.io/community/)!

---

**_Authors:_**

* Ta-Ching Chen **|** [Fission Contributor](https://github.com/life1347) **|** [Tech blog](https://tachingchen.com/blog)
