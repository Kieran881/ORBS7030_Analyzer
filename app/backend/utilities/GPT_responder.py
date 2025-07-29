from utilities.models import ChatMessage as _ChatMessage
from utilities.models import systemPrompt, developerPrompt
from utilities.parser import unpackNotebook as _unpackNotebook
from utilities.parser import encodePDF as _encodePDF
from utilities.parser import getCellContent as _getCellContent

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
        # systemPrompt = "Output text in markdown format"
        # developerPrompt = "Be yourself"
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

async def get_analysis(notebook_name: str) -> str:
    from openai import OpenAI
    import os

    message: list = []
    try:
        message = notebookToLLMRequest(notebook_name=notebook_name)
    except:
        return "Sorry. Something went wrong with formatting your notebook for LLM"

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
        # systemPrompt = "Output text in markdown format"
        # developerPrompt = "Be yourself"
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
                message[0]
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

def notebookToLLMRequest(notebook_name: str) -> list:
    # Will return list structure with embedded cell content 
    # and charts packed in one PDF file (base64 str) from one .ipynb notebook

    # .ipynb --> .txt + .pdf
    from os import path
    _unpackNotebook(filepath=path.join("app", "uploaded", notebook_name))

    # .txt --> str
    cellContent: str = _getCellContent(
        txt_path=path.join("app", "temp", f"{notebook_name[:-6]}.txt"))
    chartsPDF_filename: str = notebook_name[:-6]
    # .pdf --> base64 str
    chartsPDF_base64: str = _encodePDF(
        pdf_path=path.join("app", "temp", f"{notebook_name[:-6]}.pdf"))
    message = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": cellContent
                },
                {
                    "type": "file",
                    "file": {
                        "filename": chartsPDF_filename,
                        "file_data": chartsPDF_base64
                    }
                }
            ]
        }
    ]

    return message