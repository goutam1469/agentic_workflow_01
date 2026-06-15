"""

Agent logic powered by LLM

This file contains : 
-Planning (task decomposition)
- Tool use decisisons
-Reflection

"""

from typing import List, Dict, Any
from app.state import AgentState

## Planner

def plan_task(state: AgentState, llm_call) -> AgentState:
    """ 
    Uses the LLM to break a goal into a step by step plan
    """

    prompt = f"""

You are an autonomous AI agent.

Goal : {state['goal']}

Break the goal into smaller number of clear, executable steps
Return the steps as a numbered list.
"""
    
    response = llm_call(prompt)

    plan = [
        line.strip("0123456789. ").strip() 
        for line in response.split("\n")
        if line.strip()
    ]

    state["plan"] = plan
    state["current_step"] = 0
    state["done"] = False

    return state

## Action Decision

def decide_next_action(state: AgentState, llm_call) -> Dict[str: str]:
    """
    Asks the LLM what to do for the current step
    The LLM chooses between reasonsing or calling a tool
    """

    step = state["plan"][state["current_step"]]

    prompt = f"""

You are executing the following steps :

Step : {step}

Available tools : 
-calculator(expression: str)
-mock_retrieval(query: str)

Decide the best next action
Return ONLY one of the following formats :

REASON : <what will you reason about>
TOOL : <tool_name> | <input>
"""
    

## Reflection

def reflect_on_result(state: AgentState, llm_call) -> AgentState:
    """
    Uses the LLM to reflect on the last observation
    and decide whether to continue to finish
    """

    last_observation = (
        state["observations"][-1]
        if state["observations"]
        else "No observation produced yet"
    )

    prompt = f"""

You just eexecute a step with the following results : 
{last_observation}

Is this sufficient to complete the current step ?
Answer YES or NO with a short explanation
"""
    
    response = llm_call(prompt)

    if response.strip().lower().startswith("yes"):
        state["current_step"] += 1
    if state["current_step"] >= len(state["plan"]):
        state["done"] = True

    return state