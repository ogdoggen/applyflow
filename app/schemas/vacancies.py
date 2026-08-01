from enum import Enum
from pydantic import BaseModel, Field, HttpUrl, ConfigDict

class VacancyStatus (str, Enum):
    saved = "saved"
    applied = "applied"
    test = "test"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"


class Vacancy(BaseModel):
    company : str = Field(min_length = 1, max_length = 100)
    title : str = Field(min_length = 1, max_length = 150)
    url : HttpUrl
    status : VacancyStatus = VacancyStatus.saved
    description : str | None = None


class VacancyCreate (Vacancy):
    pass


class VacancyUpdate (BaseModel):
    company : str | None = Field(default=None, min_length=1, max_length= 100)
    title: str | None = Field(default=None, min_length=1, max_length=150)
    url : HttpUrl | None = None
    status : VacancyStatus | None = None
    description : str | None = None


class VacancyRead (BaseModel):
    id:int
    company: str
    title: str
    url: HttpUrl
    status: VacancyStatus
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)





