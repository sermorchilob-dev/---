import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import AsyncSessionLocal
from models.manufacturer import Manufacturer
from models.category import Category
from models.product import Product
from sqlalchemy import select

async def seed_products():
    async with AsyncSessionLocal() as session:
        # --- Производители (если ещё нет) ---
        # Добавляем Siemens, ABB, SEW, если их нет
        manufacturers_data = [
            {"name": "Siemens", "country": "Германия"},
            {"name": "ABB", "country": "Швеция"},
            {"name": "SEW-Eurodrive", "country": "Германия"},
        ]
        for m_data in manufacturers_data:
            result = await session.execute(
                select(Manufacturer).where(Manufacturer.name == m_data["name"])
            )
            if not result.scalar_one_or_none():
                m = Manufacturer(**m_data)
                session.add(m)
        await session.flush()

        # --- Категории ---
        categories_data = [
            {"name": "Асинхронные двигатели", "category_type": "motor"},
        ]
        for c_data in categories_data:
            result = await session.execute(
                select(Category).where(Category.name == c_data["name"])
            )
            if not result.scalar_one_or_none():
                c = Category(**c_data)
                session.add(c)
        await session.flush()

        # Получаем ID созданных записей
        siemens = (await session.execute(select(Manufacturer).where(Manufacturer.name == "Siemens"))).scalar_one()
        abb = (await session.execute(select(Manufacturer).where(Manufacturer.name == "ABB"))).scalar_one()
        sew = (await session.execute(select(Manufacturer).where(Manufacturer.name == "SEW-Eurodrive"))).scalar_one()
        motor_cat = (await session.execute(select(Category).where(Category.name == "Асинхронные двигатели"))).scalar_one()

        # --- Продукты (двигатели) ---
        products_data = [
            {
                "product_code": "1LA7136-4AB10",
                "name": "Асинхронный двигатель 5.5 кВт 1500 об/мин",
                "power_kw": 5.5,
                "speed_rpm": 1500,
                "voltage": "400V",
                "mounting_type": "IM B3",
                "ip_rating": "IP55",
                "price": 45000,
                "manufacturer_id": siemens.id,
                "category_id": motor_cat.id,
                "in_stock": True,
            },
            {
                "product_code": "1LA7136-4AC10",
                "name": "Асинхронный двигатель 7.5 кВт 1500 об/мин",
                "power_kw": 7.5,
                "speed_rpm": 1500,
                "voltage": "400V",
                "mounting_type": "IM B5",
                "ip_rating": "IP55",
                "price": 52000,
                "manufacturer_id": siemens.id,
                "category_id": motor_cat.id,
                "in_stock": True,
            },
            {
                "product_code": "M2BAX160MLB4",
                "name": "Асинхронный двигатель 11 кВт 1500 об/мин ABB",
                "power_kw": 11.0,
                "speed_rpm": 1500,
                "voltage": "400V",
                "mounting_type": "IM B3",
                "ip_rating": "IP55",
                "price": 65000,
                "manufacturer_id": abb.id,
                "category_id": motor_cat.id,
                "in_stock": True,
            },
            {
                "product_code": "DRN80MK4",
                "name": "Асинхронный двигатель SEW 1.5 кВт",
                "power_kw": 1.5,
                "speed_rpm": 1400,
                "voltage": "400V",
                "mounting_type": "IM B3",
                "ip_rating": "IP55",
                "price": 25000,
                "manufacturer_id": sew.id,
                "category_id": motor_cat.id,
                "in_stock": True,
            },
        ]

        added = 0
        for data in products_data:
            existing = await session.execute(
                select(Product).where(Product.product_code == data["product_code"])
            )
            if not existing.scalar_one_or_none():
                product = Product(**data)
                session.add(product)
                added += 1
            else:
                print(f"⏩ Продукт {data['product_code']} уже существует")

        await session.commit()
        print(f"🎉 Добавлено {added} новых продуктов")

if __name__ == "__main__":
    asyncio.run(seed_products())
