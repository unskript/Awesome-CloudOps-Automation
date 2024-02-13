##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Tuple, List, Optional
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import ssl
import socket

# Disabling insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class InputSchema(BaseModel):
    endpoints: list = Field(
        ..., description='The URLs of the endpoint whose SSL certificate is to be checked. Eg: ["https://www.google.com", "https://expired.badssl.com/"]', title='List of URLs'
    )
    threshold: Optional[int] = Field(
        30,
        description='The number of days within which, if the certificate is set to expire is considered a potential issue.',
        title='K8s Namespace',
    )
    


def k8s_check_service_status_printer(output):
    status, results = output
    if status:
        print("All services are healthy.")
        return

    if "Error" in results[0]:
        print(f"Error: {results[0]['Error']}")
        return
    print("\n" + "=" * 100) 

    for result in results:
        print(f"Service:\t{result['endpoint']}")
        print("-" * 100)  
        print(f"Status: {result['status']}\n")
        print("=" * 100) 


def check_ssl_expiry(endpoint, threshold):
    hostname = endpoint.split("//")[-1].split("/")[0]
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    # Create an SSL context that restricts to secure versions of TLS
    context = ssl.create_default_context()
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED

    # Ensure that only TLSv1.2 and later are used (disabling TLSv1.0 and TLSv1.1) as TLS versions 1.0 and 1.1 are known to be vulnerable to attacks
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1

    try:
        with socket.create_connection((hostname, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssl_sock:
                ssl_info = ssl_sock.getpeercert()
                
        expiry_date = datetime.strptime(ssl_info['notAfter'], ssl_date_fmt).date()
        days_remaining = (expiry_date - datetime.utcnow().date()).days
        if days_remaining <= threshold:
            return (days_remaining, False)
        else:
            return (days_remaining, True)
    except Exception as e:
        raise e


def k8s_check_service_status(handle, endpoints:list, threshold: int = 30) -> Tuple:
    """
    k8s_check_service_status Checks the health status of the provided endpoints.

    :param endpoints: The URLs of the endpoint whose SSL certificate is to be checked. Eg: ["https://www.google.com", "https://expired.badssl.com/"]
    :param threshold: The number of days within which, if the certificate is set to expire, 
                      is considered a potential issue.
    :return: Tuple with a boolean indicating if all services are healthy, and a list of dictionaries 
             with individual service status.
    """
    failed_endpoints = []

    for endpoint in endpoints:
        status_info = {"endpoint": endpoint}

        # Check if the endpoint is HTTPS or not
        if endpoint.startswith("https://"):
            try:
                response = requests.get(endpoint, verify=True, timeout=5)
                days_remaining, is_healthy = check_ssl_expiry(endpoint, threshold)
                if not (response.status_code == 200 and is_healthy):
                    status_info["status"] = 'unhealthy'
                    reason = f'SSL expiring in {days_remaining} days.' if not is_healthy else f'Status code: {response.status_code}'
                    status_info["Reason"] = reason
                    failed_endpoints.append(status_info)
            except requests.RequestException as e:
                status_info["status"] = 'unhealthy'
                reason = f'SSL error: {str(e)}' if 'CERTIFICATE_VERIFY_FAILED' in str(e) else f'Error: {str(e)}'
                status_info["Reason"] = reason
                failed_endpoints.append(status_info)
        else:
            # For non-HTTPS endpoints
            try:
                response = requests.get(endpoint, timeout=5)
                if response.status_code != 200:
                    status_info["status"] = 'unhealthy'
                    status_info["Reason"] = f'Status code: {response.status_code}'
                    failed_endpoints.append(status_info)
            except requests.RequestException as e:
                status_info["status"] = 'unhealthy'
                status_info["Reason"] = f'Error: {str(e)}'
                failed_endpoints.append(status_info)

    if failed_endpoints:
        return (False, failed_endpoints)
    else:
        return (True, None)
