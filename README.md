[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>unSkript Runbooks</h1>


# unSkript Runbooks

This Directory has unSkript runbooks seperated by each category. Please choose the Links Below to navigate to the respective Runbook. 

1. [MongoDB](./mongodb/README.md)
2. [K8S](./k8s/README.md)
3. [AWS](./aws/README.md)


# How to bring up on Intel based platform (x86 based) (Windows/Linux/Mac)

`docker run -it -p 8888:8888 \
    -v $HOME/.unskript:/data  \
    -e NB_USER=jovyan \
    -e CHOWN_HOME=yes \
    -e CHOWN_EXTRA_OPTS='-R' \
    --user root \
    -w /home/jovyan \
    public.ecr.aws/unskript/awesome-runbooks:latest`

New files are created inside the docker and will persist unless --rm option is given (which we have not suggested)
ie
Save-As function can be used, but user has to remember the file name and insert in the URL


# Using the Runbook
Point your browser to any of these URL to open the Runbook.

1. http://127.0.0.1:8888/lab/tree/K8S_Pod_Stuck_In_CrashLoopBack_State.ipynb
2. http://127.0.0.1:8888/lab/tree/MongoDB_Server_Connectivity.ipynb
3. http://127.0.0.1:8888/lab/tree/K8S_Pod_Stuck_In_ImagePullBackOff_State.ipynb
4. http://127.0.0.1:8888/lab/tree/Restart_AWS_EC2_Instances.ipynb
5. http://127.0.0.1:8888/lab/tree/K8S_Pod_Stuck_In_Terminating_State.ipynb
6. http://127.0.0.1:8888/lab/tree/Configure-url-endpoint-on-a-cloudwatch-alarm.ipynb
7. http://127.0.0.1:8888/lab/tree/Detect-ECS-failed-deployment.ipynb
8. http://127.0.0.1:8888/lab/tree/Display-postgresql-long-running.ipynb
9. http://127.0.0.1:8888/lab/tree/ec2-disk-cleanup.ipynb
10. http://127.0.0.1:8888/lab/tree/fetch-jenkins-build-logs.ipynb
11. http://127.0.0.1:8888/lab/tree/get-aws-elb-unhealthy-instances.ipynb
12. http://127.0.0.1:8888/lab/tree/get-kube-system-config-map.ipynb
13. http://127.0.0.1:8888/lab/tree/k8s-get-candidate-nodes-given-config.ipynb
14. http://127.0.0.1:8888/lab/tree/resize-ebs-volume.ipynb
15. http://127.0.0.1:8888/lab/tree/resize-pvc.ipynb
16. http://127.0.0.1:8888/lab/tree/restart-aws-instance-given-tag.ipynb
17. http://127.0.0.1:8888/lab/tree/restart-unhealthy-services-target-group.ipynb


# Where data is stored

Inside the docker there is `/data` folder that is where we store the `credentials` and `runbooks`.
So if you would like to retain the `connectors` and `runbooks` you can use the docker's `-v` option
to retain the changes done on the `docker`. 


# TODO

1. Update build pipelines to take care of pushing to public repo (need new build target)
2. Create a symlink in the docker, so that URL is always same across different dockers for different runbooks
3. Need to package awesome legos
4. AWS v2 credential needs to be packaged and tested

