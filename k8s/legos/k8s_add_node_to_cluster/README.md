[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">](https://unskript.com/assets/favicon.png) 
<h1>Add Node in a Kubernetes Cluster </h1>

## Description
This Lego add Node in a Kubernetes Cluster


## Lego Details

    k8s_add_node_to_cluster(handle, 
                            node_name: str, 
                            cluster_name: str, 
                            provider_id: str, 
                            node_info: dict, 
                            capacity: dict)

        handle: Object of type unSkript K8S Connector
        node_name: k8s node name
        cluster_name: k8s cluster Name
        provider_id:k8s node spec provider ID. Eg aws:///us-west-2a/{instance_type}
        node_info: Node system info like architecture, boot_id, etc.
        capacity: Node Parameters, like cpu, storage, memory.

## Lego Input

This Lego take six inputs handle, node_name, cluster_name, provider_id, node_info and capacity.


## Lego Output
Here is a sample output.
<img src="./1.png">


## See it in Action

You can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)