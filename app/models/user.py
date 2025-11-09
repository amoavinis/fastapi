from sqlalchemy import Column, String, BigInteger, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from ..db.database import Base

class User(Base):
    __tablename__ = "User"
    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, server_default='false')
    created_dt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
