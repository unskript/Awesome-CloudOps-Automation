"""
Enhanced Email Notification System using Microsoft Graph API and HashiCorp Vault
"""

import os
import requests
import json
import base64
import logging
from typing import Optional, Dict, Any, Union
from pathlib import Path
from tenacity import retry, stop_after_attempt, wait_exponential
from urllib3.exceptions import InsecureRequestWarning
from dataclasses import dataclass

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Constants
DEFAULT_EMAIL_TEMPLATE = """
<html>
    <body>
        <h1>Hello!</h1>
        <p>This is a <b>test email</b> sent using <i>Microsoft Graph API</i> with HTML content and an attachment.</p>
        <p>Have a great day!</p>
    </body>
</html>
"""

GRAPH_API_BASE_URL = "https://graph.microsoft.com/v1.0"
OAUTH_TOKEN_URL = "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

@dataclass
class VaultConfig:
    """Configuration for HashiCorp Vault"""
    addr: str
    token: str
    path: str = "lb-secrets/smtp-server/credentials/smtp"
    verify_ssl: bool = True

class EmailNotificationError(Exception):
    """Base exception for email notification errors"""
    pass

class VaultError(EmailNotificationError):
    """Exception for Vault-related errors"""
    pass

class AuthenticationError(EmailNotificationError):
    """Exception for authentication-related errors"""
    pass

class EmailSendError(EmailNotificationError):
    """Exception for email sending failures"""
    pass

class CustomEmailNotification:
    """
    A system for sending emails using Microsoft Graph API with Vault integration
    """
    
    def __init__(
        self,
        vault_config: VaultConfig,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize the email notification system.
        
        Args:
            vault_config: VaultConfig object containing Vault settings
            logger: Optional logger instance
        """
        self.vault_config = vault_config
        self.logger = logger or logging.getLogger(__name__)
        self.credentials = self._fetch_vault_secret()

    def _fetch_vault_secret(self) -> Dict[str, Any]:
        """
        Fetch secrets from HashiCorp Vault.
        
        Returns:
            Dict containing the secret data
            
        Raises:
            VaultError: If secret fetching fails
        """
        headers = {"X-Vault-Token": self.vault_config.token}
        url = f"{self.vault_config.addr}/v1/{self.vault_config.path}"

        try:
            self.logger.debug(f"Fetching secret from Vault at path: {self.vault_config.path}")
            response = requests.get(
                url,
                headers=headers,
                verify=self.vault_config.verify_ssl,
                timeout=10
            )
            response.raise_for_status()
            
            secret_data = response.json().get("data", {}).get("value")
            if not secret_data:
                raise VaultError("No secret found at the specified path")
            
            return json.loads(secret_data)
            
        except requests.exceptions.RequestException as e:
            raise VaultError(f"Failed to fetch secret from Vault: {str(e)}")
        except json.JSONDecodeError as e:
            raise VaultError(f"Failed to parse secret data: {str(e)}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry_error_callback=lambda retry_state: None
    )
    def _get_access_token(self) -> str:
        """
        Get OAuth2 token from Microsoft Graph API.
        
        Returns:
            str: Access token
            
        Raises:
            AuthenticationError: If token acquisition fails
        """
        try:
            url = OAUTH_TOKEN_URL.format(
                tenant_id=self.credentials["credentials"]["tenantId"]
            )
            
            data = {
                "grant_type": "client_credentials",
                "client_id": self.credentials["credentials"]["clientId"],
                "client_secret": self.credentials["credentials"]["clientSecret"],
                "scope": self.credentials["credentials"]["scope"]
            }
            
            response = requests.post(
                url,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=data,
                timeout=10
            )
            response.raise_for_status()
            
            return response.json()["access_token"]
            
        except requests.exceptions.RequestException as e:
            raise AuthenticationError(f"Failed to obtain access token: {str(e)}")

    def _create_attachment(self, file_path: Union[str, Path]) -> Dict[str, str]:
        """
        Create file attachment payload.
        
        Args:
            file_path: Path to the file to attach
            
        Returns:
            Dict containing the attachment data
            
        Raises:
            ValueError: If file operations fail
        """
        path = Path(file_path)
        if not path.exists():
            raise ValueError(f"File not found: {file_path}")
        if not path.is_file():
            raise ValueError(f"Not a file: {file_path}")

        try:
            with path.open("rb") as file:
                file_content = file.read()
                encoded_content = base64.b64encode(file_content).decode("utf-8")
                
                return {
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": path.name,
                    "contentType": "application/octet-stream",
                    "contentBytes": encoded_content
                }
        except Exception as e:
            raise ValueError(f"Failed to create attachment: {str(e)}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry_error_callback=lambda retry_state: False
    )
    def send_email(
        self,
        recipient_email: str,
        subject: str,
        email_content: Optional[str] = None,
        file_path: Optional[Union[str, Path]] = None
    ) -> bool:
        """
        Send email using Microsoft Graph API.
        
        Args:
            recipient_email: Email address of the recipient
            subject: Email subject
            email_content: HTML content of the email (optional)
            file_path: Path to attachment file (optional)
            
        Returns:
            bool: True if email was sent successfully
            
        Raises:
            EmailSendError: If email sending fails
            ValueError: If input validation fails
        """
        # Get fresh access token
        access_token = self._get_access_token()

        email_data = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "HTML",
                    "content": email_content or DEFAULT_EMAIL_TEMPLATE
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": recipient_email
                        }
                    }
                ]
            }
        }

        # Add attachment if provided
        if file_path:
            attachment = self._create_attachment(file_path)
            email_data["message"]["attachments"] = [attachment]

        url = f"{GRAPH_API_BASE_URL}/users/{self.credentials['credentials']['smtpSender']}/sendMail"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=email_data,
                timeout=30
            )
            response.raise_for_status()
            
            if response.status_code == 202:
                self.logger.info("Email sent successfully!")
                return True
            else:
                raise EmailSendError(f"Unexpected status code: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to send email: {str(e)}")
            raise EmailSendError(f"Email sending failed: {str(e)}")

def setup_logger(log_level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with the specified log level.
    
    Args:
        log_level: Logging level (default: logging.INFO)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger("email_notification_system")
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)
    return logger

def custom_email_notification_main(_logger,
         email_subject,
         email_content,
         email_recipient,
         file_path = None):
    """Main entry point for the email notification system."""
    retval = False
    # Get environment variables
    vault_addr = os.getenv("VAULT_ADDR")
    vault_token = os.getenv("VAULT_TOKEN")
    
    # Setup logging
    if _logger:
        logger = _logger
    else:
        logger = setup_logger()
    
    if not vault_addr or not vault_token:
        logger.error(
            "VAULT_ADDR and VAULT_TOKEN environment variables must be set."
        )
        return retval

    
    # Initialize Vault configuration
    vault_config = VaultConfig(
        addr=vault_addr,
        token=vault_token,
        verify_ssl=False 
    )
    
    try:
        # Initialize the email notification system
        email_system = CustomEmailNotification(vault_config, logger)
        
        # Example usage
        success = email_system.send_email(
            recipient_email=email_recipient,
            subject=email_subject,
            email_content=email_content,
            file_path=file_path
        )
        
        if success:
            logger.info("Email notification sent successfully")
            retval = True
        else:
            logger.error("Failed to send email notification")
            
    except EmailNotificationError as e:
        logger.error(f"Email notification error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

    return retval