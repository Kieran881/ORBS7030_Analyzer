from utilities.models import ChatMessage as _ChatMessage
from utilities.models import systemPrompt, developerPrompt


# Get LLM response
async def get_response(human_input: str) -> str:
    import requests
    import json
    import os

    OPEROUTER_API_KEY = os.environ.get("OPENROUTER_KEY")
    try: 
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPEROUTER_API_KEY}",
                "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
                "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
            },
            data=json.dumps({
                "model": "openai/gpt-4.1", # Optional
                "messages": [
                    {
                        "role": "system",
                        "content": systemPrompt
                    },
                    {
                        "role": "developer",
                        "content": developerPrompt
                    },
                    {
                        "role": "user",
                        "content": human_input
                    }
                ]
            })
        )
    except:
        return "Something went wrong with the request to the LLM. Please try again later."

    print(response.json())
    try:
        return response.json()['choices'][0]['message']['content']
    except:
        return "Something went wrong with the request to the LLM. Please try again later."

def formatChatHistory(chat_history: list[_ChatMessage]) -> str:
    formatted_history = ""
    for message in chat_history:
        if message.role == "user":
            formatted_history += f"User: {message.content}\n"
        elif message.role == "bot":
            formatted_history += f"Bot: {message.content}\n"
        else:
            formatted_history += "\n"
    return formatted_history