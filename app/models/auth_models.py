from pydantic import BaseModel
from typing import Optional



class SignupUser(BaseModel):
    id: Optional[int] 
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

class UserProfile(BaseModel):
    id: int
    name: str
    email: str
    gender: Optional[str] = None
    bio: Optional[str] = None