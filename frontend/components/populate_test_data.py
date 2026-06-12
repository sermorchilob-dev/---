#!/usr/bin/env python3
"""
Скрипт для наполнения БД тестовыми данными (электродвигатели, пневмоцилиндры).
Использует асинхронный SQLAlchemy.
Запуск: python populate_test_data.py
"""

import asyncio
import sys
# В самом начале скрипта, после импортов
import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")

if not DATABASE_URL or not REDIS_URL:
    print("❌ Ошибка: переменные окружения DATABASE_URL и REDIS_URL не найдены.")
    print("Убедитесь, что вы создали файл .env и заполнили его.")
    sys.exit(1)
from datetime import datetime
from decimal import Decimal

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# Конфигурация подключения (измените при необходимости)
DATABASE_URL = 
postgresql://postgres:d20s11d02v83i79@db.mujugcwbzvnhcdozfxmz.supabase.co:5432/postgres

# Импорт моделей (предполагаем, что файлы моделей доступны по этим путям)
# Если структура отличается, подправьте импорты
try:
    from app.models import (
        Base, ProductCategory, Manufacturer, Product,
        ProductSpecification, MountingOption, ConnectionSpec
    )
except ImportError:
    # Если модели определены в другом месте, попробуем относительный импорт
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent))
    from models import (
        Base, ProductCategory, Manufacturer, Product,
        ProductSpecification, MountingOption, ConnectionSpec
    )

# ------------------------------------------------------------
# Данные для заполнения
# ------------------------------------------------------------

MANUFACTURERS = [
    {"name": "Siemens", "short_name": "SIE", "country_code": "DE"},
    {"name": "ABB", "short_name": "ABB", "country_code": "CH"},
    {"name": "SEW-Eurodrive", "short_name": "SEW", "country_code": "DE"},
    {"name": "Festo", "short_name": "FES", "country_code": "DE"},
    {"name": "Parker", "short_name": "PAR", "country_code": "US"},
]

CATEGORIES = [
    {"category_type": "electric_motor", "name": "Асинхронный двигатель", "parent_id": None},
    {"category_type": "electric_motor", "name": "Серводвигатель", "parent_id": None},
    {"category_type": "pneumatic_cylinder", "name": "Пневмоцилиндр поршневой", "parent_id": None},
    {"category_type": "hydraulic_cylinder", "name": "Гидроцилиндр", "parent_id": None},
]

