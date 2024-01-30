from fastapi import FastAPI

from api_v1 import router as router_v1

app = FastAPI(title="Restaurant Menu")


app.include_router(router=router_v1, prefix='/api/v1')
