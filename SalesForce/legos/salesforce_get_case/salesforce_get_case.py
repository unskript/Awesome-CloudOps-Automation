import json
import pprint
from typing import Dict
from pydantic import BaseModel, Field

pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    case_number: str = Field(
        title='Case Number',
        description='The Case number to get the details about the case')

def salesforce_get_case_printer(output):
    if output is None:
        return
    print("\n")
    print(json.dumps(output, indent=4))

def salesforce_get_case(handle, case_number: str) -> Dict:
    """salesforce_get_case gets the details about a particular case.
           :type case_number: str
           :param case_number: The Case number to get the details about the case
       """
    record_id = handle.query(f"SELECT Id FROM Case WHERE CaseNumber = '{case_number}'")
    if not record_id['records']:
        return {"Error": "Invalid Case Number"}
    return handle.Case.get(record_id['records'][0]['Id'])
