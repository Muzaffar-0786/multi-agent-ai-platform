from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==========================================================
# User Schemas
# ==========================================================

class UserCreate(BaseModel):
    """
    User registration schema.
    """

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )


class UserLogin(BaseModel):
    """
    User login schema.
    """

    email: EmailStr

    password: str


class UserResponse(BaseModel):
    """
    Public user response.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime


# ==========================================================
# Authentication Schemas
# ==========================================================

class TokenResponse(BaseModel):
    """
    JWT token response.
    """

    access_token: str

    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    JWT decoded payload.
    """

    user_id: Optional[int] = None


# ==========================================================
# Conversation Schemas
# ==========================================================

class ConversationCreate(BaseModel):
    """
    Create new conversation.
    """

    title: str = Field(
        default="New Conversation",
        max_length=255,
    )


class ConversationResponse(BaseModel):
    """
    Conversation output.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    title: str
    user_id: int
    created_at: datetime
    # ==========================================================
# Message Schemas
# ==========================================================

class MessageCreate(BaseModel):
    """
    Create chat message.
    """

    conversation_id: int

    content: str = Field(
        ...,
        min_length=1,
    )


class MessageResponse(BaseModel):
    """
    Message output.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime


# ==========================================================
# Chat Schemas
# ==========================================================

class ChatRequest(BaseModel):
    """
    User AI request.
    """

    conversation_id: int

    prompt: str = Field(
        ...,
        min_length=1,
    )


class ChatResponse(BaseModel):
    """
    Complete AI pipeline response.
    """

    conversation_id: int

    user_message: str

    final_response: str

    planner_output: Optional[str] = None

    research_output: Optional[str] = None

    coding_output: Optional[str] = None

    reviewer_output: Optional[str] = None


# ==========================================================
# Agent Log Schemas
# ==========================================================

class AgentLogResponse(BaseModel):
    """
    Agent execution log output.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    conversation_id: int
    agent_name: str
    step_number: int
    status: str
    input_text: str
    output_text: str
    execution_time: float
    created_at: datetime


# ==========================================================
# Common Response Schemas
# ==========================================================

class SuccessResponse(BaseModel):
    """
    Common success response.
    """

    success: bool = True

    message: str


class ErrorResponse(BaseModel):
    """
    Common error response.
    """

    success: bool = False

    error: str
