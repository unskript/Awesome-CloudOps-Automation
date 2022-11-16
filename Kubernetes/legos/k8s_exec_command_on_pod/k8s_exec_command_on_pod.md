{
"action_title": "Execute a command on a Kubernetes POD in a given Namespace",
"action_description": "Execute a command on a Kubernetes POD in a given Namespace",
"action_type": "LEGO_TYPE_K8S",
"action_entry_function": "k8s_exec_command_on_pod",
"action_needs_credential": true,
"action_supports_poll": true,
"action_supports_iteration": true,
"action_output_type": "ACTION_OUTPUT_TYPE_STR",
"action_verbs": [
"execute"
],
"action_nouns": [
"command",
"kuberentes",
"pod",
"namespace"
]
}
