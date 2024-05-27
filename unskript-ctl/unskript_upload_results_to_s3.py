import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
import os
from datetime import datetime
import json
from unskript_ctl_factory import UctlLogger

logger = UctlLogger('UnskriptDiagnostics')

class S3Uploader:
    def __init__(self):
        logger.debug("Initializing S3Uploader")
        aws_access_key_id = os.getenv('LIGHTBEAM_AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('LIGHTBEAM_AWS_SECRET_ACCESS_KEY')
        self.bucket_name = 'lightbeam-reports'

        if not aws_access_key_id or not aws_secret_access_key:
            logger.debug("AWS credentials are not set in environment variables")
            return

        self.bucket_name = 'lightbeam-reports'

        try:
            self.s3_client = boto3.client('s3',
                                          aws_access_key_id=aws_access_key_id,
                                          aws_secret_access_key=aws_secret_access_key,
                                          )
            self.s3_client.list_buckets()                       
            logger.debug("AWS credentials are valid")
        except (NoCredentialsError, PartialCredentialsError) as e:
            logger.debug("Invalid AWS credentials")
        except ClientError as e:
            logger.debug(f"Client error: {e}")

    def rename_and_upload(self, customer_name, checks_output):
        now = datetime.now()
        rfc3339_timestamp = now.isoformat() + 'Z'
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")

        file_name = f"{rfc3339_timestamp}.json"
        folder_path = f"{customer_name}/{year}/{month}/{day}/"
        file_path = f"{folder_path}{file_name}"
        local_file_name = f"/tmp/{file_name}"

        try:
            # Convert checks_output to JSON format
            checks_output_json = json.dumps(checks_output, indent=2)
        except json.JSONDecodeError:
            logger.debug(f"Failed to decode JSON response for {customer_name}")
            return

        # Write JSON data to a local file
        try:
            logger.debug(f"Writing JSON data to local file: {local_file_name}")
            with open(local_file_name, 'w') as json_file:
                json_file.write(checks_output_json)
        except IOError as e:
            logger.debug(f"Failed to write JSON data to local file: {e}")
            return

        # Ensure the folder structure exists in the bucket
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=folder_path)
            folder_exists = True
            logger.debug(f"S3 folder {folder_path} exists")
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                folder_exists = False
                logger.debug(f"S3 folder {folder_path} does not exist")
            else:
                logger.debug(f"Error checking folder existence: {e}")

        # Create folder if it doesn't exist
        if not folder_exists:
            logger.debug(f"Creating folder {folder_path} in the bucket")
            try:
                self.s3_client.put_object(Bucket=self.bucket_name, Key=(folder_path))
            except ClientError as e:
                logger.debug(f"Failed to create folder: {e}")

        # Upload the JSON file
        try:
            logger.debug(f"Uploading file {file_name} to {self.bucket_name}/{file_path}")
            self.s3_client.upload_file(local_file_name, self.bucket_name, file_path)
            logger.debug(f"File {file_name} uploaded successfully to {self.bucket_name}/{folder_path}")
        except NoCredentialsError:
            logger.debug("Credentials not available")
        except Exception as e:
            logger.debug(f"Unable to upload failed objetcs file to S3 bucket: {e}")
        # Remove the local file after upload
        logger.debug(f"Removing local file of check outputs json from /tmp: {local_file_name}")
        os.remove(local_file_name)