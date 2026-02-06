import os
from tools.search_tool import get_search_tool
from langchain_google_genai import ChatGoogleGenerativeAI 
from graph.state import VideoState
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()

def researcher_node(state: VideoState):
    # Get the topic from the state dictionary safely
    topic = state.get("topic", "Latest AI Tech Trends")
    print(f"🔍 Researcher: Investigating {topic}...")

    search_tool = get_search_tool()
    
    # 1. Create a dynamic tool map to prevent KeyErrors
    # This maps the tool's internal name to the tool object
    tools = [search_tool]
    tool_map = {tool.name.lower(): tool for tool in tools}

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    llm_with_tools = llm.bind_tools(tools)

    # 2. First Call: Model decides to use the tool
    messages = [HumanMessage(content=f"Find the 5 most shocking facts about {topic}.")]
    ai_msg = llm_with_tools.invoke(messages)

    # 3. Check for Tool Calls
    if ai_msg.tool_calls:
        print("🛠️ Model is calling the Search Tool...")
        messages.append(ai_msg)
        
        for tool_call in ai_msg.tool_calls:
            # Look up the tool by the name the AI requested
            tool_name = tool_call["name"].lower()
            selected_tool = tool_map.get(tool_name)
            
            if selected_tool:
                tool_output = selected_tool.invoke(tool_call["args"])
                messages.append(ToolMessage(
                    content=str(tool_output), 
                    tool_call_id=tool_call["id"]
                ))
            else:
                print(f"❌ Error: Tool '{tool_name}' not found in map.")

        # 4. Final Call: Summarize the results
        final_response = llm_with_tools.invoke(messages)
        ai_report = final_response.content
    else:
        ai_report = ai_msg.content

    print(f"✅ Final Report Generated!")
    return {
        "search_results": ai_report,
        "is_trending": True if ai_report else False
    }