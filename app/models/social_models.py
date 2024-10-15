from pydantic import BaseModel, EmailStr

class InviteFriendSchema(BaseModel):
    referrer_id: int
    invitee_email: EmailStr

class FollowUserSchema(BaseModel):
    follower_id: int
    followee_id: int
