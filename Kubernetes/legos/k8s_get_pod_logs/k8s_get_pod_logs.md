{
"action_title": "Get Kubernetes Logs for a given POD in a Namespace",
"action_description": "Get Kubernetes Logs for a given POD in a Namespace",
"action_type": "LEGO_TYPE_K8S",
"action_entry_function": "k8s_get_pod_logs",
"action_needs_credential": true,
"action_supports_poll": true,
"action_supports_iteration": true,
"action_output_type": "ACTION_OUTPUT_TYPE_STR",
"action_verbs": [
"get"
],
"action_nouns": [
"logs",
"kubernetes",
"pod",
"namespace"
]
}
