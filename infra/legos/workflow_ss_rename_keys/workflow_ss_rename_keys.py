##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from pydantic import BaseModel, Field
from unskript.connectors.infra import InfraConnector

class InputSchema(BaseModel):
    old_key: str = Field(
        title='Old Key',
        description='Name of the old key'
    )
    new_key: str = Field(
        title='New Key',
        description='Key to update'
    )

def workflow_ss_rename_keys_printer(output):
    if output is None:
        return
    if output:
        pprint.pprint("The workflow key renamed successfully!")

def workflow_ss_rename_keys(handle: InfraConnector, old_key, new_key) -> bool:
    """workflow_ss_rename_keys rename workflow key.

        :type old_key: str.
        :param old_key: Name of the key to update.

        :type new_key: str.
        :param new_key: key to update.
        
        :rtype: String confirming the successful renaming of the key.
    """

    try:
        handle.rename_workflow_key(old_key, new_key)
    except Exception as e:
        raise e

    return True
