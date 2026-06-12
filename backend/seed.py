import asyncio
import random
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import AsyncSessionLocal, init_db
from models import (
    Manufacturer, Category, Product, 
    BearingType, BearingManufacturer, BearingSeries, Bearing
)
from datetime import datetime

async def seed_database():
    """Заполнение базы данных тестовыми данными"""
    print("🌱 Начинаем заполнение базы данных...")
    
    async with AsyncSessionLocal() as session:
        
        # ============== ПРОИЗВОДИТЕЛИ ==============
        print("📦 Создаем производителей...")
        manufacturers = [
            Manufacturer(name="Siemens", country="Германия", 
                        website="https://www.siemens.com",
                        description="Ведущий мировой производитель электрооборудования"),
            Manufacturer(name="ABB", country="Швеция", 
                        website="https://new.abb.com",
                        description="Шведско-швейцарская компания, производитель электрооборудования"),
            Manufacturer(name="SEW-Eurodrive", country="Германия", 
                        website="https://www.sew-eurodrive.de",
                        description="Производитель приводной техники"),
            Manufacturer(name="Lenze", country="Германия", 
                        website="https://www.lenze.com",
                        description="Производитель электроприводов и автоматизации"),
            Manufacturer(name="WEG", country="Бразилия", 
                        website="https://www.weg.net",
                        description="Производитель электродвигателей"),
        ]
        session.add_all(manufacturers)
        await session.flush()
        print(f"  ✅ Добавлено {len(manufacturers)} производителей")
        
        # ============== КАТЕГОРИИ ==============
        print("📂 Создаем категории...")
        categories = [
            Category(name="Асинхронные двигатели", 
                    category_type="motor",
                    description="Трехфазные асинхронные электродвигатели общепромышленного применения"),
            Category(name="Серводвигатели", 
                    category_type="motor",
                    description="Высокоточные серводвигатели для позиционирования"),
            Category(name="Взрывозащищенные двигатели", 
                    category_type="motor",
                    description="Двигатели для химической и нефтегазовой промышленности"),
            Category(name="Крановые двигатели", 
                    category_type="motor",
                    description="Двигатели для кранового оборудования"),
            Category(name="Подшипники качения", 
                    category_type="bearing",
                    description="Подшипники для промышленного оборудования"),
        ]
        session.add_all(categories)
        await session.flush()
        print(f"  ✅ Добавлено {len(categories)} категорий")
        
        # ============== ПРОДУКТЫ (ДВИГАТЕЛИ) ==============
        print("⚙️ Создаем продукты (двигатели)...")
        products = [
            # Siemens
            Product(
                product_code="1LA7136-4AB10",
                name="Асинхронный двигатель 5.5 кВт 1500 об/мин",
                power_kw=5.5,
                speed_rpm=1500,
                voltage="400V",
                current_a=11.2,
                efficiency=87.5,
                mounting_type="IM B3",
                shaft_diameter_mm=38,
                shaft_length_mm=80,
                ip_rating="IP55",
                insulation_class="F",
                weight_kg=45.5,
                price=45000,
                manufacturer_id=manufacturers[0].id,  # Siemens
                category_id=categories[0].id,  # Асинхронные
                in_stock=True
            ),
            Product(
                product_code="1LA7136-4AC10",
                name="Асинхронный двигатель 7.5 кВт 1500 об/мин",
                power_kw=7.5,
                speed_rpm=1500,
                voltage="400V",
                current_a=14.8,
                efficiency=88.2,
                mounting_type="IM B5",
                shaft_diameter_mm=42,
                shaft_length_mm=110,
                ip_rating="IP55",
                insulation_class="F",
                weight_kg=52.0,
                price=52000,
                manufacturer_id=manufacturers[0].id,  # Siemens
                category_id=categories[0].id,
                in_stock=True
            ),
            Product(
                product_code="1LA7136-4AD10",
                name="Асинхронный двигатель 11 кВт 1500 об/мин",
                power_kw=11.0,
                speed_rpm=1500,
                voltage="400V",
                current_a=21.5,
                efficiency=89.5,
                mounting_type="IM B3",
                shaft_diameter_mm=42,
                shaft_length_mm=110,
                ip_rating="IP55",
                insulation_class="F",
                weight_kg=68.0,
                price=68000,
                manufacturer_id=manufacturers[0].id,  # Siemens
                category_id=categories[0].id,
                in_stock=True
            ),
            
            # ABB
            Product(
                product_code="M2BAX160MLB4",
                name="Асинхронный двигатель 11 кВт 1500 об/мин ABB",
                power_kw=11.0,
                speed_rpm=1500,
                voltage="400V",
                current_a=21.0,
                efficiency=90.0,
                mounting_type="IM B3",
                shaft_diameter_mm=42,
                shaft_length_mm=110,
                ip_rating="IP55",
                insulation_class="F",
                weight_kg=65.0,
                price=65000,
                manufacturer_id=manufacturers[1].id,  # ABB
                category_id=categories[0].id,
                in_stock=True
            ),
            Product(
                product_code="M2BAX180MLB4",
                name="Асинхронный двигатель 15 кВт 1500 об/мин ABB",
                power_kw=15.0,
                speed_rpm=1500,
                voltage="400V",
                current_a=28.5,
                efficiency=91.0,
                mounting_type="IM B5",
                shaft_diameter_mm=48,
                shaft_length_mm=110,
                ip_rating="IP55",
                insulation_class="F",
                weight_kg=85.0,
                price=85000,
                manufacturer_id=manufacturers[1].id,  # ABB
                category_id=categories[0].id,
                in_stock=True
            ),
            
            # SEW
            Product(
                product_code="DRN80MK4",
                name="Асинхронный двигатель SEW 1.5 кВт",
                power_kw=1.5,
                speed_rpm=1400,
                voltage="400V",
                current_a=3.4,
                efficiency=84.0,
                mounting_type="IM B3",
                shaft_diameter_mm=24,
                shaft_length_mm=50,
                ip_rating="IP55",
                insulation_class="F",
                weight_kg=18.0,
                price=25000,
                manufacturer_id=manufacturers[2].id,  # SEW
                category_id=categories[0].id,
                in_stock=True
            ),
            Product(
                product_code="DRN90LK4",
                name="Асинхронный двигатель SEW 2.2 кВт",
                power_kw=2.2,
                speed_rpm=1420,
                voltage="400V",
                current_a=4.8,
                efficiency=85.0,
                mounting_type="IM B3",
                shaft_diameter_mm=28,
                shaft_length_mm=60,
                ip_rating="IP55",
                insulation_class="F",
                weight_kg=22.0,
                price=32000,
                manufacturer_id=manufacturers[2].id,  # SEW
                category_id=categories[0].id,
                in_stock=True
            ),
        ]
        session.add_all(products)
        await session.flush()
        print(f"  ✅ Добавлено {len(products)} продуктов")
        
        # ============== ТИПЫ ПОДШИПНИКОВ ==============
        print("🔧 Создаем типы подшипников...")
        bearing_types = [
            BearingType(name="Шариковый радиальный", code="DEEP_GROOVE",
                       description="Однорядный шариковый радиальный подшипник"),
            BearingType(name="Шариковый радиально-упорный", code="ANGULAR_CONTACT",
                       description="Шариковый радиально-упорный подшипник"),
            BearingType(name="Роликовый радиальный", code="CYLINDRICAL",
                       description="Цилиндрический роликовый подшипник"),
            BearingType(name="Роликовый конический", code="TAPERED",
                       description="Конический роликовый подшипник"),
        ]
        session.add_all(bearing_types)
        await session.flush()
        print(f"  ✅ Добавлено {len(bearing_types)} типов подшипников")
        
        # ============== ПРОИЗВОДИТЕЛИ ПОДШИПНИКОВ ==============
        print("🏭 Создаем производителей подшипников...")
        bearing_manufacturers = [
            BearingManufacturer(name="SKF", country="Швеция",
                              website="https://www.skf.com"),
            BearingManufacturer(name="FAG", country="Германия",
                              website="https://www.schaeffler.com"),
            BearingManufacturer(name="NSK", country="Япония",
                              website="https://www.nsk.com"),
            BearingManufacturer(name="Timken", country="США",
                              website="https://www.timken.com"),
        ]
        session.add_all(bearing_manufacturers)
        await session.flush()
        print(f"  ✅ Добавлено {len(bearing_manufacturers)} производителей подшипников")
        
        # ============== СЕРИИ ПОДШИПНИКОВ ==============
        print("📊 Создаем серии подшипников...")
        bearing_series = [
            BearingSeries(series_code="6200", name="Легкая серия",
                        bearing_type_id=bearing_types[0].id,
                        description="Шариковые подшипники легкой серии"),
            BearingSeries(series_code="6300", name="Средняя серия",
                        bearing_type_id=bearing_types[0].id,
                        description="Шариковые подшипники средней серии"),
            BearingSeries(series_code="16000", name="Очень легкая серия",
                        bearing_type_id=bearing_types[0].id,
                        description="Шариковые подшипники очень легкой серии"),
        ]
        session.add_all(bearing_series)
        await session.flush()
        print(f"  ✅ Добавлено {len(bearing_series)} серий подшипников")
        
        # ============== ПОДШИПНИКИ ==============
        print("⚙️ Создаем подшипники...")
        bearings = [
            # SKF
            Bearing(
                bearing_number="6204-2Z",
                manufacturer_id=bearing_manufacturers[0].id,  # SKF
                series_id=bearing_series[0].id,
                bearing_type_id=bearing_types[0].id,
                bore_diameter_mm=20,
                outer_diameter_mm=47,
                width_mm=14,
                dynamic_load_rating_kn=12.7,
                static_load_rating_kn=6.55,
                limiting_speed_rpm=15000,
                seal_type="2Z",
                clearance="CN",
                weight_kg=0.106,
                price=850,
                application="Электродвигатели, насосы"
            ),
            Bearing(
                bearing_number="6204-2RS1",
                manufacturer_id=bearing_manufacturers[0].id,  # SKF
                series_id=bearing_series[0].id,
                bearing_type_id=bearing_types[0].id,
                bore_diameter_mm=20,
                outer_diameter_mm=47,
                width_mm=14,
                dynamic_load_rating_kn=12.7,
                static_load_rating_kn=6.55,
                limiting_speed_rpm=9000,
                seal_type="2RS1",
                clearance="CN",
                weight_kg=0.108,
                price=980,
                application="Электродвигатели с повышенной защитой"
            ),
            # FAG
            Bearing(
                bearing_number="6304-2Z",
                manufacturer_id=bearing_manufacturers[1].id,  # FAG
                series_id=bearing_series[1].id,
                bearing_type_id=bearing_types[0].id,
                bore_diameter_mm=20,
                outer_diameter_mm=52,
                width_mm=15,
                dynamic_load_rating_kn=15.9,
                static_load_rating_kn=7.8,
                limiting_speed_rpm=13000,
                seal_type="2Z",
                clearance="C3",
                weight_kg=0.144,
                price=1100,
                application="Электродвигатели, редукторы"
            ),
            # NSK
            Bearing(
                bearing_number="6205-2Z",
                manufacturer_id=bearing_manufacturers[2].id,  # NSK
                series_id=bearing_series[0].id,
                bearing_type_id=bearing_types[0].id,
                bore_diameter_mm=25,
                outer_diameter_mm=52,
                width_mm=15,
                dynamic_load_rating_kn=14.8,
                static_load_rating_kn=7.8,
                limiting_speed_rpm=13000,
                seal_type="2Z",
                clearance="CN",
                weight_kg=0.128,
                price=950,
                application="Электродвигатели, вентиляторы"
            ),
            # Timken
            Bearing(
                bearing_number="30206",
                manufacturer_id=bearing_manufacturers[3].id,  # Timken
                bearing_type_id=bearing_types[3].id,  # Конический
                bore_diameter_mm=30,
                outer_diameter_mm=62,
                width_mm=17.25,
                width_inner_mm=17.25,
                width_outer_mm=14,
                dynamic_load_rating_kn=48.5,
                static_load_rating_kn=54.0,
                limiting_speed_rpm=6000,
                clearance="CN",
                weight_kg=0.32,
                price=2100,
                application="Колесные ступицы, редукторы"
            ),
        ]
        session.add_all(bearings)
        await session.flush()
        print(f"  ✅ Добавлено {len(bearings)} подшипников")
        
        await session.commit()
        print("\n" + "="*50)
        print("✅ БАЗА ДАННЫХ УСПЕШНО ЗАПОЛНЕНА!")
        print("="*50)
        print(f"📊 Итог:")
        print(f"  - Производителей: {len(manufacturers)}")
        print(f"  - Категорий: {len(categories)}")
        print(f"  - Продуктов: {len(products)}")
        print(f"  - Типов подшипников: {len(bearing_types)}")
        print(f"  - Производителей подшипников: {len(bearing_manufacturers)}")
        print(f"  - Серий подшипников: {len(bearing_series)}")
        print(f"  - Подшипников: {len(bearings)}")

if __name__ == "__main__":
    asyncio.run(seed_database())
