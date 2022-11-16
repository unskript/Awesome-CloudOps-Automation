{
"action_title": "Filter AWS EBS Unattached volumes",
"action_description": "Filter AWS EBS Unattached volumes",
"action_type": "LEGO_TYPE_AWS",
"action_entry_function": "aws_filter_ebs_unattached_volumes",
"action_needs_credential": true,
"action_supports_poll": true,
"action_output_type": "ACTION_OUTPUT_TYPE_LIST",
"action_supports_iteration": true,
"action_verbs": ["filter"],
"action_nouns": [
"aws",
"ebs",
"volumes"
]
}
