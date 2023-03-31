#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#

from pydantic import BaseModel, Field
from typing import Optional, Tuple
from kubernetes import client
import pprint

class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        default='',
        title='Namespace',
        description='k8s Namespace')


def k8s_gather_data_for_service_troubleshoot_printer(output):
    if not output:
        return 
    pprint.pprint(output)

def k8s_gather_data_for_service_troubleshoot(handle, namespace: str) -> dict:
    if not namespace:
        raise Exception("Namespace is a mandatory parameter")
    
    core_api = client.CoreV1Api(api_client=handle)
    api_client = client.ApiClient(handle)
    extension_api = client.ExtensionsV1beta1Api(api_client=handle)
    services = core_api.list_namespaced_service(namespace=namespace)
    retval = {}

    ingress_list = api_client.configuration()
    for service in services.items:
        endpoints = core_api.list_namespaced_endpoints(namespace=namespace, field_selector=f'metadata.name={service}')
        service_active = False
        if endpoints and endpoints.items and endpoints.items[0].subsets and endpoints.items[0].subsets[0].addresses:
            service_active = True
        
        retval[service.metadata.name] = {}
        retval[service.metadata.name]['active'] = service_active 
        retval[service.metadata.name]['namespace'] = service.metadata.namespace 
        retval[service.metadata.name]['type'] = service.spec.type
        retval[service.metadata.name]['cluster_ip'] = service.spec.cluster_ip
        retval[service.metadata.name]['port'] = service.spec.port

        selector_string = selector_string = ','.join([f"{k}={v}" for k, v in service.spec.selector.items()])
        pods = core_api.list_namespaced_pod(namespace, label_selector=selector_string)
        retval[service.metadata.name]['pods'] = [x.metadata.name for x in pods.items]
        for ingress in ingress_list.items:
            for rule in ingress.spec.rules:
                for http_path in rule.http.paths:
                    if http_path.backend.service_name == service.metadata.name:
                        retval[service.metadata.name]['ingress'] = {}
                        retval[service.metadata.name]['ingress'] = {'name': ingress.metadata.name, 
                                                                    'namespace': ingress.metadata.namespace,
                                                                    'host': rule.host,
                                                                    'path': http_path.path}
        
        

        


    return retval