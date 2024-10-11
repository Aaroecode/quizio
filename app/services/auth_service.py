from fastapi import HTTPException, status


class AuthService():
    def __init__(self) -> None:
        pass

    def signup(self, name:str, email: str, password:str, gender:str, termsAccepted:bool):
        if termsAccepted is False:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="User did not accept Terms and condition")
        elif email in 