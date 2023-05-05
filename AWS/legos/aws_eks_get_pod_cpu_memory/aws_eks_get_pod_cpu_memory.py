##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import List
import pandas as pd
from pydantic import BaseModel, Field
from kubernetes import client
from kubernetes.client.rest import ApiException


class InputSchema(BaseModel):
    clusterName: str = Field(
        title='Cluster Name',
        description='Name of cluster')
    namespace: str = Field(
        title='Cluster namespace',
        description='Cluster Namespace')
    region: str = Field(
        title='Region',
        description='AWS Region of the cluster')


def aws_eks_get_pod_cpu_memory_printer(output):
    if output is None:
        return
    print("\n")
    pprint.pprint(pd.DataFrame(output))


def aws_eks_get_pod_cpu_memory(handle, clusterName: str, namespace: str, region: str) -> List:
    """aws_eks_get_pod_cpu_memory returns list.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type clusterName: string
        :param clusterName: Cluster name.

        :type namespace: string
        :param namespace: Cluster Namespace.

        :type region: string
        :param region: AWS Region of the EKS cluster.

        :rtype: List of pods with cpu and memory usage details.
    """
    k8shandle = handle.unskript_get_eks_handle(clusterName, region)
    CustomObjectsClient = client.CustomObjectsApi(api_client=k8shandle)

    try:
        data = []
        resp = CustomObjectsClient.list_namespaced_custom_object(group="metrics.k8s.io",
                                                                 version="v1beta1",
                                                                 namespace=namespace,
                                                                 plural="pods")

        for pod in resp.get('items', []):
            for container in pod.get('containers', []):
                data.append({
                    "pod_name": pod['metadata']['name'], "container_name": container.get('name'),
                    "cpu": container['usage']["cpu"],
                    "memory": "%s Mi" %
                              round(int(container['usage']["memory"].split("Ki")[0]) / 1024, 2)})

    except ApiException as e:
        pprint.pprint(str(e))
        data = [
            {'error': 'An Exception occured while executing the command' + e.reason}]
        raise e
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    return data
