from langgraph.graph import StateGraph, START, END
from agents.researcher import researcher_node
from agents.planner import planner_node
from agents.writer import writer_node
from agents.critic import critic_node
from agents.uploader_node import uploader_node
from tools.assembler import assembler_node 
from graph.state import VideoState

def should_continue(state: VideoState):
    # This matches the logic in your screenshot line 9-13
    if state["critic_score"] >= 2:
        return "media_engine" 
    else:
        return "writer"

workflow = StateGraph(VideoState)

# Add all nodes
workflow.add_node("researcher", researcher_node)
workflow.add_node("planner", planner_node)
workflow.add_node("writer", writer_node)
workflow.add_node("critic", critic_node)
workflow.add_node("media_engine", assembler_node) # Named media_engine to match your logic
workflow.add_node("uploader",uploader_node) 
# Define the flow
workflow.add_edge(START, "researcher")
workflow.add_edge("researcher", "planner")
workflow.add_edge("planner", "writer")
workflow.add_edge("writer", "critic")

# Add the conditional loop
workflow.add_conditional_edges(
    "critic",
    should_continue,
    {
        "media_engine": "media_engine",
        "writer": "writer"
    }
)

# Connect the final node to END
workflow.add_edge("media_engine", "uploader") 
workflow.add_edge("uploader", END)

