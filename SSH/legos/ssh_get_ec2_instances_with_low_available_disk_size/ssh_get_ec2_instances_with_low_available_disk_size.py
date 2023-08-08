##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import List, Optional
from pydantic import BaseModel, Field
from unskript.legos.ssh.ssh_execute_remote_command.ssh_execute_remote_command import ssh_execute_remote_command


class InputSchema(BaseModel):
    hosts: List[str] = Field(
        ...,
        description='List of hosts to connect to. For eg. ["host1", "host2"].',
        title='Hosts',
    )
    threshold: Optional[float] = Field(
        default = 5, description='The disk size threshold in GB. Default- 5GB', title='Threshold(in GB)'
    )
    command: Optional[str] = Field(
        default = "df -h /dev/xvda1", description='Command to get disk size. Default- df -h /dev/xvda1', title='Command to get disk size.'
    )


def ssh_get_ec2_instances_with_low_available_disk_size_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def ssh_get_ec2_instances_with_low_available_disk_size(handle, hosts: list, threshold: float = 5, command:str = "df -h /dev/xvda1")-> List:
    """Checks the available root disk size and compares it with the threshold.

    :type handle: SSH Client object
    :param handle: The SSH client.

    :type hosts: list
    :param hosts: List of hosts to connect to.

    :type threshold: float
    :param threshold: The disk size threshold in GB.

    :type command: str
    :param command: Command to get disk size. Default- df -h /dev/xvda1

    :rtype: Status, list of dicts of hosts with available disk size less than the threshold
    """
    output = ssh_execute_remote_command(handle, hosts, command)
    result = []
    hosts_with_less_space = {}
    for host, host_output in output.items():
        try:
            lines = host_output.split("\n")
            # Assuming 'Available' column is always the 4th one
            available = lines[2].split()[3]
            available_size = float(available[:-1])  # excluding the 'G'

            if available_size < threshold:
                hosts_with_less_space[host] = available_size
                result.append(hosts_with_less_space)
        except Exception as e:
            raise e
    if len(result) != 0:
        return (False, result)
    return (True, None)

