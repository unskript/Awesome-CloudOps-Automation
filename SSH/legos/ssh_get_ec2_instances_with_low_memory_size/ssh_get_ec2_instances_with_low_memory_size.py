##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import List, Optional, Tuple
from pydantic import BaseModel, Field
from unskript.legos.ssh.ssh_execute_remote_command.ssh_execute_remote_command import ssh_execute_remote_command


class InputSchema(BaseModel):
    hosts: list = Field(
        ...,
        description='List of hosts to connect to. For eg. ["host1", "host2"].',
        title='Hosts',
    )
    threshold: Optional[float] = Field(
        default= 400,
        description='Optional memory size threshold in MB. Default- 400 MB',
        title='Threshold(in MB)',
    )


def ssh_get_ec2_instances_with_low_memory_size_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def ssh_get_ec2_instances_with_low_memory_size(handle, hosts: list, threshold: float = 400) -> Tuple:
    """Get EC2 instances with free memory size less than a given threshold.

    :type handle: SSH Client object
    :param handle: The SSH client.

    :type hosts: list
    :param hosts: List of hosts to connect to.

    :type threshold: float
    :param threshold: Optional memory size threshold in MB.

    :rtype: Status, list of dicts of hosts with available disk size less than the threshold along with the size in MB
    """
    command = "free -m| awk 'NR==2{printf \"%.2f\", $7}'"
    output = ssh_execute_remote_command(handle, hosts, command)
    result = []
    hosts_with_less_memory = {}
    for host, host_output in output.items():
        try:
            available_memory = float(host_output)

            # Compare the available memory size with the threshold
            if available_memory < threshold:
                hosts_with_less_memory[host] = available_memory
                result.append(hosts_with_less_memory)
        except Exception as e:
            raise e

    if len(result) != 0:
        return (False, result)
    return (True, None)


