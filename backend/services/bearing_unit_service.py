from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from typing import Optional, List
from decimal import Decimal

from models.bearing_unit import BearingUnit
from schemas.bearing_unit import BearingUnitCreate, BearingUnitUpdate

class BearingUnitService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_bearing_units(
        self,
        skip: int = 0,
        limit: int = 100,
        shaft_diameter_min: Optional[Decimal] = None,
        shaft_diameter_max: Optional[Decimal] = None,
        housing_type: Optional[str] = None,
        manufacturer_id: Optional[int] = None
    ) -> List[BearingUnit]:
        query = select(BearingUnit).where(BearingUnit.is_active == True)

        if shaft_diameter_min is not None:
            query = query.where(BearingUnit.shaft_diameter_mm >= shaft_diameter_min)
        if shaft_diameter_max is not None:
            query = query.where(BearingUnit.shaft_diameter_mm <= shaft_diameter_max)
        if housing_type is not None:
            query = query.where(BearingUnit.housing_type == housing_type)
        if manufacturer_id is not None:
            query = query.where(BearingUnit.manufacturer_id == manufacturer_id)

        query = query.offset(skip).limit(limit).order_by(BearingUnit.unit_number)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_bearing_unit_by_id(self, unit_id: int) -> Optional[BearingUnit]:
        query = select(BearingUnit).where(
            BearingUnit.id == unit_id,
            BearingUnit.is_active == True
        ).options(
            selectinload(BearingUnit.manufacturer),
            selectinload(BearingUnit.bearing)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_bearing_unit_by_number(self, unit_number: str) -> Optional[BearingUnit]:
        query = select(BearingUnit).where(
            BearingUnit.unit_number == unit_number,
            BearingUnit.is_active == True
        ).options(
            selectinload(BearingUnit.manufacturer),
            selectinload(BearingUnit.bearing)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_bearing_unit(self, unit_data: BearingUnitCreate) -> BearingUnit:
        unit = BearingUnit(**unit_data.model_dump())
        self.db.add(unit)
        await self.db.commit()
        await self.db.refresh(unit)
        return unit

    async def update_bearing_unit(
        self,
        unit_id: int,
        unit_data: BearingUnitUpdate
    ) -> Optional[BearingUnit]:
        unit = await self.get_bearing_unit_by_id(unit_id)
        if not unit:
            return None
        for field, value in unit_data.model_dump(exclude_unset=True).items():
            setattr(unit, field, value)
        await self.db.commit()
        await self.db.refresh(unit)
        return unit

    async def delete_bearing_unit(self, unit_id: int) -> bool:
        unit = await self.get_bearing_unit_by_id(unit_id)
        if not unit:
            return False
        unit.is_active = False
        await self.db.commit()
        return True
