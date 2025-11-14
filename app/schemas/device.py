from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class DeviceBase(BaseModel):
    name: str
    vehicle_id: Optional[int] = None

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    vehicle_id: Optional[int] = None

class DeviceStatusUpdate(BaseModel):
    status: bool

class DevicePositionUpdate(BaseModel):
    latitude: float
    longitude: float

class Device(DeviceBase):
    id: int
    status: Optional[bool] = None
    last_latitude: Optional[float] = None
    last_longitude: Optional[float] = None
    position_updated_dt: Optional[datetime] = None
    created_dt: datetime

    model_config = ConfigDict(from_attributes=True)
