##
# Copyright (c) 2024 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Tuple
import base64
import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from kubernetes import client, watch
from kubernetes.client.rest import ApiException
from tabulate import tabulate


class InputSchema(BaseModel):
    namespace: Optional[str] = Field(
        default='',
        title='Namespace',
        description='K8s Namespace. Default- all namespaces')
    expiring_threshold: Optional[int] = Field(
        default=7,
        title='Expiration Threshold (in days)',
        description='Expiration Threshold of certificates (in days). Default- 90 days')


def k8s_get_expiring_tls_secret_certificates_printer(output):
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


def k8s_get_expiring_tls_secret_certificates(handle, namespace:str='', expiring_threshold:int=7) -> Tuple:
    """
    Get the expiring TLS secret certificates for a K8s cluster.

    Args:
        handle: Object of type unSkript K8S Connector
        namespace (str): The Kubernetes namespace where the certificates are stored.
        expiration_threshold (int): The threshold (in days) for considering a certificate as expiring soon.

    Returns:
        tuple: Status, a list of expiring certificate names.
    """
    result = []
    coreApiClient = client.CoreV1Api(api_client=handle)

    try:
        if namespace:
            # Check if namespace exists and has secrets
            secrets = coreApiClient.list_namespaced_secret(namespace, watch=False, limit=1).items
            if not secrets:
                return (True, None)  # No secrets in the namespace
            all_namespaces = [namespace]
        else:
            all_namespaces = [ns.metadata.name for ns in coreApiClient.list_namespace().items]

    except ApiException as e:
        print(f"Error occurred while accessing Kubernetes API: {e}")
        return False, None

    for n in all_namespaces:
        secrets = coreApiClient.list_namespaced_secret(n, watch=False, limit=200).items

        for secret in secrets:
            # Check if the secret contains a certificate
            if secret.type == "kubernetes.io/tls":
                # Get the certificate data
                cert_data = secret.data.get("tls.crt")
                if cert_data:
                    # Decode the certificate data
                    cert_data_decoded = base64.b64decode(cert_data).decode("utf-8")
                    # Parse the certificate expiration date
                    cert_exp = get_expiry_date(cert_data_decoded)
                    days_remaining = (cert_exp - datetime.datetime.now()).days
                    if days_remaining < 0:
                        # Certificate has already expired
                        result.append({
                            "secret_name": secret.metadata.name,
                            "namespace": n,
                            "days_remaining": days_remaining,
                            "status": "Expired"
                        })
                    elif cert_exp and cert_exp < datetime.datetime.now() + datetime.timedelta(days=expiring_threshold):
                        result.append({
                        "secret_name": secret.metadata.name,
                        "namespace": n,
                        "days_remaining": days_remaining,
                        "status": "Expiring Soon"  # Indicating the certificate is close to expiring
                            })

    if len(result) != 0:
        return (False, result)
    return (True, None)
    