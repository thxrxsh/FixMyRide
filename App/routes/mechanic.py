from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models, schemas, utils, database, oauth2
from database import get_db

router = APIRouter(prefix='/mechanic', tags=['Mechanic'])

@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=schemas.MechanicCreated)
def createMechanic(mechanic: schemas.MechanicCreate, db: Session = Depends(get_db)):

    email = db.query(models.Mechanic).filter(models.Mechanic.email == mechanic.email).first()
    if email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Mechanic with Email:{mechanic.email} is alredy exsist")

    hashed_password = utils.hash(mechanic.password)
    mechanic.password = hashed_password

    new_mechanic = models.Mechanic(**mechanic.dict())
    db.add(new_mechanic)
    db.commit()
    db.refresh(new_mechanic)

    return new_mechanic


@router.get('/', status_code=status.HTTP_200_OK,  response_model=schemas.MechanicAccount)
def getMechanicAccount(mechanic: int = Depends(oauth2.getCurrentMechanic), db: Session = Depends(get_db)):
    
    mechanic = db.query(models.Mechanic).filter(models.Mechanic.mechanic_id == mechanic.mechanic_id).first()

    if not mechanic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"mechanic with {mechanic.mechanic_id} does not exist")

    return mechanic



@router.get('/{mechanic_id}', status_code=status.HTTP_200_OK, response_model=schemas.Mechanic)
def getMechanic(mechanic_id: int, db: Session = Depends(get_db)):
    
    mechanic = db.query(models.Mechanic).filter(models.Mechanic.mechanic_id == mechanic_id).first()

    if not mechanic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"mechanic with {mechanic_id} does not exist")

    return mechanic

    
@router.delete('/',status_code=status.HTTP_200_OK)
def deleteMechanic(mechanic_id: int, db: Session = Depends(get_db)):
    
    email = db.query(models.Mechanic.email).filter(models.Mechanic.mechanics_id == mechanic_id).first()

    result = db.query(models.Mechanic).filter(models.Mechanic.mechanics_id == mechanic_id).delete()
    db.commit()

    if result == 1:
        return f"Mechanic account with email : {email} has deleted successfully"

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Something went wrong while deleting the account")