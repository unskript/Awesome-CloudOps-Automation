from __future__ import annotations

##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
import pprint
from typing import Dict
from pydantic import BaseModel, Field



from typing import List

from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    region: str = Field(..., description='AWS Region.', title='Region')
    resource_arn: List = Field(..., description='Resource ARNs.', title='Resource ARN')
    tag_key: str = Field(..., description='Resource Tag Key.', title='Tag Key')
    tag_value: str = Field(..., description='Resource Tag Value.', title='Tag Value')


# This API has a limit of 20 ARNs per api call...
#we'll need to break up the list into chunks of 20
def break_list(long_list, max_size):
    return [long_list[i:i + max_size] for i in range(0, len(long_list), max_size)]



def aws_attach_tags_to_resources_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_attach_tags_to_resources(
    handle,
    resource_arn: list,
    tag_key: str,
    tag_value: str,
    region: str
    ) -> Dict:
    """aws_attach_tags_to_resources Returns an Dict of resource info.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type resource_arn: list
        :param resource_arn: Resource ARNs.

        :type tag_key: str
        :param tag_key: Resource Tag Key.

        :type tag_value: str
        :param tag_value: Resource Tag value.

        :type region: str
        :param region: Region to filter resources.

        :rtype: Dict of resource info.
    """
    ec2Client = handle.client('resourcegroupstaggingapi', region_name=region)
    result = {}

    #break the ARN list into groups of 20 to send through the API
    list_of_lists = break_list(taggedResources, 20)

    for index, smallerList in enumerate(list_of_lists):

        try:
            response = ec2Client.tag_resources(
                ResourceARNList=smallerList,
                Tags={tag_key: tag_value}
                )
            result[index] = response

        except Exception as error:
            result[f"{index} error"] = error

    return result



