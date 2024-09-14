from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship

class UsersTable(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] 
    email: Mapped[str]
    role: Mapped[str]
    date_joined:Mapped[date]
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

