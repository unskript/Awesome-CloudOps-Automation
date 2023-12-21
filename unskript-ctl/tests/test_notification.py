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
import sys
import unittest
from unittest.mock import patch, Mock, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

try:
    from unskript_ctl_notification import SlackNotification, Notification, SmtpNotification
except Exception as e:
    print(f"ERROR: {e}")

class TestSlackNotification(unittest.TestCase):
    @patch('unskript_ctl_notification.requests.post')
    def test_notify_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = "OK"

        # Mocking summary results
        summary_results = [
            {'result': [('Check1', 'PASS'), ('Check2', 'FAIL')]},
            {'result': [('Check3', 'ERROR'), ('Check4', 'PASS')]}
        ]

        slack = SlackNotification()
        result = slack.notify(summary_result_table=summary_results)

        self.assertTrue(result)
        mock_post.assert_called_once()

    @patch('unskript_ctl_notification.requests.post')
    def test_notify_failure(self, mock_post):
        mock_post.return_value.status_code = 500
        mock_post.return_value.text = "Internal Server Error"

        # Mocking empty summary results
        summary_results = []

        slack = SlackNotification()
        result = slack.notify(summary_result_table=summary_results)

        self.assertFalse(result)

    def test_generate_notification_message(self):
        slack = SlackNotification()

        summary_results = [
            {'result': [('Check1', 'PASS'), ('Check2', 'FAIL')]},
            {'result': [('Check3', 'ERROR'), ('Check4', 'PASS')]}
        ]

        expected_message = (
            ':wave: *unSkript Ctl Check Results* \n'
            ':hash: *Check1*  :white_check_mark: \n'
            ':hash: *Check2*  :x: \n'
            ':hash: *Check3*  :x: \n'
            ':hash: *Check4*  :white_check_mark: \n'
            ':trophy: *(Pass/Fail/Error)* <-> *(2/1/1)*\n\n'
        )

        message = slack._generate_notification_message(summary_results)
        self.assertEqual(message, expected_message)




# Import the Notification class and other necessary classes here
class TestNotification(unittest.TestCase):
    def setUp(self):
        # Initialize any necessary objects or configurations
        pass

    def tearDown(self):
        # Clean up after each test case, if needed
        pass

    @patch('unskript_ctl_notification.SlackNotification.notify')  # Replace 'path.to' with the actual path
    def test_slack_notification(self, mock_slack_notify):
        # Mock the SlackNotification.notify method
        mock_slack_notify.return_value = True  # Mock the return value
        summary_result = [
            {'result': [('Check1', 'PASS'), ('Check2', 'FAIL')]},
            {'result': [('Check3', 'ERROR'), ('Check4', 'PASS')]}
        ]

        notification = Notification()
        result = notification.notify(mode='slack', summary_result=summary_result)
        mock_slack_notify.assert_called_once_with(summary_results=summary_result)
        self.assertTrue(result)  # Assert that the Slack notification was successful

    @patch('unskript_ctl_notification.SmtpNotification.notify')  # Replace 'path.to' with the actual path
    def test_email_notification(self, mock_smtp_notify):
        # Mock the SmtpNotification.notify method
        mock_smtp_notify.return_value = True  # Mock the return value
        summary_result = [
            {'result': [('Check1', 'PASS'), ('Check2', 'FAIL')]},
            {'result': [('Check3', 'ERROR'), ('Check4', 'PASS')]}
        ]

        failed_objects = {"result": [{"check1": ["object1", "object2"]}]}  # Provide a sample of failed objects
        to_email = 'test@example.com'  # Provide a sample recipient email
        from_email = 'sender@example.com'  # Provide a sample sender email
        subject = 'Test Subject'  # Provide a sample subject
        notification = Notification()
        result = notification.notify(mode='email', summary_result=summary_result, failed_objects=failed_objects,
                                     to_email=to_email, from_email=from_email, subject=subject)
        mock_smtp_notify.assert_called_once_with(
            summary_result=summary_result,
            failed_result=failed_objects,
            output_metadata_file=None,  # Mock other kwargs as needed
            smtp_host=None,
            smtp_user=None,
            smtp_password=None,
            to_email=to_email,
            from_email=from_email,
            subject=subject
        )
        self.assertTrue(result)  # Assert that the Email notification was successful

    @patch.multiple('unskript_ctl_notification.SlackNotification', notify=Mock(return_value=True))
    @patch.multiple('unskript_ctl_notification.SmtpNotification', notify=Mock(return_value=True))
    def test_both_notification(self):
        summary_result = [
            {'result': [('Check1', 'PASS'), ('Check2', 'FAIL')]},
            {'result': [('Check3', 'ERROR'), ('Check4', 'PASS')]}
        ]
        failed_objects = {"result": [{"check1": ["object1", "object2"]}]}  # Provide a sample of failed objects
        to_email = 'test@example.com'  # Provide a sample recipient email
        from_email = 'sender@example.com'  # Provide a sample sender email
        subject = 'Test Subject'  # Provide a sample subject
        notification = Notification()
        result = notification.notify(mode='both', summary_result=summary_result, failed_objects=failed_objects,
                                     to_email=to_email, from_email=from_email, subject=subject)
        self.assertTrue(result)  # Assert that both Slack and Email notifications were successful


if __name__ == '__main__':
    unittest.main()