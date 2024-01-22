from fastapi import FastAPI
from src.menu.router import router


app = FastAPI(title="Restaurant Menu")


app.include_router(router)
