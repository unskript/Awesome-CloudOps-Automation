#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
import subprocess
from pydantic import BaseModel

class InputSchema(BaseModel):
    pass


def k8s_get_versioning_info_printer(output):
    print("Versions:")
    for key, value in output.items():
        print(f"{key}: {value}")


def k8s_get_versioning_info(handle):
    """
    k8s_get_versioning_info returns the kubectl, Kubernetes cluster, and Docker version if available.

    :type handle: Object
    :param handle: Object returned from the task.validate(...) function

    :rtype: Dict of version results.
    """
    versions = {}

    try:
        # Getting kubectl version
        kubectl_version_command = ["kubectl", "version", "--client", "--short"]
        result = subprocess.run(kubectl_version_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            versions['kubectl'] = result.stdout.decode('utf-8').strip()
    except FileNotFoundError:
        versions['kubectl'] = "Not found"

    try:
        # Getting Kubernetes cluster version
        k8s_version_command = ["kubectl", "version", "--short"]
        result = subprocess.run(k8s_version_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            versions['kubernetes'] = result.stdout.decode('utf-8').strip()
    except FileNotFoundError:
        versions['kubernetes'] = "Not found"

    try:
        # Getting Docker version
        docker_version_command = ["docker", "version", "--format", "'{{.Server.Version}}'"]
        result = subprocess.run(docker_version_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            versions['docker'] = result.stdout.decode('utf-8').strip()
    except FileNotFoundError:
        versions['docker'] = "Not found"

    return versions