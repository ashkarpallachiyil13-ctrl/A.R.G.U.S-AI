import os
from openai import OpenAI

# Initialize OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = "openai/gpt-oss-120b:free"

SYSTEM_PROMPT = """
You are Argus, a helpful AI assistant.
Be accurate, friendly, and concise.
If you don't know something, say so instead of making it up.
"""


async def chat_with_argus(user_message: str, history: list):
    """
    Generates a response from Argus.

    Args:
        user_message (str): The user's latest message.
        history (list): Previous chat history in OpenAI format.

    Returns:
        str: Assistant response.
    """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # Add previous conversation
    messages.extend(history)

    # Add latest user message
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

        return response.choices[0].message.content

    except Exception as e:
        print(f"AI Error: {e}")
        return "Sorry, something went wrong while contacting the AI."