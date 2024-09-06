from fastapi import FastAPI
from src.routes.route import router
from CustomMiddleware.middleware import CustomMiddleWare
from chat_service.routes import router as chat_router

app = FastAPI()

app.add_middleware(CustomMiddleWare)

app.include_router(router=router)
app.include_router(chat_router)