from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import database, schemas, models, utils, oauth2

router = APIRouter(prefix='/login', tags=['Authentication'])

@router.post('/user', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")


    access_token = oauth2.createAccessToken(data={"account_id": user.user_id})

    return {"access_token": access_token, "token_type":"bearer"}




@router.post('/mechanic', response_model=schemas.Token)
def login(mechanic_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    mechanic = db.query(models.Mechanic).filter(models.Mechanic.email == mechanic_credentials.username).first()

    if not mechanic:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(mechanic_credentials.password, mechanic.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")


    access_token = oauth2.createAccessToken(data={"account_id": mechanic.mechanic_id})

    return {"access_token": access_token, "token_type":"bearer"}

