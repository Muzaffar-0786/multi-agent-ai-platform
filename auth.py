from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from passlib.context import CryptContext

from sqlalchemy.orm import Session

from database import get_db

from config import settings

from models import User


# ==========================================================
# Password Configuration
# ==========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# ==========================================================
# JWT Configuration
# ==========================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)


# ==========================================================
# Password Functions
# ==========================================================

def hash_password(
    password: str,
) -> str:
    """
    Convert plain password into hash.
    """

    return pwd_context.hash(
        password
    )


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify user password.
    """

    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# ==========================================================
# JWT Token Creation
# ==========================================================

def create_access_token(
    user_id: int,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create JWT access token.
    """

    if expires_delta is None:

        expires_delta = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )


    expire = datetime.utcnow() + expires_delta


    payload = {
        "user_id": user_id,
        "exp": expire,
    }


    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


    return token
# ==========================================================
# JWT Decode
# ==========================================================

def decode_access_token(
    token: str,
) -> Optional[int]:
    """
    Decode JWT token and return user id.
    """

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[
                settings.ALGORITHM
            ],
        )

        user_id = payload.get(
            "user_id"
        )

        if user_id is None:
            return None

        return int(user_id)


    except JWTError:

        return None



# ==========================================================
# Get Current User
# ==========================================================

def get_current_user(
    token: str = Depends(
        oauth2_scheme
    ),
    db: Session = Depends(
        get_db
    ),
) -> User:
    """
    Validate token and return user.
    """

    user_id = decode_access_token(
        token
    )


    if user_id is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )


    user = db.query(
        User
    ).filter(
        User.id == user_id
    ).first()


    if user is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )


    if not user.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user.",
        )


    return user
