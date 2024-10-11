from fastapi import APIRouter
from app.services import auth_service
from app.models import auth_models

router = APIRouter()

@router.post("/signup")
async def signup(createUser: auth_models.CreateUser):
    auth_service.create_user()