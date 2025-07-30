# Create a log in chat history that user uploaded files and what files were saved
def markFileUpload(d: dict[str, dict[str, str | bool]]):
    filenames = []
    for (key, item) in d.items():
        if item['Saved'] == True:
            filenames.append(key)

    output = "*User uploaded files: "
    for i in range(0, len(filenames)):
        if i == 0:
            output += filenames[i]
        elif i == len(filenames) -1:
            output += ", " + filenames[i] + "*"
        else:
            output += ", " + filenames[i]

    return output

# Turn chat history list of messages into a formatted string log for LLM reference
from utilities.models import ChatMessage as _ChatMessage
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