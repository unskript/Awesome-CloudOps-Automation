##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##  @author: Yugal Pachpande, @email: yugal.pachpande@unskript.com
##
import pprint
from pydantic import BaseModel, Field
from botocore.exceptions import ClientError


class InputSchema(BaseModel):
    SecretId: str = Field(
        title='Secret Name',
        description='Name of the secret.')
    region: str = Field(
        title='Region',
        description='AWS Region.')


def aws_get_secret_from_secretmanager_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def aws_get_secret_from_secretmanager(handle, SecretId: str, region: str) -> str:
    """aws_get_secrets_from_secretsmanager returns The decrypted secret value

     :type handle: object
     :param handle: Object returned from task.validate(...).

     :type SecretId: string
     :param SecretId: Name of the secret.

     :type region: string
     :param region: AWS Region.

     :rtype: The decrypted secret value
    """

    secretsmanager_client = handle.client(service_name='secretsmanager', region_name=region)

    try:
        response = secretsmanager_client.get_secret_value(SecretId=SecretId)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + SecretId + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
        elif e.response['Error']['Code'] == 'DecryptionFailure':
            print("The requested secret can't be decrypted using the provided KMS key:", e)
        elif e.response['Error']['Code'] == 'InternalServiceError':
            print("An error occurred on service side:", e)
    else:
        # Secrets Manager decrypts the secret value using the associated KMS CMK
        # Depending on whether the secret was a string or binary, only one of
        # these fields will be populated
        if 'SecretString' in response:
            text_secret_data = response['SecretString']
            pprint.pprint(text_secret_data)
            return text_secret_data

        binary_secret_data = response['SecretBinary']
        pprint.pprint(binary_secret_data)
        return binary_secret_data
