##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##

import pprint
from pydantic import BaseModel, Field
from github import GithubException, BadCredentialsException, UnknownObjectException


class InputSchema(BaseModel):
    organization_name: str = Field(
        description='Name of Github Organization. Eg: "unskript"',
        title='Organization Name',
    )
    username: str = Field(
        description='Organization member\'s username. Eg: "jane-mitch-unskript"',
        title='Member\'s Username',
    )


def github_remove_member_from_org_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def github_remove_member_from_org(handle, organization_name:str, username:str)-> str:
    """github_remove_member_from_org returns the status to remove a member

        :type organization_name: string
        :param organization_name: Name of Github Organization. Eg: "unskript"

        :type username: string
        :param username: Organization member's username. Eg: "jane-mitch-unskript"

        :rtype: List of return status of removing a member from Org
    """
    organization = handle.get_organization(organization_name)
    try:
        user = handle.get_user(username)
        mem_exist = organization.has_in_members(user)
        if mem_exist:
            result = organization.remove_from_members(user)
    except GithubException as e:
        if e.status == 403:
            raise BadCredentialsException("You need admin access") from e
        if e.status == 404:
            raise UnknownObjectException("No organization or user found") from e
        raise e.data
    except Exception as e:
        raise e
    if result is None:
        return f"Successfully removed user {username}"
    return None
