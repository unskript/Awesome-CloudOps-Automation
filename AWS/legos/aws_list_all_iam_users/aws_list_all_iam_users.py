##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel

class InputSchema(BaseModel):
    pass

def aws_list_all_iam_users_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_list_all_iam_users(handle) -> List:
    """aws_list_all_iam_users lists all the IAM users

        :type handle: object
        :param handle: Object returned from Task Validate
        
        :rtype: Result List of all IAM users
    """
    client = handle.client('iam') 
    users_list=[]
    response = client.list_users()
    try:
        for x in response['Users']:
            users_list.append(x['UserName'])
    except Exception as e:
        users_list.append(e)
    return users_list
