from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File
from app.application.use_cases.detection_service import DetectionService
from app.presentation.schemas.detection_request import DetectionCreateRequest, DetectionUpdateRequest
from app.presentation.dependencies import get_detection_service
from app.presentation.mappers.detection_mapper import _to_detection_list_response, _to_detection_input_dto, _to_detection_response, _to_detection_update_dto

router = APIRouter(prefix="/detection", tags=["detection"])

@router.get("/{order_id}")
def compare_detections(
    order_id: str,
    service: DetectionService = Depends(get_detection_service),
):
    try:
        detection_comparison = service.compare_detections(order_id)
        print(detection_comparison)
        return _to_detection_list_response(detection_comparison)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{detection_id}")
def update_detection(
    detection_id: str,
    request: DetectionUpdateRequest,
    service: DetectionService = Depends(get_detection_service)
):
    try:
        detection_update_dto = _to_detection_update_dto(detection_id, request)
        detection_response = service.update_detection(detection_update_dto)
        return _to_detection_response(detection_response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/{order_id}/infer")
def infer_detection(
    order_id: str,
    image: UploadFile = File(...),
    service: DetectionService = Depends(get_detection_service)
):
    try:
        response = service.detection(order_id, image)
        return _to_detection_response(response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))