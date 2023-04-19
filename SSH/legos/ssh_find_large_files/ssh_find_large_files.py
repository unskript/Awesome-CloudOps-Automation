##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

from pydantic import BaseModel, Field
from typing import Optional
import pprint


class InputSchema(BaseModel):
    host: str = Field(
        title='Host',
        description='Host to connect to. Eg 10.10.10.10'
    )
    proxy_host: Optional[str] = Field(
        title='Proxy host',
        description='Override the proxy host provided in the credentials. It still uses the proxy_user and port from the credentials.'
    )
    inspect_folder: str = Field(
        title='Inspect Folder',
        description='''Folder to inspect on the remote host. Folders are scanned using "find inspect_folder -type f -exec du -sk '{}' + | sort -rh | head -n count"'''
    )
    threshold: Optional[int] = Field(
        default=100,
        title="Size Threshold",
        description="Threshold the files on given size. Specified in Mb. Default is 100Mb"
    )
    count: Optional[int] = Field(
        default=10,
        title="Count",
        description="Number of files to report from the scan. Default is 10"
    )
    sudo: Optional[bool] = Field(
        default=False,
        title='Run with sudo',
        description='Run the scan with sudo.'
    )

def ssh_find_large_files_printer(output):
    if output is None:
        return
    print("\n")
    pprint.pprint(output)


def ssh_find_large_files(
    sshClient,
    host: str,
    inspect_folder: str,
    proxy_host: str = None,
    threshold: int = 0,
    sudo: bool = False,
    count: int = 10) -> dict:

    """ssh_find_large_files scans the file system on a given host

        :type host: str
        :param host: Host to connect to. Eg 10.10.10.10.

        :type inspect_folder: str
        :param inspect_folder: Folder to inspect on the remote host.

        :type proxy_host: str
        :param proxy_host: Proxy Host to connect host via. Eg 10.10.10.10.

        :type sudo: bool
        :param sudo: Run the scan with sudo.

        :type threshold: bool
        :param threshold: Threshold the files on given size. Specified in Mb. Default is 100Mb.

        :type count: bool
        :param count: Number of files to report from the scan. Default is 10.

        :rtype:
    """

    client = sshClient([host], proxy_host)

    # find size in Kb
    command = "find " + inspect_folder + \
        " -type f -exec du -sm '{}' + | sort -rh | head -n " + str(count)
    runCommandOutput = client.run_command(command=command, sudo=sudo)
    client.join()
    res = {}

    for host_output in runCommandOutput:
        for line in host_output.stdout:
            # line is of the form {size} {fullfilename}
            (size, filename) = line.split()
            if int(size) > threshold:
                res[filename] = int(size)

    return res
