import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import AsyncSessionLocal
from models.bearing_unit import BearingUnit, HousingType, HousingMaterial
from models.bearing import BearingManufacturer  # ИСПРАВЛЕНО
from sqlalchemy import select

async def seed_initial_bearing_units():
    async with AsyncSessionLocal() as session:
        # Создаём производителя ASAHI, если его нет
        result = await session.execute(select(BearingManufacturer).where(BearingManufacturer.name == "ASAHI"))
        asahi = result.scalar_one_or_none()
        if not asahi:
            asahi = BearingManufacturer(name="ASAHI", country="Japan", website="https://www.asahi-seiko.co.jp/")
            session.add(asahi)
            await session.flush()
            print("➕ Добавлен производитель ASAHI")
        else:
            print("✅ Производитель ASAHI уже есть")

        # Данные из каталога ASAHI (страница 8, UCP 201–204)
        units_data = [
            {
                "unit_number": "UCP 201",
                "shaft_diameter_mm": 12,
                "housing_type": HousingType.PILLOW_BLOCK,
                "housing_material": HousingMaterial.CAST_IRON,
                "a_mm": 127,
                "e_mm": 95,
                "i_mm": 38,
                "g_mm": 13.2,
                "l_mm": 165,
                "s_mm": 15,
                "b_mm": 31,
                "weight_kg": 0.65,
                "dynamic_load_kn": 12.7,
                "static_load_kn": 6.65,
            },
            {
                "unit_number": "UCP 202",
                "shaft_diameter_mm": 15,
                "housing_type": HousingType.PILLOW_BLOCK,
                "housing_material": HousingMaterial.CAST_IRON,
                "a_mm": 127,
                "e_mm": 95,
                "i_mm": 38,
                "g_mm": 13.2,
                "l_mm": 165,
                "s_mm": 15,
                "b_mm": 31,
                "weight_kg": 0.63,
                "dynamic_load_kn": 12.7,
                "static_load_kn": 6.65,
            },
            {
                "unit_number": "UCP 203",
                "shaft_diameter_mm": 17,
                "housing_type": HousingType.PILLOW_BLOCK,
                "housing_material": HousingMaterial.CAST_IRON,
                "a_mm": 127,
                "e_mm": 95,
                "i_mm": 38,
                "g_mm": 13.2,
                "l_mm": 165,
                "s_mm": 15,
                "b_mm": 31,
                "weight_kg": 0.62,
                "dynamic_load_kn": 12.7,
                "static_load_kn": 6.65,
            },
            {
                "unit_number": "UCP 204",
                "shaft_diameter_mm": 20,
                "housing_type": HousingType.PILLOW_BLOCK,
                "housing_material": HousingMaterial.CAST_IRON,
                "a_mm": 127,
                "e_mm": 95,
                "i_mm": 38,
                "g_mm": 13.2,
                "l_mm": 165,
                "s_mm": 15,
                "b_mm": 31,
                "weight_kg": 0.65,
                "dynamic_load_kn": 12.8,
                "static_load_kn": 6.65,
            },
        ]

        added = 0
        for data in units_data:
            # Проверка на дубликат
            existing = await session.execute(
                select(BearingUnit).where(BearingUnit.unit_number == data["unit_number"])
            )
            if not existing.scalar_one_or_none():
                unit = BearingUnit(**data, manufacturer_id=asahi.id)
                session.add(unit)
                added += 1
            else:
                print(f"⏩ {data['unit_number']} уже существует")

        await session.commit()
        print(f"🎉 Добавлено {added} новых подшипниковых узлов ASAHI")

if __name__ == "__main__":
    asyncio.run(seed_initial_bearing_units())
