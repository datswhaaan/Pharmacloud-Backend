from fastapi import APIRouter, Depends, HTTPException
from app.application.use_cases.prescription_service import PrescriptionService
from app.presentation.dependencies import get_prescription_service
from app.presentation.mappers.prescription_mapper import _to_prescription_response, _to_prescription_list_response, _to_detection_list_response

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

@router.get("/")
def get_all_prescriptions(
    start_time: str | None = None,
    end_time: str | None = None,
    limit: int = 10,
    skip: int = 0,
    order: str = "desc",
    search: str | None = None,
    status: str | None = None,
    service: PrescriptionService = Depends(get_prescription_service),
):
    try:
        prescription_list = service.get_all(start_time, end_time, limit, skip, order, status, search)
        return _to_prescription_list_response(prescription_list)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/compare/{order_id}")
def compare_detections(
    order_id: str,
    service: PrescriptionService = Depends(get_prescription_service),
):
    try:
        detection_comparison = service.compare_detections(order_id)
        return _to_detection_list_response(detection_comparison)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))