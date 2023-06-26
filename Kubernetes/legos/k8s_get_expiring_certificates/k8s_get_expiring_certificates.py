##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Tuple
import base64
from kubernetes import client
from kubernetes.client.rest import ApiException
from datetime import datetime, timedelta
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
    all_namespaces = [namespace]
    cmd = "kubectl get ns  --no-headers -o custom-columns=':metadata.name'"
    if namespace is None or len(namespace)==0:
        kubernetes_namespaces = k8s_kubectl_command(handle=handle,kubectl_command=cmd )
        replaced_str = kubernetes_namespaces.replace("\n"," ")
        stripped_str = replaced_str.strip()
        all_namespaces = stripped_str.split(" ")
    coreApiClient = client.CoreV1Api(api_client=handle)
    for n in all_namespaces:
        coreApiClient.read_namespace_status(n, pretty=True)
        secret = coreApiClient.list_namespaced_secret(n).items
        expiration_threshold = timedelta(days=expiring_threshold)
        # Check if the secret contains a certificate
        if secret[0].type == "kubernetes.io/tls":
            # Get the certificate data
            cert_data = secret[0].data.get("tls.crt")
            if cert_data:
                # Decode the certificate data
                cert_data_decoded = base64.b64decode(cert_data).decode("utf-8")
                # Parse the certificate expiration date
                cert_exp = None
                try:
                    cert_exp = datetime.strptime(cert_data_decoded.split("-----END CERTIFICATE-----")[0].split("Not After : ")[-1].strip(), "%b %d %H:%M:%S %Y %Z")
                except ValueError:
                    pass
                if cert_exp and cert_exp < datetime.now() + expiration_threshold:
                    result.append({"secret_name": secret[0].metadata.name, "namespace": n})
    if len(result) != 0:
        return (False, result)
    return (True, None)