from typing import Type, TypedDict

from backend.agent.tool import Tool
from backend.agent.utils.tool_fn import get_tool_name


class FunctionDescription(TypedDict):
    """Representation of a callable function to the OpenAI API."""

    name: str
    """The name of the function."""
    description: str
    """A description of the function."""
    parameters: dict[str, object]
    """The parameters of the function."""


def get_tool_function(tool: Type[Tool]) -> FunctionDescription:
    """A function that will return the tool's function specification"""
    name = get_tool_name(tool)
    parent = None
    if tool.parent:
        parent = get_tool_name(tool.parent)

    return {
        "name": name,
        "description": tool.description,
        "parent_function": parent,
        "parameters": {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string",
                    "description": (
                        f"Reasoning is how the task will be accomplished with the current function. "
                        "Detail your overall plan along with any concerns you have."
                        "Ensure this reasoning value is in the user defined langauge "
                    ),
                },
                "arg": {
                    "type": "string",
                    "description": tool.arg_description,
                },
            },
            "required": ["reasoning", "arg"],
        },
    }
