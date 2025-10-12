from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
from jwt import PyJWTError, encode as jwt_encode 
from .config import settings 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    ## Verifica senha corresponde --> hash
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    ## Retorna hash --> texto
    return pwd_context.hash(password)

# Token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=1)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt_encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt