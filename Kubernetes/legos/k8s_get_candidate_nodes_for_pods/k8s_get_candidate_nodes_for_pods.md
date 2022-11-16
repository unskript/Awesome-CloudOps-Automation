{
"action_title": "Get candidate k8s nodes for given configuration",
"action_description": "Get candidate k8s nodes for given configuration",
"action_type": "LEGO_TYPE_K8S",
"action_entry_function": "k8s_get_candidate_nodes_for_pods",
"action_needs_credential": true,
"action_supports_poll": true,
"action_output_type": "ACTION_OUTPUT_TYPE_LIST",
"action_supports_iteration": true,
"action_verbs": [
"get"
],
"action_nouns": [
"candidate",
"nodes",
"configuration"
]
}
