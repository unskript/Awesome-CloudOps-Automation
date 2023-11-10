##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import json
from typing import Optional, Tuple
from pydantic import BaseModel, Field



class InputSchema(BaseModel):
    restart_threshold: Optional[int] = Field(
        default = 90,
        description='Threshold number of times for which a pod should be restarting. Default is 90 times.',
        title='Restart threshold',
    )


def k8s_get_frequently_restarting_pods_printer(output):
    if output is None:
        return
    print(output)


def k8s_get_frequently_restarting_pods(handle, restart_threshold:int=90) -> Tuple:
    """k8s_get_frequently_restarting_pods finds any K8s pods that have restarted more number of times than a given threshold

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type restart_threshold: int
        :param restart_threshold: Threshold number of times for which a pod should be restarting

        :rtype: Tuple of status and list of namespaces and pods that have restarted more than the threshold number of times.
    """
    result = []
    cmd = "kubectl get pods --all-namespaces --sort-by='.status.containerStatuses[0].restartCount' -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,RESTART_COUNT:.status.containerStatuses[0].restartCount' -o json"
    response = handle.run_native_cmd(cmd)
    if response is None:
        print(
            f"Error while executing command ({cmd}) (empty response)")

    if response.stderr:
        raise Exception(
            f"Error occurred while executing command {cmd} {response.stderr}")

    all_pods_data = json.loads(response.stdout)
    for pod_data in all_pods_data['items']:
        pod = pod_data['metadata']['name']
        nmspace = pod_data['metadata']['namespace']

        # Check if 'containerStatuses' is present and if it's not empty
        if 'containerStatuses' in pod_data['status'] and pod_data['status']['containerStatuses']:
            restart_count = pod_data['status']['containerStatuses'][0]['restartCount']
            if restart_count > restart_threshold:
                pods_dict = {
                    'pod': pod,
                    'namespace': nmspace
                }
                result.append(pods_dict)
    if len(result) != 0:
        return (False, result)
    return (True, None)

