#Python
from typing import Dict,Optional
#pydantic
from pydantic import BaseModel
#FastAPI
from fastapi import FastAPI,Body
# Models
class Person(BaseModel):
    name: str
    last_name: str
    age: int
    hair_color: Optional[str]
    is_married: Optional[bool]
app:FastAPI = FastAPI()
#Metodos
@app.get("/")
def home() -> Dict:
    return {"Hello": "world"}
# Request and response body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person
