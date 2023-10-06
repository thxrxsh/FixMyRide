from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
import models, schemas, utils, database, oauth2
from database import get_db


router = APIRouter(prefix='/service', tags=['Service'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def CreateService(service: schemas.ServiceCreate, db: Session = Depends(get_db), mechanic: int = Depends(oauth2.getCurrentMechanic)):
    try:
        new_service = models.Service(mechanic_id=mechanic.mechanic_id, **service.dict())
        db.add(new_service)
        db.commit()
        db.refresh(new_service)

    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return f"Service : '{new_service.service}' has successfuly added to your services"


@router.get('/mechanic/{mechanic_id}')
def getServices(mechanic_id: int, db: Session = Depends(get_db)):

    services = db.query(models.Service).filter(models.Service.mechanic_id == mechanic_id).all()
    return services


@router.get('/{service_id}', response_model=schemas.Service)
def getService(service_id: int, db: Session = Depends(get_db)):

    service = db.query(models.Service).filter(models.Service.service_id == service_id).first()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Service with service_id:{service_id} is not found")

    return service



@router.delete('/{service_id}', status_code=status.HTTP_200_OK)
def deleteService(service_id:int, current_mechanic:int = Depends(oauth2.getCurrentMechanic), db: Session = Depends(get_db)):
    
    service_title = db.query(models.Service.service).filter(models.Service.service_id == service_id).first()
    
    if not service_title:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"service with service_id:{service_id} is not found")

    result = db.query(models.Service).filter( and_(models.Service.mechanic_id == current_mechanic.mechanic_id, models.Service.service_id == service_id)).delete()
    db.commit()

    if result == 1:
        return f"Service with title : '{service_title[0]}' has removed successfully"

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Something Went wrong while removing the service")


