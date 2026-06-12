from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from typing import List, Optional, Dict, Any
from decimal import Decimal

from database.connection import get_db
from models.product import Product as ProductModel
from models.bearing import Bearing
from models.gearbox import Gearbox
from schemas.product import Product as ProductSchema
from schemas.bearing import Bearing as BearingSchema
from schemas.gearbox import Gearbox as GearboxSchema

router = APIRouter(prefix="/selection", tags=["selection"])

class SelectionParams(BaseModel):
    equipment_type: str  # "motor", "bearing", "gearbox"
    power_kw_min: Optional[float] = None
    power_kw_max: Optional[float] = None
    speed_rpm_min: Optional[int] = None
    speed_rpm_max: Optional[int] = None
    bore_diameter_min: Optional[float] = None
    bore_diameter_max: Optional[float] = None
    outer_diameter_min: Optional[float] = None
    outer_diameter_max: Optional[float] = None
    width_min: Optional[float] = None
    width_max: Optional[float] = None
    ratio_min: Optional[float] = None
    ratio_max: Optional[float] = None
    manufacturer_id: Optional[int] = None

class SelectionResult(BaseModel):
    products: List[ProductSchema] = []
    bearings: List[BearingSchema] = []
    gearboxes: List[GearboxSchema] = []

@router.post("/", response_model=SelectionResult)
async def search_by_parameters(
    params: SelectionParams,
    db: AsyncSession = Depends(get_db)
):
    """Поиск оборудования по заданным параметрам"""
    result = SelectionResult()

    if params.equipment_type == "motor" or params.equipment_type == "all":
        # Запрос к продуктам (двигателям)
        query = select(ProductModel).where(ProductModel.is_active == True)
        if params.power_kw_min is not None:
            query = query.where(ProductModel.power_kw >= params.power_kw_min)
        if params.power_kw_max is not None:
            query = query.where(ProductModel.power_kw <= params.power_kw_max)
        if params.speed_rpm_min is not None:
            query = query.where(ProductModel.speed_rpm >= params.speed_rpm_min)
        if params.speed_rpm_max is not None:
            query = query.where(ProductModel.speed_rpm <= params.speed_rpm_max)
        if params.manufacturer_id is not None:
            query = query.where(ProductModel.manufacturer_id == params.manufacturer_id)
        query = query.limit(50)
        motor_result = await db.execute(query)
        motors = motor_result.scalars().all()
        result.products = motors

    if params.equipment_type == "bearing" or params.equipment_type == "all":
        # Запрос к подшипникам
        query = select(Bearing).where(Bearing.is_active == True)
        if params.bore_diameter_min is not None:
            query = query.where(Bearing.bore_diameter_mm >= params.bore_diameter_min)
        if params.bore_diameter_max is not None:
            query = query.where(Bearing.bore_diameter_mm <= params.bore_diameter_max)
        if params.outer_diameter_min is not None:
            query = query.where(Bearing.outer_diameter_mm >= params.outer_diameter_min)
        if params.outer_diameter_max is not None:
            query = query.where(Bearing.outer_diameter_mm <= params.outer_diameter_max)
        if params.width_min is not None:
            query = query.where(Bearing.width_mm >= params.width_min)
        if params.width_max is not None:
            query = query.where(Bearing.width_mm <= params.width_max)
        if params.manufacturer_id is not None:
            query = query.where(Bearing.manufacturer_id == params.manufacturer_id)
        query = query.limit(50)
        bearing_result = await db.execute(query)
        bearings = bearing_result.scalars().all()
        result.bearings = bearings

    if params.equipment_type == "gearbox" or params.equipment_type == "all":
        # Запрос к редукторам
        query = select(Gearbox).where(Gearbox.is_active == True)
        if params.power_kw_min is not None:
            query = query.where(Gearbox.input_power_kw >= params.power_kw_min)
        if params.power_kw_max is not None:
            query = query.where(Gearbox.input_power_kw <= params.power_kw_max)
        if params.ratio_min is not None:
            query = query.where(Gearbox.ratio >= params.ratio_min)
        if params.ratio_max is not None:
            query = query.where(Gearbox.ratio <= params.ratio_max)
        if params.speed_rpm_min is not None:
            query = query.where(Gearbox.output_speed_rpm >= params.speed_rpm_min)
        if params.speed_rpm_max is not None:
            query = query.where(Gearbox.output_speed_rpm <= params.speed_rpm_max)
        if params.manufacturer_id is not None:
            query = query.where(Gearbox.manufacturer_id == params.manufacturer_id)
        query = query.limit(50)
        gearbox_result = await db.execute(query)
        gearboxes = gearbox_result.scalars().all()
        result.gearboxes = gearboxes

    return result
