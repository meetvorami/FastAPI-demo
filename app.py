from fastapi import FastAPI
from src.routes.route import router
from CustomMiddleware.middleware import CustomMiddleWare

app = FastAPI()

app.add_middleware(CustomMiddleWare)

app.include_router(router=router)
