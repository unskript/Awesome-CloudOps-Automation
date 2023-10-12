##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from unskript.legos.ssh.ssh_execute_remote_command.ssh_execute_remote_command import ssh_execute_remote_command


class InputSchema(BaseModel):
    hosts: list = Field(
        ...,
        description='List of hosts to connect to. For eg. ["host1", "host2"].',
        title='Lis of Hosts',
    )
    threshold: Optional[float] = Field(
        10,
        description='Time threshold in seconds to flag a host for potential latency issues.',
        title='Threshold (in seconds)',
    )


def ssh_get_hosts_with_low_disk_latency_printer(output):
    if not output:
        print("No issues found.")
        return

    status, problematic_hosts = output
    if not status:
        print("Hosts with potential disk latency issues:", ', '.join(problematic_hosts))
    else:
        print("No latency issues found on any hosts.")

def ssh_get_hosts_with_low_disk_latency(handle, hosts: list, threshold: int = 5) -> Tuple:
    """
    ssh_get_hosts_with_low_disk_latency Checks the disk latency on the provided hosts by running a disk write command and 
    measuring the time taken. If the time taken exceeds a given threshold, the host is 
    flagged as having potential latency issues.

    :type handle: SSH Client object
    :param handle: The SSH client.

    :type hosts: list
    :param hosts: List of hosts to connect to.

    :type threshold: float
    :param threshold: Time threshold in seconds to flag a host for potential latency issues.

    :return: Status and the hosts with potential latency issues if any.
    """
    print("Starting the disk latency check...")

    latency_command = "/usr/bin/time -p dd if=/dev/zero of=~/test.png bs=8192 count=10240 oflag=direct 2>&1"
    outputs = ssh_execute_remote_command(handle, hosts, latency_command)

    # Cleanup: Remove the created test file
    print("Cleaning up resources...")
    cleanup_command = "rm ~/test.png"
    ssh_execute_remote_command(handle, hosts, cleanup_command)

    hosts_with_issues = []

    for host, output in outputs.items():
        if not output.strip():
            print(f"Command execution failed or returned empty output on host {host}.")
            continue

        for line in output.splitlines():
            if line.startswith("real"):
                time_line = line
                break
        else:
            print(f"Couldn't find 'real' time in output for host {host}.")
            continue

        # Parse the time and check against the threshold
        try:
            total_seconds = float(time_line.split()[1])

            if total_seconds > threshold:
                hosts_with_issues.append(host)
        except Exception as e:
            raise e

    if hosts_with_issues:
        return (False, hosts_with_issues)
    return (True, None)




