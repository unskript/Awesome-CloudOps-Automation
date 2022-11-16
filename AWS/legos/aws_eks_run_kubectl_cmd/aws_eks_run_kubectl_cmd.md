{
"action_title": " Run Kubectl commands on EKS Cluster",
"action_description": "This action runs a kubectl command on an AWS EKS Cluster",
"action_type": "LEGO_TYPE_AWS",
"action_entry_function": "aws_eks_run_kubectl_cmd",
"action_needs_credential": true,
"action_supports_poll": true,
"action_output_type": "ACTION_OUTPUT_TYPE_STR",
"action_supports_iteration": true,
"action_verbs": [
"run"
],
"action_nouns": [
"kubectl",
"commands",
"eks",
"cluster"
]
}
