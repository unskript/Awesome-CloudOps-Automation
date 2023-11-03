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

import json
import yaml
import requests
import subprocess
import smtplib
import os
import base64

from pathlib import Path
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from unskript_utils import *

try:
    from envyaml import EnvYAML
except Exception as e:
    print("ERROR: Unable to find required yaml package to parse the config file")
    raise e

# Global Constants used in this file
GLOBAL_UNSKRIPT_CONFIG_FILE = '/etc/unskript/unskript_ctl_config.yaml'
SMTP_TLS_PORT = 587

def unskript_ctl_config_read_notification(n_type: str):
    """unskript_ctl_config_read_notification: This function reads the configuration
    and returns the Notification configuration as a python dictionary.
    """
    if not n_type:
        print("ERROR: Type is mandatory parameters for this function")
        return

    existing_data = {}
    if os.path.exists(GLOBAL_UNSKRIPT_CONFIG_FILE) is True:
        existing_data = EnvYAML(GLOBAL_UNSKRIPT_CONFIG_FILE, strict=False)
    else:
        print("ERROR: unskript-ctl configuration is missing, please check if it exists in /unskript/etc folder")
        return

    n_dict = existing_data.get('notification')
    if not n_dict:
        print("ERROR: No Notification data found")
        return

    if n_dict.get(n_type):
        if n_type.lower() == 'email':
            if n_dict.get('Email').get('enable') is True:
                notify_data = n_dict.get('Email')
                return notify_data
            else:
                print("Email notification disabled")
                return {}
        elif n_type.lower() == 'slack':
            if n_dict.get('Slack').get('enable') is True:
                return n_dict.get('Slack')
            else:
                print("Slack notification disabled")
                return {}
        else:
            print(f"ERROR: option {n_type} is not supported")
            return {}
    else:
        print(f"No Notification found for {n_type}")
        return {}

def send_notification(summary_result_table: list, 
                      failed_result: dict, 
                      output_metadata_file: str = None):
    """send_notification: This function is called by unskript-ctl or
       unctl to send notification of any given result. The requirement is that
       the result should be in the form of a list of dictionaries.
    """
    retval = None
    if os.path.exists(GLOBAL_UNSKRIPT_CONFIG_FILE) is False:
        print("ERROR: unskript-ctl configuration is missing. Ensure it exists in /unskript/etc")
        return

    slack_settings = unskript_ctl_config_read_notification('Slack')
    mail_settings = unskript_ctl_config_read_notification('Email')

    # Currently it is coded for Either / Or scenario, we can always
    # make it both if need be
    if len(slack_settings) and summary_result_table is not None:
        # Slack configuration was found
        s = slack_settings
        retval = send_slack_notification(summary_result_table,
                                s.get('web-hook-url'),
                                s.get('channel-name'))

    # We support sending attachment only in emails. The parameter output_metadata_file
    # if given, then we shall use that to send the output reading from the metadata file instead
    # of the summary_result_table or failed_result
    if len(mail_settings):
        # Mail configuration was found
        m = mail_settings
        retval = send_email_notification(summary_result_table,
                                failed_result,
                                output_metadata_file,
                                m)

    if retval is False:
        print("ERROR: Unable to send notification!")

