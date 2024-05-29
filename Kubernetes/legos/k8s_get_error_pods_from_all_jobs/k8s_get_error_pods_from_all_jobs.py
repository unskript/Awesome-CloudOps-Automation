#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#

import pprint
from typing import Tuple, Optional
from pydantic import BaseModel, Field
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


def k8s_get_error_pods_from_all_jobs(handle, namespace:str="") -> Tuple:
    """k8s_get_error_pods_from_all_jobs This check function uses the handle's native command
       method to execute a pre-defined kubectl command and returns the output of list of error pods
       from all jobs.

       :type handle: Object
       :param handle: Object returned from the task.validate(...) function

       :rtype: Tuple Result in tuple format.
    """
    result = []
    # Fetch jobs for a particular namespace or if not given all namespaces
    ns_cmd = f"-n {namespace}" if namespace else "--all-namespaces"
    kubectl_cmd = f"kubectl get jobs {ns_cmd} -o json"
    response = handle.run_native_cmd(kubectl_cmd)
    
    if response.stderr:
        raise Exception(f"Error occurred while executing command {kubectl_cmd}: {response.stderr}")
    jobs = {}
    try:
        if response.stdout:
            jobs = json.loads(response.stdout)
    except json.JSONDecodeError:
        raise Exception("Failed to parse JSON output from kubectl command.")

    for job in jobs.get("items", []):
        job_name = job["metadata"]["name"]
        job_namespace = job["metadata"]["namespace"]
        # Fetch pods for each job
        pod_kubectl_cmd = f"kubectl get pods -n {job_namespace} -l job-name={job_name} -o json"
        pod_response = handle.run_native_cmd(pod_kubectl_cmd)
        
        if pod_response.stderr:
            print(f"Error occurred while fetching pods for job {job_name}: {pod_response.stderr}")
            continue
        pods = {}
        try:
            if response.stdout:
                pods = json.loads(pod_response.stdout)
        except json.JSONDecodeError:
            print(f"Failed to parse JSON pod response output for kubectl command: {pod_kubectl_cmd}")
            pass
        for pod in pods.get("items", []):
            if pod["status"]["phase"] not in ["Succeeded", "Running"]:
                result.append({"pod_name": pod["metadata"]["name"],
                                "job_name": job_name,
                                "namespace": pod["metadata"]["namespace"]
                                })
    if result:
        return (False, result)
    else:
        return (True, None)
