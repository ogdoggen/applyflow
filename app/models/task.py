from typing import Optional
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey

from app.db.base import Base

class PreparationTaskModel(Base):
    __tablename__ = "preparation_tasks"
    id : Mapped[int] = mapped_column(primary_key=True)
    vacancy_id : Mapped[int] = mapped_column(ForeignKey("vacancies.id", ondelete = "CASCADE"), nullable=False)
    title : Mapped[str] = mapped_column(String(100), nullable=False)
    notes : Mapped[str | None] = mapped_column(Text, nullable=True)
    is_done : Mapped[bool] = mapped_column(default=False, nullable=False)
    due_date : Mapped[date] = mapped_column(nullable=False)

    vacancy : Mapped["VacancyModel"] = relationship(back_populates="tasks")