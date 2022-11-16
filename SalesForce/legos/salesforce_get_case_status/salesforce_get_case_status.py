import json

from pydantic import BaseModel, Field
import pprint
from typing import Dict

pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    case_number: str = Field(
        title='Case Number',
        description='The Case number to get the details about the case')

def salesforce_get_case_status_printer(output):
    if output is None:
        return
    print("\n")
    print(output)

def salesforce_get_case_status(handle, case_number: str) -> str:
    """salesforce_get_case_status gets the status about a particular case.
           :type case_number: str
           :param case_number: The Case number to get the details about the case
       """
    records = handle.query("SELECT Id FROM Case WHERE CaseNumber = '%s'" % case_number)
    if not records['records']:
        return "Invalid Case Number"
    else:
        case = handle.Case.get(records['records'][0]['Id'])
        return case.get("Status")
