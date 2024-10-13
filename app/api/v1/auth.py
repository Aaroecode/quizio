from fastapi import APIRouter, Depends, HTTPException
from app.services.auth_service import AuthService
from app.models.auth_models import SignupUser, Login, ResetPassword, UserProfile
from app.db.postgres import PostgresDB

router = APIRouter()
db = PostgresDB("postgresql://admin:admin@localhost:5432/quizo")
auth_service = AuthService(db)

# Updated Sign Up API
@router.post("/api/auth/signup")
async def signup(user: SignupUser):
    print(user)
    print("*" * 40)
    try:
        return await auth_service.signup(user)
    except HTTPException as e:
        raise e

# Updated Login API
@router.post("/api/auth/login")
async def login(user: Login):
    return await auth_service.login(user.email, user.password)

# Updated Logout API
@router.post("/api/auth/logout")
async def logout():
    return await auth_service.logout()

# Updated Forgot Password API
@router.post("/api/auth/forgot-password")
async def forgot_password(email: str):
    return await auth_service.forgot_password(email)

# Updated Reset Password API
@router.post("/api/auth/reset-password")
async def reset_password(reset: ResetPassword):
    return await auth_service.reset_password(reset.email, reset.newPassword)

# Updated User Profile API
@router.get("/api/user/profile")
async def get_user_profile(email: str):
    return await auth_service.get_user_profile(email)

# Updated User Profile Update API
@router.put("/api/user/update")
async def update_user_profile(email: str, profile_data: UserProfile):
    return await auth_service.update_user_profile(email, profile_data)
