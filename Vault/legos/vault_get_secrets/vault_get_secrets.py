from typing import Tuple, Optional
import hvac
from pydantic import BaseModel, Field

class InputSchema(BaseModel):
    paths: list = Field(
        title='List of paths',
        description='List of paths'),
    mount_point: str = Field(
        title= 'Mount point of secrets',
        description= 'Mount point of secrets'
    )

def vault_get_secrets_printer(output):
    """
    Prints the secrets fetched from Vault in a readable format.

    :param secrets: A dictionary with paths as keys and their corresponding secrets.
    """
    if output:
        print("Fetched secrets from Vault:")
        for path, secret in output.items():
            print(f"\nPath: {path}")
            for key, value in secret.items():
                print(f"  - {key}: {value}")
    else:
        print("No secrets fetched or Vault contains no secrets.")

def vault_get_secrets(handle, paths: list, mount_point:str):
    """
    Fetches secrets from the specified paths in Vault.

    :type handle: hvac.Client
    :param handle: Handle containing the Vault instance.

    :type paths: Optional[List[str]]
    :param paths: Optional list of paths to fetch the secrets from. Fetches all if None.

    :rtype: Dict containing the paths as keys and the fetched secrets as values.
    """
    secrets = {}

    for path in paths:
        # Trim any wildcard or file indicators from the path for the API call
        clean_path = path.replace(mount_point, "").rstrip("/*")
        try:
            # Attempt to list secrets in the path if it's a directory
            list_response = handle.secrets.kv.v2.list_secrets(mount_point=mount_point, path=clean_path)
            if 'keys' in list_response['data']:
                for key in list_response['data']['keys']:
                    secret_path = f"{clean_path}/{key}".rstrip("/")
                    read_response = handle.secrets.kv.read_secret_version(path=secret_path, mount_point=mount_point)
                    secrets[f"{mount_point}{secret_path}"] = read_response['data']['data']
        except hvac.exceptions.InvalidPath:
            # If the path is not a directory, try to read it directly as a secret
            try:
                read_response = handle.secrets.kv.read_secret_version(path=clean_path, mount_point=mount_point)
                secrets[f"{mount_point}{clean_path}"] = read_response['data']['data']
            except Exception as e:
                print(f"Error fetching secret from {mount_point}{clean_path}: {e}")
        except Exception as e:
            print(f"Error processing path {mount_point}{clean_path}: {e}")

    return secrets