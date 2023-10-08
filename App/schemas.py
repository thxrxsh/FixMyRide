from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime, time
from typing import Optional
from pydantic.types import conint

class UserCreate(BaseModel):
    name: str
    email: str
    mobile: str
    password: str


class UserCreated(BaseModel):
    user_id: int
    email: str

class UserLogin(BaseModel):
    email: str
    password: str

class User(BaseModel):
    user_id: int
    name: str
    mobile: str

class UserAccount(BaseModel):
    user_id: int
    email: str
    name: str
    mobile: str

class VehicleCreate(BaseModel):
    number_plate: str
    vehicle_type: str
    model: str
    fuel_type: str

class Vehicle(BaseModel):
    vehicle_id: int
    user_id: int
    number_plate: str
    vehicle_type: str
    model: str
    fuel_type: str


# class Vehicles(BaseModel):
#     Vehicles : List[Vehicle]


class MechanicCreate(BaseModel):
    name: str
    email: str
    mobile: str
    password: str
    address: str
    location: str
    district: str
    province: str
    country: str

class MechanicCreated(BaseModel):
    mechanic_id: int
    email: str

class MechanicLogin(BaseModel):
    email: str
    password: str

class Mechanic(BaseModel):
    mechanic_id: int
    name: str
    address: str
    location: str
    mobile: str
    rating_count: Optional[int] 
    rating_total: Optional[int] 

class MechanicAccount(BaseModel):
    mechanic_id: int
    name: str
    email: str
    address: str
    location: str
    mobile: str
    rating_count: Optional[int] 
    rating_total: Optional[int] 


class ServiceCreate(BaseModel):
    vehicle_type: str
    service: str
    price: Optional[float]

class Service(BaseModel):
    service_id: int
    service: str
    mechanic_id: int
    vehicle_type: str
    price: Optional[float]
    rating_count: Optional[int]
    rating_total: Optional[int]

    # module_config = ConfigDict(orm_mode=True)

class WorkCreate(BaseModel):
    day: str
    time_from: time
    time_to: time  

class Work(BaseModel):
    work_id: int
    mechanic_id: int
    day: str
    time_from: time
    time_to: time


class MapFilter(BaseModel):
    filter_type: str
    location: str
    country: str
    province: str
    district: str
    radius: int
    vehicle_type: str
    model: str
    fuel_type: str
    service: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    account_id: Optional[int] = None
