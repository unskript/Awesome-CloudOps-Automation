{
"action_title": "Filter AWS Untagged EC2 Instances",
"action_description": "Filter AWS Untagged EC2 Instances",
"action_type": "LEGO_TYPE_AWS",
"action_entry_function": "aws_filter_untagged_ec2_instances",
"action_needs_credential": true,
"action_supports_poll": true,
"action_output_type": "ACTION_OUTPUT_TYPE_LIST",
"action_supports_iteration": true,
"action_verbs": ["filter"],
"action_nouns": [
"aws",
"ec2",
"instances",
"untagged"
]
}