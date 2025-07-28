from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import jwt
from pydantic import BaseModel

from domain.entities.user import UserRole


class JWTConfig:
    SECRET_KEY = "uamitos-ca-secure-jwt-key-2023"  # In production, this should be an environment variable
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8  # 8 hours


class TokenData(BaseModel):
    uuid: str
    email: str
    role: str
    exp: datetime


class JWTManager:
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token with the provided data
        
        :param data: Data to encode in the token
        :param expires_delta: Optional expiration time delta
        :return: JWT token as string
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=JWTConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWTConfig.SECRET_KEY, algorithm=JWTConfig.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def decode_token(token: str) -> Optional[TokenData]:
        """
        Decode a JWT token and return the token data
        
        :param token: JWT token string
        :return: TokenData or None if invalid
        """
        try:
            payload = jwt.decode(token, JWTConfig.SECRET_KEY, algorithms=[JWTConfig.ALGORITHM])
            token_data = TokenData(
                uuid=payload.get("uuid"),
                email=payload.get("email"),
                role=payload.get("role"),
                exp=datetime.fromtimestamp(payload.get("exp"))
            )
            return token_data
        except jwt.PyJWTError:
            return None
    
    @staticmethod
    def is_token_valid(token: str) -> bool:
        """
        Check if a token is valid
        
        :param token: JWT token string
        :return: True if valid, False otherwise
        """
        return JWTManager.decode_token(token) is not None
    
    @staticmethod
    def create_user_token(uuid: str, email: str, role: UserRole) -> str:
        """
        Create a token for a user
        
        :param uuid: User UUID
        :param email: User email
        :param role: User role
        :return: JWT token string
        """
        data = {
            "uuid": str(uuid),
            "email": email,
            "role": role.value
        }
        return JWTManager.create_access_token(data)