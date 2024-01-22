from fastapi import FastAPI

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api_v1 import router as router_v1

app = FastAPI(title="Restaurant Menu")


app.include_router(router=router_v1, prefix='/api/v1')
