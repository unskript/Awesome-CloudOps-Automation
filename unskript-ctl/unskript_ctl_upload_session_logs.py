#!/usr/bin/env python
#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE
#
#
import os
import shutil
import tarfile
import logging
from datetime import datetime
import requests
import subprocess


SOURCE_DIRECTORY = '/var/unskript/sessions/logs'
DESTINATION_DIRECTORY = '/var/unskript/sessions/uploads'
TAR_FILE_PATH = '/var/unskript/sessions/session_logs.tgz'
RTS_HOST = 'http://10.8.0.1:6443'
URL_PATH = '/v1alpha1/sessions/logs'
LOG_FILE_PATH = '/var/log/unskript/upload_script.log'
command = f'find {DESTINATION_DIRECTORY} -type f -exec stat -c "%W %n" {{}} \\;'

# Set logging config
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_logs_timestamps():
    # Run the command and capture the output
    output = subprocess.check_output(command, shell=True, text=True)

    # Parse the output and create a dictionary
    file_timestamp_dict = {}
    for line in output.split('\n'):
        if line:
            timestamp, full_path = line.split(' ', 1)
            filename = full_path.split('/')[-1]  # Extracting the filename from the full path
            file_timestamp_dict[filename.split('.log')[0]] = int(timestamp)

    return file_timestamp_dict

def upload_session_logs():
    # Check if the SOURCE_DIRECTORY is empty or not. 
    if not any(os.scandir(SOURCE_DIRECTORY)):
        return
    if not os.path.exists(DESTINATION_DIRECTORY):
        os.makedirs(DESTINATION_DIRECTORY)
    # Move files from logs to uploads
    for filename in os.listdir(SOURCE_DIRECTORY):
        source_path = os.path.join(SOURCE_DIRECTORY, filename)
        # if file is empty, don't upload it
        if os.path.getsize(source_path) == 0:
            continue
        destination_path = os.path.join(DESTINATION_DIRECTORY, filename)
        try:
            shutil.move(source_path, destination_path)
        except Exception as e:
            logger.error("File move error: %s", str(e))
            return
    # If there are no files to upload, cancel operation
    num_files = [f for f in os.listdir(DESTINATION_DIRECTORY) if os.path.isfile(os.path.join(DESTINATION_DIRECTORY, f))]
    if len(num_files) == 0:
        return
    # Capture start time
    start_time = datetime.now()
    logger.info(f'Start Time: {start_time}')
    # Create a tar.gz archive
    with tarfile.open(TAR_FILE_PATH, 'w:gz') as tar:
        tar.add(DESTINATION_DIRECTORY, arcname='uploads')
    # Upload to rts
    try:
        upload_logs_files(num_files)
    except Exception as e:
        logger.error(str(e))
    
    # Capture end time
    end_time = datetime.now()
    logger.info(f'End Time: {end_time}')

def upload_logs_files(num_files):
    # Open the file in binary mode
    response = None
    try:
        with open(TAR_FILE_PATH, 'rb') as file:
            # Set up the files parameter with a tuple containing the filename and file object
            files = {'file': (TAR_FILE_PATH, file)}
            url = f'{RTS_HOST}{URL_PATH}'
            # Make the POST request with the files parameter
            try:
                response = requests.post(url, files=files)
            except Exception:
                logger.error("Status Code: %s. Response: %s", response.status_code, response.text)
    except FileNotFoundError:
        logger.error("File not found. Tar file path: %s",TAR_FILE_PATH)
        return
    # Check the response
    if response.status_code == 204:
        logger.info("%d file(s) uploaded successfully", len(num_files))
        # Remove the files from the uploads folder
        shutil.rmtree(DESTINATION_DIRECTORY)
    # Remove Tar file
    os.remove(TAR_FILE_PATH)
    
if __name__ == "__main__":
    upload_session_logs()