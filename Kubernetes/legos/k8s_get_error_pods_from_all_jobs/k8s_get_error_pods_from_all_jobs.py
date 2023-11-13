#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#

import pprint
from typing import Tuple, Optional
from pydantic import BaseModel, Field


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

    # If namespace is provided, get jobs from the specified namespace
    if namespace:
        get_jobs_command = f"kubectl get jobs -n {namespace} --no-headers -o custom-columns=NAME:.metadata.name"
    # If namespace is not provided, get jobs from all namespaces
    else:
        get_jobs_command = "kubectl get jobs --all-namespaces --no-headers -o custom-columns=NAME:.metadata.name"

    try:
        # Execute the kubectl command to get job names
        #response = subprocess.run(get_jobs_command.split(), capture_output=True, text=True, check=True)
        response = handle.run_native_cmd(get_jobs_command)
        job_names = response.stdout.splitlines()
    except Exception as e:
        raise Exception(f"Error fetching job names: {e.stderr}") from e

    for job_name in job_names:
        # Fetching all the pods associated with the current job
        get_pods_command = f"kubectl get pods -n {namespace} -l job-name={job_name} --no-headers -o custom-columns=NAME:.metadata.name,PHASE:.status.phase"
        
        try:
            # Execute the kubectl command to get pod names and phases
            #response = subprocess.run(get_pods_command.split(), capture_output=True, text=True, check=True)
            response = handle.run_native_cmd(get_pods_command)
            pod_info = [line.split() for line in response.stdout.splitlines()]
        except Exception as e:
            raise Exception(f"Error fetching pods for job {job_name}: {e.stderr}") from e

        # Checking the status of each pod
        for pod_name, pod_phase in pod_info:
            # If the pod status is not 'Succeeded', add it to the result list
            if pod_phase != "Succeeded":
                result.append({"namespace": namespace, "pod_name": pod_name})

    if len(result) != 0:
        return False, result
    else:
        return True, None

