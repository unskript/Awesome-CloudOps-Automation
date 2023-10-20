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
    endpoints: Optional[list] = Field(
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

    context = ssl.create_default_context()
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED

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


def k8s_check_service_status(handle, endpoints:list=[], threshold: int = 30) -> Tuple:
    """
    k8s_check_service_status Checks the health status of the provided endpoints.

    :param endpoints: The URLs of the endpoint whose SSL certificate is to be checked. Eg: ["https://www.google.com", "https://expired.badssl.com/"]
    :param threshold: The number of days within which, if the certificate is set to expire, 
                      is considered a potential issue.
    :return: Tuple with a boolean indicating if all services are healthy, and a list of dictionaries 
             with individual service status.
    """
    # Check if no endpoints are provided
    if not endpoints:
        return False, [{"Error": "No endpoints specified."}]

    status_list = []

    for endpoint in endpoints:
        status_info = {"endpoint": endpoint}
        try:
            response = requests.get(endpoint, verify=True, timeout=5)
            days_remaining, is_healthy = check_ssl_expiry(endpoint, threshold)
            if response.status_code == 200:
                if not is_healthy:
                    status_info["status"] = f'SSL expiring in {days_remaining} days.'
                else:
                    status_info["status"] = 'healthy'
            else:
                status_info["status"] = f'unhealthy. Status code: {response.status_code}'
        except requests.RequestException as e:
            if 'CERTIFICATE_VERIFY_FAILED' in str(e) or 'SSL: CERTIFICATE_VERIFY_FAILED' in str(e):
                status_info["status"] = 'SSL error. Certificate is invalid or not trusted.'
            else:
                status_info["status"] = f'Error: {str(e)}'

        status_list.append(status_info)

    return (all(info["status"] == 'healthy' for info in status_list), status_list)
