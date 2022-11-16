{
  "action_title": "List pvcs",
  "action_description": "List pvcs by namespace. By default, it will list all pvcs in all namespaces.",
  "action_type": "LEGO_TYPE_K8S",
  "action_version": "2.0.0",
  "action_entry_function": "k8s_list_pvcs",
  "action_needs_credential": true,
  "action_supports_poll": true,
  "action_supports_iteration": true,
  "action_output_type": "ACTION_OUTPUT_TYPE_LIST",
  "action_verbs": [
    "list"
  ],
  "action_nouns": [
    "pvc"
  ]
}
