from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app import config

# SQLALCHEMY_DATABASE_URL='postgresql://<username>:<password>@<ip-address>/hostname/<database_name>'
SQLALCHEMY_DATABASE_URL=f'postgresql://{config.setting.database_username}:{config.setting.database_password}@{config.setting.database_hostname}:{config.setting.database_port}/{config.setting.database_name}'
postgresql://render_devhobby_user:eiKVk96fRVYE3mWG7dOx7R40jLcJ4KgF@dpg-cqoc9hrv2p9s73ang990-a.oregon-postgres.render.com/render_devhobby

engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()