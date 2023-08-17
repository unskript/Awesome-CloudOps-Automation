##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from unskript.legos.ssh.ssh_execute_remote_command.ssh_execute_remote_command import ssh_execute_remote_command


class InputSchema(BaseModel):
    hosts: list[str] = Field(
        ...,
        description='List of hosts to connect to. For eg. ["host1", "host2"].',
        title='Hosts',
    )
    threshold: Optional[float] = Field(
        default = 5, description='The disk size threshold in GB. Default- 5GB', title='Threshold(in GB)'
    )


def ssh_get_ec2_instances_with_low_available_disk_size_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def ssh_get_ec2_instances_with_low_available_disk_size(handle, hosts: list, threshold: float = 5) -> Tuple:
    """Checks the available root disk size and compares it with the threshold.

    :type handle: SSH Client object
    :param handle: The SSH client.

    :type hosts: list
    :param hosts: List of hosts to connect to.

    :type threshold: float
    :param threshold: The disk size threshold in GB.

    :rtype: Status, list of dicts of hosts with available disk size less than the threshold
    """
     # Command to determine the root disk
    determine_disk_command = "lsblk -o NAME,MOUNTPOINT | grep ' /$' | awk '{print $1}' | tr -d '└─-'"
    disks = ssh_execute_remote_command(handle, hosts, determine_disk_command)

    # Check if all disks are the same for all hosts
    unique_disks = set(disks.values())
    if len(unique_disks) > 1:
        disk_details = ', '.join([f"{host}: {disk}" for host, disk in disks.items()])
        raise ValueError(f"The provided hosts have different disk names. Details: {disk_details}. Please execute them one by one.")
    disk = unique_disks.pop()


    # Create the command using the determined common disk
    command = f"df -h /dev/{disk.strip()} | tail -1"
    print(f"Executing command: {command}")
    outputs = ssh_execute_remote_command(handle, hosts, command)

    result = []
    for host, host_output in outputs.items():
        try:
            # Extracting available space from the output
            parts = host_output.split()
            if len(parts) > 4:
                available = parts[3]  # Assuming 'Available' column is the 4th one
                available_size = float(available[:-1])  # excluding the 'G'

                if available_size < threshold:
                    result.append({host: available_size})
            else:
                print(f'For host {host}, the output is not in expected format.')
                pass
        except Exception as e:
            raise e

    if result:
        return (False, result)
    return (True, None)
