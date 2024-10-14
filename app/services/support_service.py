from fastapi import HTTPException, status
from app.db.postgres import PostgresDB
from app.models import support_models


class SupportService:
    def __init__(self, db: PostgresDB) -> None:
        self.db = db
    
    async def fetch_faq(self):
        query = """
                select * from faq"""
        print(f"Executing Query: {query}")
        try:
            faqs = await self.db.fetch(query)
            return faqs
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=400, detail=f"Error fetching faq: {str(e)}")
    
    async def submit_ticket(self, ticket: support_models.CreateTicket):
        query = """
                INSER INTO tickets (userId, issueDescription) values ($1, $2)"""
        try:

            ticket_id = await self.db.execute(query, ticket.userId, ticket.isssueDescrption)
            print(f"Ticket Raised Successfully: {ticket_id}")
            return {"message": "Ticker Raised successfully", "ticket_id": ticket_id}
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=400, detail=f"Error raising ticket: {str(e)}")
        
