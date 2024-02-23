#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from typing import List
from kubernetes import client
from kubernetes.client.rest import ApiException
from tabulate import tabulate 
import time
from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    namespace_to_check_bandwidth: str = Field(description='The namespace where the DaemonSet will be deployed.', title='Namespace')



def pods_have_written_results(handle, core_v1, label_selector, namespace, timeout=150) -> bool:
    """Check if all pods with the given label selector have written their results."""
    end_time = time.time() + timeout
    # Marks the beginning of polling
    time.sleep(5)
    while time.time() < end_time:
        pods = core_v1.list_namespaced_pod(namespace=namespace, label_selector=label_selector).items
        all_written_results = True
        for pod in pods:
            pod_name = pod.metadata.name
            check_files_command = f"kubectl exec -n {namespace} {pod_name} -- ls /results/"
            result = handle.run_native_cmd(check_files_command)

            if "time.txt" in result.stdout:
                continue
            elif "in_progress.txt" in result.stdout:
                all_written_results = False
                break
            else:
                all_written_results = False
                break

        if all_written_results:
            return True
        # Retrying in 2 seconds...
        time.sleep(2)

    return False


def k8s_measure_worker_node_network_bandwidth_printer(output):
    """Print the network bandwidth results in tabular format."""
    if output:
        headers = ["Node", "Bandwidth"]
        table_data = [[entry['Node'], entry['Bandwidth'].replace('Time taken: ', '')] for entry in output]
        table = tabulate(table_data, headers=headers, tablefmt='grid')
        print(table)
    else:
        print("No data available")

def k8s_measure_worker_node_network_bandwidth(handle, namespace_to_check_bandwidth: str) -> List:
    """
     k8s_measure_worker_node_network_bandwidth measures the network bandwidth for each worker node using a DaemonSet and returns the results.

    :type handle: object
    :param handle: Object returned from the Task validate method

    :type namespace: str
    :param namespace: The namespace where the DaemonSet will be deployed.

    :return: List containing node and bandwidth details.
    """

    # DaemonSet spec to run our bandwidth test
    daemonset = {
        "apiVersion": "apps/v1",
        "kind": "DaemonSet",
        "metadata": {"name": "bandwidth-tester"},
        "spec": {
            "selector": {"matchLabels": {"app": "bandwidth-tester"}},
            "template": {
                "metadata": {"labels": {"app": "bandwidth-tester"}},
                "spec": {
                    "containers": [
                        {
                            "name": "tester",
                            "image": "appropriate/curl",
                             "command": [
                                            "sh",
                                            "-c",
                                            ("touch /results/in_progress.txt && "
                                            "start_time=$(date +%s) && "
                                            "curl -O https://speed.hetzner.de/100MB.bin && "
                                            "end_time=$(date +%s) && "
                                            "duration=$((end_time - start_time)) && "
                                            "echo 'Time taken: '$duration' seconds' > /results/time.txt && "
                                            "rm /results/in_progress.txt")
                                        ],
                            "volumeMounts": [{"name": "results", "mountPath": "/results"}],
                        }
                    ],
                    "volumes": [{"name": "results", "emptyDir": {}}],
                },
            },
        },
    }


    v1 = client.AppsV1Api(api_client=handle)
    core_v1 = client.CoreV1Api(api_client=handle)
    try:
        try:
            v1.delete_namespaced_daemon_set(name="bandwidth-tester", namespace=namespace_to_check_bandwidth, 
                                            propagation_policy="Foreground", grace_period_seconds=0)
        except ApiException as ae:
            if ae.status == 404:  # Not Found error
                print(f"Checking for an existing DaemonSet 'bandwidth-tester' in namespace {namespace_to_check_bandwidth}...")
            else:
                raise
        print(f"Deploying DaemonSet 'bandwidth-tester' in namespace {namespace_to_check_bandwidth}...")
        v1.create_namespaced_daemon_set(namespace=namespace_to_check_bandwidth, body=daemonset)

        print("Waiting for DaemonSet to run on all nodes...")
        if not pods_have_written_results(handle, core_v1, "app=bandwidth-tester", namespace_to_check_bandwidth):
            print("Timeout waiting for pods to write results.")
            return []

        # Collect results
        pods = core_v1.list_namespaced_pod(namespace=namespace_to_check_bandwidth, label_selector="app=bandwidth-tester").items
        results = []
        for pod in pods:
            pod_name = pod.metadata.name
            retry_count = 0
            max_retries = 20
            delay_between_retries = 5
            while retry_count < max_retries:
                print(f"Fetching results from pod: {pod_name}, status: {pod.status.phase}")

                if pod.status.phase != "Running":
                    time.sleep(delay_between_retries)
                    retry_count += 1
                    continue

                fetch_results_command = f"kubectl exec -n {namespace_to_check_bandwidth} {pod.metadata.name} -- cat /results/time.txt"
                fetch_output = handle.run_native_cmd(fetch_results_command)

                if fetch_output and not fetch_output.stderr:
                    bandwidth = fetch_output.stdout.strip()
                    results.append({"Node": pod.spec.node_name, "Bandwidth": bandwidth})
                    break
                else:
                    retry_count += 1

                    print(f"Retrying in {delay_between_retries} seconds...")
                    time.sleep(delay_between_retries)

        print("\nCleaning up: Deleting the DaemonSet after collecting results...\n")
        v1.delete_namespaced_daemon_set(name="bandwidth-tester", namespace=namespace_to_check_bandwidth, 
                                        propagation_policy="Foreground", grace_period_seconds=0)

        return results

    except Exception as e:
        print("An error occurred. Performing cleanup...")
        # Cleanup in case of exceptions: Ensure that DaemonSet is deleted
        try:
            v1.delete_namespaced_daemon_set(name="bandwidth-tester", namespace=namespace_to_check_bandwidth, 
                                            propagation_policy="Foreground", grace_period_seconds=0)
        except Exception as cleanup_err:
            print(f"Error during cleanup: {cleanup_err}")
        raise e


