import os
import traceback
from openai import OpenAI

# ==========================
# Configuration
# ==========================

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "OPENROUTER_API_KEY environment variable is not set."
    )

MODEL = "openai/gpt-oss-120b:free"

SYSTEM_PROMPT = """
You are A.R.G.U.S, an advanced AI assistant.

Rules:
- Be helpful.
- Be accurate.
- Be concise.
- If you don't know something, admit it.
- Do not make up facts.
"""

# ==========================
# OpenRouter Client
# ==========================

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)


# ==========================
# Chat Function
# ==========================

def chat_with_argus(user_message: str, history: list = None) -> str:
    """
    Sends a message to OpenRouter and returns the AI response.

    Args:
        user_message: Latest user message.
        history: Previous messages in OpenAI format.

    Returns:
        Assistant reply.
    """

    if history is None:
        history = []

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(history)

    messages.append({
        "role": "user",
        "content": user_message
    })

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            extra_body={
                "reasoning": {
                    "enabled": True
                }
            }
        )

        reply = response.choices[0].message.content

        if not reply:
            return "I couldn't generate a response."

        return reply

    except Exception:
        traceback.print_exc()
        return "Sorry, I encountered an error while generating a response."