from app import models, schemas, utils
from sqlalchemy.orm import Session
from app.database import  get_db
from fastapi import status, HTTPException,Depends, APIRouter

router=APIRouter(prefix="/users",tags=['Users'])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def userCreate(user:schemas.User,db: Session = Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=models.UserRegistration(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.UserOut)
def getUser(id:int, db: Session = Depends(get_db)):
    get_user=db.query(models.UserRegistration).filter(models.UserRegistration.id==id).first()
    if not get_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id:{id} is not found")
    return get_user