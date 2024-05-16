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

        self.bucket_name = 'lightbeam-reports'

        try:
            self.s3_client = boto3.client('s3',
                                          aws_access_key_id=aws_access_key_id,
                                          aws_secret_access_key=aws_secret_access_key,
                                          )
        except (NoCredentialsError, PartialCredentialsError) as e:
            logger.debug("Invalid AWS credentials")
            pass
        except ClientError as e:
            logger.debug(f"Client error: {e}")
            pass

    def rename_and_upload(self, customer_name, checks_output):
        today_date = datetime.now().strftime("%m_%d_%y")
        file_name = f"{customer_name}_{today_date}.json"
        folder_name = today_date
        file_path = f"{folder_name}/{file_name}"

        try:
            # Convert checks_output to JSON format
            checks_output_json = json.dumps(checks_output, indent=2)
        except json.JSONDecodeError:
            logger.debug(f"Failed to decode JSON response for {customer_name}")

        # Write JSON data to a local file
        local_file_name = f"/tmp/{file_name}"
        with open(local_file_name, 'w') as json_file:
            json_file.write(checks_output_json)

        # Check if the folder already exists in the bucket
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=f"{folder_name}/")
            folder_exists = True
        except:
            folder_exists = False
            logger.debug(f"S3 folder {folder_name} does not exist")

        # Create folder if it doesn't exist
        if not folder_exists:
            # logger.debug(f"Creating folder {folder_name} in the bucket")
            self.s3_client.put_object(Bucket=self.bucket_name, Key=(folder_name+'/'))

        # Upload the JSON file
        try:
            logger.debug(f"Uploading file {file_name} to {self.bucket_name}/{file_path}")
            self.s3_client.upload_file(local_file_name, self.bucket_name, file_path)
            logger.debug(f"File {file_name} uploaded successfully to {self.bucket_name}/{folder_name}")
        except NoCredentialsError:
            logger.debug("Credentials not available")
        except Exception as e:
            logger.debug(f"Unable to upload failed objetcs file to S3 bucket: {e}")
        # Remove the local file after upload
        # logger.debug(f"Removing local file of check outputs json from /tmp: {local_file_name}")
        os.remove(local_file_name)