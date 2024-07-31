from fastapi import APIRouter

from src.api.v1.routes import routes

# Add route with prefix /api/v1 to manage v1 APIs.
router = APIRouter(prefix="/api")

# all v1 routes
router.include_router(routes.router)