---
title: "Accessing URL parameters"
date: 2018-10-25T17:39:41+08:00
weight: 3
description: >
  Define path parameters in an HTTP trigger URL with gorilla/mux patterns and read their values inside a function via request headers.
---

**Define placeholders in the trigger URL, then read their values from the HTTP request header inside your function.**

A REST API often carries its parameters in the URL path itself, for example:

```bash
http://192.168.0.1/guestbook/{name}/{age}
```

Put parameter placeholders in the value of the `--url` flag.
Fission uses gorilla/mux as its underlying URL router, so you can also write a regular expression to filter out illegal API requests.

```bash
$ fission httptrigger create --method GET \
    --url "/guestbook/{name}/{age}" --function restapi-get

$ fission httptrigger create --method GET \
    --url "/guestbook/{name}/{age:[0-9]+}" --function restapi-get
```

Fission attaches the value of each URL parameter to the HTTP request header, as shown below.

```text
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

X-Fission-Params-Name: Alice
X-Fission-Params-Age: 23
```

The headers with key prefix `X-Fission-Params-` are the fields that hold the URL parameter values.

In some languages, such as Go, the header key is displayed in `MIME canonical format`.
For example:

```bash
url: /guestbook/{name}
header key: X-Fission-Params-Name

url: /guestbook/{FooBar}
header key: X-Fission-Params-Foobar
```

Check the letter case of the header key and convert it if necessary to get the right parameter value.

(In Go, call `request.Header.Get()` to get the header value without worrying about the key case.)
