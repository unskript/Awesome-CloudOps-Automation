{
"action_title": "Filter AWS Unused Keypairs",
"action_description": "Filter AWS Unused Keypairs",
"action_type": "LEGO_TYPE_AWS",
"action_entry_function": "aws_filter_unused_keypairs",
"action_needs_credential": true,
"action_output_type": "ACTION_OUTPUT_TYPE_LIST",
"action_supports_poll": true,
"action_supports_iteration": true,
"action_verbs": ["filter"],
"action_nouns": [
"aws",
"keypairs"
]
}
  