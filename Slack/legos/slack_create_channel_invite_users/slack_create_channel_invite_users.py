from __future__ import annotations

##
# Copyright (c) 2023 unSkript, Inc
# All rights reserved.
##
import pprint
from typing import List
from pydantic import BaseModel, Field
from slack_sdk import WebClient
## note: Your Slack App will need the files:write scope.
# Your Bot will also need to be a member of the channel




class InputSchema(BaseModel):
    channel: str = Field(..., description='Name of slack channel.', title='Channel')
    user_list: List = Field(
        ...,
        description='List of users to invite to the new channel.',
        title='user_list',
        #list is slack user IDs, for example ['U046UH5F2HZ']
    )



pp = pprint.PrettyPrinter(indent=2)


def slack_create_channel_invite_users_printer(output):
    if output is not None:
        pprint.pprint(output)
    else:
        return


def slack_create_channel_invite_users(
        handle: WebClient,
        channel: str,
        user_list: list) -> str:

    try:
        response = handle.conversations_create(
            name = channel,
            is_private=False
    )
        # Extract the ID of the created channel
        channel_id = response["channel"]["id"]
        for username in user_list:
            # Call the conversations.invite method to invite each user to the channel
            user_response=handle.conversations_invite(
                channel=channel_id,
                users=username
            )
            print(user_response)
            print(f"Invited user '{username}' to the channel.")

        return f"Successfully created Channel: #{channel}"

    except Exception as e:
        print("\n\n")
        pp.pprint(
            f"Failed sending message to slack channel {channel}, Error: {str(e)}")
        return f"Unable to send message on {channel}"


