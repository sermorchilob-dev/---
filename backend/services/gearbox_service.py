from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from typing import Optional, List
from decimal import Decimal

from models.gearbox import Gearbox
from schemas.gearbox import GearboxCreate, GearboxUpdate

class GearboxService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_gearboxes(
        self,
        skip: int = 0,
        limit: int = 100,
        gearbox_type: Optional[str] = None,
        series: Optional[str] = None,
        input_power_min: Optional[Decimal] = None,
        input_power_max: Optional[Decimal] = None,
        output_torque_min: Optional[Decimal] = None,
        output_torque_max: Optional[Decimal] = None,
        ratio_min: Optional[Decimal] = None,
        ratio_max: Optional[Decimal] = None,
        manufacturer_id: Optional[int] = None,
        search: Optional[str] = None,
    ) -> List[Gearbox]:
        query = select(Gearbox).where(Gearbox.is_active == True)

        if gearbox_type:
            query = query.where(Gearbox.gearbox_type == gearbox_type)
        if series:
            query = query.where(Gearbox.series == series)
        if input_power_min is not None:
            query = query.where(Gearbox.input_power_kw >= input_power_min)
        if input_power_max is not None:
            query = query.where(Gearbox.input_power_kw <= input_power_max)
        if output_torque_min is not None:
            query = query.where(Gearbox.output_torque_nm >= output_torque_min)
        if output_torque_max is not None:
            query = query.where(Gearbox.output_torque_nm <= output_torque_max)
        if ratio_min is not None:
            query = query.where(Gearbox.ratio >= ratio_min)
        if ratio_max is not None:
            query = query.where(Gearbox.ratio <= ratio_max)
        if manufacturer_id is not None:
            query = query.where(Gearbox.manufacturer_id == manufacturer_id)
        if search:
            query = query.where(
                or_(
                    Gearbox.gearbox_number.ilike(f"%{search}%"),
                    Gearbox.name.ilike(f"%{search}%"),
                )
            )

        query = query.offset(skip).limit(limit).order_by(Gearbox.gearbox_number)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_gearbox_by_id(self, gearbox_id: int) -> Optional[Gearbox]:
        query = select(Gearbox).where(
            Gearbox.id == gearbox_id,
            Gearbox.is_active == True
        ).options(
            selectinload(Gearbox.manufacturer)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_gearbox_by_number(self, gearbox_number: str) -> Optional[Gearbox]:
        query = select(Gearbox).where(
            Gearbox.gearbox_number == gearbox_number,
            Gearbox.is_active == True
        ).options(
            selectinload(Gearbox.manufacturer)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_gearbox(self, gearbox_data: GearboxCreate) -> Gearbox:
        gearbox = Gearbox(**gearbox_data.model_dump())
        self.db.add(gearbox)
        await self.db.commit()
        await self.db.refresh(gearbox)
        return gearbox

    async def update_gearbox(
        self,
        gearbox_id: int,
        gearbox_data: GearboxUpdate
    ) -> Optional[Gearbox]:
        gearbox = await self.get_gearbox_by_id(gearbox_id)
        if not gearbox:
            return None
        for field, value in gearbox_data.model_dump(exclude_unset=True).items():
            setattr(gearbox, field, value)
        await self.db.commit()
        await self.db.refresh(gearbox)
        return gearbox

    async def delete_gearbox(self, gearbox_id: int) -> bool:
        gearbox = await self.get_gearbox_by_id(gearbox_id)
        if not gearbox:
            return False
        gearbox.is_active = False
        await self.db.commit()
        return True
