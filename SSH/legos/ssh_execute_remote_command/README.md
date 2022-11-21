[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>SSH Execute Remote Command</h2>

<br>

## Description
This Lego executes the given command on the remote.


## Lego Details

    ssh_execute_remote_command(sshClient, hosts: List[str], command: str, sudo: bool)

        sshClient: Object of type unSkript ssh Connector
        hosts: List of hosts to connect to. For eg. ["host1", "host2"].
        command: Command to be executed on the remote server.
        sudo: Run the command with sudo.

## Lego Input
This Lego take four inputs handle, hosts, command and sudo.

## Lego Output
Here is a sample output.
<img src="./1.png">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)