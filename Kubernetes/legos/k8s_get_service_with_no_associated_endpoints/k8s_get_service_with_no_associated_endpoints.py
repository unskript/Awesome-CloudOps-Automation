#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
import subprocess
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from tabulate import tabulate



class InputSchema(BaseModel):
    namespace:Optional[str] = Field(
        default = "",
        title = "K8S Namespace",
        description = "Kubernetes Namespace Where the Service exists"
    )

def k8s_get_service_with_no_associated_endpoints_printer(output):
    status, data = output
    if status:
        print("No services with missing endpoints found !")
    else:
        table_headers = ["Namespace", "Service Name"]
        table_data = [(entry["namespace"], entry["name"]) for entry in data]

        print(tabulate(table_data, headers=table_headers, tablefmt = "grid"))

def k8s_get_service_with_no_associated_endpoints(handle, namespace: str = "") -> Tuple:
    """k8s_get_service_with_no_associated_endpoints This function returns Services that
       do not have any associated endpoints.

       :type handle: Object
       :param handle: Object returned from the task.validate(...) function

       :type namespace: str
       :param namespace: String, K8S Namespace as python string

       :rtype: Tuple Result in tuple format.
    """
    retval = []
    if handle.client_side_validation is not True:
        print(f"K8S Connector is invalid: {handle}")
        return str()

    if namespace:
        kubectl_command = "kubectl get svc --namespace " + namespace + " -o custom-columns=NAME:.metadata.name,ENDPOINTS:.subsets[*].addresses[*].ip --no-headers"
    else:
        kubectl_command = "kubectl get svc -A -o custom-columns=NAME:.metadata.name,ENDPOINTS:.subsets[*].addresses[*].ip --no-headers"

    result = handle.run_native_cmd(kubectl_command)

    if result is None:
        print(
            f"Error while executing command ({kubectl_command}) (empty response)")
        return (False, retval)

    if result.stderr:
        raise Exception(f"Error occurred while executing command {kubectl_command} {result.stderr}")
    
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, kubectl_command, result.stderr)

    if result.stdout:
        output_lines = result.stdout.splitlines()
    elif result.stderr:
        output_lines = result.stderr.splitlines()


    for line in output_lines:
        name, endpoints = line.split()
        if endpoints == "<none>":
            retval.append({"name": name, "namespace": namespace})

    if retval:
        return (False, retval)

    return (True, None)
