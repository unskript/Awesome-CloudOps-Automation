##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel, Field
from github import GithubException, BadCredentialsException, UnknownObjectException

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
    if output is None:
        return
    pprint.pprint(output)

def github_get_team(handle, organization_name:str, team_name:str) -> Dict:
    """github_get_team returns details of the team

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type organization_name: string
        :param organization_name: Organization name Eg: "infosec"

        :type team_name: string
        :param team_name: Team name. Eg: "backend"

        :rtype: List of a teams and its details
    """
    result = []
    try:
        organization = handle.get_organization(organization_name)
        team = organization.get_team_by_slug(team_name)
        team_details = {}
        team_details["team_name"] = team.name
        team_details["team_id"] = team.id
        team_details["members_count"]= team.members_count
        team_details["repos_count"]= team.repos_count
        team_details["privacy"]= team.privacy
        team_details["permission"]= team.permission
    except GithubException as e:
        if e.status == 403:
            raise BadCredentialsException("You need admin access") from e
        if e.status == 404:
            raise UnknownObjectException("No such organization or repository found") from e
        raise e.data
    except Exception as e:
        raise e
    return result
