from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from database.connection import get_db
from models import Manufacturer
from schemas.manufacturer import Manufacturer, ManufacturerCreate, ManufacturerUpdate

router = APIRouter(prefix="/manufacturers", tags=["manufacturers"])

@router.get("/", response_model=List[Manufacturer])
async def get_manufacturers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Manufacturer).offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.get("/{manufacturer_id}", response_model=Manufacturer)
async def get_manufacturer(
    manufacturer_id: int,
    db: AsyncSession = Depends(get_db)
):
    manufacturer = await db.get(Manufacturer, manufacturer_id)
    if not manufacturer:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    return manufacturer

@router.post("/", response_model=Manufacturer, status_code=201)
async def create_manufacturer(
    manufacturer: ManufacturerCreate,
    db: AsyncSession = Depends(get_db)
):
    db_manufacturer = Manufacturer(**manufacturer.model_dump())
    db.add(db_manufacturer)
    await db.commit()
    await db.refresh(db_manufacturer)
    return db_manufacturer
