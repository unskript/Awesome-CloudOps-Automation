#
# Copyright (c) 2024 unSkript.com
# All rights reserved.
#
import subprocess
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    helm_command: str = Field(
        title='Helm Command',
        description='Helm command to execute in the K8s Cluster'
    )

def k8s_execute_helm_command_printer(data: str):
    if not data:
        return 
    
    print(data)


def k8s_execute_helm_command(handle, helm_command: str) -> str:
    """k8s_execute_helm_command executes the given helm command in the k8s cluster

       :type handle: object
       :param handle: Object returned from the Task validate method

       :type helm_command: str
       :param helm_command: Helm Command that need to be executed 

       :rtype: String, Output of the given helm command. Empty string in case of error
    """
    retval = None 
    if handle.client_side_validation is not True:
        print(f"K8S Connector is invalid: {handle}")
        return str()
    
    if not helm_command:
        print(f"Given helm command is empty, cannot proceed further!")
        return str()
    
    config_file = None
    try:
        config_file = handle.temp_config_file 
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return str()
    
    if config_file:
        if not '--kubeconfig' in helm_command:
            helm_command = helm_command.replace('helm',
                                                f'helm --kubeconfig {config_file}')
    else:
        # Incluster configuration, so need not have any kubeconfig 
        pass 

    try:
        result = subprocess.run(helm_command,
                                check=True,
                                shell=True,
                                capture_output=True,
                                text=True)
        retval = result.stdout 
        
        # If error is set, then lets dump the error code
        if result.stderr and result.returncode != 0:
            print(result.stderr)

    except subprocess.CalledProcessError as e:
        error_message = f"Error running command: {e}\n{e.stderr.decode('utf-8')}" \
                    if e.stderr else f"Error running command: {e}"
        print(error_message)

    return retval
             