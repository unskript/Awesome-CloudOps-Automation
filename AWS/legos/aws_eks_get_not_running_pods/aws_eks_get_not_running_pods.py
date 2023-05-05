##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import List
import pandas as pd
from pydantic import BaseModel, Field
from unskript.legos.aws.aws_get_handle.aws_get_handle import Session
from kubernetes import client
from kubernetes.client.rest import ApiException


class InputSchema(BaseModel):
    clusterName: str = Field(
        title='Cluster Name.',
        description='Name of EKS cluster.')
    region: str = Field(
        title='Region',
        description='AWS Region of the EKS cluster.')


def aws_eks_get_not_running_pods_printer(output):
    if output is None:
        return
    print("\n")
    pprint.pprint(pd.DataFrame(output))


def aws_eks_get_not_running_pods(handle: Session, clusterName: str, region: str) -> List:
    """aws_eks_get_not_running_pods returns list.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type clusterName: string
        :param clusterName: Cluster name.

        :type region: string
        :param region: AWS Region of the EKS cluster.

        :rtype: List of pods not in running state .
    """
    k8shandle = handle.unskript_get_eks_handle(clusterName, region)
    coreApiClient = client.CoreV1Api(api_client=k8shandle)
    try:
        resp = coreApiClient.list_pod_for_all_namespaces(pretty=True)

    except ApiException as e:
        pprint.pprint(str(e))
        resp = 'An Exception occured while executing the command' + e.reason

    res = []
    for container in resp.items:
        if container.status.phase not in ["Running"]:
            res.append({"pod_name": container.metadata.name, "status": container.status.phase,
                        "namespace": container.metadata.namespace,
                        "node_name": container.spec.node_name})
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)
    return res
