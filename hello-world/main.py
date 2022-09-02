#Python
from typing import Dict,Optional
#pydantic
from pydantic import BaseModel
#FastAPI
from fastapi import FastAPI,Body,Query,Path
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
# Validations of Query parameters
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title= "Person Name",
        description= "This is the name of the person, its between 1 and 50 characters"
    ),
    age: str = Query(
        ...,
        title= "Person Age",
        description= "This is the age of the person, its REQUIRED"
    )
):
    return {name: age}
#Validations: path parameters
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person Id",
        description= "This is the id of the person, must be greater than zero.",
    )
):
    return {person_id: "Exist!!"}

