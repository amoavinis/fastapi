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

class Device(DeviceBase):
    id: int
    created_dt: datetime

    model_config = ConfigDict(from_attributes=True)
