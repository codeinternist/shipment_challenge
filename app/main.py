from fastapi import FastAPI

from controllers import items, shipment

app = FastAPI()

app.include_router(
    shipment.router,
    tags=["shipment"]
)

app.include_router(
    items.router,
    tags=["items"]
)