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
    status,
    UploadFile,
    HTTPException,
    Body,
    Query,
    Path,
    Form,
    Header,
    Cookie,
    File,
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

class LoginOut(BaseModel):
    username: str = Field(
        ...,
        max_length=20,
        example="juanito2022",
    )
    message: str = Field(default="Login Successful")
app:FastAPI = FastAPI()
#Metodos
@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["Home"],
    summary="Home 🏠"
    )

def home() -> Dict:
    """
    Home

    This is the main page of the app

    Parameters:
    - None

    Returns:
    - A dictionary containing the following keys: "Hello" and the following values: "World".

    """
    return {"Hello": "world"}
# Request and response body
@app.post(
    path="/person/new",
    response_model = PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="Create a new person  in the app 💻"
    )
def create_person(person: Person = Body(...)):
    """
    Create Person

    This path operation creates a new Person in the app and saves the information in Database.

    Parameters:
    - Request Body parameter:
        - **person: Person** -> A person model with name,last name, age,email,favourite color, hair color and marital status.

    Returns a person model with name,last name, age,email,favourite color, hair color and marital status.
    """
    return person
# Validations of Query parameters
@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary="Shows the name and age of the person"
    )
def show_person(
    name: str = Query(
        min_length=1,
        max_length=50,
        title= "Person Name",
        description= "This is the name of the person",
        example="Erick",
    ),
    age: int = Query(
        title= "Person Age",
        description= "This is the age of the person ",
        example=25,
    )
):
    """
    Show Person

    This path operation shows a Person in the app and saves the information in Database.

    Parameters:
    - **name: Optional[str]**
    - **age: int**

    Returns:
    - A dictionary containing the following keys: "name" and the following values: "age".

    """
    return {name : age}
#Validations: path parameters

persons = [1,2,3,4,5,6]

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary="Validate if a person ID exists in the database"
    )
def person_id(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person Id",
        description= "This is the id of the person, must be greater than zero.",
        example=1
    )
):
    """
    Person ID

    This path operation validates the ID of a person.

    Parameters:
    - **person_id: int**

    Returns:
    - If person_id is not valid raise an  404 error and shows a message indicating that the person not exist.
    - A dictionary containing the following keys: "person_id" and the following values: "Exist!!".

    """
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person does not exist!!!"
        )
    return {person_id: "Exist!!"}
# Validations: Body parameters (Request body)
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary= "Add location and update the person"
    )
def update_person(
    person_id: int = Path(
        ...,
        title="Person Id",
        description= "This is the id of the person, must be greater than zero.",
        gt=0,
        example=1,
    ),
    person: Person = Body(...),
    location:Location = Body(...),

):
    """
    Update person

    This path operation updates the person(if have a valid ID), adding itself location information.

    Parameters:
    - **person_id: int**
    - **person: Person**
    - **location: Location**

    Returns:
    - A person model updated with location.

    """
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person does not exist!!!"
        )
    results = person.dict()
    results.update(location.dict())
    return results
@app.post(
    path='/login',
    #response_model=LoginOut
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary="Login Path"
)
def login(
    username:str = Form(...),
    password:str = Form(...)
):
    """
    Login

    This path operation send the username and password from a form  to the server .

    Parameters:
    - **username:str**
    - **password:str**

    Returns:
    - A dictionary containing the following keys: "username" and the following values: "message".

    """
    return LoginOut(username=username)
# Cookie y Header
@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK,
    tags=["Contact"],
    summary= "Contact data"
)
def contact(
    name:str = Form(
        ...,
        max_length=20,
        min_length=1,
    ),
    last_name:str = Form(
        ...,
        max_length=20,
        min_length=1,
    ),
    email:EmailStr = Form(...),
    message:str = Form(
        ...,
        min_length=20,
        ),
    user_agent:Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None),
):
    """
    Contact

    This path operation send the contact information from a form  to the server.

    Parameters:
    - **name:str**
    - **last_name:str**
    - **email:EmailStr**
    - **message:str**
    - **user_agent:Optional[str]**
    - **ads:Optional[str]**

    Returns:
    - the user agent

    """
    return user_agent
# Files
@app.post(
    path = '/post-image',
    tags=["Upload Files"],
    summary="Upload Image Files"
    )
def post_image(
    image:UploadFile = File(...)
):
    """
    PostImage

    This path operation send a image to the server .

    Parameters:
    - **image: UploadFile**

    Returns:
    - A complete information about the uploaded image like filename, content_type and size(kb).

    """
    return {
        "Filename": image.filename,
        "Content-Type": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024,ndigits=2)
    }
