from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class VehicleBase(BaseModel):
    lic: str
    model: str
    year: int

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    lic: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None

class VehicleStatusUpdate(BaseModel):
    status: bool

class VehiclePositionUpdate(BaseModel):
    latitude: float
    longitude: float

class Vehicle(VehicleBase):
    id: int
    status: Optional[bool] = None
    last_latitude: Optional[float] = None
    last_longitude: Optional[float] = None
    position_updated_dt: Optional[datetime] = None
    created_dt: datetime
    updated_dt: datetime

    model_config = ConfigDict(from_attributes=True)

class VehicleWithDevice(Vehicle):
    device: Optional["DeviceResponse"] = None

    model_config = ConfigDict(from_attributes=True)

# Import at the end to avoid circular import
from .device import Device as DeviceResponse