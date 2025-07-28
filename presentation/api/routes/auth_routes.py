from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from application.use_cases.auth_use_cases import AuthUseCases, LoginRequest, LoginResponse
from infrastructure.database import get_db
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.security.bcrypt_hasher import BcryptHasher

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/login", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token
    """
    # Create use case
    repository = UserRepository(db)
    hasher = BcryptHasher()
    use_cases = AuthUseCases(repository, hasher)
    
    # Process login request
    request = LoginRequest(
        email=form_data.username,  # OAuth2 uses username field for email
        password=form_data.password
    )
    
    response = use_cases.login(request)
    if not response:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return response