##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
import pprint


class InputSchema(BaseModel):
    clusterName: str = Field(
        title='EKS Cluster Name',
        description='Name EKS Cluster')
    command: str = Field(
        title='Kubectl Command',
        description='kubectl commands For Eg. kubectl get pods --all-namespaces')
    region: str = Field(
        title='Region',
        description='AWS Region of the cluster')


def aws_eks_run_kubectl_cmd_printer(output):
    if output is None:
        return
    print("\n")
    pprint.pprint(output)


def aws_eks_run_kubectl_cmd(handle, clusterName: str, command: str, region: str) -> str:
    """aws_eks_run_kubectl_cmd returns string.

        :type handle: object
        :param handle: Object returned from task.validate(...).

        :type clusterName: string
        :param clusterName: Cluster name.

        :type command: string
        :param command: Kubectl command to run on EKS Cluster .

        :type region: string
        :param region: AWS Region of the EKS cluster.

        :rtype: string of output of command result.
    """
    result = handle.unskript_get_eks_handle(clusterName, region).run_native_cmd(command)
    if result.stderr:
        return "The kubectl command didn't work!"
    return result.stdout
