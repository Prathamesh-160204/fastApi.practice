from jose import jwt,JWTError
from datetime import datetime,timedelta
from app import schemas, database,models
from fastapi import Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import config
#JWT REQUIRES 3 PARAM SCRET_KEY, ALGORITHM, AND EXPIRATIONTIME(THE TIMW TILL TOKEN IS VALID)
SECRET_KEY = config.setting.secret_key
ALGORITHM = config.setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.setting.access_token_expire_minutes

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')
def create_user_token(data:dict):
    to_encode=data.copy()

    expire=datetime.utcnow()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = str(payload.get("user"))

        if id is None:
            raise credentials_exception
        token_data=schemas.TokenOut(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    token= verify_access_token(token,credentials_exception)
    user=db.query(models.UserRegistration).filter(models.UserRegistration.id==token.id).first()
    return user