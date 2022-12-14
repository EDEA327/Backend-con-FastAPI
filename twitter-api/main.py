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
from fastapi import status,HTTPException
from fastapi import Body,Path,Form

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
    birth_date: Optional[date] = Field(default= None)

class UserRegister(User,UserLogin):
    pass

class Tweets(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length = 1,
        max_length = 256,
        example = "Este es un tweet"
        )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by:User = Field(...)

class LoginOut(BaseModel):
    email: EmailStr = Field(...)
    message: str = Field(default="Login Successfully!")

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
def login(email:EmailStr = Form(...), password:str = Form(...)):
    """
    Login

    This path operation login a Person in the app

    Parameters:
    - Request body parameters:
        - email: EmailStr
        - password: str

    Returns a LoginOut model with username and message
    """
    with open("user.json", "r+", encoding="utf-8") as f:
        data = json.loads(f.read())
        for user in data:
            if email == user['email'] and password == user['password']:
                return LoginOut(email=email)
            else:
                return LoginOut(email=email, message="Login Unsuccessfully!")
### Show all users
@app.get(
    path='/users',
    #response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users():
    """
    This path operation shows all users

    Parameters:
        -

    Returns a json list with all users in the app with the following attributes:

        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birth_date: date

    """
    with open("user.json","r",encoding="utf-8") as f:
        results = json.loads(f.read())
        return results
### Show a user
@app.get(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=["Users"]
)
def show_a_user(
    user_id: UUID = Path(
        ...,
        title = "User ID",
        description = "User ID",
        example = "3fa85f64-5717-4562-b3fc-2c963f66afa2",
        )
    ):
    """
    Show a User

    This path operation show if a person exist in the app

    Parameters:
        - user_id: UUID

    Returns a json with user data:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    with open("user.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        id = str(user_id)
    for data in results:
        if data["user_id"] == id:
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"??This user_id doesn't exist!"
        )
### Delete a user
@app.delete(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["Users"]
)
def delete_a_user(
    user_id: UUID = Path(
        ...,
        title="User ID",
        description="This is the user ID",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa1"
    )
    ):
    """
    Delete a User

    This path operation delete a user in the app

    Parameters:
        - user_id: UUID

    Returns a json with deleted user data:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    with open("user.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        id = str(user_id)
    for data in results:
        if data["user_id"] == id:
            results.remove(data)
            with open("user.json", "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(results))
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="??This user_id doesn't exist!"
        )

### Update a user
@app.put(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    tags=["Users"]
)
def update_a_user(
    user_id: UUID = Path(
            ...,
            title="User ID",
            description="This is the user ID",
            example="3fa85f64-5717-4562-b3fc-2c963f66afa3"
        ),
        user: UserRegister = Body(...)
    ):
    """
    Update User

    This path operation update a user information in the app and save in the database

    Parameters:
    - user_id: UUID
    - Request body parameter:
        - **user: User** -> A user model with user_id, email, first name, last name, birth date and password

    Returns a user model with user_id, email, first_name, last_name and birth_date
    """
    user_id = str(user_id)
    user_dict = user.dict()
    user_dict["user_id"] = str(user_dict["user_id"])
    user_dict["birth_date"] = str(user_dict["birth_date"])
    with open("user.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
    for user in results:
        if user["user_id"] == user_id:
            results[results.index(user)] = user_dict
            with open("user.json", "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(results))
            return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="??This user_id doesn't exist!"
        )

## Tweets

### Post a tweet
@app.post(
    path='/post',
    response_model=Tweets,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post(tweet: Tweets = Body(...)):
    """
    Post a Tweet
    This path operation post a tweet in the app
    Parameters:
        - Request body parameter
            - tweet: Tweets

    Returns a json with the basic tweet information:

        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])

        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet
### Show all Tweets
@app.get(
    path='/',
    response_model=List[Tweets],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
)
def home():
    """
    Post a Tweet
    This path operation shows all tweets in the app

    Parameters:
        -

    Returns a json with the basic tweet information:

        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    with open("tweets.json","r",encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Show a tweet
@app.get(
    path='/tweets/{tweet_id}',
    response_model=Tweets,
    status_code=status.HTTP_200_OK,
    summary="Shows a tweet",
    tags=["Tweets"]
)
def show_a_tweet(
    tweet_id: UUID = Path(
    ...,
    title="Tweet ID",
    description="This is the tweet ID",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )
):
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        id = str(tweet_id)
    for data in results:
        if data["tweet_id"] == id:
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"??This tweet_id doesn't exist!"
        )

### Delete a tweet
@app.delete(
    path='/tweets/{tweet_id}',
    response_model=Tweets,
    status_code=status.HTTP_200_OK,
    summary="Deletes a tweet",
    tags=["Tweets"]
)
def delete_a_tweet(
    tweet_id: UUID = Path(
        ...,
        title="Tweet ID",
        description="This is the tweet ID",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa2"
    )
):
    """
    Delete a Tweet

    This path operation delete a tweet in the app

    Parameters:
        - tweet_id: UUID

    Returns a json with deleted tweet data:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        id = str(tweet_id)
    for data in results:
        if data["tweet_id"] == id:
            results.remove(data)
            with open("tweets.json", "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(results))
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="??This tweet_id doesn't exist!"
        )

### Update a tweet
@app.put(
    path='/tweets/{tweet_id}',
    response_model=Tweets,
    status_code=status.HTTP_200_OK,
    summary="Updates a tweet",
    tags=["Tweets"]
)
def update_a_tweet(
    tweet_id: UUID = Path(
            ...,
            title="Tweet ID",
            description="This is the tweet ID",
            example="3fa85f64-5717-4562-b3fc-2c963f66afa8"
        ),
        content: str = Form(
        ...,
        min_length=1,
        max_length=256,
        title="Tweet content",
        description="This is the content of the tweet",
        )
):
    """
    Update Tweet

    This path operation update a tweet information in the app and save in the database

    Parameters:
    - tweet_id: UUID
    - content:str

    Returns a json with:

        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: datetime
        - by: User
    """
    tweet_id = str(tweet_id)
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
    for tweet in results:
        if tweet["tweet_id"] == tweet_id:
            tweet['content'] = content
            tweet['updated_at'] = str(datetime.now())
            print(tweet)
            with open("tweets.json", "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(results))
            return tweet
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="??This tweet_id doesn't exist!"
        )
