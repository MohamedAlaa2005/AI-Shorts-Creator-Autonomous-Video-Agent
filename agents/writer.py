from graph.state import VideoState
from langchain_google_genai import ChatGoogleGenerativeAI

def writer_node(state: VideoState):
    """
    Writer Agent: A high-energy viral creator persona.
    """
    print("✍️ Writer: Crafting a viral masterpiece...")
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.8)
    
    # 1. Personality & System Instructions
    persona = (
        "You are 'The Hook Specialist,' a world-class YouTube Shorts creator. "
        "Your style is aggressive, fast-paced, and intensely engaging. "
        "You NEVER start with 'Here is the script' or 'Sure thing.' "
        "You only output the raw narration followed by the image prompts."
    )
    feedback = state.get("feedback", "No feedback yet. This is the first draft.")

    # 2. Detailed Viral Instructions
    user_instructions = (
        f"Critic Feedback: {feedback}\n\n"
        f"Base Material: {state['script']}\n\n"
        "STORYTELLING RE-WRITE RULES:\n"
        "1. THE HOOK: Open with a moment of high tension or a shocking choice. (e.g., 'He had 10 seconds to decide, or lose everything.')\n"
        "2. THE ARC: Structure the narration as: The Struggle -> The Unexpected Twist -> The Resolution.\n"
        "3. EMOTIONAL VIBE: Use sensory details (the smell of smoke, the cold wind) instead of raw facts.\n"
        "4. LANGUAGE: Use 'Storyteller' voice. Use active verbs. Avoid 'In this video we will see...'\n"
        "5. FORMAT: \n"
        "   - NARRATION: Write the script as a dramatic voiceover.\n"
        "   - PROMPTS: Exactly 10 cinematic image prompts labeled PROMPT 1: to PROMPT 10:.\n"
    )
    # 3. Combine Persona + Instructions
    # We use a combined string or a SystemMessage if your LangChain version prefers it
    full_prompt = f"{persona}\n\n{user_instructions}"
    
    response = llm.invoke(full_prompt)
    content = response.content

    # 4. Parsing the content
    # We look for 'PROMPT' to separate narration from the image generation instructions
    if "PROMPT 1" in content:
        parts = content.split("PROMPT 1")
        final_script = parts[0].strip()
        # Re-adding 'PROMPT 1' to the split list to keep the parsing consistent
        prompts_raw = "PROMPT 1" + parts[1]
        prompts = [p.strip() for p in prompts_raw.split("PROMPT") if p.strip()]
    else:
        # Fallback if the AI deviates
        final_script = content
        prompts = state.get("image_prompts", [])

    return {
        "script": final_script,
        "image_prompts": prompts,
        "retry_count": state.get("retry_count", 0) + 1
    }