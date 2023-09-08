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
   git submodule add http://github.com/Awesome-CloudOps-Automation.git Awesome-CloudOps-Automation
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
   cp Awesome-CloudOps-Automation/build/templates/Dockerfile.template Dockerfile
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

#### Steps for awesome-runbooks deployed as K8S POD

1. First port-forward the docker instance's port `8888` to your local host
```
kubectl port-forward pod/<AWESOME_POD_NAME> -n <NAMESPACE> 8888:8888
```
2. Launch your browser and point to `http://127.0.0.1:8888/awesome` 
3. Click on any of the Runbook that is of interest to open it in a new browser tab.
4. Once the page is loaded, Search for any pre-built actions by typing keywords like `aws`, `kubernetes` `kubectl`,  `postgresql`, `mongo` etc. To pick the Action that you want to extend, drag-n-drop it to the main notebook area. You can refer [to this](https://docs.unskript.com) to get familiar with the UI.

5. After you are done with the modifications, you can use the `Save-As` option to save your custom Action. You can refer  [to this](https://docs.unskript.com) on how to save custom Action.

   > Tip: If you want to verify the modification, you can create a credential for the given connector and test your modification to make sure
   > you are satisfied with the changes.

<br/>


#### Steps for awesome-runbooks deployed as docker

1. Launch the Awesome CloudOps Docker. 
      ```
      docker run -it -p 8888:8888 \
             -v $HOME/.unskript:/unskript/credentials  \
             -v $YOUR_REPO_DIRECTORY/actions:/unskript/data/actions \
             -v $YOUR_REPO_DIRECTORY/runbooks:/unskript/data/runbooks \
             -e ACA_AWESOME_MODE=1 \
             --user root \
             unskript/awesome-runbooks:latest
      ```
      
      > Tip: If you are interested in building your custom docker image off of a Tag, you can replace the `latest` keyword
      > in the above command with the tag number. You can find the tags [Here](https://hub.docker.com/r/unskript/awesome-runbooks/tags)

    * Here you may notice we have two `-v` mount point. The first one `$HOME/.unskript` is for storing credentials.   
    
    * You would see a Welcome Message once the Docker starts. At this juncture point your browser to `http://127.0.0.1:8888/lab/tree/GetStarted.ipynb` (We recommend Google Chrome or MS Edge or Chromium)
    
2. Once the page is loaded, Search for any pre-built actions by typing keywords like `aws`, `kubernetes` `kubectl`,  `postgresql`, `mongo` etc. To pick the Action that you want to extend, drag-n-drop it to the main notebook area. You can refer [to this](https://docs.unskript.com) to get familiar with the UI.

3. After you are done with the modifications, you can use the `Save-As` option to save your custom Action. You can refer  [to this](https://docs.unskript.com) on how to save custom Action.

   > Tip: If you want to verify the modification, you can create a credential for the given connector and test your modification to make sure
   > you are satisfied with the changes.
<br/>