from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
import models, schemas, utils, database, oauth2
from database import get_db


router = APIRouter(prefix='/work', tags=['Work TIme'])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Work)
def createWork(work: schemas.WorkCreate, current_mechanic:int = Depends(oauth2.getCurrentMechanic),  db:Session = Depends(get_db)):

    day = db.query(models.Work).filter(models.Work.day == work.day).first()
    
    if day:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"work time of '{work.day} is alredy exsist")

    new_work = models.Work(**work.dict(), mechanic_id=current_mechanic.mechanic_id)
    
    db.add(new_work)
    db.commit()
    db.refresh(new_work)    

    return new_work


@router.get('/{mechanic_id}', status_code=status.HTTP_200_OK)
def getWorks(mechanic_id:int, db: Session = Depends(get_db)):

    works = db.query(models.Work).filter(models.Work.mechanic_id == mechanic_id).all()

    if not works:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Didn't found any work times")

    return works
    

@router.delete('/{day}', status_code=status.HTTP_200_OK)
def deleteWorkTime(day: str, mechanic: int = Depends(oauth2.getCurrentMechanic), db: Session = Depends(get_db)):

    result = db.query(models.Work).filter( and_(models.Work.day == day, models.Work.mechanic_id == mechanic.mechanic_id)).delete()
    db.commit()
    if result == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You don't have any work time on {day}")

    return f"{day} has successfuly removed from your work time."