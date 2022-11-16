{
"action_title": " EKS Get pod status",
"action_description": " Get a Status of given POD in a given Namespace and EKS cluster name",
"action_type": "LEGO_TYPE_AWS",
"action_entry_function": "aws_eks_get_pod_status",
"action_needs_credential": true,
"action_supports_poll": true,
"action_output_type": "ACTION_OUTPUT_TYPE_DICT",
"action_supports_iteration": true,
"action_verbs": [
"get"
],
"action_nouns": [
"eks",
"pod",
"status"
]
}
