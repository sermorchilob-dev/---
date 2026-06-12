from .products import router as products_router
from .manufacturers import router as manufacturers_router

__all__ = ['products_router', 'manufacturers_router']
from .bearing_units import router as bearing_units_router

__all__.append('bearing_units_router')
