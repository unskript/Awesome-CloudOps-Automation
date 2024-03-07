##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
from pydantic import BaseModel, Field
from typing import Optional, Tuple
import base64
import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend


class InputSchema(BaseModel):
    expiring_threshold: Optional[int] = Field(
        default=7,
        title='Expiration Threshold (in days)',
        description='Expiration Threshold of certificates (in days). Default- 90 days')

def k8s_get_expiring_cluster_certificate_printer(output):
    if output is None:
        return
    success, data = output
    if not success:
        print(data)
    else:
        print("K8s certificate is valid.")

def get_expiry_date(pem_data: str) -> datetime.datetime:
    cert = x509.load_pem_x509_certificate(pem_data.encode(), default_backend())
    return cert.not_valid_after

def k8s_get_expiring_cluster_certificate(handle, expiring_threshold:int=7) -> Tuple:
    """
    Check the validity for a K8s cluster certificate.

    Args:
        handle: Object of type unSkript K8S Connector
        expiration_threshold (int): The threshold (in days) for considering a certificate as expiring soon.

    Returns:
        tuple: Status, details of the certificate.
    """
    result = []
    try:
        # Fetch cluster CA certificate
        ca_cert = handle.run_native_cmd("kubectl get secret -o jsonpath=\"{.items[?(@.type=='kubernetes.io/service-account-token')].data['ca\\.crt']}\" --all-namespaces")
        if ca_cert.stderr:
            raise Exception(f"Error occurred while fetching cluster CA certificate: {ca_cert.stderr}")

        # Decode and check expiry date of the cluster's CA certificate
        ca_cert_decoded = base64.b64decode(ca_cert.stdout.strip()).decode("utf-8")
        ca_cert_exp = get_expiry_date(ca_cert_decoded)
        days_remaining = (ca_cert_exp - datetime.datetime.now()).days
        if days_remaining < 0:
            # Certificate has already expired
            result.append({
                "certificate": "Kubeconfig Cluster certificate",
                "days_remaining": days_remaining,
                "status": "Expired"
            })
        elif ca_cert_exp < datetime.datetime.now() + datetime.timedelta(days=expiring_threshold):
            result.append({
                "certificate": "Kubeconfig Cluster certificate",
                "days_remaining": days_remaining,
                "status": "Expiring Soon"
            })
    except Exception as e:
        print(f"Error occurred while checking cluster CA certificate: {e}")
        raise e
    
    if len(result) != 0:
        return (False, result)
    return (True, None)
