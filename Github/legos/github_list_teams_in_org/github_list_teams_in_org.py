##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from github import GithubException
from typing import Optional, List
from pydantic import BaseModel, Field
import pprint

class InputSchema(BaseModel):
    organization_name: str = Field(
        description='Name of the GitHub Organization. Eg: "wheelorg"',
        title='Organization Name',
    )



def github_list_teams_in_org_printer(output):
    if not output:
        return
    pprint.pprint(output)

def github_list_teams_in_org(handle, organization_name:str) -> List:
    """github_list_teams_in_org returns 100 open github branches for a user.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type organization_name: string
        :param organization_name: Name of the GitHub Organization. Eg: "wheelorg"

        :rtype: List of teams in a github org
    """
    result = []
    organization = handle.get_organization(organization_name)
    teams = organization.get_teams()
    try:
        [result.append(team.name) for team in teams]
    except GithubException as e:
        if e.status == 403:
            return [f"You need admin access"]
    return result

