##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint

from pydantic import BaseModel, Field

from unskript.connectors.infra import InfraConnector


class InputSchema(BaseModel):
    key: str = Field(
        title='Key',
        description='Name of the key to update'
    )
    value: str = Field(
        title='Value',
        description='Value to update'
    )

def workflow_ss_update_keys_printer(output):
    if output is None:
        return
    if output:
        pprint.pprint("The workflow key updated successfully!")

def workflow_ss_update_keys(handle: InfraConnector, key, value) -> bool:
    """workflow_ss_update_keys updates workflow key.

        :type key: str.
        :param key: Name of the key to update.

        :type value: str.
        :param value: Value to update.
        
        :rtype: String confirming the successful updating of the key.
    """

    try:
        handle.upd_workflow_key(key, value)
    except Exception as e:
        raise e

    return True
