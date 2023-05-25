##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

import pprint
from typing import Dict, Optional
from pydantic import BaseModel, Field
from jira.client import JIRA


class InputSchema(BaseModel):
    issue_id: str = Field(
        title='JIRA Issue ID',
        description='Issue ID. Eg EN-1234'
    )
    comment: str = Field(
        title='Comment',
        description='Comment to add in Jira Issue'
    )
    visibility: Optional[Dict[str, str]] = Field(
        None,
        title='Visibility',
        description='''a dict containing two entries: "type" and "value".
              "type" is 'role' (or 'group' if the Jira server has configured comment visibility for groups)
              "value" is the name of the role (or group) to which viewing of this comment 
              will be restricted.'''
    )
    is_internal: Optional[bool] = Field(
        False,
        title='Internal',
        description=('True marks the comment as \'Internal\' in Jira Service Desk '
                     '(Default: ``False``)')
    )


def jira_add_comment_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def jira_add_comment(hdl: JIRA,
                     issue_id: str,
                     comment: str,
                     visibility: Dict[str, str] = None,
                     is_internal: bool = False) -> int:
    """jira_get_issue Get Jira Issue Info

        :type hdl: JIRA
        :param hdl: Jira handle.

        :type issue_id: str
        :param issue_id: Issue ID.

        :type comment: str
        :param comment: Comment to add in Jira Issue.

        :type visibility: Dict[str, str]
        :param visibility: a dict containing two entries: "type" and "value".
              "type" is 'role' (or 'group' if the Jira server has configured 
              comment visibility for groups)
              "value" is the name of the role (or group) to which viewing of 
              this comment will be restricted.

        :type is_internal: bool
        :param is_internal: True marks the comment as \'Internal\' in Jira 
        Service Desk (Default: ``False``)

        :rtype: Jira comment id (int)
    """
    try:
        issue = hdl.issue(issue_id)
        comment = hdl.add_comment(issue, comment, visibility=visibility, is_internal=is_internal)
    except Exception as e:
        raise e
    return int(comment.id)
