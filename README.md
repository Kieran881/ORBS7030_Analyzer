# Bytewise - Jupyter Notebook Grading Assistant

**MVP Status: READY FOR PRODUCTION**

A comprehensive web application designed for Hong Kong Baptist University's ORBS7030: Business Statistics with Python course. Enables instructors to upload student Jupyter notebooks and receive AI-powered analysis and grading suggestions.

Youtube Demo -->: *https://youtu.be/wmKsvV70buE*

## Project Overview

Bytewise is a full-stack academic grading assistant that processes student Jupyter notebook submissions and provides intelligent analysis. The system handles secure file uploads, parses notebook content into LLM-friendly formats, and maintains contextual conversations for detailed grading discussions and even compraring student submissions with each other.

**Academic Context**: Built specifically for HKBU Mathematics Department's Business Statistics course, focusing on statistical inference methods and Python programming analysis. System prompt specifically was tailored for the course description and types of assignments.

## Core Features

### File Management
- **Multi-file drag-and-drop upload** with real-time validation
- **Comprehensive security**: Path traversal protection, 24MB size limits, format validation
- **Duplicate detection and removal** with automatic cleanup
- **Support for multiple notebook formats**: Handles both the standard .ipynb from Jupyter Lab and .ipynb from VS Code
- **Notebook parsing**: Unpacks Jupyter Notebook into ASCII text content and image charts, formats and packs them for sending to LLM

### AI-Powered Grading Assistant
- **Persistent conversation memory** throughout grading sessions (however if page was refreshed, chatbot clears all memories - messages and uploaded files)
- **Context-aware responses** using complete chat history
- **Professional conversation interface** with user/assistant message distinction

## File Tree

```
Bytewise/
├── app/
│   ├── backend/                    # FastAPI Server
│   │   ├── main.py                # API endpoints & logic
│   │   └── utilities/
│   │       ├── models.py          # Pydantic models & system prompt
│   │       ├── GPT_responder.py   # OpenRouter AI integration
│   │       ├── parser.py          # Notebook parsing 
│   │       ├── chat_history.py    # Conversation history management
│   │       └── cleaner.py         
│   ├── frontend/                  # Client Interface
│   │   ├── index.html            
│   │   └── static/
│   │       ├── script.js         
│   │       └── style.css         
│   ├── uploaded/                 # Student notebook storage
│   └── temp/                     # Processing workspace
├── lib/                          
├── bin/                          
└── README.md                     # Documentation
```

---

## API Reference

| Method | Endpoint | Purpose | Status |
|--------|----------|---------|--------|
| `GET` | `/` | Serve main application interface | Ready |
| `POST` | `/chatbot-answer` | Send message to AI assistant | Ready |
| `POST` | `/files-upload` | Upload student notebook files | Ready |
| `POST` | `/analyze` | Start notebook analysis workflow | Ready |
| `POST` | `/clear-chat-history` | Reset conversation memory | Ready |

## MVP Implementation Status

### Fully Implemented and Tested ✔️

*This application represents a complete, deployable solution for academic notebook grading with AI assistance. All core functionality has been implemented and testeds.*