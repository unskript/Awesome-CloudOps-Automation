<center>
  <a href="https://github.com/unskript/Awesome-CloudOps-Automation">
    <img src="https://unskript.com/assets/favicon.png" alt="Logo" width="80" height="80">
  </a>
  <h1> Extending Awesome Docker </h1>
</center>


## Extending the docker
You can use our base docker to extend the functionality to fit your need. The steps below could be used to package your custom Actions/Runbooks and re-build your custom docker that you can upload and distribute to/from any docker registry.

---
**NOTE**

unskript-ctl config is stored in unskript_ctl_config.yaml. Please look at the template at
```
/unskript-ctl/config/unskript_ctl_config.yaml
```

To package your unskript-ctl config, do the following:

* Make your version of unskript_ctl_config.yaml
* Uncomment the following line in the Dockerfile
```
#COPY unskript_ctl_config.yaml /etc/unskript/unskript_ctl_config.yaml
```
---


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
      Awesome-CloudOps-Automation/
      your-repo-folders/
      your-repo-files
      ...
   ```
4. You have a working Python 3 environment installed on your build system
5. You have `make` and other build tools installed on your build system
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

You can specify the values for the arguments that are used in the Checks in the **checks** section of the unskript_ctl_config.yaml. For eg:
   ```
   checks:
     # Arguments common to all checks, like region, namespace, etc.
     arguments:
       global:
         region: us-west-2
         namespace: "awesome-ops"
         threshold: "string"
         services: ["calendar", "audit"]
   ```

> Here namespace is the argument used in the checks and "awesome-ops" is the value assigned to that argument.

#### Multiple values support
You can specify multiple values for an argument, using the keyword **matrix**. For eg:
```
checks:
  # Arguments common to all checks, like region, namespace, etc.
  arguments:
    global:
      matrix:
       namespace: [n1, n2]
```

The above config makes unskript-ctl run for 2 values of namespace.

**NOTE**: We support exactly ONE argument of type **matrix**.

### Creating a schedule for checks to run periodically

To schedule checks, you first need to define a **job**.

A job can be a set of checks or connector types.

In future, we will support suites and custom scripts.

A job **SHOULD** have a unique name.

You define a job in the **jobs** section of the unskript_ctl_config.yaml.

Once you have define a job, you can use that job name to configure a schedule.

The schedule can be configured in the **scheduler** section of the config file.

For the schedule, you need to define the following:
* cadence - cron style of cadence.
* job_name - name of the job for the schedule.

### How to get checks run report via email/slack

You can configure the email/slack notification via the **notification** section of the config file.

For email, we support 3 providers:

1. SMTP: Any smtp server
2. SES: Amazon SES
3. Sendgrid

Once configured, you are all set to receive the report whenever check is run with `--report` option
```
unskript-ctl.sh -r --check --type k8s, aws, postgresql --report
```

Here, the checks for all three connectors, k8s, aws and postgresql are run and the result is sent via slack  or email to the recipient.
