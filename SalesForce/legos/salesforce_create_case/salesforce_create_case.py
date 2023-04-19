import json
from typing import Dict, Optional
from pydantic import BaseModel, Field
from tabulate import tabulate

from unskript.enums.salesforce_enums import Status, CaseOrigin, CaseType, Priority, CaseReason, \
    PotentialLiability, SLAViolation
import pprint

pp = pprint.PrettyPrinter(indent=4)


class AdditionalInformation(BaseModel):
    product: Optional[str] = Field(
        title='Product',
        description='Product associated with case')
    engineering_req_number: Optional[str] = Field(
        title='Engineering Req Number',
        description='Engineering Req Number')
    potential_liability: Optional[PotentialLiability] = Field(
        title='Potential Liability',
        description='Potential Liability')
    sla_violation: Optional[SLAViolation] = Field(
        title='SLA Violation',
        description='SLA Violation')


class WebInformation(BaseModel):
    web_email: Optional[str] = Field(
        title='Web Email',
        description='Web Email')
    web_company: Optional[str] = Field(
        title='Web Company',
        description='Web Company')
    web_name: Optional[str] = Field(
        title='Web Name',
        description='Web Name')
    web_phone: Optional[str] = Field(
        title='Web Phone',
        description='Web Phone')


class InputSchema(BaseModel):
    status: Status = Field(
        title='Status',
        description='The status of the case. Default is "New"')
    priority: Optional[Priority] = Field(
        title='Priority',
        description='The priority of the case')
    case_origin: CaseOrigin = Field(
        title='Case Origin',
        description='The origin of the case')
    contact_name: Optional[str] = Field(
        title='Contact Name',
        description='The name of the contact')
    account_name: Optional[str] = Field(
        title='Account Name',
        description='The name of the Account')
    type: Optional[CaseType] = Field(
        title='Type',
        description='The type of the case')
    case_reason: Optional[CaseReason] = Field(
        title='Case Reason ',
        description='The Reason for the case')
    subject: Optional[str] = Field(
        title='Subject',
        description='Title of the case')
    description: Optional[str] = Field(
        title='Description',
        description='A short description about the case')
    internal_comments: Optional[str] = Field(
        title='Internal Comments',
        description='Comments about thw case')
    additional_information: Optional[AdditionalInformation] = Field(...)
    web_information: Optional[WebInformation] = Field(None, alias='Web Information')


def salesforce_create_case_printer(output):
    if output is None:
        return
    print("\n")
    print(json.dumps(output, indent=4))
    case_number = output.get("CaseNumber")
    data = []
    data.append(case_number)
    print("\n")
    od = tabulate([data], headers=['CaseNumber'], tablefmt="grid")
    print(od)

def salesforce_create_case(handle,
                           status: Status,
                           case_origin: CaseOrigin,
                           priority: Priority = Priority.LOW,
                           contact_name: str = "",
                           account_name: str = "",
                           type: CaseType = CaseType.ELECTRONIC,
                           case_reason: CaseReason = CaseReason.OTHER,
                           subject: str = "",
                           description: str = "",
                           internal_comments: str = "",
                           additional_information: dict = None,
                           web_information: dict = None,
                           ) -> Dict:
    """salesforce_create_case create salesforce case

        :type status: Status
        :param status: The status of the case. Default is "New"

        :type case_origin: CaseOrigin
        :param case_origin: The origin of the case.

        :type priority: Priority
        :param priority: The priority of the case.

        :type contact_name: str
        :param contact_name: The name of the contact.

        :type account_name: str
        :param account_name: The name of the Account.

        :type type: CaseType
        :param type: The type of the case.

        :type case_reason: CaseReason
        :param case_reason: The Reason for the case.

        :type subject: str
        :param subject: Title of the case.
        
        :type description: str
        :param description: A short description about the case.

        :type internal_comments: str
        :param internal_comments: Comments about thw case.

        :rtype: 
    """

    """salesforce_create_case creates a case in Salesforce. """

    contact_id = ""
    account_id = ""
    status = status.value if status else None
    case_origin = case_origin.value if case_origin else None
    type = type.value if type else None
    priority = priority.value if priority else None
    case_reason = case_reason.value if case_reason else None

    if contact_name != "":
        contact_id = handle.query("SELECT Id FROM Contact WHERE Name = '%s'" % contact_name)
        if contact_id['records'] == []:
            return {"Error": "Invalid Contact name"}
        else:
            contact_id = contact_id['records'][0]['Id']
    if account_name != "":
        account_id = handle.query("SELECT Id FROM Account WHERE Name = '%s'" % account_name)
        if account_id['records'] == []:
            return {"Error": "Invalid Account name"}
        else:
            account_id = account_id['records'][0]['Id']

    data = {}
    data['Status'] = status
    data['Priority'] = priority
    data['Origin'] = case_origin
    data['ContactId'] = contact_id
    data['AccountId'] = account_id
    data['Type'] = type
    data['Reason'] = case_reason
    if web_information:
        data['SuppliedEmail'] = web_information.get("web_email", None)
        data['SuppliedName'] = web_information.get("web_name", None)
        data['SuppliedCompany'] = web_information.get("web_company", None)
        data['SuppliedPhone'] = web_information.get("web_phone", None)
    if additional_information:
        if additional_information.get("product"):
            data["Product__c"] = additional_information.get("product")
        if additional_information.get("engineering_req_number"):
            data["EngineeringReqNumber__c"] = additional_information.get("engineering_req_number")
        if additional_information.get("potential_liability"):
            data["PotentialLiability__c"] = additional_information.get("potential_liability")
        if additional_information.get("sla_violation"):
            data["SLAViolation__c"] = additional_information.get("sla_violation")
    data['Subject'] = subject
    data['Description'] = description
    data['Comments'] = internal_comments
    case = handle.Case.create(data)
    if case.get("success"):
        return handle.Case.get(case.get("id"))
    else:
        return case.get("errors")
