from __future__ import annotations

##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
## You must have the Sender email set up and 
#verified in AWS SES for this actio to work.
from pydantic import BaseModel, Field, SecretStr
from typing import Dict, List
import pprint



from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    Message: str = Field(
        ..., description='The body of the message to be sent.', title='Message'
    )
    Receiver: str = Field(
        ..., description='Email address to receive the message.', title='Receiver'
    )
    Region: str = Field(..., description='AWS Region', title='Region')
    Sender: str = Field(
        ..., description='Email address sending the message.', title='Sender'
    )
    Subject: str = Field(..., description='Subject line of the email.', title='Subject')



def aws_send_email_printer(output):
    if output is None:
        return
    pprint.pprint(output)

def aws_send_email(handle, Region:str, Sender:str, Receiver:str, Subject:str, Message:str) -> Dict:
    client = handle.client('ses', region_name=Region)
    # Create the email message
    message = {
        'Subject': {
            'Data': Subject
        },
        'Body': {
            'Text': {
                'Data': Message
            }
        }
    }

    # Send the email
    response = client.send_email(
        Source=Sender,
        Destination={
            'ToAddresses': [Receiver]
        },
        Message=message
    )

    # Print the response
    print(response)
    return response


