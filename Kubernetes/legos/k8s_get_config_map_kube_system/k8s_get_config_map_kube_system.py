##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
from typing import List

from kubernetes import client
from pydantic import BaseModel, Field
from tabulate import tabulate


class InputSchema(BaseModel):
    namespace: str = Field(
        default='all',
        title='Namespace',
        description='Kubernetes namespace')
    config_map_name: str = Field(
        default="",
        title='Config Map',
        description='Kubernetes Config Map Name')

def k8s_get_config_map_kube_system_printer(output):
    if output is None:
        return 
    
    for config in output:
        data_set_1 = []
        data_set_1.append("Name:")
        data_set_1.append(config.metadata.name)

        data_set_2 = []
        data_set_2.append("Namespace:")
        data_set_2.append(config.metadata.namespace)

        data_set_3 = []
        data_set_3.append("Labels:")
        data_set_3.append(config.metadata.labels)

        data_set_4 = []
        data_set_4.append("Annotations:")
        data_set_4.append(config.metadata.annotations)

        data_set_5 = []
        data_set_5.append("Data:")
        data_set_5.append(config.data)

        tabular_config_map = []
        tabular_config_map.append(data_set_1)
        tabular_config_map.append(data_set_2)
        tabular_config_map.append(data_set_3)
        tabular_config_map.append(data_set_4)
        tabular_config_map.append(data_set_5)

        print(tabulate(tabular_config_map, tablefmt="github"))


def k8s_get_config_map_kube_system(handle, config_map_name: str = '', namespace: str = 'all') -> List:
    """k8s_get_config_map_kube_system get kube system config map

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type config_map_name: str
        :param config_map_name: Kubernetes Config Map Name.

        :type namespace: str
        :param namespace: Kubernetes namespace.

        :rtype: List
    """
    retval = None
    coreApiClient = client.CoreV1Api(api_client=handle)

    res = coreApiClient.list_namespaced_config_map(
        namespace=namespace, pretty=True)
    if len(res.items) > 0:
        if config_map_name:
            config_maps = list(
                filter(lambda x: (x.metadata.name == config_map_name), res.items))
        else:
            config_maps = res.items
        retval = config_maps

    return retval
