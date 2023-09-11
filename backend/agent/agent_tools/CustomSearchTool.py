from backend.agent.tool import Tool


class CustomSearchTool(Tool):

    # name = "Search"
    description = "Useful when you need to search information on the internet"

    async def call(
        self, goal: str, task: str, input_str: str
    ) -> str:
        """Use the tool asynchronously."""
        
        return ""

        raise NotImplementedError("Search does not support async")
