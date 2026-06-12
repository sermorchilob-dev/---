from .products import router as products_router
from .manufacturers import router as manufacturers_router
from .bearings import router as bearings_router
from .categories import router as categories_router

__all__ = [
    'products_router',
    'manufacturers_router',
    'bearings_router',
    'categories_router'
]
from .bearing_units import router as bearing_units_router
from .gearboxes import router as gearboxes_router

__all__.append('gearboxes_router')
