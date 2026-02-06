from graph.state import VideoState
from langchain_google_genai import ChatGoogleGenerativeAI

def planner_node(state: VideoState):
    """
    Planner Agent: Organizes search data into a viral storyboard structure.
    """
    print("📋 Planner: Organizing facts into a storyboard...")
    
    # 1. Initialize the 'Brain'
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    
    # 2. Craft the instructions
    # We ask for a "Storyboard" that the Writer can easily follow.
    prompt = (
        f"You are a YouTube Shorts Strategist. Review these research results: {state['search_results']}\n\n"
        "Create a 3-part storyboard for a 60-second video:\n"
        "1. THE HOOK: A controversial or shocking opening statement.\n"
        "2. THE CORE: 2-3 key facts presented in a fast-paced sequence.\n"
        "3. THE CTA: A quick call-to-action to like or subscribe.\n\n"
        "Keep the plan concise and high-energy."
    )
    
    plan_output = llm.invoke(prompt)
    
    # 3. Update the state
    # We keep the topic and search_results, but add the new storyboard plan.
    return {
        "search_results": state['search_results'], # Pass along for the writer
        "script": plan_output.content  # The Planner's 'script' is actually the Storyboard
    }