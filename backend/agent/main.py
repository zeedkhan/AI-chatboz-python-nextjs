from fastapi import FastAPI, Depends
from backend.agent.chatbot import OpenAIAgentService


app = FastAPI()


@app.get("/start")
async def start_tasks_agent():
    goal = "How far from Malaysia to England?"

    new_tasks = await OpenAIAgentService().start_goal_agent(goal, lang="English")

    output = {
        "goal": goal,
        "all_tasks": new_tasks,
        "subtask": [],
        "action": []
    }

    analyze_task = await OpenAIAgentService().analyze_task_agent(goal=goal, task=new_tasks[0])

    exec_t_1 = await OpenAIAgentService().execute_task_agent(goal=goal, task=new_tasks[0], analysis=analyze_task)

    output["subtask"].append(analyze_task)
    output["action"].append(exec_t_1)

    return {
        "tasks": output
    }

    # testTask = tasks[0]

    # analysis = await analyze_task_agent(
    #     goal=goal,
    #     task=testTask,
    #     tool_names=[]
    # )
    # return tasks


@app.get("/")
def read_root():
    return {"Hello": "World"}
