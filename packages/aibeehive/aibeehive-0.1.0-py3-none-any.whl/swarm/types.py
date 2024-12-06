from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
    Function,
)
from typing import List, Callable, Union, Optional

# Third-party imports
from pydantic import BaseModel

BeeFunction = Callable[[], Union[str, "Bee", dict]]


class Bee(BaseModel):
    name: str = "Bee"
    model: str = "gpt-4o"
    instructions: Union[str, Callable[[], str]] = "You are a helpful bee."
    functions: List[BeeFunction] = []
    tool_choice: str = None
    parallel_tool_calls: bool = True


class Response(BaseModel):
    messages: List = []
    bee: Optional[Bee] = None
    context_variables: dict = {}


class Result(BaseModel):
    """
    Encapsulates the possible return values for an bee function.

    Attributes:
        value (str): The result value as a string.
        bee (Bee): The bee instance, if applicable.
        context_variables (dict): A dictionary of context variables.
    """

    value: str = ""
    bee: Optional[Bee] = None
    context_variables: dict = {}
