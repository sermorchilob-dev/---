from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.connection import engine, Base, init_db

# Импортируем роутеры
from api import (
    products_router,
    manufacturers_router,
    bearings_router,
    bearing_units_router,
    gearboxes_router,
)

app = FastAPI(
    title="Motor Selector MVP",
    description="API для конфигуратора приводной техники",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем все роутеры
app.include_router(products_router)
app.include_router(manufacturers_router)
app.include_router(bearings_router)
app.include_router(bearing_units_router)
app.include_router(gearboxes_router)

@app.on_event("startup")
async def startup_event():
    # Инициализация базы данных при запуске
    await init_db()
    print("🚀 Сервер запущен и готов к работе")
    print("📚 Документация: /docs")
    print("📌 Доступные роутеры: /products, /manufacturers, /bearings, /bearing-units, /gearboxes")

@app.get("/")
async def root():
    return {
        "message": "Motor Selector API is running",
        "status": "ok",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "products": "/products",
            "manufacturers": "/manufacturers",
            "bearings": "/bearings",
            "bearing-units": "/bearing-units",
            "gearboxes": "/gearboxes"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "database": "connected"
    }