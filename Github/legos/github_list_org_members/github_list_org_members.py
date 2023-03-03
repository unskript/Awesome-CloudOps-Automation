
##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##

from typing import Optional, List
from pydantic import BaseModel, Field
from github import GithubException
import pprint


class InputSchema(BaseModel):
    organization_name: str = Field(
        description='Name of Github Organization. Eg: "unskript"',
        title='Organization Name',
    )


def github_list_org_members_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def github_list_org_members(handle, organization_name:str)-> List:
    result = []
    try:
        organization = handle.get_organization(organization_name)
        members = organization.get_members()
        [result.append(member.login) for member in members]
    except GithubException as e:
        if e.status == 403:
            raise Exception("You need admin access")
        if e.status == 404:
            raise Exception("No such organization or user found")
        raise e.data
    except Exception as e:
        raise e
    return result