# Электродвигатели (20 штук)
MOTORS = [
    # Siemens
    {"code": "1LA7096-4AB10", "name": "Siemens 1LA7 5.5 кВт 1500 об/мин", "manufacturer": "Siemens",
     "power": 5.5, "voltage": "400V", "speed": 1500, "torque": 35.0, "price": 45000,
     "mounting": "IM B3", "ip": "IP55", "eff_class": "IE3"},
    {"code": "1LA7096-4AB11", "name": "Siemens 1LA7 7.5 кВт 1500 об/мин", "manufacturer": "Siemens",
     "power": 7.5, "voltage": "400V", "speed": 1500, "torque": 47.7, "price": 52000,
     "mounting": "IM B3", "ip": "IP55", "eff_class": "IE3"},
    {"code": "1LA7106-4AB10", "name": "Siemens 1LA7 11 кВт 1500 об/мин", "manufacturer": "Siemens",
     "power": 11.0, "voltage": "400V", "speed": 1500, "torque": 70.0, "price": 68000,
     "mounting": "IM B5", "ip": "IP55", "eff_class": "IE3"},
    {"code": "1LA7136-4AB10", "name": "Siemens 1LA7 5.5 кВт 1000 об/мин", "manufacturer": "Siemens",
     "power": 5.5, "voltage": "400V", "speed": 1000, "torque": 52.5, "price": 49000,
     "mounting": "IM B3", "ip": "IP55", "eff_class": "IE3"},
    # ABB
    {"code": "M2BAX90LA4", "name": "ABB M2BAX 1.5 кВт 1500 об/мин", "manufacturer": "ABB",
     "power": 1.5, "voltage": "400V", "speed": 1500, "torque": 9.8, "price": 18500,
     "mounting": "IM B14", "ip": "IP55", "eff_class": "IE2"},
    {"code": "M2BAX100LB4", "name": "ABB M2BAX 3.0 кВт 1500 об/мин", "manufacturer": "ABB",
     "power": 3.0, "voltage": "400V", "speed": 1500, "torque": 19.5, "price": 24500,
     "mounting": "IM B3", "ip": "IP55", "eff_class": "IE2"},
    {"code": "M2BAX132SB4", "name": "ABB M2BAX 5.5 кВт 1500 об/мин", "manufacturer": "ABB",
     "power": 5.5, "voltage": "400V", "speed": 1500, "torque": 36.0, "price": 38000,
     "mounting": "IM B3", "ip": "IP55", "eff_class": "IE3"},
    {"code": "M3BP160MLA4", "name": "ABB M3BP 15 кВт 1500 об/мин", "manufacturer": "ABB",
     "power": 15.0, "voltage": "400V", "speed": 1500, "torque": 95.5, "price": 89000,
     "mounting": "IM B5", "ip": "IP55", "eff_class": "IE3"},
    # SEW
    {"code": "DRS80M4", "name": "SEW DRS80M4 1.1 кВт 1500 об/мин", "manufacturer": "SEW-Eurodrive",
     "power": 1.1, "voltage": "400V", "speed": 1500, "torque": 7.2, "price": 22000,
     "mounting": "IM B14", "ip": "IP54", "eff_class": "IE3"},
    {"code": "DRS90L4", "name": "SEW DRS90L4 1.5 кВт 1500 об/мин", "manufacturer": "SEW-Eurodrive",
     "power": 1.5, "voltage": "400V", "speed": 1500, "torque": 9.8, "price": 26800,
     "mounting": "IM B3", "ip": "IP55", "eff_class": "IE3"},
    {"code": "DRS112M4", "name": "SEW DRS112M4 4.0 кВт 1500 об/мин", "manufacturer": "SEW-Eurodrive",
     "power": 4.0, "voltage": "400V", "speed": 1500, "torque": 26.0, "price": 41500,
     "mounting": "IM B5", "ip": "IP55", "eff_class": "IE3"},
    {"code": "DRS132S4", "name": "SEW DRS132S4 5.5 кВт 1500 об/мин", "manufacturer": "SEW-Eurodrive",
     "power": 5.5, "voltage": "400V", "speed": 1500, "torque": 36.0, "price": 49800,
     "mounting": "IM B3", "ip": "IP55", "eff_class": "IE3"},
    # Дополнительные разной мощности
    {"code": "1LA7076-4AB10", "name": "Siemens 1LA7 2.2 кВт 1500 об/мин", "manufacturer": "Siemens",
     "power": 2.2, "voltage": "400V", "speed": 1500, "torque": 14.5, "price": 28500,
     "mounting": "IM B3", "ip": "IP55", "eff_class": "IE3"},
    {"code": "1LA7086-4AB10", "name": "Siemens 1LA7 4.0 кВт 1500 об/мин", "manufacturer": "Siemens",
     "power": 4.0, "voltage": "400V", "speed": 1500, "torque": 25.5, "price": 36500,
     "mounting": "IM B3", "ip": "IP55", "eff_class": "IE3"},
    {"code": "1LA7166-4AB10", "name": "Siemens 1LA7 18.5 кВт 1500 об/мин", "manufacturer": "Siemens",
     "power": 18.5, "voltage": "400V", "speed": 1500, "torque": 118.0, "price": 112000,
     "mounting": "IM B5", "ip": "IP55", "eff_class": "IE3"},
    {"code": "M2BAX160MLA4", "name": "ABB M2BAX 15 кВт 1500 об/мин", "manufacturer": "ABB",
     "power": 15.0, "voltage": "400V", "speed": 1500, "torque": 95.5, "price": 85000,
     "mounting": "IM B3", "ip": "IP55", "eff_class": "IE3"},
    {"code": "M3BP200MLA4", "name": "ABB M3BP 30 кВт 1500 об/мин", "manufacturer": "ABB",
     "power": 30.0, "voltage": "400V", "speed": 1500, "torque": 191.0, "price": 155000,
     "mounting": "IM B3", "ip": "IP55", "eff_class": "IE4"},
    {"code": "DRS160M4", "name": "SEW DRS160M4 11 кВт 1500 об/мин", "manufacturer": "SEW-Eurodrive",
     "power": 11.0, "voltage": "400V", "speed": 1500, "torque": 70.0, "price": 89000,
     "mounting": "IM B5", "ip": "IP55", "eff_class": "IE3"},
    {"code": "DRS180M4", "name": "SEW DRS180M4 18.5 кВт 1500 об/мин", "manufacturer": "SEW-Eurodrive",
     "power": 18.5, "voltage": "400V", "speed": 1500, "torque": 118.0, "price": 129000,
     "mounting": "IM B3", "ip": "IP55", "eff_class": "IE3"},
]

