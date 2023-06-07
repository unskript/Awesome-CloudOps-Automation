import json
import sys

def check_json(file_path):
    with open(file_path) as file:
        data = json.load(file)

        # Check if "action_output_type" is set to "ACTION_OUTPUT_TYPE_LIST"
        if data.get("action_output_type") != "ACTION_OUTPUT_TYPE_LIST":
            print("Error: 'action_output_type' should be set to 'ACTION_OUTPUT_TYPE_LIST'")
            return False

        # Check if "action_next_hop" is set and not empty
        if not data.get("action_next_hop"):
            print("Error: 'action_next_hop' should be set and not empty")
            return False

        # Check if "action_next_hop_parameter_mapping" is set and not empty
        if not data.get("action_next_hop_parameter_mapping"):
            print("Error: 'action_next_hop_parameter_mapping' should be set and not empty")
            return False

        return True

# Provide the path to the JSON file
file_path = "/Users/shlokabhalgat/Awesome-CloudOps-Automation/AWS/legos/aws_get_long_running_redshift_clusters_without_reserved_nodes/aws_get_long_running_redshift_clusters_without_reserved_nodes.json"

# Call the function to check the JSON file
if check_json(file_path):
    print("JSON file passed all checks.")
    sys.exit(0)
else:
    print("JSON file failed the checks.")
    sys.exit(-1)

