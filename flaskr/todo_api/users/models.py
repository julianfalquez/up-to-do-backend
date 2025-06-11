from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Date
from ...models import Base  # Make sure path is correct
from ...config import SessionLocal  # Instead of from ...db import SessionLocal
import datetime

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(200))
    dob: Mapped[datetime.date] = mapped_column(Date)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    profile_picture: Mapped[str] = mapped_column(String(255), nullable=True)
    
    def __repr__(self) -> str:
        return f"<User username={self.username!r}>"