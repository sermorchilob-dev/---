import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import AsyncSessionLocal
from models.manufacturer import Manufacturer
from models.gearbox import Gearbox, GearboxType, MountingPosition
from sqlalchemy import select

async def seed_gearboxes():
    async with AsyncSessionLocal() as session:
        # --- 1. Производитель ESQ (Элком) ---
        result = await session.execute(
            select(Manufacturer).where(Manufacturer.name == "Элком (ESQ)")
        )
        esq = result.scalar_one_or_none()
        if not esq:
            esq = Manufacturer(
                name="Элком (ESQ)",
                country="Россия",
                website="https://elcomspb.ru"
            )
            session.add(esq)
            await session.flush()
            print("➕ Добавлен производитель Элком (ESQ)")
        else:
            print("✅ Производитель Элком (ESQ) уже существует")

        # --- 2. Данные из каталога ESQ (червячные редукторы NMRW) ---
        gearboxes_data = [
            # NMRW 030 (страница 28, 0.12 кВт)
            {
                "gearbox_number": "NMRW 030-80",
                "name": "Червячный редуктор NMRW 030 i=80",
                "gearbox_type": GearboxType.WORM,
                "series": "NMRW",
                "input_power_kw": 0.12,
                "output_torque_nm": 95,
                "ratio": 80,
                "input_speed_rpm": 1400,
                "output_speed_rpm": 17.5,
                "service_factor": 0.85,
                "efficiency": 77.4,  # из таблицы на стр. 36
                "weight_kg": 1.2,
                "mounting_position": MountingPosition.M1,
                "output_shaft_diameter_mm": 18,
                "output_shaft_length_mm": 30,
            },
            {
                "gearbox_number": "NMRW 030-60",
                "name": "Червячный редуктор NMRW 030 i=60",
                "gearbox_type": GearboxType.WORM,
                "series": "NMRW",
                "input_power_kw": 0.12,
                "output_torque_nm": 91,
                "ratio": 60,
                "input_speed_rpm": 1400,
                "output_speed_rpm": 23.3,
                "service_factor": 0.89,
                "efficiency": 80.2,
                "weight_kg": 1.2,
                "mounting_position": MountingPosition.M1,
                "output_shaft_diameter_mm": 18,
                "output_shaft_length_mm": 30,
            },
            # NMRW 040 (страница 28, 0.12 кВт)
            {
                "gearbox_number": "NMRW 040-80",
                "name": "Червячный редуктор NMRW 040 i=80",
                "gearbox_type": GearboxType.WORM,
                "series": "NMRW",
                "input_power_kw": 0.12,
                "output_torque_nm": 166,
                "ratio": 80,
                "input_speed_rpm": 1400,
                "output_speed_rpm": 17.5,
                "service_factor": 0.99,
                "efficiency": 80.0,
                "weight_kg": 2.3,
                "mounting_position": MountingPosition.M1,
                "output_shaft_diameter_mm": 18,
                "output_shaft_length_mm": 30,
            },
            {
                "gearbox_number": "NMRW 040-60",
                "name": "Червячный редуктор NMRW 040 i=60",
                "gearbox_type": GearboxType.WORM,
                "series": "NMRW",
                "input_power_kw": 0.12,
                "output_torque_nm": 150,
                "ratio": 60,
                "input_speed_rpm": 1400,
                "output_speed_rpm": 23.3,
                "service_factor": 1.05,
                "efficiency": 82.0,
                "weight_kg": 2.3,
                "mounting_position": MountingPosition.M1,
                "output_shaft_diameter_mm": 18,
                "output_shaft_length_mm": 30,
            },
            # NMRW 050 (страница 28, 0.18 кВт)
            {
                "gearbox_number": "NMRW 050-80",
                "name": "Червячный редуктор NMRW 050 i=80",
                "gearbox_type": GearboxType.WORM,
                "series": "NMRW",
                "input_power_kw": 0.18,
                "output_torque_nm": 210,
                "ratio": 80,
                "input_speed_rpm": 1400,
                "output_speed_rpm": 17.5,
                "service_factor": 1.0,
                "efficiency": 81.0,
                "weight_kg": 3.8,
                "mounting_position": MountingPosition.M1,
                "output_shaft_diameter_mm": 25,
                "output_shaft_length_mm": 40,
            },
        ]

        added = 0
        for data in gearboxes_data:
            existing = await session.execute(
                select(Gearbox).where(Gearbox.gearbox_number == data["gearbox_number"])
            )
            if not existing.scalar_one_or_none():
                gearbox = Gearbox(**data, manufacturer_id=esq.id)
                session.add(gearbox)
                added += 1
            else:
                print(f"⏩ Редуктор {data['gearbox_number']} уже существует")

        await session.commit()
        print(f"🎉 Добавлено {added} новых редукторов ESQ")

if __name__ == "__main__":
    asyncio.run(seed_gearboxes())