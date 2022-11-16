{
"action_title": "Delete AWS Volume by Id",
"action_description": "Delete AWS volumes by using Volume Id",
"action_type": "LEGO_TYPE_AWS",
"action_entry_function": "aws_delete_volumes",
"action_needs_credential": true,
"action_supports_poll": true,
"action_output_type": "ACTION_OUTPUT_TYPE_LIST",
"action_supports_iteration": true,
"action_verbs": ["delete"],
"action_nouns": [
"aws",
"volumes"
]
}
