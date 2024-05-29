import pprint
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from unskript.enums.github_team_privacy_enums import GithubTeamPrivacy
from github import GithubException

class InputSchema(BaseModel):
    team_name: str = Field(
     description='Team name. Eg:"backend"',
     title='Team Name'
    )
    description: Optional[str] = Field(
        '', 
        description='Description of the new team.',
        title='Description'
    )
    privacy: Optional[GithubTeamPrivacy] = Field(
        description=('Privacy type to be given to the team. "secret" - only visible to '
                     'organization owners and members of this team, "closed"- visible to '
                     'all members of this organization. By default type "secret" will be '
                     'considered. '), 
        title='Privacy'
    )
    organization_name: str = Field(
       description='Github Organization Name. Eg: "infosecorg"',
       title='Organization Name'
    )
    repositories: List = Field(
        description='List of the GitHub repositories to add to the new team. Eg: ["repo1","repo2"]',
        title='repositories',
    )



def github_create_team_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def github_create_team(
        handle,
        organization_name:str,
        team_name:str,
        repositories:list,
        privacy:GithubTeamPrivacy=GithubTeamPrivacy.secret,
        description:str=""
        ) -> Dict:
    """github_create_team returns details of newly created team.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type organization_name: string
        :param organization_name: Organization name Eg: "infosec"

        :type team_name: string
        :param team_name: Team name. Eg: "backend"

        :type description: string
        :param description: Description of the new team.

        :type repositories: string
        :param repositories: List of the GitHub repositories to add to the new team. 
        Eg: ["repo1","repo2"]

        :type privacy: Enum
        :param privacy: Privacy type to be given to the team. "secret" - only visible 
        to organization owners and members of this team, "closed"- visible to all members 
        of this organization. By default type "secret" will be considered. 

        :rtype: Dict of details of newly created team
    """
    result = []
    team_details = {}
    repo_names =[]
    list_of_repos = ''
    privacy_settings = ''
    if privacy is None or len(privacy)==0:
        privacy_settings = "secret"
    organization = handle.get_organization(organization_name)
    for repo in repositories:
        list_of_repos  = organization.get_repo(repo)
        repo_names.append(list_of_repos)
    try:
        result = organization.create_team(
            name=team_name,
            repo_names=repo_names,
            privacy=privacy_settings,
            description=description
            )
        team_details["name"]= result.name
        team_details["id"]= result.id
    except GithubException as e:
        if e.status == 404:
            raise Exception("No such organization found") from e
        raise e.data
    except Exception as e:
        raise e
    return team_details
