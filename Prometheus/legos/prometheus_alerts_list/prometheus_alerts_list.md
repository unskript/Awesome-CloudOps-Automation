{
"action_title": "Get Prometheus rules",
"action_description": "Get Prometheus rules",
"action_type": "LEGO_TYPE_PROMETHEUS",
"action_entry_function": "prometheus_alerts_list",
"action_needs_credential": true,
"action_supports_poll": true,
"action_output_type": "ACTION_OUTPUT_TYPE_LIST",
"action_supports_iteration": true,
"action_verbs": [
"get"
],
"action_nouns": [
"prometheus",
"alerts",
"rules"
]
}
