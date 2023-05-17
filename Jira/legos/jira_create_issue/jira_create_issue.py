##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import enum
import pprint
from typing import Optional
from pydantic import BaseModel, Field
from jira import JIRA

pp = pprint.PrettyPrinter(indent=4)

class CustomFieldTypes(enum.Enum):
    MULTICHECKBOXES = 'com.atlassian.jira.plugin.system.customfieldtypes:multicheckboxes'
    LABELS = 'com.atlassian.jira.plugin.system.customfieldtypes:labels'
    FLOAT = 'com.atlassian.jira.plugin.system.customfieldtypes:float'
    USERPICKER = 'com.atlassian.jira.plugin.system.customfieldtypes:userpicker'
    TEXTAREA = 'com.atlassian.jira.plugin.system.customfieldtypes:textarea'
    CASCADINGSELECT = 'com.atlassian.jira.plugin.system.customfieldtypes:cascadingselect'
    TEXTFIELD = 'com.atlassian.jira.plugin.system.customfieldtypes:textfield'
    MULTISELECT = 'com.atlassian.jira.plugin.system.customfieldtypes:multiselect'
    SELECT = 'com.atlassian.jira.plugin.system.customfieldtypes:select'
    URL = 'com.atlassian.jira.plugin.system.customfieldtypes:url'
    RADIOBUTTONS = 'com.atlassian.jira.plugin.system.customfieldtypes:radiobuttons'


class InputSchema(BaseModel):
    project_name: str = Field(
        title="Project Name",
        description="The name of the project for which the issue will be generated"
    )
    summary: str = Field(
        title="Summary",
        description="Summary of the issue"
    )
    description: Optional[str] = Field(
        title="Description",
        description="Description of the issue"
    )
    issue_type: str = Field(
        title="Issue Type",
        description="JIRA Issue Type."
    )
    fields: dict = Field(
        None,
        title='Extra fields',
        description='''
            User needs to pass the fields in the format of dict(KEY=VALUE) pair
            where key is the Field Name and value is actual value
            Value will be vary based on there field type like mention below
            fields can be passed as mentioned below:
                Quarter field can be passed as: {QuarterExample:["Q1", "Q2"]}
                Labels field can be passed as : {"Labelexample": ["cherry-picker"]}
                Numbers can be provided through numbers field Eg: {"NumberExample": 10}
                User picker (single user) can be passed as: {"UserPickerExample": "John Smith"}
                Paragraphs (multi-line) field can be passed as a string like so: {"ParagraphTest": "ABC ABC ABC ABC"}
                Select list (cascading) field can be passed as: {"SelectListCascadeExample": {"parent": "ABC", "child": "XYZ"}}
                Short text field can be passed as: {"ShortTextExample": "test"}
                Select list (multiple choice) field is passed as: {"SelectListMultipleChoicesSample": ["ABC", "XYZ"]}
                Select list (single choice) field is passed as: {"SelectListSingleTest": ["123"]}
                URL Field is passed as: {"UrlFieldTest": "http://www.example.com}
                RadioButton field is passed as: {"RadioButtonTest": "Q1"}
            For more information about custom fields visit: https://support.atlassian.com/jira-cloud-administration/docs/custom-fields-types-in-company-managed-projects/
            '''
    )


def jira_create_issue_printer(output):
    if output is None:
        return
    pp.pprint(output)

