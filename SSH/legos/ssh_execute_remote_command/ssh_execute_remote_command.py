##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import pprint
from unskript.enums.ssh_enums import SSHAuthType


class InputSchema(BaseModel):
    hosts: List[str] = Field(
        title='Hosts',
        description='List of hosts to connect to. For eg. ["host1", "host2"].'
    )
    command: str = Field(
        title='Command',
        description='Command to be executed on the remote server.'
    )
    sudo: Optional[bool] = Field(
        default=False,
        title='Run with sudo',
        description='Run the command with sudo.'
    )
    proxy_host: Optional[str] = Field(
        title='Proxy host',
        description='Override the proxy host provided in the credentials. It still uses the proxy_user and port from the credentials.'
    )


def ssh_execute_remote_command_printer(output):
    if output is None:
        return
    print("\n")
    pprint.pprint(output)


def ssh_execute_remote_command(sshClient, hosts: List[str], command: str, sudo: bool = False, proxy_host: str = None) -> Dict:
    """ssh_execute_remote_command executes the given command on the remote

        :type hosts: List[str]
        :param hosts: List of hosts to connect to. For eg. ["host1", "host2"].

        :type command: str
        :param command: Command to be executed on the remote server.

        :type sudo: bool
        :param sudo: Run the command with sudo.

        :type proxy_host: str
        :param proxy_host: Optional proxy host to use.

        :rtype: dict of command output
    """

    client = sshClient(hosts)
    if proxy_host is not None:
        #Need to do the following:
        # 1. Close the existing handles.
        # 2. Create new handles using the new proxy_host.
        client.join()
        client =  client.duplicate(hosts, proxy_host)

    runCommandOutput = client.run_command(command=command, sudo=sudo)
    client.join()
    res = {}

    for host_output in runCommandOutput:
        hostname = host_output.host
        output = []
        for line in host_output.stdout:
            output.append(line)

        o = "\n".join(output)
        res[hostname] = o

    return res
