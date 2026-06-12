
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from decimal import Decimal

from database.connection import get_db
from services.gearbox_service import GearboxService
from schemas.gearbox import Gearbox, GearboxCreate, GearboxUpdate, GearboxWithManufacturer

router = APIRouter(prefix="/gearboxes", tags=["gearboxes"])

@router.get("/", response_model=List[Gearbox])
async def get_gearboxes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    gearbox_type: Optional[str] = Query(None, description="Filter by gearbox type (WORM, HELICAL, etc.)"),
    series: Optional[str] = Query(None, description="Filter by series (NMRW, R, KA, etc.)"),
    input_power_min: Optional[float] = Query(None, ge=0, description="Min input power (kW)"),
    input_power_max: Optional[float] = Query(None, ge=0, description="Max input power (kW)"),
    output_torque_min: Optional[float] = Query(None, ge=0, description="Min output torque (Nm)"),
    output_torque_max: Optional[float] = Query(None, ge=0, description="Max output torque (Nm)"),
    ratio_min: Optional[float] = Query(None, ge=0, description="Min gear ratio"),
    ratio_max: Optional[float] = Query(None, ge=0, description="Max gear ratio"),
    manufacturer_id: Optional[int] = Query(None, description="Filter by manufacturer ID"),
    search: Optional[str] = Query(None, description="Search by gearbox number or name"),
    db: AsyncSession = Depends(get_db)
):
    """Get list of gearboxes with optional filters"""
    service = GearboxService(db)
    gearboxes = await service.get_gearboxes(
        skip=skip,
        limit=limit,
        gearbox_type=gearbox_type,
        series=series,
        input_power_min=Decimal(str(input_power_min)) if input_power_min else None,
        input_power_max=Decimal(str(input_power_max)) if input_power_max else None,
        output_torque_min=Decimal(str(output_torque_min)) if output_torque_min else None,
        output_torque_max=Decimal(str(output_torque_max)) if output_torque_max else None,
        ratio_min=Decimal(str(ratio_min)) if ratio_min else None,
        ratio_max=Decimal(str(ratio_max)) if ratio_max else None,
        manufacturer_id=manufacturer_id,
        search=search,
    )
    return gearboxes

@router.get("/{gearbox_id}", response_model=GearboxWithManufacturer)
async def get_gearbox(
    gearbox_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get gearbox by ID with manufacturer info"""
    service = GearboxService(db)
    gearbox = await service.get_gearbox_by_id(gearbox_id)
    if not gearbox:
        raise HTTPException(status_code=404, detail="Gearbox not found")
    return gearbox

@router.get("/by-number/{gearbox_number}", response_model=GearboxWithManufacturer)
async def get_gearbox_by_number(
    gearbox_number: str,
    db: AsyncSession = Depends(get_db)
):
    """Get gearbox by its model number (e.g. NMRW 030-80)"""
    service = GearboxService(db)
    gearbox = await service.get_gearbox_by_number(gearbox_number)
    if not gearbox:
        raise HTTPException(status_code=404, detail="Gearbox not found")
    return gearbox

@router.post("/", response_model=Gearbox, status_code=201)
async def create_gearbox(
    gearbox_data: GearboxCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new gearbox (admin use)"""
    service = GearboxService(db)
    existing = await service.get_gearbox_by_number(gearbox_data.gearbox_number)
    if existing:
        raise HTTPException(status_code=400, detail="Gearbox number already exists")
    gearbox = await service.create_gearbox(gearbox_data)
    return gearbox

@router.put("/{gearbox_id}", response_model=Gearbox)
async def update_gearbox(
    gearbox_id: int,
    gearbox_data: GearboxUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update gearbox"""
    service = GearboxService(db)
    gearbox = await service.update_gearbox(gearbox_id, gearbox_data)
    if not gearbox:
        raise HTTPException(status_code=404, detail="Gearbox not found")
    return gearbox

@router.delete("/{gearbox_id}", status_code=204)
async def delete_gearbox(
    gearbox_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Soft delete gearbox"""
    service = GearboxService(db)
    deleted = await service.delete_gearbox(gearbox_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Gearbox not found")
    return None

  
 