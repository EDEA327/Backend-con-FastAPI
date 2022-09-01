# Dependencias del proyecto
from fastapi import FastAPI
from typing import Dict
# Instanciando la clase FastAPI
app:FastAPI = FastAPI()

@app.get("/")
def home() -> Dict:
    return {"Hello": "world"}