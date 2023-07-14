#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#

import pprint
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from kubernetes.client.rest import ApiException
from kubernetes import client, watch


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
    coreApiClient = client.CoreV1Api(api_client=handle)
    BatchApiClient = client.BatchV1Api(api_client=handle)
    # If namespace is provided, get jobs from the specified namespace
    if namespace:
        jobs = BatchApiClient.list_namespaced_job(namespace,watch=False, limit=200).items
    # If namespace is not provided, get jobs from all namespaces
    else:
        jobs = BatchApiClient.list_job_for_all_namespaces(watch=False, limit=200).items

    for job in jobs:
        # Fetching all the pods associated with the current job
        pods = coreApiClient.list_namespaced_pod(job.metadata.namespace, label_selector=f"job-name={job.metadata.name}",watch=False, limit=200).items

        # Checking the status of each pod
        for pod in pods:
            # If the pod status is 'Failed', print its namespace and name
            if pod.status.phase != "Succeeded":
                result.append({"namespace":pod.metadata.namespace,"pod_name":pod.metadata.name})
    if len(result) != 0:
        return (False, result)
    else:
        return (True, None)
