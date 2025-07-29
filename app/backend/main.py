import os
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from utilities import models, mark_file_upload, GPT_responder, parser

# Main FastAPI application
app = FastAPI()

# Mount the static files directory to our host (localhost)
app.mount("/static", StaticFiles(directory="app/frontend/static", html=True), name="static")

# Store chat history for LLM reference (LLM-memory)
chatHistory: list[models.ChatMessage] = []
filesList: list[str] = []
filesUploaded = False

# Serve initial starting page
@app.get("/")
async def serve_index():
    global chatHistory
    chatHistory.clear()
    return FileResponse(os.path.join("app", "frontend", "index.html"))

# Clear chat history, LLM's memory
@app.post("/clear-chat-history")
async def clear_chat_history():
    global chatHistory
    chatHistory.clear()  # or chatHistory = []
    return {"status": "success", "message": "Chat history cleared"}

# Send API request to a LLM and update the chat history
@app.post("/chatbot-answer")
async def chatbot_answer(message: models.ChatMessage):
    chatHistory.append(message)
    chatHistory_as_a_string = GPT_responder.formatChatHistory(chatHistory[0:-1])  # Exclude the last message for context

    # chatbot_response = await GPT_responder.get_response(
    #     human_input="Previous messages: \n" + \
    #         chatHistory_as_a_string + \
    #         "Current message: \n" + message.content
    # )
    chatbot_response = "Sample response based on the chat history and current message."

    response_message = models.ChatMessage(role="bot", content=chatbot_response)
    chatHistory.append(response_message)
    chatHistory_as_a_string = GPT_responder.formatChatHistory(chatHistory)

    print(chatHistory_as_a_string)

    return response_message

# File upload API endpoint
# Implemented robust error and edge cases handling
# Valid file(-s) is/are saved in the app/uploaded directory 
# File uploading is also included in the chat history
@app.post("/files-upload")
async def process_files(files: list[UploadFile]):    
    total_response: dict[str, dict[str, str | bool]] = {}
    
    # Ensure upload directory exists
    upload_dir = os.path.join("app", "uploaded") 
    os.makedirs(upload_dir, exist_ok=True)

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

    chatHistory.append(models.ChatMessage(role="user", content=mark_file_upload.markFileUpload(d=total_response)))
    chatHistory_as_a_string = GPT_responder.formatChatHistory(chatHistory)

    print(chatHistory_as_a_string)

    parser.processNotebooks()

    global filesUploaded
    filesUploaded = True
    return total_response

# API endpoint to enter file analysis cycle
@app.post("/start-analysis")
def start_analysis():
    # If user tries to use /start command before any files have been uploaded
    response_message: models.ChatMessage
    if filesUploaded == False:
        response_message = models.ChatMessage(
            role="bot", content="No Jupyter Notebooks found. Make sure to send them first!")
        return response_message
    
    # Include list of notebook files to the history for LLM reference
    files_list: str = "Received Jupyter Notebooks:\n"
    global filesList
    import os

    for file in os.listdir(os.path.join("app", "uploaded")):
        if file != ".gitkeep" and file != ".DS_Store":
            file = file.replace(".txt", ".ipynb") # For display - to not confuse user
            filesList.append(file)
            files_list = files_list + file + '\n' 
    
    
    chatHistory.append(models.ChatMessage(role="user", content="/start"))
    chatHistory.append(models.ChatMessage(role="bot", content="Starting analysis of the first notebook"))

    chatHistory_as_a_string = GPT_responder.formatChatHistory(chatHistory)  
    chatHistory_as_a_string = files_list + chatHistory_as_a_string 

    print(chatHistory_as_a_string)

    response_message = models.ChatMessage(
        role="bot", content="Starting analysis of the first notebook")
    return response_message
    # TODO: Actually implement automatic sending the first notebook's content along with /start message