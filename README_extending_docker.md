<center>
  <a href="https://github.com/unskript/Awesome-CloudOps-Automation">
    <img src="https://unskript.com/assets/favicon.png" alt="Logo" width="80" height="80">
  </a>
  <h1> Extending Awesome Docker </h1>
</center>


## Extending the docker
You can use our base docker to extend the functionality to fit your need. The steps below could be used to package your custom Actions/Runbooks and re-build your custom docker that you can upload and distribute to/from any docker registry. 


## Pre-requisites
1. You are submoduling our Awesome-CloudOps-Automation to your existing
   Git repo.
   ```
   cd $YOUR_REPO_DIRECTORY
   git submodule add https://github.com/unskript/Awesome-CloudOps-Automation.git Awesome-CloudOps-Automation
   ```
2. In same directory, you will need to create two sub-folders.
   ```
   mkdir -p $YOUR_REPO_DIRECTORY/runbooks $YOUR_REPO_DIRECTORY/actions
   ```

3. The Directory structure resulting would be something like this
   ```
   YOUR_REPO_DIRECTORY/
      actions/  
      runbooks/
      Awesome-CloudOps-Auatomation/ 
      your-repo-folders/
      your-repo-files
      ...
   ```
4. You have a working Python 3 environment installed on your build system
5. You have `make` and other build tools installed on your bulid system
6. You have Docker-ce installed and working on your build system


## Building Custom Docker 
1. To build your custom docker. You need to set two environment variables
   `CUSTOM_DOCKER_NAME` and `CUSTOM_DOCKER_VERSION`. If not set, by default the
   Make rule will assume `my-custom-docker` and `0.1.0` as values for these 
   variables.

   ```
   export CUSTOM_DOCKER_NAME=my-awesome-docker
   export CUSTOM_DOCKER_VERSION='0.1.0'
   cd $YOUR_REPO_DIRECTORY
   cp Awesome-CloudOps-Automation/build/templates/Makefile.extend-docker.template Makefile
   make -f Makefile build
   ```

   It may take a few minutes to build the docker, once built, you can verify it using 

   ```
   docker run -it -p 8888:8888 \
       $CUSTOM_DOCKER_NAME:$CUSTOM_DOCKER_VERSION 
   ```

   This would run your `custom docker` and you can point your browser to `http://127.0.0.1:8888/awesome`! 

2. Push your `custom docker` to any docker registry for redistribution.
<br/>

## Action and agruments

Actions are small python functions that is designed to do a specific task. For example, aws_sts_get_caller_identity action
is designed to display the  AWS sts caller identity for a given configuration. Actions may take one or more arguments, like 
any python function do. Some or all of these arguments may also assume a default value if none given at the time of calling.
Many checks may have the same argument name used. For example `region` could be a common name of the argument used across
multiple AWS actions, likewise `namespace` could be a common argument for an K8S action. 

We call an action a check (short for health check) when the return value of the action is in the form of a Tuple.
First value being the result of the action (a boolean) and the second value being the errored object or None. 
We bundle a number of checks for some of the popular connectors like AWS, K8S, etc.. And you can write you own custom
Actions (or checks) too. 


### How to Copy Custom Actions and Runbook 

If you have deployed our Awesome runbook as a Kubernetes POD then follow the step below
1. Copy the custom actions from the POD to your local machine so you can bundle into your custom Docker for re-distribution
```
kubectl cp <AWESOME_POD_NAME>:/unskript/data/runbooks -n <NAMESPACE> $YOUR_REPO_DIRECTORY/runbooks
kubectl cp <AWESOME_POD_NAME>:/unskript/data/actions -n <NAMESPACE> $YOUR_REPO_DIRECTORY/actions
cd $YOUR_REPO_DIRECTORY
git clone https://github.com/unskript/Awesome-CloudOps-Automation.git

Example:

kubectl cp awesome-runbooks-0:/unskript/data/actions -n awesome-ops $YOUR_REPO_DIRECTORY/actions 
kubectl cp awesome-runbooks-0:/unskript/data/runbooks -n awesome-ops $YOUR_REPO_DIRECTORY/runbooks
```

If you have deployed our Awesome runbook as a Docker instance, then you can use
the following step.
```
export CONTAINER_ID=`docker ps | grep awesome-runbooks | awk '{print $1}'`
docker cp $CONTAINER_ID:/unskript/data/actions $HOME/Workspace/acme/actions
docker cp $CONTAINER_ID:/unskript/data/runbooks $HOME/Workspace/acme/runbooks
```


### How to create Custom Actions

You can refer to [this link](https://docs.unskript.com/unskript-product-documentation/actions/create-custom-actions) on how to create custom Action

### Action and agruments

Actions are small python functions that is designed to do a specific task. For example, aws_sts_get_caller_identity action
is designed to display the  AWS sts caller identity for a given configuration. Actions may take one or more arguments, like 
any python function do. Some or all of these arguments may also assume a default value if none given at the time of calling.
Many checks may have the same argument name used. For example `region` could be a common name of the argument used across
multiple AWS actions, likewise `namespace` could be a common argument for an K8S action. 

We call an action a check (short for health check) when the return value of the action is in the form of a Tuple.
First value being the result of the action (a boolean) and the second value being the errored object or None. 
We bundle a number of checks for some of the popular connectors like AWS, K8S, etc..

Using the global file `unskript_config.yaml`, we can specify values for all the arguments needed to run the action.
Example if 


## How to specify values for arguments used in checks

You can specify the variables that are used in the checks in the global file `unskript_config.yaml` You can see an example
of that file in `unskript-ctl` Folder.  This step  be done before you start building your custom docker image.

* In your `YOUR_REPO_DIRECTORY/actions/` directory create a file unskript_config.yaml
   > touch $YOUR_REPO_DIRECTORY/actions/unskript_config.yaml
* Update the contents of the unskript_config.yaml file like so.
   ```
   globals:
      namespace: "awesome-ops"
      threshold: "string"
      region: "us-west-2"
      services: ["calendar", "audit"]
   ```
* This is a YAML file. under `globals` you can sepcify the variable you are expecting in the your check and the value of that variable on the right hand side of the variable. For example in the above snippet, `"awesome-ops"` is assigned to variable `namespace`