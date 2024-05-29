import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
import os
from datetime import datetime
import json
from unskript_ctl_factory import UctlLogger
from unskript_utils import *

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
        self.uglobals = UnskriptGlobals()

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

        # Initialize folder_exists
        folder_exists = False
        
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
                self.s3_client.put_object(Bucket=self.bucket_name, Key=folder_path)
            except ClientError as e:
                logger.debug(f"Failed to create folder: {e}")

        # Upload the files in the CURRENT_EXECUTION_RUN_DIRECTORY 
        file_list_to_upload = [local_file_name]
        if self.uglobals.get('CURRENT_EXECUTION_RUN_DIRECTORY') and \
            os.path.exists(self.uglobals.get('CURRENT_EXECUTION_RUN_DIRECTORY')):
            try:
                for parent_dir, _, _files in os.walk(self.uglobals.get('CURRENT_EXECUTION_RUN_DIRECTORY')):
                    # Currently there is no need to read the sub_directories (child_dir) under CURRENT_EXECUTION_RUN_DIRECTORY
                    # So we can ignore it. Lets create list of files that needs to be uploaded
                    # to S3.
                    for _file in _files:
                        file_list_to_upload.append(os.path.join(parent_dir, _file))
            except:
                logger.debug(f"Failed to get contents of Execution Run directory")
        
        for _file in file_list_to_upload:
            if not self.do_upload_(_file, folder_path + os.path.basename(_file)):
                logger.debug(f"ERROR: Uploading error for {_file}")
        
        os.remove(local_file_name)
    
    def do_upload_(self, file_name, file_path):
        """Uploads the given file_name to s3 bucket defined in file_path
        """
        try:
            logger.debug(f"Uploading file {file_name} to {self.bucket_name}/{file_path}")
            self.s3_client.upload_file(file_name, self.bucket_name, file_path)
            logger.debug(f"File {file_name} uploaded successfully to {self.bucket_name}/{file_path}")
            return True
        except NoCredentialsError:
            logger.debug("Credentials not available")
        except Exception as e:
            logger.debug(f"Unable to upload failed objects file to S3 bucket: {e}")
       
        return False
