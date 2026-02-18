from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.repositories.drug_metadata_repository_impl import DrugMetadataRepositoryImpl
from app.application.use_cases.drug_metadata_service import DrugMetadataService

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_drug_service(db: Session = Depends(get_db)):
    repo = DrugMetadataRepositoryImpl(db)
    return DrugMetadataService(repo)