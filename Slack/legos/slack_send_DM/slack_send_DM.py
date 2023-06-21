from __future__ import annotations

##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import pprint
from pydantic import BaseModel, Field
from slack_sdk import WebClient
from typing import Dict
## note: Your Slack App will need the:
#im:write  (for DM)
#mpim:write scope (for group IM messages).
# Your Bot will also need to be a member of the channel



from typing import List

from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    users: List = Field(..., description='List of users to DM', title='users')
    message: str = Field(..., description='Message to DM to users.', title='message')



pp = pprint.PrettyPrinter(indent=2)


def slack_send_DM_printer(output):
    if output is not None:
        pprint.pprint(output)
    else:
        return


def slack_send_DM(
        handle: WebClient,
        users: list,
        message:str) -> Dict:

    #slack takes in multiple users as a comma separated string
    comma_separated_users = ', '.join(str(user) for user in users)
    try:
        #open the DM
        createDM = handle.conversations_open(users=comma_separated_users)
        #get the ID
        channel_id = createDM['channel']['id']

        #send a message
        # Send message
        message_response = handle.chat_postMessage(channel=channel_id, text=message)
        return message_response['message']

    except Exception as e:
        print("\n\n")
        pp.pprint(
            f"Failed sending message to slack channel, Error: {str(e)}")
        return f"Unable to send message "


