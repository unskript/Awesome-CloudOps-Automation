
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
        ..., description='Github Organization Name', title='Organization Name'
    )
    team_name: str = Field(
        ..., description='Team name in a GitHub Organization', title='Team name'
    )

def github_list_team_members_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def github_list_team_members(handle, organization_name:str, team_name:str) -> List:
    """github_list_team_members returns details of the team members for a given team

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type organization_name: string
        :param organization_name: Organization name Eg: "infosec"

        :type team_name: string
        :param team_name: Team name. Eg: "backend"

        :rtype: List of a teams members details
    """
    result = []
    try:
        organization = handle.get_organization(organization_name)
        team = organization.get_team_by_slug(team_name)
        members = team.get_members()
        for member in members:
            member_details = {}
            member_details["name"] = member.login
            member_details["id"] = member.id
            result.append(member_details)
    except GithubException as e:
        if e.status == 403:
            raise Exception("You need admin access")
        if e.status == 404:
            raise Exception("No such organization or team found")
        raise e.data
    except Exception as e:
        raise e
    return result


