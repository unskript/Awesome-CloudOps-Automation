import json
import pprint
from typing import List
from pydantic import BaseModel, Field
from tabulate import tabulate

pp = pprint.PrettyPrinter(indent=4)


class InputSchema(BaseModel):
    case_number: str = Field(
        title='Case Number',
        description='The Case number to get the details about the case')


def salesforce_search_case_printer(output):
    if output is None:
        return
    print("\n")
    tb_data = []
    for record in output:
        print(json.dumps(record, indent=4))
        case_number = record.get("CaseNumber")
        data = [case_number]
        tb_data.append(data)
    print("\n")
    od = tabulate(tb_data, headers=['CaseNumber'], tablefmt="grid")
    print(od)


def salesforce_search_case(handle, search: str) -> List:
    """salesforce_search_case gets the details about a particular case.
           :type search: str
           :param search: Search based on Status/Priority/Subject/CaseNumber/Reason
       """
    search = "%" + search
    query = f"SELECT Id FROM Case WHERE Priority Like '{search}'" \
            f"Or Status Like '{search}' " \
            f"Or Subject Like '{search}' " \
            f"Or Reason Like '{search}' " \
            f"Or CaseNumber Like '{search}' " \

    records = handle.query(query)['records']
    if records:
        cases = []
        for record in records:
            cases.append(handle.Case.get(record['Id']))
        return cases
    return records
