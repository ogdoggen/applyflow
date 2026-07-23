from datetime import date
from pydantic import BaseModel


class PreparationTaskCreate(BaseModel):

    title : str
    notes : str | None = None
    due_date : date

class PreparationTaskRead(BaseModel):

    id : int
    vacancy_id : int
    title : str
    notes : str | None = None
    is_done : bool
    due_date : date

class PreparationTaskUpdate(BaseModel):

    title : str | None = None
    notes : str | None = None
    is_done : bool | None = None
    due_date : date | None = None