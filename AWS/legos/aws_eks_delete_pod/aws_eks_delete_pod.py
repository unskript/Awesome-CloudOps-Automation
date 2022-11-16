# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
# @author: Yugal Pachpande, @email: yugal.pachpande@unskript.com
##

from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException
import pprint
from typing import Dict


class InputSchema(BaseModel):
    clusterName: str = Field(
        title='Cluster Name',
        description='Name of cluster')
    namespace: str = Field(
        title='Namespace',
        description='Kubernetes namespace')
    podname: str = Field(
        title='Podname',
        description='K8S Pod Name')
    region: str = Field(
        title='Region',
        description='AWS Region of the cluster')


def aws_eks_delete_pod_printer(output):
    if output is None:
        return
    print("\n")
    pprint.pprint(output)


def aws_eks_delete_pod(handle, clusterName: str, namespace: str, podname: str, region: str) -> Dict:
    """aws_eks_delete_pod returns list.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type clusterName: string
        :param clusterName: Cluster name.

        :type namespace: string
        :param namespace: Cluster Namespace.

        :type podname: string
        :param podname: Name of pod to be deleted.

        :type region: string
        :param region: AWS Region of the EKS cluster.

        :rtype: Dict of details of deleted pod.
    """
    k8shandle = handle.unskript_get_eks_handle(clusterName, region)
    CoreV1Api = client.CoreV1Api(api_client=k8shandle)

    try:
        resp = CoreV1Api.delete_namespaced_pod(
            name=podname, namespace=namespace, pretty=True)
    except ApiException as e:
        resp = 'An Exception occured while executing the command' + e.reason
    return resp
