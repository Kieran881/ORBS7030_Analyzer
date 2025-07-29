from utilities.models import ChatMessage as _ChatMessage
from utilities.models import systemPrompt, developerPrompt

async def get_response(human_input: str) -> str:
    from openai import OpenAI
    import os

    try:
        OPEROUTER_API_KEY = os.environ.get("OPENROUTER_KEY")
    except:
        return "Sorry. Something went wrong with getting response from LLM (API key required)"

    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPEROUTER_API_KEY,
        )
        # For dev purposes override the uni prompts
        systemPrompt = "Output text in markdown format"
        developerPrompt = "Be yourself"
        completion = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
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
        )
        LLM_outputDICT: dict = completion.to_dict()
        LLM_output: str = LLM_outputDICT['choices'][0]['message']['content']

        return LLM_output
    except:
        return "Something went wrong with the request to the LLM. Please try again later."

def formatChatHistory(chat_history: list[_ChatMessage]) -> str:
    formatted_history = "Chat history: \n"
    for message in chat_history:
        if message.role == "user":
            formatted_history += f"User: {message.content}\n"
        elif message.role == "bot":
            formatted_history += f"Bot: {message.content}\n"
        else:
            formatted_history += "\n"
    return formatted_history