#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#
from pydantic import BaseModel, Field
from typing_extensions import Annotated

import requests

from typing import List, Optional
import json


class InputSchema(BaseModel):
    repo: str = Field(
        title='Git Repository',
        description='Repository that has Terraform Scripts eg: https://github.com/acme/acme.git'
    )
    branch: str = Field(
        title='Git Repository Branch',
        description='Branch name of repository that has Terraform Scripts eg: master, dev, feature/multiuser'
    )
    dir_path: Optional[str] = Field(
        title='Directory Path',
        description='Directory within Repository to run the terraform command eg: acme, ./, acme/terrform/main'
    )
    command: str = Field(
        title='Terraform Command',
        description='Terraform Command to Execute eg: terraform init, terraform apply -var="instance_type=t3.micro"'
    )


def terraform_exec_command(handle, repo, branch, command, dir_path:str=None) -> str:
    """terraform_exec_command Executes the terraform command
       with any arguments.

       :type handle: object
        :param handle: Object returned from task.validate(...).

        :type repo: str
        :param repo: Repository that has Terraform Scripts.

        :type dir_path: str
        :param dir_path: Directory within Repository to run the terraform command.

        :type command: str
        :param command: Terraform Command to Execute.

        :rtype: Str Output of the command .
    """
    assert(command.startswith("terraform"))
    print(f'WARNING: Please note terraform apply and terraform destroy will be run with -auto-approve for non-interactive run')

    # Reason we are doing this instead of setting the default value in InputSchema is "" dont get inserted for the default value.
    # causing an issue when we drag and drop in jupyter.
    if dir_path is None:
        dir_path = "./"

    output = ''
    # sanitize inputs that have come from validate

    try:
        result = handle.sidecar_command(repo, branch, handle.credential_id, dir_path, command, str(""))
        output = result.data.decode('utf-8')
        output = json.loads(output)['output']
    except Exception as e:
        output = f"Execution was not successful %s " % e

    return output
