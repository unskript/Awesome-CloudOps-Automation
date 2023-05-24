#
# Copyright (c) 2022 unSkript.com
# All rights reserved.
#

import pprint
from pydantic import BaseModel, Field
import os
import subprocess

class InputSchema(BaseModel):
    pod_name: str = Field(
        title="Pod Name",
        description="K8S Pod Name"
    )
    namespace: str = Field(
        title="Namespace",
        description="K8S Namespace where the POD exists"
    )
    script_text: str = Field(
        title="Script Text",
        description="Text data of the script that needs to be run on the pod. "
    )

def k8s_execute_local_script_on_a_pod_printer(output):
    if output is None:
        return
    pprint.pprint(output)


def k8s_execute_local_script_on_a_pod(handle, namespace: str, pod_name:str, script_text:str)->str:
    """k8s_execute_local_script_on_a_pod executes a given script on a pod

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type namespace: str
        :param namespace: Namespace to get the pods from. Eg:"logging"

        :type pod_name: str
        :param pod_name: Pod name to to run the script.

        :type script_text: str
        :param script_text: Text data of the script that needs to be run on the pod.

        :rtype: String of the result of the script that was run on the pod
    """
    # Step 1: Create a temporary file in /tmp and populate it with the script passed as input
    tmp_script_path = '/tmp/script.sh'
    with open(tmp_script_path, 'w') as tmp_script:
        tmp_script.write(script_text)

    # Step 2: Copy the script to the pod using kubectl cp command
    subprocess.run(['kubectl', 'cp', tmp_script_path, f'{namespace}/{pod_name}:{tmp_script_path}'])

    # Step 3: Make the script executable on the pod
    subprocess.run(['kubectl', 'exec', '-n', namespace, pod_name, '--', 'chmod', '+x', tmp_script_path])

    # Step 4: Execute the script on the pod and get the output
    command = f'kubectl exec -n {namespace} {pod_name} -- {tmp_script_path}'
    output = subprocess.check_output(command, shell=True, text=True)
    
    # Remove the temporary script file
    os.remove(tmp_script_path)
    
    return output