from typing import TypedDict, List, Optional
from pydantic import BaseModel, Field

# Pydantic model for structured Critic feedback
class CriticReview(BaseModel):
    score: int = Field(description="Score from 1-10", ge=1, le=10)
    feedback: str = Field(description="Detailed rewrite instructions")

# The Main Graph State
class VideoState(TypedDict):
    topic: str
    search_results: str
    script: str
    image_prompts: List[str]
    critic_score: int
    retry_count: int
    feedback: Optional[str] # Stores the Critic's notes
    video_path: Optional[str] # Final MP4 location