[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>SCP: Remote file transfer over SSH</h2>

<br>

## Description
This Lego Copy files from or to remote host. Files are copied over SCP.


## Lego Details

    ssh_scp(sshClient, host: str, remote_file: str, local_file: str, direction: bool)

        sshClient: Object of type unSkript ssh Connector
        host: Host to connect to. Eg 10.10.10.10.
        remote_file: Filename on the remote server. Eg /home/ec2-user/my_remote_file
        local_file: Filename on the unSkript proxy. Eg /tmp/my_local_file
        direction: Direction of the copy operation. Default is receive-from-remote-server

## Lego Input
This Lego take five inputs sshClient, host, remote_file, local_file and direction.

## Lego Output
Here is a sample output.
<img src="./1.png">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)