from fastapi import FastAPI, Response, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import engine, get_db

#Criar tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Endpoint para criar um novo usuário
@app.post("/users/", response_model=schemas.User)
def create_user_api(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verifica se o email já está em uso
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered / Email já cadastrado")
    
    #se não, cria o usuário
    return crud.create_user(db=db, user=user)

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