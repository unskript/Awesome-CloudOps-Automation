
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
        description='Name of the GitHub Organization. Eg: "wheelorg"',
        title='Organization Name',
    )
    team_name: str = Field(
        description='Team name. Eg: "backend"',
        title='Team Name'
    )



def github_list_team_repos_printer(output):
    if output is None:
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
        result = [repo.full_name for repo in repos]
    except GithubException as e:
        if e.status == 403:
            raise Exception("You need admin access") from e
        if e.status == 404:
            raise Exception("No such organization or repository found") from e
        raise e.data
    except Exception as e:
        raise e
    return result
