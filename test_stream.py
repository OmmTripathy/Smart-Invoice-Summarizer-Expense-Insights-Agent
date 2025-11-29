from openai import OpenAI
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()

client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Explain AI in simple words."}
    ],
    stream=True,
)

print("AI Streaming Output:\n")
for chunk in stream:
    if chunk.choices and chunk.choices[0].delta:
        text = chunk.choices[0].delta.content
        if text:
            print(text, end="", flush=True)

print("\n\n--- Stream End ---")
