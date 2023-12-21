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
from unittest.mock import patch, MagicMock

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

if __name__ == '__main__':
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
    
    try:
        from unskript_ctl_notification import SlackNotification
    except Exception as e:
        print(f"ERROR: {e}")
    
    unittest.main()