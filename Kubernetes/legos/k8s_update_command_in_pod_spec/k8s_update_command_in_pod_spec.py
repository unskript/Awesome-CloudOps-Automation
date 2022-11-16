#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
import pprint
from typing import List
from typing import Tuple
from kubernetes import client
from kubernetes.client.rest import ApiException
from pydantic import BaseModel, Field

pp = pprint.PrettyPrinter(indent=2)


class InputSchema(BaseModel):
    namespace: str = Field(
        title='Namespace',
        description='Kubernetes namespace')
    deployment_name: str = Field(
        title='Deployment Name',
        description='Kubernetes Deployment Name')
    command: list = Field(
        title='Command',
        description='''
            List of Commands to update on the Pod Deployment
            For eg: ["nginx" , "-t"]
            ''')


def k8s_update_command_in_pod_spec_printer(output):
    if output is None:
        return 
    
    (command, resp) = output
    pprint.pprint(command)
    

def k8s_update_command_in_pod_spec(handle, namespace: str, deployment_name: str, command: List) -> Tuple:
    """k8s_update_command_in_pod_spec updateb command in pod spec

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type namespace: str
        :param namespace: Kubernetes namespace.

        :type deployment_name: strdeployment_name: Kubernetes Deployment Name.
        :param 

        :type command: List
        :param command: List of Commands to update on the Pod Deployment.

        :rtype: Tuple
    """
    coreApiClient = client.AppsV1Api(api_client=handle)

    try:
        deployment = coreApiClient.read_namespaced_deployment(
            deployment_name, namespace, pretty=True)
        deployment.spec.template.spec.containers[0].command = list(command)
        resp = coreApiClient.patch_namespaced_deployment(
            name=deployment.metadata.name, namespace=namespace, body=deployment
        )
        return (resp.spec.template.spec.containers[0].command, resp)
    except ApiException as e:
        error = 'An Exception occured while executing the command :{}'.format(
            e)
        pp.pprint(error)
        return (None, error)
