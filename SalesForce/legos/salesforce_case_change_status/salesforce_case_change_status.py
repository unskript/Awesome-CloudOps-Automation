##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from pydantic import BaseModel, Field
from unskript.enums.salesforce_enums import Status

pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    case_number: str = Field(
        title='Case Number',
        description='The Case number to get the details about the case')
    status: Status = Field(
        title='Status',
        description='The status of the case. Default is "New"')


def salesforce_case_change_status_printer(output):
    if output is None:
        return
    print(output)


def salesforce_case_change_status(handle, case_number: str, status: Status) -> str:
    """salesforce_case_change_status change status for given case
        :type case_number: str
        :param case_number: The Case number to get the details about the case

        :type status: Status
        :param status: Salesforce Case Status. Possible values: New|Working|Escalated
        
        :rtype: str
    """
    record_id = handle.query(f"SELECT Id FROM Case WHERE CaseNumber = '{case_number}'")
    if not record_id['records']:
        return "Invalid Case Number"
    status = status.value if status else None
    record_id = record_id['records'][0]['Id']
    data = {
    "Status": status
    }
    resp = handle.Case.update(record_id, data)
    if resp == 204:
        return f"Status change successfully for case {case_number} "
    return "Error Occurred"
