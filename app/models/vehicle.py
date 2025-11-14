from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from ..db.database import Base

class Vehicle(Base):
    __tablename__ = "Vehicle"
    id = Column(Integer, primary_key=True, nullable=False)
    lic = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=True, server_default='false')  # on/off status
    last_latitude = Column(Float, nullable=True)  # last known latitude
    last_longitude = Column(Float, nullable=True)  # last known longitude
    position_updated_dt = Column(TIMESTAMP(timezone=True), nullable=True)  # last position update time
    created_dt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_dt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    device = relationship("Device", back_populates="vehicle", uselist=False, cascade="all, delete-orphan")