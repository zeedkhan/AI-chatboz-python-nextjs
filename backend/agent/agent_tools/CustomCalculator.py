from backend.agent.tool import Tool
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Optional, Type
from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
)
from langchain import LLMMathChain
from dotenv import load_dotenv
import os


load_dotenv()
open_ai_key = os.getenv("OPENAI_API_KEY")
print(open_ai_key)


class CustomCalculatorTool(Tool):
    name = "Calculator"
    llm = ChatOpenAI(temperature=0)
    description = (
        "useful for when you need to answer questions about math"
    )
    args_schema = "Calculator"
    public_args_schema = "Calculator"

    async def call(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        llm_math_chain = LLMMathChain(llm=self.llm, verbose=True)
        return llm_math_chain.run(query)
