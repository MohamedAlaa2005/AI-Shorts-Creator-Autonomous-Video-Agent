# 🎬 AI Shorts Creator: Autonomous Video Agent

An intelligent agentic system built with **LangGraph** and **Gemini 2.5 Flash** that researches trending topics, writes viral scripts, generates consistent AI imagery, and automatically uploads the result to YouTube.

## 🚀 Features

* **Autonomous Research:** Uses Tavily Search to find the 5 most shocking facts about any topic.
* **Viral Scriptwriting:** A "Writer" node converts facts into high-retention 60-second scripts.
* **Critic Loop:** A "Critic" node reviews the script and forces a rewrite if the hook isn't "viral" enough.
* **Consistent Visuals:** Generates images via Pollinations (Flux model) using **Prompt Chaining** and **Seed Locking** for visual continuity.
* **Automated SEO:** Uses LLM Structured Output to generate catchy titles and trending hashtags.
* **Auto-Upload:** Seamless integration with YouTube Data API v3.

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone https://github.com/MohamedAlaa2005/AI-Shorts-Creator-Autonomous-Video-Agent.git
cd shorts-gen-agent

```


2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Set up Environment Variables:**
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_key
POLLINATIONS_API_KEY=your_key

```


4. **YouTube API Credentials:**
* Place your `client_secrets.json` from Google Cloud Console in the project root.



## 🧠 The Agent Workflow

The system uses a **StateGraph** to manage the video production pipeline:

1. **Researcher:** Searches for facts and tech trends.
2. **Planner:** Organizes the facts into a logical flow.
3. **Writer:** Generates the narration and 5 cinematic image prompts.
4. **Critic:** Grades the script (PASS/FAIL). If FAIL, it loops back to the Writer with feedback.
5. **Media Engine:** Downloads images in parallel and assembles the video.
6. **Uploader:** Generates SEO metadata and pushes to YouTube.

## 📂 Project Structure

```text

├── .env                    # API Keys (Gemini, Tavily, Pollinations)
├── .gitignore              # Ignores .env, __pycache__, and secrets
├── client_secrets.json     # YouTube OAuth Credentials (keep secure!)
├── requirements.txt        # Project dependencies
├── main.py                 # Entry point: Runs the LangGraph app
│
├── agents/                 # The "Brains" (LLM Logic)
│   ├── researcher.py       # Finds trends and facts
│   ├── planner.py          # Structures the video flow
│   ├── writer.py           # Generates scripts and image prompts
│   ├── critic.py           # Reviews and provides feedback (The Loop)
│   ├── uploader_node.py    # Generates titles/tags and triggers upload
│   └── __init__.py
│
├── graph/                  # The "Nervous System" (Orchestration)
│   ├── state.py            # Defines VideoState TypedDict
│   ├── builder.py          # Compiles nodes and conditional edges
│   └── __init__.py
│
├── tools/                  # The "Hands" (External Actions)
│   ├── search_tool.py      # Tavily API wrapper
│   ├── image_gen.py        # Async Pollinations/Flux engine
│   ├── voice_gen.py        # TTS/Audio generation
│   ├── assembler.py        # MoviePy/FFmpeg video stitching
│   ├── youtube_uploader.py # Google API upload logic
│   └── __init__.py
│
└── project_output/         # (Generated) Temporary storage
    ├── frames/             # frame_0.jpg, frame_1.jpg, etc.
    ├── audio/              # Generated narration files
    └── final_video.mp4     # The finished product

```

---

**Would you like me to add a "Troubleshooting" section to this README to help with common API errors?**
