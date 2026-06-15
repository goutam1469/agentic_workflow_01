"""
Entry point for the autonomous agent framework
    
This file :
- Defines the LLM interface (llm_call)
- Initializes the agent
- Runs the LangGraph agent loop

"""

from app.state import AgentState
from app.graph import build_graph

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key = os.getenv("NVIDIA_API_KEY")
    base_url = "" #Paste the URL of model
)

def llm_call(prompt: str) -> str:
    response = client.chat.completions.create(
        model = "" # paste the nvidia model
        messages = [
            {"role" : "system", "content" : "You are a helpful autonomous AI agent."},
            {"role" : "user", "content" : prompt},
        ],
        temperature=0.3,
    )

    return response.cjoices[0].messages.content

# Main

def main():

    # Initial state

    initial_state: AgentState={
        "goal" : "Learn what agentic AI is",
        "plan" : [],
        "current_step" : 0,
        "observations" : [],
        "memory" : [],
        "last_action" : None,
        "done" : False,
    }

    # Build and run the graph

    app = build_graph(llm_call)
    final_state = app.invoke(initial_state)

    # Output
    print("\n FINAL STATE")
    for key, value in final_state.items():
        print(f"{key}:{value}")


if __name__ == "__main__":
    main()