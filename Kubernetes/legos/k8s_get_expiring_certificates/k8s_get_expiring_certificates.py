##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import json 
import base64
import datetime

from pydantic import BaseModel, Field
from typing import Optional, Tuple
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from tabulate import tabulate
from unskript.legos.kubernetes.k8s_kubectl_command.k8s_kubectl_command import k8s_kubectl_command


class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        default='',
        title='Namespace',
        description='K8s Namespace. Default- all namespaces')
    expiring_threshold: Optional[int] = Field(
        default=90,
        title='Expiration Threshold (in days)',
        description='Expiration Threshold of certificates (in days). Default- 90 days')


def k8s_get_expiring_certificates_printer(output):
    if output is None:
        return
    success, data = output
    if not success:
        headers = ['Secret Name', 'Namespace']
        table = [[item['secret_name'], item['namespace']] for item in data]
        print(tabulate(table, headers=headers, tablefmt='grid'))
    else:
        print("No expiring certificates found.")

def get_expiry_date(pem_data: str) -> datetime.datetime:
    cert = x509.load_pem_x509_certificate(pem_data.encode(), default_backend())
    return cert.not_valid_after


def k8s_get_expiring_certificates(handle, namespace:str='', expiring_threshold:int=90) -> Tuple:
    """
    Get the expiring certificates for a K8s cluster.

    Args:
        handle: Object of type unSkript K8S Connector
        namespace (str): The Kubernetes namespace where the certificates are stored.
        expiration_threshold (int): The threshold (in days) for considering a certificate as expiring soon.

    Returns:
        tuple: Status, a list of expiring certificate names.
    """
    result = []

    # If namespace is provided, get secrets from the specified namespace
    if namespace:
        get_secrets_command = f"kubectl get secrets -n {namespace} --field-selector type=kubernetes.io/tls -o=json"
    # If namespace is not provided, get secrets from all namespaces
    else:
        get_secrets_command = "kubectl get secrets --all-namespaces --field-selector type=kubernetes.io/tls -o=json"

    try:
        # Execute the kubectl command to get secret information
        response = handle.run_native_cmd(get_secrets_command)
        secrets_info = json.loads(response.stdout)
    except Exception as e:
        raise Exception(f"Error fetching secret information: {e.stderr}") from e

    for secret_info in secrets_info['items']:
        secret_name = secret_info['metadata']['name']
        namespace = secret_info['metadata'].get('namespace', '')

        # Check if the secret contains a certificate
        cert_data = secret_info['data'].get('tls.crt')
        if cert_data:
            # Decode the certificate data
            cert_data_decoded = base64.b64decode(cert_data).decode("utf-8")
            # Parse the certificate expiration date
            cert_exp = get_expiry_date(cert_data_decoded)
            if cert_exp and cert_exp < datetime.datetime.now() + datetime.timedelta(days=expiring_threshold):
                result.append({"secret_name": secret_name, "namespace": namespace})

    if len(result) != 0:
        return (False, result)

    return (True, None)
    