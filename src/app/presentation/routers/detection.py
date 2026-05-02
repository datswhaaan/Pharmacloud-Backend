from PIL import Image
import io
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File
from app.application.use_cases.detection_service import DetectionService
from app.presentation.schemas.detection_request import DetectionCreateRequest, DetectionUpdateRequest
from app.presentation.dependencies import get_detection_service
from app.presentation.mappers.detection_mapper import _to_detection_list_response, _to_detection_infer_response, _to_detection_response, _to_detection_update_dto, _to_detection_image_input_dto
from app.presentation.dependencies import get_current_user_id

router = APIRouter(prefix="/detection", tags=["detection"],
    dependencies=[Depends(get_current_user_id)])

@router.get("/{order_id}")
def get_order_and_detections_by_order_id(
    order_id: str,
    service: DetectionService = Depends(get_detection_service),
):
    try:
        detection_comparison = service.get_order_and_detections_by_order_id(order_id)
        return _to_detection_list_response(detection_comparison)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{detection_id}")
def update_detection(
    detection_id: str,
    request: DetectionUpdateRequest,
    verified_by: str = Depends(get_current_user_id),
    service: DetectionService = Depends(get_detection_service)
):
    try:
        detection_update_dto = _to_detection_update_dto(detection_id, verified_by, request)
        detection_response = service.update_detection(detection_update_dto)
        return _to_detection_response(detection_response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/{order_id}/infer")
async def infer_detection(
    order_id: str,
    image: UploadFile = File(...),
    service: DetectionService = Depends(get_detection_service)
):
    try:
        if image.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Invalid file type")

        image_bytes = await image.read()

        img = Image.open(io.BytesIO(image_bytes))
        if img.format not in ["JPEG", "PNG"]:
            raise HTTPException(status_code=400, detail="Invalid image content")
        
        image_input_dto = _to_detection_image_input_dto(image_bytes, image.content_type)

        response = service.detection(order_id, image_input_dto)

        return _to_detection_infer_response(response)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))