#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#

import pprint
from pydantic import BaseModel, Field
import os
#import subprocess

class InputSchema(BaseModel):
    pod_name: str = Field(
        title="Pod Name",
        description="K8S Pod Name"
    )
    namespace: str = Field(
        title="Namespace",
        description="K8S Namespace where the POD exists"
    )
    file_name: str = Field(
        title="Script Text",
        description="Text data of the script that needs to be run on the pod. "
    )

def k8s_execute_local_script_on_a_pod_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def k8s_execute_local_script_on_a_pod(handle, namespace: str, pod_name:str, file_name:str)->str:
    """k8s_execute_local_script_on_a_pod executes a given script on a pod

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type namespace: str
        :param namespace: Namespace to get the pods from. Eg:"logging"

        :type pod_name: str
        :param pod_name: Pod name to to run the script.

        :type file_name: str
        :param file_name: Script file name.

        :rtype: String of the result of the script that was run on the pod
    """
    # Step 2: Copy the script to the pod using kubectl cp command
    tmp_script_path = "/tmp/script.sh"
    handle.run_native_cmd(f'kubectl cp {file_name} {namespace}/{pod_name}:{tmp_script_path}')

    # Step 3: Make the script executable on the pod
    handle.run_native_cmd(f'kubectl exec -n {namespace} {pod_name} -- chmod +x {tmp_script_path}')

    # Step 4: Execute the script on the pod and get the output
    command = f'kubectl exec -n {namespace} {pod_name} -- sh -c {tmp_script_path}'

    result = handle.run_native_cmd(command)
    # Remove the temporary script file
    handle.run_native_cmd(f'kubectl exec -n {namespace} {pod_name} -- rm -f {tmp_script_path}')

    if result.stderr not in ('', None):
        raise result.stderr
    return result.stdout