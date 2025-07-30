from utilities.models import ChatMessage as _ChatMessage
def markNewMessage(historySoFar: list[_ChatMessage], role: str, message: str) \
    -> list[_ChatMessage]:

    formattedMessage: _ChatMessage = _ChatMessage(role=role, content=message)
    historySoFar.append(formattedMessage)
    updatedHistory: list[_ChatMessage] = historySoFar

    return updatedHistory

# Create a log in chat history that user uploaded files and what files were saved
def markFileUpload(historySoFar: list[_ChatMessage], d: dict[str, dict[str, str | bool]], \
    role: str = "user") -> list[_ChatMessage]:

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

    formattedMessage: _ChatMessage = _ChatMessage(role=role, content=output)
    historySoFar.append(formattedMessage)
    updatedHistory: list[_ChatMessage] = historySoFar

    return updatedHistory

# Turn chat history list of messages into a formatted string log for LLM reference
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

# user_input = f"*User used \"start\" command*\n \
# *Server sent to you the notebook \"{filesList[currentNotebook]}\"*\n \
# *\"{filesList[currentNotebook]}\" text content:*\n \
# {parser.getCellContent(txt_path=os.path.join("app", "temp", f"{filesList[currentNotebook][:-6]}.txt"))}"
def markContentSending(filesList, currentNotebook) -> str:
    import utilities.parser as parser
    import os

    user_input = ""
    user_action = "*User used \"start\" command*\n"
    server_action = f"*Server sent to you the notebook \"{filesList[currentNotebook]}\"*\n"
    cell_content = parser.getCellContent(txt_path=os.path.join("app", "temp", f"{filesList[currentNotebook][:-6]}.txt"))

    user_input = \
        user_action + \
        server_action + \
        "Notebook\'s cell content + text outputs: \n" + \
        cell_content

    return user_input

def reductPreviousNotebookContent(history: str, filesList, currentNotebook) -> str:
    previousNotebookContent = markContentSending(filesList, currentNotebook)
    shortened_entry = f"*You and User analyzed the notebook \"{filesList[currentNotebook]}\"*\n"
    history = history.replace(previousNotebookContent, shortened_entry)

    return history