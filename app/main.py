import logging as log
from fastapi import FastAPI

from controllers import items, shipment
from services import db

log.basicConfig(level=log.DEBUG)

app = FastAPI()

app.include_router(
    shipment.router,
    tags=["shipment"]
)

app.include_router(
    items.router,
    tags=["items"]
)

if __name__ == '__main__':
    import uvicorn
    log.info("starting server...")
    uvicorn.run(app)