{
"action_title": "Get list of checkIDs given a name",
"action_description": "Get list of checkIDS given a name. If name is not given, it gives all checkIDs. If transaction is set to true, it returns transaction checkIDs",
"action_type": "LEGO_TYPE_PINGDOM",
"action_entry_function": "pingdom_get_checkids_by_name",
"action_needs_credential": true,
"action_supports_poll": true,
"action_output_type": "ACTION_OUTPUT_TYPE_LIST",
"action_supports_iteration": true,
"action_verbs": [
"get",
"list"
],
"action_nouns": [
"pingdom",
"checks",
"name"
]
}
