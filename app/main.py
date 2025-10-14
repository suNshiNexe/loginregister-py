from fastapi import FastAPI
from .database import engine
from . import models
from .routers import auth_router

#Criar tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

# main
app = FastAPI()
# auth router
app.include_router(auth_router.router)

# /
@app.get("/")
def read_root():
    return {"status": "API is running! / A API está funcionando!"}
