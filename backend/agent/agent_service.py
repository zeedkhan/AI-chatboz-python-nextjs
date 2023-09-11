from typing import List, Optional, Protocol
from backend.agent.analysis import Analysis
from fastapi.responses import StreamingResponse as FastAPIStreamingResponse

# class AgentService(Protocol):
#     async def start_goal_agent(self, *, goal: str) -> List[str]:
#         pass

#     async def analyze_task_agent(
#         self, *, goal: str, task: str, tool_names: List[str]
#     ) -> Analysis:
#         pass

#     async def execute_task_agent(
#         self,
#         *,
#         goal: str,
#         task: str,
#         analysis: Analysis,
#     ) -> FastAPIStreamingResponse:
#         pass

#     async def create_tasks_agent(
#         self,
#         *,
#         goal: str,
#         tasks: List[str],
#         last_task: str,
#         result: str,
#         completed_tasks: Optional[List[str]] = None,
#     ) -> List[str]:
#         pass

#     async def summarize_task_agent(
#         self,
#         *,
#         goal: str,
#         results: List[str],
#     ) -> FastAPIStreamingResponse:
#         pass

#     async def chat(
#         self,
#         *,
#         message: str,
#         results: List[str],
#     ) -> FastAPIStreamingResponse:
#         pass

class AgentService():
    async def start_goal_agent(self, *, goal: str) -> List[str]:
        pass

    async def analyze_task_agent(
        self, *, goal: str, task: str, tool_names: List[str]
    ) -> Analysis:
        pass

    async def execute_task_agent(
        self,
        *,
        goal: str,
        task: str,
        analysis: Analysis,
    ) -> FastAPIStreamingResponse:
        pass

    async def create_tasks_agent(
        self,
        *,
        goal: str,
        tasks: List[str],
        last_task: str,
        result: str,
        completed_tasks: Optional[List[str]] = None,
    ) -> List[str]:
        pass

    async def summarize_task_agent(
        self,
        *,
        goal: str,
        results: List[str],
    ) -> FastAPIStreamingResponse:
        pass

    async def chat(
        self,
        *,
        message: str,
        results: List[str],
    ) -> FastAPIStreamingResponse:
        pass