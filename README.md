# 🤖 Multi-Agent AI Platform (MVP)

A professional AI-powered Multi-Agent application built with **Python, FastAPI, Gemini AI, SQLAlchemy, JWT Authentication, and SQLite**.

This project demonstrates a structured AI workflow where multiple specialized AI agents collaborate to process user tasks and generate a final response.

The goal of this MVP is to build a clean, scalable backend architecture for an AI agent system.

---

# ✨ Features

## 🔐 User Authentication

- User Registration
- User Login
- Secure Password Hashing
- JWT Token Based Authentication
- Protected API Endpoints
- Active User Verification


---

# 🤖 Multi-Agent AI Workflow

The system uses multiple AI agents, where each agent has a specific responsibility.

## 🧠 Planner Agent

Responsibilities:

- Understand user requirements
- Break complex tasks into smaller steps
- Create a structured plan before execution


## 🔍 Research Agent

Responsibilities:

- Analyze the given task
- Provide supporting information
- Generate research-based insights


## 💻 Coding Agent

Responsibilities:

- Generate programming solutions
- Follow clean coding practices
- Provide technical implementation ideas


## ✅ Reviewer Agent

Responsibilities:

- Review generated output
- Identify possible improvements
- Provide quality feedback


---

# 🔄 Agent Execution Pipeline

The AI workflow follows this process:

```
User Input

     ↓

Planner Agent

     ↓

Research Agent

     ↓

Coding Agent

     ↓

Reviewer Agent

     ↓

Final AI Response
```

---

# 💬 Conversation System

The application supports AI conversations.

Features:

- Create conversations
- Store user messages
- Store AI responses
- Maintain conversation records
- Link conversations with users


---

# 📊 Agent Execution Logging

The system stores agent execution details.

Stored information:

- Agent name
- Execution step
- Agent status
- Input data
- Output data
- Execution time
- Creation timestamp


---

# 🗄️ Database System

Database technology:

- SQLite
- SQLAlchemy ORM


Database Models:

- User
- Conversation
- Message
- Agent Log


---

# 🧩 Backend Architecture

The project follows a layered backend structure:

```
User
 |
 |
FastAPI Routes
 |
 |
Services Layer
 |
 |
Agent Manager
 |
 |
AI Agents
 |
 |
Gemini AI
 |
 |
Database
```

---

# 🛠️ Technology Stack

## Backend

- Python
- FastAPI
- Uvicorn


## Database

- SQLite
- SQLAlchemy


## AI

- Google Gemini AI
- Multi-Agent Architecture


## Authentication

- JWT Authentication
- Passlib Password Hashing


## Data Validation

- Pydantic


---

# 📁 Project Structure

```
multi-agent-ai-platform/

│
├── main.py
├── config.py
├── database.py
├── models.py
├── schemas.py
├── gemini.py
├── agents.py
├── manager.py
├── auth.py
├── services.py
├── routes.py
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙️ Installation & Setup

## 1. Clone Repository

```bash
git clone <repository-url>

cd multi-agent-ai-platform
```


## 2. Create Virtual Environment

```bash
python -m venv venv
```


Activate Environment:

Windows:

```bash
venv\Scripts\activate
```


Linux / Mac:

```bash
source venv/bin/activate
```


---

# 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Configuration

Create a `.env` file:

```env
APP_NAME=Multi-Agent AI Platform

DATABASE_URL=sqlite:///multi_agent.db

SECRET_KEY=your_secret_key

GEMINI_API_KEY=your_gemini_api_key

GEMINI_MODEL=gemini-2.5-flash
```

---

# ▶️ Run Application

Start server:

```bash
uvicorn main:app --reload
```


Application URL:

```
http://127.0.0.1:8000
```


API Documentation:

```
http://127.0.0.1:8000/docs
```

---

# 📡 Available API Modules

## Authentication

```
POST /api/auth/register

POST /api/auth/login
```


## Conversation

```
POST /api/conversations
```


## AI Chat

```
POST /api/chat
```


## Health Check

```
GET /api/health
```

---

# 🎯 Current MVP Scope

This MVP currently provides:

✅ FastAPI Backend  
✅ Gemini AI Integration  
✅ Multi-Agent Workflow  
✅ JWT Authentication  
✅ Database Storage  
✅ Conversation Management  
✅ Agent Execution Logs  
✅ Clean Backend Architecture  


---

# 🚀 Future Improvements

Possible future upgrades:

- Frontend Application
- File Upload Support
- Advanced Memory System
- Vector Database Integration
- RAG Implementation
- Streaming AI Responses
- Cloud Deployment


---

# 📌 Project Status

Current Version:

```
MVP v1.0
```

The project is designed as a foundation for building a larger AI Agent platform.

---

# 📄 License

This project is created for educational purposes, portfolio demonstration, and AI application development.
