from pydantic import BaseModel
from typing import Optional, List
class NewsPostCreateSchema(BaseModel):
    title: str 
    description: str
    category_id: int 

class NewsPostResponseSchema(BaseModel):
    id: int 

    title: str

class UserSchema(BaseModel):
    id: int
    username: str
    role: str


class CategoryResponseSchema(BaseModel):
    id: int 
    name: str
    newsposts: list[Optional[NewsPostResponseSchema]]

class ImageSchema(BaseModel):
    image: str


class NewsPostResponseSchemain(BaseModel):
    id: int 
    title: str
    category_id: int
    description: str
    images: list[ImageSchema]


class CommentCreateSchema(BaseModel):
    comment: str