from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from . import models, schemas, crud, auth
from .database import engine, get_db

#Criar tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Endpoint para criar um novo usuário
@app.post("/users/", response_model=schemas.User)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verifica se o email já está em uso
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered / Email já cadastrado")
    
    # se não, cria o usuário
    return crud.create_user(db=db, user=user)

# Endpoint Login
@app.post("/token", response_model=schemas.Token)
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

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

#Rota de teste para a conexão com o banco de dados
"""@app.get("/db-test")
def test_db_connection():
    try:
        #Tenta estabelecer uma conexão
        connection = engine.connect()
        connection.close()
        return {"status": "success", "message": "Conexão com o banco de dados estabelecida com sucesso"} 
    except Exception as e:
        return Response(content=f"Falha na conexão com o banco: {e}", status_code=500)"""