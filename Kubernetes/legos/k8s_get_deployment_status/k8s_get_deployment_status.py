#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#

import pprint
import json
from typing import Optional, Tuple
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        default='',
        title='Namespace',
        description='k8s Namespace')
    deployment: Optional[str] = Field(
        default='',
        title='Deployment',
        description='k8s Deployment')


def k8s_get_deployment_status_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def k8s_get_deployment_status(handle, deployment: str = "", namespace: str = "") -> Tuple:
    """k8s_get_deployment_status executes the command and give failed deployment list

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type deployment: str
        :param deployment: Deployment Name.
        
        :type namespace: str
        :param namespace: Kubernetes Namespace.

        :rtype: Tuple with status result and list of failed deployments.
    """
    result = []
    if handle.client_side_validation is not True:
        print(f"K8S Connector is invalid: {handle}")
        raise Exception("K8S Connector is invalid")

    status_details = ""
    if namespace and deployment:
        name_cmd = "kubectl get deployment " + deployment + " -n " + namespace + " -o json"
        exec_cmd = handle.run_native_cmd(name_cmd)
        status_op = exec_cmd.stdout
        status_details = json.loads(status_op)

    if not namespace and not deployment:
        name_cmd = "kubectl get deployments --all-namespaces -o json"
        exec_cmd = handle.run_native_cmd(name_cmd)
        status_op = exec_cmd.stdout
        status_details = json.loads(status_op)

    if namespace and not deployment:
        name_cmd = "kubectl get deployment -n " + namespace + " -o json"
        exec_cmd = handle.run_native_cmd(name_cmd)
        status_op = exec_cmd.stdout
        status_details = json.loads(status_op)

    if deployment and not namespace:
        name_cmd = "kubectl get deployment " + deployment + " -o json"
        exec_cmd = handle.run_native_cmd(name_cmd)
        status_op = exec_cmd.stdout
        status_details = json.loads(status_op)

    if status_details:
        if "items" in status_details:
            for items in status_details["items"]:
                namespace_name = items["metadata"]["namespace"]
                deployment_name = items["metadata"]["name"]
                replica_details = items["status"]["conditions"]
                for i in replica_details:
                    deployment_dict = {}
                    if ("FailedCreate" in i["reason"] and "ReplicaFailure" in i["type"] and
                        "True" in i["status"]):
                        deployment_dict["namespace"] = namespace_name
                        deployment_dict["deployment_name"] = deployment_name
                        result.append(deployment_dict)
                    if ("ProgressDeadlineExceeded" in i["reason"] and "Progressing" in i["type"] and
                        "False" in i["status"]):
                        deployment_dict["namespace"] = namespace_name
                        deployment_dict["deployment_name"] = deployment_name
                        result.append(deployment_dict)
        else:
            namespace_name = status_details["metadata"]["namespace"]
            deployment_name = status_details["metadata"]["name"]
            replica_details = status_details["status"]["conditions"]
            for i in replica_details:
                deployment_dict = {}
                if ("FailedCreate" in i["reason"] and "ReplicaFailure" in i["type"] and
                    "True" in i["status"]):
                    deployment_dict["namespace"] = namespace_name
                    deployment_dict["deployment_name"] = deployment_name
                    result.append(deployment_dict)
                if ("ProgressDeadlineExceeded" in i["reason"] and "Progressing" in i["type"] and
                    "False" in i["status"]):
                    deployment_dict["namespace"] = namespace_name
                    deployment_dict["deployment_name"] = deployment_name
                    result.append(deployment_dict)

    if len(result) != 0:
        return (False, result)
    return (True, None)
