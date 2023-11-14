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


def k8s_check_cronjob_pod_status(handle, namespace: str = '') -> Tuple:
    """
    Checks the status of the CronJob pods.

    :type handle: Object
    :param handle: Object returned from the task.validate(...) function

    :type name: str
    :param namespace: Namespace where the CronJob is deployed.

    :return: A tuple where the first item has the status if the check and second has a list of failed objects.
    """
    issues = {"NotAssociated": [], "Pending": [], "UnexpectedState": []}

    # Get namespaces to check
    if namespace:
        namespaces = [namespace]
    else:
        get_namespace_command = "kubectl get namespaces -o=jsonpath='{.items[*].metadata.name}'"
        response = handle.run_native_cmd(get_namespace_command)

        if response.returncode != 0:
            raise Exception(f"Error fetching namespaces: {response.stderr}")

        namespaces = response.stdout.split()

    for ns in namespaces:
        # Fetch all CronJobs in the namespace using kubectl
        get_cronjob_command = f"kubectl get cronjobs -n {ns} " + "-o=jsonpath={.items[*].metadata.name}"
        response = handle.run_native_cmd(get_cronjob_command)
        
        if response.returncode != 0:
            raise Exception(f"Error fetching CronJobs for namespace {ns}: {response.stderr}")

        cronjob_names = response.stdout.split()
        for cronjob_name in cronjob_names:
            get_cronjob_details_command = f"kubectl get cronjob {cronjob_name} -n {ns} -o=json"
            try:
                response = handle.run_native_cmd(get_cronjob_details_command)

                if response.returncode != 0:
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
            get_jobs_command = f"kubectl get jobs -n {ns}" + " -o=json | jq -r '.items[] | select(.metadata.name ) | .metadata.name'"
            response = handle.run_native_cmd(get_jobs_command)

            if response.returncode != 0:
                raise Exception(f"Error fetching jobs for CronJob {cronjob_name} in namespace {ns}: {response.stderr}")

            job_names = response.stdout.split()
            if not job_names:
                issues["NotAssociated"].append({"cronjob_name": cronjob_name, "namespace": ns})
                continue

            latest_job_name = sorted(job_names, key=None, reverse=True)[0]
            

            # Check job's pods for any issues
            get_pods_command = f"kubectl get pods -n {ns} --selector=job-name={latest_job_name} -o=jsonpath={{.items[*].metadata.name}}"
            response = handle.run_native_cmd(get_pods_command)
            if response.returncode != 0:
                raise Exception(f"Error fetching pods for Job {latest_job_name} in namespace {ns}: {response.stderr}")

            pod_names = response.stdout.split()
            if not pod_names:
                issues["NotAssociated"].append({"cronjob_name": cronjob_name, "namespace": ns})
                continue

            for pod_name in pod_names:
                get_pod_status_command = f"kubectl get pod {pod_name} -n {ns} -o=jsonpath={{.status.phase}}"
                response = handle.run_native_cmd(get_pod_status_command)

                if response.returncode != 0:
                    raise Exception(f"Error fetching status for Pod {pod_name} in namespace {ns}: {response.stderr}")

                pod_status = response.stdout.strip()

                if pod_status == 'Pending' and now - datetime.strptime(response.stderr, "%Y-%m-%dT%H:%M:%S%z") > time_to_next_run:
                    issues["Pending"].append({"pod_name": pod_name, "namespace": ns})
                elif pod_status not in ['Running', 'Succeeded']:
                    issues["UnexpectedState"].append({"pod_name": pod_name, "namespace": ns, "state": pod_status})

    if all(not val for val in issues.values()):
        return True, None
    else:
        return False, issues
