from pydantic import BaseModel
from typing import Optional


class CreateUser(BaseModel):
    name: str
    email: str
    password: str
    gender: str
    termsAccepted: bool

class Login(BaseModel):
    email: str
    password: str

class Logout(BaseModel):
    email: str

class ForgotPassword(BaseModel):
    email: str

class ResetPassword(BaseModel):
    email: str
    newPassword: str

