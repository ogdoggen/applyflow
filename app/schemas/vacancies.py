from enum import Enum
from pydantic import BaseModel, Field, HttpUrl

class VacancyStatus (str, Enum):
    saved = "saved"
    applied = "applied"
    test = "test"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"


class VacancyCreate (BaseModel):
    company : str = Field(min_length = 1, max_length = 100)
    title : str = Field(min_length = 1, max_length = 150)
    url : HttpUrl
    status : VacancyStatus = VacancyStatus.saved
    description : str = None

class VacancyRead (VacancyCreate):
    id : int


