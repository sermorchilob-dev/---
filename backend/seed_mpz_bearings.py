import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import AsyncSessionLocal
from models.bearing import (
    BearingManufacturer,
    BearingType,
    BearingSeries,
    Bearing
)
from sqlalchemy import select

async def seed_mpz_bearings():
    async with AsyncSessionLocal() as session:
        # --- 1. Производитель МПЗ ---
        result = await session.execute(
            select(BearingManufacturer).where(BearingManufacturer.name == "МПЗ")
        )
        mpz = result.scalar_one_or_none()
        if not mpz:
            mpz = BearingManufacturer(
                name="МПЗ",
                country="Беларусь",
                website="http://www.mpz.com.by"
            )
            session.add(mpz)
            await session.flush()
            print("➕ Добавлен производитель МПЗ")
        else:
            print("✅ Производитель МПЗ уже существует")

        # --- 2. Типы подшипников ---
        # Шариковый радиальный
        result = await session.execute(
            select(BearingType).where(BearingType.code == "DEEP_GROOVE")
        )
        deep_groove = result.scalar_one_or_none()
        if not deep_groove:
            deep_groove = BearingType(
                name="Шариковый радиальный",
                code="DEEP_GROOVE",
                description="Однорядный шариковый радиальный подшипник"
            )
            session.add(deep_groove)
            await session.flush()
            print("➕ Добавлен тип 'Шариковый радиальный'")
        else:
            print("✅ Тип 'Шариковый радиальный' уже существует")

        # Роликовый сферический
        result = await session.execute(
            select(BearingType).where(BearingType.code == "SPHERICAL_ROLLER")
        )
        spherical_roller = result.scalar_one_or_none()
        if not spherical_roller:
            spherical_roller = BearingType(
                name="Роликовый сферический",
                code="SPHERICAL_ROLLER",
                description="Двухрядный роликовый сферический подшипник"
            )
            session.add(spherical_roller)
            await session.flush()
            print("➕ Добавлен тип 'Роликовый сферический'")
        else:
            print("✅ Тип 'Роликовый сферический' уже существует")

        # --- 3. Серии подшипников ---
        series_list = [
            {"series_code": "6200", "name": "Легкая серия", "bearing_type_id": deep_groove.id},
            {"series_code": "6300", "name": "Средняя серия", "bearing_type_id": deep_groove.id},
            {"series_code": "22200", "name": "Сферическая легкая серия", "bearing_type_id": spherical_roller.id},
            {"series_code": "22300", "name": "Сферическая средняя серия", "bearing_type_id": spherical_roller.id},
        ]
        series_map = {}
        for s in series_list:
            result = await session.execute(
                select(BearingSeries).where(BearingSeries.series_code == s["series_code"])
            )
            series = result.scalar_one_or_none()
            if not series:
                series = BearingSeries(**s)
                session.add(series)
                await session.flush()
                print(f"➕ Добавлена серия {s['series_code']}")
            else:
                print(f"✅ Серия {s['series_code']} уже существует")
            series_map[s["series_code"]] = series.id

        await session.commit()  # сохраняем, чтобы id были доступны

        # --- 4. Подшипники (данные из каталога МПЗ) ---
        bearings_data = [
            # Серия 6200 (шариковые радиальные)
            {
                "bearing_number": "6204",
                "series_id": series_map["6200"],
                "bearing_type_id": deep_groove.id,
                "manufacturer_id": mpz.id,
                "bore_diameter_mm": 20,
                "outer_diameter_mm": 47,
                "width_mm": 14,
                "dynamic_load_rating_kn": 12.7,
                "static_load_rating_kn": 6.65,
                "limiting_speed_rpm": 15000,
                "weight_kg": 0.106,
                "seal_type": "OPEN",
                "clearance": "CN",
            },
            {
                "bearing_number": "6205",
                "series_id": series_map["6200"],
                "bearing_type_id": deep_groove.id,
                "manufacturer_id": mpz.id,
                "bore_diameter_mm": 25,
                "outer_diameter_mm": 52,
                "width_mm": 15,
                "dynamic_load_rating_kn": 14.0,
                "static_load_rating_kn": 7.8,
                "limiting_speed_rpm": 13000,
                "weight_kg": 0.129,
                "seal_type": "OPEN",
                "clearance": "CN",
            },
            {
                "bearing_number": "6206",
                "series_id": series_map["6200"],
                "bearing_type_id": deep_groove.id,
                "manufacturer_id": mpz.id,
                "bore_diameter_mm": 30,
                "outer_diameter_mm": 62,
                "width_mm": 16,
                "dynamic_load_rating_kn": 19.5,
                "static_load_rating_kn": 11.3,
                "limiting_speed_rpm": 11000,
                "weight_kg": 0.199,
                "seal_type": "OPEN",
                "clearance": "CN",
            },
            {
                "bearing_number": "6207",
                "series_id": series_map["6200"],
                "bearing_type_id": deep_groove.id,
                "manufacturer_id": mpz.id,
                "bore_diameter_mm": 35,
                "outer_diameter_mm": 72,
                "width_mm": 17,
                "dynamic_load_rating_kn": 25.5,
                "static_load_rating_kn": 15.3,
                "limiting_speed_rpm": 9500,
                "weight_kg": 0.288,
                "seal_type": "OPEN",
                "clearance": "CN",
            },
            {
                "bearing_number": "6208",
                "series_id": series_map["6200"],
                "bearing_type_id": deep_groove.id,
                "manufacturer_id": mpz.id,
                "bore_diameter_mm": 40,
                "outer_diameter_mm": 80,
                "width_mm": 18,
                "dynamic_load_rating_kn": 30.7,
                "static_load_rating_kn": 19.0,
                "limiting_speed_rpm": 8500,
                "weight_kg": 0.366,
                "seal_type": "OPEN",
                "clearance": "CN",
            },
            # Серия 6300 (шариковые радиальные)
            {
                "bearing_number": "6304",
                "series_id": series_map["6300"],
                "bearing_type_id": deep_groove.id,
                "manufacturer_id": mpz.id,
                "bore_diameter_mm": 20,
                "outer_diameter_mm": 52,
                "width_mm": 15,
                "dynamic_load_rating_kn": 15.9,
                "static_load_rating_kn": 7.8,
                "limiting_speed_rpm": 13000,
                "weight_kg": 0.144,
                "seal_type": "OPEN",
                "clearance": "CN",
            },
            {
                "bearing_number": "6305",
                "series_id": series_map["6300"],
                "bearing_type_id": deep_groove.id,
                "manufacturer_id": mpz.id,
                "bore_diameter_mm": 25,
                "outer_diameter_mm": 62,
                "width_mm": 17,
                "dynamic_load_rating_kn": 22.5,
                "static_load_rating_kn": 11.4,
                "limiting_speed_rpm": 11000,
                "weight_kg": 0.230,
                "seal_type": "OPEN",
                "clearance": "CN",
            },
            {
                "bearing_number": "6306",
                "series_id": series_map["6300"],
                "bearing_type_id": deep_groove.id,
                "manufacturer_id": mpz.id,
                "bore_diameter_mm": 30,
                "outer_diameter_mm": 72,
                "width_mm": 19,
                "dynamic_load_rating_kn": 29.6,
                "static_load_rating_kn": 16.0,
                "limiting_speed_rpm": 9500,
                "weight_kg": 0.345,
                "seal_type": "OPEN",
                "clearance": "CN",
            },
            {
                "bearing_number": "6307",
                "series_id": series_map["6300"],
                "bearing_type_id": deep_groove.id,
                "manufacturer_id": mpz.id,
                "bore_diameter_mm": 35,
                "outer_diameter_mm": 80,
                "width_mm": 21,
                "dynamic_load_rating_kn": 33.4,
                "static_load_rating_kn": 19.2,
                "limiting_speed_rpm": 8500,
                "weight_kg": 0.457,
                "seal_type": "OPEN",
                "clearance": "CN",
            },
            {
                "bearing_number": "6308",
                "series_id": series_map["6300"],
                "bearing_type_id": deep_groove.id,
                "manufacturer_id": mpz.id,
                "bore_diameter_mm": 40,
                "outer_diameter_mm": 90,
                "width_mm": 23,
                "dynamic_load_rating_kn": 41.0,
                "static_load_rating_kn": 24.0,
                "limiting_speed_rpm": 7500,
                "weight_kg": 0.633,
                "seal_type": "OPEN",
                "clearance": "CN",
            },
            # Роликовые сферические (примеры)
            {
                "bearing_number": "22208",
                "series_id": series_map["22200"],
                "bearing_type_id": spherical_roller.id,
                "manufacturer_id": mpz.id,
                "bore_diameter_mm": 40,
                "outer_diameter_mm": 80,
                "width_mm": 23,
                "dynamic_load_rating_kn": 90.5,
                "static_load_rating_kn": 96.5,
                "limiting_speed_rpm": 5300,
                "weight_kg": 0.53,
                "seal_type": "OPEN",
                "clearance": "CN",
            },
            {
                "bearing_number": "22308",
                "series_id": series_map["22300"],
                "bearing_type_id": spherical_roller.id,
                "manufacturer_id": mpz.id,
                "bore_diameter_mm": 40,
                "outer_diameter_mm": 90,
                "width_mm": 33,
                "dynamic_load_rating_kn": 124.0,
                "static_load_rating_kn": 143.0,
                "limiting_speed_rpm": 4300,
                "weight_kg": 0.95,
                "seal_type": "OPEN",
                "clearance": "CN",
            },
            {
                "bearing_number": "22210",
                "series_id": series_map["22200"],
                "bearing_type_id": spherical_roller.id,
                "manufacturer_id": mpz.id,
                "bore_diameter_mm": 50,
                "outer_diameter_mm": 90,
                "width_mm": 23,
                "dynamic_load_rating_kn": 97.0,
                "static_load_rating_kn": 114.0,
                "limiting_speed_rpm": 4800,
                "weight_kg": 0.61,
                "seal_type": "OPEN",
                "clearance": "CN",
            },
            {
                "bearing_number": "22310",
                "series_id": series_map["22300"],
                "bearing_type_id": spherical_roller.id,
                "manufacturer_id": mpz.id,
                "bore_diameter_mm": 50,
                "outer_diameter_mm": 110,
                "width_mm": 40,
                "dynamic_load_rating_kn": 186.0,
                "static_load_rating_kn": 216.0,
                "limiting_speed_rpm": 3800,
                "weight_kg": 1.55,
                "seal_type": "OPEN",
                "clearance": "CN",
            },
        ]

        added = 0
        for data in bearings_data:
            # Проверяем, нет ли уже такого подшипника (по номеру)
            existing = await session.execute(
                select(Bearing).where(Bearing.bearing_number == data["bearing_number"])
            )
            if not existing.scalar_one_or_none():
                bearing = Bearing(**data)
                session.add(bearing)
                added += 1
            else:
                print(f"⏩ Подшипник {data['bearing_number']} уже существует")

        await session.commit()
        print(f"🎉 Добавлено {added} новых подшипников МПЗ")

if __name__ == "__main__":
    asyncio.run(seed_mpz_bearings())
