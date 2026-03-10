from fastapi import APIRouter, Depends, HTTPException
from app.application.use_cases.prescription_service import PrescriptionService
from app.presentation.dependencies import get_prescription_service
from app.presentation.mappers.prescription_mapper import _to_prescription_response

router = APIRouter(prefix="/prescriptions", tags=["prescriptions"])

@router.get("/{id}")
def get_prescription(
    id: str,
    service: PrescriptionService = Depends(get_prescription_service),
):
    try:
        prescription = service.get_by_id(id)
        return _to_prescription_response(prescription)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))