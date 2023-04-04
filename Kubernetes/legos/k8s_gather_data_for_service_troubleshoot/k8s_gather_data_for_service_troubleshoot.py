#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#

from pydantic import BaseModel, Field
from typing import Optional, Tuple
from kubernetes import client
import pprint

class InputSchema(BaseModel):
    service_name: str = Field(
        title="Service Name",
        description="K8S Service Name to gather data"
    )
    namespace: str = Field(
        title='Namespace',
        description='k8s Namespace')


def k8s_gather_data_for_service_troubleshoot_printer(output):
    if not output:
        return 
    pprint.pprint(output)

def k8s_gather_data_for_service_troubleshoot(handle, servicename: str, namespace: str) -> dict:
    """k8s_gather_data_for_service_troubleshoot This utility function can be used to gather data
       for a given service in a namespace. 

       :type handle: object
       :param handle: Object returned from task.validate(...) function

       :type servicename: str
       :param servicename: Service Name that needs gathering data

       :type namespace: str
       :param namespace: K8S Namespace

       :rtype: Dictionary containing the result
    """
    if not namespace or not servicename :
        raise Exception("Namespace and Servicename are mandatory parameter")
    
    # Get Service Detail
    describe_cmd = f'kubectl describe svc {servicename} -n {namespace}'
    describe_output = handle.run_native_cmd(describe_cmd)
    retval = {}
    if not describe_output.stderr:
        retval['describe'] = describe_output.stdout 
    
    ingress_rules_cmd = f'kubectl get svc {servicename} -n {namespace} | jq ".items[].spec.rules[]'
    ingress_rules_output = handle.run_native_cmd(ingress_rules_cmd)
    if not ingress_rules_output.stderr:
        retval['ingress_rules'] = ingress_rules_output.stdout
        
    
    return retval