from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.db.database import SessionLocal
from app.infrastructure.repositories.drug_metadata_repository_impl import DrugMetadataRepositoryImpl
from app.infrastructure.repositories.drug_repository_impl import DrugRepositoryImpl
from app.application.use_cases.drug_metadata_service import DrugMetadataService
from app.application.use_cases.drug_service import DrugService
from app.infrastructure.repositories.prescription_repository_impl import PrescriptionRepositoryImpl
from app.application.use_cases.prescription_service import PrescriptionService
from app.application.use_cases.auth_service import AuthService
from app.infrastructure.security.password_hasher_impl import PasswordHasherImpl
from app.infrastructure.security.token_impl import TokenImpl
from fastapi.security import APIKeyHeader
from jose import JWTError

api_key_scheme = APIKeyHeader(name="Authorization", auto_error=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_drug_metadata_service(db: Session = Depends(get_db)):
    repo = DrugMetadataRepositoryImpl(db)
    return DrugMetadataService(repo)

def get_drug_service(db: Session = Depends(get_db)):
    repo = DrugRepositoryImpl(db)
    return DrugService(repo)

def get_prescription_service(db: Session = Depends(get_db)):
    repo = PrescriptionRepositoryImpl(db)
    return PrescriptionService(repo)

def get_auth_service():
    return AuthService(password = PasswordHasherImpl(), token = TokenImpl())

def get_current_user_email(
        token: str = Depends(api_key_scheme),
        auth_service: AuthService = Depends(get_auth_service)
    ):
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")
    try:
        payload = auth_service.decode_access_token(token)

        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {
            "email": payload.email,
            "role": payload.role
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")