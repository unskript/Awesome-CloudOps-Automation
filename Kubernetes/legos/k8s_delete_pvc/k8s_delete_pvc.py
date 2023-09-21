from __future__ import annotations

##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from typing import Dict
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
import pprint
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    namespace: str = Field(..., description='Kubernetes namespace', title='K8s namespace')
    pvc_names: list = Field(..., description='List of K8S PVC Names. Eg: ["data-dir-1", "data-dir-2"]', title='List of PVC names')



def k8s_delete_pvc_printer(output):
    if output is None:
        return

    pprint.pprint(output)

def k8s_delete_pvc(handle, namespace: str, pvc_names: list) -> Dict:
    """
    k8s_delete_pvc force deletes one or more Kubernetes PVCs in a given Namespace.

    :type handle: object
    :param handle: Object returned from the Task validate method or Kubernetes client configuration

    :type namespace: str
    :param namespace: Kubernetes namespace

    :type pvc_names: list
    :param pvc_names: List of K8S PVC Names. Eg: ["data-dir-1", "data-dir-2"]

    :rtype: Dict or str with information about the deletion or error.
    """
    coreApiClient = client.CoreV1Api(api_client=handle)

    responses = {}
    for pvc_name in pvc_names:
        try:
            resp = coreApiClient.delete_namespaced_persistent_volume_claim(
                name=pvc_name,
                namespace=namespace,
                body=client.V1DeleteOptions(propagation_policy='Foreground')  # This forces the deletion
            )
            responses[pvc_name] = resp.status
        except ApiException as e:
            resp = 'An Exception occurred while executing the command ' + e.reason
            responses[pvc_name] = resp
            raise e

    return responses



