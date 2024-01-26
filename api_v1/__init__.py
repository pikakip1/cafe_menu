from fastapi import APIRouter
from api_v1.menu.router import router as menu_router
from api_v1.sub_menu.router import router as sub_menu_router
from api_v1.dish.router import router as dish_router

router = APIRouter()
router.include_router(router=menu_router, prefix='/menus')
router.include_router(router=sub_menu_router, prefix='/menus')
router.include_router(router=dish_router, prefix='/menus')
