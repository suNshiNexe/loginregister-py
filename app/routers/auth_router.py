from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta

from .. import models, schemas, crud, auth
from ..database import get_db
#
bearer_scheme = HTTPBearer()

def get_current_user(token: str = Depends(bearer_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials \n Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = auth.verify_token(token.credentials, credentials_exception)
    email: str = payload.get("sub")

    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    
    return user
# 

router = APIRouter()

# Endpoint para criar um novo usuário
@router.post("/users/", response_model=schemas.User)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verifica se o email já está em uso
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered / Email já cadastrado")
    
    return crud.create_user(db=db, user=user)

# Endpoint Login
@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.authenticate_user(
        db,
        email=form_data.username,
        password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password", 
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=auth.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return schemas.Token(
        access_token=access_token,
        token_type="bearer"
    )

# Endpoint para obter o usuário atual
@router.get(
        "/users/me", 
        response_model=schemas.User, 
        tags=["Users"],
        
)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user
