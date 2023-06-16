from fastapi import APIRouter, Header, Request

from src.application.usecases.cancel_order import CancelOrder
from src.application.usecases.change_order_status import ChangeOrderStatus
from src.application.usecases.place_order import PlaceOrder
from src.application.usecases.update_order import UpdateOrder
from src.application.usecases.view_order_details import ViewOrderDetails

from . import Config

router = APIRouter()


@router.post("/orders")
async def place_order(request: Request):
    body = await request.json()
    customer_id = body.get("customer_id")
    products = body.get("products")
    location = body.get("location")

    place_order = PlaceOrder(Config.__dict__)
    order = {"customer_id": customer_id, "products": products, "location": location}
    place_order.execute(order)


@router.get("/orders")
async def list_orders():
    view_order_details = ViewOrderDetails(Config.orders_repository)
    orders = view_order_details.execute()

    return {"data": orders}


@router.put("/orders/{order_id}")
async def update_order(order_id: str, request: Request):
    body = await request.json()
    customer_id = body.get("customer_id")
    products = body.get("products")
    location = body.get("location")

    update_order = UpdateOrder(Config.__dict__)
    order = {
        "order_id": order_id,
        "customer_id": customer_id,
        "products": products,
        "location": location,
    }
    update_order.execute(order)


@router.delete("/orders/{order_id}")
async def cancel_order(order_id: str):
    cancel_order = CancelOrder(Config.orders_repository)
    cancel_order.execute(order_id)


@router.post("/manager/orders/{order_id}")
async def manager_order(
    order_id: str,
    manager_id: str = Header(None, convert_underscores=False, case_sensitive=False),
):
    change_order_status = ChangeOrderStatus(
        Config.managers_repository, Config.orders_repository, Config.broker
    )
    change_order_status.execute({"manager_id": manager_id, "order_id": order_id})
