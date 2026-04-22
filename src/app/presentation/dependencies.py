from fastapi import Depends, HTTPException
import os
from dotenv import load_dotenv
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
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.application.use_cases.user_service import UserService
from app.infrastructure.websocket.connection_manager import ConnectionManager
from app.application.use_cases.notify_service import NotifyService
from app.infrastructure.repositories.detection_repository_impl import DetectionRepositoryImpl
from app.application.use_cases.detection_service import DetectionService
from app.infrastructure.external.medication_vision_inference_impl import MedicationVisionInferenceImpl
from fastapi.security import APIKeyHeader
from jose import JWTError

from app.infrastructure.storage.google_drive_storage import GoogleDriveStorage

api_key_scheme = APIKeyHeader(name="Authorization", auto_error=False)

load_dotenv()
GOOGLE_DRIVE_DRUG_IMAGE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_DRUG_IMAGE_FOLDER_ID")
GOOGLE_DRIVE_DETECTION_IMAGE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_DETECTION_IMAGE_FOLDER_ID")
GOOGLE_SERVICE_ACCOUNT_PATH="service-account.json"

GOOGLE_OAUTH_CREDENTIALS_PATH = os.getenv("GOOGLE_OAUTH_CREDENTIALS_PATH")

manager = ConnectionManager()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_drug_metadata_service(db: Session = Depends(get_db)):
    repo = DrugMetadataRepositoryImpl(db)
    return DrugMetadataService(repo)

def get_google_drive_storage(folder_id: str):
    credentials_path = GOOGLE_OAUTH_CREDENTIALS_PATH
    return GoogleDriveStorage(credentials_path, folder_id)

drug_storage = get_google_drive_storage(GOOGLE_DRIVE_DRUG_IMAGE_FOLDER_ID)
detection_storage = get_google_drive_storage(GOOGLE_DRIVE_DETECTION_IMAGE_FOLDER_ID)

def get_drug_service(db: Session = Depends(get_db)):
    repo = DrugRepositoryImpl(db, drug_storage)    
    return DrugService(repo)

def get_prescription_service(db: Session = Depends(get_db)):
    prescription = PrescriptionRepositoryImpl(db)
    return PrescriptionService(prescription)

def get_user_service(db: Session = Depends(get_db)):
    repo = UserRepositoryImpl(db)
    return UserService(repo)

def get_auth_service(db: Session = Depends(get_db)):
    password = PasswordHasherImpl()
    token = TokenImpl()
    user = UserRepositoryImpl(db)
    return AuthService(password, token, user)

def get_detection_service(db: Session = Depends(get_db)):
    detection_repo = DetectionRepositoryImpl(db, detection_storage)
    prescription_repo = PrescriptionRepositoryImpl(db)
    medication_vision_service = MedicationVisionInferenceImpl(model=None)
    return DetectionService(detection_repo, prescription_repo, medication_vision_service)

def get_notify_service():
    return NotifyService(manager)

def get_current_user_id(
    token: str = Depends(api_key_scheme), 
    auth_service: AuthService = Depends(get_auth_service)
):
    
    try:
        if not token:
            raise HTTPException(status_code=401, detail="Token missing")

        payload = auth_service.decode_access_token(token)

        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return payload.user_id

    except JWTError as e:
        print(f"JWT Error: {str(e)}")
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        raise HTTPException(status_code=400, detail="Bad Request")