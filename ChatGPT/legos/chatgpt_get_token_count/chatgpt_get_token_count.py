from __future__ import annotations

##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
#Note - this requires the tiktoken library to be installed
from pydantic import BaseModel
import tiktoken



from typing import List

from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    messages: List = Field(..., description='Your Chat GPT message', title='messages')
    model: str = Field(..., description='The ChatGOT Model', title='model')





def chatgpt_get_token_count(handle, messages: list, model: str):
  """Returns the number of tokens used by a list of messages."""
  try:
      encoding = tiktoken.encoding_for_model(model)
  except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")
  if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name":  # if there's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
      num_tokens += 2  # every reply is primed with <im_start>assistant
      return num_tokens
  else:
      raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")


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

