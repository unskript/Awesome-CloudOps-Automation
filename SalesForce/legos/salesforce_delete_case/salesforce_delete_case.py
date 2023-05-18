import pprint
from pydantic import BaseModel, Field

pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    case_number: str = Field(
        title='Case Number',
        description='The Case number of the case to delete')

def salesforce_delete_case_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def salesforce_delete_case(handle, case_number: str) -> str:
    """salesforce_delete_case deletes a particular case.
           :type case_number: str
           :param case_number: The Case number of the case to delete
       """
    record_id = handle.query(f"SELECT Id FROM Case WHERE CaseNumber = '{case_number}'")
    if not record_id['records']:
        return "Invalid Case Number"
    resp = handle.Case.delete(record_id['records'][0]['Id'])
    if resp == 204:
        return f"Case {case_number} deleted successfully"
    return "Error Occurred"
