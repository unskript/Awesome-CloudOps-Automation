##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from pydantic import BaseModel

class InputSchema(BaseModel):
    pass

def aws_get_acount_number_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_get_acount_number(handle) -> str:
    # Create a client object for the AWS Identity and Access Management (IAM) service
    iam_client = handle.client('iam')

    # Call the get_user() method to get information about the current user
    response = iam_client.get_user()

    # Extract the account ID from the ARN (Amazon Resource Name) of the user
    account_id = response['User']['Arn'].split(':')[4]

    # Print the account ID
    return account_id
