from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from decimal import Decimal

from database.connection import get_db
from services.bearing_service import BearingService
from schemas.bearing import (
    Bearing, BearingCreate, BearingUpdate, BearingWithRelations, BearingFilter,
    BearingType, BearingTypeCreate,
    BearingManufacturer, BearingManufacturerCreate,
    BearingSeries, BearingSeriesCreate,
    BearingMotorCompatibility, BearingMotorCompatibilityCreate
)

router = APIRouter(prefix="/bearings", tags=["bearings"])


# ============== Основные эндпоинты для подшипников ==============

@router.get("/", response_model=List[BearingWithRelations])
async def get_bearings(
    search: Optional[str] = Query(None, description="Поиск по номеру подшипника"),
    manufacturer_id: Optional[int] = Query(None, description="ID производителя"),
    series_id: Optional[int] = Query(None, description="ID серии"),
    bearing_type_id: Optional[int] = Query(None, description="ID типа подшипника"),
    
    bore_diameter_min: Optional[Decimal] = Query(None, ge=0, description="Мин. внутренний диаметр (мм)"),
    bore_diameter_max: Optional[Decimal] = Query(None, ge=0, description="Макс. внутренний диаметр (мм)"),
    outer_diameter_min: Optional[Decimal] = Query(None, ge=0, description="Мин. наружный диаметр (мм)"),
    outer_diameter_max: Optional[Decimal] = Query(None, ge=0, description="Макс. наружный диаметр (мм)"),
    width_min: Optional[Decimal] = Query(None, ge=0, description="Мин. ширина (мм)"),
    width_max: Optional[Decimal] = Query(None, ge=0, description="Макс. ширина (мм)"),
    
    seal_type: Optional[str] = Query(None, description="Тип уплотнения (OPEN, 2Z, 2RS)"),
    clearance: Optional[str] = Query(None, description="Зазор (CN, C3, C4)"),
    
    skip: int = Query(0, ge=0, description="Пропустить записей"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    db: AsyncSession = Depends(get_db)
):
    """Получить список подшипников с фильтрацией"""
    filter_params = BearingFilter(
        search=search,
        manufacturer_id=manufacturer_id,
        series_id=series_id,
        bearing_type_id=bearing_type_id,
        bore_diameter_min=bore_diameter_min,
        bore_diameter_max=bore_diameter_max,
        outer_diameter_min=outer_diameter_min,
        outer_diameter_max=outer_diameter_max,
        width_min=width_min,
        width_max=width_max,
        seal_type=seal_type,
        clearance=clearance,
        skip=skip,
        limit=limit
    )
    
    service = BearingService(db)
    bearings = await service.get_bearings(filter_params)
    return bearings


@router.get("/search", response_model=List[Bearing])
async def search_bearings(
    q: str = Query(..., min_length=2, description="Поисковый запрос (номер подшипника)"),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Быстрый поиск подшипников по номеру"""
    filter_params = BearingFilter(search=q, limit=limit)
    service = BearingService(db)
    bearings = await service.get_bearings(filter_params)
    return bearings


@router.get("/by-shaft/{shaft_diameter}", response_model=List[Bearing])
async def find_bearings_by_shaft(
    shaft_diameter: float = Path(..., description="Диаметр вала в мм"),
    tolerance: float = Query(0.1, ge=0.01, le=1.0, description="Допуск в мм"),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Найти подшипники по диаметру вала"""
    service = BearingService(db)
    bearings = await service.find_bearings_by_shaft_diameter(
        shaft_diameter_mm=Decimal(str(shaft_diameter)),
        tolerance_mm=Decimal(str(tolerance)),
        limit=limit
    )
    return bearings


@router.get("/by-dimensions", response_model=List[Bearing])
async def find_bearings_by_dimensions(
    bore_diameter: Optional[float] = Query(None, description="Внутренний диаметр (мм)"),
    outer_diameter: Optional[float] = Query(None, description="Наружный диаметр (мм)"),
    width: Optional[float] = Query(None, description="Ширина (мм)"),
    tolerance: float = Query(0.5, ge=0.1, le=2.0, description="Допуск в мм"),
    db: AsyncSession = Depends(get_db)
):
    """Найти подшипники по точным размерам"""
    service = BearingService(db)
    bearings = await service.find_bearings_by_dimensions(
        bore_diameter_mm=Decimal(str(bore_diameter)) if bore_diameter else None,
        outer_diameter_mm=Decimal(str(outer_diameter)) if outer_diameter else None,
        width_mm=Decimal(str(width)) if width else None,
        tolerance_mm=Decimal(str(tolerance))
    )
    return bearings


@router.get("/for-motor/{motor_id}", response_model=List[Bearing])
async def get_bearings_for_motor(
    motor_id: int = Path(..., description="ID двигателя"),
    position: Optional[str] = Query(None, description="Позиция (DE, NDE)"),
    db: AsyncSession = Depends(get_db)
):
    """Получить подшипники, совместимые с двигателем"""
    service = BearingService(db)
    bearings = await service.find_bearings_for_motor(motor_id, position)
    return bearings


@router.get("/{bearing_id}", response_model=BearingWithRelations)
async def get_bearing(
    bearing_id: int = Path(..., description="ID подшипника"),
    db: AsyncSession = Depends(get_db)
):
    """Получить подшипник по ID"""
    service = BearingService(db)
    bearing = await service.get_bearing_by_id(bearing_id)
    
    if not bearing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Подшипник не найден"
        )
    
    # Добавляем дополнительные поля для ответа
    response = BearingWithRelations.model_validate(bearing)
    if bearing.manufacturer:
        response.manufacturer_name = bearing.manufacturer.name
    if bearing.series:
        response.series_code = bearing.series.series_code
    if bearing.bearing_type:
        response.type_name = bearing.bearing_type.name
    
    return response


@router.get("/by-number/{bearing_number}", response_model=Bearing)
async def get_bearing_by_number(
    bearing_number: str = Path(..., description="Номер подшипника (например, 6204-2Z)"),
    db: AsyncSession = Depends(get_db)
):
    """Получить подшипник по номеру"""
    service = BearingService(db)
    bearing = await service.get_bearing_by_number(bearing_number)
    
    if not bearing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Подшипник не найден"
        )
    
    return bearing


