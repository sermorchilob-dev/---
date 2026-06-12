from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import List, Optional
from decimal import Decimal

from database.connection import get_db
from models.product import Product as ProductModel
from models import Manufacturer, Category
from schemas.product import Product as ProductSchema, ProductCreate, ProductUpdate, ProductWithRelations

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductSchema])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    manufacturer_id: Optional[int] = None,
    category_id: Optional[int] = None,
    power_min: Optional[float] = Query(None, ge=0),
    power_max: Optional[float] = Query(None, ge=0),
    speed_min: Optional[int] = Query(None, ge=0),
    speed_max: Optional[int] = Query(None, ge=0),
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(ProductModel).where(ProductModel.is_active == True)

    if manufacturer_id:
        query = query.where(ProductModel.manufacturer_id == manufacturer_id)
    if category_id:
        query = query.where(ProductModel.category_id == category_id)
    if power_min is not None:
        query = query.where(ProductModel.power_kw >= power_min)
    if power_max is not None:
        query = query.where(ProductModel.power_kw <= power_max)
    if speed_min is not None:
        query = query.where(ProductModel.speed_rpm >= speed_min)
    if speed_max is not None:
        query = query.where(ProductModel.speed_rpm <= speed_max)
    if search:
        query = query.where(
            or_(
                ProductModel.name.ilike(f"%{search}%"),
                ProductModel.product_code.ilike(f"%{search}%")
            )
        )

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    products = result.scalars().all()
    return products

@router.get("/{product_id}", response_model=ProductWithRelations)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    response = ProductWithRelations.model_validate(product)
    if product.manufacturer:
        response.manufacturer_name = product.manufacturer.name
    if product.category:
        response.category_name = product.category.name

    return response

@router.post("/", response_model=ProductSchema, status_code=201)
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product
