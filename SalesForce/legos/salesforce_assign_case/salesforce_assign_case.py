##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from pydantic import BaseModel, Field

pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    case_number: str = Field(
        title='Case Number',
        description='The Case number to get the details about the case')
    owner_id: str = Field(
        title='Owner ID',
        description='Owner ID to assign the case"')


def salesforce_assign_case_printer(output):
    if output is None:
        return
    print(output)


def salesforce_assign_case(handle, case_number: str, owner_id: str) -> str:
    """salesforce_assign_case assigns a given case to a user

        :type case_number: str
        :param case_number: The Case number to get the details about the case

        :type owner_id: str
        :param owner_id: User to assign the case to. Eg user@acme.com
        
        :rtype: str
    """
    record_id = handle.query(f"SELECT Id FROM Case WHERE CaseNumber = '{case_number}'")
    if not record_id['records']:
        return "Invalid Case Number"
    record_id = record_id['records'][0]['Id']
    data = {
        "OwnerId": owner_id
    }
    resp = handle.Case.update(record_id, data)
    if resp == 204:
        return f"Case {case_number} assigned successfully"
    return "Error Occurred"
