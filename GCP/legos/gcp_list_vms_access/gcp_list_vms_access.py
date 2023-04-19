##  Copyright (c) 2023 unSkript, Inc
## Written by Doug Sillars & ChatGPT
##  All rights reserved.
##
from pydantic import BaseModel, Field
import pprint
from typing import List,Any, Dict
from google.cloud import compute

from beartype import beartype


class InputSchema(BaseModel):
    project: str = Field(
        title='Project Name',
        description='Name of the Google Cloud Project.')
    zone: str = Field(
        title='Zone',
        description='Name of the Google Cloud Zone where the project is located.')



@beartype
def gcp_list_VMs_access_printer(output):
    if len(output)==0:
        print("There are no publicly readable buckets available")
        return
    print(output)


@beartype
def gcp_list_VMs_access(handle, project:str, zone:str) -> List:


    compute_client = compute.InstancesClient(credentials=handle)
    
    vms = compute_client.list(project=project, zone=zone)
    vm_list = []
    for vm in vms:
        vm_info = {}
        vm_info['name'] = vm.name
        vm_info['publicly_accessible'] = vm.can_ip_forward
        vm_list.append(vm_info)

    return(vm_list)