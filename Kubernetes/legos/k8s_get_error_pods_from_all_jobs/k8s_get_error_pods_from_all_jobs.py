#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#

import pprint
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from kubernetes.client.rest import ApiException
import json


class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        default='',
        title='Namespace',
        description='k8s Namespace')


def k8s_get_error_pods_from_all_jobs_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def k8s_get_error_pods_from_all_jobs(handle, namespace: str = '') -> Tuple:
    """k8s_get_error_pods_from_all_jobs This check function uses the handle's native command
       method to execute a pre-defined kubectl command and returns the output of list of error pods
       from all jobs.

       :type handle: Object
       :param handle: Object returned from the task.validate(...) function

       :rtype: Tuple Result in tuple format.
    """
    action_op = []
    if handle.client_side_validation is not True:
        raise ApiException(f"K8S Connector is invalid {handle}")

    if not namespace:
        kubectl_command = f"kubectl get jobs --all-namespaces -o json"
    else:
        kubectl_command = f"kubectl get jobs -n {namespace} -o json"
    result = handle.run_native_cmd(kubectl_command)
    if result.stderr:
        raise ApiException(f"Error occurred while executing command {kubectl_command} {result.stderr}")
    job_names = []
    if result.stdout:
        op = json.loads(result.stdout)
        for jobs in op["items"]:
            job_dict = {}
            job_dict["job_name"] = jobs["metadata"]["name"]
            job_dict["namespace"] = jobs["metadata"]["namespace"]
            job_names.append(job_dict)
    if job_names:
        for job in job_names:
            command = f"""kubectl get pods --selector=job-name={job["job_name"]} -n {job["namespace"]} --field-selector=status.phase!=Running -o json"""
            pod_result = handle.run_native_cmd(kubectl_command)
            if pod_result.stderr:
                raise ApiException(f"Error occurred while executing command {command} {pod_result.stderr}")
            job_names = []
            if pod_result.stdout:
                pod_op = json.loads(pod_result.stdout)
                for pods in pod_op["items"]:
                    pod_dict = {}
                    pod_dict["job_name"] = job["job_name"]
                    pod_dict["namespace"] = job["namespace"]
                    pod_dict["pod_name"] = pods["metadata"]["name"]
                    action_op.append(pod_dict)
    if len(action_op) != 0:
        return (False, action_op)
    else:
        return (True, None)
