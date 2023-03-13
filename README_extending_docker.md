<center>
  <a href="https://github.com/unskript/Awesome-CloudOps-Automation">
    <img src="https://unskript.com/assets/favicon.png" alt="Logo" width="80" height="80">
  </a>
  <h1> Extending Awesome Docker </h1>
</center>


## Extending the docker
You can use our base docker to extend the functionality to fit your need. The recepie below could be used to package your custom Actions and re-build your custom docker that you can upload and distribute to/from any docker registry. 

### Pre-requisite
1. You have a working Python 3 environment installed on your build system
2. You have Docker-ce installed on your build system

### Receipe 
1. If you have not already done, Please check-out the Awesome-CloudOps-Automation repo with this command
   ```cd $HOME && git clone https://github.com/unskript/Awesome-CloudOps-Automation``` 

2. Set an environment variable to point to the name of the custom directory. 
   ```export CUSTOM_DIR_NAME=custom```

3. Next task is to create a custom Actions directory under Awesome-CloudOps-Automation. You could use any of
   the following methods to accomplish this task.
    1. Create directory under Awesome-CloudOps-Automation by name `custom`
       ```cd $HOME/Awesome-CloudOps-Automation && mkdir $CUSTOM_DIR_NAME```
    2. Submodule your Git repo that has your custom Actions in it. 
       ```cd $HOME/Awesome-CloudOps-Automation && git submodule add https://<YOUR REPO LOCATION> $CUSTOM_DIR_NAME```

4. Launch the Awesome Runbooks Docker. Either you can use a specific tag like `930` or `latest` 
      ```
      docker run -it -p 8888:8888 \
             -v $HOME/.unskript:/unskript  \
             -v $HOME/Awesome-CloudOps-Automation/$CUSTOM_DIR_NAME:/data \
             --user root \
             unskript/awesome-runbooks:latest
      ```

    Here you may notice we have two `-v` mount point. The first one `$HOME/.unskript` is for storing Awesome Docker settings so all the credentials that you create are saved for the next run.  The second mount point
    `$HOME/Awesome-CloudOps-Automation/$CUSTOM_DIR_NAME` is where we inform Awesome Docker to save any new custom Legos or Runbooks in that directory. This means any content that is created will survive Docker reboots.

    You would see a welcome message that tells you to point your browser to `http://127.0.0.1:8888/lab/tree/Welcome.ipynb` Please do copy this URL and open it in your favorite browser (We recommend Google Chrome or MS Edge or Chromium)
    
5. Once the page is loaded. Go to the end of the Welcome page.  

As the Page loads, you would see `Credentials` Options on top of the Page. Please click it and Create
   new credentials for the `Connectors` that you are working on. Example, if you are working on Kubernetes, you may
   want to create a K8S credential. 

4. Once the credential is saved, you would see a message like `Active` to indicate that the credential was
   created successfuly and is ready to be used.  Go ahead and create your own `Custom Action` and use the `Save As`
   Option in the Action toolbar to save the custom action. 

5. Next, lets package the `Custom Action` into a new Docker build that is based off of `awesome-runbooks` 
   Please Copy The content below and paste it to a file by name `Dockerfile` under `$HOME/Awesome-CloudOps-Automation`
    ```
    FROM unskript/awesome-runbooks:930 as base 
    RUN mkdir -p /data
    ADD custom /data/ 

    CMD ["./start.sh"]
    ```

    Now execute the docker build command `docker build -t <YOUR CUSTOM NAME>:<CUSTOM VERSION> .` 

    Build may take a few minutes, Once built, You can distribute the docker image via publishing to any docker registry.
<br/>

