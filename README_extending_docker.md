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

## Action and arguments

Actions are small python functions that is designed to do a specific task. For example, aws_sts_get_caller_identity action
is designed to display the  AWS sts caller identity for a given configuration. Actions may take one or more arguments, like 
any python function do. Some or all of these arguments may also assume a default value if none given at the time of calling.
Many actions may have the same argument name used. For example `region` could be a common name of the argument used across
multiple AWS actions, likewise `namespace` could be a common argument for an K8S action. 


We call an action a check (short for health check) when the return value of the action is in the form of a Tuple.
First value being the result of the check (a boolean), whether it passed or not. True being check passed, False otherwise.
And the second value being the list of errored objects, incase of failure, None otherwise.

We bundle a number of checks for some of the popular connectors like AWS, K8S, etc.. And you can write your own too!


### How to create Custom Actions 

You can create custom action on your workstation using your editor. Please follow the steps below to setup your workstation:

1. We recommend to use [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) to avoid any conflicts with preinstalled Python libraries.
```
conda create --name=unskript-dev python=3.9.6 -y
conda activate unskript-dev
```

2. Install the following pip packages:

```
pip install -U pytest
pip install jinja2
pip install unskript-core
pip install unskript-custom
```

3. To create a new check template files, do the following:
```
cd $YOUR_REPO_DIRECTORY
./Awesome-CloudOps-Automation/bin/unskript-add-check.sh -t <Check type> -n <short name for the check, separated by _> -d <description of the check>
```

The above command will create the template .py and pytest files. For eg:

```
(py396) amits-mbp-2:custom-checks amit$ ls -l actions/aws_list_public_sg/
total 24
-rw-r--r--  1 amit  staff     0 Sep 25 17:42 __init__.py
-rw-r--r--  1 amit  staff   349 Sep 25 17:42 aws_list_public_sg.json
-rw-r--r--  1 amit  staff  2557 Sep 25 17:44 aws_list_public_sg.py
-rw-r--r--  1 amit  staff  1409 Sep 25 21:09 test_aws_list_public_sg.py
```

4. Edit the <short_name>.py (in the above eg, its aws_list_public_sg.py) and write the logic for the check. Please ensure that you define the InputSchema as well, if required.

5. In order to test the check, you need to add a credential for the check. You can use the following utility to add credential
```
./Awesome-CloudOps-Automation/bin/add_creds.sh -c <Credential type> -h
```

6. Once the credential is programmed, you are ready to test out the check using pytest (Please ensure that pytest is installed on your workstation). You can test the check by running:

```
 pytest -s actions/<short_name>/test_<short_name>.py
```

Please ensure if your check requires any inputs, you fill the *InputParamsJson* accordingly.

### Creating custom actions using jupyterlab

You can refer to [this link](https://docs.unskript.com/unskript-product-documentation/actions/create-custom-actions) on how to create custom Action using Jupyter Lab interface

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

### How to specify values for arguments used in checks

You can sepcify the values for the arguments that are used in the Checks in the Global file `unskript_config.yaml` You can see an example
of that file in `unskript-ctl` Folder.

* In your `YOUR_REPO_DIRECTORY/actions/` Directory create a file unskript_config.yaml
   > touch $YOUR_REPO_DIRECTORY/actions/unskript_config.yaml
* Update the contents of the unskript_config.yaml file like so.
   ```
   globals:
      namespace: "awesome-ops"
      threshold: "string"
      region: "us-west-2"
      services: ["calendar", "audit"]
   ```

> Here namespace is the argument used in the checks and "awesome-ops" is the value assigned to that argument.


### Creating a scheule for checks to run periodically

You can create a schedule to run built-in (pre-coded) or custom checks. This recipie describes how to configure the docker so it runs the schedule 
periodically. 

1. Copy the scheduler template file to  `YOUR_REPO_DIRECTORY`
```
cp YOUR_REPO_DIRECTORY/Awesome-CloudOps-Automation/templates/scheduler.template  YOUR_REPO_DIRECTORY/scheduler
```
2. The contents of the scheduler template file are as follows
```
#!/bin/bash

* * * * * /usr/local/bin/unskript-ctl.sh -rc --type k8s, aws --report

```

The line with `*` should be familiar to you as it is in the same lines as `cronjob`.  To learn more about what is
cronjob, and what each `*` mean, please refer [here](https://crontab.guru/every-5-minutes).

3. Modify the `scheduler` file to add all the tests you want to run. In the above snippets, all checks for connectors `k8s` and `aws` are
schedled to run. Edit the cadence at which the scheduler should run and also change the type of connectors you want the checks to run against.

4. Open your Custom Build Dockerfile From the step [above](#building-custom-docker) And Add the following line before the `CMD` line like so:
```
FROM unskript/awesome-runbooks:latest as base
COPY custom/actions/. /unskript/data/actions/
COPY custom/runbooks/. /unskript/data/runbooks/

# Copy the populate_credentials.sh file to ./
COPY populate_credentials.sh .
RUN chmod +x populate_credentials.sh

# Copy Scheduler file to ./
COPY scheduler .
RUN chmod 600 scheduler

CMD ["./start.sh"]
```
In the above snippet, we have modfied the `Dockerfile.template` to copy the `scheduler` to docker so that it can register
the scheduler to run at the desired frequency. 

5. Build the docker as explained above and when your custom docker is booted, it will have the scheduler ready to run!