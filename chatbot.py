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
- If you don't know something, say so.
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
# Streaming Chat Function
# ==========================

def stream_chat_with_argus(user_message: str, history: list = None):
    """
    Streams the AI response token-by-token.
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

    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    try:

        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True,
            extra_body={
                "reasoning": {
                    "enabled": True
                }
            }
        )

        for chunk in stream:

            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta

            if delta is None:
                continue

            content = getattr(delta, "content", None)

            if content:
                yield content

    except Exception:

        traceback.print_exc()

        yield "Sorry, I encountered an error while generating a response."