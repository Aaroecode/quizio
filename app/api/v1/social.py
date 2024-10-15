# api/v1/social_api.py

from fastapi import APIRouter, Depends, HTTPException
from db.postgres import PostgresDB
from services.social_service import SocialService
from models.social_models import InviteFriendSchema, FollowUserSchema

router = APIRouter()
db = PostgresDB("postgresql://admin:admin@localhost:5432/quizo")
social_service = SocialService(db)

@router.post("/user/invite", response_model=dict)
async def invite_friend(data: InviteFriendSchema):
    try:
       
        result = await social_service.invite_friend(data.referrer_id, data.invitee_email)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/referral-rewards", response_model=dict)
async def get_referral_rewards(user_id: int):
    try:
        result = await social_service.get_referral_rewards(user_id)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/user/{user_id}/follow", response_model=dict)
async def follow_unfollow_user(data: FollowUserSchema):
    try:
        result = await social_service.follow_unfollow_user(data.follower_id, data.followee_id)
        return {"status": "success", "message": result["message"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
