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
    status,
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
class PersonBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Erick",
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Escobar",
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=23,
    )
    email: EmailStr = Field(
        ...,
        title="Email",
        description=" This the Email of the person",
        example="user@example.com",
    )
    favourite_color: Optional[Color] = Field(default=None,example="Red")
    hair_color: Optional[HairColor] = Field(default = None)
    is_married: Optional[bool] = Field(default = None)

    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Erick",
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Escobar",
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=23,
    )
    email: EmailStr = Field(
        ...,
        title="Email",
        description=" This the Email of the person",
        example="user@example.com",
    )
    favourite_color: Optional[Color] = Field(default=None,example="Red")
    hair_color: Optional[HairColor] = Field(default = None)
    is_married: Optional[bool] = Field(default = None)

class Person(PersonBase):
    password: str = Field(
        ...,
        min_length = 8,
        max_length = 64,
        example="password",
        )
class PersonOut(PersonBase):
    pass
app:FastAPI = FastAPI()
#Metodos
@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    )

def home() -> Dict:
    return {"Hello": "world"}
# Request and response body
@app.post(
    path="/person/new",
    response_model = PersonOut,
    status_code=status.HTTP_201_CREATED,
    )
def create_person(person: Person = Body(...)):
    return person
# Validations of Query parameters
@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    )
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title= "Person Name",
        description= "This is the name of the person",
        example="Erick",
    ),
    age: str = Query(
        ...,
        title= "Person Age",
        description= "This is the age of the person",
        example=25,
    )
):
    return {name : age}
#Validations: path parameters
@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK)
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person Id",
        description= "This is the id of the person, must be greater than zero.",
        example=123,
    )
):
    return {person_id: "Exist!!"}
# Validations: Body parameters (Request body)
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_201_CREATED,
    )
def update_person(
    person_id: int = Path(
        ...,
        title="Person Id",
        description= "This is the id of the person, must be greater than zero.",
        gt=0,
        example=123,
    ),
    person: Person = Body(...),
    location:Location = Body(...),

):
    results = person.dict()
    results.update(location.dict())
    return results
