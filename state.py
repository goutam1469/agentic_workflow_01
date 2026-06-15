from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    """

    Shared state for the autonomous agent>

    Every node in the LangGraph reads from and writes to this structure

    This is the ONLY way agents communicate and evolve over time
    """

    goal : str # High level user goal
    
    plan : List[str] # Planner output : ordered list of steps

    current_step : int # Index of the current step being executed

    observations : List[str] # Observations from tools or reasoning steps

    memory : List[str] # Long lived memory accumulated during execution

    last_action : Optional[str] # Last action taken by the agent(tool name, reasoning, reflect, etc)

    done : bool # Flag to signal completion
    