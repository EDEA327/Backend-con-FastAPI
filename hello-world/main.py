#Python
from typing import (
    Dict,
    Optional,
)
from enum import Enum
#pydantic
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
)
from pydantic.color import Color
#FastAPI
from fastapi import (
    FastAPI,
    Body,
    Query,
    Path,
)
# Models
class HairColor(str,Enum):
    white = "White"
    black = "Black"
    blonde = "Blonde"
    gray = "Gray"
    red = "Red"
class Location(BaseModel):
    city:str = Field(
        ...,
        min_length=1,
        max_length=100,
        title="City",
        description=" This the City where person lives",
        )
    state:str = Field(
        ...,
        min_length=1,
        max_length=100,
        title="State",
        description=" This the State where person lives",
        )
    country:str = Field(
        ...,
        min_length=1,
        max_length=100,
        title="Country",
        description=" This the Country where person lives",
        )
    class Config:
        schema_extra={
            "example": {
                "city": " My City",
                "state": "My State",
                "country": "My Country",
        }
        }
class Person(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        le=115
    )
    email: EmailStr = Field(
        ...,
        title="Email",
        description=" This the Email of the person",
    )
    favourite_color: Color = Field(default=None)
    hair_color: Optional[HairColor] = Field(default = None)
    is_married: Optional[bool] = Field(default = None)
    class Config:
        schema_extra = {
            "example":{
                "name": "Erick",
                "last_name": "Escobar",
                "age": 23,
                "email": "e@e.e",
                "favourite_color": "orange",
                "hair_color":"Black",
                "is_married": False,
            }
        }
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
# Validations: Body parameters (Request body)
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person Id",
        description= "This is the id of the person, must be greater than zero.",
        gt=0
    ),
    person: Person = Body(...),
    location:Location = Body(...)

):
    results = person.dict()
    results.update(location.dict())
    return results
