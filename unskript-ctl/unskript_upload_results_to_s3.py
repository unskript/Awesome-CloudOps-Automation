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
        now = datetime.now()
        rfc3339_timestamp = now.isoformat() + 'Z'
        self.ts = rfc3339_timestamp
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        self.customer_name = os.getenv('CUSTOMER_NAME','UNKNOWN_CUSTOMER_NAME')
        self.file_name = f"dashboard_{rfc3339_timestamp}.json"
        self.folder_path = f"{self.customer_name}/{year}/{month}/{day}/"
        self.file_path = f"{self.folder_path}{self.file_name}"
        self.local_file_name = f"/tmp/{self.file_name}"

        if not aws_access_key_id or not aws_secret_access_key:
            logger.debug("AWS credentials are not set in environment variables")
            return

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

    def create_s3_folder_path(self):
        # Initialize folder_exists
        folder_exists = False

        # Ensure the bucket exists
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            logger.debug(f"S3 bucket {self.bucket_name} exists")
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                logger.debug(f"S3 bucket {self.bucket_name} does not exist, creating bucket")
                try:
                    self.s3_client.create_bucket(Bucket=self.bucket_name)
                    logger.debug(f"S3 bucket {self.bucket_name} created")
                except ClientError as e:
                    logger.debug(f"Failed to create bucket: {e}")
                    return False  # Exit if the bucket cannot be created
            else:
                logger.debug(f"Error checking bucket existence: {e}")
                return False  # Exit if there is any other error
        
        # Ensure the folder structure exists in the bucket
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=self.folder_path)
            folder_exists = True
            logger.debug(f"S3 folder {self.folder_path} exists")
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                folder_exists = False
                logger.debug(f"S3 folder {self.folder_path} does not exist")
            else:
                logger.debug(f"Error checking folder existence: {e}")

        # Create folder if it doesn't exist
        if not folder_exists:
            logger.debug(f"Creating folder {self.folder_path} in the bucket")
            try:
                self.s3_client.put_object(Bucket=self.bucket_name, Key=self.folder_path)
            except ClientError as e:
                logger.debug(f"Failed to create folder: {e}")
    
        return True

    # def rename_and_upload_failed_objects(self, checks_output):
    #     try:
    #         # Convert checks_output to JSON format
    #         checks_output_json = json.dumps(checks_output, indent=2)
    #     except json.JSONDecodeError:
    #         logger.debug(f"Failed to decode JSON response for {self.customer_name}")
    #         return

    #     # Write JSON data to a local file
    #     try:
    #         logger.debug(f"Writing JSON data to local file: {self.local_file_name}")
    #         with open(self.local_file_name, 'w') as json_file:
    #             json_file.write(checks_output_json)
    #     except IOError as e:
    #         logger.debug(f"Failed to write JSON data to local file: {e}")
    #         return

    #     if not self.create_s3_folder_path():
    #         logger.debug("Unable to create bucket")
    #         return

    #     # Upload the JSON file
    #     try:
    #         logger.debug(f"Uploading file {self.file_name} to {self.bucket_name}/{self.file_path}")
    #         self.s3_client.upload_file(self.local_file_name, self.bucket_name, self.file_path)
    #         logger.debug(f"File {self.file_name} uploaded successfully to {self.bucket_name}/{self.folder_path}")
    #     except NoCredentialsError:
    #         logger.debug("Credentials not available")
    #     except Exception as e:
    #         logger.debug(f"Unable to upload failed objetcs file to S3 bucket: {e}")
    #     # Remove the local file after upload
    #     logger.debug(f"Removing local file of check outputs json from /tmp: {self.local_file_name}")
    #     os.remove(self.local_file_name)

    def rename_and_upload_other_items(self):
        if not self.create_s3_folder_path():
            logger.debug("Unable to create bucket")
            return
        # Upload the files in the CURRENT_EXECUTION_RUN_DIRECTORY 
        file_list_to_upload = [self.local_file_name]
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
                logger.debug("Failed to get contents of Execution Run directory")
        
        for _file in file_list_to_upload:
            base_name, extension = os.path.splitext(os.path.basename(_file))
            if base_name.startswith("dashboard"):
                file_path = os.path.join(self.folder_path, os.path.basename(_file))
            else:
                temp_fp = f"{base_name}_{self.ts}{extension}"
                file_path = os.path.join(self.folder_path, temp_fp)
            
            if not self.do_upload_(_file, file_path):
                logger.debug(f"ERROR: Uploading error for {_file}")

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
