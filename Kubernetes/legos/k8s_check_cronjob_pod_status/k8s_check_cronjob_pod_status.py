#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
from datetime import datetime, timezone
from kubernetes import client
from typing import Tuple, Optional
from pydantic import BaseModel, Field
from croniter import croniter
import json


class InputSchema(BaseModel):
    namespace: Optional[str] = Field(..., description='k8s Namespace', title='Namespace')


def k8s_check_cronjob_pod_status_printer(output):
    status, issues = output
    if status:
        print("CronJobs are running as expected.")
    else:
        for issue in issues:
            print(f"CronJob '{issue['cronjob_name']}' Alert: {issue['message']}")


def k8s_check_cronjob_pod_status(handle, namespace: str='') -> Tuple:
    """
    Checks the status of the CronJob pods.

    :type handle: object
    :param handle: The Kubernetes client handle.

    :type name: str
    :param namespace: Namespace where the CronJob is deployed.

    :return: A tuple where the first item has the status if the check and second has a list of failed objects.
    """
    # Initialize the K8s API clients
    batch_v1 = client.BatchV1Api(api_client=handle)
    core_v1 = client.CoreV1Api(api_client=handle)

    issues = {"NotAssociated": [], "Pending": [], "UnexpectedState": []}

    # Get namespaces to check
    if namespace:
        namespaces = [namespace]
    else:
        ns_obj = core_v1.list_namespace()
        namespaces = [ns.metadata.name for ns in ns_obj.items]

    for ns in namespaces:
        # Fetch all CronJobs in the namespace using kubectl
        get_cronjob_command = f"kubectl get cronjobs -n {ns} -o=jsonpath='{{.items[*].metadata.name}}'"
        response = handle.run_native_cmd(get_cronjob_command)

        if not response or response.stderr:
            raise Exception(f"Error fetching CronJobs for namespace {ns}: {response.stderr if response else 'empty response'}")

        cronjob_names = response.stdout.split()
        for cronjob_name in cronjob_names:
            get_cronjob_details_command = f"kubectl get cronjob {cronjob_name} -n {ns} -o=json"
            try:
                response = handle.run_native_cmd(get_cronjob_details_command)
                if response.stderr:
                    raise Exception(f"Error fetching details for CronJob {cronjob_name} in namespace {ns}: {response.stderr}")
            except Exception as e:
                print(f"Failed to fetch details for CronJob {cronjob_name} in namespace {ns}: {str(e)}")
                continue
            cronjob = json.loads(response.stdout)

            schedule = cronjob['spec']['schedule']

            # Calculate the next expected run
            now = datetime.now(timezone.utc)
            iter = croniter(schedule, now)
            next_run = iter.get_next(datetime)
            time_to_next_run = next_run - now

            # Fetch the most recent Job associated with the CronJob
            jobs = batch_v1.list_namespaced_job(ns)  # Fetch all jobs, and then filter by prefix.

            associated_jobs = [job for job in jobs.items if job.metadata.name.startswith(cronjob['metadata']['name'])]
            if not associated_jobs:
                # If no associated jobs, that means the job is not scheduled.
                return (True, None)

            latest_job = sorted(associated_jobs, key=lambda x: x.status.start_time, reverse=True)[0]

            # Check job's pods for any issues
            pods = core_v1.list_namespaced_pod(ns, label_selector=f"job-name={latest_job.metadata.name}")

            for pod in pods.items:
                if pod.status.phase == 'Pending' and now - pod.status.start_time > time_to_next_run:
                    issues["Pending"].append({"pod_name": pod.metadata.name, "namespace": ns})
                elif pod.status.phase not in ['Running', 'Succeeded']:
                    issues["UnexpectedState"].append({"pod_name": pod.metadata.name, "namespace": ns, "state": pod.status.phase})

    if all(not val for val in issues.values()):
        return (True, None)
    else:
        return (False, issues)