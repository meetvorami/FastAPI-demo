from fastapi import APIRouter

from src.api.v1.productManagement.views import product_views
from src.api.v1.UserManagement.views import views

router = APIRouter(prefix="/v1")

router.include_router(views.router)
router.include_router(product_views.product_router)
