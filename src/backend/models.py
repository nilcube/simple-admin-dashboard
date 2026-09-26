from pydantic import BaseModel, Field
from dataclasses import dataclass




class UserCredential(BaseModel):
    user: str = Field(min_length=1)
    password: str = Field(min_length=6)



class User(BaseModel):
    id: int | None = None
    user: str = Field(min_length=1)
    password: str = Field(min_length=6)
    is_admin: bool = False


@dataclass(frozen=True)
class Token:
    expired: bool
    token: str
    user_id: int
