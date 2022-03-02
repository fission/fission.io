+++
title = "Develop a Guestbook Application With Fission and CockroachDB"
date = "2022-03-02T09:30:34+05:30"
author = "Atulpriya Sharma"
description = "Write serverless Java functions with JVM (Part 2)"
categories = ["Tutorials"]
type = "blog"
+++

Fission provides you with a serverless framework that you can deploy on your Kubernetes clusters.
There are various use cases where you can use Fission and today we'll show you how to develop a guestbook application with Fission in GoLang using CockroachDB as a database.

## Serverless Guestbook Application

![router maps req to fn](/images/how-to-develop-a-serverless-application-with-fission/guestbook-diagram.svg)

The guestbook is composed with four REST APIs and each API consist of a function and a HTTP trigger.  
This application allows a user to create, edit and delete a message.
You can submit a message, retrieve a list of messages, delete a message all by means of REST APIs.
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

## Installation

### HTTP Trigger

The first step is to create a HTTP trigger for your function

```bash
$ fission httptrigger create --method GET --url "/my-first-function" --function hello
```

There are 3 important elements in the command:

* `method`: *The HTTP method of REST API*
* `url`: *The API URL contains the resource placeholder*
* `function`: *The function reference to a fission function*

As a real world REST API, the URL would be more complex and contains the resource placeholder.
To support such use cases, you can change URL to something like following:

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

## CockroachDB Setup

In guestbook application we need to store messages in a database.
Since fission is build on top of kubernetes, it's very easy to achieve this by creating Kubernetes `Service(svc)` and `Deployment`.
For this sample application, we are using [CockroachDB](https://www.cockroachlabs.com/docs/cockroachcloud/quickstart.html).

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

In [cockroachdb.yaml](https://github.com/fission/fission-restapi-sample/blob/4398eb195aeb59523101aa68a62782d91f86d85a/cockroachdb.yaml), we create a deployment and service for CockroachDB.
After the creation, the function can access the service with DNS name `<service>.<namespace>:<port>`.
In this case, the DNS name will be `cockroachdb.guestbook:26257`.

* [rest-api/api.go](https://github.com/fission/fission-restapi-sample/blob/4398eb195aeb59523101aa68a62782d91f86d85a/rest-api/api.go#L29)

```go
dbUrl := "postgresql://root@cockroachdb.guestbook:26257/guestbook?sslmode=disable"
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
