##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##

from typing import Optional, List
from github import GithubException
from pydantic import BaseModel, Field
import pprint

class InputSchema(BaseModel):
    organization_name: str = Field(
        description='Github Organization Name', 
        title='Organization Name'
    )
    team_name: str = Field(
        description='Team name in a GitHub Organization', 
        title='Team name'
    )


def github_get_team_printer(output):
    if not output:
        return
    pprint.pprint(output)

def github_get_team(handle, organization_name:str, team_name:str) -> List:
    """github_get_team returns details of the team

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type organization_name: string
        :param organization_name: Organization name Eg: "infosec"

        :type team_name: string
        :param team_name: Team name. Eg: "backend"

        :rtype: List of objects of a team and its id in an organization
    """
    result = []
    try:
        organization = handle.get_organization(organization_name)
        team = organization.get_team_by_slug(team_name)
        team_details = {}
        team_details["team_name"] = team.name
        team_details["team_id"] = team.id
        result.append(team_details)
    except GithubException as e:
        if e.status == 403:
            return [f"You need admin access"]
        if e.status == 404:
            return [f"No such organization or repository"]
        else:
            return [e.data]
    return result


