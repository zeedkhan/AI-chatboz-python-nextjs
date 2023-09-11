from langchain.schema import AgentAction, AgentFinish, OutputParserException, HumanMessage, BaseOutputParser
from langchain.agents.conversational_chat.output_parser import ConvoOutputParser
from langchain.agents import AgentOutputParser
from typing import Union, Any
import re
from langchain.output_parsers.json import parse_json_markdown
import json


class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split(
                    "Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
            # Action Input:
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            #  ValueError(f"Could not parse LLM output: `{llm_output}`")
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split(
                    "Final Answer:")[-1].strip()},
                log=llm_output,
            )

        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)


class NewAgentOutputParser(ConvoOutputParser):
    def get_format_instructions(self) -> str:
        return """RESPONSE FORMAT INSTRUCTIONS
        ----------------------------

        When responding to me, please output a response in one of two formats:

        **Option 1:**
        Use this if you want the human to use a tool.
        Markdown code snippet formatted in the following schema:

        ```json
        {{{{
            "action": string, \\ The action to take. Must be one of {tool_names}
            "action_input": string \\ The input to the action
        }}}}
        ```

        **Option #2:**
        Use this if you want to respond directly to the human. Markdown code snippet formatted in the following schema:

        ```json
        {{{{
            "action": "Final Answer",
            "action_input": string \\ You should put what you want to return to use here
        }}}}
        ```"""

    def parse(self, text: str) -> Any:
        print("-" * 20)
        cleaned_output = text.strip()
        # Regex patterns to match action and action_input
        action_pattern = r'"action":\s*"([^"]*)"'
        action_input_pattern = r'"action_input":\s*"([^"]*)"'

        # Extracting first action and action_input values
        action = re.search(action_pattern, cleaned_output)
        action_input = re.search(action_input_pattern, cleaned_output)

        if action:
            action_value = action.group(1)
            print(f"First Action: {action_value}")
        else:
            print("Action not found")

        if action_input:
            action_input_value = action_input.group(1)
            print(f"First Action Input: {action_input_value}")
        else:
            print("Action Input not found")

        print("-" * 40)
        if action:
            action_value = action.group(1)
            if action_value and action_input_value:
                return {"action": action_value, "action_input": action_input_value}

        # Problematic code left just in case
        if "```json" in cleaned_output:
            _, cleaned_output = cleaned_output.split("```json")
        if "```" in cleaned_output:
            cleaned_output, _ = cleaned_output.split("```")
        if cleaned_output.startswith("```json"):
            cleaned_output = cleaned_output[len("```json"):]
        if cleaned_output.startswith("```"):
            cleaned_output = cleaned_output[len("```"):]
        if cleaned_output.endswith("```"):
            cleaned_output = cleaned_output[: -len("```")]

        cleaned_output = cleaned_output.strip()

        response = json.loads(cleaned_output)
        return {"action": response["action"], "action_input": response["action_input"]}
        # end of problematic code
