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

class InputSchema(BaseModel):
    channel: str = Field(
        title='Channel',
        description='Name of slack channel.')
    message: str = Field(
        title='Message',
        description='Message for slack channel.')

@beartype
def slack_post_message_printer(output):
    if output is not None:
        pprint.pprint(output)
    else:
        return


@beartype
def slack_post_message(
        handle: WebClient,
        channel: str,
        message: str) -> str:

    try:
        response = handle.chat_postMessage(
            channel=channel,
            text=message)
        return f"Successfully Sent Message on Channel: #{channel}"
    except SlackApiError as e:
        pp.pprint(
            f"Failed sending message to slack channel {channel}, Error: {e.response['error']}")
        if e.response['error'] == 'channel_not_found':
            raise Exception('Channel Not Found')
        elif e.response['error'] == 'duplicate_channel_not_found':
            raise Exception('Channel associated with the message_id not valid')
        elif e.response['error'] == 'not_in_channel':
            raise Exception('Cannot post message to channel user is not in')
        elif e.response['error'] == 'is_archived':
            raise Exception('Channel has been archived')
        elif e.response['error'] == 'msg_too_long':
            raise Exception('Message text is too long')
        elif e.response['error'] == 'no_text':
            raise Exception('Message text was not provided')
        elif e.response['error'] == 'restricted_action':
            raise Exception('Workspace preference prevents user from posting')
        elif e.response['error'] == 'restricted_action_read_only_channel':
            raise Exception('Cannot Post message, read-only channel')
        elif e.response['error'] == 'team_access_not_granted':
            raise Exception('The token used is not granted access to the workspace')
        elif e.response['error'] == 'not_authed':
            raise Exception('No Authtnecition token provided')
        elif e.response['error'] == 'invalid_auth':
            raise Exception('Some aspect of Authentication cannot be validated. Request denied')
        elif e.response['error'] == 'access_denied':
            raise Exception('Access to a resource specified in the request denied')
        elif e.response['error'] == 'account_inactive':
            raise Exception('Authentication token is for a deleted user')
        elif e.response['error'] == 'token_revoked':
            raise Exception('Authentication token for a deleted user has been revoked')
        elif e.response['error'] == 'no_permission':
            raise Exception('The workspace toekn used does not have necessary permission to send message')
        elif e.response['error'] == 'ratelimited':
            raise Exception('The request has been ratelimited. Retry sending message later')
        elif e.response['error'] == 'service_unavailable':
            raise Exception('The service is temporarily unavailable')
        elif e.response['error'] == 'fatal_error':
            raise Exception('The server encountered catostrophic error while sending message')
        elif e.response['error'] == 'internal_error':
            raise Exception('The server could not complete operation, likely due to transietn issue')
        elif e.response['error'] == 'request_timeout':
            raise Exception('Sending message error via POST: either message was missing or truncated')
        else:
            raise Exception(f'Failed Sending Message to slack channel {channel} Error: {e.response["error"]}')

    except Exception as e:
        print("\n\n")
        pp.pprint(
            f"Failed sending message to slack channel {channel}, Error: {e.__str__()}")
        return f"Unable to send message on {channel}"