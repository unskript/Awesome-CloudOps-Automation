##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import pprint


class InputSchema(BaseModel):
    hosts: List[str] = Field(
        title='Hosts',
        description='List of hosts to connect to. For eg. ["host1", "host2"].'
    )
    service_name: str = Field(
        title='Service Name',
        description='Service name to restart.'
    )
    sudo: Optional[bool] = Field(
        default=False,
        title='Restart with sudo',
        description='Restart service with sudo.'
    )

def ssh_restart_service_using_sysctl_printer(output):
    if output is None:
        return
    print("\n")
    pprint.pprint(output)


def ssh_restart_service_using_sysctl(sshClient, hosts: List[str], service_name: str, sudo: bool = False) -> Dict:

    """ssh_restart_service_using_sysctl restart Service Using sysctl

        :type hosts: List[str]
        :param hosts: List of hosts to connect to. For eg. ["host1", "host2"].

        :type service_name: str
        :param service_name: Service name to restart.

        :type sudo: bool
        :param sudo: Restart service with sudo.

        :rtype: 
    """
    client = sshClient(hosts)
    runCommandOutput = client.run_command(command="systemctl restart %s" % service_name, sudo=sudo)
    client.join()
    res = {}

    for host_output in runCommandOutput:
        hostname = host_output.host
        output = [line for line in host_output.stdout]
        res[hostname] = output

    return res
