##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Tuple
from datetime import datetime, timedelta
from kubernetes import client
import base64
from cryptography import x509
from cryptography.hazmat.backends import default_backend
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
    print(output)

def k8s_get_expiring_certificates(handle, namespace: str = '', expiring_threshold: int = 90) -> Tuple:
    """
    Get the expiring certificates for a K8s cluster.

    Args:
        handle: Object of type unSkript K8S Connector
        namespace (str): The Kubernetes namespace where the certificates are stored.
        expiring_threshold (int): The threshold (in days) for considering a certificate as expiring soon.

    Returns:
        tuple: Status, a list of expiring certificate names.
    """
    result = []
    all_namespaces = [namespace]
    cmd = "kubectl get ns --no-headers -o custom-columns=':metadata.name'"
    if not namespace:
        kubernetes_namespaces = handle.run_native_cmd(cmd)
        replaced_str = kubernetes_namespaces.stdout.replace("\n", " ")
        stripped_str = replaced_str.strip()
        all_namespaces = stripped_str.split(" ")

    coreApiClient = client.CoreV1Api(api_client=handle)
    expiration_threshold = timedelta(days=expiring_threshold)

    for n in all_namespaces:
        secrets = coreApiClient.list_namespaced_secret(n, watch=False, limit=200).items

        for secret in secrets:
            # Check if the secret contains a certificate
            if secret.type == "kubernetes.io/tls":
                # Get the certificate data
                cert_data = secret.data.get("tls.crt")
                if cert_data:
                    # Decode the certificate data
                    cert_data_decoded = base64.b64decode(cert_data)
                    # Parse the certificate expiration date
                    cert = x509.load_pem_x509_certificate(cert_data_decoded, default_backend())
                    cert_exp = cert.not_valid_after
                    if cert_exp and cert_exp < datetime.now() + expiration_threshold:
                        result.append({"secret_name": secret.metadata.name, "namespace": n})
    if len(result) != 0:
        return (False, result)
    return (True, None)