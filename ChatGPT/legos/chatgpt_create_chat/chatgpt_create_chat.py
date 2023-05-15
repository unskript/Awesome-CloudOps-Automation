from __future__ import annotations

##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel
from typing import Dict, List



from typing import List

from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    messages: List = Field(
        ..., description='The messages for Chat GPT', title='messages'
    )
    model: str = Field(
        ..., description='The ChatGPT Model to use in your query.', title='model'
    )
    temperature: float = Field(
        ...,
        description='The Temperature of the response.  Valid values are 0 to 2. Higher values will give more random results.',
        title='temperature',
    )


def chatgpt_create_chat(handle, model: str, messages:list, temperature:float)-> Dict:
    response = handle.ChatCompletion.create(
        model = model,
        messages = messages
    )
    return response






def unskript_default_printer(output):
    if isinstance(output, (list, tuple)):
        for item in output:
            print(f'item: {item}')
    elif isinstance(output, dict):
        for item in output.items():
            print(f'item: {item}')
    else:
        print(f'Output for {task.name}')
        print(output)

