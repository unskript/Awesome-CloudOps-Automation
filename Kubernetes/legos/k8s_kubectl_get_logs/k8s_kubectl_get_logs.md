{
"action_title": "Kubectl get logs",
"action_description": "Kubectl get logs for a given pod",
"action_type": "LEGO_TYPE_K8S",
"action_entry_function": "k8s_kubectl_get_logs",
"action_needs_credential": true,
"action_supports_poll": true,
"action_supports_iteration": true,
"action_output_type": "ACTION_OUTPUT_TYPE_STR",
"action_verbs": [
"get"
],
"action_nouns": [
"logs", 
"pod"
]
}
