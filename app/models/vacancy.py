from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey

from ..db.base import Base

class VacancyModel(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key = True)
    company: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="saved")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    tasks : Mapped[list["PreparationTaskModel"]] = relationship(back_populates="vacancy", passive_deletes=True)

    owner_id : Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner : Mapped["UserModel"] = relationship(back_populates="vacancies")