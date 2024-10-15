from fastapi import HTTPException, status
from passlib.context import CryptContext
from jose import jwt, JWTError
from pydantic import BaseModel
from app.db.postgres import PostgresDB
from app.models.auth_models import SignupUser  # Assuming you have a PostgresDB class in db/postgres.py

# Set up password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")
SECRET_KEY = "your_secret_key"  # Should be moved to environment variables for security

class AuthService:
    def __init__(self, db: PostgresDB):
        self.db = db

    async def signup(self, user: SignupUser):
        print("Starting signup process")
        hashed_password = pwd_context.hash(user.password)
        print(f"Password hashed: {hashed_password}")

        query = """
                INSERT INTO users ("name", "email", "password", "gender", "termsAccepted")
        VALUES ($1, $2, $3, $4, $5)
        """
        print(f"Executing query: {query}")

        try:

            user_id = await self.db.execute(query, user.name, user.email, hashed_password, user.gender, user.termsAccepted)
            print(f"User created with ID: {user_id}")
            return {"message": "User created successfully", "user_id": user_id}
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=400, detail=f"Error creating user: {str(e)}")

    async def login(self, email: str, password: str):

        query = "SELECT * FROM users WHERE email = $1"
        user = await self.db.fetch_one(query, email)

        if not user:
            raise HTTPException(status_code=400, detail="Email does not exist")
        
        if not pwd_context.verify(password, user['password']):
            raise HTTPException(status_code=400, detail="Invalid password")

        # Create JWT token
        access_token = jwt.encode({"sub": email}, SECRET_KEY, algorithm="HS256")
        return {"access_token": access_token, "token_type": "bearer"}

    async def logout(self):
        return {"message": "User logged out successfully"}

    async def forgot_password(self, email: str):
        query = "SELECT * FROM users WHERE email = $1"
        user = await self.db.fetch_one(query, email)

        if not user:
            raise HTTPException(status_code=400, detail="Email does not exist")

        # Send a password reset email (you can implement this with an email service)
        return {"message": "Password reset email sent successfully"}

    async def reset_password(self, email: str, new_password: str):
        hashed_password = pwd_context.hash(new_password)

        query = "UPDATE users SET password = $1 WHERE email = $2"
        result = await self.db.execute(query, hashed_password, email)

        if result != "UPDATE 1":
            raise HTTPException(status_code=400, detail="Error updating password")
        return {"message": "Password reset successfully"}

    async def get_user_profile(self, email: str):
        query = "SELECT * FROM users WHERE email = $1"
        user = await self.db.fetch_one(query, email)

        if not user:
            raise HTTPException(status_code=400, detail="Email does not exist")

        return {
            "name": user['name'],
            "email": user['email'],
            "gender": user['gender']
        }

    async def update_user_profile(self, email: str, profile_data: BaseModel):
        query = """
        UPDATE users SET name = $1, profile_picture = $2, bio = $3, updated_at = NOW()
        WHERE email = $4
        """
        result = await self.db.execute(query, profile_data.name, profile_data.profilePicture, profile_data.bio, email)

        if result != "UPDATE 1":
            raise HTTPException(status_code=400, detail="Error updating profile")
        return {"message": "User profile updated successfully"}
