from pydantic import BaseModel, Field, ConfigDict, EmailStr

class UserCreate(BaseModel):
    email : EmailStr
    password : str = Field(min_length=6)

class UserRead(BaseModel):
    id : int
    email : EmailStr
    model_config = ConfigDict(from_attributes=True)