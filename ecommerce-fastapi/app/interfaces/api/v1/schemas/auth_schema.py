from pydantic import BaseModel
from typing import List

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: int
    username: str
    roles: List[str]