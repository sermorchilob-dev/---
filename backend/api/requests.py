from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from services.request_service import RequestService
from schemas.request import RequestCreate, RequestOut

router = APIRouter(prefix="/requests", tags=["requests"])

@router.post("/", response_model=RequestOut, status_code=status.HTTP_201_CREATED)
async def create_request(
    req_data: RequestCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создать новую заявку на КП"""
    service = RequestService(db)
    try:
        request = await service.create_request(req_data)
        return request
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
