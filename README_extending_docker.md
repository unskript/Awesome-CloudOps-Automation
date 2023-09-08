<center>
  <a href="https://github.com/unskript/Awesome-CloudOps-Automation">
    <img src="https://unskript.com/assets/favicon.png" alt="Logo" width="80" height="80">
  </a>
  <h1> Extending Awesome Docker </h1>
</center>


## Extending the docker
You can use our base docker to extend the functionality to fit your need. The steps below could be used to package your custom Actions and re-build your custom docker that you can upload and distribute to/from any docker registry. 

><strong>Pre-requisite</strong>
>1. You have a working Python 3 environment installed on your build system
>2. You have Docker-ce installed on your build system

Lets consider two scenarios as starting point for extending Awesome docker

### Deployed as a POD in a kubernetes cluster

>You have just deployed Awesome Runbooks docker instance as a POD in your kubernetes cluster. We assume you have a PVC attached to the POD with mount path as /unskript 

Then follow these steps

#### Steps for docker deployed as K8S POD

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

6. Now copy the custom actions from the PVC to your local machine so you can bundle into your custom Docker for re-distribution
```
kubectl cp <AWESOME_POD_NAME>:/unskript/data/runbooks -n <NAMESPACE> /path/to/your/work/directory/runbooks
kubectl cp <AWESOME_POD_NAME>:/unskript/data/actions -n <NAMESPACE> /path/to/your/work/directory/actions
cd /path/to/your/work/directory
git clone https://github.com/unskript/Awesome-CloudOps-Automation.git

Example:

kubectl cp awesome-runbooks-0:/unskript/data/actions -n awesome-ops $HOME/Workspace/actions 
kubectl cp awesome-runbooks-0:/unskript/data/runbooks -n awesome-ops $HOME/Workspace/runbooks 
cd $HOME/Workspace
git clone https://github.com/unskript/Awesome-CloudOps-Automation.git
export ACA_ROOTDIR=$PWD

```

7. Next step is to build your custom docker from the Awesome-CloudOps-Automation directory

   ```
   export CUSTOM_DOCKER_NAME=my-awesome-docker
   export CUSTOM_DOCKER_VERSION='0.1.0'
   cd $ACA_ROOTDIR
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

8. Push your `custom docker` to any docker registry for redistribution.
<br/>


### Deployed as a local docker instance

>You dont have any custom Actions created and you are starting fresh to create your custom Actions. 

Then follow these steps


#### Steps for local Docker deployment
You can add Awesome-CloudOps-Automation as a submodule to your existing Git repo so that you can include
your custom Actions and/or runbooks and build a custom Docker image.
1. 
    1. Here we assume $HOME/Workspace is where you have your Git repo cloned
       ```
       cd $HOME/Workspace  # Please change this directory whereever your Git repo is cloned
       export $ACA_ROOTDIR=$PWD
       ```
    2. Submodule your Git repo that has your custom Actions in it. 
       ```
       cd $ACA_ROOTDIR
       git submodule add https://github.com/unskript/Awesome-CloudOps-Automation Awesome-CloudOps-Automation
       ```

2. If you have not already done, please check-out the Awesome-CloudOps-Automation repo with this command

   ```
   mkdir $HOME/Workspace  # Change this to any other location where you want to build the docker
   mkdir -p actions runbooks 
   ```

4. Launch the Awesome CloudOps Docker. 
      ```
      docker run -it -p 8888:8888 \
             -v $HOME/.unskript:/unskript/credentials  \
             -v $ACA_ROOTDIR/actions:/unskript/data/actions \
             -v $ACA_ROOTDIR/runbooks:/unskript/data/runbooks \
             -e ACA_AWESOME_MODE=1 \
             --user root \
             unskript/awesome-runbooks:latest
      ```
      
      > Tip: If you are interested in building your custom docker image off of a Tag, you can replace the `latest` keyword
      > in the above command with the tag number. You can find the tags [Here](https://hub.docker.com/r/unskript/awesome-runbooks/tags)

    * Here you may notice we have two `-v` mount point. The first one `$HOME/.unskript` is for storing credentials.   
    
    * You would see a Welcome Message once the Docker starts. At this juncture point your browser to `http://127.0.0.1:8888/lab/tree/GetStarted.ipynb` (We recommend Google Chrome or MS Edge or Chromium)
    
5. Once the page is loaded, Search for any pre-built actions by typing keywords like `aws`, `kubernetes` `kubectl`,  `postgresql`, `mongo` etc. To pick the Action that you want to extend, drag-n-drop it to the main notebook area. You can refer [to this](https://docs.unskript.com) to get familiar with the UI.

6. After you are done with the modifications, you can use the `Save-As` option to save your custom Action. You can refer  [to this](https://docs.unskript.com) on how to save custom Action.

   > Tip: If you want to verify the modification, you can create a credential for the given connector and test your modification to make sure
   > you are satisfied with the changes.

7. Next step is to build your custom docker from the Awesome-CloudOps-Automation directory

   ```
   export CUSTOM_DOCKER_NAME=my-awesome-docker
   export CUSTOM_DOCKER_VERSION='0.1.0'
   cd $ACA_ROOTDIR
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

8. Push your `custom docker` to any docker registry for redistribution.
<br/>