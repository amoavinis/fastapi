from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from .. import models, schemas
from ..db.database import get_db
from ..utils.auth import get_current_user

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)

@router.get("/", response_model=List[schemas.Vehicle])
def get_vehicles(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    vehicles = db.query(models.Vehicle).all()

    return vehicles

@router.get("/{id}", response_model=schemas.Vehicle)
def get_vehicles(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == id).first()

    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle with id: {id} was not found.")

    return vehicle

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Vehicle)
def create_vehicle(
    vehicle: schemas.VehicleCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_vehicle = models.Vehicle(**vehicle.model_dump())
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)

    return new_vehicle

@router.put("/{id}", response_model=schemas.Vehicle)
def update_vehicle(
    id: int,
    updated_vehicle: schemas.VehicleCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Vehicle).filter(models.Vehicle.id == id)

    vehicle = query.first()

    if vehicle == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Vehicle with id: {id} was not found.")

    query.update(updated_vehicle.model_dump(), synchronize_session=False)
    db.commit()

    return query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Vehicle).filter(models.Vehicle.id == id)

    vehicle = query.first()

    if vehicle == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Vehicle with id: {id} was not found.")

    query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{id}/status", response_model=schemas.Vehicle)
def update_vehicle_status(
    id: int,
    status_update: schemas.VehicleStatusUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Vehicle).filter(models.Vehicle.id == id)

    vehicle = query.first()

    if vehicle == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Vehicle with id: {id} was not found.")

    query.update({"status": status_update.status}, synchronize_session=False)
    db.commit()

    return query.first()

@router.patch("/{id}/position", response_model=schemas.Vehicle)
def update_vehicle_position(
    id: int,
    position_update: schemas.VehiclePositionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Vehicle).filter(models.Vehicle.id == id)

    vehicle = query.first()

    if vehicle == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Vehicle with id: {id} was not found.")

    query.update({
        "last_latitude": position_update.latitude,
        "last_longitude": position_update.longitude,
        "position_updated_dt": datetime.now(timezone.utc)
    }, synchronize_session=False)
    db.commit()

    return query.first()

@router.get("/{id}/device", response_model=schemas.VehicleWithDevice)
def get_vehicle_with_device(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == id).first()

    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle with id: {id} was not found.")

    return vehicle
