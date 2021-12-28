+++
title = "How to use Fission with PostgreSQL Serverless database"
date = "2021-12-27T12:28:34+05:30"
author = "Atulpriya Sharma"
description = "Tutorial on how to use Fission with PostgreSQL serverless database on Kubernetes Cluster. Serveless database using fission with PostgreSQL"
categories = ["Tutorial","Application","Python","Database"]
type = "blog"
+++

Software development and deployment methods have evolved greatly over the years. From the times when system admins used to setup servers to run software applications to today when developers are not concerned about how the server is provisioned. Containers and container orchestration tools like Kubernetes help developers deploy serverless applications quickly. Similarly serverless functions like [Fission](https://fission.io) help you focus on the code rather than the infrastructure. 

In this blog post, I'll show you how to use **Fission with PostgreSQL serverless database**.

{{< imgproc fission-postgreSQL-serverless-database.png Fit "1000X1000" >}}
Fission with PostgreSQL Serverless Database
{{< /imgproc >}}

## Voting App using Fission & PostgreSQL Serverless Database

In this example, we will create a basic voting application that allows users to vote for an option and view the results. This application is written in **Python** and uses **PostgreSQL** database to store the results. By the end of this blog post you would have learnt how to use Fission with PostgreSQL serverless database. You can then extend this application to use Fission with other relational and non relational databases.

So let's get started!

{{< imgproc  myvotingapp-app.png Fit "1000X1000" >}}
Voting App using Fission & PostgreSQL Serverless Database
{{< /imgproc >}}

## Pre Requisites

### Installing PostgreSQL

Before you start working on this demo, you need to ensure that you have Fission installed and running on your system. You can refer to our [Fission Installation](https://fission.io/docs/installation/) guide for more. Further, this example uses PostgreSQL hence you must also have a PostgreSQL instance in place. You can either run it on your system locally, in a docker container or your Kubernetes cluster.

Below are few guides you can refer to for installing PostgreSQL:

- Installing PostgreSQL on your local system - <a href="https://www.postgresql.org/download/" target="_blank">Postgresql.org</a>
- PostgreSQL Docker container - <a href="https://hub.docker.com/_/postgres" target="_blank">Docker Hub</a>
- PostgreSQL HELM charts - <a href="https://bitnami.com/stack/postgresql/helm" target="_blank">Bitnami</a> - *used in this example*

<br>

> *Note: If you have installed it using Helm Charts, please ensure to note down the service url and port number. This will be used to connect to the database from the function. You can get it by running  `helm status postgresql` in your terminal.*

{{< imgproc myvotingapp-postgres-helm.png Fit "1000X1000" >}}
Helm PostgreSQL Status
{{< /imgproc >}}

#### Database and Table Setup

For this application, we have created a database named `votedb` and a table named `votebank`. You can use the following query to create the table:

```  
 CREATE TABLE votebank (
        id serial PRIMARY KEY,
	    voter_id VARCHAR ( 50 )  NOT NULL,
	    vote VARCHAR ( 50 ) NOT NULL
    );
```

{{< imgproc myvotingapp-tableschema.png Fit "1000X1000" >}}
Votebank table schema
{{< /imgproc >}}

### Environment Setup

#### Python Environment setup
Using PostgreSQL with Fission requires certain libraries and Python modules to be present in the Python environment. For that you need to create a custom Python image. To do this you can refer to [Fisson Python Environment](https://github.com/fission/environments/tree/master/python) and follow the steps to create a custom image.

In this case we need extra libraries like *postgresql-dev and libpq*. For this you need to update the `Dockerfile` and append these two libraries  in the `RUN` command.

It should look like this: `RUN apk add --update --no-cache gcc python3-dev build-base libev-dev libffi-dev bash musl-dev postgresql-dev libpq`. After this create a docker image and push it to your Docker hub repository.
<br>

Building the docker image for our custom Python environment. *(Replace the username with your actual username on Docker Hub.)*
```
docker build -t username/python-postgres:latest --build-arg PY_BASE_IMG=3.7-alpine -f Dockerfile .
```

{{< imgproc myvotingapp-dockerimage.png Fit "1000X1000" >}}
Docker image for creating Python environment
{{< /imgproc >}}

Pushing the docker image to Docker Hub registry:
```
docker push username/python-postgres:latest
```

#### Source Package Setup
Since we require external libraries for this example, we need to create a source package of our code. In order to do that, you need to create a folder `Worker` and create the following files:

- `build.sh` - contains commands to setup the environment by installing required libraries
- `requirements.txt` - contains the Python modules that are required to run the code
- `db-worker.py` - Fission function
- `___init__.py` - standard Python init file

> *Make sure that build.sh file is executable. Update the permissions using `chmod +x build.sh`*
  
Create a `.zip` file of all the above files and name it `dbworker.zip`.

<br>

## Steps

For the front end, we are using **Flask** framework for Python. A simple UI with two buttons that send a POST request with the choice to our Fission function.

For the back end, we start by creating a new fission environment using the custom Python image we created in the earler step.

```
fission env create --name pythonsrc --image username/python-postgres --builder fission/python-builder:latest
```

Once the environment is ready, we ereate a new Fission source package that will be used to deploy our Fission function.

```
fission package create --sourcearchive dbworker.zip --env pythonsrc --buildcmd "./build.sh"
```

Note down the name of the Fission package being created. It will be something like `dbworker-zip-xjax`

{{< imgproc myvotingapp-package.png Fit "1000X1000" >}}
Details of the package created
{{< /imgproc >}}

Creating our Fission function by using the source package created in the above step.

```
fission fn create --name dbworkernew --pkg dbworker-zip-xjax --entrypoint "db-worker.main"
```

Now that our function is deployed, we need a route to allow it to be executed. Since we are going to use`HTTP POST` we need to create a `[POST]` route. To do that we execute the following command:

```
fission route create --method POST --url /castvote --function dbworkernew
```

With this our custom Python environment is ready along with our Fission function. Run `index.py` and cast your vote. When you cast your vote, the request will be handled by the `dbworkernew` fission function which will connect with the PostgreSQL database, update the table and return the values.

{{< imgproc myvotingapp-results.png Fit "1000X1000" >}}
Results from our Voting app
{{< /imgproc >}}

You can also use `CURL` to test the function. In order to do that, you'll first need to forward the route to a port on your localhost. To do that, you need to run `kubectl port-forward svc/router 8888:80 -nfission` in your terminal. This will allow you to access port 8888 from your local system.

Send the following CURL request to check whether the function is working as expected or not:

```
curl -XPOST "localhost:8888/castvote" -H 'Content-Type: application/json' -d '{"vote":"a";"voter_id":"afdad"}'
```

> You can also use Postman to check the function by sending a POST request.

{{< imgproc myvotingapp-postman.png Fit "1000X1000" >}}
Using postman to test our Fission function
{{< /imgproc >}}

## Conclusion

Congratulations! You now know how to use Fission with PostgreSQL Serverless database. This was a simple tutorial to show you how you can leverage Fission and create real world application using databases. You are now ready to extend this example for your use case, use it with another relational database like MySQL or a NoSQL database like MongoDB.

*So what side are you on, Mountains or Beaches? ;)*

You can find the code to this example [here](https://github.com/fission/examples/tree/master/python)

## Want more?

More examples can be found in our [examples directory on GitHub](https://github.com/fission/examples/). Follow **[Fission on Twitter](https://www.twitter.com/fissionio)** for more updates!

**_ Author:_**

[Atulpriya Sharma](https://twitter.com/TheTechMaharaj)  **|**  Developer Advocate - [InfraCloud Technologies](http://infracloud.io/)