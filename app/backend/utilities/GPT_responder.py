# TODO: Create a proper system (developer) prompt, ask Dr Wu for examples to feed to LLM
# TODO: Implement token counting mechanism so that the model output
# won't get suddenly truncated (context window) - recommend user to clear chat history
# TODO: Format chat history the way OpenAI expects - multiple messages, 
# not just one big-ass message. Chat history as a list of dictionaries (messages),
# rather than just one dictionary with very long message content
# TODO: Implement the chat history compression where after we analyzed one notebook,
# its content and analysises will not be in full text but rather as just a few sentences,
# just enough to provide context for LLM on what happened before and nothing more
# 
# Some info about GPT4.1 for reference
# 1,047,576 tokens context window
# 32,768 tokens max output 

"""
Get response from LLM (OpenRouter API) based on user input.
User input is just a plain text, not analysis commands.
Output is the response from LLM, not analysis result.
Input: human_input (str) - user input text
Output: LLM response (str)
"""
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
async def get_response(human_input: list[ChatCompletionMessageParam]) -> str:
    from openai import OpenAI
    import os
    from utilities.models import LLM_MODEL, DEVELOPER_PROMPT

    try:
        OPEROUTER_API_KEY = os.environ.get("OPENROUTER_KEY")
    except:
        return "Sorry. Something went wrong with getting response from LLM (API key required)"

    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPEROUTER_API_KEY,
        )
        # For dev purposes override the uni prompt
        developerPrompt = "Output text in markdown format"
        completion = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "developer", "content": developerPrompt},
                *human_input 
            ]
        )
        LLM_outputDICT: dict = completion.to_dict()
        LLM_output: str = LLM_outputDICT['choices'][0]['message']['content']

        return LLM_output
    except:
        return "Something went wrong with the request to the LLM. Please try again later."

"""
Get analysis of a Jupyter Notebook file using LLM (OpenRouter API).
Input: notebook_name (str) - name of the Jupyter Notebook file
Output: LLM analysis result (str)
"""
async def get_analysis(notebook_name: str) -> str:
    from openai import OpenAI
    import os
    from utilities.models import LLM_MODEL, DEVELOPER_PROMPT

    message: list = []
    try:
        message = notebookToLLMRequest(notebook_name=notebook_name)
    except:
        return "Sorry. Something went wrong with formatting your notebook for LLM"

    try:
        OPENROUTER_API_KEY = os.environ.get("OPENROUTER_KEY")
    except:
        return "Sorry. Something went wrong with getting response from LLM (API key required)"

    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )
        # For dev purposes override the uni prompts
        systemPrompt = "Output text in markdown format"
        developerPrompt = "Be yourself"
        completion = client.chat.completions.create(
            model=LLM_MODEL,
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

"""
Convert a Jupyter Notebook file to a format suitable for LLM request.
Input: notebook_name (str) - name of the Jupyter Notebook file
Output: message (list) - formatted message (request) for LLM with all needed info
"""
def notebookToLLMRequest(notebook_name: str) -> list:
    # Will return list structure with embedded cell content 
    # and charts packed in one PDF file (base64 str) from one .ipynb notebook

    # .ipynb --> .txt + .pdf
    from os import path
    from utilities.parser import unpackNotebook as _unpackNotebook
    from utilities.parser import encodePDF as _encodePDF
    from utilities.parser import getCellContent as _getCellContent

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