##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    secret_name: str = Field(
        title='Secret Name',
        description='Name of the secret to be deleted.')
    region: str = Field(
        title='Region',
        description='AWS Region.')


def aws_delete_secret_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_delete_secret(handle, region: str, secret_name: str) -> Dict:
    """aws_delete_secret Dict with secret details.

        :type handle: object
        :param handle: Object returned from Task Validate

        :type secret_name: string
        :param secret_name: Name of the secret to be deleted.

        :type region: string
        :param region: AWS Region.

        :rtype: Dict with secret details.
    """
    try:
        secrets_client = handle.client('secretsmanager', region_name=region)
        response = secrets_client.delete_secret(SecretId=secret_name)
        return response
    except Exception as e:
        raise Exception(e) from e
    