
##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Optional, List
from pydantic import BaseModel, Field
from github import GithubException
from unskript.enums.github_user_role_enums.py import GithubUserRole
import pprint


class InputSchema(BaseModel):
    email: str = Field(
        description='Email address of the user to invite to the Github Organization. Eg: user@gmail.com',
        title='Email',
    )
    organization_name: str = Field(
        description='Github Organization Name', 
        title='Organization Name'
    )
    role: Optional[GithubUserRole] = Field(
        '',
        description='Role to assign to the new user. By default, direct_member role will be assigned. Eg:"admin" or "direct_member" or "billing_manager". ',
        title='Role',
    )
    list_of_teams: List = Field(
        description='List of teams to add the user to. Eg:["frontend-dev","backend-dev"]',
        title='List of Teams',
    )


def github_invite_user_to_org_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def github_invite_user_to_org(handle, organization_name:str, email:str, list_of_teams:list, role:GithubUserRole=None)-> str:
    """github_invite_user_to_org returns status of the invite

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type organization_name: string
        :param organization_name: Organization name Eg: "infosec"

        :type list_of_teams: list
        :param list_of_teams: List of teams to add the user to. Eg:["frontend-dev","backend-dev"]

        :type email: str
        :param email: Email address of the user to invite to the Github Organization. Eg: user@gmail.com

        :type role: GithubUserRole (Enum)
        :param role: Role to assign to the new user. By default, direct_member role will be assigned. Eg:"admin" or "direct_member" or "billing_manager". 

        :rtype: String, Status message for a the invite
    """
    result = []
    teams_list = []
    organization = handle.get_organization(organization_name)
    if role is None:
        role = "direct_member"
    try:
        teams = organization.get_teams()
        for each_team in teams:
            if each_team.name in list_of_teams:
                teams_list.append(each_team)
        result = organization.invite_user(email=email, role=role, teams=teams_list)
        if result is None:
            return f"Successfully sent invite"
    except GithubException as e:
        if e.status == 403:
            raise Exception("You need admin access")
        if e.status == 404:
            raise Exception("No such organization found")
        raise e.data


