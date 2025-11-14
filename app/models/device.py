from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from ..db.database import Base

class Device(Base):
    __tablename__ = "Device"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    vehicle_id = Column(Integer, ForeignKey("Vehicle.id", ondelete="CASCADE"), nullable=True, unique=True)
    status = Column(Boolean, nullable=True, server_default='false')  # on/off status
    last_latitude = Column(Float, nullable=True)  # last known latitude
    last_longitude = Column(Float, nullable=True)  # last known longitude
    position_updated_dt = Column(TIMESTAMP(timezone=True), nullable=True)  # last position update time
    created_dt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    vehicle = relationship("Vehicle", back_populates="device")
