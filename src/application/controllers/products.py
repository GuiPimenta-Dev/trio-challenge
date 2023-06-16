from fastapi import APIRouter

from src.application.usecases.view_menu import ViewMenu

from . import Config

router = APIRouter()


@router.get("/menu")
async def view_menu():
    view_menu = ViewMenu(Config.products_repository)
    menu = view_menu.execute()

    return {"data": menu}