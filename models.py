from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


def current_time():
    return datetime.now(timezone.utc)


class User(Base):
    """
    Application User Model
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=current_time,
        nullable=False
    )


    conversations: Mapped[list["Conversation"]] = relationship(
        "Conversation",
        back_populates="user",
        cascade="all, delete-orphan"
    )


    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"



class Conversation(Base):
    """
    User Chat Conversation Model
    """

    __tablename__ = "conversations"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    title: Mapped[str] = mapped_column(
        String(255),
        default="New Conversation",
        nullable=False
    )


    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=current_time,
        nullable=False
    )


    user: Mapped["User"] = relationship(
        "User",
        back_populates="conversations"
    )


    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )


    agent_logs: Mapped[list["AgentLog"]] = relationship(
        "AgentLog",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )


    def __repr__(self):
        return f"<Conversation id={self.id} title={self.title}>"



class Message(Base):
    """
    Individual Chat Messages
    """

    __tablename__ = "messages"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    conversation_id: Mapped[int] = mapped_column(
        ForeignKey(
            "conversations.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )


    sender: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )


    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=current_time,
        nullable=False
    )


    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="messages"
    )


    def __repr__(self):
        return f"<Message id={self.id} sender={self.sender}>"



class AgentLog(Base):
    """
    Multi-Agent Execution Logs
    """

    __tablename__ = "agent_logs"


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )


    conversation_id: Mapped[int] = mapped_column(
        ForeignKey(
            "conversations.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )


    agent_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )


    action_taken: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )


    log_output: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=current_time,
        nullable=False
    )


    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="agent_logs"
    )


    def __repr__(self):
        return f"<AgentLog id={self.id} agent={self.agent_name}>"
