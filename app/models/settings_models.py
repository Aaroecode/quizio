from pydantic import BaseModel

class UpdatePreferencesSchema(BaseModel):
    notifications_enabled: bool
    privacy_settings: str

class ChangePasswordSchema(BaseModel):
    current_password: str
    new_password: str

class VerifyIdentitySchema(BaseModel):
    id_type: str
    id_document: str