def send_slack_notification(summary_results: list,
                            webhook_url: str,
                            channel: str):
    """send_slack_notification: This function uses the slack sdk to send message
       to the given channel. The message is constructed from the summary_results.
    """
    # Construct the Message to be sent
    message = ''
    summary_message = ':wave: *unSkript Ctl Check Results* \n'
    if len(summary_results):
        p = f = e = 0
        for sd in summary_results:
            if sd == {}:
                continue
            for st in sd.get('result'):
                status  = st[-1]
                check_name = st[0]
                if status == 'PASS':
                    message += f':hash: *{check_name}*  :white_check_mark: ' + '\n'
                    p += 1
                elif status == 'FAIL':
                    message += f':hash: *{check_name}*  :x: ' + '\n'
                    f += 1
                elif status == 'ERROR':
                    message += f':hash: *{check_name}*  :x: ' + '\n'
                    e += 1
                else:
                    pass
            summary_message += f':trophy: *(Pass/Fail/Error)* <-> *({p}/{f}/{e})*' + '\n\n'
    else:
        print("Slack Notification disabled")
        return False

    if message:
        message = summary_message + message
        try:
            to_send = { "text": f"{message:<25}" , "mrkdwn": True, "type": "mrkdwn"}
            response = requests.post(webhook_url,
                                    data=json.dumps(to_send, indent=4),
                                    headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                print("Slack message sent successfully!")
                return True
            else:
                print(f"ERROR: Failed to send message {response.status_code}, {response.text}")
                return False
        except Exception as e:
            print(f"ERROR: Not able to send slack message: {e.str()}")
    else:
        print("ERROR: Nothing to send, Results Empty")
        return False

    return True

def send_email_notification(summary_results: list,
                            failed_result: dict,
                            output_metadata_file: str,
                            creds_data: dict):
    """send_email_notification: This function sends the summary result
       in the form of an email.
    """
    retval = False
    if not creds_data:
        print("ERROR: Mail Notification setting is empty. Cannot send Mail out")

    if creds_data.get('provider').lower() == "smtp":
        c_data = creds_data.get('SMTP')
        retval = send_smtp_notification(summary_results,
                               failed_result,
                               output_metadata_file,
                               c_data.get('smtp-host'),
                               c_data.get('smtp-user'),
                               c_data.get('smtp-password'),
                               c_data.get('to-email'),
                               c_data.get('from-email'))
    elif creds_data.get('provider').lower() == "sendgrid":
        c_data = creds_data.get('Sendgrid')
        retval = send_sendgrid_notification(summary_results,
                                   failed_result,
                                   output_metadata_file,
                                   c_data.get('from-email'),
                                   c_data.get('to-email'),
                                   c_data.get('api_key'))
    elif creds_data.get('provider').lower() == "ses":
        c_data = creds_data.get('SES')
        retval = prepare_to_send_awsses_notification(summary_results,
                                   failed_result,
                                   output_metadata_file,
                                   c_data.get('access_key'),
                                   c_data.get('secret_access'),
                                   c_data.get('to-email'),
                                   c_data.get('from-email'),
                                   c_data.get('region'))
    else:
        print(f"ERROR: Unknown notification service {creds_data.get('provider')}")

    return retval

def prepare_to_send_awsses_notification(summary_results: list,
                             failed_result: dict,
                             output_metadata_file: str,
                             access_key: str,
                             secret_key: str,
                             to_email: str,
                             from_email: str,
                             region: str):
    if not access_key or not secret_key:
        print("ERROR: Cannot send AWS SES Notification without access and/or secret_key")
        return  False
    
    # WE CAN TAKE A TITLE AS WELL, IF WE WANT CUSTOM TITLE IN THE REPORT
    attachment_ = MIMEMultipart('mixed')
    attachment_['Subject'] = 'unSkript ctl Run Result'
    
    attachment_ = prepare_combined_email(summary_results=summary_results,
                                         failed_result=failed_result,
                                         output_metadata_file=output_metadata_file,
                                         title=None,
                                         attachment=attachment_)
    
    return do_send_awsses_email(from_email=from_email,
                                to_email=to_email,
                                attachment_=attachment_,
                                access_key=access_key,
                                secret_key=secret_key,
                                region=region)

def do_send_awsses_email(from_email: str,
                         to_email: str,
                         attachment_,
                         access_key: str,
                         secret_key: str,
                         region: str):
    # Boto3 client needs AWS Access Key and Secret Key
    # to be able to initialize the SES client.
    # We do it by setting  the os.environ variables
    # for access and secret key
    import boto3
    from botocore.exceptions import NoCredentialsError

    os.environ['AWS_ACCESS_KEY_ID'] = access_key
    os.environ['AWS_SECRET_ACCESS_KEY'] = secret_key
    client = boto3.client('ses', region_name=region)
    try:
        response = client.send_raw_email(
            Source=from_email,
            Destinations=[to_email],
            RawMessage={'Data': attachment_.as_string()}
        )
        if response.get('ResponseMetadata') and response.get('ResponseMetadata').get('HTTPStatusCode') == 200:
            print(f"Email notification sent to {to_email}")
        return True
    except NoCredentialsError:
        print("ERROR: Unable to send email notification to {to_email}, credentials are invalid")
        return False
    except client.exceptions.MessageRejected:
        print(f"ERROR: Unable to send email. Message was Rejected from SES server check from email-id {to_email} is valid!")
        return False
    except client.exceptions.MailFromDomainNotVerifiedException:
        print("ERROR: Unable to send email. Domain of from email-id is not verified!, Please use a valid from email-id")
        return False
    except client.exceptions.ConfigurationSetDoesNotExistException:
        print("ERROR: Unable to send email. Email Configuration set does not exist. Please check SES policy")
        return False
    except client.exceptions.ConfigurationSetSendingPausedException:
        print(f"ERROR: Unable to send email. Email sending is paused for the from email id {from_email}!")
        return False
    except client.exceptions.AccountSendingPausedException:
        print("ERROR: Unable to send email. Sending email is paused for the AWS Account!")
        return False
    except client.exceptions.ClientError as e:
        print(f"ERROR: {e}")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
    return False

def send_sendgrid_notification(summary_results: list,
                               failed_result: dict,
                               output_metadata_file: str,
                               from_email: str,
                               to_email: str,
                               api_key: str):
    # Dynamic Load (Import) necessary libraries for sendgrid
    import sendgrid
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType

    if not from_email or not to_email or not api_key:
        print("ERROR: From Email, To Email and API Key are mandatory parameters to send email notification")
        return False
    
    html_message = ''
    email_subject = 'unSkript-ctl Check Run result'
    parent_folder = UNSKRIPT_GLOBALS.get('CURRENT_EXECUTION_RUN_DIRECTORY')
    target_name = os.path.basename(parent_folder)
    tar_file_name = f"{target_name}" + '.tar.bz2'
    target_file_name = None
    metadata = None
    try: 
        # We can have custom Title here
        html_message += create_email_header(title=None)
        if summary_results and len(summary_results):
            html_message += create_checks_summary_message(summary_results=summary_results,
                                                          failed_result=failed_result)
            create_temp_files_of_failed_results(failed_result=failed_result)            
        if output_metadata_file:
            html_message += create_script_summary_message(output_metadata_file=output_metadata_file)
            with open(output_metadata_file, 'r') as f:
                metadata = json.loads(f.read())
            if metadata and metadata.get('output_file'):
                target_file_name = os.path.basename(metadata.get('output_file'))
            parent_folder = os.path.dirname(output_metadata_file)
            target_name = os.path.basename(parent_folder)
            tar_file_name = f"{target_name}" + '.tar.bz2'
        if metadata and metadata.get('compress') is True:
            output_metadata_file = output_metadata_file.split('/')[-1]
            if create_tarball_archive(tar_file_name=tar_file_name,
                                        output_metadata_file=output_metadata_file,
                                        parent_folder=parent_folder) is False: 
                raise ValueError("ERROR: Archiving attachments failed!")
            target_file_name = tar_file_name
        else:
            if create_tarball_archive(tar_file_name=tar_file_name,
                                        output_metadata_file=None,
                                        parent_folder=parent_folder) is False: 
                raise ValueError("ERROR: Archiving attachments failed!")
            target_file_name = tar_file_name
        
        email_message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=email_subject,
            html_content=html_message
        )
        if target_file_name: 
            email_message = sendgrid_add_email_attachment(email_message=email_message,
                                                        file_to_attach=target_file_name,
                                                        compress=True)
        try:
            if tar_file_name:
                os.remove(target_file_name)
        except Exception as e:
            print(f"ERROR: {e}")

        sg = sendgrid.SendGridAPIClient(api_key)
        sg.send(email_message)
        print(f"Notification sent successfully to {to_email}")
    except Exception as e:
        print(f"ERROR: Unable to send notification as email. {e}")
        return False
    
    return True

