from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from .. import models, schemas
from ..db.database import get_db
from ..utils.auth import get_current_user
from ..utils.websocket import manager

router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)

@router.get("/", response_model=List[schemas.Device])
def get_devices(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    devices = db.query(models.Device).all()
    return devices

@router.get("/{id}", response_model=schemas.Device)
def get_device(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    device = db.query(models.Device).filter(models.Device.id == id).first()

    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Device with id: {id} was not found.")

    return device

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Device)
def create_device(
    device: schemas.DeviceCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Verify vehicle exists if vehicle_id is provided
    if device.vehicle_id is not None:
        vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == device.vehicle_id).first()
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle with id: {device.vehicle_id} was not found."
            )

        # Check if vehicle already has a device (1-to-1 relationship)
        existing_device = db.query(models.Device).filter(models.Device.vehicle_id == device.vehicle_id).first()
        if existing_device:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Vehicle with id: {device.vehicle_id} already has a device assigned."
            )

    new_device = models.Device(**device.model_dump())
    db.add(new_device)
    db.commit()
    db.refresh(new_device)

    return new_device

@router.put("/{id}", response_model=schemas.Device)
def update_device(
    id: int,
    updated_device: schemas.DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Device).filter(models.Device.id == id)

    device = query.first()

    if device == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Device with id: {id} was not found.")

    # Verify vehicle exists if vehicle_id is being updated
    update_data = updated_device.model_dump(exclude_unset=True)
    if "vehicle_id" in update_data and update_data["vehicle_id"] is not None:
        vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == update_data["vehicle_id"]).first()
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle with id: {update_data['vehicle_id']} was not found."
            )

        # Check if vehicle already has a different device (1-to-1 relationship)
        existing_device = db.query(models.Device).filter(
            models.Device.vehicle_id == update_data["vehicle_id"],
            models.Device.id != id
        ).first()
        if existing_device:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Vehicle with id: {update_data['vehicle_id']} already has a device assigned."
            )

    query.update(update_data, synchronize_session=False)
    db.commit()

    return query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Device).filter(models.Device.id == id)

    device = query.first()

    if device == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Device with id: {id} was not found.")

    query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{id}/status", response_model=schemas.Device)
async def update_device_status(
    id: int,
    status_update: schemas.DeviceStatusUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Device).filter(models.Device.id == id)

    device = query.first()

    if device == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Device with id: {id} was not found.")

    query.update({"status": status_update.status}, synchronize_session=False)
    db.commit()

    updated_device = query.first()

    # Broadcast status update via WebSocket (using vehicle_id if device is linked)
    if updated_device.vehicle_id:
        await manager.broadcast_vehicle_update(updated_device.vehicle_id, {
            "type": "status_update",
            "device_id": id,
            "vehicle_id": updated_device.vehicle_id,
            "status": status_update.status,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    return updated_device

@router.patch("/{id}/position", response_model=schemas.Device)
async def update_device_position(
    id: int,
    position_update: schemas.DevicePositionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Device).filter(models.Device.id == id)

    device = query.first()

    if device == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Device with id: {id} was not found.")

    position_updated_time = datetime.now(timezone.utc)

    query.update({
        "last_latitude": position_update.latitude,
        "last_longitude": position_update.longitude,
        "position_updated_dt": position_updated_time
    }, synchronize_session=False)
    db.commit()

    updated_device = query.first()

    # Broadcast position update via WebSocket (using vehicle_id if device is linked)
    if updated_device.vehicle_id:
        await manager.broadcast_vehicle_update(updated_device.vehicle_id, {
            "type": "position_update",
            "device_id": id,
            "vehicle_id": updated_device.vehicle_id,
            "latitude": position_update.latitude,
            "longitude": position_update.longitude,
            "position_updated_dt": position_updated_time.isoformat(),
            "timestamp": position_updated_time.isoformat()
        })

    return updated_device
