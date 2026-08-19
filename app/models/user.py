from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey

from app.db.base import Base

class UserModel(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)
    email : Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    password_hash : Mapped[str] = mapped_column(nullable=False)

    vacancies : Mapped["VacancyModel"] = relationship(back_populates="owner")