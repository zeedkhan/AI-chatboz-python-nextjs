from backend.agent.tool import Tool
from typing import List, Type
from backend.agent.agent_tools.reason import Reason
from backend.agent.agent_tools.CustomCalculator import CustomCalculatorTool
from backend.agent.agent_tools.CustomSearchTool import CustomSearchTool
from backend.agent.agent_tools.GoogleCloudDatabaseQuery import GoogleCloudDatabaseSQLQuery
from backend.agent.agent_tools.GoogleCloud import GoogleCloudDatabases, GoogleCloudInstances, GoogleCloudGetDB, GoogleCloudAuth, GoogleCloudProject


def get_external_tools() -> List[Type[Tool]]:
    return [
        CustomCalculatorTool,
        CustomSearchTool,
        GoogleCloudDatabaseSQLQuery,
        GoogleCloudDatabases,
        GoogleCloudInstances,
        GoogleCloudGetDB,
        GoogleCloudProject
    ]


def format_tool_name(tool_name: str) -> str:
    return tool_name.lower()


def get_tool_name(tool: Type[Tool]) -> str:
    return format_tool_name(tool.__name__)


def get_tool_from_name(tool_name: str) -> Type[Tool]:
    for tool in get_available_tools():
        if get_tool_name(tool) == format_tool_name(tool_name):
            return tool


def get_user_tools(tool_names: List[str]) -> List[Type[Tool]]:
    return list(map(get_tool_from_name, tool_names)) + get_default_tools()


def get_available_tools() -> List[Type[Tool]]:
    return get_external_tools() + get_default_tools()


def get_available_tools_names() -> List[str]:
    return [get_tool_name(tool) for tool in get_available_tools()]


def get_default_tools() -> List[Type[Tool]]:
    return [
        Reason,
    ]


def get_tools_overview(tools: List[Type[Tool]]) -> str:
    """Return a formatted string of name: description pairs for all available tools"""

    # Create a list of formatted strings
    formatted_strings = [
        f"'{get_tool_name(tool)}': {tool.description}" for tool in tools
    ]

    # Remove duplicates by converting the list to a set and back to a list
    unique_strings = list(set(formatted_strings))

    # Join the unique strings with newlines
    return "\n".join(unique_strings)


def get_default_tool() -> Type[Tool]:
    return Reason


def get_default_tool_name() -> str:
    return get_tool_name(get_default_tool())