@router.post("/", response_model=Bearing, status_code=status.HTTP_201_CREATED)
async def create_bearing(
    bearing_data: BearingCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создать новый подшипник"""
    service = BearingService(db)
    
    # Проверяем уникальность номера
    existing = await service.get_bearing_by_number(bearing_data.bearing_number)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Подшипник с таким номером уже существует"
        )
    
    bearing = await service.create_bearing(bearing_data)
    return bearing


@router.put("/{bearing_id}", response_model=Bearing)
async def update_bearing(
    bearing_id: int = Path(..., description="ID подшипника"),
    bearing_data: BearingUpdate = None,  # Исправлено: сначала Path, потом Query
    db: AsyncSession = Depends(get_db)
):
    """Обновить подшипник"""
    if bearing_data is None:
        bearing_data = BearingUpdate()
    
    service = BearingService(db)
    
    # Проверяем существование
    existing = await service.get_bearing_by_id(bearing_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Подшипник не найден"
        )
    
    bearing = await service.update_bearing(bearing_id, bearing_data)
    return bearing


@router.delete("/{bearing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bearing(
    bearing_id: int = Path(..., description="ID подшипника"),
    db: AsyncSession = Depends(get_db)
):
    """Удалить подшипник (мягкое удаление)"""
    service = BearingService(db)
    deleted = await service.delete_bearing(bearing_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Подшипник не найден"
        )
    
    return None


@router.get("/{bearing_id}/compatible-motors", response_model=List[dict])
async def get_compatible_motors(
    bearing_id: int = Path(..., description="ID подшипника"),
    db: AsyncSession = Depends(get_db)
):
    """Получить список двигателей, совместимых с подшипником"""
    service = BearingService(db)
    motors = await service.get_compatible_motors(bearing_id)
    
    return [
        {
            "id": motor.id,
            "product_code": motor.product_code,
            "name": motor.name,
            "manufacturer": motor.manufacturer.name if motor.manufacturer else None
        }
        for motor in motors
    ]


@router.get("/{bearing_id}/life-calculation", response_model=dict)
async def calculate_bearing_life(
    bearing_id: int = Path(..., description="ID подшипника"),
    radial_load: float = Query(..., description="Радиальная нагрузка (кН)"),
    speed: int = Query(..., description="Частота вращения (об/мин)"),
    reliability: float = Query(90, ge=90, le=99, description="Надежность (%)"),
    db: AsyncSession = Depends(get_db)
):
    """Рассчитать ресурс подшипника в часах"""
    service = BearingService(db)
    result = await service.calculate_life_hours(
        bearing_id=bearing_id,
        radial_load_kn=Decimal(str(radial_load)),
        speed_rpm=speed,
        reliability=reliability
    )
    
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return result


# ============== Эндпоинты для типов подшипников ==============

@router.get("/types/all", response_model=List[BearingType])
async def get_bearing_types(
    db: AsyncSession = Depends(get_db)
):
    """Получить все типы подшипников"""
    service = BearingService(db)
    types = await service.get_bearing_types()
    return types


@router.post("/types", response_model=BearingType, status_code=status.HTTP_201_CREATED)
async def create_bearing_type(
    type_data: BearingTypeCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создать новый тип подшипника"""
    service = BearingService(db)
    bearing_type = await service.create_bearing_type(type_data)
    return bearing_type


# ============== Эндпоинты для производителей ==============

@router.get("/manufacturers/all", response_model=List[BearingManufacturer])
async def get_bearing_manufacturers(
    db: AsyncSession = Depends(get_db)
):
    """Получить всех производителей подшипников"""
    service = BearingService(db)
    manufacturers = await service.get_bearing_manufacturers()
    return manufacturers


@router.post("/manufacturers", response_model=BearingManufacturer, status_code=status.HTTP_201_CREATED)
async def create_bearing_manufacturer(
    manufacturer_data: BearingManufacturerCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создать нового производителя подшипников"""
    service = BearingService(db)
    manufacturer = await service.create_bearing_manufacturer(manufacturer_data)
    return manufacturer


# ============== Эндпоинты для серий ==============

@router.get("/series/all", response_model=List[BearingSeries])
async def get_bearing_series(
    bearing_type_id: Optional[int] = Query(None, description="Фильтр по типу подшипника"),
    db: AsyncSession = Depends(get_db)
):
    """Получить все серии подшипников"""
    service = BearingService(db)
    series = await service.get_bearing_series(bearing_type_id)
    return series


@router.post("/series", response_model=BearingSeries, status_code=status.HTTP_201_CREATED)
async def create_bearing_series(
    series_data: BearingSeriesCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создать новую серию подшипников"""
    service = BearingService(db)
    series = await service.create_bearing_series(series_data)
    return series


# ============== Эндпоинты для совместимости ==============

@router.post("/compatibility", response_model=BearingMotorCompatibility)
async def add_compatibility(
    compat_data: BearingMotorCompatibilityCreate,
    db: AsyncSession = Depends(get_db)
):
    """Добавить запись о совместимости подшипника с двигателем"""
    service = BearingService(db)
    compat = await service.add_compatibility(compat_data)
    return compat


@router.delete("/compatibility/{bearing_id}/{motor_id}")
async def remove_compatibility(
    bearing_id: int = Path(..., description="ID подшипника"),
    motor_id: int = Path(..., description="ID двигателя"),
    position: Optional[str] = Query(None, description="Позиция (DE, NDE)"),
    db: AsyncSession = Depends(get_db)
):
    """Удалить запись о совместимости"""
    service = BearingService(db)
    removed = await service.remove_compatibility(bearing_id, motor_id, position)
    
    if not removed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись о совместимости не найдена"
        )
    
    return {"message": "Совместимость удалена"}


# ============== Статистика ==============

@router.get("/stats/overview", response_model=dict)
async def get_bearing_statistics(
    db: AsyncSession = Depends(get_db)
):
    """Получить статистику по подшипникам"""
    service = BearingService(db)
    stats = await service.get_statistics()
    return stats
