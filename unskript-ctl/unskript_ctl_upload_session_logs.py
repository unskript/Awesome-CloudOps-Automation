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


source_directory = '/var/unskript/sessions/logs'
destination_directory = '/var/unskript/sessions/uploads'
tar_file_path = '/var/unskript/sessions/session_logs.tgz'
command = f'find {destination_directory} -type f -exec stat -c "%W %n" {{}} \\;'

logging.basicConfig(filename="/var/log/unskript/upload_script.log",
                    level=logging.DEBUG,
                    format=f'%(asctime)s - %(levelname)s - %(message)s')

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

    # Print the resulting dictionary
    logging.info(file_timestamp_dict)
    return file_timestamp_dict

def upload_session_logs():
    # Capture start time
    start_time = datetime.now()
    logging.info(f'Start Time: {start_time}')
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    # Move files from logs to uploads
    for filename in os.listdir(source_directory):
        source_path = os.path.join(source_directory, filename)
        destination_path = os.path.join(destination_directory, filename)
        shutil.move(source_path, destination_path)
    # Create a tar.gz archive
    with tarfile.open(tar_file_path, 'w:gz') as tar:
        tar.add(destination_directory, arcname='uploads')
    
    files = [f for f in os.listdir(destination_directory) if os.path.isfile(os.path.join(destination_directory, f))]
    logging.info(f'Num files uploaded: {len(files)}')
    # Upload to rts
    try:
        upload_logs_files()
    except Exception as e:
        logging.error(f'Error uploading files: {str(e)}')
    
    # if upload fails don't remove files in upload directory else remove it
    # remove tar.gz file in tar_file_path
    os.remove(tar_file_path)
    # Remove the files from the uploads folder
    shutil.rmtree(destination_directory)
    # Capture end time
    end_time = datetime.now()
    logging.info(f'End Time: {end_time}')

def upload_logs_files():
    url = 'http://10.8.0.1:6443/v1alpha1/sessions/logs'

    # Open the file in binary mode
    with open(tar_file_path, 'rb') as file:
        # Set up the files parameter with a tuple containing the filename and file object
        files = {'file': (tar_file_path, file)}

        # Make the POST request with the files parameter
        response = requests.post(url, files=files)

    # Check the response
    if response.status_code == 204:
        logging.info("File uploaded successfully.")
    else:
        logging.info(f"Failed to upload file. Status code: {response.status_code}")
        logging.info(response.text)
    
if __name__ == "__main__":
    upload_session_logs()