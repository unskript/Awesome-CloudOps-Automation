{
"action_title": "Get pod CPU and Memory usage from given namespace",
"action_description": "Get all pod CPU and Memory usage from given namespace",
"action_type": "LEGO_TYPE_AWS",
"action_entry_function": "aws_eks_get_pod_cpu_memory",
"action_needs_credential": true,
"action_supports_poll": true,
"action_output_type": "ACTION_OUTPUT_TYPE_LIST",
"action_supports_iteration": true,
"action_verbs": [
"get"
],
"action_nouns": [
"cpu",
"memory",
"usage",
"namespace"
]
}
