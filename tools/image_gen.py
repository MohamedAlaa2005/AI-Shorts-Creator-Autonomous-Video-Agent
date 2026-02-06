import asyncio
import aiohttp
import os
from dotenv import load_dotenv

import random 
async def download_image(session, prompt, i,seed):
    api_key = os.getenv("POLLINATIONS_API_KEY")

    # 1. Add &seed={seed} to your URL parameters
    clean_prompt = prompt.replace(" ", "%20")
    url = (
        f"https://gen.pollinations.ai/image/{clean_prompt}?"
        f"width=1080&height=1920&model=flux&seed={seed}&nologo=true"
    )
    headers = {"Authorization": f"Bearer {api_key}"}
    async with session.get(url, headers=headers) as resp:
        if resp.status == 200:
            content = await resp.read()
            os.makedirs("project_output/frames", exist_ok=True)
            with open(f"project_output/frames/frame_{i}.jpg", "wb") as f:
                f.write(content)
            print(f"✅ Image {i} Success!")
            return True
            
    print(f"❌ Image {i} Failed: {resp.status}")
    return False

async def generate_all_images(prompts, topic):
    async with aiohttp.ClientSession() as session:
        # 1. Create a "Global Context" to glue the images together
        # This tells the AI the overall theme so the style doesn't jump around
        global_context = f"A consistent cinematic story about {topic}, high quality, 8k, professional lighting. "
        
        # 2. Use a single seed for the whole video to keep the AI's 'mood' the same
        session_seed = random.randint(1, 99999)
        
        tasks = []
        for i, p in enumerate(prompts):
            # 3. Combine Global Context + Current Frame Prompt
            # This ensures the AI knows it's part of the same series
            chained_prompt = f"{global_context} Frame {i+1}: {p}"
            
            # We use the same seed for all images to maximize visual consistency
            task = download_image(session, chained_prompt, i, session_seed)
            tasks.append(task)
        
        print(f"🚀 Generating {len(prompts)} related images for: {topic}...")
        await asyncio.gather(*tasks)

