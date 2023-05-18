##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    hosts: List[str] = Field(
        title='Hosts',
        description='List of hosts to connect to. For eg. ["host1", "host2"].'
    )
    proxy_host: Optional[str] = Field(
        title='Proxy host',
        description='Override the proxy host provided in the credentials. \
            It still uses the proxy_user and port from the credentials.'
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


def ssh_restart_service_using_sysctl(
        sshClient,
        hosts: List[str],
        service_name: str,
        sudo: bool = False,
        proxy_host: str = None
        ) -> Dict:

    """ssh_restart_service_using_sysctl restart Service Using sysctl

        :type hosts: List[str]
        :param hosts: List of hosts to connect to. For eg. ["host1", "host2"].

        :type service_name: str
        :param service_name: Service name to restart.

        :type sudo: bool
        :param sudo: Restart service with sudo.

        :type proxy_host: str
        :param proxy_host: Optional proxy host to use.

        :rtype:
    """
    client = sshClient(hosts, proxy_host)
    runCommandOutput = client.run_command(command=f"systemctl restart {service_name}", sudo=sudo)
    client.join()
    res = {}

    for host_output in runCommandOutput:
        hostname = host_output.host
        output = [line for line in host_output.stdout]
        res[hostname] = output

    return res
