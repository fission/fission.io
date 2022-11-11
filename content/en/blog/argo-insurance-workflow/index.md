+++
title = "Fission Function Orchestration with Argo Workflows"
date = "2022-09-22T12:22:07+05:30"
author = "Neha Gupta"
description = "Multiple Fission function orchestration using Argo Workflows"
categories = ["Tutorials"]
type = "blog"
images = ["/images/featured/argo-workflows.png"]
+++

Fission Functions allow user to perform one logical task. To group multiple task together such as one function is dependent on other we can use Argo Workflows.

[Argo Workflows](https://argoproj.github.io/workflows) is an open source container-native workflow engine with a feature to create DAGs i.e. running task sequentially, in parallel and with dependencies. We will try to develop a simple Insurance Eligibility program which will take different input and calculate insurance installment on basis of the inputs.

{{< figure src="/images/featured/argo-workflows.png" alt="Orchestrate Workflows using Fission and Argo Workflows" height="600" width="1000">}}

### Understanding the Insurance Calculator

The application/Workflow will take basic information from the user and check their eligibility for Insurance. Below are the input user needs to provide:

* first_name
* last_name
* age
* salary
  
**Note**: for simplicity we have default values for all parameters defined in the Argo Workflow itself. You can use any custom value by changing parameter in [Workflow Yaml file](https://github.com/neha-Gupta1/argo-workflow/blob/main/insurance/insuranceDag.yaml) or by passing parameter to the workflow from CLI which is explained later in this blog.

The different tasks in the workflow are:

* Take first name of the user
* Take last name of the user
* Create full name using the above two.
* Input age
* Get monthly salary.
* With predefined criteria i.e. ,
  * if user's age is below a certain number(30 yrs) and yearly salary is above some numbers(1200000), user lies in a low risk criteria
  * otherwise he/she falls in high risk criteria. And the installments varies accordingly.
* We print the above calculated output to the user.

{{< figure src="insurance-workflow-argo.png" alt="Developing Insurance calculator DAG using Argo Workflows" >}}

## Pre Requisites

### Fission

You should have Fission running on your system. You can refer to our [Fission Installation](/docs/installation) guide for more information.

### Argo Workflows

For installing the latest version Argo Workflows, you can refer to [Argo Workflows Installation](https://argoproj.github.io/argo-workflows/quick-start/)  

Verify the Argo Workflows installation by running an example workflow,

```bash
$ argo submit -n argo --watch https://raw.githubusercontent.com/argoproj/argo-workflows/master/examples/hello-world.yaml

Name:                hello-world-wqxqz
Namespace:           argo
ServiceAccount:      unset (will run with the default ServiceAccount)
Status:              Running
Created:             Wed Sep 21 15:16:48 +0530 (10 seconds ago)
Started:             Wed Sep 21 15:16:48 +0530 (10 seconds ago)
Duration:            10 seconds
Progress:            0/1

STEP                  TEMPLATE  PODNAME            DURATION  MESSAGE
 ◷ hello-world-wqxqz  whalesay  hello-world-wqxqz  10s         

This workflow does not have security context set. You can run your workflow pods more securely by setting it.
Learn more at https://argoproj.github.io/argo-workflows/workflow-pod-security-context/

```

The successful run of workflow will verify our successful installation.

**Note** We will be using Argo Workflows HTTP agent which requires some custom roles. You can refer to [Argo Workflows quick-start Manifests](https://github.com/argoproj/argo-workflows/blob/master/manifests/quick-start/base/agent-role.yaml) and [workflow RBAC](https://argoproj.github.io/argo-workflows/workflow-rbac/) to create the role on basis of which version of Argo Workflows you will be using.

We are ready to build our Insurance Installment calculator now.

### Creating Fission functions and triggers

We have to create all the functions which would be helping us with the calculation. The functions are handlers which can be present in any language. Here we have them in go-lang. `set-first-name` function looks like,

```go

type firstname struct {
	FirstName string `json:"first_name"`
}

// Handler is the entry point for this fission function
func PostFirstNameHandler(w http.ResponseWriter, r *http.Request) { 
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error reading request body",
			http.StatusInternalServerError)
	}
	firstname := firstname{}
	json.Unmarshal(body, &firstname)
	fmt.Println(firstname.FirstName)
	_, err = w.Write([]byte(firstname.FirstName))
	if err != nil {
		http.Error(w, "Error writing response", http.StatusInternalServerError)
	}
}

```

You can refer to [Fission Function](https://github.com/neha-Gupta1/argo-workflow/tree/main/insurance/fission-functions) folder for all the functions required for this application. Clone the above folder and run below command -

`sudo chmod 755 insurance/fission-functions/spec.sh`

it runs the below-mentioned tasks,

```bash
fission function create --name set-first-name --env go --src fission-function/postFirstName.go --entrypoint PostFirstNameHandler
fission httptrigger create --name postfirstname --url /postfirstname --method GET --function set-first-name

fission function create --name set-last-name --env go --src fission-function/postLastName.go --entrypoint PostLastNameHandler
fission httptrigger create --name postlastname --url /postlastname --method GET --function set-last-name

fission function create --name get-full-name --env go --src fission-functions/getFullName.go --entrypoint GetFullNameHandler
fission httptrigger create --name getfullname --url /getfullnamehandler --method GET --function get-full-name

fission function create --name set-age --env go --src fission-functions/getAge.go --entrypoint PostAgeHandler
fission httptrigger create --name postage --url /setage --method GET --function set-age

fission function create --name set-salary --env go --src fission-functions/getMonthlySalary.go --entrypoint PostSalaryHandler
fission httptrigger create --name postsalary --url /setmonthlysalary --method GET --function set-salary

fission function create --name lowriskinsurance --env go --src fission-functions/calculateEligibililty.go --entrypoint GetLowRiskInsuranceHandler
fission httptrigger create --name getlowriskinsurance --url /getLowRiskEligibility --method GET --function lowriskinsurance

fission function create --name highriskinsurance --env go --src fission-functions/calculateEligibililty.go --entrypoint GetHighRiskInsuranceHandler
fission httptrigger create --name gethighriskinsurance --url /getHighRiskEligibility --method GET --function highriskinsurance
```

Verify that all the required functions and triggers are created:

```bash
$ fission fn list
NAME              ENV    EXECUTORTYPE MINSCALE MAXSCALE MINCPU MAXCPU MINMEMORY MAXMEMORY SECRETS CONFIGMAPS
get-full-name     go     poolmgr      0        0        0      0      0         0
highriskinsurance go     poolmgr      0        0        0      0      0         0
lowriskinsurance  go     poolmgr      0        0        0      0      0         0
set-age           go     poolmgr      0        0        0      0      0         0
set-first-name    go     poolmgr      0        0        0      0      0         0
set-last-name     go     poolmgr      0        0        0      0      0         0
set-salary        go     poolmgr      0        0        0      0      0         0
```

```bash
$ fission httptrigger list
NAME                                 METHOD URL                     FUNCTION(s)       INGRESS HOST PATH                    TLS ANNOTATIONS
getfullname                          [GET]  /getfullnamehandler     get-full-name     false   *    /getfullnamehandler         
gethighriskinsurance                 [GET]  /getHighRiskEligibility highriskinsurance false   *    /getHighRiskEligibility     
getlowriskinsurance                  [GET]  /getLowRiskEligibility  lowriskinsurance  false   *    /getLowRiskEligibility      
postage                              [GET]  /setage                 set-age           false   *    /setage                     
postfirstname                        [GET]  /postfirstname          set-first-name    false   *    /postfirstname              
postlastname                         [GET]  /postlastname           set-last-name     false   *    /postlastname               
postsalary                           [GET]  /setmonthlysalary       set-salary        false   *    /setmonthlysalary  
```

### Running the application

The above functions helped us in creating independent logics. Now we are going to club them together and create a workflow using Argo Workflows. This workflow takes its decision on the basis of inputs provided.

#### Running application with default inputs

We will try to first run our application with the default inputs:

```bash
argo submit --watch insurance/insuranceDag.yaml 

Name:                hello-argo-4n4pm
Namespace:           fission
ServiceAccount:      unset (will run with the default ServiceAccount)
Status:              Running
Created:             Tue Sep 20 10:56:57 +0530 (10 seconds ago)
Started:             Tue Sep 20 10:56:57 +0530 (10 seconds ago)
Duration:            10 seconds
Progress:            0/4
Parameters:          
  age:               35
  salary:            20000

STEP                   TEMPLATE          PODNAME  DURATION  MESSAGE
 ● hello-argo-4n4pm    insurance                              
 ├─◷ getage            getage                                 
 ├─◷ getmonthlysalary  getmonthlysalary                       
 ├─◷ postfirstname     postfirstname                          
 └─◷ postlastname      postlastname                           

This workflow does not have security context set. You can run your workflow pods more securely by setting it.
Learn more at https://argoproj.github.io/argo-workflows/workflow-pod-security-context/
```

`--watch` will help us to follow the status of workflow. You can view the logs/output of the Workflow using the below command,

```bash
$ argo logs -f hello-argo-4n4pm

hello-argo-4n4pm-761537852:  _______________________ 
hello-argo-4n4pm-761537852: < {Hello Neha Gupta!! as per your age: 35 We can give you an insurance with assured money 20000} >
hello-argo-4n4pm-761537852:  ----------------------- 
hello-argo-4n4pm-761537852:     \
hello-argo-4n4pm-761537852:      \
hello-argo-4n4pm-761537852:       \     
hello-argo-4n4pm-761537852:                     ##        .            
hello-argo-4n4pm-761537852:               ## ## ##       ==            
hello-argo-4n4pm-761537852:            ## ## ## ##      ===            
hello-argo-4n4pm-761537852:        /""""""""""""""""___/ ===        
hello-argo-4n4pm-761537852:   ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~   
hello-argo-4n4pm-761537852:        \______ o          __/            
hello-argo-4n4pm-761537852:         \    \        __/             
hello-argo-4n4pm-761537852:           \____\______/   
hello-argo-4n4pm-761537852: time="2022-09-20T05:28:20.770Z" level=info msg="sub-process exited" argo=true error="<nil>"
```

**Note** `hello-argo-4n4pm` should be replaced by the Workflow name in the above command.

#### Running application with custom inputs

We can provide any custom input to the workflow by passing input file from the command line.
For this workflow our input file will look something similar to,

```json
{
	"first_name": "name",
	"last_name": "surname",
	"age": 56,
	"salary": 1500
}
```

Save the above file as input.json in insurance folder and now let's run the workflow with given input,

```bash
argo submit --watch -f insurance/input.json  insurance/insuranceDag.yaml 

Name:                insurance-argo-s79p7
Namespace:           fission
ServiceAccount:      unset (will run with the default ServiceAccount)
Status:              Running
Conditions:          
 PodRunning          False
Created:             Wed Sep 21 17:14:50 +0530 (1 minute ago)
Started:             Wed Sep 21 17:14:50 +0530 (1 minute ago)
Duration:            1 minute 4 seconds
Progress:            7/7
ResourcesDuration:   8s*(1 cpu),8s*(100Mi memory)
Parameters:          
  age:               56
  first_name:        name
  last_name:         surname
  salary:            1500

STEP                       TEMPLATE              PODNAME                          DURATION  MESSAGE
 ● insurance-argo-s79p7    insurance                                                                                                               
 ├─✔ getage                getage                                                                                                                  
 ├─✔ getmonthlysalary      getmonthlysalary                                                                                                        
 ├─✔ postfirstname         postfirstname                                                                                                           
 ├─✔ postlastname          postlastname                                                                                                            
 ├─✔ getfullname           getfullname                                                                                                             
 ├─✔ echolowriskresult     echo                  insurance-argo-s79p7-3888718883  9s                                                               
 ├─✔ gethighriskinsurance  gethighriskinsurance                                                                                                    
 └─○ getlowriskinsurance   getlowriskinsurance                                              when '(1500*12 > 1200000) || (56<30)' evaluated false  

This workflow does not have security context set. You can run your workflow pods more securely by setting it.
Learn more at https://argoproj.github.io/argo-workflows/workflow-pod-security-context/

```

```bash

argo logs -f insurance-argo-gf8dx 

insurance-argo-gf8dx-2121782614:  ________________________________________ 
insurance-argo-gf8dx-2121782614: / Hello name surname !! as per your age: \
insurance-argo-gf8dx-2121782614: | 56 We can give you an insurance with   |
insurance-argo-gf8dx-2121782614: \ assured money 75000                    /
insurance-argo-gf8dx-2121782614:  ---------------------------------------- 
insurance-argo-gf8dx-2121782614:     \
insurance-argo-gf8dx-2121782614:      \
insurance-argo-gf8dx-2121782614:       \     
insurance-argo-gf8dx-2121782614:                     ##        .            
insurance-argo-gf8dx-2121782614:               ## ## ##       ==            
insurance-argo-gf8dx-2121782614:            ## ## ## ##      ===            
insurance-argo-gf8dx-2121782614:        /""""""""""""""""___/ ===        
insurance-argo-gf8dx-2121782614:   ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~   
insurance-argo-gf8dx-2121782614:        \______ o          __/            
insurance-argo-gf8dx-2121782614:         \    \        __/             
insurance-argo-gf8dx-2121782614:           \____\______/   
insurance-argo-gf8dx-2121782614: time="2022-09-21T11:49:24.809Z" level=info msg="sub-process exited" argo=true error="<nil>"

```

## Conclusion

In this post we tried to orchestrate multiple Fission functions. We saw that functions were running independently or were dependent on output of one or more tasks/stages. We were making decisions on basis of input received. We also have few parallel and other sequential tasks running. 

This Argo Workflows can be further used to create enormous scenarios such as adding Fission's connector to create workflows or using Argo Workflows functionalities like `retry` and `for loop`. This will increase the capabilities of Fission. As it can now have bigger flows.

In case you still have any questions or a specific scenario, feel free to reach out to us. We would be happy to help.

## Want more?

More examples can be found in our [examples directory on GitHub](https://github.com/fission/examples/). Follow **[Fission on Twitter](https://www.twitter.com/fissionio)** for more updates!

---

**_Author:_**

[Neha Gupta](https://www.linkedin.com/in/neha-gupta-g16)  **|**  Software Engineer - [InfraCloud Technologies](http://infracloud.io/)
