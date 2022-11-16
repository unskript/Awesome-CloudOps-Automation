##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from pydantic import BaseModel, Field
from typing import Optional, List
from kubernetes import client
from kubernetes.client.rest import ApiException
import pandas as pd
from unskript.legos.aws.aws_get_handle.aws_get_handle import Session


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


def aws_eks_get_all_dead_pods_printer(output):
    if output is None:
        return
    print("\n")
    if not output:
        print ("There are no dead pods in this namespace")
        return
    pprint.pprint(pd.DataFrame(output))


def aws_eks_get_all_dead_pods(handle: Session,clusterName: str,region: str,namespace: str = 'all',) -> List:
    """aws_eks_get_all_dead_podsr eturns list.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type clusterName: string
        :param clusterName: Cluster name.

        :type namespace: string
        :param namespace: Cluster Namespace.

        :type region: string
        :param region: AWS Region of the EKS cluster.

        :rtype: List of all dead pods in a namespace.
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
        for container_status in i.status.container_statuses:
            if container_status.started is False or container_status.ready is False:
                waiting_state = container_status.state.waiting
                status = waiting_state.reason
                if status.lower() in ["evicted"]:
                    data.append({"Pod Ip": i.status.pod_ip,
                                 "Namespace": i.metadata.namespace,
                                 "Pod Name": i.metadata.name,
                                 "Container Name": container_status.name,
                                 "Status": status,
                                 "Start Time": i.status.start_time,
                                 })
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    return data
