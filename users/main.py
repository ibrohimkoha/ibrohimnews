from fastapi import APIRouter, Depends, HTTPException, status

from users.schemas import UsersResponseSchema, UserCreateSchema, UserLoginSchema

from sqlalchemy.orm  import Session

from users.utils import authenticate_user, create_access_token

from general import get_session

from datetime import datetime, timedelta

from users.models import UsersTable

import os

router = APIRouter(prefix='/users', tags=['users'])

from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from sqlalchemy.exc import IntegrityError

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 0    ))

from users.descriptions import create_user_description

from users.dependencies.JWT.handlers import JWTHandler

from posts.schemas import UserSchema

from users.dependencies.users.user import UserHandling

@router.post("/create-user", description=create_user_description)
async def create_user(data: UserCreateSchema,session: Session = Depends(get_session) ):
    try:
        user = UsersTable(username=data.username,first_name=data.first_name,last_name=data.last_name, email=data.email, role="user", password=bcrypt_context.hash(data.password), date_joined=data.date_joined)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"user exist or bad request")

@router.post('/token/')
async def signin_by_access_token(data: UserLoginSchema,session:Session = Depends(get_session)):
    user = authenticate_user(session, data.username, data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    token = JWTHandler.create_token(self=JWTHandler,username=user.username, user_id=user.id)
    return {
        'access_token': token,
        'token_type': 'Bearer'
    }

@router.post('/user-role-change')
async def change_role(code: str,
user: UserSchema = Depends(UserHandling().user),
session: Session = Depends(get_session)):
    if code != "a29oYToxMzFyNjNzaDI0bw==":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Code xato")
    db_user = session.query(UsersTable).filter(UsersTable.id == user.id).first()
    db_user.role = "employee"
    session.commit()
    return HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="Role o'zgardi")