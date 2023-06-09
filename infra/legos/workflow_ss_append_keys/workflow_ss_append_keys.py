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

def workflow_ss_append_keys_printer(output):
    if output is None:
        return
    pprint.pprint("The workflow key appended successfully!")

def workflow_ss_append_keys(handle, key, value) -> bool:
    """workflow_ss_append_keys append the values for that key

        :type key: str.
        :param key: Name of the key to create.

        :type value: str.
        :param value: Value to persist.
        
        :rtype: String confirming the successful append of the key.
    """
    try:
        handle.append_workflow_key(key, value)
    except Exception as e:
        raise e

    return True
