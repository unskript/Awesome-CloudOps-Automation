from typing import Tuple
import hvac
from pydantic import BaseModel


class InputSchema(BaseModel):
    pass

def vault_get_service_health_printer(output):
    is_healthy, errors = output

    if is_healthy:
        print("Vault Service is Healthy.")
    else:
        print("Vault Service is Unhealthy.")
        if errors:
            print("\nErrors:")
            for error in errors:
                print(f"  - {error}")

def vault_get_service_health(handle) -> Tuple:
    """
    vault_get_service_health fetches the health of the Vault service by using hvac's sys/health call.

    :type handle: object
    :param handle: Handle containing the Vault instance.

    :rtype: Tuple indicating if the service is healthy and an error message (or None if healthy).
    """
    try:
        health_data = handle.sys.read_health_status(method='GET')

        # Health check is successful if Vault is initialized, not in standby, and unsealed
        if health_data["initialized"] and not health_data["standby"] and not health_data["sealed"]:
            return (True, None)
        else:
            error_msg = []
            if not health_data["initialized"]:
                error_msg.append("Vault is not initialized.")
            if health_data["standby"]:
                error_msg.append("Vault is in standby mode.")
            if health_data["sealed"]:
                error_msg.append("Vault is sealed.")
            return (False, error_msg)

    except Exception as e:
        raise e

