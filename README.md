[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>unSkript Runbooks</h1>


# unSkript Runbooks

This Directory has unSkript runbooks seperated by each category. Please choose the Links Below to navigate to the respective Runbook. 

1. [MongoDB](./mongodb/README.md)
2. [K8S](./k8s/README.md)


How to bring up on Mac (x86 based)

docker run -it -p 8888:8888 \
    -v $HOME/.unskript:/home/jovyan/.local  \
    -e NB_USER=jovyan \
    -e CHOWN_HOME=yes \
    -e CHOWN_EXTRA_OPTS='-R' \
    --user root \
    -w /home/jovyan \
public.ecr.aws/unskript/awesome-runbooks:latest

New files are created inside the docker and will persist unless --rm option is given (which we have not suggested)
ie
Save-As function can be used, but user has to remember the file name and insert in the URL



Point your browser to the following URL (use the 127.0.0.1)

[C 2022-08-18 21:42:05.542 ServerApp]

    To access the server, open this file in a browser:
        file:///home/jovyan/.local/share/jupyter/runtime/jpserver-7-open.html
    Or copy and paste one of these URLs:
        http://34bd1f6d1868:8888/lab/tree/MongoDB_Server_Connectivity.ipynb?token=f6c782cf1cb242d4ea846fd1c0c906c069b4efb547620088
     or http://127.0.0.1:8888/lab/tree/MongoDB_Server_Connectivity.ipynb?token=f6c782cf1cb242d4ea846fd1c0c906c069b4efb547620088. <<<

Issues

1. Move docker into prod ECR (see this: https://stackoverflow.com/questions/62840036/aws-ecr-repository-how-to-copy-images-from-one-account-and-push-to-another-acc)
2. Such ECR needs to be public
3. Update build pipelines to take care of pushing to public repo (need new build target)
4. Create a symlink in the docker, so that URL is always same across different dockers for different runbooks
5. Need to package awesome legos
6. AWS v2 credential needs to be packaged and tested
7. Redirect output from jupyter into file

