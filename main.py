from fastapi import FastAPI
# from fastapi.params import Body
# import psycopg2
# from psycopg2.extras import RealDictCursor
from app import models
from routers import post, user, authentication,vote
from app.database import engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
app=FastAPI()
origin=["https://www.google.com/"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# try:
#     conn= psycopg2.connect(host='localhost',database='fastApi',user='postgres',password='Pass1234',cursor_factory=RealDictCursor)
#     cursor=conn.cursor()
#     print("Database Connection was Successful")
# except Exception as error:
#     print("Connection was unsuccessful")
#     print("Error: ",error)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my API world!!!"} 

