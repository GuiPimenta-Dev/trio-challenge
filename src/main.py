from fastapi import FastAPI

from src.application.controllers import order, products

app = FastAPI()

app.include_router(order.router)
app.include_router(products.router)
