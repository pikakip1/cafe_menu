from fastapi import APIRouter
from api_v1.menu.router import router as menu_router

router = APIRouter()
router.include_router(router=menu_router, prefix='/menus')
