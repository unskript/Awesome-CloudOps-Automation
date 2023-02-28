
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
        description='Name of the GitHub Organization. Eg: "wheelorg"',
        title='Organization Name',
    )
    team_name: str = Field(
        description='Team name. Eg: "backend"', 
        title='Team Name'
    )



def github_list_team_repos_printer(output):
    if not output:
        return
    pprint.pprint(output)

def github_list_team_repos(handle, organization_name:str, team_name:str) -> List:
    """github_list_team_repos returns list of repositories in a team

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type organization_name: string
        :param organization_name: Organization name Eg: "infosec"

        :type team_name: string
        :param team_name: Team name. Eg: "backend"

        :rtype: List of repositories in a team
    """
    result = []
    try:
        organization = handle.get_organization(organization_name)
        team = organization.get_team_by_slug(team_name)
        repos = team.get_repos()
        [result.append(repo.full_name) for repo in repos]
    except GithubException as e:
        if e.status == 403:
            return [f"You need admin access"]
        if e.status == 404:
            return [f"No such organization or repository"]
        else:
            return [f"e.data"]
    return result


