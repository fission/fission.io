---
title: "Languages (Environment)"
weight: 50
description: >
  Tutorial for supported language
---

Environments provide a runtime which is used to execute the functions.

## Supported language images

The following pre-built environments are currently available for use in Fission:

| Environment                         | Image                     | Builder Image              | v1  | v2  | v3  |
|-------------------------------------|---------------------------|----------------------------|-----|-----|-----|
| NodeJS                              | `fission/node-env`        | `fission/node-builder`     | O   | O   | O   |
| Python 3                            | `fission/python-env`      | `fission/python-builder`   | O   | O   | O   |
| Go                                  | see [here]({{% ref "go.md" %}}#add-the-go-environment-to-your-cluster) for more info | | O   | O   | O   |
| JVM (Java)                          | `fission/jvm-env`         | `fission/jvm-builder`      | O   | O   | O   |
| Ruby                                | `fission/ruby-env`        | `fission/ruby-builder`     | O   | O   | O   |
| Binary (for executables or scripts) | `fission/binary-env`      | `fission/binary-builder`   | O   | O   | O   |
| PHP 7                               | `fission/php-env`         | `fission/php-builder`      | O   | O   | O   |
| .NET 2.0                            | `fission/dotnet20-env`    | `fission/dotnet20-builder` | O   | O   | O   |
| .NET                                | `fission/dotnet-env`      | -                          | O   | X   | X   |
| Perl                                | `fission/perl-env`        | -                          | O   | X   | X   |

{{% notice info %}}
You can get the latest info about the environments at [environment portal](/environments/).
{{% /notice %}}

## Environment Interface Version

Currently, Fission support three environment interface version: v1, v2 and v3.

- v1
  - Support loading function from a **single file**. (Mainly for interpreted languages like Python and JavaScript.)
  - You are **NOT** allowed to specify which entrypoint to load in if there are multiple entrypoint in the file.

---

- v2 (**Recommend**)
  - The function code can be placed in a directory or having multiple entry points in a single file.  
  - **Load function by specific entry point**. (For the v2 interface, the function may not work if no entry point is provided.)
  - Support downloading necessary dependencies and source code compilation. (Optional)

---

- v3 (**Recommend**)
  - All features in v2 interface.
  - Pre-warmed pool size adjustment.

### Which Interface Version Should I Choose

If all source code and dependencies can be put into a single and non-compiled file, v1 interface would be enough.

If the function requires third party dependencies during the runtime or the function is written in compiled language, you should choose v2 interface in order to load function from a directory/binary with specific entry point.

If you want to adjust size of environment pre-warmed pool, use v3.

## Using Specific Environment Interface Version

```sh
  # add version option to fission environment create command
  --version=3
```

For example, to create a go env with version 3 environment interface.

```sh
fission environment create --name go --image fission/go-env-1.16 --builder fission/go-builder-1.16  --version 3
```
