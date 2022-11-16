{
"action_title": "Run a Kafka command using kafka CLI",
"action_description": "Run a Kafka command using kafka CLI. Eg kafka-topics.sh --list --exclude-internal",
"action_type": "LEGO_TYPE_KAFKA",
"action_entry_function": "kafka_run_command",
"action_needs_credential": true,
"action_supports_poll": true,
"action_output_type": "ACTION_OUTPUT_TYPE_STR",
"action_supports_iteration": true,
"action_verbs": [
"run"
],
"action_nouns": [
"kafka",
"command",
"cli"
]
}
