from typing import List
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.youtube_uploader import upload_video
from graph.state import VideoState
import os
# 1. Define the structure you want
class VideoMetadata(BaseModel):
    title: str = Field(description="A viral, catchy YouTube title under 100 characters.")
    hashtags: List[str] = Field(description="A list of 3-5 trending hashtags relevant to the content.")

def uploader_node(state: VideoState):
    print("🧠 Uploader: Generating structured SEO metadata...")
    
    # 2. Setup the model with structured output
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    structured_llm = llm.with_structured_output(VideoMetadata)
    
    script_context = state.get("script", "")
    topic = state.get("topic", "AI Trends")
    
    prompt = (
        f"Analyze this script: '{script_context}' and topic: '{topic}'. "
        "Create a high-retention title and a list of trending hashtags."
    )
    
    # 3. Invoke and get back a Python Object (not a string!)
    metadata = structured_llm.invoke(prompt)
    
    print(f"🎬 Title: {metadata.title}")
    print(f"🏷️ Hashtags: {', '.join(metadata.hashtags)}")
    topic=topic.replace(" ","_")
    # 4. Prepare for upload
    video_path = f"project_output/{topic}_final.mp4"
    
    # Format description with the structured hashtags
    formatted_hashtags = " ".join([f"#{h.strip('#')}" for h in metadata.hashtags])
    description = f"{script_context}\n\n{formatted_hashtags}"

    # 5. Execute the Upload
    if os.path.exists(video_path):
        try:
            video_id = upload_video(video_path, metadata.title, description)
            print(f"✅ Video LIVE: https://youtu.be/{video_id}")
            return {"is_uploaded": True, "title": metadata.title}
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            return {"is_uploaded": False}
    
    return {"is_uploaded": False}

