from pydantic import BaseModel
from typing import Optional


class UsersInCreate(BaseModel):
    username: str
    nama: str
    nomor_telpon : str
    password: str

class UsersInUpdate(BaseModel):
    nama: Optional[str]
    nomor_telpon : Optional[str]

class ValidateRekening(BaseModel):
    nomor_rekening: Optional[str]

class UsersInLogIn(BaseModel):
    username: str
    password: str