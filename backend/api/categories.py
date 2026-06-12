from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from database.connection import get_db
from models import Category
from schemas.category import Category, CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[Category])
async def get_categories(
    skip: int = Query(0, ge=0, description="Пропустить записей"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    category_type: Optional[str] = Query(None, description="Тип категории (motor, bearing, cylinder)"),
    db: AsyncSession = Depends(get_db)
):
    """Получить список категорий"""
    query = select(Category)
    if category_type:
        query = query.where(Category.category_type == category_type)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    categories = result.scalars().all()
    return categories

@router.get("/{category_id}", response_model=Category)
async def get_category(
    category_id: int = Path(..., description="ID категории"),
    db: AsyncSession = Depends(get_db)
):
    """Получить категорию по ID"""
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )
    return category

@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создать новую категорию"""
    db_category = Category(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

@router.put("/{category_id}", response_model=Category)
async def update_category(
    category_id: int = Path(..., description="ID категории"),
    category_update: CategoryUpdate = None,
    db: AsyncSession = Depends(get_db)
):
    """Обновить категорию"""
    if category_update is None:
        category_update = CategoryUpdate()
    
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )
    
    for field, value in category_update.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    
    await db.commit()
    await db.refresh(category)
    return category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int = Path(..., description="ID категории"),
    db: AsyncSession = Depends(get_db)
):
    """Удалить категорию"""
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )
    
    await db.delete(category)
    await db.commit()
    return None
