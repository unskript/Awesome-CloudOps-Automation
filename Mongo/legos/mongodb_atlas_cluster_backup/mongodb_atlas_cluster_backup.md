{
"action_title": "MongoDB Atlas cluster cloud backup",
"action_description": "Trigger on-demand Atlas cloud backup",
"action_type": "LEGO_TYPE_MONGODB",
"action_entry_function": "mongodb_atlas_cluster_backup",
"action_needs_credential": true,
"action_supports_poll": true,
"action_output_type": "ACTION_OUTPUT_TYPE_DICT",
"action_supports_iteration": true,
"action_verbs": [
"create",
"backup",
"trigger"
],
"action_nouns": [
"mongodb",
"atlas",
"snapshot",
"cluster"
]
}