def sendgrid_add_email_attachment(email_message, 
                                  file_to_attach: str,
                                  compress: bool = True):
    from sendgrid.helpers.mail import Attachment, FileContent, FileName, FileType
    with open(file_to_attach, 'rb') as f:
        file_data = f.read()

        encoded = base64.b64encode(file_data).decode()
        attachment = Attachment()
        attachment.file_content = FileContent(encoded)
        file_name = os.path.basename(file_to_attach)
        attachment.file_name = FileName(file_name)
        if compress is True:
            attachment.file_type = FileType('application/zip')
        else:
            attachment.file_type = FileType('application/text')
        attachment.disposition = 'attachment'
        email_message.add_attachment(attachment)
    
    return email_message


def create_email_header(title: str = None):
    if not title:
        email_title = "unSkript-ctl run result"
    else:
        email_title = title
    message = f'''
        <!DOCTYPE html>
        <html>
        <head>
        </head>
        <body>
        <center>
        <h1> {email_title} </h1>
        <h3> <strong>Tested On <br> {datetime.now().strftime("%a %b %d %I:%M:%S %p %Y %Z")} </strong></h3>
        </center>
        '''
    return message

def create_checks_summary_message(summary_results: list,
                                  failed_result: dict):
    message = ''
    if not summary_results or not failed_result:
        return message
    
    if len(summary_results):
        p = f = e = 0
        tr_message = ''
        for sd in summary_results:
            if sd == {}:
                continue
            tr_message += '''
                <br>
                <h3> Check Summary Result </h3>
                <table border="1">
                <tr>
                <th> CHECK NAME </th>
                <th> RESULT </th>
                </tr>
            '''
            for st in sd.get('result'):
                status  = st[-1]
                check_name = st[0]
                if status == 'PASS':
                    tr_message += f'<tr> <td> {check_name}</td> <td> <strong>PASS</strong> </td></tr>' + '\n'
                    p += 1
                elif status == 'FAIL':
                    check_link = f"{check_name}".lower().replace(' ','_')
                    tr_message += f'<tr><td> <a href="#{check_link}">{check_name}</a></td><td>  <strong>FAIL</strong> </td></tr>' + '\n'
                    f += 1
                elif status == 'ERROR':
                    tr_message += f'<tr><td> {check_name}</td><td>  <strong>ERROR</strong> </td></tr> ' + '\n'
                    e += 1
                else:
                    pass
        message += f'<center><h3>Checks Summary<br>Pass : {p}  Fail: {f}  Error: {e}</h3></center><br>' + '\n'
        message += tr_message + '\n'
        message += '</table>' + '\n'


    return message

