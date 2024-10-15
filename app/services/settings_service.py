from fastapi import HTTPException, status
from app.db.postgres import PostgresDB
from passlib.context import CryptContext
from app.models.settings_models import UpdatePreferencesSchema, ChangePasswordSchema, VerifyIdentitySchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SettingsService:
    def __init__(self, db: PostgresDB):
        self.db = db

    async def update_preferences(self, user_id: int, preferences: UpdatePreferencesSchema):
      
        user = await self.db.fetch("SELECT * FROM users WHERE id = $1", user_id)
        if not user:
            raise ValueError("User not found")
        await self.db.execute(
            """
            UPDATE users SET notifications_enabled = $1, privacy_settings = $2 WHERE id = $3
            """,
            preferences.notifications_enabled,
            preferences.privacy_settings,
            user_id
        )
        return {
            "user_id": user_id,
            "notifications_enabled": preferences.notifications_enabled,
            "privacy_settings": preferences.privacy_settings
        }

    async def change_password(self, user_id: int, data: ChangePasswordSchema):
        
        user = await self.db.fetch("SELECT * FROM users WHERE id = $1", user_id)
        if not user:
            raise ValueError("User not found")
        if not pwd_context.verify(data.current_password, user["password"]):
            raise ValueError("Current password is incorrect")
        new_password_hashed = pwd_context.hash(data.new_password)
        await self.db.execute(
            "UPDATE users SET password = $1 WHERE id = $2",
            new_password_hashed, user_id
        )
        return {"message": "Password changed successfully"}

    async def verify_identity(self, user_id: int, data: VerifyIdentitySchema):
      
        user = await self.db.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
        if not user:
            raise ValueError("User not found")
        await self.db.execute(
            """
            UPDATE users SET id_type = $1, id_document = $2 WHERE id = $3
            """,
            data.id_type,
            data.id_document,
            user_id
        )
        return {
            "user_id": user_id,
            "id_type": data.id_type,
            "id_document": data.id_document
        }
