from fastapi import APIRouter, HTTPException
from models import models
from uuid import UUID

router = APIRouter()

@router.get("/")
async def list_shipments():
    return {"list": "shipments"}

@router.get("/{shipment_id}", response_model=models.Shipment, status_code=200)
async def get_shipment(shipment_id: UUID):
    return {"get": "shipment", "shipment_id": shipment_id}

@router.post("/")
async def create_shipment(data):
    return {"create": "shipment", "data": data}

@router.put("/{shipment_id}")
async def update_shipment(shipment_id: UUID, data):
    return {"update": "shipment", "shipment_id": shipment_id, "data": data}        

@router.delete("/{shipment_id}")
async def delete_shipment(shipment_id: UUID):
    return {"delete": "shipment", "shipment_id": shipment_id}