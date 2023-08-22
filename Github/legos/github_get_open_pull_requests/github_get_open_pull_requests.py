##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from github import GithubException, BadCredentialsException, UnknownObjectException
from tabulate import tabulate

class InputSchema(BaseModel):
    owner: Optional[str] = Field(
        description='Username of the GitHub user. Eg: "johnwick"',
        title='Owner'
    )
    repository: str = Field(
        description='Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"',
        title='Repository',
    )


def github_get_open_pull_requests_printer(output_tuple):
    if output_tuple is None or output_tuple[1] is None:
        return
    success, output = output_tuple
    if not success:
        headers = ["PR Number", "Title", "Changed Files", "Review Comments", "Commits"]
        table = [[pr["pull_number"], pr["pull_title"], pr["pull_changed_files"],
                  pr["pull_review_comments"], pr["pull_commits"]] for pr in output]
        print(tabulate(table, headers, tablefmt="grid"))
    else:
        print("No unmerged pull requests found.")


def github_get_open_pull_requests(handle, repository: str, owner: str = "") -> Tuple:
    """github_get_open_pull_requests returns status, list of open pull requests.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type owner: string (Optional)
        :param owner: Username of the GitHub user. Eg: "johnwick"

        :type repository: string
        :param repository: Name of the GitHub repository. Eg: "Awesome-CloudOps-Automation"

        :rtype: Status, List of details of pull requests if it is not merged
    """
    result = []
    try:
        if not owner:
            owner = handle.get_user().login
        repo = handle.get_repo(f"{owner}/{repository}")
        prs = repo.get_pulls()

        # Check if there are no open pull requests
        if prs.get_page(0) == []:
            print("No pull requests are open at the moment.")
            return (True, None)

        for pr in prs:
            if not pr.is_merged():
                prs_dict = {
                    "pull_number": pr.number,
                    "pull_title": pr.title,
                    "pull_changed_files": pr.changed_files,
                    "pull_review_comments": pr.review_comments,
                    "pull_commits": pr.commits
                }
                result.append(prs_dict)
    except Exception as e:
        raise e

    return (False, result) if result else (True, None)