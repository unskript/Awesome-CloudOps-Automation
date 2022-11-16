{
"action_title": "Kubectl get services",
"action_description": "Kubectl get services in a given namespace",
"action_type": "LEGO_TYPE_K8S",
"action_entry_function": "k8s_kubectl_get_service_namespace",
"action_needs_credential": true,
"action_supports_poll": true,
"action_supports_iteration": true,
"action_output_type": "ACTION_OUTPUT_TYPE_LIST",
"action_verbs": [
"get"
],
"action_nouns": [
"service", 
"namespace" 
]
}
