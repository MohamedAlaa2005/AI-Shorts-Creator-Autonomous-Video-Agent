# Compile the graph
import asyncio
from graph.builder import workflow
app = workflow.compile()
async def run():
    inputs = {"topic": "day in life of rice man", "retry_count": 0}
    # You MUST loop through the stream to see progress!
    async for output in app.astream(inputs):
        print(f"--- Finished Node: {list(output.keys())[0]} ---")
        # Optional: Print the actual state change
        # print(output) 

if __name__ == "__main__":
    asyncio.run(run())