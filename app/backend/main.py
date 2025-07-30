import os
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from utilities import models, chat_history, GPT_responder, parser, cleaner

# Main FastAPI application
app = FastAPI()

# Mount the static files directory to our host (localhost)
app.mount("/static", StaticFiles(directory="app/frontend/static", html=True), name="static")

# Store chat history for LLM reference (LLM-memory)
chatHistory: list[models.ChatMessage] = []
# Store the list of files user uploaded
filesList: list[str] = []
# To keep track of what notebook is analyzed now
currentNotebook: int = 0
# To determine if user uploaded files or not
filesUploaded = False

# Serve initial starting page
@app.get("/")
async def serve_index():
    global chatHistory
    chatHistory.clear()
    cleaner.clean(os.path.join("app", "temp"))  # Clean temp folder
    cleaner.clean(os.path.join("app", "uploaded")) # Clean uploaded folder
    return FileResponse(os.path.join("app", "frontend", "index.html"))

# Clear chat history, LLM's memory
# TODO: Modify to also clean up all the files from server memory
@app.post("/clear-chat-history")
async def clear_chat_history():
    global chatHistory
    chatHistory.clear()  # or chatHistory = []
    return {"status": "success", "message": "Chat history cleared"}

# Send API request to a LLM and update the chat history
@app.post("/chatbot-answer")
async def chatbot_answer(message: models.ChatMessage):
    global chatHistory

    chatHistory = chat_history.markNewMessage(chatHistory, message.role, message.content)
    chatHistory_as_a_string = chat_history.formatChatHistory(chatHistory[0:-1])  # Exclude the last message for context

    chatbot_response = await GPT_responder.get_response(
        human_input="Previous messages by you and user (chat context): \n" + \
            chatHistory_as_a_string + \
            "Current message sent by user: \n" + message.content
    )
    print("Previous messages by you and user (chat context): \n" + \
            chatHistory_as_a_string + \
            "Current message sent by user: \n" + message.content)
    # chatbot_response = "Sample response based on the chat history and current message."

    response_message = models.ChatMessage(role="bot", content=chatbot_response)
    chatHistory = chat_history.markNewMessage(chatHistory, "bot", chatbot_response)
    chatHistory_as_a_string = chat_history.formatChatHistory(chatHistory)

    return response_message

# File upload API endpoint
# Implemented robust error and edge cases handling
# Valid file(-s) is/are saved in the app/uploaded directory 
# File uploading is also included in the chat history
@app.post("/files-upload")
async def process_files(files: list[UploadFile]):    
    total_response: dict[str, dict[str, str | bool]] = {}
    global chatHistory
    
    # Ensure upload directory exists
    upload_dir = os.path.join("app", "uploaded") 
    os.makedirs(upload_dir, exist_ok=True)

    cleaner.clean(os.path.join("app", "temp"))  # Clean temp folder
    cleaner.clean(os.path.join("app", "uploaded")) # Clean uploaded folder

    for file in files:
        # Check if file exists and has a filename
        if not file or not file.filename:
            total_response["Unknown"] = {"Saved": False, "Context": "No file provided"}
            continue

        file_name = file.filename.strip()
        
        # Validate filename 
        if not file_name or file_name.lower() == 'none':
            total_response["Invalid"] = {"Saved": False, "Context": "Invalid filename"}
            continue

        # Check file extension
        if not file_name.lower().endswith(".ipynb"):
            total_response[file_name] = {"Saved": False, "Context": "Not a valid Jupyter Notebook file (.ipynb required)"}
            continue
        
        # Sanitize filename to prevent path traversal
        safe_filename = os.path.basename(file_name)
        if safe_filename != file_name:
            total_response[file_name] = {"Saved": False, "Context": "Invalid filename, contains path separators"}
            continue
        
        file_path = os.path.join(upload_dir, safe_filename)
        
        # Try to save the file
        try:
            content = await file.read()
            
            # Basic validation - check if file is not empty
            if len(content) == 0:
                total_response[file_name] = {"Saved": False, "Context": "File is empty"}
                continue
            
            # Check file size (limit to 24MB)
            if len(content) > 24 * 1024 * 1024:  # 24MB 
                total_response[file_name] = {"Saved": False, "Context": "File too large (max 10MB)"}
                continue
            
            with open(file_path, "wb") as f:
                f.write(content)
                
            total_response[file_name] = {"Saved": True, "Context": f"Saved to {safe_filename}"}
            
        except PermissionError:
            total_response[file_name] = {"Saved": False, "Context": "Permission denied - cannot save file"}
        except OSError as e:
            total_response[file_name] = {"Saved": False, "Context": f"File system error: {str(e)}"}
        except Exception as e:
            total_response[file_name] = {"Saved": False, "Context": f"Unexpected error: {str(e)}"}

    chatHistory = chat_history.markFileUpload(chatHistory, total_response)

    # Removes any duplicates, just a safety check
    # if user accidentally uploadede the same notebook twices
    # On my OS this is done automatically, not so sure about other platforms
    parser.removeDuplicates() 

    global filesUploaded
    filesUploaded = True
    return total_response

# API endpoint to enter file analysis cycle
@app.post("/start-analysis")
async def start_analysis():
    global filesList
    global currentNotebook
    global chatHistory

    # If user tries to use /start command before any files have been uploaded
    response_message: models.ChatMessage
    if filesUploaded == False:
        response_message = models.ChatMessage(
            role="bot", content="No Jupyter Notebooks found. Make sure to send them first!")
        chatHistory = chat_history.markNewMessage(chatHistory, "user", "*/start*")
        chatHistory = chat_history.markNewMessage(chatHistory, "bot", response_message.content)
        return response_message
    
    # Include list of notebook files to the history for LLM reference
    files_list: str = "Received Jupyter Notebooks:\n"
    for file in os.listdir(os.path.join("app", "uploaded")):
        if file != ".gitkeep" and file != ".DS_Store":
            filesList.append(file)
            files_list = files_list + file + '\n' 

    if currentNotebook >= len(filesList):
        response_message = models.ChatMessage(
            role="bot", content="No more Notebooks left to analyze. If you have more, please upload them"
        )
        chatHistory = chat_history.markNewMessage(chatHistory, "user", "*/start*")
        chatHistory = chat_history.markNewMessage(chatHistory, "bot", response_message.content)
        return response_message
    
    chatbot_response = await GPT_responder.get_analysis(filesList[currentNotebook])

    # I have a good fucking idea
    # What if I will make not one ugly user_input where I try to combine all stuff
    # like context of user&server actions for LLM, chat history, and notebook content
    # Instead, I propose creating a function that will connect all the things automatically
    # Plus, that way it will be much more clearer to implement notebook forgetting 
    # We will have chat history as usual, 
    # then notebook content (very long) with analysises (also very long),
    # And continued chat with another content + analysises
    # I propose that by outsourcing marking content + analysis by function,
    # We can reduce the length of history we are sending to LLM considerably
    # When user submits /next then we will simply replace 
    # content + analysis of the previous notebook by some context (*You and user analyzed notebook 69.ipynb*)
    # And the cycle continues on
    user_input = chat_history.markContentSending(filesList, currentNotebook)

    chatHistory = chat_history.markNewMessage(chatHistory, "user", user_input)
    chatHistory = chat_history.markNewMessage(chatHistory, "bot", chatbot_response)

    response_message = models.ChatMessage(
        role="bot", content=chatbot_response)
    
    currentNotebook += 1

    return response_message