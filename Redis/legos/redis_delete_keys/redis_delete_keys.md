{
    "action_title": "Delete Redis Keys",
    "action_description": "Delete Redis keys matching pattern",
    "action_entry_function": "redis_delete_keys",
    "action_type": "LEGO_TYPE_REDIS",
    "action_needs_credential": true,
    "action_output_type": "ACTION_OUTPUT_TYPE_LIST",
    "action_supports_poll": true,
    "action_supports_iteration": true,
    "action_verbs": ["delete"],
    "action_nouns": ["pattern","keys","redis"]
}