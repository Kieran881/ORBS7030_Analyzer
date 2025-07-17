# Bytewise (Jupyter Notebook Analysis Module)

A web application for uploading and analyzing Jupyter notebook files using AI. Users can upload `.ipynb` files and interact with an AI assistant about their notebook content.

## Project Overview

Bytewise is a full-stack application that processes Jupyter notebook files and provides an AI chat interface. The system handles file uploads, parses notebook content, and maintains conversation context for analysis discussions. See app/backend/models.py for system and developer prompts.

## Features

### File Upload & Processing
- Multi-file upload with drag-and-drop interface
- File validation (format, size, security checks)
- Duplicate detection and prevention
- Security measures: path traversal protection, 24MB file size limit

### AI Chat Interface
- Persistent conversation memory during session
- Context-aware responses using chat history
- Real-time messaging interface
- Chat history management (clear/refresh functionality)

### Notebook Processing
User uploads a batch of `.ipynb` files. The system:
1. **Validates and stores** files in the `/uploaded` directory
2. **Parses notebook content** for structuring in more LLM-friendly format
3. **Extracts components**: markdown cells, code cells, outputs, and metadata
4. **Processes outputs**: text results (one .txt file) and PNG chart images (multiple .png images)
5. **Archives processed content** as ZIP files for sending to LLM

The parser handles both standard Jupyter JSON format and VS Code XML-based notebook format. No matter what software student used to create his Notebook, parser will work.

## 📂 Project Structure

```
Bytewise/
├── app/
│   ├── backend/
│   │   ├── main.py                 # FastAPI server & API endpoints
│   │   ├── utilities/
│   │   │   ├── models.py          # Pydantic data models and system prompt
│   │   │   ├── GPT_responder.py   # AI integration module
│   │   │   ├── mark_file_upload.py # File upload marking (for chat history)
│   │   │   ├── packager.py        # Notebook packaging utilities
│   │   │   └── parser_pro.py      # Advanced notebook parsing
│   │   └── temp/                  # Temporary notebook content processing
│   ├── frontend/
│   │   ├── index.html             # Main application interface
│   │   └── static/
│   │       ├── script.js          # Frontend JavaScript logic
│   │       └── style.css          # Custom styling
│   └── uploaded/                  # User-uploaded notebook storage
├── lib/                           # Python virtual environment
├── bin/                           # Virtual environment binaries
└── README.md                      # This file
```

## 📋 API Documentation

### **Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serve main application interface |
| `POST` | `/chatbot-answer` | Send message to AI assistant |
| `POST` | `/files-upload` | Upload Jupyter notebook files |
| `POST` | `/clear-chat-history` | Clear conversation memory |

## Current Status

### Working Features
- File upload pipeline with validation and security measures
- AI chat interface with persistent conversation memory
- Notebook parsing
- Web interface
- Conversation with AI
- File archiving and packaging utilities
<br><br> --> Note: Although chatting with AI and file processing & storing works, the functionality to send those parsed Notebook to LLM is not yet implemented.

### In Development
- **LLM file content integration** - Sending processed notebook content to AI for analysis
- **Export functionality** - Download processed content and analysis results
