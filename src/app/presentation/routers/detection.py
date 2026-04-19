from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File
from app.application.use_cases.detection_service import DetectionService
from app.presentation.schemas.detection_request import DetectionCreateRequest
from app.presentation.dependencies import get_detection_service
from app.presentation.mappers.detection_mapper import _to_detection_list_response, _to_detection_input_dto, _to_detection_image_input_dto, _to_detection_response

router = APIRouter(prefix="/detection", tags=["detection"])

@router.get("/{order_id}")
def compare_detections(
    order_id: str,
    service: DetectionService = Depends(get_detection_service),
):
    try:
        detection_comparison = service.compare_detections(order_id)
        return _to_detection_list_response(detection_comparison)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/{order_id}")
def create_detection(
    order_id: str,
    request: str = Form(...),
    image: UploadFile = File(...),
    service: DetectionService = Depends(get_detection_service)
):
    try:
        request_obj = DetectionCreateRequest.model_validate_json(request)

        detection_input_dto = _to_detection_input_dto(order_id, request_obj)
        detection_image_input_dto = _to_detection_image_input_dto(image)

        detection_response = service.create_detection(
            detection_input_dto,
            detection_image_input_dto
        )

        return _to_detection_response(detection_response)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))