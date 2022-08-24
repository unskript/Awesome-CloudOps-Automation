
# ![#fc4103](https://via.placeholder.com/15/fc4103/fc4103.png) Awesome-CloudOps-Automation

unSkript offers an open source version of its platform with a finite set of functionality. You can easily set up an environment and navigate it to get an ide
a of the actual platform.

## Docker command to pull the image

#### - For Windows, Linux, and macOS(x86)-
```
docker run -it -p 8888:8888 \\
    -v $HOME/.unskript:/data  \\
    -e NB_USER=jovyan \\
    -e CHOWN_HOME=yes \\
    -e CHOWN_EXTRA_OPTS='-R' \\
    --user root \\
    -w /home/jovyan \\
    public.ecr.aws/unskript/awesome-runbooks:latest
```
#### - For macOS M1-
```
docker run -it -p 8888:8888 \\
    -v $HOME/.unskript:/data  \\
    -e NB_USER=jovyan \\
    -e CHOWN_HOME=yes \\
    -e CHOWN_EXTRA_OPTS='-R' \\
    --user root \\
    -w /home/jovyan \\
   public.ecr.aws/unskript/awesome-runbooks:v0.6.0-arm64
```
Once the image is downloaded, you can run the following links in your browser to check out the xRunBooks-

### 1. AWS [view details](https://simplistic-twilight-7e8.notion.site/AWS-xRunBook-for-Restarting-an-EC2-Instance-d5d1ce7ab1d8418592c4ec389d6ef84e)
#### - Restart AWS EC2 Instances
###### [Link to Environment](http://127.0.0.1:8888/lab/tree/Restart_AWS_EC2_Instances.ipynb)

### 2. MongoDB [view details](https://simplistic-twilight-7e8.notion.site/MongoDB-xRunBook-for-Server-Connectivity-031c156f40154eda9b9c67520ea2a8aa)
#### - MongoDB server connectivity/ Kill long-running queries
###### [Link to Environment](http://127.0.0.1:8888/lab/tree/MongoDB_Server_Connectivity.ipynb)

### 3. Kubernetes [view details]()
#### - K8s Pod stuck in CrashLoopBack state
###### [Link to Environment](http://127.0.0.1:8888/lab/tree/K8S_Pod_Stuck_In_CrashLoopBack_State.ipynb)
#### - K8s Pod stuck in ImagePullBackOff state
###### [Link to Environment](http://127.0.0.1:8888/lab/tree/K8S_Pod_Stuck_In_ImagePullBackOff_State.ipynb)
#### - K8s Pod stuck in Terminating state
###### [Link to Environment](http://127.0.0.1:8888/lab/tree/K8S_Pod_Stuck_In_Terminating_State.ipynb)