# Пневмоцилиндры (5 штук)
CYLINDERS = [
    {"code": "DSNU-25-50-P-A", "name": "Festo DSNU-25-50", "manufacturer": "Festo",
     "pressure": 10.0, "bore": 25, "stroke": 50, "force": 490, "price": 4500,
     "mounting": "Передняя лапка", "material": "Алюминий"},
    {"code": "DSNU-32-100-P-A", "name": "Festo DSNU-32-100", "manufacturer": "Festo",
     "pressure": 10.0, "bore": 32, "stroke": 100, "force": 804, "price": 6200,
     "mounting": "Задняя лапка", "material": "Алюминий"},
    {"code": "DNC-50-200-PPV-A", "name": "Festo DNC-50-200", "manufacturer": "Festo",
     "pressure": 10.0, "bore": 50, "stroke": 200, "force": 1963, "price": 12800,
     "mounting": "Фланцевое", "material": "Алюминий"},
    {"code": "P1D-S063MS-0200", "name": "Parker P1D 63x200", "manufacturer": "Parker",
     "pressure": 10.0, "bore": 63, "stroke": 200, "force": 3117, "price": 16500,
     "mounting": "Сквозной шток", "material": "Нержавеющая сталь"},
    {"code": "P1D-S080MS-0300", "name": "Parker P1D 80x300", "manufacturer": "Parker",
     "pressure": 10.0, "bore": 80, "stroke": 300, "force": 5026, "price": 22400,
     "mounting": "Передняя лапка", "material": "Нержавеющая сталь"},
]

# ------------------------------------------------------------
# Вспомогательные функции
# ------------------------------------------------------------

async def clear_data(session: AsyncSession):
    """Очистить таблицы в правильном порядке (с учетом FK)"""
    print("Очистка существующих данных...")
    # Отключаем проверку FK для очистки
    await session.execute(text("TRUNCATE TABLE product_specifications RESTART IDENTITY CASCADE;"))
    await session.execute(text("TRUNCATE TABLE mounting_options RESTART IDENTITY CASCADE;"))
    await session.execute(text("TRUNCATE TABLE connection_specs RESTART IDENTITY CASCADE;"))
    await session.execute(text("TRUNCATE TABLE products RESTART IDENTITY CASCADE;"))
    await session.execute(text("TRUNCATE TABLE manufacturers RESTART IDENTITY CASCADE;"))
    await session.execute(text("TRUNCATE TABLE product_categories RESTART IDENTITY CASCADE;"))
    await session.commit()
    print("Очистка завершена.")

