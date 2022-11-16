[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h2>SSH: Locate large files on host</h2>

<br>

## Description
This Lego scans the file system on a given host and returns a dict of large files. The command used to perform the scan is \"find inspect_folder -type f -exec du -sk '{}' + | sort -rh | head -n count\".


## Lego Details

    ssh_execute_remote_command(sshClient, host: str, inspect_folder: str, threshold: int,
                                sudo: bool, count: int)

        sshClient: Object of type unSkript ssh Connector
        hosts: Host to connect to. Eg 10.10.10.10.
        inspect_folder: Folder to inspect on the remote host.
        sudo: Run the scan with sudo.
        threshold: Threshold the files on given size. Specified in Mb. Default is 100Mb.
        count: Number of files to report from the scan. Default is 10.

## Lego Input
This Lego take six inputs sshClient, hosts, inspect_folder, threshold, count and sudo.

## Lego Output
Here is a sample output.
<img src="./1.png">

## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)