from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_db

def get_database_session(db: Session = Depends(get_db)):
    return db