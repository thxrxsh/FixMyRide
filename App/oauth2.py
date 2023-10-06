import jwt
from datetime import datetime, timedelta
import schemas, database, models
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from config import Settings

oauth2_schem = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = Settings.secret_key
ALGORITHM = Settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = Settings.access_token_expire_minutes


def createAccessToken(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt



def verifyAccessToken(token: str, credential_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        account_id: str = payload.get('account_id')

        if account_id is None:
            raise credential_exception

        print(account_id)
        token_data = schemas.TokenData(account_id=account_id)


    except:
        raise credential_exception

    return token_data




def getCurrentUser(token: str = Depends(oauth2_schem), db: Session = Depends(database.get_db)):
    
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Coud not validate credentials", headers={"WWW-Authenticate":"Bearer"})

    token = verifyAccessToken(token, credential_exception)

    user = db.query(models.User).filter(models.User.user_id == token.account_id).first()

    return user


def getCurrentMechanic(token: str = Depends(oauth2_schem), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Coud not validate credentials", headers={"WWW-Authenticate":"Bearer"})

    token = verifyAccessToken(token, credential_exception)

    mechanic = db.query(models.Mechanic).filter(models.Mechanic.mechanic_id == token.account_id).first()

    return mechanic