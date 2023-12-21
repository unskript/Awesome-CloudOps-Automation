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

from jsonschema import validate, ValidationError


from unskript_utils import *
from unskript_factory import NotificationFactory

class SlackNotification(NotificationFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        config = self._config.get_notification()
        self.slack_config = config.get('Slack')
        self.schema_file = os.path.join(os.path.dirname(__file__), "unskript_slack_notify_schema.json")

    def validate_data(self, data):
        if not os.path.exists(self.schema_file):
            self.logger.error(f"Unable to find Notification Schema file {self.schema_file}!")
            return False  
        try:
            with open(self.checks_schema_file, 'r') as f:
                schema = json.load(f)
                validate(instance=data, schema=schema)
                return True 
        except ValidationError as e:
            self.logger.error(e)
            return False 

    def notify(self, **kwargs):
        summary_results = kwargs.get('summary_result_table', None)

        if self.slack_config.get('enable') is False:
            self.logger.error("Slack Notification disabled")
            return False

        if len(summary_results) == 0:
            self.logger.error("Result Empty: No results to notify")
            return False 

        if not self.validate_data(summary_results):
            self.logger.error("Given Summary Result does not validate against Slack Schema")
            return False 
        
        message = self._generate_notification_message(summary_results)
        if not message:
            self.logger.error("ERROR: Nothing to send, Results Empty")
            return False

        try:
            to_send = {"text": message, "mrkdwn": True, "type": "mrkdwn"}
            response = requests.post(self.slack_config.get('web-hook-url'),
                                     data=json.dumps(to_send, indent=4),
                                     headers={"Content-Type": "application/json"})

            if response.status_code == 200:
                self.logger.info("Slack message sent successfully!")
                return True
            else:
                self.logger.error(f"ERROR: Failed to send message {response.status_code}, {response.text}")
                return False
        except requests.RequestException as e:
            self.logger.error(f"ERROR: Not able to send slack message: {str(e)}")
            return False
    
    def _generate_notification_message(self, summary_results):
        summary_message = ':wave: *unSkript Ctl Check Results* \n'
        status_count = {'PASS': 0, 'FAIL': 0, 'ERROR': 0}

        for result_set in summary_results:
            if not result_set:
                continue

            for check_name, status in result_set.get('result', []):
                if status in status_count:
                    status_count[status] += 1

                if status == 'PASS':
                    summary_message += f':hash: *{check_name}*  :white_check_mark: ' + '\n'
                elif status in ('FAIL', 'ERROR'):
                    summary_message += f':hash: *{check_name}*  :x: ' + '\n'

        summary_message += f':trophy: *(Pass/Fail/Error)* <-> *({status_count["PASS"]}/{status_count["FAIL"]}/{status_count["ERROR"]})*' + '\n\n'
        return summary_message


class EmailNotification(NotificationFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        config = self._config.get_notification()
        self.execution_dir = kwargs.get('execution_dir', './temp_folder')
        self.email_config = config.get('Email')
        self.provider = self.email_config.get('provider', '').lower()
        self.checks_schema_file = os.path.join(os.path.dirname(__file__), "unskript_email_notify_check_schema.json")


    def notify(self, **kwargs):
        pass 

    def validate_data(self, data, schema_file):
        if not os.path.exists(schema_file):
            self.logger.error(f"Data Differs From  Schema file {schema_file}!")
            return False  
        try:
            with open(self.schema_file, 'r') as f:
                schema = json.load(f)
                validate(instance=data, schema=schema)
                return True 
        except ValidationError as e:
            self.logger.error(e)
            return False 

    def create_tarball_archive(self, 
                               tar_file_name: str,
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
    
    def create_temp_files_of_failed_check_results(self, 
                                            failed_result: dict):
        list_of_failed_files = []
        if not failed_result:
            self.logger.error("Failed Result is Empty")
            return list_of_failed_files
        if not self.validate(failed_result, self.checks_schema_file):
            self.logger.error("Validation of Given Result failed against Notification Schema")
            return list_of_failed_files
        
        if failed_result and len(failed_result):
            connectors_list = [x.split(':')[0] for res in failed_result.get('result') for x in res.keys()]
            for connector in connectors_list:
                connector_file = self.execution_dir + f'/{connector}_failed_objects.txt'
                with open(connector_file, 'w', encoding='utf-8') as f:
                    for c_name, f_obj in failed_result.items():
                        if c_name.startswith(connector):
                            f.write('\n' + c_name + '\n')
                            f.write(yaml.dump(f_obj, default_flow_style=False))
                if connector_file not in list_of_failed_files:
                    list_of_failed_files.append(connector_file)

        return list_of_failed_files

    def create_script_summary_message(self, output_metadata_file: str):
        message = ''
        if os.path.exists(output_metadata_file) is False:
            self.logger.error(f"ERROR: The metadata file is missing, please check if file exists? {output_metadata_file}")
            return message

        metadata = ''
        with open(output_metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.loads(f.read())

        if not metadata:
            self.logger.error(f'ERROR: Metadata is empty for the script. Please check content of {output_metadata_file}')
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
    
    def create_email_attachment(self, output_metadata_file: str = None):
        """create_email_attachment: This function reads the output_metadata_file
        to find out the name of the attachment, the output that should be included as the attachment
        of the test run as listed in the output_metadata_file.
        """
        metadata = ''
        with open(output_metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.loads(f.read())

        if not metadata:
            self.logger.error(f'ERROR: Metadata is empty for the script. Please check content of {output_metadata_file}')
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
            if self.create_tarball_archive(tar_file_name=tar_file_name,
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
            self.logger.error(f"ERROR: {e}")

        return attachment_

    def create_checks_summary_message(self, 
                                      summary_results: list,
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
    
    def create_email_header(self, title: str = None):
        email_title = title or "unSkript-ctl run result"
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

    def prepare_combined_email(self, 
                               summary_results: list,
                               failed_result: dict,
                               output_metadata_file: str,
                               title: str,
                               attachment: MIMEMultipart):
        message = self.create_email_header(title=title)
        temp_attachment = msg = None
        if summary_results and len(summary_results):
            message += self.create_checks_summary_message(summary_results=summary_results,
                                                    failed_result=failed_result)
            self.create_temp_files_of_failed_results(failed_result=failed_result)
            parent_folder = self.execution_dir
            target_name = os.path.basename(parent_folder)
            tar_file_name = f"{target_name}" + '.tar.bz2'
            if self.create_tarball_archive(tar_file_name=tar_file_name,
                                    output_metadata_file=None,
                                    parent_folder=parent_folder) is False:
                self.logger.error("ERROR Archiving attachments")
                raise ValueError("ERROR: Archiving attachments failed!")
            target_file_name = tar_file_name
            msg = MIMEMultipart('mixed')
            with open(target_file_name, 'rb') as f:
                part = MIMEApplication(f.read())
                part.add_header('Content-Disposition', 'attachment', filename=target_file_name)
                msg.attach(part)

        if output_metadata_file:
            message += self.create_script_summary_message(output_metadata_file=output_metadata_file)
            temp_attachment = self.create_email_attachment(output_metadata_file=output_metadata_file)

        if failed_result and len(failed_result):
            message += '<br> <ul>' + '\n'
            message += '<h3> DETAILS ABOUT THE FAILED OBJECTS CAN BE FOUND IN THE ATTACHMENTS </h3>' + '\n'
            message += '</ul> <br>' + '\n'
        message += "</body> </html>"
        attachment.attach(MIMEText(message, 'html'))
        if temp_attachment:
            attachment.attach(temp_attachment)
        elif msg:
            attachment.attach(msg)

        return attachment

class SendgridNotification(EmailNotification):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sendgrid_config = self.email_config.get('Sendgrid')
    
    def notify(self, **kwargs):
        summary_results = kwargs.get('summary_results', [])
        failed_result = kwargs.get('failed_result', {})
        output_metadata_file = kwargs.get('output_metadata_file')
        from_email = kwargs.get('from_email', self.sendgrid_config.get('from-email'))
        to_email = kwargs.get('to_email', self.sendgrid_config.get('to-email'))
        api_key = kwargs.get('api_key', self.sendgrid_config.get('api_key'))
        subject = kwargs.get('subject', self.email_config.get('email_subject_line', 'Run Result'))

        
        return self.send_sendgrid_notification(summary_results=summary_results,
                                               failed_result=failed_result,
                                               output_metadata_file=output_metadata_file,
                                               from_email=from_email,
                                               to_email=to_email,
                                               api_key=api_key,
                                               subject=subject)
    def send_sendgrid_notification(self, 
                                summary_results: list,
                                failed_result: dict,
                                output_metadata_file: str,
                                from_email: str,
                                to_email: str,
                                api_key: str,
                                subject: str):
        # Dynamic Load (Import) necessary libraries for sendgrid
        import sendgrid
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType

        if not from_email or not to_email or not api_key:
            print("ERROR: From Email, To Email and API Key are mandatory parameters to send email notification")
            return False

        html_message = ''
        email_subject = subject
        parent_folder = self.execution_dir
        target_name = os.path.basename(parent_folder)
        tar_file_name = f"{target_name}" + '.tar.bz2'
        target_file_name = None
        metadata = None
        try:
            # We can have custom Title here
            html_message += self.create_email_header(title=None)
            if summary_results and len(summary_results):
                html_message += self.create_checks_summary_message(summary_results=summary_results,
                                                            failed_result=failed_result)
                self.create_temp_files_of_failed_results(failed_result=failed_result)
            if output_metadata_file:
                html_message += self.create_script_summary_message(output_metadata_file=output_metadata_file)
                with open(output_metadata_file, 'r') as f:
                    metadata = json.loads(f.read())
                if metadata and metadata.get('output_file'):
                    target_file_name = os.path.basename(metadata.get('output_file'))
                parent_folder = os.path.dirname(output_metadata_file)
                target_name = os.path.basename(parent_folder)
                tar_file_name = f"{target_name}" + '.tar.bz2'
            if metadata and metadata.get('compress') is True:
                output_metadata_file = output_metadata_file.split('/')[-1]
                if self.create_tarball_archive(tar_file_name=tar_file_name,
                                            output_metadata_file=output_metadata_file,
                                            parent_folder=parent_folder) is False:
                    raise ValueError("ERROR: Archiving attachments failed!")
                target_file_name = tar_file_name
            else:
                if self.create_tarball_archive(tar_file_name=tar_file_name,
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
                email_message = self.sendgrid_add_email_attachment(email_message=email_message,
                                                            file_to_attach=target_file_name,
                                                            compress=True)
            try:
                if tar_file_name:
                    os.remove(target_file_name)
            except Exception as e:
                self.logger.error(f"ERROR: {e}")

            sg = sendgrid.SendGridAPIClient(api_key)
            sg.send(email_message)
            self.logger.error(f"Notification sent successfully to {to_email}")
        except Exception as e:
            self.logger.error(f"ERROR: Unable to send notification as email. {e}")
            return False

        return True

    def sendgrid_add_email_attachment(self, 
                                      email_message,
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


class AWSEmailNotification(EmailNotification):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.aws_config = self.email_config.get('AWS')

    def notify(self, **kwargs):
        summary_results = kwargs.get('summary_results', [])
        failed_result = kwargs.get('failed_result', {})
        output_metadata_file = kwargs.get('output_metadata_file')
        access_key = kwargs.get('access_key', self.aws_config.get('access_key'))
        secret_key = kwargs.get('secret_key', self.aws_config.get('secret_access'))
        to_email = kwargs.get('to_email', self.aws_config.get('to-email'))
        from_email = kwargs.get('from_email', self.aws_config.get('from-email'))
        region = kwargs.get('region', self.aws_config.get('region'))
        subject = kwargs.get('subject', self.email_config.get('email_subject_line', 'Run Result'))

        return self.prepare_combined_email(summary_results=summary_results,
                                    failed_result=failed_result,
                                    output_metadata_file=output_metadata_file,
                                    access_key=access_key,
                                    secret_key=secret_key,
                                    to_email=to_email,
                                    from_email=from_email,
                                    region=region,
                                    subject=subject)

    def prepare_to_send_awsses_notification(self, summary_results: list,
                                failed_result: dict,
                                output_metadata_file: str,
                                access_key: str,
                                secret_key: str,
                                to_email: str,
                                from_email: str,
                                region: str,
                                subject: str):
        if not access_key or not secret_key:
            self.logger.error("ERROR: Cannot send AWS SES Notification without access and/or secret_key")
            return  False

        # WE CAN TAKE A TITLE AS WELL, IF WE WANT CUSTOM TITLE IN THE REPORT
        attachment_ = MIMEMultipart('mixed')
        attachment_['Subject'] = subject

        attachment_ = self.prepare_combined_email(summary_results=summary_results,
                                            failed_result=failed_result,
                                            output_metadata_file=output_metadata_file,
                                            title=None,
                                            attachment=attachment_)

        return self.do_send_awsses_email(from_email=from_email,
                                    to_email=to_email,
                                    attachment_=attachment_,
                                    access_key=access_key,
                                    secret_key=secret_key,
                                    region=region)

    def do_send_awsses_email(self, from_email: str,
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
                self.logger.info(f"Email notification sent to {to_email}")
            return True
        except NoCredentialsError:
            self.logger.error("ERROR: Unable to send email notification to {to_email}, credentials are invalid")
            return False
        except client.exceptions.MessageRejected:
            self.logger.error(f"ERROR: Unable to send email. Message was Rejected from SES server check from email-id {to_email} is valid!")
            return False
        except client.exceptions.MailFromDomainNotVerifiedException:
            self.logger.error("ERROR: Unable to send email. Domain of from email-id is not verified!, Please use a valid from email-id")
            return False
        except client.exceptions.ConfigurationSetDoesNotExistException:
            self.logger.error("ERROR: Unable to send email. Email Configuration set does not exist. Please check SES policy")
            return False
        except client.exceptions.ConfigurationSetSendingPausedException:
            self.logger.error(f"ERROR: Unable to send email. Email sending is paused for the from email id {from_email}!")
            return False
        except client.exceptions.AccountSendingPausedException:
            self.logger.error("ERROR: Unable to send email. Sending email is paused for the AWS Account!")
            return False
        except client.exceptions.ClientError as e:
            self.logger.error(f"ERROR: {e}")
            return False
        except Exception as e:
            self.logger.error(f"ERROR: {e}")
        return False
    
class SmtpNotification(EmailNotification):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SMTP_TLS_PORT = 587
        self.smtp_config = self.email_config.get('SMTP')

    def notify(self, **kwargs):
        summary_results = kwargs.get('summary_results', [])
        failed_result = kwargs.get('failed_result', {})
        output_metadata_file = kwargs.get('output_metadata_file')
        smtp_host = kwargs.get('smtp-host', self.smtp_config.get('smtp-host'))
        smtp_user = kwargs.get('smtp-user', self.smtp_config.get('smtp-user'))
        smtp_password = kwargs.get('smtp-password', self.smtp_config.get('smtp-password'))
        to_email = kwargs.get('to_email', self.smtp_config.get('to-email'))
        from_email = kwargs.get('from_email', self.smtp_config.get('from-email'))
        subject = kwargs.get('subject', self.email_config.get('email_subject_line', 'Run Result'))
        return self.send_smtp_notification(summary_results=summary_results,
                                           failed_result=failed_result,
                                           smtp_host=smtp_host,
                                           smtp_user=smtp_user,
                                           smtp_password=smtp_password,
                                           to_email=to_email,
                                           from_email=from_email,
                                           subject=subject)
    
    def send_smtp_notification(self,
                                summary_results: list,
                                failed_result: dict,
                                output_metadata_file: str,
                                smtp_host: str,
                                smtp_user: str,
                                smtp_password: str,
                                to_email: str,
                                from_email: str,
                                subject: str):
        """send_smtp_notification: This function sends the summary result
        in the form of an email for smtp option.
        """
        msg = MIMEMultipart('mixed')
        if from_email:
            msg['From'] =  from_email
        else:
            msg['From'] = smtp_user

        msg['To'] = to_email
        msg['Subject'] = subject
        try:
            server = smtplib.SMTP(smtp_host, self.SMTP_TLS_PORT)
            server.starttls()
            server.login(smtp_user, smtp_password)
        except Exception as e:
            self.logger.error(e)
            return False

        msg = self.prepare_combined_email(summary_results=summary_results,
                                    failed_result=failed_result,
                                    output_metadata_file=output_metadata_file,
                                    title=None,
                                    attachment=msg)

        try:
            server.sendmail(smtp_user, to_email, msg.as_string())
        except Exception as e:
            self.logger.error(f"ERROR: {e}")
        finally:
            self.logger.info(f"Notification sent successfully to {to_email}")

        return True
    
    # Usage:
    # n = Notification()
    # n.notify(
    #          mode='slack',   # slack, email or both, Mandatory parameter
    #          data_type='checks',  # checks, script or both, Mandatory parameter
    #          failed_objects=failed_objects,  # Failed objects from the checks run, Mandatory parameter
    #          output_metadata_file=None,  # Metadata that is generated after script run, Optional 
    #          summary_result=summary_result,  # Summary result of the run that includes pass,fail,error, Mandatory parameter
    #          to_email=to_email,   # Only applicable for `email` mode, Optional
    #          from_email=from_email,  # Only applicable for `email` mode, Optional
    #          subject=subject, # Only applicable for `email` mode, Optional
    #          access_key=access_key, # Only applicable for AWS SES email, Optional
    #          secret_access=secret_access,  # Only applicable for AWS SES email, Optional
    #          api_key=api_key, # Only applicable for sendgrid email, Optional
    #          smtp_host=smtp_host, # Only applicable for SMTP email, Optional
    #          smtp_user=smtp_user, # Only applicable for SMTP email, Optional
    #          smtp_password=smtp_password # Only applicable for SMTP email, Optional
    #          )
    class Notification(NotificationFactory):
        def __init__(self, **kwargs):
            pass
            super().__init__(**kwargs)

        def notify(self, **kwargs):
            mode = kwargs.get('mode', 'slack')
            result_type = kwargs.get('result_type', 'checks')
            result = kwargs.get('result', {})
            summary_result = kwargs.get('summary_result', [])
            output_metadata_file = kwargs.get('output_metadata_file')

            if mode.lower() == 'slack':
                pass 
            elif mode.lower() == 'email':
                pass 
            elif mode.lower() == 'both':
                pass 
            
            pass 
