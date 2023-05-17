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
        description='Name of the key to fetch'
    )

def workflow_ss_get_keys_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def workflow_ss_get_keys(handle: InfraConnector, key) -> bytes:
    """workflow_ss_get_keys get workflow key.
        :type key: str.
        :param key: Name of the key to fetch.
        :rtype: bytes with the key value.
    """

    try:
        v = handle.get_workflow_key(key)
    except Exception as e:
        raise e

    return v
