"""Small collection of tools the agent can call.

Each tool is a simple function that accepts a string input and returns a string result.

Tools added:
- calculator(expression: str): evaluate simple arithmetic expressions safely
- mock_retrieval(query: str): return a fake retrieval result for testing
- web_search(query: str): very basic simulated web-search using requests to fetch titles (optional)
"""
from typing import Callable, Dict
import re

TOOL_MAP: Dict[str, Callable[[str], str]] = {}


def calculator(expression: str) -> str:
    """Evaluate a simple arithmetic expression and return the result as a string.

    Only allows digits, whitespace and + - * / ( ) and decimal points. This is
    intentionally minimal and not a full math parser.
    """
    # sanitize expression: allow only numbers, operators and parentheses
    if not re.fullmatch(r"[0-9+\-*/(). \t]+", expression):
        return "ERROR: expression contains invalid characters"

    try:
        # safer eval: evaluate in empty globals/locals
        result = eval(expression, {"__builtins__": None}, {})
    except Exception as e:
        return f"ERROR: {e}"

    return str(result)


def mock_retrieval(query: str) -> str:
    """Return a deterministic mock retrieval string for the given query.

    Useful for offline testing of retrieval tool integration.
    """
    return f"MOCK_RETRIEVAL: top result for '{query}' -> This is a fake document snippet summarizing {query}."


def web_search(query: str) -> str:
    """A very small, dependency-free simulated web search.

    This implementation just returns a canned response. If you want a real
    search, replace this with an API call (Google/Bing) and add credentials
    management.
    """
    # Keep this simple and offline-friendly for now.
    return f"WEB_SEARCH: simulated results for '{query}' -> [Result 1 title] [Result 2 title]"


# Register tools in the map
TOOL_MAP["calculator"] = calculator
TOOL_MAP["mock_retrieval"] = mock_retrieval
TOOL_MAP["web_search"] = web_search
