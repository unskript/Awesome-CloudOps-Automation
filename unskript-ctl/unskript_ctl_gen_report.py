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
import requests
import smtplib 
import os

from pathlib import Path 
from datetime import datetime 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from unskript_ctl_config import *

# Global Constants used in this file
GLOBAL_UNSKRIPT_CONFIG_FILE = '/unskript/etc/unskript_global.yaml'
SMTP_TLS_PORT = 587

def send_notification(summary_result_table: list, failed_result: dict):
    """send_notification: This function is called by unskript-ctl or
       unctl to send notification of any given result. The requirement is that
       the result should be in the form of a list of dictionaries. 
    """
    if os.path.exists(GLOBAL_UNSKRIPT_CONFIG_FILE) is False:
        print("ERROR: Global Configuration file not found. Please run add_notification first")
        return 
    
    slack_settings = unskript_ctl_config_read_notification('slack')
    mail_settings = unskript_ctl_config_read_notification('mail')
    
    # Currently it is coded for Either / Or scenario, we can always
    # make it both if need be
    if slack_settings and len(slack_settings):
        # Slack configuration was found
        if slack_settings.get('notification') and slack_settings.get('notification').get('slack'):
            s = slack_settings.get('notification').get('slack')
            send_slack_notification(summary_result_table, 
                                    s.get('creds').get('hook_url'),
                                    s.get('creds').get('channel'))
        pass
    elif mail_settings and len(mail_settings):
        # Mail cnofiguration aws found
        if mail_settings.get('notification') and mail_settings.get('notification').get('mail'):
            m = mail_settings.get('notification').get('mail')
            send_email_notification(summary_result_table,
                                    failed_result,
                                    m.get('creds').get('smtp_host'),
                                    m.get('creds').get('smtp_user'),
                                    m.get('creds').get('smtp_password'),
                                    m.get('creds').get('to_email'))

def send_slack_notification(summary_results: list,
                            webhook_url: str,
                            channel: str):
    """send_slack_notification: This function uses the slack sdk to send message
       to the given channel. The message is constructed from the summary_results.
    """
    # Construct the Message to be sent
    message = ':wave: *unSkript Ctl Check Results* \n'
    if len(summary_results):
        p = f = e = 0
        for sd in summary_results:
            if sd == {}:
                continue
            for st in sd.get('result'):
                status  = st[-1]
                check_name = st[0]
                if status == 'PASS':
                    message += f'*{check_name}*  :white_check_mark: ' + '\n'
                    p += 1
                elif status == 'FAIL':
                    message += f'*{check_name}*  :x: ' + '\n'
                    f += 1
                elif status == 'ERROR':
                    message += f'*{check_name}*  :dizzy_face: ' + '\n'
                    e += 1
                else:
                    pass
            message += f'*(Pass/Fail/Error)* <-> *({p}/{f}/{e})*' + '\n'
        pass
    else:
        print("ERROR: Summary Result is Empty, Not sending notification")
    
    if message:
        try:
            to_send = { "text": f"{message:<25}" , "mrkdwn": True, "type": "mrkdwn"}
            response = requests.post(webhook_url,
                                    data=json.dumps(to_send, indent=4),
                                    headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                print("Message sent successfully!")
            else:
                print(f"ERROR: Failed to send message {response.status_code}, {response.text}")
        except:
            pass
    else:
        print("ERROR: Nothing to send, Results Empty")

def send_email_notification(summary_results: list,
                            failed_result: dict,
                            smtp_host: str,
                            smtp_user: str,
                            smtp_password: str,
                            to_email: str):
    """send_email_notification: This function sends the summary result
       in the form of an email.
    """

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = 'unSkript-ctl Check Run result'
    try:
        server = smtplib.SMTP(smtp_host, SMTP_TLS_PORT)
        server.starttls()
        server.login(smtp_user, smtp_password)
    except Exception as e:
        print(e)
        return
    
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
            <p> <strong>Test run on: {datetime.now()} </strong></p>
            </center>
            <table border="1">    
            <tr>
              <th> CHECK NAME </th>
              <th> RESULT </th>
            </tr>
        '''
        p = f = e = 0
        for sd in summary_results:
            if sd == {}:
                continue
            for st in sd.get('result'):
                status  = st[-1]
                check_name = st[0]
                if status == 'PASS':
                    message += f'<tr> <td> {check_name}</td> <td> <strong>PASS</strong> </td></tr>' + '\n'
                    p += 1
                elif status == 'FAIL':
                    message += f'<tr><td> {check_name}</td><td>  <strong>FAIL</strong> </td></tr>' + '\n'
                    f += 1
                elif status == 'ERROR':
                    message += f'<tr><td> {check_name}</td><td>  <strong>ERROR</strong> </td></tr> ' + '\n'
                    e += 1
                else:
                    pass
        message += f'<tr><td>(Pass/Fail/Error) </td><td> <strong>({p}/{f}/{e})</strong></td></tr>' + '\n'
        message += '</table>' + '\n'

        if len(failed_result):
            message += '<br> <ul>' + '\n'
            message += '<h2> FAILED OBJECTS </h2>' + '\n'
            for k,v in failed_result.items():
                message += f'<li> <strong>{k}</strong> </li>' + '\n'
                message += f'<pre> {json.dumps(v,indent=4)} </pre>' + '\n'
            message += '</ul> <br> </body> </html>' + '\n'
        pass
        
    else:
        print("ERROR: Nothing to send, Results Empty")
        return 
    
    if message:
        msg.attach(MIMEText(message, 'html'))
        server.sendmail(smtp_user, to_email, msg.as_string())
        print("Notification Sent Successfully as Email")
    else:
        print("ERROR: Nothing to send, Results Empty")