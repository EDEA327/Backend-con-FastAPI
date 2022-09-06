# Python
import json
from uuid import UUID
from datetime import date,datetime
from typing import Optional,List
# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body

app = FastAPI()

# Models

class UserBase(BaseModel):
    user_id:UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length = 8,
        example = "password"
        )

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50,
        example = "Erick"
        )
    last_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50,
        example = "Escobar"
        )
    birth_date: Optional[date] = Field(default=None)
class UserRegister(User,UserLogin):
    pass
class Tweets(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length = 1,
        max_length = 256,
        examples = "Este es un tweet"
        )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by:User = Field(...)

# Path Operations

## Users

### Register a user
@app.post(
    path='/signup',
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a user",
    tags=["Users"]
)
def signup(user:UserRegister = Body(...)):
    """
    Signup

    This path operation registers a user in the app

    Parameters:

        -Request body parameters
            -user: UserRegister

    Returns: A json with the basic user information:

        -user_id: UUID
        -email: EmailStr
        -first_name: str
        -birth_date: date
    """
    with open("user.json","r+",encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user



### Login a user
@app.post(
    path='/login',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    tags=["Users"]
)
def login():
    pass
### Show all users
@app.get(
    path='/users',
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users():
    pass
### Show al user
@app.get(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=["Users"]
)
def show_a_user():
    pass
### Delete a user
@app.delete(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["Users"]
)
def delete_a_user():
    pass
### Update a user
@app.put(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    tags=["Users"]
)
def update_a_user():
    pass


## Tweets

### Show all Tweets
@app.get(
    path='/',
    response_model=List[Tweets],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
)
def home():
    return {"Twitter-API": "Working"}
### Post a tweet
@app.post(
    path='/post',
    response_model=Tweets,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post():
    pass
### Show a tweet
@app.get(
    path='/tweets/{tweet_id}',
    response_model=Tweets,
    status_code=status.HTTP_200_OK,
    summary="Shows a tweet",
    tags=["Tweets"]
)
def show_a_tweet():
    pass
### Delete a tweet
@app.delete(
    path='/tweets/{tweet_id}',
    response_model=Tweets,
    status_code=status.HTTP_200_OK,
    summary="Deletes a tweet",
    tags=["Tweets"]
)
def delete_a_tweet():
    pass
### Update a tweet
@app.put(
    path='/tweets/{tweet_id}',
    response_model=Tweets,
    status_code=status.HTTP_200_OK,
    summary="Updates a tweet",
    tags=["Tweets"]
)
def update_a_tweet():
    pass