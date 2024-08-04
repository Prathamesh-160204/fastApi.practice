from app import models, schemas, oauth2
from sqlalchemy.orm import Session
from app.database import  get_db
from fastapi import FastAPI, Response, status, HTTPException,Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func

router=APIRouter(prefix="/posts",tags=['Posts'])
# @router.get("/",response_model=List[schemas.Post]) for post query 
@router.get("/",response_model=List[schemas.PostOut])
def getPost(db: Session = Depends(get_db), limit:int=6, skip:int=0, search: Optional[str]=""):
    # cursor.execute("""SELECT * FROM posts""")
    # post=cursor.fetchall()#without the fetchall() function we will not get any query
    # post=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    post=db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Given post is not found")
    

    return post


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def createPosts(post:schemas.PostCreate,db: Session = Depends(get_db), current_user:int=Depends(oauth2.get_current_user)):#f-string is not useful here because if user enter any title name such as insert into then it will be difficult for the sql injection
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()#without this line of code database will not be modified
    # new_post=models.Post(title=post.title, content=post.content, published=post.published)
    #if there are millions of field then above syntax is inefficient so for that use below syntax
    # print(current_user)
    new_post=models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)#similar to returning keyword
    return new_post

@router.get("/{id}",response_model=schemas.PostOut)
def getPostById(id:int,db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))#if we remove the comma we will face some serious issue"
    # post=cursor.fetchone()
    post=db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id==models.Post.id,isouter=True).group_by(models.Post.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return post

@router.delete("/delete/{id}")
def deletePost(id:int,db: Session = Depends(get_db), user_id:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id),))
    # deletedPost=cursor.fetchone()
    # conn.commit()
    post=db.query(models.Post).filter(models.Post.id==id)
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    
    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform the actions")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/put/{id}",response_model=schemas.Post)
def updatePost(id:int, updated_post:schemas.PostCreate,db: Session = Depends(get_db), user_id:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s,published=%s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    # updatedPost=cursor.fetchone()
    # conn.commit()
    print(user_id)
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    if post.owner_id != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform the actions")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
