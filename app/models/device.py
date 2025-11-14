from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from ..db.database import Base

class Device(Base):
    __tablename__ = "Device"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    vehicle_id = Column(Integer, ForeignKey("Vehicle.id", ondelete="CASCADE"), nullable=True, unique=True)
    created_dt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    vehicle = relationship("Vehicle", back_populates="device")
