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

from pathlib import Path 
from datetime import datetime 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    from envyaml import EnvYAML
except Exception as e:
    print("ERROR: Unable to find required yaml package to parse the config file")
    raise e

# Global Constants used in this file
GLOBAL_UNSKRIPT_CONFIG_FILE = '/unskript/etc/unskript_ctl_config.yaml'
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
                print("ERROR: Enable flag under Email section is set to false, please change to true and re-run")
                return {}
        elif n_type.lower() == 'slack':
            if n_dict.get('Slack').get('enable') is True:
                return n_dict.get('Slack')
            else:
                print("ERROR: Enable flag under Slack section is set to false, please change to true and re-run")
                return {}
        else:
            print(f"ERROR: option {n_type} is not supported")
            return {}
    else:
        print(f"No Notification found for {n_type}")
        return {} 

def send_notification(summary_result_table: list, failed_result: dict):
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
    if len(slack_settings):
        # Slack configuration was found
        s = slack_settings
        retval = send_slack_notification(summary_result_table, 
                                s.get('web-hook-url'),
                                s.get('channel-name'))
    else:
        retval = False

    if len(mail_settings):
        # Mail cnofiguration aws found
        m = mail_settings
        retval = send_email_notification(summary_result_table,
                                failed_result,
                                m)
    else:
        retval = False

    if retval is False:
        print(f"Notification was not sent. Please check if notification is enabled in the unskript-ctl configuration file")

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
                    message += f':hash: *{check_name}*  :dizzy_face: ' + '\n'
                    e += 1
                else:
                    pass
            summary_message += f':trophy: *(Pass/Fail/Error)* <-> *({p}/{f}/{e})*' + '\n\n'
    else:
        print("ERROR: Summary Result is Empty, Not sending notification")
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
                               c_data.get('smtp-host'),
                               c_data.get('smtp-user'),
                               c_data.get('smtp-password'),
                               c_data.get('to-email'),
                               c_data.get('from-email'))
    elif creds_data.get('provider').lower() == "sendgrid":
        c_data = creds_data.get('Sendgrid')
        retval = send_sendgrid_notification(summary_results,
                                   failed_result,
                                   c_data.get('from-email'),
                                   c_data.get('to-email'),
                                   c_data.get('api_key'))
    elif creds_data.get('provider').lower() == "ses":
        c_data = creds_data.get('SES')
        retval = send_awsses_notification(summary_results,
                                   failed_result,
                                   c_data.get('access_key'),
                                   c_data.get('secret_access'),
                                   c_data.get('to-email'),
                                   c_data.get('from-email'),
                                   c_data.get('region'))
    else: 
        print(f"ERROR: Unknown notification service {creds_data.get('service_provider')}")

    return retval


def send_awsses_notification(summary_results: list,
                             failed_result: dict,
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
    print(f"REGION: {region}")
    client = boto3.client('ses', region_name=region)

    charset='UTF-8'
    message = ''
    if len(summary_results):
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
        print("Unable to send email notification to {to_email}")
        return False

    return False

def send_sendgrid_notification(summary_results: list,
                               failed_result: dict,
                               from_email: str,
                               to_email: str,
                               api_key: str):
    # Dynamic Load (Import) necessary libraries for sendgrid
    import sendgrid
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail

    if not from_email or not to_email or not api_key:
        print("ERROR: From Email, To Email and API Key are mandatory parameters to send email notification")
        return False
    try:
        html_message = ''
        if len(summary_results):
            html_message = create_email_message(summary_results, failed_result)
        email_message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject='unSkript-ctl Check Run result',
            html_content=html_message
        )
        sg = sendgrid.SendGridAPIClient(api_key)
        response = sg.send(email_message)
        print(f"Notification sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"ERROR: Unable to send notification as email. {e.__str__()}")
        return False

    return False

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
    
    if len(summary_results):
        message = create_email_message(summary_results, failed_result)

    else:
        print("ERROR: Nothing to send, Results Empty")
        return False
    
    if message:
        msg.attach(MIMEText(message, 'html'))
        server.sendmail(smtp_user, to_email, msg.as_string())
        print(f"Notification sent successfully to {to_email}")
        return True
    else:
        print("ERROR: Nothing to send, Results Empty")


    return False