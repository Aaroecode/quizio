
from app.db.postgres import PostgresDB
from models.social_models import InviteFriendSchema, FollowUserSchema

class SocialService:
    def __init__(self, db: PostgresDB):
        self.db = db
    

    async def invite_friend(self, referrer_id: int, invitee_email: str):
        referrer = await self.db.fetch("SELECT id FROM users WHERE id = $1", referrer_id)
        if not referrer:
            raise ValueError("Referrer not found")
        # Insert into referral invites
        await self.db.execute(
            """
            INSERT INTO referral_invites (referrer_id, invitee_email) 
            VALUES ($1, $2)
            """, referrer_id, invitee_email
        )
        return {"message": "Invite sent successfully"}

   
    async def get_referral_rewards(self, user_id: int):
        rewards = await self.db.fetch(
            "SELECT referral_rewards FROM users WHERE id = $1", user_id
        )
        if not rewards:
            raise ValueError("User not found")
        return {"user_id": user_id, "referral_rewards": rewards["referral_rewards"]}

   
    async def follow_unfollow_user(self, follower_id: int, followee_id: int):
        
       
        follower = await self.db.fetch("SELECT id FROM users WHERE id = $1", follower_id)
        followee = await self.db.fetch("SELECT id FROM users WHERE id = $1", followee_id)
        if not follower or not followee:
            raise ValueError("User not found")
        follow_status = await self.db.fetch(
            "SELECT id FROM user_follows WHERE follower_id = $1 AND followee_id = $2",
            follower_id, followee_id
        )
        if follow_status:
            await self.db.execute(
                "DELETE FROM user_follows WHERE follower_id = $1 AND followee_id = $2",
                follower_id, followee_id
            )
            return {"message": f"User {follower_id} unfollowed user {followee_id}"}
        else:
            await self.db.execute(
                "INSERT INTO user_follows (follower_id, followee_id) VALUES ($1, $2)",
                follower_id, followee_id
            )
            return {"message": f"User {follower_id} followed user {followee_id}"}
