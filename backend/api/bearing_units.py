from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from decimal import Decimal

from database.connection import get_db
from services.bearing_unit_service import BearingUnitService
from schemas.bearing_unit import BearingUnit, BearingUnitCreate, BearingUnitUpdate, BearingUnitWithRelations

router = APIRouter(prefix="/bearing-units", tags=["bearing-units"])

@router.get("/", response_model=List[BearingUnit])
async def get_bearing_units(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    shaft_diameter_min: Optional[float] = Query(None, ge=0, description="Min shaft diameter (mm)"),
    shaft_diameter_max: Optional[float] = Query(None, ge=0, description="Max shaft diameter (mm)"),
    housing_type: Optional[str] = Query(None, description="Housing type (e.g. PILLOW_BLOCK)"),
    manufacturer_id: Optional[int] = Query(None, description="Filter by manufacturer ID"),
    db: AsyncSession = Depends(get_db)
):
    """Get list of bearing units with optional filters"""
    service = BearingUnitService(db)
    units = await service.get_bearing_units(
        skip=skip,
        limit=limit,
        shaft_diameter_min=Decimal(str(shaft_diameter_min)) if shaft_diameter_min else None,
        shaft_diameter_max=Decimal(str(shaft_diameter_max)) if shaft_diameter_max else None,
        housing_type=housing_type,
        manufacturer_id=manufacturer_id
    )
    return units

@router.get("/{unit_id}", response_model=BearingUnitWithRelations)
async def get_bearing_unit(
    unit_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get bearing unit by ID with related data"""
    service = BearingUnitService(db)
    unit = await service.get_bearing_unit_by_id(unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Bearing unit not found")
    return unit

@router.get("/by-number/{unit_number}", response_model=BearingUnit)
async def get_bearing_unit_by_number(
    unit_number: str,
    db: AsyncSession = Depends(get_db)
):
    """Get bearing unit by its number (e.g. UCP 204)"""
    service = BearingUnitService(db)
    unit = await service.get_bearing_unit_by_number(unit_number)
    if not unit:
        raise HTTPException(status_code=404, detail="Bearing unit not found")
    return unit

@router.post("/", response_model=BearingUnit, status_code=201)
async def create_bearing_unit(
    unit_data: BearingUnitCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new bearing unit"""
    service = BearingUnitService(db)
    # Check uniqueness
    existing = await service.get_bearing_unit_by_number(unit_data.unit_number)
    if existing:
        raise HTTPException(status_code=400, detail="Unit number already exists")
    unit = await service.create_bearing_unit(unit_data)
    return unit

@router.put("/{unit_id}", response_model=BearingUnit)
async def update_bearing_unit(
    unit_id: int,
    unit_data: BearingUnitUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update bearing unit"""
    service = BearingUnitService(db)
    unit = await service.update_bearing_unit(unit_id, unit_data)
    if not unit:
        raise HTTPException(status_code=404, detail="Bearing unit not found")
    return unit

@router.delete("/{unit_id}", status_code=204)
async def delete_bearing_unit(
    unit_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Soft delete bearing unit"""
    service = BearingUnitService(db)
    deleted = await service.delete_bearing_unit(unit_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bearing unit not found")
    return None
