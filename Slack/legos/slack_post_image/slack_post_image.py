##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

import pprint

from pydantic import BaseModel, Field
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

pp = pprint.PrettyPrinter(indent=2)

from beartype import beartype

## note: Your Slack App will need the files:write scope.  Your Bot will also need to be a member of the channel

class InputSchema(BaseModel):
    channel: str = Field(
        title='Channel',
        description='Name of slack channel.')
    message: str = Field(
        title='message',
        description='Message for slack channel.')
    image: str = Field(
        title='image',
        description='Path to image to be sent.')

@beartype
def slack_post_image_printer(output):
    if output is not None:
        pprint.pprint(output)
    else:
        return


@beartype
def slack_post_image(
        handle: WebClient,
        channel: str,
        message:str,
        image: str) -> str:

    try:
        result = handle.files_upload(
            channels = channel,
            initial_comment=message,
            file=image
    )
        return f"Successfully Sent Message on Channel: #{channel}"

    except Exception as e:
        print("\n\n")
        pp.pprint(
            f"Failed sending message to slack channel {channel}, Error: {e.__str__()}")
        return f"Unable to send message on {channel}"
