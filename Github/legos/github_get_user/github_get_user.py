##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##

from typing import Optional, List
from pydantic import BaseModel, Field
from github import GithubException
import pprint


class InputSchema(BaseModel):
    owner: str = Field(
        description='Username of the GitHub user. Eg: "johnwick"', 
        title='Owner'
    )


def github_get_user_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def github_get_user(handle, owner:str) -> List:
    """github_get_user returns details of a user

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :rtype: List of details of a user
    """
    result = []
    try:
        user_details = {}
        user = handle.get_user(login=owner)
        user_details["name"] = user.login
        user_details["company"] = user.company
        user_details["email"] = user.email
        user_details["bio"] = user.bio
        user_details["followers"] = user.followers
        user_details["following"] = user.following
        result.append(user_details)
    except GithubException as e:
        if e.status == 404:
            raise Exception("User not found")
        raise e.data
    except Exception as e:
        raise e
    return result

