##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field
from typing import List
import pprint
from beartype import beartype


class InputSchema(BaseModel):
    region: str = Field(
        description='AWS Region.', 
        title='Region'
        )
    secret_name: str = Field(
         description='AWS Secret Name', 
         title='secret_name'
        )


@beartype
def aws_get_secrets_manager_secretARN_printer(output):
    if output is None:
        return
    pprint.pprint({"secret": output})


@beartype
def aws_get_secrets_manager_secretARN(handle, region: str, secret_name:str) -> str:
    # Create a Secrets Manager client
    client = handle.client(
        service_name='secretsmanager',
        region_name=region
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e
    # Decrypts secret using the associated KMS key.
    secretArn = get_secret_value_response['ARN']
    return secretArn


