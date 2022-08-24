[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png)
<h1>unSkript Runbooks</h1>


# unSkript Runbooks

This Repository has unSkript runbooks seperated by each category. Please choose the Links Below to navigate to the respective Runbooks.

1. [MongoDB](./Mongo/README.md)
2. [K8S](./Kubernetes/README.md)
3. [AWS](./AWS/README.md)
4. [Jenkins](./Jenkins/README.md)
5. [Postgresql](./Postgresql/README.md)


# How to bring up on Intel based platform (x86 based) (Windows/Linux/Mac)

```
docker run -it -p 8888:8888 \
     -v $HOME/.unskript:/data \
     -e NB_USER=jovyan \
     -e CHOWN_HOME=yes \
     -e CHOWN_EXTRA_OPTS='-R' \
     --user root \
     -w /home/jovyan \ 
     public.ecr.aws/unskript/awesome-runbooks:latest
```

# How to bring up on Arm based platform (arm64) (Windows/Linux/Mac)
```
docker run -it -p 8888:8888 \
    -v $HOME/.unskript:/data  \
    -e NB_USER=jovyan \
    -e CHOWN_HOME=yes \
    -e CHOWN_EXTRA_OPTS='-R' \
    --user root \
    -w /home/jovyan \
   public.ecr.aws/unskript/awesome-runbooks:v0.6.0-arm64
```

New files are created inside the docker and will persist unless --rm option is given (which we have not suggested)
ie
Save-As function can be used, but user has to remember the file name and insert in the URL


# Using the Runbook
Once you run the above command, point your browser to any of these URL to open the Runbook.

1. http://127.0.0.1:8888/lab/tree/K8S_Pod_Stuck_In_CrashLoopBack_State.ipynb
2. http://127.0.0.1:8888/lab/tree/MongoDB_Server_Connectivity.ipynb
3. http://127.0.0.1:8888/lab/tree/K8S_Pod_Stuck_In_ImagePullBackOff_State.ipynb
4. http://127.0.0.1:8888/lab/tree/Restart_AWS_EC2_Instances.ipynb
5. http://127.0.0.1:8888/lab/tree/K8S_Pod_Stuck_In_Terminating_State.ipynb
6. http://127.0.0.1:8888/lab/tree/Configure-url-endpoint-on-a-cloudwatch-alarm.ipynb
7. http://127.0.0.1:8888/lab/tree/Detect-ECS-failed-deployment.ipynb
8. http://127.0.0.1:8888/lab/tree/Display-postgresql-long-running.ipynb
9. http://127.0.0.1:8888/lab/tree/EC2-Disk-Cleanup.ipynb
10. http://127.0.0.1:8888/lab/tree/Fetch-Jenkins-Build-Logs.ipynb
11. http://127.0.0.1:8888/lab/tree/Get-Aws-Elb-Unhealthy-Instances.ipynb
12. http://127.0.0.1:8888/lab/tree/Get-Kube-System-Config-Map.ipynb
13. http://127.0.0.1:8888/lab/tree/K8S-Get-Candidate-Nodes-Given-Config.ipynb
14. http://127.0.0.1:8888/lab/tree/Resize-EBS-Volume.ipynb
15. http://127.0.0.1:8888/lab/tree/Resize_PVC.ipynb
16. http://127.0.0.1:8888/lab/tree/Restart-Aws-Instance-given-Tag.ipynb
17. http://127.0.0.1:8888/lab/tree/Restart-Unhealthy-Services-Target-Group.ipynb


# Where data is stored

Inside the docker there is `/data` folder that is where we store the `credentials` and `runbooks`.
So if you would like to retain the `connectors` and `runbooks` you can use the docker's `-v` option
to retain the changes done on the `docker`.

# Documentation
Detail documentation at [docs](https://unskript.gitbook.io/unskript-product-documentation/open-source/docker-for-oss)

# Community
Join us on Slack @ http://awesome-runbooks.slack.com/ 

# TODO

1. Update build pipelines to take care of pushing to public repo (need new build target)
2. Package testcases

