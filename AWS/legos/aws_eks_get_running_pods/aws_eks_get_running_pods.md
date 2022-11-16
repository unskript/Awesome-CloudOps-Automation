{
"action_title": " EKS Get Running Pods",
"action_description": " Get a list of running pods from given namespace and EKS cluster name",
"action_type": "LEGO_TYPE_AWS",
"action_entry_function": "aws_eks_get_running_pods",
"action_needs_credential": true,
"action_supports_poll": true,
"action_output_type": "ACTION_OUTPUT_TYPE_LIST",
"action_supports_iteration": true,
"action_verbs": [
"get"
],
"action_nouns": [
"eks",
"pods"
]
}
