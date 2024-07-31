from fastapi import FastAPI
from src.routes.route import router

app = FastAPI()


app.include_router(router=router)
