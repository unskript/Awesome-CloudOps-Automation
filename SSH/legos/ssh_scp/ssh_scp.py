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
        description='Hosts to connect to. For eg. "10.10.10.10"'
    )
    proxy_host: Optional[str] = Field(
        title='Proxy host',
        description='Override the proxy host provided in the credentials. It still uses the proxy_user and port from the credentials.'
    )
    remote_file: str = Field(
        title='Remote File',
        description='Filename on the remote server. Eg /home/ec2-user/my_remote_file'
    )
    local_file: str = Field(
        title="Local File",
        description='Filename on the unSkript proxy. Eg /tmp/my_local_file'
    )
    direction: bool = Field(
        default=True,
        title="Receive",
        description="Direction of the copy operation. Default is receive-from-remote-server"
    )

def ssh_scp_printer(output):
    if output is None:
        return
    print("\n")
    pprint.pprint(output)


def ssh_scp(
        sshClient,
        host: str,
        remote_file: str,
        local_file: str,
        proxy_host: str = None,
        direction: bool = True):
    """ssh_scp Copy files from or to remote host.

        :type host: str
        :param host: Host to connect to. Eg 10.10.10.10.

        :type remote_file: str
        :param remote_file: Filename on the remote server. Eg /home/ec2-user/my_remote_file

        :type local_file: str
        :param local_file: Filename on the unSkript proxy. Eg /tmp/my_local_file

        :type proxy_host: str
        :param proxy_host: Proxy Host to connect host via. Eg 10.10.10.10.

        :type direction: bool
        :param direction: Direction of the copy operation. Default is receive-from-remote-server

        :rtype:
    """
    client = sshClient([host], proxy_host)
    copy_args = [{'local_file': local_file, 'remote_file': remote_file}]
    cmds = client.copy_file(local_file, remote_file, direction)
    client.join()