def create_script_summary_message(output_metadata_file: str):
    message = ''
    if os.path.exists(output_metadata_file) is False:
        print(f"ERROR: The metadata file is missing, please check if file exists? {output_metadata_file}")
        return message

    metadata = ''
    with open(output_metadata_file, 'r', encoding='utf-8') as f:
        metadata = json.loads(f.read())

    if not metadata:
        print(f'ERROR: Metadata is empty for the script. Please check content of {output_metadata_file}')
        raise ValueError("Metadata is empty")
        
    message += f'''
            <br>
            <h3> Custom Script Run Result </h3>
            <table border="1">
                <tr>
                    <th> Status </th>
                    <th> Time (in seconds) </th>
                    <th> Error </th>
                </tr>
                <tr>
                    <td>{metadata.get('status')}</td>
                    <td>{metadata.get('time_taken')}</td>
                    <td>{metadata.get('error')}</td>
                </tr>
            </table>
    '''
    return message 


def create_email_attachment(output_metadata_file: str = None):
    """create_email_attachment: This function reads the output_metadata_file
    to find out the name of the attachment, the output that should be included as the attachment
    of the test run as listed in the output_metadata_file.
    """
    metadata = ''
    with open(output_metadata_file, 'r', encoding='utf-8') as f:
        metadata = json.loads(f.read())

    if not metadata:
        print(f'ERROR: Metadata is empty for the script. Please check content of {output_metadata_file}')
        raise ValueError("Metadata is empty")

    # if the status is FAIL, then there is no file to attach, so just send the message.
    multipart_content_subtype = 'mixed'
    attachment_ = MIMEMultipart(multipart_content_subtype)

    target_file_name = None
    if metadata.get('output_file'):
        target_file_name  = os.path.basename(metadata.get('output_file'))
    else:
        target_file_name = "unskript_ctl_result"

    if metadata.get('compress') is True:
        parent_folder = os.path.dirname(output_metadata_file)
        target_name = os.path.basename(parent_folder)
        tar_file_name = f"{target_name}" + '.tar.bz2'
        output_metadata_file = output_metadata_file.split('/')[-1]
        if create_tarball_archive(tar_file_name=tar_file_name,
                                  output_metadata_file=output_metadata_file,
                                  parent_folder=parent_folder) is False:
            raise ValueError("ERROR: Archiving attachments failed!")
        target_file_name = tar_file_name

    with open(target_file_name, 'rb') as f:
        part = MIMEApplication(f.read())
        part.add_header('Content-Disposition', 'attachment', filename=target_file_name)
        attachment_.attach(part)
    try:
        if metadata.get('compress') is True:
            os.remove(target_file_name)
    except Exception as e:
        print(f"ERROR: {e}")

    return attachment_



