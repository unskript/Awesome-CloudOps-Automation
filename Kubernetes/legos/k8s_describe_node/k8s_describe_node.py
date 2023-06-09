#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
import pprint
from typing import Dict
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException


class InputSchema(BaseModel):
    node_name: str = Field(
        title='Node',
        description='Kubernetes Node name'
    )

def k8s_desribe_node_printer(output):
    if output is None:
        return

    pprint.pprint(output)


def k8s_describe_node(handle, node_name: str):
    """k8s_describe_node get nodes details

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type node_name: str
        :param node_name: Kubernetes Node name.

        :rtype: Dict of nodes details
    """
    coreApiClient = client.CoreV1Api(handle)

    try:
        resp = coreApiClient.read_node(node_name, pretty=True)

    except ApiException as e:
        resp = 'An Exception occured while executing the command' + e.reason

    return resp
