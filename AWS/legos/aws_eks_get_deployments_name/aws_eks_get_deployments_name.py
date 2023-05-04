##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##  @author: Yugal Pachpande, @email: yugal.pachpande@unskript.com
##

import pprint
from typing import List
from pydantic import BaseModel, Field
import pandas as pd
from kubernetes import client
from kubernetes.client.rest import ApiException

class InputSchema(BaseModel):
    clusterName: str = Field(
        title='Cluster Name',
        description='Name of cluster')
    namespace: str = Field(
        title='Cluster Namespace',
        description='Cluster Namespace')
    region: str = Field(
        title='Region',
        description='AWS Region of the cluster')


def aws_eks_get_deployments_name_printer(output):
    if output is None:
        return
    print("\n")
    pprint.pprint(pd.DataFrame(output))


def aws_eks_get_deployments_name(handle, clusterName: str, namespace: str, region: str) -> List:
    """aws_eks_get_deployments_name returns list.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type clusterName: string
        :param clusterName: Cluster name.

        :type namespace: string
        :param namespace: Cluster Namespace.

        :type region: string
        :param region: AWS Region of the EKS cluster.

        :rtype: List of deployments.
    """
    k8shandle = handle.unskript_get_eks_handle(clusterName, region)
    coreApiClient = client.AppsV1Api(api_client=k8shandle)
    deployments_list = []

    try:
        resp = coreApiClient.list_namespaced_deployment(namespace, pretty=True)
        for deployment in resp.items:
            res = {}
            res["NAME"] = deployment.metadata.name
            res['READY'] = (f"Ready {deployment.status.ready_replicas}/"
            f"{deployment.status.available_replicas}")
            res['UP-TO-DATE'] = deployment.status.updated_replicas
            res['AVAILABLE'] = deployment.status.available_replicas
            res['START_TIME'] = deployment.metadata.creation_timestamp.strftime("%m/%d/%Y, %H:%M:%S")
            deployments_list.append(res)

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
    except ApiException as e:
         return ['An Exception occured while executing the command' + e.reason]
    return deployments_list