def jira_create_issue(
        handle: JIRA,
        project_name: str,
        summary: str,
        issue_type: str,
        description: str = "",
        fields: dict=None
        ) -> str:
    """create_issue creates issue in jira.
        :type project_name: str
        :param project_name: The name of the project for which the issue will be generated
        :type summary: str
        :param summary: Summary of the issue
        :type description: str
        :param description: Description of the issue
        :type issue_type: IssueType
        :param issue_type: JIRA Issue Type.
        :type fields: dict
        :param fields: User needs to pass the fields in the format of dict(KEY=VALUE) pair
        :rtype: String with issues key
    """
    issue_type = issue_type if issue_type else None
    if fields:
        issue_fields = {
            'project': project_name,
            'summary': summary,
            'description': description,
            'issuetype': {'name': issue_type}
        }


        for key in list(fields.keys()):
            found = False
            for f in handle.fields():
                if 'schema' not in f:
                    continue
                if f['name'] == key:
                    found = True
                    custom_field_type = f['schema'].get("custom", "")
                    if custom_field_type == CustomFieldTypes.MULTICHECKBOXES.value:
                        issue_fields.update({f['id']: [{'value': i} for i in fields[key]]})

                    elif custom_field_type == CustomFieldTypes.LABELS.value:
                        issue_fields.update({f['id']: fields[key]})

                    elif custom_field_type == CustomFieldTypes.FLOAT.value:
                        issue_fields.update({f['id']: fields[key]})

                    elif custom_field_type == CustomFieldTypes.USERPICKER.value:
                        accountId = get_user_accountId(handle, fields[key])
                        issue_fields.update({f['id']: {"accountId":accountId}})

                    elif custom_field_type == CustomFieldTypes.TEXTAREA.value:
                        issue_fields.update({f['id']: fields[key]})

                    elif custom_field_type == CustomFieldTypes.CASCADINGSELECT.value:
                        cascade_list = {
                              "value": fields[key]["parent"],
                              "child": {
                                "value": fields[key]["child"]
                              }
                            }
                        issue_fields.update({f['id']: cascade_list})

                    elif custom_field_type == CustomFieldTypes.TEXTFIELD.value:
                        issue_fields.update({f['id']: fields[key]})

                    elif custom_field_type == CustomFieldTypes.MULTISELECT.value:
                        issue_fields.update({f['id']: [{'value': i} for i in fields[key]]})

                    elif custom_field_type == CustomFieldTypes.SELECT.value:
                        issue_fields.update({f['id']: {'value': fields[key][0]}})

                    elif custom_field_type == CustomFieldTypes.URL.value:
                        issue_fields.update({f['id']: fields[key]})

                    elif custom_field_type == CustomFieldTypes.RADIOBUTTONS.value:
                        issue_fields.update({f['id']: {'value': fields[key]}})

                    else:
                        if f['schema']['type'] == "array":
                            #There can be 2 scenarios here.
                            # For labels, its an array of strings.
                            # {'id': 'labels', 'key': 'labels', 'name': 'Labels', 'custom':
                            # False, 'orderable': True,
                            # 'navigable': True, 'searchable': True, 'clauseNames': ['labels'],
                            # 'schema': {'type': 'array', 'items': 'string', 'system': 'labels'}}
                            #
                            # For others, its an array of dictionary.
                            # {'id': 'components', 'key': 'components', 'name': 'Components',
                            # 'custom': False,
                            # 'orderable': True, 'navigable': True, 'searchable': True,
                            # 'clauseNames': ['component'],
                            # 'schema': {'type': 'array', 'items': 'component',
                            # 'system': 'components'}}
                            if f['schema']['items'] == "string":
                                issue_fields.update({f['id']: fields[key]})
                            else:
                                issue_fields.update({f['id']: [{'name': i} for i in fields[key]]})
                        elif f['schema']['type'] == "user":
                            accountId = get_user_accountId(handle, fields[key])
                            issue_fields.update({f['id']: {"id": accountId}})
                        else:
                            issue_fields.update({f['id']: {'name': fields[key]}})

            if found is False:
                    raise Exception(f'Invalid field: {key}')


        issue = handle.create_issue(fields=issue_fields)
    else:
        issue = handle.create_issue(project=project_name, summary=summary,
                                    description=description, issuetype={'name': issue_type})
    return issue.key

def get_user_accountId(handle: JIRA, user: str)->str:
    get_user = handle._get_json(f"user/search?query=[{user}]")
    if len(get_user) != 0:
        return get_user[0].get('accountId')
    raise  Exception(f'Unable to get accountId for {user}')
