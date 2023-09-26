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



## How to Copy Custom Actions and Runbook

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

Lets consider two scenarios as starting point for extending Awesome docker

### How to create Custom Actions

You can create custom action on your workstation using your editor. Please follow the steps below to setup your workstation:

1. Install the following pip packages:
```
pip install unskript-core
pip install unskript-custom
```
2. To create a new check template files, do the following:
```
cd $YOUR_REPO_DIRECTORY

./Awesome-CloudOps-Automation/bin/unskript-add-check.sh -t <Check type> -n <short name for the check, separated by _> -d <description of the check>

```
The above command will create the template .py and pytest files. For eg:
```
(py396) amits-mbp-2:custom-checks amit$ ls -l actions/aws_list_public_sg/
total 24
-rw-r--r--  1 amit  staff     0 Sep 25 17:42 __init__.py
drwxr-xr-x  5 amit  staff   160 Sep 25 21:09 __pycache__
-rw-r--r--  1 amit  staff   349 Sep 25 17:42 aws_list_public_sg.json
-rw-r--r--  1 amit  staff  2557 Sep 25 17:44 aws_list_public_sg.py
-rw-r--r--  1 amit  staff  1409 Sep 25 21:09 test_aws_list_public_sg.py
```

3. Edit the <short_name>.py (in the above eg, its aws_list_public_sg.py) and write the logic for the check. Please ensure that you define the InputSchema as well, if required.

4. In order to test the check, you need to add an credential for the check. You can use the following utility to add credential
```
./Awesome-CloudOps-Automation/bin/add_creds.sh -c <Credential type> -h
```

5. Once the credential is programmed, you are ready to test out the check using pytest (Please ensure that pytest is installed on your workstation).
You can test the check by running:
```
 pytest -s actions/<short_name>/test_<short_name>.py
```
Please ensure if your check requires any inputs, you fill the **InputParamsJson** accordingly.
