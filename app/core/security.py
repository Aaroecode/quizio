# utils/jwt_handler.py
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer
import jwt
from app.db.postgres import PostgresDB





SECRET_KEY = "Signature"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        raise HTTPException(status_code=403, detail="Token is invalid or expired")


def get_current_user(token: str = Security(security)):
    try:
        payload = verify_token(token.credentials)
        return payload
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))


class SecurityService:
    def __init__(self, db: PostgresDB):
        self.db = db

    async def authenticate_user(self, email: str, password: str):
        
        user = await self.db.fetch("SELECT * FROM users WHERE email = $1", email)
        if user and user["password"] == password:  # Simple password check (use hashed passwords in production)
            return user
        return None

    
    async def login_user(self, email: str, password: str):
        user = await self.authenticate_user(email, password)
        if not user:
            raise ValueError("Invalid credentials")
        
        access_token = create_access_token(
            data={"user_id": user["id"], "email": user["email"]},
            expires_delta=timedelta(minutes=30)
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Placeholder for DB pool
db = PostgresDB("postgresql://admin:admin@localhost:5432/quizo")
security_service = SecurityService(db)

class LoginRequest(BaseModel):
    email: str
    password: str

# Login API
@router.post("/login", response_model=dict)
async def login(data: LoginRequest):
    try:
        token = await security_service.login_user(data.email, data.password)
        return {"status": "success", "data": token}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))