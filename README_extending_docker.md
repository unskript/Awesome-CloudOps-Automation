<center>
  <a href="https://github.com/unskript/Awesome-CloudOps-Automation">
    <img src="https://unskript.com/assets/favicon.png" alt="Logo" width="80" height="80">
  </a>
  <h1> Extending Awesome Docker </h1>
</center>


## Extending the docker
You can use our base docker to extend the functionality to fit your need. The steps below could be used to package your custom Actions and re-build your custom docker that you can upload and distribute to/from any docker registry. 

### Pre-requisite
1. You have a working Python 3 environment installed on your build system
2. You have Docker-ce installed on your build system

### Steps 
1. If you have not already done, please check-out the Awesome-CloudOps-Automation repo with this command

   ```
   cd $HOME 
   git clone https://github.com/unskript/Awesome-CloudOps-Automation
   ``` 

2. Set an environment variable to point to the name of the custom directory. 
   ```
   export CUSTOM_DIR_NAME=custom
   ```

3. Next task is to create a custom Actions directory under Awesome-CloudOps-Automation. You could use any of
   the following methods to accomplish this task.
    1. Create directory under Awesome-CloudOps-Automation by name `$CUSTOM_DIR_NAME`
       ```
       cd $HOME/Awesome-CloudOps-Automation
       mkdir $CUSTOM_DIR_NAME
       ```
    2. Submodule your Git repo that has your custom Actions in it. 
       ```
       cd $HOME/Awesome-CloudOps-Automation
       git submodule add https://<YOUR REPO LOCATION> $CUSTOM_DIR_NAME
       ```

4. Launch the Awesome Runbooks Docker. 
      ```
      docker run -it -p 8888:8888 \
             -v $HOME/.unskript:/unskript  \
             -v $HOME/Awesome-CloudOps-Automation/$CUSTOM_DIR_NAME:/data \
             --user root \
             unskript/awesome-runbooks:latest
      ```
      
      > Tip: If you are interested in building your custom docker image off of a Tag, you can replace the `latest` keyword
      > in the above command with the tag number. You can find the tags [Here](https://hub.docker.com/r/unskript/awesome-runbooks/tags)

    * Here you may notice we have two `-v` mount point. The first one `$HOME/.unskript` is for storing credentials.   
    * The second mount point `$HOME/Awesome-CloudOps-Automation/$CUSTOM_DIR_NAME` is where we save custom Actions or custom Runbooks. 
    
       > Note: This means any content that is created will survive Docker reboots.

    * You would see a Welcome Message once the Docker starts. At this juncture point your browser to `http://127.0.0.1:8888/lab/tree/GetStarted.ipynb` (We recommend Google Chrome or MS Edge or Chromium)
    
5. Once the page is loaded, Search for any pre-coded actions by typing keywords like `aws`, `kubernetes` `kubectl`,  `postgresql`, `mongo` etc..
   Pick the standard Action that you want to extend the functionality, drag-n-drop it to the main cell area. You can refer [to this](https://docs.unskript.com) to get familiar with the UI.

6. After you are done with the modification, you can use the `Save-As` option to save your custom Action. You can refer  [to this](https://docs.unskript.com) on how to save custom Action.

   > Tip: If you want to verify the modification, you can create a credential for the given connector and test your modification to make sure
   > you are satisfied with the changes.

7. Next step is to build your custom docker. Following these commands

   ```
   1. export CUSTOM_DOCKER_NAME=my-awesome-docker
   2. export CUSTOM_DOCKER_VERSION='0.1.0'
   3. cd $HOME/Awesome-CloudOps-Automation/
   4. cp ./build/templates/Dockerfile.template Dockerfile
   5. docker build -t $CUSTOM_DOCKER_NAME:$CUSTOM_DOCKER_VERSION .
   ```

   It may take a few minutes to build the docker, once built, you can verify it using 

   ```
   docker run -it -p 8888:8888 \
       $CUSTOM_DOCKER_NAME:$CUSTOM_DOCKER_VERSION 
   ```

   This would run your `custom docker` and you can point your browser to `http://127.0.0.1:8888/lab/tree/Welcome.ipynb`! 

8. Push your `custom docker` to any docker registry for redistribution.
<br/>