async def populate(session: AsyncSession):
    """Заполнение данными"""
    print("Начинаем заполнение БД...")
    
    # 1. Производители
    manufacturers_dict = {}
    for m in MANUFACTURERS:
        obj = Manufacturer(**m)
        session.add(obj)
        manufacturers_dict[m["name"]] = obj
    await session.flush()  # чтобы получить id
    print(f"Добавлено {len(MANUFACTURERS)} производителей")
    
    # 2. Категории
    categories_dict = {}
    for cat in CATEGORIES:
        obj = ProductCategory(**{k: v for k, v in cat.items() if k != "parent_id"})
        if cat["parent_id"]:
            obj.parent_category_id = cat["parent_id"]
        session.add(obj)
    await session.flush()
    # Получаем id категорий по имени
    motor_cat = next(c for c in CATEGORIES if c["name"] == "Асинхронный двигатель")
    motor_cat_id = None
    pneum_cat = next(c for c in CATEGORIES if c["name"] == "Пневмоцилиндр поршневой")
    pneum_cat_id = None
    for obj in session.new:
        if isinstance(obj, ProductCategory):
            if obj.name == "Асинхронный двигатель":
                motor_cat_id = obj.id
            if obj.name == "Пневмоцилиндр поршневой":
                pneum_cat_id = obj.id
    print(f"Категории: электродвигатели id={motor_cat_id}, пневмоцилиндры id={pneum_cat_id}")
    
    # 3. Электродвигатели
    for m in MOTORS:
        manufacturer = manufacturers_dict.get(m["manufacturer"])
        if not manufacturer:
            print(f"Производитель {m['manufacturer']} не найден, пропускаем {m['code']}")
            continue
        product = Product(
            product_code=m["code"],
            manufacturer_sku=m["code"],
            category_id=motor_cat_id,
            manufacturer_id=manufacturer.id,
            name=m["name"],
            power_kw=Decimal(str(m["power"])),
            voltage=m["voltage"],
            speed_rpm=m["speed"],
            torque_nm=Decimal(str(m["torque"])) if "torque" in m else None,
            price=Decimal(str(m["price"])),
            currency="RUB",
            is_active=True,
        )
        session.add(product)
        await session.flush()  # чтобы получить product.id
        
        # Спецификации (IP, класс КПД)
        specs = [
            {"spec_group": "electrical", "spec_key": "ip_rating", "spec_name": "Степень защиты",
             "spec_value": m["ip"]},
            {"spec_group": "electrical", "spec_key": "efficiency_class", "spec_name": "Класс КПД",
             "spec_value": m["eff_class"]},
            {"spec_group": "mechanical", "spec_key": "bearing", "spec_name": "Подшипник",
             "spec_value": "6308-2Z/C3", "spec_unit": None},
        ]
        for spec in specs:
            spec_obj = ProductSpecification(
                product_id=product.id,
                **spec
            )
            session.add(spec_obj)
        
        # Монтажное исполнение
        mounting = MountingOption(
            product_id=product.id,
            standard_code="IEC",
            mounting_code=m["mounting"],
            mounting_name={"IM B3": "На лапах", "IM B5": "Фланцевое", "IM B14": "Комбинированное"}.get(m["mounting"], m["mounting"]),
            is_primary=True
        )
        session.add(mounting)
        
        # Присоединение (вал)
        conn = ConnectionSpec(
            product_id=product.id,
            connection_type="shaft",
            shaft_diameter_mm=Decimal(str(38 if m["power"] < 5.5 else 42 if m["power"] < 11 else 48)),
            shaft_length_mm=Decimal("80"),
            shaft_type="cylindrical"
        )
        session.add(conn)
    
    print(f"Добавлено {len(MOTORS)} электродвигателей")
    
    # 4. Пневмоцилиндры
    for c in CYLINDERS:
        manufacturer = manufacturers_dict.get(c["manufacturer"])
        if not manufacturer:
            print(f"Производитель {c['manufacturer']} не найден, пропускаем {c['code']}")
            continue
        product = Product(
            product_code=c["code"],
            manufacturer_sku=c["code"],
            category_id=pneum_cat_id,
            manufacturer_id=manufacturer.id,
            name=c["name"],
            pressure_max_bar=Decimal(str(c["pressure"])),
            bore_diameter_mm=c["bore"],
            stroke_mm=c["stroke"],
            torque_nm=Decimal(str(c["force"])) if "force" in c else None,
            price=Decimal(str(c["price"])),
            currency="RUB",
            is_active=True,
        )
        session.add(product)
        await session.flush()
        
        # Спецификации
        specs = [
            {"spec_group": "pneumatic", "spec_key": "material", "spec_name": "Материал корпуса",
             "spec_value": c["material"]},
            {"spec_group": "pneumatic", "spec_key": "medium", "spec_name": "Рабочая среда",
             "spec_value": "Сжатый воздух"},
        ]
        for spec in specs:
            spec_obj = ProductSpecification(
                product_id=product.id,
                **spec
            )
            session.add(spec_obj)
        
        # Монтажное исполнение
        mounting = MountingOption(
            product_id=product.id,
            mounting_code=c["mounting"],
            mounting_name=c["mounting"],
            is_primary=True
        )
        session.add(mounting)
    
    print(f"Добавлено {len(CYLINDERS)} пневмоцилиндров")
    await session.commit()
    print("Наполнение БД успешно завершено!")

# ------------------------------------------------------------
# Основная функция
# ------------------------------------------------------------
async def main():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Раскомментируйте следующую строку, если хотите очистить перед заполнением
        # await clear_data(session)
        await populate(session)
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())