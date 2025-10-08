from fastapi import FastAPI, Response
from database import engine 

#Criar tabelas no banco de dados
# Base.metadata.create_all(bind=engine) # descomentar next

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

#Rota de teste para a conexão com o banco de dados
@app.get("/db-test")
def test_db_connection():
    try:
        #Tenta estabelecer uma conexão
        connection = engine.connect()
        connection.close()
        return {"status": "success", "message": "Conexão com o banco de dados estabelecida com sucesso"} 
    except Exception as e:
        return Response(content=f"Falha na conexão com o banco: {e}", status_code=500)