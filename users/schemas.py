from pydantic import BaseModel, EmailStr, Field
from datetime import date

class UsersResponseSchema(BaseModel):
    id: int
    username: str 
    email: EmailStr
    is_staff: bool


class UserCreateSchema(BaseModel):
    first_name:str
    last_name:str
    username: str 
    email: EmailStr
    password: str 
    date_joined: date



class UserLoginSchema(BaseModel):
    username: str
    password: str