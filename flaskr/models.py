
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Date
import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(200))
    dob: Mapped[datetime.date] = mapped_column(Date)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    
    def __repr__(self) -> str:
        return f"<User username={self.username!r}>"