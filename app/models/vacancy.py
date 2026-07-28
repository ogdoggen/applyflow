from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text

from ..db.base import Base

class VacancyModel(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key = True)
    company: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="saved")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)