
##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field
from github import GithubException


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
    """github_remove_member_from_org returns the status to remove a member

        :type organization_name: string
        :param organization_name: Name of Github Organization. Eg: "unskript"
        
        :rtype: List of return status of removing a member from Org
    """
    result = []
    try:
        organization = handle.get_organization(organization_name)
        members = organization.get_members()
        result = [member.login for member in members]
    except GithubException as e:
        if e.status == 403:
            raise Exception("You need admin access") from e
        if e.status == 404:
            raise Exception("No such organization or user found") from e
        raise e.data
    except Exception as e:
        raise e
    return result
