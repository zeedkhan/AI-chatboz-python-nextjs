from typing import Dict, Any, List
from pydantic import BaseModel, validator
from backend.agent.utils.tool_fn import get_default_tool_name, get_tool_name


class AnalysisArguments(BaseModel):
    """
    Arguments for the analysis function of a tool. OpenAI functions will resolve these values but leave out the action.
    """

    reasoning: str
    arg: str = ""


class Analysis(AnalysisArguments):
    action: str

    @validator("action")
    def action_must_be_valid_tool(cls, v: str) -> str:
        # TODO: Remove circular import
        from backend.agent.utils.tool_fn import get_available_tools_names

        if v not in get_available_tools_names():
            raise ValueError(f"Analysis action '{v}' is not a valid tool")
        return v

    @validator("action")
    def action_must_have_arg(cls, v: str, values: Dict[str, str]) -> str:
        from backend.agent.agent_tools.reason import Reason

        if v != get_tool_name(Reason) and not values["arg"]:
            raise ValueError(f"Analysis arg cannot be empty if action is {v}")
        return v

    @classmethod
    def get_default_analysis(cls) -> "Analysis":
        # TODO: Remove circular import
        return cls(
            reasoning="Hmm... I'll have to try again",
            action=get_default_tool_name(),
            arg="Analyze the last output and find missing parts or summarize if satisfied the goal!",
        )
