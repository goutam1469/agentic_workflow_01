"""

LangGraph definition for the autonomous agent

This file wires together:

- PLanning
- Acting
- Memory Update
- Reflection
 into a controllable agentic loop

"""

from langgraph.graph import StateGraph
from app.state import AgentState
from app.agent import plan_task, decide_next_action, reflect_on_result


#Change this line
from app.tools import esc esc


# Tool Execution Node :

def execute_action(state: AgentState) -> AgentState:

    """
    Exectues the action decided by the agent
    this is where tool calls actually happen
    """

    decision = state["last_action"]

    if decision.startswith("TOOL:"):
        _, payload = decision.split("TOOL:", 1)
        tool_name, tool_input = payload.split("|", 1)

        # Write code for tool calling

    else :
        # Reason path
        result = decision
        state["observations"].append(result)

        return state


# Decision Node

def decide_node(state: AgentState, llm_call) -> AgentState:
    """
    Uses LLM to decide the next action
    """

    decision = decide_next_action(state, llm_call)
    state["last_action"] = decision["decision"]

    return state

# Graph Builder

def build_graph(llm_call):
    """
    Builds and returns the LangGraph app
    """

    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("plan", lambda s: plan_task(s, llm_call))
    graph.add_node("decide", lambda s: decide_node(s, llm_call))
    graph.add_node("act", execute_action)
    graph.add_node("reflect", lambda s: reflect_on_result(s, llm_call))

    # Entry
    graph.set_entry_point("plan")

    # Flow
    graph.add_edge("plan", "decide")
    graph.add_edge("decide", "act")
    graph.add_edge("act", "reflect")

    # Loop or finish
    graph.add_conditional_edges(
        "reflect",
        lambda s: "__end__" if s["done"] else "decide",
        {
            "decide": "decide",
            "__end__": "__end__"
        }
    )

    return graph.compile()