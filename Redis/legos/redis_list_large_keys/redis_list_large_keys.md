{
    "action_title": " List Redis Large keys",
    "action_description": "Find Redis Large keys given a size threshold in bytes",
    "action_entry_function": "redis_list_large_keys",
    "action_type": "LEGO_TYPE_REDIS",
    "action_needs_credential": true,
    "action_output_type": "ACTION_OUTPUT_TYPE_DICT",
    "action_supports_poll": true,
    "action_supports_iteration": true,
    "action_verbs": ["list"],
    "action_nouns": ["large","keys","redis"]
}
