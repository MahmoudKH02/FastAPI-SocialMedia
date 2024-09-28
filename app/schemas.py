from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional, Annotated, Tuple


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    published: bool = True


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    published: bool
    created_at: datetime
    owner: 'User'

    class Config:
        from_attributes = True


class PostVote(BaseModel):
    Post: Post
    votes: int


# Users
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int]


class VoteBase(BaseModel):
    post_id: int
    dir: Annotated[int, conint(ge=0, le=1)]


class VoteCreate(VoteBase):
    pass
