import json
from sqlalchemy.ext.asyncio import AsyncSession
from models.request import Request
from schemas.request import RequestCreate

class RequestService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_request(self, req_data: RequestCreate) -> Request:
        items_json = json.dumps([item.dict() for item in req_data.items], ensure_ascii=False)
        request = Request(
            customer_name=req_data.customer_name,
            customer_email=req_data.customer_email,
            customer_phone=req_data.customer_phone,
            company_name=req_data.company_name,
            comment=req_data.comment,
            items=items_json
        )
        self.db.add(request)
        await self.db.commit()
        await self.db.refresh(request)
        return request
