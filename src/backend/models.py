from pydantic import BaseModel, Field




class UserCredential(BaseModel):
    user: str = Field(min_length=1)
    password: str = Field(min_length=6)



class User(BaseModel):
    _id: int | None = None
    user: str = Field(min_length=1)
    password: str = Field(min_length=6)
    is_admin: bool = False
