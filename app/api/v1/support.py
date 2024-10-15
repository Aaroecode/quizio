from fastapi import APIRouter, Depends, HTTPException
from app.services.support_service import SupportService
from app.core.security import get_current_user
from app.models import support_models
from app.db.postgres import PostgresDB

db = PostgresDB("postgresql://admin:admin@localhost:5432/quizo") 
supportService = SupportService(db)

router = APIRouter()

@router.get("/api/support/faqs", response_model= dict)
async def faq(user: dict = Depends(get_current_user)):
    return await supportService.fetch_faq()

@router.post("/api/support/ticket", response_model= dict)
async def ticket(ticket: support_models.CreateTicket, user: dict = Depends(get_current_user)):
    try:
        ticket_id = await supportService.submit_ticket(ticket)
        return ticket_id
    except HTTPException as e:
        raise e
