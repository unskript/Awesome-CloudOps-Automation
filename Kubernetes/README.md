# Kubernetes RunBooks
* [k8s: Delete Evicted Pods From All Namespaces](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/Delete_Evicted_Pods_From_Namespaces.ipynb): This runbook shows and deletes the evicted pods for given namespace. If the user provides the namespace input, then it only collects pods for the given namespace; otherwise, it will select all pods from all the namespaces.
* [k8s: Get kube system config map](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/Get_Kube_System_Config_Map.ipynb): This runbook fetches the kube system config map for a k8s cluster and publishes the information on a Slack channel.
* [k8s: Get candidate nodes for given configuration](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/K8S_Get_Candidate_Nodes_Given_Config.ipynb): This runbook get the matching nodes for a given configuration (storage, cpu, memory, pod_limit) from a k8s cluster
* [Kubernetes Log Healthcheck](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/K8S_Log_Healthcheck.ipynb): This RunBook checks the logs of every pod in a namespace for warning messages.
* [k8s: Pod Stuck in CrashLoopBackoff State](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/K8S_Pod_Stuck_In_CrashLoopBack_State.ipynb): This runbook checks if any Pod(s) in CrashLoopBackoff state in a given k8s namespace. If it finds, it tries to find out the reason why the Pod(s) is in that state.
* [k8s: Pod Stuck in ImagePullBackOff State](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/K8S_Pod_Stuck_In_ImagePullBackOff_State.ipynb): This runbook checks if any Pod(s) in ImagePullBackOff state in a given k8s namespace. If it finds, it tries to find out the reason why the Pod(s) is in that state.
* [k8s: Pod Stuck in Terminating State](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/K8S_Pod_Stuck_In_Terminating_State.ipynb): This runbook checks any Pods are in terminating state in a given k8s namespace. If it finds, it tries to recover it by resetting finalizers of the pod.
* [k8s: Resize List of PVCs](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/Resize_List_of_PVCs.ipynb): This runbook resizes a list of Kubernetes PVCs.
* [k8s: Resize PVC](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/Resize_PVC.ipynb): This runbook resizes a Kubernetes PVC.
* [Rollback Kubernetes Deployment](https://github.com/unskript/Awesome-CloudOps-Automation/tree/master/Kubernetes/Rollback_k8s_Deployment_and_Update_Jira.ipynb): This runbook can be used to rollback Kubernetes Deployment

# Kubernetes Actions
* [Add Node in a Kubernetes Cluster](/Kubernetes/legos/k8s_add_node_to_cluster/README.md): Add Node in a Kubernetes Cluster
* [Change size of Kubernetes PVC](/Kubernetes/legos/k8s_change_pvc_size/README.md): Change size of Kubernetes PVC
* [Delete a Kubernetes POD in a given Namespace](/Kubernetes/legos/k8s_delete_pod/README.md): Delete a Kubernetes POD in a given Namespace
* [Describe Kubernetes Node](/Kubernetes/legos/k8s_describe_node/README.md): Describe a Kubernetes Node
* [Describe a Kubernetes POD in a given Namespace](/Kubernetes/legos/k8s_describe_pod/README.md): Describe a Kubernetes POD in a given Namespace
* [Execute a command on a Kubernetes POD in a given Namespace](/Kubernetes/legos/k8s_exec_command_on_pod/README.md): Execute a command on a Kubernetes POD in a given Namespace
* [Kubernetes Execute a command on a POD in a given namespace and filter](/Kubernetes/legos/k8s_exec_command_on_pods_and_filter/README.md): Execute a command on Kubernetes POD in a given namespace and filter output
* [Gather Data for POD Troubleshoot](/Kubernetes/legos/k8s_gather_data_for_pod_troubleshoot/README.md): Gather Data for POD Troubleshoot
* [Gather Data for K8S Service Troubleshoot](/Kubernetes/legos/k8s_gather_data_for_service_troubleshoot/README.md): Gather Data for K8S Service Troubleshoot
* [Get All Evicted PODS From Namespace](/Kubernetes/legos/k8s_get_all_evicted_pods_from_namespace/README.md): This action get all evicted PODS from given namespace. If namespace not given it will get all the pods from all namespaces.
* [ Get All Kubernetes PODS with state in a given Namespace](/Kubernetes/legos/k8s_get_all_pods/README.md):  Get All Kubernetes PODS with state in a given Namespace
* [Get candidate k8s nodes for given configuration](/Kubernetes/legos/k8s_get_candidate_nodes_for_pods/README.md): Get candidate k8s nodes for given configuration
* [Get k8s kube system config map](/Kubernetes/legos/k8s_get_config_map_kube_system/README.md): Get k8s kube system config map
* [Get Kubernetes Deployment For a Pod in a Namespace](/Kubernetes/legos/k8s_get_deployment/README.md): Get Kubernetes Deployment for a POD in a Namespace
* [Get Deployment Rollout Status](/Kubernetes/legos/k8s_get_deployment_rollout_status/README.md): This action search for failed deployment rollout status and returns list.
* [Get Deployment Status](/Kubernetes/legos/k8s_get_deployment_status/README.md): This action search for failed deployment status and returns list.
* [Get Kubernetes Failed Deployments](/Kubernetes/legos/k8s_get_failed_deployments/README.md): Get Kubernetes Failed Deployments
* [Get Kubernetes Handle](/Kubernetes/legos/k8s_get_handle/README.md): Get Kubernetes Handle
* [Get All Kubernetes Healthy PODS in a given Namespace](/Kubernetes/legos/k8s_get_healthy_pods/README.md): Get All Kubernetes Healthy PODS in a given Namespace
* [Get Kubernetes Nodes](/Kubernetes/legos/k8s_get_nodes/README.md): Get Kubernetes Nodes
* [Get Kubernetes Nodes that have insufficient resources](/Kubernetes/legos/k8s_get_nodes_with_insufficient_resources/README.md): Get Kubernetes Nodes that have insufficient resources
* [Get Kubernetes POD Configuration](/Kubernetes/legos/k8s_get_pod_config/README.md): Get Kubernetes POD Configuration
* [Get Kubernetes Logs for a given POD in a Namespace](/Kubernetes/legos/k8s_get_pod_logs/README.md): Get Kubernetes Logs for a given POD in a Namespace
* [Get Kubernetes Logs for a list of PODs & Filter in a Namespace](/Kubernetes/legos/k8s_get_pod_logs_and_filter/README.md): Get Kubernetes Logs for a list of PODs and Filter in a Namespace
* [Get Kubernetes Status for a POD in a given Namespace](/Kubernetes/legos/k8s_get_pod_status/README.md): Get Kubernetes Status for a POD in a given Namespace
* [Get pods attached to Kubernetes PVC](/Kubernetes/legos/k8s_get_pods_attached_to_pvc/README.md): Get pods attached to Kubernetes PVC
* [Get all K8s Pods in CrashLoopBackOff State](/Kubernetes/legos/k8s_get_pods_in_crashloopbackoff_state/README.md): Get all K8s pods in CrashLoopBackOff State
* [Get all K8s Pods in ImagePullBackOff State](/Kubernetes/legos/k8s_get_pods_in_imagepullbackoff_state/README.md): Get all K8s pods in ImagePullBackOff State
* [Get Kubernetes PODs in not Running State](/Kubernetes/legos/k8s_get_pods_in_not_running_state/README.md): Get Kubernetes PODs in not Running State
* [Get all K8s Pods in Terminating State](/Kubernetes/legos/k8s_get_pods_in_terminating_state/README.md): Get all K8s pods in Terminating State
* [Get Kubernetes PODS with high restart](/Kubernetes/legos/k8s_get_pods_with_high_restart/README.md): Get Kubernetes PODS with high restart
* [Get K8S Service with no associated endpoints](/Kubernetes/legos/k8s_get_service_with_no_associated_endpoints/README.md): Get K8S Service with no associated endpoints
* [Get Kubernetes Services for a given Namespace](/Kubernetes/legos/k8s_get_services/README.md): Get Kubernetes Services for a given Namespace
* [Get Kubernetes Unbound PVCs](/Kubernetes/legos/k8s_get_unbound_pvcs/README.md): Get Kubernetes Unbound PVCs
* [Kubectl command](/Kubernetes/legos/k8s_kubectl_command/README.md): Execute kubectl command.
* [Kubectl set context entry in kubeconfig](/Kubernetes/legos/k8s_kubectl_config_set_context/README.md): Kubectl set context entry in kubeconfig
* [Kubectl display merged kubeconfig settings](/Kubernetes/legos/k8s_kubectl_config_view/README.md): Kubectl display merged kubeconfig settings
* [Kubectl delete a pod](/Kubernetes/legos/k8s_kubectl_delete_pod/README.md): Kubectl delete a pod
* [Kubectl describe a node](/Kubernetes/legos/k8s_kubectl_describe_node/README.md): Kubectl describe a node
* [Kubectl describe a pod](/Kubernetes/legos/k8s_kubectl_describe_pod/README.md): Kubectl describe a pod
* [Kubectl drain a node](/Kubernetes/legos/k8s_kubectl_drain_node/README.md): Kubectl drain a node
* [Execute command on a pod](/Kubernetes/legos/k8s_kubectl_exec_command/README.md): Execute command on a pod
* [Kubectl get api resources](/Kubernetes/legos/k8s_kubectl_get_api_resources/README.md): Kubectl get api resources
* [Kubectl get logs](/Kubernetes/legos/k8s_kubectl_get_logs/README.md): Kubectl get logs for a given pod
* [Kubectl get services](/Kubernetes/legos/k8s_kubectl_get_service_namespace/README.md): Kubectl get services in a given namespace
* [Kubectl list pods](/Kubernetes/legos/k8s_kubectl_list_pods/README.md): Kubectl list pods in given namespace
* [Kubectl update field](/Kubernetes/legos/k8s_kubectl_patch_pod/README.md): Kubectl update field of a resource using strategic merge patch
* [Kubectl rollout deployment history](/Kubernetes/legos/k8s_kubectl_rollout_deployment/README.md): Kubectl rollout deployment history
* [Kubectl scale deployment](/Kubernetes/legos/k8s_kubectl_scale_deployment/README.md): Kubectl scale a given deployment
* [Kubectl show metrics](/Kubernetes/legos/k8s_kubectl_show_metrics_node/README.md): Kubectl show metrics for a given node
* [Kubectl show metrics](/Kubernetes/legos/k8s_kubectl_show_metrics_pod/README.md): Kubectl show metrics for a given pod
* [List matching name pods](/Kubernetes/legos/k8s_list_all_matching_pods/README.md): List all pods matching a particular name string. The matching string can be a regular expression too
* [List pvcs](/Kubernetes/legos/k8s_list_pvcs/README.md): List pvcs by namespace. By default, it will list all pvcs in all namespaces.
* [Remove POD from Deployment](/Kubernetes/legos/k8s_remove_pod_from_deployment/README.md): Remove POD from Deployment
* [Update Commands in a Kubernetes POD in a given Namespace](/Kubernetes/legos/k8s_update_command_in_pod_spec/README.md): Update Commands in a Kubernetes POD in a given Namespace
