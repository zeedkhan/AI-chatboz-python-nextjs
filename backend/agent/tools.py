from langchain.chat_models import ChatOpenAI
from typing import List, Set
import re
import os
from dotenv import load_dotenv
from langchain.schema import HumanMessage, SystemMessage
from backend.agent.tool import Tool


load_dotenv()
open_ai_key = os.getenv("OPENAI_API_KEY")


class Tools():
    def __init__(self):
        pass

    def get_all_agents(self, agent):

        all_agents = [agent]
        for current_agent in all_agents:
            for child_agent in current_agent.child:
                all_agents.extend(self.get_all_agents(child_agent))
        return all_agents

    def get_all_agents_with_parents(self, agent):
        all_agents = []
        uuid_set = set()  # Set to store unique UUIDs

        current_agent = agent  # Use a different variable name here

        while current_agent is not None:
            agents_to_add = self.get_all_agents(current_agent)

            # Add only the agents that are not already in the uuid_set
            for agent in agents_to_add:
                if agent.uuid not in uuid_set:
                    all_agents.append(agent)
                    uuid_set.add(agent.uuid)

            current_agent = current_agent.parent

        return all_agents

    def _transform_agent(self, names: List[str], build_in_tools: List[Tool] = []) -> List[Tool]:
        # Create a set to store the names of tools already encountered
        encountered_names: Set[str] = set()

        # Create a list to store the merged tools (self.tools and build_in_tools)
        merged_tools: List[Tool] = []

        # Add self.tools to the merged_tools list while avoiding duplicates
        for tool in self.tools:
            if tool.name not in encountered_names:
                merged_tools.append(tool)
                encountered_names.add(tool.name)

        # Add build_in_tools to the merged_tools list while avoiding duplicates
        for tool in build_in_tools:
            if tool.name not in encountered_names:
                merged_tools.append(tool)
                encountered_names.add(tool.name)

        # Filter the merged tools based on the names provided in the input list
        agent_tools = [tool for tool in merged_tools if tool.name in names]

        # print(agent_tools)

        return agent_tools

    def process_command_find_agent(self, *args, **kwargs):
        # Check if the first argument is a string (command string)
        # Use RegEx to match the command and value

        for conversation in args:
            conversation = "".join(conversation)

            match = re.match(r'(\S+)\s+agent\s+(.+)',
                             conversation, re.IGNORECASE)
            if match:
                command = match.group(1)
                agent_name = match.group(2)

                return {
                    "status": "success",
                    "value": agent_name
                }

        return {
            "status": "failed",
            "value": f"Invalid command format. Please follow format 'Find agent [name]'"
        }

    def process_command_switch_agent(self, *args, **kwargs):
        regex_pattern = r"From agent (.+?), To agent (.+)"

        for conversation in args:
            conversation = "".join(conversation)

            match = re.search(regex_pattern, conversation)

            if match:
                from_agent = match.group(1).strip()
                to_agent = match.group(2).strip()
                if from_agent != to_agent:
                    return {
                        "status": "success",
                        "value": {
                            "from": from_agent,
                            "to": to_agent
                        }
                    }
                else:
                    return {
                        "status": "failed",
                        "value": "Couldn't switch from yourself, to yourself"
                    }

        return {
            "status": "failed",
            "value": f"Invaid command format. Please follow format 'From agent [your name], To agent [the new agent name]'"
        }

    def process_command_check_authority_agent(self, *args, **kwargs):
        # Check if the first argument is a string (command string)
        # Use RegEx to match the command and value

        for conversation in args:
            conversation = "".join(conversation)

            match = re.match(r'(\S+)\s+authority agent\s+(.+)',
                             conversation, re.IGNORECASE)
            if match:
                command = match.group(1)
                agent_name = match.group(2)

                return {
                    "status": "success",
                    "value": agent_name
                }

        return {
            "status": "failed",
            "value": f"Invalid command format. Please follow format 'Check authority agent [name]'"
        }