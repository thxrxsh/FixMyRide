from sqlalchemy import Column, Integer, String, Float, Boolean, Time, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

try:
    from database import Base
except ImportError:
    from .database import Base


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    mobile = Column(Integer, nullable=False)

class Mechanic(Base):
    __tablename__ = "mechanic"
    mechanic_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=False)
    location = Column(String, nullable=False)
    district = Column(String, nullable=False)
    province = Column(String, nullable=False)
    country = Column(String, nullable=False)
    mobile = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    rating_count = Column(Float, nullable=True)
    rating_total = Column(Float, nullable=True)

class Service(Base):
    __tablename__ = "service"
    service_id = Column(Integer, primary_key=True, nullable=False)
    vehicle_type = Column(String, nullable=False)
    model = Column(String, nullable=False)
    service = Column(String, nullable=False)
    price = Column(Float, nullable=True)
    rating_count = Column(Float, nullable=True)
    rating_total = Column(Float, nullable=True)
    mechanic_id = Column(Integer, ForeignKey("mechanic.mechanic_id", ondelete="CASCADE"), nullable=False)
    owner = relationship("Mechanic")

class Vehicle(Base):
    __tablename__ = "vehicle"
    vehicle_id = Column(Integer, primary_key=True, nullable=False)
    number_plate = Column(String, nullable=False)
    vehicle_type = Column(String, nullable=False)
    model = Column(String, nullable=False)
    fuel_type = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")



class Work(Base):
    __tablename__ = "work"
    work_id = Column(Integer, primary_key=True, nullable=False)
    day = Column(String, nullable=False)
    time_from = Column(Time, nullable=False)
    time_to = Column(Time, nullable=False)
    mechanic_id = Column(Integer, ForeignKey("mechanic.mechanic_id", ondelete="CASCADE"), nullable=False)
    owner = relationship("Mechanic")