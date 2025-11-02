from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class VehicleBase(BaseModel):
    lic: str
    model: str
    year: int

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int
    created_dt: datetime
    updated_dt: datetime

    model_config = ConfigDict(from_attributes=True)