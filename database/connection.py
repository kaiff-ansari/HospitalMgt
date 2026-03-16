from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os 
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("db")
engine = create_engine(db_url)

session  = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()