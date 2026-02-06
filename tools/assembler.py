import asyncio
from tools.voice_gen import generate_voiceover
from tools.image_gen import generate_all_images
from moviepy import AudioFileClip, ImageClip, concatenate_videoclips
import numpy as np
import math
from PIL import Image
from pathlib import Path
import os
def zoom_effect(clip, zoom_ratio=0.04, direction='in'):
    """
    Direction: 'in' for Zoom In, 'out' for Zoom Out.
    """
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size
        
        # Reverse the math for Zoom Out
        if direction == 'in':
            scale = 1 + (zoom_ratio * t)
        else:
            # Start at max zoom (e.g., 1.2) and subtract over time
            # Assuming typical clip duration of 3-5 seconds
            max_zoom = 1 + (zoom_ratio * clip.duration)
            scale = max_zoom - (zoom_ratio * t)
            
        new_size = [
            math.ceil(base_size[0] * scale),
            math.ceil(base_size[1] * scale)
        ]
        
        # Ensure dimensions are even (required by most codecs)
        new_size[0] += (new_size[0] % 2)
        new_size[1] += (new_size[1] % 2)
        
        img = img.resize(new_size, Image.LANCZOS)
        
        # Center crop back to original size
        x = (new_size[0] - base_size[0]) // 2
        y = (new_size[1] - base_size[1]) // 2
        img = img.crop([x, y, new_size[0] - x, new_size[1] - y]).resize(base_size)
        
        return np.array(img)

    return clip.transform(effect)

async def assemble_assets(state):
    """
    Ensures folders exist and runs TTS/Image Gen in parallel.
    """
    # Create output directories using Path for cross-platform safety
    out_dir = Path("project_output")
    frames_dir = out_dir / "frames"
    out_dir.mkdir(parents=True, exist_ok=True)
    frames_dir.mkdir(parents=True, exist_ok=True)

    # Use clean, absolute strings for the tools
    audio_path = str(out_dir / "voice.mp3")
    
    # 1. Start TTS and Image Generation at the same time!
    audio_task = generate_voiceover(state['script'], audio_path)
    image_task = generate_all_images(state['image_prompts'],state['topic'])
    
    await asyncio.gather(audio_task, image_task)

def assembler_node(state):
    print("🎬 Assembler: Starting parallel asset generation...")
    
    # 1. Run the async asset gathering
    asyncio.run(assemble_assets(state))
    
    # 2. Define paths for loading
    audio_path = "project_output/voice.mp3"
    
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Missing audio file at {audio_path}")

    audio = AudioFileClip(audio_path)
    duration_per_clip = audio.duration / len(state['image_prompts'])
    
    # 3. Build the dynamic clips
    clips = []
    for i in range(len(state['image_prompts'])):
        img_path = f"project_output/frames/frame_{i}.jpg"
        
        if not os.path.exists(img_path):
            print(f"⚠️ Warning: Frame {i} missing, skipping...")
            continue

        clip = ImageClip(img_path).with_duration(duration_per_clip).with_fps(24)
        
        # Alternate zoom direction for a more professional feel
        direction = 'in' if i % 2 == 0 else 'out'
        clips.append(zoom_effect(clip, direction=direction))
        
    # 4. Final Export
    if not clips:
        return {"error": "No clips were generated."}

    final_video = concatenate_videoclips(clips, method="compose").with_audio(audio)
    
    # Sanitize topic name for filename
    safe_topic = "".join(x for x in state['topic'] if x.isalnum() or x in "._- ").strip().replace(" ", "_")
    output_path = f"project_output/{safe_topic}_final.mp4"
    
    print(f"🎥 Rendering final video to: {output_path}")
    
    final_video.write_videofile(
    output_path, 
    codec="libx264", 
    audio_codec="aac", 
    fps=24,
    # Use 'preset' to make rendering faster (ultrafast, superfast, medium)
    preset="medium",
    # ffmpeg_params ensures the video is strictly compatible with mobile players
    ffmpeg_params=["-pix_fmt", "yuv420p"] 
)
    
    return {"video_path": output_path}