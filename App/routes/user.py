from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models, schemas, utils, database, oauth2
from database import get_db

router = APIRouter(prefix='/user', tags=['User'])

@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreated)
def createUser(user: schemas.UserCreate, db: Session = Depends(get_db)):


    email = db.query(models.User).filter(models.User.email == user.email).first()

    if email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with Email:{user.email} is alredy exsist")

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    

    return new_user


@router.get('/',status_code=status.HTTP_200_OK, response_model=schemas.UserAccount)
def getUserAccount(current_user:int = Depends(oauth2.getCurrentUser), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.user_id == current_user.user_id).first()
    if not user:    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with user_id:{user_id} does not exist")

    return user



@router.get('/{user_id}',status_code=status.HTTP_200_OK, response_model=schemas.User)
def getUser(user_id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {user_id} does not exist")

    return user


@router.delete('/',status_code=status.HTTP_200_OK)
def deleteUser(user:int = Depends(oauth2.getCurrentUser), db: Session = Depends(get_db)):
    
    email = db.query(models.User.email).filter(models.User.user_id == user.user_id).first()

    result = db.query(models.User).filter(models.User.user_id == user.user_id).delete()
    db.commit()

    if result == 1:
        return f"user account with email : {email[0]} has deleted successfully"

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Something went wrong while deleting the account")