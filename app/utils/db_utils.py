from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from app.model.base import Base

load_dotenv()

PASSWORD = os.getenv("MARIADB_ROOT_PWD")
print(PASSWORD)
DATABASE_URL = f'mariadb+mariadbconnector://root:{PASSWORD}@localhost:3306/TM_alchemy'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
