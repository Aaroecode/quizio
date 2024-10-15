from pydantic import BaseModel

class InviteFriendSchema(BaseModel):
    referrer_id: int
    invitee_email: str

class FollowUserSchema(BaseModel):
    follower_id: int
    followee_id: int
