from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload
from typing import Optional, List, Dict, Any
from decimal import Decimal
import math

from models import (
    Bearing, BearingType, BearingManufacturer, 
    BearingSeries, BearingMotorCompatibility, Product
)
from schemas.bearing import (
    BearingCreate, BearingUpdate, BearingFilter,
    BearingTypeCreate, BearingManufacturerCreate,
    BearingSeriesCreate, BearingMotorCompatibilityCreate
)

class BearingService:
    """Сервис для работы с подшипниками"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # ============== Основные CRUD операции ==============
    
    async def get_bearings(self, filter_params: BearingFilter) -> List[Bearing]:
        """Получить список подшипников с фильтрацией"""
        query = select(Bearing).where(Bearing.is_active == True)
        
        # Текстовый поиск по номеру
        if filter_params.search:
            query = query.where(
                or_(
                    Bearing.bearing_number.ilike(f"%{filter_params.search}%"),
                    Bearing.alternative_numbers.ilike(f"%{filter_params.search}%")
                )
            )
        
        # Фильтры по связанным ID
        if filter_params.manufacturer_id:
            query = query.where(Bearing.manufacturer_id == filter_params.manufacturer_id)
        if filter_params.series_id:
            query = query.where(Bearing.series_id == filter_params.series_id)
        if filter_params.bearing_type_id:
            query = query.where(Bearing.bearing_type_id == filter_params.bearing_type_id)
        
        # Фильтры по размерам
        if filter_params.bore_diameter_min is not None:
            query = query.where(Bearing.bore_diameter_mm >= filter_params.bore_diameter_min)
        if filter_params.bore_diameter_max is not None:
            query = query.where(Bearing.bore_diameter_mm <= filter_params.bore_diameter_max)
        
        if filter_params.outer_diameter_min is not None:
            query = query.where(Bearing.outer_diameter_mm >= filter_params.outer_diameter_min)
        if filter_params.outer_diameter_max is not None:
            query = query.where(Bearing.outer_diameter_mm <= filter_params.outer_diameter_max)
        
        if filter_params.width_min is not None:
            query = query.where(Bearing.width_mm >= filter_params.width_min)
        if filter_params.width_max is not None:
            query = query.where(Bearing.width_mm <= filter_params.width_max)
        
        # Фильтры по характеристикам
        if filter_params.seal_type:
            query = query.where(Bearing.seal_type == filter_params.seal_type)
        if filter_params.clearance:
            query = query.where(Bearing.clearance == filter_params.clearance)
        if filter_params.material_type:
            query = query.where(Bearing.material_type == filter_params.material_type)
        
        # Загружаем связанные данные
        query = query.options(
            selectinload(Bearing.manufacturer),
            selectinload(Bearing.series),
            selectinload(Bearing.bearing_type)
        )
        
        # Пагинация
        query = query.offset(filter_params.skip).limit(filter_params.limit)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_bearing_by_id(self, bearing_id: int) -> Optional[Bearing]:
        """Получить подшипник по ID"""
        query = select(Bearing).where(
            Bearing.id == bearing_id,
            Bearing.is_active == True
        ).options(
            selectinload(Bearing.manufacturer),
            selectinload(Bearing.series),
            selectinload(Bearing.bearing_type)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_bearing_by_number(self, bearing_number: str) -> Optional[Bearing]:
        """Получить подшипник по номеру"""
        query = select(Bearing).where(
            Bearing.bearing_number == bearing_number,
            Bearing.is_active == True
        ).options(
            selectinload(Bearing.manufacturer),
            selectinload(Bearing.series),
            selectinload(Bearing.bearing_type)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def create_bearing(self, bearing_data: BearingCreate) -> Bearing:
        """Создать новый подшипник"""
        bearing = Bearing(**bearing_data.model_dump())
        self.db.add(bearing)
        await self.db.commit()
        await self.db.refresh(bearing)
        return bearing
    
    async def update_bearing(
        self, 
        bearing_id: int, 
        bearing_data: BearingUpdate
    ) -> Optional[Bearing]:
        """Обновить подшипник"""
        bearing = await self.get_bearing_by_id(bearing_id)
        if not bearing:
            return None
        
        # Обновляем только переданные поля
        for field, value in bearing_data.model_dump(exclude_unset=True).items():
            setattr(bearing, field, value)
        
        bearing.updated_at = func.now()
        await self.db.commit()
        await self.db.refresh(bearing)
        return bearing
    
    async def delete_bearing(self, bearing_id: int) -> bool:
        """Мягкое удаление подшипника"""
        bearing = await self.get_bearing_by_id(bearing_id)
        if not bearing:
            return False
        
        bearing.is_active = False
        bearing.updated_at = func.now()
        await self.db.commit()
        return True
    
    # ============== Специализированные методы подбора ==============
    
    async def find_bearings_by_shaft_diameter(
        self, 
        shaft_diameter_mm: Decimal,
        tolerance_mm: Decimal = Decimal('0.1'),
        limit: int = 20
    ) -> List[Bearing]:
        """
        Найти подшипники по диаметру вала
        Ищет подшипники с внутренним диаметром в пределах допуска
        """
        query = select(Bearing).where(
            and_(
                Bearing.bore_diameter_mm >= shaft_diameter_mm - tolerance_mm,
                Bearing.bore_diameter_mm <= shaft_diameter_mm + tolerance_mm,
                Bearing.is_active == True
            )
        ).order_by(
            # Сортируем по близости к нужному диаметру
            func.abs(Bearing.bore_diameter_mm - shaft_diameter_mm)
        ).limit(limit)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def find_bearings_by_dimensions(
        self,
        bore_diameter_mm: Optional[Decimal] = None,
        outer_diameter_mm: Optional[Decimal] = None,
        width_mm: Optional[Decimal] = None,
        tolerance_mm: Decimal = Decimal('0.5')
    ) -> List[Bearing]:
        """
        Найти подшипники по точным размерам
        """
        conditions = [Bearing.is_active == True]
        
        if bore_diameter_mm is not None:
            conditions.append(
                and_(
                    Bearing.bore_diameter_mm >= bore_diameter_mm - tolerance_mm,
                    Bearing.bore_diameter_mm <= bore_diameter_mm + tolerance_mm
                )
            )
        
        if outer_diameter_mm is not None:
            conditions.append(
                and_(
                    Bearing.outer_diameter_mm >= outer_diameter_mm - tolerance_mm,
                    Bearing.outer_diameter_mm <= outer_diameter_mm + tolerance_mm
                )
            )
        
        if width_mm is not None:
            conditions.append(
                and_(
                    Bearing.width_mm >= width_mm - tolerance_mm,
                    Bearing.width_mm <= width_mm + tolerance_mm
                )
            )
        
        query = select(Bearing).where(and_(*conditions))
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def find_bearings_for_motor(
        self,
        motor_id: int,
        position: Optional[str] = None
    ) -> List[Bearing]:
        """
        Найти подшипники, совместимые с конкретным двигателем
        """
        query = select(Bearing).join(
            BearingMotorCompatibility,
            Bearing.id == BearingMotorCompatibility.bearing_id
        ).where(
            BearingMotorCompatibility.motor_id == motor_id,
            Bearing.is_active == True
        )
        
        if position:
            query = query.where(BearingMotorCompatibility.position == position)
        
        query = query.options(
            selectinload(Bearing.manufacturer),
            selectinload(Bearing.series),
            selectinload(Bearing.bearing_type)
        )
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def calculate_life_hours(
        self,
        bearing_id: int,
        radial_load_kn: Decimal,
        speed_rpm: int,
        reliability: float = 90
    ) -> Dict[str, Any]:
        """
        Расчет ресурса подшипника в часах (по ISO 281)
        L10h = (10^6 / (60 * n)) * (C / P)^p
        
        где:
        L10h - номинальный ресурс в часах
        n - частота вращения (об/мин)
        C - динамическая грузоподъемность (кН)
        P - эквивалентная динамическая нагрузка (кН)
        p = 3 для шариковых подшипников, 10/3 для роликовых
        """
        bearing = await self.get_bearing_by_id(bearing_id)
        if not bearing:
            return {"error": "Bearing not found"}
        
        if not bearing.dynamic_load_rating_kn or bearing.dynamic_load_rating_kn <= 0:
            return {"error": "Dynamic load rating not available"}
        
        # Определяем показатель степени
        if bearing.bearing_type:
            if "шариков" in bearing.bearing_type.name.lower():
                p = 3
            else:
                p = 10/3
        else:
            p = 3  # по умолчанию
        
        # Рассчитываем ресурс в миллионах оборотов
        C = float(bearing.dynamic_load_rating_kn)
        P = float(radial_load_kn)
        
        if P <= 0:
            return {"error": "Load must be positive"}
        
        L10 = (C / P) ** p
        
        # Переводим в часы
        if speed_rpm > 0:
            L10h = (10**6 / (60 * speed_rpm)) * L10
        else:
            L10h = 0
        
        # Поправочный коэффициент на надежность
        reliability_factors = {
            90: 1.0,
            95: 0.62,
            96: 0.53,
            97: 0.44,
            98: 0.33,
            99: 0.21
        }
        
        a1 = reliability_factors.get(reliability, 1.0)
        L10h_adjusted = L10h * a1
        
        return {
            "bearing_number": bearing.bearing_number,
            "dynamic_load_rating_kn": C,
            "applied_load_kn": P,
            "speed_rpm": speed_rpm,
            "reliability": reliability,
            "life_millions_revolutions": round(L10, 2),
            "life_hours": round(L10h, 0),
            "life_hours_adjusted": round(L10h_adjusted, 0),
            "formula_used": f"L10 = (C/P)^{p:.3f}"
        }
    
    async def get_compatible_motors(
        self,
        bearing_id: int
    ) -> List[Product]:
        """
        Получить список двигателей, совместимых с подшипником
        """
        query = select(Product).join(
            BearingMotorCompatibility,
            Product.id == BearingMotorCompatibility.motor_id
        ).where(
            BearingMotorCompatibility.bearing_id == bearing_id,
            Product.is_active == True
        )
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    # ============== Методы для справочников ==============
    
    async def get_bearing_types(self) -> List[BearingType]:
        """Получить все типы подшипников"""
        result = await self.db.execute(select(BearingType))
        return result.scalars().all()
    
    async def create_bearing_type(self, type_data: BearingTypeCreate) -> BearingType:
        """Создать новый тип подшипника"""
        bearing_type = BearingType(**type_data.model_dump())
        self.db.add(bearing_type)
        await self.db.commit()
        await self.db.refresh(bearing_type)
        return bearing_type
    
    async def get_bearing_manufacturers(self) -> List[BearingManufacturer]:
        """Получить всех производителей подшипников"""
        result = await self.db.execute(select(BearingManufacturer))
        return result.scalars().all()
    
    async def create_bearing_manufacturer(
        self, 
        manufacturer_data: BearingManufacturerCreate
    ) -> BearingManufacturer:
        """Создать нового производителя"""
        manufacturer = BearingManufacturer(**manufacturer_data.model_dump())
        self.db.add(manufacturer)
        await self.db.commit()
        await self.db.refresh(manufacturer)
        return manufacturer
    
    async def get_bearing_series(
        self, 
        bearing_type_id: Optional[int] = None
    ) -> List[BearingSeries]:
        """Получить серии подшипников (опционально по типу)"""
        query = select(BearingSeries)
        if bearing_type_id:
            query = query.where(BearingSeries.bearing_type_id == bearing_type_id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def create_bearing_series(self, series_data: BearingSeriesCreate) -> BearingSeries:
        """Создать новую серию подшипников"""
        series = BearingSeries(**series_data.model_dump())
        self.db.add(series)
        await self.db.commit()
        await self.db.refresh(series)
        return series
    
    # ============== Методы для совместимости ==============
    
    async def add_compatibility(
        self,
        compat_data: BearingMotorCompatibilityCreate
    ) -> BearingMotorCompatibility:
        """Добавить запись о совместимости подшипника с двигателем"""
        compat = BearingMotorCompatibility(**compat_data.model_dump())
        self.db.add(compat)
        await self.db.commit()
        await self.db.refresh(compat)
        return compat
    
    async def remove_compatibility(
        self,
        bearing_id: int,
        motor_id: int,
        position: Optional[str] = None
    ) -> bool:
        """Удалить запись о совместимости"""
        query = select(BearingMotorCompatibility).where(
            BearingMotorCompatibility.bearing_id == bearing_id,
            BearingMotorCompatibility.motor_id == motor_id
        )
        if position:
            query = query.where(BearingMotorCompatibility.position == position)
        
        result = await self.db.execute(query)
        compat = result.scalar_one_or_none()
        
        if compat:
            await self.db.delete(compat)
            await self.db.commit()
            return True
        return False
    
    # ============== Статистика ==============
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Получить статистику по подшипникам"""
        # Общее количество активных подшипников
        total = await self.db.execute(
            select(func.count(Bearing.id)).where(Bearing.is_active == True)
        )
        total_count = total.scalar()
        
        # Количество производителей
        manufacturers = await self.db.execute(
            select(func.count(BearingManufacturer.id))
        )
        manufacturers_count = manufacturers.scalar()
        
        # Количество типов
        types = await self.db.execute(
            select(func.count(BearingType.id))
        )
        types_count = types.scalar()
        
        # Диапазон размеров
        min_bore = await self.db.execute(
            select(func.min(Bearing.bore_diameter_mm)).where(Bearing.is_active == True)
        )
        max_bore = await self.db.execute(
            select(func.max(Bearing.bore_diameter_mm)).where(Bearing.is_active == True)
        )
        
        return {
            "total_bearings": total_count,
            "total_manufacturers": manufacturers_count,
            "total_types": types_count,
            "bore_diameter_range": {
                "min": float(min_bore.scalar() or 0),
                "max": float(max_bore.scalar() or 0)
            }
        }
