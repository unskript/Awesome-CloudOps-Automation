#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
from typing import Dict
from kubernetes import client
from kubernetes.client.rest import ApiException
from pydantic import BaseModel, Field
import pprint 

class InputSchema(BaseModel):
    namespace: str = Field(
        title='Namespace',
        description='Kubernetes namespace')
    podname: str = Field(
        title='Podname',
        description='K8S Pod Name')


def k8s_delete_pod_printer(output):
    if output is None:
        return 
        
    pprint.pprint(output)
        

def k8s_delete_pod(handle, namespace: str, podname: str) -> Dict:
    """k8s_delete_pod delete a Kubernetes POD in a given Namespace

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type namespace: str
        :param namespace: Kubernetes namespace

        :type podname: str
        :param podname: K8S Pod Name

        :rtype: Dict of POD info
    """
    coreApiClient = client.CoreV1Api(api_client=handle)

    try:
        resp = coreApiClient.delete_namespaced_pod(
            name=podname, namespace=namespace)
    except ApiException as e:
        resp = 'An Exception occured while executing the command' + e.reason

    return resp
