from fastapi import Depends,status,HTTPException,APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import schemas, database,models,utils,oauth2

router=APIRouter()

@router.post("/login",response_model=schemas.Token)
def userRegistration(user_credentials:OAuth2PasswordRequestForm=Depends(), db: Session = Depends(database.get_db)):
    user=db.query(models.UserRegistration).filter(models.UserRegistration.email==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    access_token=oauth2.create_user_token(data={"user":user.id})
    return {"access_token":access_token, "token_type":"bearer"}