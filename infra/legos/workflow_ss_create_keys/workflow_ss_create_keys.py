##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint

from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    key: str = Field(
        title='Key',
        description='Name of the key to create'
    )
    value: str = Field(
        title='Value',
        description='Value to persist'
    )

def workflow_ss_create_keys_printer(output):
    if output is None:
        return
    if output:
        pprint.pprint("The workflow key set successfully!")

def workflow_ss_create_keys(handle, key, value) -> bool:
    """workflow_ss_create_keys create new workflow key.
        :type key: str.
        :param key: Name of the key to create.
        :type value: str.
        :param value: Value to persist.
        :rtype: String confirming the successful creation of the key.
    """
    try:
        handle.set_workflow_key(key, value)
    except Exception as e:
        raise e

    return True
