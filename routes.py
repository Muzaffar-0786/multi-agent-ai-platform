from __future__ import annotations

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from database import get_db

from models import User

from schemas import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
    ConversationCreate,
    ConversationResponse,
    ChatRequest,
    ChatResponse,
)

from services import (
    user_service,
    conversation_service,
    chat_service,
)

from auth import (
    verify_password,
    create_access_token,
    get_current_user,
)



# ==========================================================
# Router Setup
# ==========================================================

router = APIRouter(
    prefix="/api",
    tags=["AI Platform"],
)



# ==========================================================
# Authentication Routes
# ==========================================================

@router.post(
    "/auth/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    data: UserCreate,
    db: Session = Depends(get_db),
):

    existing_user = (
        user_service.get_user_by_email(
            db,
            data.email,
        )
    )


    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered.",
        )


    return (
        user_service.create_user(
            db,
            data,
        )
    )



@router.post(
    "/auth/login",
    response_model=TokenResponse,
)
def login_user(
    data: UserLogin,
    db: Session = Depends(get_db),
):

    user = (
        user_service.get_user_by_email(
            db,
            data.email,
        )
    )


    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials.",
        )


    if not verify_password(
        data.password,
        user.hashed_password,
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials.",
        )


    token = create_access_token(
        user.id
    )


    return {
        "access_token": token,
        "token_type": "bearer",
    }
# ==========================================================
# Conversation Routes
# ==========================================================

@router.post(
    "/conversations",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_conversation(
    data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return (
        conversation_service.create_conversation(
            db=db,
            user_id=current_user.id,
            data=data,
        )
    )



# ==========================================================
# Chat Routes
# ==========================================================

@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat_with_ai(
    data: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    result = (
        chat_service.execute_chat(
            db=db,
            conversation_id=data.conversation_id,
            prompt=data.prompt,
        )
    )


    return ChatResponse(
        conversation_id=(
            result["conversation_id"]
        ),
        user_message=data.prompt,
        final_response=(
            result["final_response"]
        ),
    )



# ==========================================================
# Health Route
# ==========================================================

@router.get(
    "/health",
)
def health_check():

    return {
        "status": "running",
        "service": "Multi-Agent AI Platform",
    }