def create_temp_files_of_failed_results(failed_result: dict):
    list_of_failed_files = []
    if not failed_result:
        return list_of_failed_files
    
    if failed_result and len(failed_result):
        connectors_list = [x.split(':')[0] for x in failed_result.keys()]
        for connector in connectors_list:
            connector_file = UNSKRIPT_GLOBALS.get('CURRENT_EXECUTION_RUN_DIRECTORY') + f'/{connector}.txt'
            with open(connector_file, 'w', encoding='utf-8') as f:
                for c_name, f_obj in failed_result.items():
                    if c_name.startswith(connector):
                        f.write('\n' + c_name + '\n')
                        f.write(yaml.dump(f_obj, default_flow_style=False))
            if connector_file not in list_of_failed_files:
                list_of_failed_files.append(connector_file)
        
    return list_of_failed_files


def create_tarball_archive(tar_file_name: str, 
                           output_metadata_file: str,
                           parent_folder: str):
    if not output_metadata_file:
        tar_cmd = ["tar", "jcvf", tar_file_name, f"--exclude={output_metadata_file}", "-C" , parent_folder, "."]
    else:
        tar_cmd = ["tar", "jcvf", tar_file_name, "-C" , parent_folder, "."]
    try:
        subprocess.run(tar_cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    return True

def send_smtp_notification(summary_results: list,
                            failed_result: dict,
                            output_metadata_file: str,
                            smtp_host: str,
                            smtp_user: str,
                            smtp_password: str,
                            to_email: str,
                            from_email: str):
    """send_smtp_notification: This function sends the summary result
       in the form of an email for smtp option.
    """

    msg = MIMEMultipart('mixed')
    if from_email:
        msg['From'] =  from_email
    else:
        msg['From'] = smtp_user

    msg['To'] = to_email
    msg['Subject'] = 'unSkript-ctl Run result'
    try:
        server = smtplib.SMTP(smtp_host, SMTP_TLS_PORT)
        server.starttls()
        server.login(smtp_user, smtp_password)
    except Exception as e:
        print(e)
        return False
    
    msg = prepare_combined_email(summary_results=summary_results,
                                 failed_result=failed_result,
                                 output_metadata_file=output_metadata_file,
                                 title=None,
                                 attachment=msg)
    
    try:
        server.sendmail(smtp_user, to_email, msg.as_string())
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        print(f"Notification sent successfully to {to_email}")

    return True

def prepare_combined_email(summary_results: list,
                           failed_result: dict,
                           output_metadata_file: str,
                           title: str,
                           attachment: MIMEMultipart):
    message = create_email_header(title=title)
    temp_attachment = msg = None 
    if summary_results and len(summary_results):
        message += create_checks_summary_message(summary_results=summary_results,
                                                 failed_result=failed_result)
        create_temp_files_of_failed_results(failed_result=failed_result)
        parent_folder = UNSKRIPT_GLOBALS.get('CURRENT_EXECUTION_RUN_DIRECTORY')
        target_name = os.path.basename(parent_folder)
        tar_file_name = f"{target_name}" + '.tar.bz2'
        if create_tarball_archive(tar_file_name=tar_file_name,
                                output_metadata_file=None,
                                parent_folder=parent_folder) is False: 
            raise ValueError("ERROR: Archiving attachments failed!")
        target_file_name = tar_file_name
        msg = MIMEMultipart('mixed')
        with open(target_file_name, 'rb') as f:
            part = MIMEApplication(f.read())
            part.add_header('Content-Disposition', 'attachment', filename=target_file_name)
            msg.attach(part)
        
    if output_metadata_file:
        message += create_script_summary_message(output_metadata_file=output_metadata_file)
        temp_attachment = create_email_attachment(output_metadata_file=output_metadata_file)
        
    if failed_result and len(failed_result):
        message += '<br> <ul>' + '\n'
        message += '<h3> DETAILS ABOUT THE FAILED OBJECTS CAN BE FOUND IN THE ATTACHMENTS FOR EACH CONNECTORS </h3>' + '\n'
        message += '</ul> <br>' + '\n'
    message += "</body> </html>"
    attachment.attach(MIMEText(message, 'html'))
    if temp_attachment:
        attachment.attach(temp_attachment)
    elif msg:
        attachment.attach(msg)
    
    return attachment