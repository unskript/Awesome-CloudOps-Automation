{
    "action_title": "Get AWS EMR Instances",
    "action_description": "Get a list of EC2 Instances for an EMR cluster. Filtered by node type (MASTER|CORE|TASK)",
    "action_type": "LEGO_TYPE_AWS",
    "action_entry_function": "aws_emr_get_instances",
    "action_needs_credential": true,
    "action_supports_poll": true,
    "action_output_type": "ACTION_OUTPUT_TYPE_LIST",
    "action_supports_iteration": true,
    "action_verbs": [
        "get"
    ],
    "action_nouns": [
        "aws",
        "emr",
        "instances"
    ]
}
