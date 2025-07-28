from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from domain.entities.user import UserRole
from infrastructure.database import get_db
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.security.jwt_manager import JWTManager, TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user_token(token: str = Depends(oauth2_scheme)) -> TokenData:
    """
    Validate token and return token data
    
    :param token: JWT token
    :return: TokenData object
    :raises HTTPException: If token is invalid
    """
    token_data = JWTManager.decode_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data


async def get_current_user(
    token_data: TokenData = Depends(get_current_user_token),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user
    
    :param token_data: Decoded token data
    :param db: Database session
    :return: User object
    :raises HTTPException: If user not found
    """
    user_repository = UserRepository(db)
    user = user_repository.get_by_uuid(token_data.uuid)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    
    return user


# Role-based access control dependencies
def get_admin_user(user = Depends(get_current_user)):
    """Dependency for admin-only routes"""
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return user


def get_teacher_user(user = Depends(get_current_user)):
    """Dependency for teacher-only routes"""
    if user.role != UserRole.TEACHER and user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return user


def get_student_user(user = Depends(get_current_user)):
    """Dependency for student-only routes"""
    if user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return user