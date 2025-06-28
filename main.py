import os
import chainlit as cl
from dotenv import load_dotenv
from openai import AsyncOpenAI

# 1. Load API Key from .env
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

if not gemini_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env")

# 2. Initialize Gemini client (OpenAI-compatible)
client = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 3. Chainlit bot starts
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="👋 Mera Chatbot.").send()

# 4. Handle user message
@cl.on_message
async def on_message(message: cl.Message):
    try:
        response = await client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[{"role": "user", "content": message.content}]
        )
        content = response.choices[0].message.content or ""
        await cl.Message(content=content).send()
    except Exception as e:
        await cl.Message(content=f"❌ Error: {str(e)}").send()
