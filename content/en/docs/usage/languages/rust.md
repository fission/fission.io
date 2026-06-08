---
title: "Rust Functions"
description: "Writing Rust functions with fission"
weight: 10
---

Fission supports Rust as a first-class function language.
Rust functions are compiled by the builder into native server binaries built on [axum](https://docs.rs/axum) and [tokio](https://tokio.rs), so invocations run at native speed with no per-request process startup.

In this usage guide we'll cover how to use this environment, write functions, and work with dependencies.

### Before you start

We'll assume you have Fission and Kubernetes set up.
If not, head over to the [install guide]({{% ref "../../installation/_index.en.md" %}}).
Verify your Fission setup with:

```bash
fission version
```

### Add the Rust environment to your cluster

Rust is a compiled language, so source code must be compiled before it runs.
The builder manager inside Fission does this automatically whenever a Rust function or package is created: the Rust builder converts a source package into a deployable native binary.

```bash
fission environment create --name rust \
  --image ghcr.io/fission/rust-env \
  --builder ghcr.io/fission/rust-builder
```

#### Rust environment image list

| Image | Builder Image |
|-------|---------------|
| [ghcr.io/fission/rust-env](https://github.com/fission/environments/pkgs/container/rust-env/versions?filters%5Bversion_type%5D=tagged) | [ghcr.io/fission/rust-builder](https://github.com/fission/environments/pkgs/container/rust-builder/versions?filters%5Bversion_type%5D=tagged) |

### Write a simple function in Rust

A single-file function is one `.rs` file that defines `pub async fn handler`.
Any [axum handler](https://docs.rs/axum/latest/axum/handler/index.html) signature works, so you can use extractors, `Json`, headers, and so on.

Here is a hello world example (`hello.rs`):

```rust
use fission_rust::IntoResponse;

pub async fn handler() -> impl IntoResponse {
    "Hello, World!\n"
}
```

Create and test the function:

```bash
fission fn create --name helloworld --env rust --src hello.rs
```

Before accessing the function, make sure its package build has succeeded:

```bash
fission pkg info --name <pkg-name>
```

Now test it:

```bash
$ fission fn test --name helloworld
Hello, World!
```

{{% notice info %}}
See [here]({{% ref "../triggers/_index.md" %}}) for how to set up different triggers for a Rust function.
{{% /notice %}}

Single-file functions may use the crates pre-baked into the builder: `fission-rust`, `axum`, `tokio`, `serde`, and `serde_json`.
For other dependencies, use a [Cargo project](#working-with-dependencies-cargo-projects).

### HTTP requests and HTTP responses

The function receives every request routed to it; axum extractors give you typed access to all parts of the request.

#### Accessing HTTP Requests

##### Headers

```rust
use fission_rust::IntoResponse;
use fission_rust::axum::http::HeaderMap;

pub async fn handler(headers: HeaderMap) -> impl IntoResponse {
    let v = headers
        .get("x-my-header")
        .and_then(|v| v.to_str().ok())
        .unwrap_or("not set");
    format!("x-my-header: {v}\n")
}
```

Create an HTTP trigger and call it:

```bash
fission httptrigger create --method GET --url "/<url>" --function <fn-name>
```

```bash
$ curl http://$FISSION_ROUTER/<url> -H 'X-My-Header: foo'
x-my-header: foo
```

##### Query string

```rust
use std::collections::HashMap;
use fission_rust::IntoResponse;
use fission_rust::axum::extract::Query;

pub async fn handler(Query(params): Query<HashMap<String, String>>) -> impl IntoResponse {
    params.get("key-name").cloned().unwrap_or_default()
}
```

```bash
$ curl "http://$FISSION_ROUTER/<url>?key-name=123"
123
```

##### Request Body

###### Plain text

```rust
use fission_rust::IntoResponse;

pub async fn handler(body: String) -> impl IntoResponse {
    body
}
```

```bash
$ curl -X POST http://$FISSION_ROUTER/<url> -d foobar
foobar
```

###### JSON

```rust
use fission_rust::IntoResponse;
use fission_rust::axum::Json;
use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize)]
pub struct Msg {
    content: String,
}

pub async fn handler(Json(msg): Json<Msg>) -> impl IntoResponse {
    Json(msg)
}
```

```bash
$ curl -X POST http://$FISSION_ROUTER/<url> \
    -H 'Content-Type: application/json' -d '{"content": "foobar"}'
{"content":"foobar"}
```

#### Controlling HTTP Responses

##### Setting response headers and status codes

Return a tuple of status, headers, and body — axum converts it into a response:

```rust
use fission_rust::IntoResponse;
use fission_rust::axum::http::StatusCode;

pub async fn handler() -> impl IntoResponse {
    (
        StatusCode::CREATED,
        [("x-request-handled-by", "fission-rust")],
        "created\n",
    )
}
```

```bash
$ curl -i http://$FISSION_ROUTER/<url>
HTTP/1.1 201 Created
x-request-handled-by: fission-rust
...
```

Handler panics are caught by the runtime: the request returns HTTP 500 and the function keeps serving.

### Multiple module files

A source archive may contain a `handler.rs` plus extra module files.
Each file becomes a crate-root module, so `handler.rs` can reach a sibling `util.rs` as `crate::util`:

```rust
// util.rs
pub fn greeting() -> String {
    "Hello from a sibling module!\n".to_string()
}
```

```rust
// handler.rs
use fission_rust::IntoResponse;

pub async fn handler() -> impl IntoResponse {
    crate::util::greeting()
}
```

```bash
zip -r function.zip handler.rs util.rs
fission pkg create --name multimod --env rust --src function.zip
```

### Working with dependencies (Cargo projects)

For third-party crates, supply a full Cargo binary crate as the source package.
The only contract: **the binary must serve HTTP on `127.0.0.1:$FISSION_RUNTIME_PORT`**.

The easiest way is the `fission-rust` SDK:

```toml
# Cargo.toml
[package]
name = "echo-example"
version = "0.1.0"
edition = "2024"

[dependencies]
fission-rust = { git = "https://github.com/fission/environments" }
tokio = { version = "1", features = ["rt-multi-thread", "macros"] }
serde_json = "1"
```

```rust
// src/main.rs
use fission_rust::IntoResponse;
use fission_rust::axum::Json;
use serde_json::Value;

async fn handler(body: String) -> impl IntoResponse {
    let value: Value = serde_json::from_str(&body)
        .unwrap_or_else(|_| Value::String(body));
    Json(value)
}

#[tokio::main]
async fn main() {
    fission_rust::serve(handler).await;
}
```

Archive and create the package as usual:

```bash
$ zip -r echo.zip Cargo.toml src
$ fission pkg create --name echo --env rust --src echo.zip
$ fission fn create --name echo --env rust --pkg echo
```

#### Bring your own framework

Because the contract is just "serve HTTP on `$FISSION_RUNTIME_PORT`", any Rust web framework works — actix-web, rocket, warp, or raw hyper:

```rust
// src/main.rs — plain axum without the SDK
use axum::{Router, routing::get};

#[tokio::main]
async fn main() {
    let port: u16 = std::env::var("FISSION_RUNTIME_PORT")
        .ok().and_then(|p| p.parse().ok()).unwrap_or(8889);
    let app = Router::new().route("/", get(|| async { "Hello!\n" }));
    let listener = tokio::net::TcpListener::bind(("127.0.0.1", port)).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

#### Multiple binaries and entrypoints

If the project defines several `[[bin]]` targets, the builder deploys all of them and the function's `--entrypoint` selects one by name:

```bash
fission fn create --name myfn --env rust --pkg mypkg --entrypoint <binary-name>
```

A project with a single binary needs no entrypoint — it is always deployed under the default name `handler`.

### How it works

The runtime image runs a small supervisor that implements the Fission environment interface.
At specialization it starts your compiled function binary **once** and then reverse-proxies all requests to it over a pooled local connection, so steady-state overhead is a single localhost hop.
If the function process exits, the pod is replaced automatically.

### Modifying/Rebuilding the environment images

Refer to the [Rust environment guide](https://github.com/fission/environments/blob/master/rust/README.md) to learn about rebuilding the environment images.

### Resource usage

Like any function, you can bound a Rust function's resources:

```bash
fission fn create --name echo --env rust --pkg echo \
                  --mincpu 20 --maxcpu 100 --minmemory 64 --maxmemory 128
```

Compiled Rust functions are typically small (a hello world binary is around 1 MB) and have low memory floors, so they are a good fit for tight resource limits.
Use `kubectl top pod -l functionName=<name>` while benchmarking to find the right values.
