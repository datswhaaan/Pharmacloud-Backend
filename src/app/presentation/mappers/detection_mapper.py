from fastapi import UploadFile
from app.application.dto.detection_dto import DetectionDTO, DetectionListDTO, DetectionInputDTO, DetectionItemInputDTO, DetectionUpdateDTO, DetectionItemUpdateDTO
from app.presentation.schemas.detection_request import DetectionCreateRequest, DetectionUpdateRequest
from app.presentation.schemas.detection_response import DetectionListResponse, DetectionItemResponse, DetectionResponse
from app.presentation.schemas.prescription_response import OrderDrugResponse

def _to_detection_response(dto: DetectionDTO) -> DetectionResponse:
    return DetectionResponse(
                detection_id=dto.detection_id,
                image_url=dto.image_url,
                status=dto.status,
                verified_by=dto.verified_by,
                verified_at=dto.verified_at,
                drug_list=[
                    DetectionItemResponse(
                        t_order_drug_id=drug.t_order_drug_id,
                        detection_item_id=drug.detection_item_id,
                        item_common_name=drug.item_common_name,
                        confidence=drug.confidence,
                        confidence_level=drug.confidence_level,
                        quantity=drug.quantity,
                        unit=drug.unit,
                        is_manually_edited=drug.is_manually_edited,
                        match_type=drug.match_type
                    ) for drug in dto.drug_list 
                ]
            )

def _to_detection_list_response(dto: DetectionListDTO) -> DetectionListResponse:
    return DetectionListResponse(
        order_drugs=[
            OrderDrugResponse(
                t_order_drug_id=od.t_order_drug_id,
                item_common_name=od.item_common_name,
                unit=od.unit,
                quantity=od.quantity
            ) for od in dto.order_drugs
        ],
        detections=[_to_detection_response(d) for d in dto.detections
        ]
    )

def _to_detection_input_dto(order_id: str, request: DetectionCreateRequest) -> DetectionInputDTO:
    return DetectionInputDTO(
        order_id=order_id,
        detections=[
            DetectionItemInputDTO(
                b_item_id=drug.b_item_id,
                confidence=drug.confidence
            ) for drug in request.drug_list
        ]
    )

def _to_detection_update_dto(detection_id: str, request: DetectionUpdateRequest) -> DetectionUpdateDTO:
    return DetectionUpdateDTO(
        detection_id=detection_id,
        status=request.status,
        verified_by=request.verified_by,
        drug_list=[
            DetectionItemUpdateDTO(
                detection_item_id=item.detection_item_id,
                quantity=item.quantity,
                is_checked=item.is_checked
            ) for item in request.drug_list
        ]
    )