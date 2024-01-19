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
import json

TEMP_FOLDER = '/var/unskript/sessions/temp'
COMPLETED_LOGS_FOLDER = '/var/unskript/sessions/completed-logs'
TAR_FILE_PATH = '/var/unskript/sessions/session_logs.tgz'
RTS_HOST = 'http://10.8.0.1:6443'
URL_PATH = '/v1alpha1/sessions/logs'
LOG_FILE_PATH = '/var/log/unskript/upload_script.log'

session_end_times = {}

# Set logging config
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



def upload_session_logs():    
    if not os.path.exists(COMPLETED_LOGS_FOLDER):
        os.makedirs(COMPLETED_LOGS_FOLDER)

    # If completed-logs folder is not empty, the get timestamps from the files in it
    # (To handle case where uploads may fail, hence logs files will be retained in the completed-logs folder)
    if any(os.scandir(COMPLETED_LOGS_FOLDER)):
        for filename in os.listdir(COMPLETED_LOGS_FOLDER):
            # Get the end time from the file
            try:
                get_session_timestamp(filename)
            except Exception as e:
                logger.error("get session timestamp: %s", str(e))
                return
            
    # If temp folder is not empty, then move the files from temp to completed-logs
    if any(os.scandir(TEMP_FOLDER)):
        for filename in os.listdir(TEMP_FOLDER):
            if not filename.endswith(".log"):
                continue
            # Get the end time from the file
            try:
                get_session_timestamp(filename)
            except Exception as e:
                logger.error("get session timestamp: %s", str(e))
                return
            source_path = os.path.join(TEMP_FOLDER, filename)
            destination_path = os.path.join(COMPLETED_LOGS_FOLDER, filename)
            try:
                shutil.move(source_path, destination_path)
            except Exception as e:
                logger.error("File move error: %s", str(e))
                return
    # Cancel upload if there are no files to upload
    if len(session_end_times) == 0:
        return
    # Create a tar.gz archive
    with tarfile.open(TAR_FILE_PATH, 'w:gz') as tar:
        tar.add(COMPLETED_LOGS_FOLDER, arcname='completed-logs')

    # Capture start time
    start_time = datetime.now()
    logger.info(f'Start Time: {start_time}')
    # Upload to rts
    try:
        upload_logs_files(session_end_times)
    except Exception as e:
        logger.error(str(e))
    
    # Capture end time
    end_time = datetime.now()
    logger.info(f'End Time: {end_time}')

def upload_logs_files(session_end_times):
    # Open the file in binary mode
    try:
        with open(TAR_FILE_PATH, 'rb') as file:
            # Set up the files parameter with a tuple containing the filename and file object
            files = {'file': (TAR_FILE_PATH, file)}
            url = f'{RTS_HOST}{URL_PATH}'
            # Make the POST request with the files parameter
            try:
                # payload contains session_ids and their corresponding session end times
                payload = {'session_end_times': json.dumps(session_end_times)}
                response = requests.post(url, files=files, data=payload)
                # Check the response
                if response.status_code == 204:
                    logger.info("%d file(s) uploaded successfully", len(session_end_times))
                    # Remove the files from the completed-logs folder
                    shutil.rmtree(COMPLETED_LOGS_FOLDER)
                else:
                    logger.error("Status Code: %s. Response: %s", response.status_code, response.text)
            except Exception as err:
                logger.error("Error Occured while uploading: %s", str(err))
    except FileNotFoundError:
        logger.error("File not found. Tar file path: %s",TAR_FILE_PATH)
        return
    
    # Remove Tar file
    os.remove(TAR_FILE_PATH)

def get_session_timestamp(filename):
    split_file = filename.split('.')[0].split('-time-')
    if len(split_file) != 2:
        logger.error("timestamp or session id missing from file name: %s",filename)
        return
    session_end_times[split_file[0]] = split_file[1]
    
if __name__ == "__main__":
    upload_session_logs()