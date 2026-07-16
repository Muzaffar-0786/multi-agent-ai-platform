from __future__ import annotations

from typing import Dict, Any

from sqlalchemy.orm import Session

from models import (
    User,
    Conversation,
    Message,
    AgentLog,
)

from schemas import (
    UserCreate,
    ConversationCreate,
)

from auth import (
    hash_password,
)

from manager import (
    agent_manager,
)



# ==========================================================
# User Service
# ==========================================================

class UserService:
    """
    Handles user related operations.
    """


    @staticmethod
    def create_user(
        db: Session,
        user_data: UserCreate,
    ) -> User:
        """
        Create new user.
        """

        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hash_password(
                user_data.password
            ),
        )


        db.add(user)

        db.commit()

        db.refresh(user)

        return user



    @staticmethod
    def get_user_by_email(
        db: Session,
        email: str,
    ) -> User | None:
        """
        Find user by email.
        """

        return db.query(
            User
        ).filter(
            User.email == email
        ).first()



# ==========================================================
# Conversation Service
# ==========================================================

class ConversationService:
    """
    Handles conversation operations.
    """


    @staticmethod
    def create_conversation(
        db: Session,
        user_id: int,
        data: ConversationCreate,
    ) -> Conversation:
        """
        Create user conversation.
        """

        conversation = Conversation(
            title=data.title,
            user_id=user_id,
        )


        db.add(conversation)

        db.commit()

        db.refresh(conversation)

        return conversation
# ==========================================================
# Chat Service
# ==========================================================

class ChatService:
    """
    Handles AI conversation workflow.
    """


    @staticmethod
    def save_message(
        db: Session,
        conversation_id: int,
        role: str,
        content: str,
    ) -> Message:
        """
        Save chat message.
        """

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        db.add(message)

        db.commit()

        db.refresh(message)

        return message



    @staticmethod
    def save_agent_log(
        db: Session,
        conversation_id: int,
        agent_name: str,
        data: Dict[str, Any],
    ) -> AgentLog:
        """
        Save agent execution log.
        """

        log = AgentLog(
            conversation_id=conversation_id,
            agent_name=agent_name,
            step_number=data.get(
                "step",
                0,
            ),
            status="SUCCESS",
            input_text="",
            output_text=data.get(
                "output",
                "",
            ),
            execution_time=data.get(
                "execution_time",
                0.0,
            ),
        )


        db.add(log)

        db.commit()

        db.refresh(log)

        return log



    @staticmethod
    def execute_chat(
        db: Session,
        conversation_id: int,
        prompt: str,
    ) -> Dict[str, Any]:
        """
        Run complete AI agent pipeline.
        """


        ChatService.save_message(
            db=db,
            conversation_id=conversation_id,
            role="user",
            content=prompt,
        )


        results = agent_manager.execute(
            prompt
        )


        for agent_name, data in results.items():

            ChatService.save_agent_log(
                db=db,
                conversation_id=conversation_id,
                agent_name=agent_name,
                data=data,
            )


        final_response = (
            agent_manager.get_final_response(
                results
            )
        )


        ChatService.save_message(
            db=db,
            conversation_id=conversation_id,
            role="assistant",
            content=final_response,
        )


        return {
            "conversation_id": conversation_id,
            "final_response": final_response,
            "agents": results,
        }



# ==========================================================
# Service Instances
# ==========================================================

user_service = UserService()

conversation_service = ConversationService()

chat_service = ChatService()
