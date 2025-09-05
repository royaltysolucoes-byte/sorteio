from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv() 

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
MONGO_DB = os.getenv("MONGO_DB")

username = quote_plus(MONGO_USER)
password = quote_plus(MONGO_PASS)

uri = f"mongodb+srv://{username}:{password}@{MONGO_CLUSTER}/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))
db = client[MONGO_DB]
collection = db["colaborador"]

app = FastAPI(title="API de Rifa")

class Usuario(BaseModel):
    nome: str
    cpf: str
    telefone: str
    numero: str


@app.post("/cadastrar")
def cadastrar(usuario: Usuario):
    if collection.find_one({"cpf": usuario.cpf}):
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    
    if collection.find_one({"numero": usuario.numero}):
        raise HTTPException(status_code=400, detail="Número já reservado")
    
    result = collection.insert_one(usuario.dict())
    return {"message": "Usuário cadastrado com sucesso!", "id": str(result.inserted_id)}

@app.get("/listar")
def listar():
    participantes = list(collection.find({}, {"_id": 0}))
    return participantes
