import asyncio
import edge_tts
import os

# Create output folder if it doesn't exist
os.makedirs("project_output", exist_ok=True)

async def generate_voiceover(text, output_filename="narration.mp3"):
    """
    Converts text to a professional neural voice.
    Recommended 2026 voices: 
    - Male: en-US-AndrewMultilingualNeural
    - Female: en-US-AvaMultilingualNeural
    """
    voice = "en-US-AndrewMultilingualNeural"
    output_path = os.path.join(output_filename)
    
    # communicate handles the connection to Microsoft's servers
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    
    print(f"✅ Voiceover saved: {output_path}")
    return output_path

