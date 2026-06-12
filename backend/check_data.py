# check_data.py
import asyncio
from database.connection import AsyncSessionLocal
from sqlalchemy import select, func
from models.bearing import Bearing
from models.bearing_unit import BearingUnit
from models.gearbox import Gearbox
from models.product import Product

async def check():
    async with AsyncSessionLocal() as session:
        for model, name in [(Bearing, "Подшипники"), (BearingUnit, "Узлы ASAHI"), (Gearbox, "Редукторы ESQ"), (Product, "Продукты")]:
            count = await session.scalar(select(func.count()).select_from(model))
            print(f"{name}: {count} записей")

asyncio.run(check())