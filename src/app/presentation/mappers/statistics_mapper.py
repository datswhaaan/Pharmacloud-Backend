from app.application.dto.statistics_dto import DetectionLogDTO, DetectionLogItemDTO
from app.presentation.schemas.statistics_response import DetectionLogResponse, DetectionLogItemResponse

def _to_detection_log_item_response(log: DetectionLogItemDTO) -> DetectionLogItemResponse:
    return DetectionLogItemResponse(
        detection_id=log.detection_id,
        visit_hn=log.visit_hn,
        visit_vn=log.visit_hn,
        patient_name=log.patient_name,
        status=log.status,
        verified_by=log.verified_by,
        verified_at=log.verified_at
    )

def _to_detection_log_response(detection: DetectionLogDTO) -> DetectionLogResponse:
    return DetectionLogResponse(
        detections=[_to_detection_log_item_response(log) for log in detection.detections],
        total=detection.total,
        page=detection.page,
        size=detection.size
    )