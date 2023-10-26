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
import smtplib
import os
import base64

from pathlib import Path
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

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

def send_notification(summary_result_table: list, failed_result: dict, output_metadata_file: str = None):
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
    if len(slack_settings) and summary_result_table != None:
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
        retval = send_awsses_notification(summary_results,
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


def send_awsses_notification(summary_results: list,
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

    # Boto3 client needs AWS Access Key and Secret Key
    # to be able to initialize the SES client.
    # We do it by setting  the os.environ variables
    # for access and secret key
    import boto3
    from botocore.exceptions import NoCredentialsError

    os.environ['AWS_ACCESS_KEY_ID'] = access_key
    os.environ['AWS_SECRET_ACCESS_KEY'] = secret_key
    client = boto3.client('ses', region_name=region)

    charset='UTF-8'
    message = ''
    if summary_results and len(summary_results):
        message = create_email_message(summary_results, failed_result)
        email_template = {
            'Subject': {
                'Data': 'unSkript-ctl Check Run result',
                'Charset': charset
            },
            'Body': {
                'Html': {
                    'Data': message,
                    'Charset': charset
                }
            }
        }
        # The AWS SES Client needs from_email address to be set
        # Else the email will not be sent.
        try:
            response = client.send_email(
                    Source=from_email,
                    Destination={
                        'ToAddresses': [to_email]
                    },
                    Message=email_template
                    )
            print(f"Notification sent successfully as email to {to_email}")
            return True
        except NoCredentialsError:
            print("ERROR: Unable to send email notification to {to_email}, credentials are invalid")
            return False
        except client.exceptions.MessageRejected:
            print(f"ERROR: Unable to send email. Message was Rejected from SES server. Please check from email {from_email} is valid")
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
            print(f"ERROR: Unable to send email out. Invalid Client Token, please verify access and/or secret_key! {e}")
            return False
        except Exception as e:
            print(f"ERROR: {e}")
            return False

    elif output_metadata_file:
        _, attachment_ = create_email_message_with_attachment(output_metadata_file=output_metadata_file)
        attachment_['Subject'] = 'unSkript-ctl Check Run result'
        attachment_['From'] = from_email
        attachment_['To'] = to_email
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
    try:
        html_message = ''
        if summary_results and len(summary_results):
            html_message = create_email_message(summary_results, failed_result)
            email_message = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject='unSkript-ctl Check Run result',
                html_content=html_message
            )
        elif output_metadata_file:
            html_message, _ = create_email_message_with_attachment(output_metadata_file=output_metadata_file)
            email_message = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject='unSkript-ctl Custom Script Run result',
                html_content=html_message
            )
            all_attachment_files = []
            with open(output_metadata_file, 'r') as f:
                metadata = json.loads(f.read())
                if metadata:
                    if isinstance(metadata.get('output_file'), str):
                        all_attachment_files.append(metadata.get('output_file'))
                    elif isinstance(metadata.get('output_file'), list):
                        all_attachment_files = metadata.get('output_file')
            file_data = ''
            for attach_file in all_attachment_files:
                if attach_file != "" or attach_file != None:
                    with open(attach_file, 'rb') as _f:
                            file_data = _f.read()

                    encoded = base64.b64encode(file_data).decode()
                    attachment = Attachment()
                    attachment.file_content = FileContent(encoded)
                    file_name = os.path.basename(attach_file)
                    attachment.file_name = FileName(file_name)
                    attachment.file_type = FileType('application/text')
                    attachment.disposition = 'attachment'
                    email_message.add_attachment(attachment)

        sg = sendgrid.SendGridAPIClient(api_key)
        response = sg.send(email_message)
        print(f"Notification sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"ERROR: Unable to send notification as email. {e}")
        return False


def create_email_message_with_attachment(output_metadata_file: str = None):
    """create_email_message_with_attachment: This function reads the output_metadata_file
    to find out the name of the attachment, the output that should be included as the attachment
    and summary of the test run as listed in the output_metadata_file.
    """
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

    message = f'''
            <!DOCTYPE html>
            <html>
            <head>
            </head>
            <body>
            <center>
            <h1> unSkript-ctl Custom Script Run result </h1>
            <h3> <strong>Tested On <br> {datetime.now().strftime("%a %b %d %I:%M:%S %p %Y %Z")} </strong></h3>
            </center>

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
            </body>
            </html>
    '''

    # if the status is FAIL, then there is no file to attach, so just send the message.
    multipart_content_subtype = 'mixed'
    attachment_ = MIMEMultipart(multipart_content_subtype)
    part1 = MIMEText(message, 'html')
    attachment_.attach(part1)

    all_files_to_attach = []
    if isinstance(metadata.get('output_file'), str):
        all_files_to_attach.append(metadata.get('output_file'))
    elif isinstance(metadata.get('output_file'), list):
        all_files_to_attach = metadata.get('output_file')
    else:
        # No other type is supported
        pass

    for attach_file in all_files_to_attach:
        if attach_file != "" or attach_file != None:
            with open(attach_file, 'r', encoding='utf-8') as f:
                part = MIMEApplication(f.read())
                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attach_file))
                attachment_.attach(part)

    return (message, attachment_)

def create_email_message(summary_results: list,
                         failed_result: dict):
    """create_email_message: Utility function that parses summary result and failed result
       to create a HTML message that can be sent out as email
    """
    message = ''
    if len(summary_results):
        message = f'''
            <!DOCTYPE html>
            <html>
            <head>
            </head>
            <body>
            <center>
            <h1> unSkript-ctl Check Run result </h1>
            <h3> <strong>Tested On <br> {datetime.now().strftime("%a %b %d %I:%M:%S %p %Y %Z")} </strong></h3>
            </center>
        '''
        p = f = e = 0
        for sd in summary_results:
            if sd == {}:
                continue
            tr_message = '''
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
        message += f'<center><h3>Test Summary<br>Pass : {p}  Fail: {f}  Error: {e}</h3></center><br>' + '\n'
        message += tr_message + '\n'
        message += '</table>' + '\n'

        if failed_result and len(failed_result):
            message += '<br> <ul>' + '\n'
            message += '<h2> FAILED OBJECTS </h2>' + '\n'
            for k,v in failed_result.items():
                check_link = f"{k}".lower().replace(' ', '_')
                message += f'<li> <strong id="{check_link}">{k}</strong> </li>' + '\n'
                message += f'<pre>{yaml.dump(v,default_flow_style=False)}</pre>' + '\n'
            message += '</ul> <br> </body> </html>' + '\n'

    return message

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

    msg = MIMEMultipart()
    if from_email:
        msg['From'] =  from_email
    else:
        msg['From'] = smtp_user

    msg['To'] = to_email
    msg['Subject'] = 'unSkript-ctl Check Run result'
    try:
        server = smtplib.SMTP(smtp_host, SMTP_TLS_PORT)
        server.starttls()
        server.login(smtp_user, smtp_password)
    except Exception as e:
        print(e)
        return False

    if summary_results and len(summary_results):
        message = create_email_message(summary_results, failed_result)
        if not message:
            print("ERROR: Nothing to send, Results Empty")
            return False
        msg.attach(MIMEText(message, 'html'))
    elif output_metadata_file:
        message, attachment = create_email_message_with_attachment(output_metadata_file=output_metadata_file)
        if attachment != None:
            msg.attach(attachment)
    else:
        print("ERROR: Nothing to send, Results Empty")
        return False

    try:
        response = server.sendmail(smtp_user, to_email, msg.as_string())
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        print(f"Notification sent successfully to {to_email}")
    return False
