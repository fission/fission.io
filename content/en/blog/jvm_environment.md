+++
title = "Writing Serverless Functions for JVM with Fission.io"
date = "2018-08-30T22:26:41+05:30"
author = "Vishal Biyani"
description = "Write serverless Java functions with JVM"
categories = ["Tutorials"]
type = "blog"
+++

# Introduction

The Java Virtual Machine (JVM) is one of the most popular application frameworks, particularly when it comes to enterprise software development - due to the  maturity of JVM, the breadth of integrated developer tools  and the vibrant community, and the extension of JVM to additional  languages. 

The historic data from [TIOBE index](https://www.tiobe.com/tiobe-index/) also shows how popular JVM and Java have been through the  years. In the last decade or so Scala and data-related technologies have made great progress using JVM as the base framework. Most recently Kotlin has seen great progress and also [got blessings of Google as an official language for Android development](https://developer.android.com/kotlin/). 

All of this make Java and JVM great candidates for Serverless Functions, and for a Function-as-a-Service (FaaS) platform such as Fission. 

This tutorial will introduce the JVM environment in Fission and walk through a simple demo.

If you want to follow along the tutorial, it will be a good idea to [install Fission](/docs/installation/) on a Kubernetes cluster of your choice.

# JVM in Fission

The new [JVM environment](https://github.com/fission/environments/tree/master/jvm) support allows you to use Java functions in Fission. 

This tutorial explains how Java functions work in Fission and guides you through building a simple "Hello World" function with the JVM environment, so you can see the Java support in action. This example can also be found in our [examples directory on GitHub](https://github.com/fission/examples/tree/main/java).

# JVM Environment: Insider View

The JVM environment in Fission is based on [Spring boot](https://spring.io/projects/spring-boot) and [Spring web frameworks](https://docs.spring.io/spring/docs/current/spring-framework-reference/web.html). 

Spring boot and Spring web is already loaded in JVM. If you are using this dependency, you can mark it at provided scope. The environment loads the function code from the JAR file during specialization and then executes it.

## Fission Contract

A function needs to implement the `io.fission.Function` class and override the `call` method. The call method receives the `RequestEntity` and `Context` as inputs and needs to return `ResponseEntity` object. Both `RequestEntity` and `ResponseEntity` are from `org.springframework.http` package and provide a fairly high level and rich API to interact with request and response.

```
ResponseEntity call(RequestEntity req, Context context);
```

The `Context` object is a placeholder to interact with JVM and Fission and provides information about the framework to the code. This also serves as an extension mechanism to provide more information to runtime code in future.

## Building a Function

### Source Code and Test

The function code responds with "Hello World" in response body.

```
public class HelloWorld implements Function {

	@Override
	public ResponseEntity<?> call(RequestEntity req, Context context) {
		return ResponseEntity.ok("Hello World!");
	}

}
```

### Project and Dependencies with Maven

First you have to define the the basic information about the function:

```
	<modelVersion>4.0.0</modelVersion>
	<groupId>io.fission</groupId>
	<artifactId>hello-world</artifactId>
	<version>1.0-SNAPSHOT</version>
	<packaging>JAR</packaging>

	<name>hello-world</name>
```
You will have to add two dependencies - specifications below - which are provided by the function runtime. 

```
	<dependencies>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-web</artifactId>
			<version>2.0.1.RELEASE</version>
			<scope>provided</scope>
		</dependency>
		<dependency>
			<groupId>io.fission</groupId>
			<artifactId>fission-java-core</artifactId>
			<version>0.0.2-SNAPSHOT</version>
			<scope>provided</scope>
		</dependency>
	</dependencies>
```

**One of the key things** when packaging the Java function is to package it as a **uber/fat JAR** so that the class and all other dependencies are packaged with the function. You can use `maven-assembly-plugin` for that:

```
<execution>
	<id>make-assembly</id> <!-- this is used for inheritance merges -->
	<phase>package</phase> <!-- bind to the packaging phase -->
	<goals>
		<goal>single</goal>
	</goals>
</execution>
```

Lastly, since the `fission-java-core` is currently in the **snapshot release**, you need to **explicitly add the sonatype repository** where it is published. 

```
	<repositories>
		<repository>
			<id>fission-java-core</id>
			<name>fission-java-core-snapshot</name>
			<url>https://oss.sonatype.org/content/repositories/snapshots/</url>
		</repository>
	</repositories>
```

### Building the Package

For building the source Java code with Maven, you either need Maven and Java installed locally or you can use the `build.sh` helper script which builds the code inside a docker image that has those dependencies.

```
docker run -it --rm  -v "$(pwd)":/usr/src/mymaven -w /usr/src/mymaven maven:3.5-jdk-8 mvn clean package
```

At this stage we assume that the build was successful and that you have the JAR file of the function ready.

Note, you can also use the Fission builder for building the JAR file, which comes with a pre-packaged Maven-based builder. (more on that  in a separate tutorial, so stay tuned).

### Deploying the Function

First you will need to **create an environment**. The `keeparchive` flag is important for Java-based applications that are packaged as JAR file. This flag will ensure that the fetcher won't extract the JAR file into a directory. Currently, the JVM environment supports version 2 and above, so we specify the environment version as 2.

```
$ fission env create --name jvm --image fission/jvm-env --version 2 --keeparchive
```

When creating the function we provide the JAR file we built and the environment. The **entrypoint** signifies the fully qualified name of the class which implements the Fission's `Function` interface. 

```
$ fission fn create --name hello --deploy target/hello-world-1.0-SNAPSHOT-JAR-with-dependencies.JAR --env jvm --entrypoint io.fission.HelloWorld
```
Now you can create a route and **test that the function works!**

```
$ fission route create --function hello --url /hello --method GET

$ fission function test --name hello 

OR

$ curl $FISSION_ROUTER/hello
Hello World!
```

# Want more?

- More examples can be found in our [examples directory on GitHub](https://github.com/fission/examples/tree/main/java)


**Follow us on Twitter for more updates! [@fissionio](https://www.twitter.com/fissionio)**

--- 


**_Author:_**

* [Vishal Biyani](https://twitter.com/vishal_biyani)  **|**  [Fission Contributor](https://github.com/vishal-biyani)  **|**  CTO - [InfraCloud Technologies](http://infracloud.io/)