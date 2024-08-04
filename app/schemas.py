from datetime import datetime
from pydantic import BaseModel,EmailStr
from pydantic.types import conint
class PostBase(BaseModel):
    title:str
    content:str
    published:bool

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    email:EmailStr
    created_at:datetime
    class Config:
        from_attributes=True

        
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner:UserOut
    class Config:
        from_attributes=True

class PostOut(BaseModel):
    Post:Post
    votes:int
    class Config:
        from_attributes=True   

class User(BaseModel):
    email:EmailStr
    password:str



class Token(BaseModel):
    access_token:str
    token_type:str

class TokenOut(BaseModel):
    id:str

class Vote(BaseModel):
    post_id:int
    dir: conint(le=1) # type: ignore
