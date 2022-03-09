+++
title = "Guestbook Application With Fission and CockroachDB"
date = "2022-03-08T09:30:34+05:30"
author = "Atulpriya Sharma"
description = "Using CockroachDB and REST APIs in Fission to create a Guestbook application"
categories = ["Tutorials"]
type = "blog"
images = ["images/featured/guestbook-application-featured.png"]
+++

Fission provides you with a serverless framework that you can deploy on your Kubernetes clusters.
There are various use cases where you can use Fission, and today we'll show you how to develop a guestbook application with Fission in Go using CockroachDB as a database.

## Serverless Guestbook Application

![router maps req to fn](/images/how-to-develop-a-serverless-application-with-fission/guestbook-diagram.svg)

The guestbook is composed with four REST APIs and each API consist of a function and an HTTP trigger.  
This application allows a user to create, edit and delete a message.
You can submit a message, retrieve a list of messages, delete a message all by means of REST APIs.
You can clone [Fission REST API Repo](https://github.com/fission/fission-restapi-sample) and follow the guide to install/try guestbook sample.

{{< figure src="/images/featured/guestbook-application-featured.png" alt="Using CockroachDB and REST APIs in Fission to create a Guestbook application." height="600" width="800">}}

## Create Fission Objects for REST API

A REST API uses HTTP method to determine what's the action server needs to perform on resource(s) represents in the URL.

```bash
POST   http://api.example.com/user-management/users/{id}
PUT    http://api.example.com/user-management/users/{id}
GET    http://api.example.com/user-management/users/{id}
DELETE http://api.example.com/user-management/users/{id}
```

To create a REST API with fission, we need to create following things to make it work:

* `HTTP Trigger` with specific HTTP method and URL contains the resource type we want to manipulate with. Read more about [HTTP Triggers](../../docs/reference/crd-reference/#httptrigger)
* `Function` to handle the HTTP request. Read more about [Function](../../docs/reference/crd-reference/#function)

## Installation

### HTTP Trigger

The first step is to create an HTTP trigger for your function

```bash
$ fission httptrigger create --url /guestbook/messages --method POST --function restapi-post --name restpost
```

There are 3 important elements in the command:

* `method`: *The HTTP method of REST API*
* `url`: *The API URL contains the resource placeholder*
* `function`: *The function reference to a fission function*

As a real world REST API, the URL would be more complex and contains the resource placeholder.
To support such use cases, you can change URL to something like following:

```bash
$ fission httptrigger create --url "/guestbook/messages/{id:[0-9]+}" --method GET --function restapi-get --name restgetpart
```

Since fission uses `gorilla/mux` as underlying URL router, you can write regular expression in URL to filter out illegal API requests.

* [route-restGetPart.yaml](https://github.com/fission/fission-restapi-sample/blob/master/specs/route-restGetPart.yaml)

```bash
$ fission httptrigger create --url "/guestbook/messages/{id:[0-9]+}" --method GET --function restapi-get --name restgetpart
```

### Function

To handle a REST API request, normally a function need to extract resource from the request URL.
In Fission, you can get the resource value from request header directly as we described in [Request Payload](#request-payload).

That means you can get value from header with key `X-Fission-Params-Id` if URL is `/guestbook/messages/{id}`.

In Go, you can use `CanonicalMIMEHeaderKey` to transform letter case.

* [rest-api/api.go](https://github.com/fission/fission-restapi-sample/blob/f98a46f4dc3756b42fce7fd292705d74e1fad249/rest-api/api.go#L83-L101)

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

* [rest-api/api.go](https://github.com/fission/fission-restapi-sample/blob/f98a46f4dc3756b42fce7fd292705d74e1fad249/rest-api/api.go#L109-L111)

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

## CockroachDB Setup

In guestbook application we need to store messages in a database.
Since fission is build on top of kubernetes, it's very easy to achieve this by creating Kubernetes `Service(svc)` and `Deployment`.
For this sample application, we are using [CockroachDB](https://www.cockroachlabs.com/docs/cockroachcloud/quickstart.html).

> We also have a post on using [PostgreSQL with Fission](../how-to-use-postgresql-database-with-fission-functions/) that you might want to read too.

![Access 3rd service](/images/how-to-develop-a-serverless-application-with-fission/access-3rd-service.svg)

Add `cockroachdb` helm repo

``` bash
helm repo add cockroachdb https://charts.cockroachdb.com/
helm repo update
```

Install cockroachdb using helm and provide values from [cockroachdb.yaml](https://github.com/fission/fission-restapi-sample/blob/master/cockroachdb.yaml)

```bash
helm install my-release --values cockroachdb.yaml cockroachdb/cockroachdb
```

## Guestbook Application Setup

Create the `go` environment

```bash
fission env create --name go --image fission/go-env-1.16 --builder fission/go-builder-1.16
```

Create a `sourcepackage` from the `rest-api` folder.
It is required to create a package.

```bash
zip -j restapi-go-pkg.zip rest-api/*
```

Create a package from the source archive

```bash
fission pkg create --name restapi-go-pkg --sourcearchive restapi-go-pkg.zip --env go
```

Create functions for `GET`, `POST`, `DELETE`, `UPDATE`

```bash
fission fn create --name restapi-delete --executortype newdeploy --maxscale 3 --env go --pkg restapi-go-pkg --entrypoint MessageDeleteHandler
fission fn create --name restapi-update --executortype newdeploy --maxscale 3 --env go --pkg restapi-go-pkg --entrypoint MessageUpdateHandler
fission fn create --name restapi-post --executortype newdeploy --maxscale 3 --env go --pkg restapi-go-pkg --entrypoint MessagePostHandler
fission fn create --name restapi-get --executortype newdeploy --maxscale 3 --env go --pkg restapi-go-pkg --entrypoint MessageGetHandler
```

Create `HTTPTriggers` for the endpoints for the above created functions

```bash
fission httptrigger create --url /guestbook/messages --method POST --function restapi-post --name restpost
fission httptrigger create --url "/guestbook/messages/{id:[0-9]+}" --method PUT --function restapi-update --name restupdate
fission httptrigger create --url "/guestbook/messages/{id:[0-9]+}" --method GET --function restapi-get --name restgetpart
fission httptrigger create --url "/guestbook/messages/{id:[0-9]+}" --method DELETE --function restapi-delete --name restdelete
fission httptrigger create --url "/guestbook/messages/" --method GET --function restapi-get --name restget
```

### Fission Spec

The entire installation can be done using a single block of `fission spec` commands as shown below

```bash
fission spec init
fission env create --name go --image fission/go-env-1.16 --builder fission/go-builder-1.16 --spec
fission pkg create --name restapi-go-pkg --sourcearchive restapi-go-pkg.zip --env go --spec
fission fn create --name restapi-delete --executortype newdeploy --maxscale 3 --env go --pkg restapi-go-pkg --entrypoint MessageDeleteHandler --spec
fission fn create --name restapi-update --executortype newdeploy --maxscale 3 --env go --pkg restapi-go-pkg --entrypoint MessageUpdateHandler --spec
fission fn create --name restapi-post --executortype newdeploy --maxscale 3 --env go --pkg restapi-go-pkg --entrypoint MessagePostHandler --spec
fission fn create --name restapi-get --executortype newdeploy --maxscale 3 --env go --pkg restapi-go-pkg --entrypoint MessageGetHandler --spec
fission httptrigger create --url /guestbook/messages --method POST --function restapi-post --spec --name restpost
fission httptrigger create --url "/guestbook/messages/{id:[0-9]+}" --method PUT --function restapi-update --spec --name restupdate
fission httptrigger create --url "/guestbook/messages/{id:[0-9]+}" --method GET --function restapi-get --spec --name restgetpart
fission httptrigger create --url "/guestbook/messages/{id:[0-9]+}" --method DELETE --function restapi-delete --spec --name restdelete
fission httptrigger create --url "/guestbook/messages/" --method GET --function restapi-get --spec --name restget
```

It will create a `specs` folder with all the required yaml files post which you can apply the changes

```bash
fission spec apply
```

## Testing The Guestbook Application

Since this guestbook application is created using `REST` APIs, we first need to export the `$FISSION_ROUTER` along with the port

```bash
export PORT=8889
kubectl --namespace fission port-forward $(kubectl --namespace fission get pod -l svc=router -o name) $PORT:8888
export FISSION_ROUTER=127.0.0.1:$PORT
```

Create a post

```bash
curl -v -X POST \
    http://${FISSION_ROUTER}/guestbook/messages \
    -H 'Content-Type: application/json' \
    -d '{"message": "hello world!"}'
```

Get all posts

```bash
curl -v -X GET http://${FISSION_ROUTER}/guestbook/messages/
```

It will return a list of all the messages

```bash

[
    {
        "id": 366739357484417025,
        "message": "hello world!",
        "timestamp": 1531990369
    },
    {
        "id": 366739413774237697,
        "message": "hello world!",
        "timestamp": 1531990387
    },
    {
        "id": 366739416644550657,
        "message": "hello world!",
        "timestamp": 1531990399
    }
]
```

You can also get a single post using the id

```bash
curl -v -X GET http://${FISSION_ROUTER}/guestbook/messages/366456868654284801
```

Updating a post

```bash
curl -v -X PUT \
    http://${FISSION_ROUTER}/guestbook/messages/366456868654284801 \
    -H 'Content-Type: application/json' \
    -d '{"message": "hello world again!"}'
```

Deleting a post

```bash
curl -X DELETE \
    http://${FISSION_ROUTER}/guestbook/messages/366456868654284801 \
    -H 'Cache-Control: no-cache'
```

## Conclusion

At this point you know how to create a simple guestbook application using REST APIs and database on Fission.
This was a simple application to show you the capabilities of Fission.
You can try to create your own application which may be more complex than this one.
If you have any issues running this, reach out to the author or post it in the [Fission Slack](https://fission.io/slack) channel.

## Want more?

More examples can be found in our [examples directory on GitHub](https://github.com/fission/examples/). Follow **[Fission on Twitter](https://www.twitter.com/fissionio)** for more updates!

---

**_Author:_**

[Atulpriya Sharma](https://twitter.com/TheTechMaharaj)  **|**  Developer Advocate - [InfraCloud Technologies](http://infracloud.io/)
