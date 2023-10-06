from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
import models, schemas, utils, database, oauth2
from database import get_db


router = APIRouter(prefix='/vehicle', tags=['Vehicle'])



@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Vehicle)
def createVehicle(vehicle: schemas.VehicleCreate, current_user:int = Depends(oauth2.getCurrentUser),  db:Session = Depends(get_db)):

    print(vehicle.number_plate)
    number_plate = db.query(models.Vehicle) .filter(models.Vehicle.number_plate == vehicle.number_plate).first()
    
    if number_plate:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Vehicle with Number plate :{vehicle.number_plate} is alredy exsist")

    new_vehicle = models.Vehicle(**vehicle.dict(), user_id=current_user.user_id)
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)    

    return new_vehicle


@router.get('/', status_code=status.HTTP_200_OK)
def getVehicles(current_user:int = Depends(oauth2.getCurrentUser), db: Session = Depends(get_db)):

    vehicles = db.query(models.Vehicle).filter(models.Vehicle.user_id == current_user.user_id).all()
    
    if not vehicles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You don't have registered any vehicles yet")
    
    return vehicles



@router.get('/{vehicle_id}', status_code=status.HTTP_200_OK, response_model=schemas.Vehicle)
def getVehicles(vehicle_id:int, db: Session = Depends(get_db)):

    vehicle = db.query(models.Vehicle).filter(models.Vehicle.vehicle_id == vehicle_id).first()
    
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle with vehicle_id:{vehicle_id} is not found")

    return vehicle



@router.delete('/{vehicle_id}', status_code=status.HTTP_200_OK)
def deleteVehicle(vehicle_id:int, current_user:int = Depends(oauth2.getCurrentUser), db: Session = Depends(get_db)):
    
    number_plate = db.query(models.Vehicle.number_plate).filter(models.Vehicle.vehicle_id == vehicle_id).first()
    
    if not number_plate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle with vehicle_id:{vehicle_id} is not found")

    result = db.query(models.Vehicle).filter( and_(models.Vehicle.user_id == current_user.user_id, models.Vehicle.vehicle_id == vehicle_id)).delete()
    db.commit()

    if result == 1:
        return f"Vehecle with Number plate : {number_plate[0]} has removed successfully"

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Something Went wrong whiile deleting the account")



    # vehicle = db.query(models.Vehicle).filter(models.Vehicle.user_id == current_user.user_id).all()

    # return vehicle