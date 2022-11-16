#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
import pprint
from pydantic import BaseModel, Field
from typing import List
from kubernetes import client
from kubernetes.client.rest import ApiException

pp = pprint.PrettyPrinter(indent=2)


class InputSchema(BaseModel):
    node_name: str = Field(
        title='Node',
        description='k8s node name')
    cluster_name: str = Field(
        title='Cluster',
        description='k8s cluster Name')
    provider_id: str = Field(
        title='Node Spec Provider',
        description='k8s node spec provider ID. Eg aws:///us-west-2a/{instance_type}')
    node_info: dict = Field(
        title='Node Info',
        description='Node system info like architecture, boot_id, etc. '
                    'Allowed key names are: '
                    'architecture, '
                    'boot_id, '
                    'container_runtime_version, '
                    'kernel_version, '
                    'kube_proxy_version, '
                    'kubelet_version, '
                    'machine_id, '
                    'operating_system, '
                    'os_image, '
                    'system_uuid.'
    )
    capacity: dict = Field(
        title='Node Capacity',
        description='Node Parameters, like cpu, storage, memory. '
                    'For eg: attachable-volumes-aws-ebs=25 in gb, '
                    'cpu=1 core, memory=7935036Ki, '
                    'ephemeral-storage:104845292Ki, hugepages-1Gi:0, '
                    'hugepages-2Mi:0, pods:29'
    )

def k8s_add_node_to_cluster_printer(output):
    if output is None:
        return
    
    (v1node, data) = output
    if v1node != None:
        pp.pprint("Creating Node {}".format(v1node))
    else:
        pp.pprint("Error Creating Node")
    if data != None:
        pp.pprint("Node Created {}".format(data))
    else:
        pp.pprint("Node Creation Error")
    return data
    

def k8s_add_node_to_cluster(handle, 
                            node_name: str, 
                            cluster_name: str, 
                            provider_id: str, 
                            node_info: dict, 
                            capacity: dict) -> List:


    """k8s_add_node_to_cluster add node to cluster

        :type handle: object
        :param handle: Object returned from the Task validate method

        :type node_name: str
        :param node_name: k8s node name

        :type cluster_name: str
        :param cluster_name: k8s cluster Name

        :type provider_id: str
        :param provider_id: k8s node spec provider ID. Eg aws:///us-west-2a/{instance_type}

        :type node_info: str
        :param node_info: Node system info like architecture, boot_id, etc.

        :type capacity: dict
        :param capacity: Node Parameters, like cpu, storage, memory.


        :rtype: None
    """

    
    print(">>>>>>>>>>")
    coreApiClient = client.CoreV1Api(handle)

    try:
        v1Node = client.V1Node()
        metadata = client.V1ObjectMeta()
        metadata.name = node_name
        metadata.cluster_name = cluster_name
        v1Node.metadata = metadata

        v1NodeSpec = client.V1NodeSpec()
        v1NodeSpec.provider_id = provider_id
        v1Node.spec = v1NodeSpec

        v1NodeStatus = client.V1NodeStatus()
        if capacity:
            v1NodeStatus.capacity = capacity

        if node_info:
            v1NodeSystemInfo = client.V1NodeSystemInfo(architecture=node_info.get("architecture", None),
                                                       boot_id=node_info.get(
                                                           "boot_id", None),
                                                       container_runtime_version=node_info.get(
                                                           "container_runtime_version", None),
                                                       kernel_version=node_info.get(
                                                           "kernel_version", None),
                                                       kube_proxy_version=node_info.get(
                                                           "kube_proxy_version", None),
                                                       kubelet_version=node_info.get(
                                                           "kubelet_version", None),
                                                       machine_id=node_info.get(
                                                           "machine_id", None),
                                                       operating_system=node_info.get(
                                                           "operating_system", None),
                                                       os_image=node_info.get(
                                                           "os_image", None),
                                                       system_uuid=node_info.get("system_uuid", None))
            v1NodeStatus.node_info = v1NodeSystemInfo

        v1Node.status = v1NodeStatus        
        resp = coreApiClient.create_node(body=v1Node, pretty=True)
        return (v1Node, resp)
    except ApiException as e:
        error = 'An Exception occured while executing the command :{}'.format(
            e)
        pp.pprint(error)
        return (None, None)

    return None
