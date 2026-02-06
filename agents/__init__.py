# agents/__init__.py
from .researcher import researcher_node
from .planner import planner_node
from .writer import writer_node
from .critic import critic_node

# This allows you to do: from agents import researcher_node, writer_node
__all__ = ["researcher_node", "planner_node", "writer_node", "critic_node"]