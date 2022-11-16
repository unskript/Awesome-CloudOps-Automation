{
"action_title": "Restart AWS ECS Service",
"action_description": "Restart an AWS ECS Service",
"action_type": "LEGO_TYPE_AWS",
"action_entry_function": "aws_ecs_service_restart",
"action_needs_credential": true,
"action_supports_poll": true,
"action_output_type": "ACTION_OUTPUT_TYPE_BOOL",
"action_supports_iteration": true,
"action_verbs": ["restart"],
"action_nouns": [
"aws",
"ecs",
"service"
]
}
