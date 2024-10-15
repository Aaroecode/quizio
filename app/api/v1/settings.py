from fastapi import APIRouter, Depends, HTTPException
from db.postgres import PostgresDB
from services.settings_service import SettingsService
from models.settings_models import UpdatePreferencesSchema, ChangePasswordSchema, VerifyIdentitySchema

router = APIRouter()

db = PostgresDB("postgresql://admin:admin@localhost:5432/quizo")
settingsService = SettingsService(db)


@router.put("/user/preferences", response_model=dict)
async def update_preferences(user_id: int, preferences: UpdatePreferencesSchema):
    try:
        updated_preferences = await settingsService.update_preferences(user_id, preferences)
        return {"status": "success", "data": updated_preferences}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/user/change-password", response_model=dict)
async def change_password(user_id: int, data: ChangePasswordSchema):
    try:
        result = await settingsService.change_password(user_id, data)
        return {"status": "success", "message": result["message"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/user/verify-identity", response_model=dict)
async def verify_identity(user_id: int, data: VerifyIdentitySchema):
    try:
        verification_result = await settingsService.verify_identity(user_id, data)
        return {"status": "success", "data": verification_result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))