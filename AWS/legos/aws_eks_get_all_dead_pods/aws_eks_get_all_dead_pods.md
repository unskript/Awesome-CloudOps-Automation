{
"action_title": "List of EKS dead pods",
"action_description": "Get list of all dead pods in a given EKS cluster",
"action_type": "LEGO_TYPE_AWS",
"action_entry_function": "aws_eks_get_all_dead_pods",
"action_needs_credential": true,
"action_supports_poll": true,
"action_output_type": "ACTION_OUTPUT_TYPE_LIST",
"action_supports_iteration": true,
"action_verbs": [
"list"
],
"action_nouns": [
"eks",
"pods"
]
}
