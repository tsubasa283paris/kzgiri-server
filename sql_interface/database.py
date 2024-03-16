import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# load .env
load_dotenv()
userhost = os.environ.get("DATABASE_USERHOST")

engine = create_engine(
    f"mysql+mysqlconnector://{userhost}/kzgiri",
)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
