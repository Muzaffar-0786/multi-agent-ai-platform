from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# =====================================================
# User Schemas
# =====================================================

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime


# =====================================================
# JWT Schemas
# =====================================================

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None


# =====================================================
# Conversation Schemas
# =====================================================

class ConversationCreate(BaseModel):
    title: Optional[str] = "New Conversation"


class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    user_id: int
    created_at: datetime
  # =====================================================
# Message Schemas
# =====================================================

class MessageCreate(BaseModel):
    conversation_id: int
    content: str = Field(..., min_length=1)


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime


# =====================================================
# Chat Schemas
# =====================================================

class ChatRequest(BaseModel):
    conversation_id: int
    prompt: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    conversation_id: int
    user_message: str
    ai_response: str
    planner_output: str
    research_output: str
    coding_output: str
    reviewer_output: str


# =====================================================
# Agent Log Schemas
# =====================================================

class AgentLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    conversation_id: int
    agent_name: str
    status: str
    input_text: str
    output_text: str
    created_at: datetime


# =====================================================
# Common Response Schemas
# =====================================================

class SuccessResponse(BaseModel):
    success: bool = True
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
