{
"action_title": "Datadog mute/unmute monitors",
"action_description": "Mute/unmute monitors",
"action_type": "LEGO_TYPE_DATADOG",
"action_entry_function": "datadog_mute_or_unmute_alerts",
"action_needs_credential": true,
"action_supports_poll": true,
"action_output_type": "ACTION_OUTPUT_TYPE_STR",
"action_supports_iteration": true,
"action_verbs": [
"mute",
"unmute",
"pause",
"unpause"
],
"action_nouns": [
"monitor",
"datadog"
]
}
