from graph.state import VideoState, CriticReview
from langchain_google_genai import ChatGoogleGenerativeAI

def critic_node(state: VideoState):
    print(f"⚖️ Critic: Grading Attempt {state['retry_count']}...")
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    # 1. Bind the Pydantic model to the LLM
    structured_llm = llm.with_structured_output(CriticReview)

    critic_prompt = (
        f"You are a YouTube Shorts Growth Expert. Evaluate this script:\n\n"
        f"SCRIPT: {state['script']}\n\n"
        "Critique the script based on:\n"
        "1. HOOK: Is the first sentence impossible to ignore?\n"
        "2. RETENTION: Are the sentences short and fast-paced?\n"
        "3. VISUALS: Do the image prompts match the narration?\n\n"
        "RETURN ONLY A JSON-LIKE FORMAT:\n"
        "SCORE: [0-10]\n"
        "FEEDBACK: [One specific instruction for the writer]"
    )
    # 2. Invoke the model (It returns a CriticReview object!)
    review = structured_llm.invoke(critic_prompt)
    
    # 3. Update the state with clean, validated data
    return {
        "critic_score": review.score,
        "feedback": review.feedback
    }