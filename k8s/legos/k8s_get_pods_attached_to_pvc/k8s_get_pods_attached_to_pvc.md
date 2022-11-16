{
"action_title": "Get pods attached to Kubernetes PVC",
"action_description": "Get pods attached to Kubernetes PVC",
"action_type": "LEGO_TYPE_K8S",
"action_entry_function": "k8s_get_pods_attached_to_pvc",
"action_needs_credential": true,
"action_supports_poll": true,
"action_supports_iteration": true,
"action_output_type": "ACTION_OUTPUT_TYPE_STR",
"action_verbs": [
"attached",
"mount",
"using"
],
"action_nouns": [
"pvc",
"kubernetes",
"pod",
"claims"
]
}
