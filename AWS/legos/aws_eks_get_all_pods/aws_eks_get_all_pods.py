##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import Optional, List
from pydantic import BaseModel, Field
import pandas as pd
from unskript.legos.aws.aws_get_handle.aws_get_handle import Session
from kubernetes import client
from kubernetes.client.rest import ApiException



class InputSchema(BaseModel):
    clusterName: str = Field(
        title='Cluster Name',
        description='Name of EKS cluster')
    namespace: Optional[str] = Field(
        'all',
        title='Cluster Namespace',
        description='Cluster Namespace')
    region: str = Field(
        title='Region',
        description='AWS Region of the EKS cluster')


def aws_eks_get_all_pods_printer(output):
    if output is None:
        return
    print("\n")
    pprint.pprint(pd.DataFrame(output))


def aws_eks_get_all_pods(
    handle: Session,
    clusterName: str,
    region: str,
    namespace: str = 'all',
    ) -> List:
    """aws_eks_get_all_pods returns list.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type clusterName: string
        :param clusterName: Cluster name.

        :type namespace: string
        :param namespace: Cluster Namespace.

        :type region: string
        :param region: AWS Region of the EKS cluster.

        :rtype: List of pods with status ip and start time.
    """

    k8shandle = handle.unskript_get_eks_handle(clusterName, region)
    coreApiClient = client.CoreV1Api(api_client=k8shandle)
    try:
        res = coreApiClient.list_namespaced_pod(
            namespace=namespace, pretty=True)
    except ApiException as e:
        pprint.pprint(str(e))
        res = 'An Exception occured while executing the command' + e.reason

    data = []
    for i in res.items:
        data.append({"Pod Ip": i.status.pod_ip,
                     "Namespace": i.metadata.namespace,
                     "Name": i.metadata.name,
                     "Status": i.status.phase,
                     "Start Time": i.status.start_time,
                     })
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    return data
