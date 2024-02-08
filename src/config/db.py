import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

engine = create_engine(f'{os.environ["DB_MANAGER"]}://{os.environ["DB_USERNAME"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_URL"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}')
db = Session(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
