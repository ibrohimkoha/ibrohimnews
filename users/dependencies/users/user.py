from users.models import UsersTable
from fastapi import Depends, HTTPException
from users.dependencies.JWT.bearer import JWTBearer
from users.dependencies.JWT.handlers import JWTHandler
from sqlalchemy.orm import Session
from general import get_session
from jose.exceptions import JWTError
from starlette import status


class UserHandling:
    def __init__(self) -> None:
        pass

    async def user(self, token: str = Depends(JWTBearer()), session: Session = Depends(get_session)):
        try:
            payload = JWTHandler().decode_jwt(token)
            user = session.query(UsersTable).filter(UsersTable.id == payload.get("id")).first()
            return user
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    

    async def employee(self, token: str = Depends(JWTBearer()), session: Session = Depends(get_session)):
        user = await self.user(token=token, session=session)
        if user.role != "employee":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                "message": "Not permitted !"
            })
        return user
    
    async def project_manager(self, token: str = Depends(JWTBearer()), session: Session = Depends(get_session)):
        user = await self.user(token=token, session=session)
        if user.role != "pm":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                "message": "Not permitted !"
            })
        return user


user_handler = UserHandling()