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
        description='Name of the key to delete'
    )

def workflow_ss_delete_keys_printer(output):
    if output is None:
        return
    if output:
        pprint.pprint("The workflow key deleted successfully!")

def workflow_ss_delete_keys(handle: InfraConnector, key) -> bool:
    """workflow_ss_delete_keys delete workflow key.
        :type key: str.
        :param key: Name of the key to delete.
        :rtype: String confirming the successful deleting of the key.
    """

    try:
        handle.del_workflow_key(key)
    except Exception as e:
        raise e

    return True
